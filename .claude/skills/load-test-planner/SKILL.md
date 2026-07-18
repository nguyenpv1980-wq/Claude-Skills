---
name: load-test-planner
description: 'Plan the load that makes performance testing mean something — a workload model from production evidence (endpoint mix, write share, arrival patterns, think times) instead of one hammered URL, a tenant mix reproducing multi-tenant reality (many-small plus few-whale tenants; the noisy-neighbor scenario where one tenant''s burst must not degrade the rest, judged per-tenant, not aggregate), data volumes seeded to production shape and skew, test types chosen by the question (load-at-target, stress-to-break, soak, spike), ramp profiles with abort criteria, and pass/fail tied to thresholds the budget/SLO owners set. PLANS only: the measuring instrument is performance-test-harness, and no scenario runs against production or live third parties without explicit human approval — blast radius stated per scenario. Use when planning load/stress/soak/spike testing, capacity validation, or noisy-neighbor verification. Do NOT use to build the harness/gates (performance-test-harness) or set targets (slo-reliability-architect).'
---

# Load Test Planner

## Purpose

A load test that hammers one endpoint with a thousand identical
requests proves the system can survive something production will never
send — and says nothing about what production will send. This skill
plans load with evidence: the workload model from observed traffic, the
tenant mix that makes multi-tenant failure modes reproducible (the
whale tenant's burst, the thousand small tenants' baseline, and whether
one degrades the other), the data volumes that make query behavior
real, the test type matched to the question being asked, ramp profiles
with abort criteria, and pass/fail owned by the people who own the
numbers. It is the traffic half of the D10 measurement pair: this
skill plans WHAT load runs; `performance-test-harness` is the
instrument that runs and measures it.

## Use When

- Use when: planning a load, stress, soak, or spike test — before a
  launch, a marketing event, a migration, or as standing pre-release
  practice.
- Use when: a capacity claim needs validation ("we can handle 3× the
  current peak") and the claim needs turning into a testable scenario
  with pass/fail.
- Use when: noisy-neighbor behavior needs verification — whether one
  tenant's burst degrades other tenants' experience, and by how much.
- Use when: an existing load test is unrealistic (single endpoint,
  no tenant dimension, empty database) and the plan needs rebuilding
  on evidence.
- Do NOT use when: building the measurement instrument — baselines,
  regression detection, CI gates, and report formats are
  `performance-test-harness`; this plan is its input.
- Do NOT use when: setting the TARGETS load is judged against — user
  journey promises and error budgets are `slo-reliability-architect`;
  per-hop numbers are `latency-budget-architect`. This plan cites
  their numbers as pass/fail.
- Do NOT use when: the load reveals a problem and the fix needs
  designing — attribution is `profiling-methodology-designer`;
  fixes belong to the D12.3 layer skills.
- Do NOT use when: designing the test DATA itself (fixtures,
  factories, PII-safe synthesis) — `test-data-architect` owns data
  generation conventions; this plan states the volumes and shapes it
  needs from them.
- Do NOT use when: functional test coverage under concurrency is the
  question (race conditions, correctness under parallel users) —
  that is functional testing with concurrency
  (`integration-test-designer` / `qa-strategy-architect` layers),
  not capacity validation.

## Inputs to Inspect

1. Production traffic evidence: endpoint mix (which calls, what
   proportion), arrival patterns (steady vs bursty, daily peaks),
   payload-size distribution, think-time behavior for session-shaped
   flows — from access logs, gateway metrics, or APM. No evidence →
   the model is assumption-flagged, never silently invented.
2. The tenant reality: tenant count and size distribution (the
   many-small / few-whale shape), per-tenant request rates, and known
   heavy tenants' behavior (batch windows, import bursts, big
   exports).
3. Data-volume reality: production table sizes, per-tenant skew, and
   growth trajectory — the volumes the test environment must be
   seeded to (via `test-data-architect` conventions) for queries to
   behave truthfully.
4. The numbers that judge the test: SLO targets, latency budgets,
   error-rate floors — from their owners; plus the capacity question
   being asked (target load, growth multiple).
5. The candidate target environment(s) and their blast radius: what
   the load can touch (dedicated perf environment, staging), what it
   must not (production, live third-party APIs, shared infrastructure
   whose other tenants are real) — stated per scenario.
6. Third-party dependencies on the tested paths: rate agreements,
   sandbox availability, or the stub-with-shaped-latency fallback
   (distributions from observation, not 1ms fantasy stubs).

## Workflow

1. **State the question each test answers.** Capacity at target
   ("does the system meet its numbers at expected peak × growth
   factor?"), limit finding ("where does it break, and how —
   gracefully or in flames?"), endurance ("what leaks, drifts, or
   fills over hours at sustained load?"), surge ("what happens in the
   first 90 seconds of a 10× spike?"). A test without a question
   produces graphs without verdicts.
2. **Build the workload model from evidence.** Endpoint mix in
   observed proportions (the write-path percentage matters most —
   all-read load tests flatter every system), session flows with
   think times where user behavior is session-shaped, payload sizes
   from the observed distribution, and arrival process (open-model
   arrivals for internet-facing surges vs closed-model virtual users
   for session systems — the choice changes what saturation looks
   like; state it).
3. **Design the tenant mix.** Concurrent tenants in the observed
   size distribution — explicitly including: the whale tenant at its
   real share, the long tail of small tenants, and per-tenant
   metrics as first-class outputs (aggregate p95 hides a single
   tenant's collapse — the harness measures per-tenant because this
   plan demands it).
4. **Write the noisy-neighbor scenario explicitly.** One tenant
   (the whale, or a synthetic burster) ramps to its worst observed
   behavior (import storm, export batch, API burst) while the rest
   hold baseline; pass/fail = other tenants' experience stays within
   its bound (cited from the SLO/budget owners). This scenario is
   the multi-tenant headline — it exists in every plan for a
   multi-tenant system, or its absence is justified in writing.
5. **Set data volumes.** Seed sizes per key table matching
   production shape including per-tenant skew (the whale's rows
   concentrated, not uniformly spread) — handed to
   `test-data-architect` conventions for generation; the plan states
   volumes and shapes, not generation mechanics.
6. **Profile the ramps with abort criteria.** Per scenario: ramp
   shape (step vs linear), hold durations at each plateau (long
   enough for percentiles to stabilize — minutes, not seconds),
   cool-down observation (does the system RECOVER?), and abort
   criteria (error rate, latency, or infrastructure signals that
   stop the run — with the safe-stop being load removal, never
   mid-run reconfiguration).
7. **Tie pass/fail to owned numbers.** Per scenario: the cited
   threshold (SLO target at load, budget at load, error floor),
   per-tenant bounds for the neighbor scenarios, and — for
   stress-to-break — no pass/fail but a required OUTPUT: the knee
   point, the failure mode (graceful shed vs cascade), and the
   first-to-saturate resource.
8. **State the safety envelope per scenario.** Target environment
   and its isolation, third-party handling (stub-shaped / sandbox /
   rate-agreed), the blast-radius statement, and the approval line:
   NOTHING in this plan runs against production or live third
   parties without explicit human approval recorded per the repo's
   conventions. Extrapolation honesty rides here too: results from
   a half-size environment do not linearly predict full-size
   behavior — scaling claims carry their assumptions.
9. **Hand the plan to the instrument.** Scenarios, models, mixes,
   ramps, and criteria in the Output Format — consumed by
   `performance-test-harness` for execution mechanics, measurement,
   and reporting; regressions and surprises route onward to
   `profiling-methodology-designer`.

Workload-model worksheet, tenant-mix and noisy-neighbor templates,
test-type selection table, and the extrapolation-honesty rules:
[references/workload-model-worksheet.md](references/workload-model-worksheet.md).

## Output Format

```
LOAD TEST PLAN — <system/scope>
Evidence base: <traffic source + window; tenant distribution source; volumes source;
                gaps = ASSUMPTION-FLAGGED items listed>
Scenarios:
  <name>: question=<capacity|limit|endurance|surge|noisy-neighbor>
  workload=<endpoint mix % (incl. write share), arrival model (open|closed), think times>
  tenant mix=<whale(s) + long tail, per observed distribution>
  data=<volumes + skew → test-data-architect conventions>
  ramp=<shape, plateaus, hold durations, cool-down> abort=<criteria → safe stop>
  pass/fail=<cited threshold (owner) | knee-point+failure-mode output (stress)>
  per-tenant bounds=<neighbor scenario limits>
  SAFETY: target=<environment>; third parties=<stubbed-shaped|sandbox|rate-agreed>;
          blast radius=<statement>; production/live-3P = human approval required
Extrapolation: <what these results can and cannot claim about production scale>
Handoff: execution/measurement → performance-test-harness;
         attribution of findings → profiling-methodology-designer
```

## Validation Checklist

- [ ] Every scenario states the question it answers; no
      graphs-without-verdicts tests.
- [ ] The workload model cites traffic evidence; assumptions are
      flagged items, not silent fills; the write share is explicit.
- [ ] The arrival model (open vs closed) is chosen and stated per
      scenario.
- [ ] The tenant mix reproduces the observed size distribution; a
      noisy-neighbor scenario exists (or its absence is justified in
      writing) with per-tenant pass bounds.
- [ ] Data volumes match production shape including skew, routed to
      test-data-architect conventions.
- [ ] Ramps have hold durations long enough for stable percentiles,
      cool-down observation, and abort criteria with a safe stop.
- [ ] Every pass/fail cites its owner's number; stress tests declare
      their required outputs instead.
- [ ] The safety envelope is stated per scenario; production and live
      third parties are behind explicit human approval.
- [ ] Extrapolation claims carry their assumptions.

## Gotchas

- The all-read flattery: load tests skewed to reads (because writes
  are annoying to script) validate a system production will falsify
  — the write share is the model's most load-bearing number.
- Open vs closed model confusion: closed models (fixed virtual users
  waiting politely) self-throttle at saturation and hide queue
  explosions an open-model (arrivals keep coming) surface exposes.
  Internet-facing spikes are open-model events; testing them closed
  understates the damage.
- Aggregate metrics hide tenant collapse: the fleet p95 looks fine
  while one tenant's every request times out. Per-tenant measurement
  is demanded by the plan, or the noisy-neighbor scenario proves
  nothing.
- The coordinated-omission trap: measuring only completed requests
  under a stalling system undercounts latency exactly when it
  matters — the plan notes the driver must account for it
  (arrival-time-based accounting), a requirement the harness
  implements.
- Cache-warm plateaus that flatter: a plateau reached after gentle
  ramp measures warm-cache behavior; the surge scenario exists
  because production spikes arrive cold. Both are real; label which.
- Ten-second plateaus prove nothing: percentiles stabilize over
  minutes; a plan whose holds are shorter than stabilization is a
  demo, not a test.
- The soak test nobody watches: endurance runs produce their value
  in the drift curves (memory, connection pools, disk, queue depth)
  — the plan names which resources the harness must trend, or the
  soak is just a long load test.
- Half-scale extrapolation: doubling from a half-size environment is
  not linear (connection limits, partition counts, cache sizes all
  step). Scaling claims state their assumptions or they are
  marketing.
- Stubbed third parties at 1ms: fantasy stubs remove the tail your
  users actually experience — stub latencies are shaped to observed
  distributions, or the blind spot is stamped.

## Stop Conditions

- Asked to run (or schedule) load against PRODUCTION or live
  third-party APIs → stop; produce the scenario with its
  blast-radius statement and require explicit recorded human
  approval; low-rate production probes included. The plan authors
  scenarios; it executes nothing.
- No pass/fail numbers exist and none can be cited (no SLO, no
  budget, no recorded decision) → capacity tests cannot conclude;
  route target-setting to `slo-reliability-architect` /
  `latency-budget-architect`, or run limit-finding (stress) honestly
  — which needs no target, only required outputs.
- No traffic evidence exists AND the requester refuses
  assumption-flagging ("just make it realistic") → stop; a workload
  model without evidence or flags is fiction wearing a lab coat.
- The only viable target environment shares infrastructure with real
  tenants such that the test's load degrades them → halt and surface
  the isolation gap; a load test whose blast radius includes
  production users is an incident by appointment.
- Required data volumes would be met by copying production data →
  route to `test-data-architect`'s PII-safe path; the plan never
  prescribes production copies.
- The capacity question is really a COST question ("can we afford
  3×?") → the load answer feeds it, but route the economics to
  `saas-cost-architect` rather than settling it in a load plan.

## Supporting Files

- [references/workload-model-worksheet.md](references/workload-model-worksheet.md)
  — workload-model worksheet (mix, arrivals, think times, write
  share), tenant-mix and noisy-neighbor scenario templates, the
  test-type selection table, ramp/abort profiles, and
  extrapolation-honesty rules.
- `evals/evals.json` — behavior cases including the noisy-neighbor
  edge and the load-production refusal.
- `evals/trigger-evals.json` — discrimination against
  `performance-test-harness` (the sibling), `slo-reliability-architect`,
  `test-data-architect`, and `qa-strategy-architect`.
