---
name: latency-budget-architect
description: 'Decompose an end-to-end latency target into per-hop engineering budgets — map the path (edge → gateway → services → stores → third parties), allocate milliseconds per hop including the overhead nobody budgets (serialization, queue wait, connection setup, retries), do the tail math honestly (percentiles do not add; fan-out exposes a dependency''s tail at 1-(0.99)^N), derive timeouts and retries FROM budgets instead of folklore, keep explicit headroom, and define violation attribution plus the rule that a new dependency on the path must claim budget. CONSUMES the journey target from slo-reliability-architect (or flags its assumption loudly): SLOs say what users must experience and when to page; budgets say which component may spend which milliseconds. Use when allocating a latency target across services, deriving timeouts/retries, or when end-to-end latency has no per-hop owner. Do NOT use to set SLOs/error budgets or alerting (slo-reliability-architect), or to measure (performance-test-harness).'
---

# Latency Budget Architect

## Purpose

Every service on the path believes it is fast enough, and the user
experiences the sum: 40ms of gateway, 60ms of auth, 120ms of service
time, 80ms of database, 90ms of serialization nobody counted, and a
retry — 700ms against a 300ms promise, with no component at fault
because no component ever owned a number. This skill turns an
end-to-end latency target into per-hop budgets: an explicit allocation
of milliseconds per component, tail-composition math done honestly,
timeouts and retry policies derived from the budgets they must respect,
headroom held in reserve, and an attribution method so a violated
budget names its hop. The target itself comes from the user-journey SLO
(`slo-reliability-architect`) — this skill engineers the spend plan
that makes the target achievable by design rather than by hope.

## Use When

- Use when: an end-to-end latency target (from an SLO, a contract, or
  a product requirement) needs decomposing into component-level
  budgets that teams can own and be reviewed against.
- Use when: timeouts and retry policies are folklore (30-second
  defaults, retry-everything) and need deriving from an actual budget.
- Use when: a new dependency is entering a latency-sensitive path and
  the question is what it may cost — the budget-claim review.
- Use when: fan-out amplification (parallel calls to N shards or
  services) needs its tail math checked against the end-to-end
  promise.
- Use when: end-to-end latency degraded and no hop admits ownership —
  the attribution design (which hop blew its budget) is missing.
- Do NOT use when: the question is what the TARGET should be, which
  journeys matter, what pages an operator, or how error budgets govern
  release velocity — that is `slo-reliability-architect`; this skill
  starts from its output (or states an assumed target loudly and
  flags it for ratification).
- Do NOT use when: building the measurement instrument — pass/fail
  latency measurement, baselines, and regression gates are
  `performance-test-harness`; budgets become its thresholds.
- Do NOT use when: the work is implementing trace instrumentation or
  dashboards — `observability-operator` wires what this design
  requires.
- Do NOT use when: a specific hop needs its time reduced — that is
  the owning skill's job (`query-plan-reader` for a query,
  `caching-strategy-designer` for a cache, `frontend-perf-engineer`
  for the browser share); this skill decides how much time the hop
  MAY spend, not how it gets there.

## Inputs to Inspect

1. The end-to-end target and its provenance: the SLO catalog entry
   (`slo-reliability-architect` output), contract clause, or product
   requirement — with its percentile (a p50 budget and a p99 budget
   are different documents; know which is being allocated).
2. The request path, as it actually is: every hop a request traverses
   — edge/CDN, gateway, auth, services, databases/caches, queues,
   third parties — from trace data where it exists, architecture docs
   where it doesn't (and mark the doc-only hops as unverified).
3. Current per-hop reality: measured per-hop latency distributions
   (p50/p95/p99) from traces or logs — the budget negotiates with
   reality, not with wishes.
4. Fan-out and serialization structure: which calls are parallel,
   which serial, where responses assemble — the composition math
   depends on the shape.
5. Existing timeout/retry configuration per hop: what is set today,
   where the defaults came from, and where retries can multiply
   (retry storms at two layers compound).
6. The frontend share, if the target is user-perceived: how much of
   the budget the browser consumes (render, hydration) — allocated
   with `frontend-perf-engineer`'s metrics vocabulary.

## Workflow

1. **Fix the target and its percentile.** One budget document per
   percentile that matters (typically p95 or p99 user-perceived).
   If no ratified target exists, state the assumption in the header
   ("ASSUMED 300ms p95 — requires slo-reliability-architect
   ratification") — an assumed target produces a real budget with a
   flagged foundation, never a silent one.
2. **Map the path and its composition shape.** Serial chains ADD.
   Parallel fan-out composes at the SLOWEST branch — and the tail
   math is where designs lie to themselves: hitting N parallel
   dependencies, the request experiences a dependency's p99 with
   probability 1-(0.99)^N — at N=10, roughly one request in ten rides
   a tail. Fan-out on the path means per-branch budgets must be set
   at a stricter percentile than the end-to-end promise.
3. **Allocate the budget per hop.** Start from measured reality
   (input 3), assign each hop a number, and include the overhead rows
   folklore omits: serialization/deserialization, connection
   establishment (cold pools, TLS), queue wait under load, and ONE
   retry of the most-likely-to-retry hop. The sum of allocations plus
   headroom equals the target — arithmetic that must visibly close.
4. **Hold headroom explicitly.** 15–25% of the target stays
   unallocated — for growth, incident conditions, and the dependency
   nobody predicted. Headroom is a line item with an owner (the path
   owner), not slack silently absorbed by whoever asks first.
5. **Derive timeouts from budgets.** A hop's timeout ≈ its budget
   (plus a stated tolerance), because a timeout longer than the
   budget means the caller has already failed the end-to-end promise
   while still waiting. Cascade correctly: an upstream timeout must
   exceed the sum of its downstream's timeout × retries, or the
   upstream gives up while the downstream still works. The 30-second
   default is a bug in a 300ms path.
6. **Derive retry policy from what the budget affords.** Retries
   spend budget: one retry of a 50ms hop costs 50ms+backoff from
   SOMEONE's allocation. State which hops may retry (idempotent
   ones), how many times (usually one, at the innermost layer only —
   two layers retrying compounds into storms), and hedging only where
   the budget's headroom explicitly funds it.
7. **Design violation attribution.** Per-hop spans with the budget
   annotated (trace attribute or naming convention), so "the p95
   regressed" decomposes into "hop X exceeded its 40ms by 60ms" —
   wiring via `observability-operator`; pre-release verification of
   budgets via `performance-test-harness` gates where they exist.
8. **Install the budget-claim review rule.** A new dependency, new
   hop, or new work on a budgeted path claims budget in the design
   review: from headroom (path owner signs), from another hop
   (that owner signs), or the end-to-end target is renegotiated
   (`slo-reliability-architect` loop). Unclaimed spend is how 300ms
   paths become 700ms paths one PR at a time.
9. **Deliver** in the Output Format: the budget table whose
   arithmetic closes, timeout/retry derivations, attribution design,
   and the review rule — with per-hop owners named.

Tail-composition math, the overhead-rows checklist, timeout-cascade
worksheet, and the budget-claim review template:
[references/tail-math-worksheet.md](references/tail-math-worksheet.md).

## Output Format

```
LATENCY BUDGET — <path/journey> @ <percentile>
Target: <N ms p<XX>> — provenance: <SLO ref | contract | ASSUMED (flagged for ratification)>
Path & shape: <hop chain; parallel sections marked; fan-out N noted>
Budget table:
  <hop>: <ms> — owner=<team/role> — current=<measured pXX> — notes=<incl. overhead rows>
  serialization/connection/queue-wait rows: <ms each>
  retry allowance: <hop, count, backoff — funded from whose budget>
  HEADROOM: <ms (15–25%)> — owner=<path owner>
  SUM CHECK: allocations + headroom = target ✓
Tail math: <fan-out branches budgeted at p<stricter> because 1-(0.99)^N = <exposure>>
Timeouts: <per hop: timeout ≈ budget + tolerance; cascade check upstream ≥ downstream×retries+ε>
Retries:  <which hops, innermost-layer-only rule, hedging iff headroom-funded>
Attribution: <span/budget annotation convention → observability-operator;
              pre-release check → performance-test-harness>
Review rule: new dependency on this path claims budget (headroom | reallocation | renegotiate SLO)
Reduction work routed: <hop over budget today → owning skill (query-plan-reader | caching-strategy-designer | frontend-perf-engineer | ...)>
```

## Validation Checklist

- [ ] The target's percentile is stated and singular per document; the
      provenance is an SLO ref or a LOUD assumption flag.
- [ ] The budget table's arithmetic closes: allocations + headroom =
      target, visibly.
- [ ] Overhead rows exist (serialization, connections, queue wait) —
      the budget that omits them is fiction by construction.
- [ ] Fan-out sections carry the tail-exposure calculation and
      stricter per-branch percentiles.
- [ ] Every timeout derives from a budget and the cascade check passes
      (upstream ≥ downstream × retries + ε).
- [ ] Retries are budgeted spend at one layer only; hedging is
      headroom-funded or absent.
- [ ] Headroom is a named line item with an owner, 15–25%.
- [ ] Every hop has an owner; hops over budget today have their
      reduction work ROUTED, not absorbed into this design.
- [ ] The budget-claim review rule is stated.

## Gotchas

- Percentiles don't add: p99(A)+p99(B) is not p99(A+B) — summing
  per-hop p99s overbudgets the path; budgeting hops at p50 while
  promising p99 underbudgets it catastrophically. Budget per-hop at
  the percentile the composition math requires, and say which.
- The fan-out tail trap: ten parallel 20ms calls feel like 20ms until
  the p99 math (1-(0.99)^10 ≈ 9.6%) puts a tail on one in ten
  requests. Wide fan-out paths need per-branch budgets at p99.9-class
  strictness or a hedging strategy the headroom funds.
- Serialization is a hop: JSON encode/decode of a fat payload can
  cost more than the service call it wraps — and it appears in no
  service's dashboard because it happens in the caller. The overhead
  rows exist because the unmeasured milliseconds are still spent.
- Timeout inversion: an upstream 2s timeout over a downstream
  3s-timeout×2-retries path means the upstream abandons work the
  downstream completes — wasted load AND a failed request. The
  cascade check is mechanical; run it.
- Two-layer retries compound: the gateway retries twice, the client
  library retries twice — one flaky hop becomes 4× load and a storm.
  Retries live at ONE stated layer (usually innermost idempotent).
- Queue wait is invisible until it isn't: async hops budgeted at
  processing time only will blow their budget under load exactly when
  it matters — queue wait at target load is a budget row.
- The budget negotiated against wishes: allocating 20ms to a hop
  currently measuring p95=80ms is not a budget, it's a hope — the
  gap becomes ROUTED reduction work (the owning skill) or the
  allocation is honest about today.
- Cold connections on the tail: pool exhaustion and TLS setup land on
  exactly the requests already unlucky — tail budgets include
  connection establishment or the p99 promise excludes cold starts
  explicitly.

## Stop Conditions

- No end-to-end target exists and none can be assumed responsibly
  (no SLO, no contract, no product number) → stop; route target-
  setting to `slo-reliability-architect`. A budget without a target
  is allocation theater.
- Asked to SET the SLO, define error budgets, or design paging as
  part of the budget work → decline that slice; that is
  `slo-reliability-architect`'s scope, and doing it here forks the
  reliability source of truth.
- The measured reality exceeds the target before allocation begins
  (the path is already slower than the promise) → present the honest
  gap and stop for a decision: renegotiate the target (SLO loop) or
  commission the reduction work (routed to owning skills) — a budget
  cannot be arithmetic'd into existence.
- Per-hop measurements don't exist and the path map is doc-only →
  deliver only a provisional budget marked as such, with the tracing
  gap named as the first work item (via `observability-operator`);
  refuse to present a doc-derived budget as engineering truth.
- A third-party dependency's latency distribution is outside the
  budget and cannot be bounded (no SLA, observed tail beyond the
  whole target) → surface the structural conflict for a human
  decision (remove from path, make async, accept the miss rate) —
  do not bury an unbudgetable hop inside a closing table.

## Supporting Files

- [references/tail-math-worksheet.md](references/tail-math-worksheet.md)
  — tail-composition math with worked fan-out examples, the
  overhead-rows checklist, timeout-cascade worksheet, retry-spend
  accounting, and the budget-claim review template.
- `evals/evals.json` — behavior cases including the fan-out tail edge
  and the refuse-to-invent-the-SLO case.
- `evals/trigger-evals.json` — discrimination against
  `slo-reliability-architect` (THE seam), `performance-test-harness`,
  `observability-operator`, and the per-hop reduction skills.
