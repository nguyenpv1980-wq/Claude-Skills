---
name: horizontal-scalability-reviewer
description: 'Review whether a system can scale OUT (add nodes) rather than only up — a can-it-scale-horizontally lens: statelessness / session and in-memory-state externalization, connection pooling and connection-count ceilings, sticky-session and in-process-singleton / local-cache / local-cron / local-filesystem smells, autoscaling + load-balancer + health-check config, and graceful shutdown/draining so scale-in does not drop work. Produces a scale-out readiness verdict with component/file findings ranked by blast radius and a remediation order. Use when reviewing readiness to run multiple instances or autoscale, when adding a second node breaks things, or when "it works on one box" must become many. Do NOT use to SET reliability targets (slo-reliability-architect), allocate a LATENCY budget (latency-budget-architect), or design the CACHE (caching-strategy-designer) — this reviews scale-out readiness and defers those.'
---

# Horizontal Scalability Reviewer

## Purpose

A system that runs fine on one box can fail the instant a second box joins
it: sessions live in local memory so half the requests log the user out,
a scheduled job fires on every node instead of once, a local write-through
cache goes stale per-node, an in-process counter under-counts, and a
scale-in drops the connections and jobs a draining node was holding. This
skill reviews a system for those failure modes BEFORE they become a 2 a.m.
incident: it hunts the state and singletons that assume one instance,
checks the connection-pool and load-balancer/health-check config, and
verifies graceful drain. The deliverable is a scale-out readiness verdict —
per-finding, with the file/component, the failure it causes when instances
multiply, blast radius, and a remediation order. It reviews readiness; it
does not set the targets, the latency budget, or design the cache those
findings may point to.

## Use When

- Use when: reviewing whether a service is ready to run as multiple
  instances or under an autoscaler — before turning on horizontal scaling.
- Use when: adding a second (or Nth) instance breaks something — users get
  logged out intermittently, a job runs N times, a cache is inconsistent
  across nodes, counts are wrong.
- Use when: "it works on one server" must become "it works on many," or a
  monolith/instance is being prepared to scale out.
- Use when: an autoscaling / load-balancer / graceful-drain configuration
  needs a scale-out-correctness review (not a cost review).
- Do NOT use when: the task is to SET reliability/availability targets or
  error budgets — that is `slo-reliability-architect`; this review may find
  scale-out gaps that threaten those targets, but it does not define them.
- Do NOT use when: the task is to allocate an end-to-end LATENCY budget
  across hops — that is `latency-budget-architect`.
- Do NOT use when: the task is to DESIGN caching (what to cache, TTLs,
  invalidation) — that is `caching-strategy-designer`; this review flags a
  node-LOCAL cache as a scale-out smell and hands the redesign over.
- Do NOT use when: the question is whether to shard the DATA layer for write
  throughput — that is data partitioning/sharding (a separate concern), not
  stateless-app scale-out.

## Inputs to Inspect

1. The deployment shape: how many instances run today, behind what load
   balancer, with what health check, and whether autoscaling is on or planned.
2. Session/auth handling: where session state lives (in-memory, sticky
   cookie, external store), and whether any request assumes it lands on the
   same node as a prior one.
3. In-process state: caches, counters, rate-limiter state, feature-flag
   caches, singletons, and anything held in a module-level variable across
   requests.
4. Scheduled work: cron/timers running inside the app process — do they fire
   once cluster-wide or once per node?
5. Connection management: DB/cache/queue connection pools, their per-instance
   size, and the total against the datastore's connection ceiling when
   instances multiply.
6. Local resources: filesystem writes, local temp files, uploads written to
   local disk, in-memory websockets/connections, and anything not shared
   across nodes.
7. Shutdown behavior: what happens to in-flight requests, jobs, and
   connections when a node is terminated (deploy, scale-in, spot reclaim).

## Workflow

1. **Establish the target topology.** N instances, autoscaled or fixed,
   behind which LB, with which health check. The review is against "many
   instances of this run concurrently and are added/removed at any time."
2. **Hunt state that assumes one instance.** For each of session/auth,
   caches, counters, rate-limiter state, and any module-level mutable state:
   does correctness depend on the same node serving related requests? Flag
   each with the concrete failure when it does not (logout, stale read,
   under-count, bypassed limit).
3. **Hunt singletons that must run once, not N times.** In-process cron,
   startup migrations, leader-only work, cache-warmers: on N nodes they run
   N times unless coordinated. Flag each and note the coordination need
   (external scheduler, leader election, advisory lock).
4. **Check sticky-session reliance.** Sticky sessions can paper over local
   state — but a node death loses that state and pins load unevenly. Flag
   stickiness used as a correctness crutch (vs a legitimate connection
   affinity) and point at session externalization.
5. **Check connection ceilings.** Per-instance pool size × max instances vs
   the datastore/cache/queue connection limit. Autoscaling that multiplies
   connection pools can exhaust the database's connection cap and take the
   whole fleet down — flag the ceiling and recommend a pooler/proxy if the
   math breaks.
6. **Check local-resource assumptions.** Filesystem writes, local upload
   staging, local temp that a later request on another node expects to find:
   flag as needing shared storage (hand file/upload redesign to
   `file-upload-storage-architect`).
7. **Check graceful drain.** On termination: does the node deregister from
   the LB, stop taking new work, finish or safely hand off in-flight
   requests/jobs/connections, within a bounded grace period? A missing drain
   drops user requests and in-flight jobs on every deploy. Verify readiness/
   liveness probes distinguish "starting" from "healthy" from "draining."
8. **Rank findings by blast radius and deliver the verdict.** Each finding:
   component/file, the scale-out failure it causes, blast radius (silent
   data wrongness > dropped work > uneven load), and remediation. Defer:
   targets → `slo-reliability-architect`; latency → `latency-budget-architect`;
   cache design → `caching-strategy-designer`.

## Output Format

```
HORIZONTAL SCALABILITY REVIEW — <service/system>
Target topology: <N instances, autoscale y/n, LB, health check>
Verdict: <READY | READY-WITH-FIXES | NOT-READY> for scale-out
Findings (ranked by blast radius):
  [BLOCKER|HIGH|MED|LOW] <component/file:line> — <state/singleton/pool/local/drain>
    scale-out failure: <what breaks when instances multiply / churn>
    remediation: <externalize / coordinate-once / pool-proxy / shared-store / drain>
Connection ceiling: <pool × instances vs datastore cap — OK | AT RISK>
Graceful drain: <present/absent; deregister → stop-new → finish/handoff → grace>
Deferrals: targets → slo-reliability-architect; latency → latency-budget-architect;
  cache design → caching-strategy-designer; file storage → file-upload-storage-architect
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Session/auth state is externalized or the review flags where it is not,
      with the concrete failure (intermittent logout) named.
- [ ] Every in-process cache/counter/limiter/singleton is checked for
      single-instance assumptions; scheduled work is checked for run-once-vs-
      run-N-times.
- [ ] Sticky-session reliance is distinguished from legitimate affinity and
      flagged where it is a correctness crutch.
- [ ] Connection-ceiling math (pool × max instances vs datastore cap) is
      done, not assumed; a breaking ceiling is a BLOCKER.
- [ ] Local-filesystem / local-upload assumptions are flagged for shared
      storage.
- [ ] Graceful drain is verified: deregister, stop-new, finish/handoff,
      bounded grace, and correct readiness/liveness semantics.
- [ ] Findings are ranked by blast radius, with silent data-wrongness above
      dropped-work above uneven-load.
- [ ] Targets, latency budgets, and cache design are deferred to their owning
      skills, not invented here.

## Gotchas

- The most dangerous scale-out bug is silent, not loud: an under-counting
  in-memory rate limiter or a per-node stale cache produces WRONG answers,
  not errors — no alarm fires while the data quietly rots.
- In-process cron on an autoscaled fleet fires the "nightly" job once per
  node per night; on 8 nodes that is 8 charges / 8 emails / 8 rollups.
- Sticky sessions are not high availability: they pin a user to a node, and
  when that node dies the user's session dies with it. Stickiness hides the
  state problem until the worst moment.
- Autoscaling can DOS your own database: each new app instance opens a pool,
  and at max scale the pools exceed the DB's connection limit — the fleet
  scales up and the database falls over.
- A local write-through cache is correct on one node and inconsistent on
  many; node A updates its cache and node B keeps serving the old value.
- No graceful drain means every deploy is a mini-outage: in-flight requests
  and jobs on the terminated node are dropped. Zero-downtime deploy is a
  drain property, not a wish.
- "We'll just use sticky sessions / one big box" is vertical scaling wearing
  a horizontal costume — say so, and point at the state that must move.

## Stop Conditions

- The intended target topology (how many instances, autoscaled or not, what
  LB) is unknown → obtain it before reviewing; "ready to scale out" is
  meaningless without the topology it must be ready for.
- A finding's fix requires SETTING an availability/error-budget target to
  decide acceptable drop/degradation → hand the target decision to
  `slo-reliability-architect`; do not invent the SLO to justify the fix.
- The real problem is write-throughput at the data layer (needs
  partitioning/sharding), not stateless-app scale-out → say so and route to
  the data-partitioning concern; this review does not shard databases.
- Asked to APPLY the fixes to a live system (change LB/autoscaler config,
  externalize sessions in production) → this skill REVIEWS and recommends;
  executing infra changes follows the repo's approval path.

## Supporting Files

- `evals/evals.json` — behavior cases: the pre-scale-out readiness review,
  the in-memory-singleton / run-N-times edge, the connection-ceiling catch,
  and the SLO-setting non-trigger.
- `evals/trigger-evals.json` — discrimination against
  `slo-reliability-architect` (targets), `latency-budget-architect` (latency
  allocation), and `caching-strategy-designer` (cache design).
- No `references/` — the state/singleton/pool/drain checklist above is the
  complete review procedure; findings live in the produced verdict.
