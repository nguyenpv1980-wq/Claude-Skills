---
name: background-job-orchestration-architect
description: 'Design the async job/worker EXECUTION model for a multi-tenant SaaS — offload slow work off the request path: worker pools, scheduled/cron jobs, job idempotency + resumability/checkpointing, retry with backoff, a job dead-letter queue, visibility timeouts, and per-tenant fairness so one tenant''s flood cannot starve others. Produces the job catalog, the execution/retry/DLQ contract, and a fairness + scaling plan. Use when moving slow work out of the request, adding scheduled jobs, or when jobs run twice, never finish, or one tenant''s backlog starves everyone. This is EXECUTION (what RUNS the work); the message TRANSPORT (topics, partitions, delivery semantics, CDC) is streaming-event-architect. Do NOT use to MEASURE throughput/latency under load (performance-test-harness / load-test-planner) or to design the internal event backbone (streaming-event-architect).'
---

# Background Job Orchestration Architect

## Purpose

Work that outlives a request — sending a batch of emails, generating an
export, processing an upload, running a nightly rollup — belongs off the
request path, and once it is off it needs its own execution discipline:
workers that pick jobs up, retry the transient failures, dead-letter the
poison ones, resume the half-done ones after a crash, and share capacity
fairly so one tenant's ten-thousand-job flood does not starve every other
tenant's single job. This skill designs that execution model: the job
catalog, the per-job execution contract (idempotency, retry, backoff,
visibility timeout, DLQ, checkpointing), and a per-tenant fairness and
scaling plan. It owns what RUNS the work. The queue/stream the jobs travel
on — its topics, partitions, and delivery semantics — is transport, and
transport belongs to `streaming-event-architect`.

## Use When

- Use when: moving slow or bursty work off the request path — exports,
  media/file processing, bulk email/notifications, third-party sync, report
  generation — into asynchronous jobs.
- Use when: adding scheduled/cron/recurring jobs (nightly rollups, cleanup,
  reminders) and they need idempotency, overlap prevention, and missed-run
  handling.
- Use when: jobs misbehave — run twice, never finish, retry forever, pile up
  in a queue nobody drains, or a crash leaves work half-applied.
- Use when: one tenant's job flood degrades or starves other tenants
  (noisy-neighbor at the worker layer) and fairness needs designing.
- Do NOT use when: the subject is the message TRANSPORT — topic/stream
  taxonomy, partition keys, consumer-group layout, delivery semantics, CDC —
  that is `streaming-event-architect`; jobs may ride that transport, but this
  skill designs the WORKER and its execution contract, not the pipe.
- Do NOT use when: the subject is MEASURING throughput, latency, or capacity
  under realistic load — `performance-test-harness` (instrument) and
  `load-test-planner` (traffic plan) measure what this skill designs.
- Do NOT use when: the "job" is really a synchronous protected write that
  belongs in the request path through the command gateway
  (`command-gateway-architect`) — not everything slow should be async.

## Inputs to Inspect

1. The work being offloaded: each task, its trigger (request-time enqueue /
   schedule / event), expected duration, side effects, and whether it is
   safe to run twice.
2. The current async substrate (if any): the queue/stream/scheduler in use,
   how workers consume it, and whether visibility timeout / ack semantics
   exist today.
3. Failure history: jobs that run twice, jobs stuck "processing" forever,
   retry storms, a dead-letter queue that exists but is never drained,
   crashes that left partial work.
4. Tenant shape: how many tenants, the size skew (one tenant's job volume vs
   the median), and whether jobs currently share one undifferentiated queue.
5. Scheduling needs: recurring jobs, their cadence, timezone/DST concerns,
   what happens on a missed run, and whether overlapping runs are unsafe.
6. Resource limits: worker concurrency, per-job memory/CPU, external rate
   limits the jobs must respect (third-party APIs, the database).

## Workflow

1. **Catalog jobs and classify each.** For every job: trigger, expected
   duration, side effects, idempotent (safe to re-run) or not, and priority.
   Flag anything currently synchronous that should be async — and anything
   async that is really a synchronous protected write in disguise (route to
   `command-gateway-architect`).
2. **Design the execution contract per job.** The load-bearing set:
   - **Idempotency**: a job may be delivered/retried more than once — define
     the dedup key or make the effect idempotent (upsert, "already done"
     check). Non-idempotent side effects (charge, email) get a guard.
   - **Retry + backoff**: max attempts, exponential backoff with jitter,
     and the classifier separating retryable (transient) from poison (never
     succeeds) — retrying poison forever is a self-inflicted outage.
   - **Visibility timeout / lease**: how long a picked-up job is invisible
     before it is redelivered, sized above the job's real runtime so a slow
     job is not double-run by a premature redelivery.
   - **Dead-letter queue**: where a job goes after max attempts, WHO owns
     draining it, and the alert when it fills — a DLQ without an owner is
     where jobs die silently.
3. **Design resumability/checkpointing for long jobs.** A job that processes
   10,000 rows and crashes at 9,000 must resume, not restart: checkpoint
   progress, make each unit idempotent, and record completion so a
   redelivery skips finished work. State the checkpoint granularity.
4. **Design per-tenant fairness.** One undifferentiated queue lets the
   largest tenant monopolize workers. Choose a mechanism: per-tenant queues
   with weighted/round-robin draining, concurrency caps per tenant, or a
   priority lane for interactive vs bulk work. State how a tenant's flood is
   bounded so others keep flowing — this is noisy-neighbor defense at the
   worker layer.
5. **Design scheduling** for recurring jobs: the scheduler, overlap
   prevention (a run must not start if the last is still going, unless
   designed to), missed-run policy (skip / run-once-catch-up / backfill),
   and timezone/DST correctness. Scheduled jobs are still jobs — they get
   the same idempotency and retry contract.
6. **Set worker scaling and drain.** Worker pool sizing, how it scales with
   backlog depth, and graceful drain on deploy/scale-in: an in-flight job
   finishes or is safely redelivered, never dropped mid-execution
   (statelessness/drain review composes `horizontal-scalability-reviewer`).
7. **Wire observability.** Backlog depth, job age, retry rate, DLQ size, and
   per-tenant queue depth as first-class signals with alert thresholds and
   owners (wiring handed to `observability-operator`). Note that CAPACITY
   validation — does this survive peak load — is measured by
   `performance-test-harness` / `load-test-planner`, not asserted here.
8. **Deliver** the job catalog, execution contract, and fairness/scaling
   plan in the Output Format, transport handoff named.

## Output Format

```
BACKGROUND JOB EXECUTION DESIGN — <system/domain>
Job catalog: <job — trigger — duration — side effects — idempotent? — priority>
Per-job execution contract:
  <job>: idempotency=<key/guard> retry=<attempts, backoff, retryable-vs-poison>
  visibility-timeout=<lease > runtime> DLQ=<dest, owner, drain SLA, alert>
  resumability=<checkpoint granularity | n/a>
Fairness:       <per-tenant queues / concurrency caps / priority lanes; how a
  tenant flood is bounded so others keep flowing>
Scheduling:     <scheduler; overlap prevention; missed-run policy; tz/DST> | n/a
Worker scaling: <pool sizing; scale-on-backlog; graceful drain → finish-or-redeliver>
  (drain/statelessness review → horizontal-scalability-reviewer)
Observability:  <backlog depth, job age, retry rate, DLQ size, per-tenant depth
  — thresholds + owners; wiring → observability-operator>
Boundaries:     transport (topics/partitions/delivery) → streaming-event-architect;
  capacity MEASUREMENT → performance-test-harness / load-test-planner
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every job is classified idempotent or not, and non-idempotent side
      effects have a guard — redelivery cannot double-apply.
- [ ] Every job has retry attempts, backoff with jitter, and a
      retryable-vs-poison classifier — nothing retries forever.
- [ ] Every job has a visibility timeout sized above its real runtime, and a
      DLQ with a named owner, drain SLA, and fill alert.
- [ ] Long jobs checkpoint and resume; a crash mid-job does not restart from
      zero or double-apply completed units.
- [ ] Per-tenant fairness is designed: one tenant's flood is bounded and
      cannot starve others (not one undifferentiated queue).
- [ ] Scheduled jobs have overlap prevention, a missed-run policy, and tz/DST
      correctness — and the same idempotency/retry contract as ad-hoc jobs.
- [ ] Workers drain gracefully: in-flight work finishes or is safely
      redelivered on deploy/scale-in.
- [ ] Transport is deferred to `streaming-event-architect`; capacity claims
      are deferred to the measurement skills, not asserted.

## Gotchas

- At-least-once delivery is the default reality: a job WILL occasionally run
  twice. Design for it with idempotency; "it shouldn't happen twice" is not
  a design.
- A visibility timeout shorter than the job's real runtime double-runs every
  slow job — the queue redelivers it while the first worker is still going.
- Retrying a poison job (bad input, permanent 4xx) forever burns workers and
  looks like a load problem; classify poison and DLQ it fast.
- A DLQ nobody drains is a silent data-loss queue; ownership and an alert are
  what make it a safety net rather than a grave.
- One shared queue is invisible unfairness: the tenant enqueuing 10,000 jobs
  gets 10,000 workers' worth of attention while a single urgent job waits
  behind them. Fairness is designed, not emergent.
- Cron overlap: a nightly job that occasionally runs 25 hours starts its next
  run before the last finishes; without overlap prevention they corrupt each
  other or double-spend.
- "Move it to a background job" is not free — an async job needs a way to
  report success/failure back to the user and a retry story; a fire-and-forget
  enqueue that silently fails is worse than a slow synchronous call.
- Dropping in-flight jobs on deploy loses work; drain must finish or safely
  redeliver, which requires the job to be idempotent (back to the first rule).

## Stop Conditions

- The work is actually a synchronous, user-blocking, security-sensitive write
  that belongs in the request path → route to `command-gateway-architect`;
  making it async to "speed up the response" can hide authorization and lose
  the user's result.
- The subject is really the message transport (topic/partition/delivery-
  semantics design) → route to `streaming-event-architect`; this skill's
  execution contract assumes a transport, it does not design one.
- A "guaranteed exactly-once job execution including external side effects"
  mandate survives → surface the honest at-least-once + idempotency
  decomposition and escalate; do not promise unqualified exactly-once.
- Asked to run jobs or a load test against production to "see if it holds" →
  this skill DESIGNS the model; executing jobs or load against production
  follows the repo's approval path and is measured by the performance skills.

## Supporting Files

- `evals/evals.json` — behavior cases: the offload design, the poison-job /
  visibility-timeout edge, per-tenant fairness, and the sync-write non-async
  refusal.
- `evals/trigger-evals.json` — discrimination against
  `streaming-event-architect` (THE hard-pinned transport-vs-execution seam),
  `performance-test-harness` / `load-test-planner` (measure vs design), and
  `command-gateway-architect` (async execution vs synchronous protected write).
- No `references/` — the execution-contract and fairness procedure above is
  complete; detail lives in the produced artifacts.
