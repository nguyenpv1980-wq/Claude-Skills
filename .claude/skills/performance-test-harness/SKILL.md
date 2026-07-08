---
name: performance-test-harness
description: Design the harness that MEASURES performance as release evidence — what to measure per surface (API endpoint latency percentiles, database query timings, frontend loading/interactivity metrics on a stated device class, edge-function and background-job durations), the environment contract that makes numbers comparable (prod-like data volume and tenant shape, isolation from noisy neighbors of the test itself, pinned hardware/config), baseline management and regression detection that respects variance (percentile comparison with repeat runs and noise bands — never two single runs diffed), pass/fail thresholds consumed from latency-budget-architect budgets and slo-reliability-architect targets (the harness ASSERTS numbers others set), CI placement per tier (per-PR smoke, nightly full, pre-release soak) with advisory-to-blocking progression, and honest reporting (conditions stamped on every result; UNRUN stated, never implied green). The harness DESIGN skill — it executes nothing against production (approval-gated) and the load scenarios it drives come from load-test-planner. Use when building perf measurement/regression gates or when "did it get slower?" has no evidenced answer. Do NOT use to design FOR performance (that is the D12.3 pack) or to plan traffic (load-test-planner).
---

# Performance Test Harness

## Purpose

Every team discovers performance regressions the same way — a customer
does — because "it seems fine" was the release evidence. This skill
designs the measurement instrument: which numbers are captured per
surface, under what pinned conditions they are comparable week to week,
how a regression is DETECTED against variance rather than eyeballed,
which thresholds gate (consumed from the budget and SLO owners — the
harness asserts numbers, it does not invent them), and where in CI each
measurement tier runs. It is the MEASURES side of the pack's seam: the
D12.3 skills design systems to be fast; this harness proves whether
they are, and catches the release that makes them slower. It designs
the instrument and its gates; it runs nothing against production, and
the traffic it drives comes from `load-test-planner` scenarios.

## Use When

- Use when: building or overhauling performance measurement for a
  product — endpoint percentiles, query timings, frontend metrics,
  job/function durations — as standing release evidence.
- Use when: "did this PR / release make it slower?" has no evidenced
  answer and regression gates are wanted in CI.
- Use when: perf numbers exist but are incomparable (unpinned
  environments, single-run diffs, unstated data volumes) and the
  measurement needs an environment contract.
- Use when: budgets (`latency-budget-architect`) or SLO targets
  (`slo-reliability-architect`) exist and need enforcement as
  pre-release assertions.
- Do NOT use when: designing the system to BE fast — caching, query
  tuning, budgets, frontend optimization are the D12.3 pack
  (`caching-strategy-designer`, `query-plan-reader`,
  `latency-budget-architect`, `frontend-perf-engineer`); this skill
  measures what they built.
- Do NOT use when: planning the traffic itself — workload models,
  tenant mix, stress/soak/spike profiles are `load-test-planner`; the
  harness EXECUTES its scenarios and measures the result.
- Do NOT use when: a caught regression needs attributing to a
  component — that investigation is `profiling-methodology-designer`;
  the harness raises the flag, the methodology finds the culprit.
- Do NOT use when: designing production SLO monitoring/alerting —
  that is `slo-reliability-architect` (targets/alerts) and
  `observability-operator` (wiring); this harness is PRE-release
  validation.
- Do NOT use when: architecting the functional test suites (unit/
  integration/E2E structure, runners, fixtures) —
  `qa-automation-architect`; the perf harness is a sibling with its
  own environment and variance disciplines.

## Inputs to Inspect

1. The surfaces worth measuring, ranked: critical-journey endpoints,
   the queries behind them, key pages (with device class), background
   jobs and edge functions with duration obligations — from budgets,
   SLOs, and incident history.
2. The thresholds that already exist: `latency-budget-architect`
   budget tables, `slo-reliability-architect` targets, contract
   promises — the harness consumes these; where none exist, the gap
   is named, not filled in silently.
3. Environment options honestly assessed: what prod-like means here —
   data volume and tenant shape (`test-data-architect` conventions
   for seeding at volume), hardware/instance parity, and what CANNOT
   be made representative (third parties, fleet size) — stated as
   known blind spots.
4. The load sources: existing `load-test-planner` scenarios (or their
   absence — smoke-level self-generated load is the floor), and the
   driver tooling the team can operate.
5. CI topology: pipeline stages, time budgets per stage
   (`ci-pipeline-architect`'s latency budget for the pipeline
   itself), and where nightly/pre-release runs can live.
6. Historical variance if any measurements exist: how noisy current
   numbers are — this sizes the noise bands and repeat counts.

## Workflow

1. **Choose the measured set.** Per surface class, the specific
   measurements: endpoints (latency p50/p95/p99, error rate,
   throughput at target load), queries (timing at representative
   volume — plan-shape checks live with `query-plan-reader`),
   frontend (the loading/interactivity/stability trio on the device
   class `frontend-perf-engineer` defined), jobs/functions (duration,
   queue wait). Every measurement names its owner and the decision it
   informs — measurements nobody acts on are deleted.
2. **Write the environment contract.** The conditions stamped on
   every result: data volume and tenant shape (seeded via
   `test-data-architect` conventions), instance/hardware class,
   config flags, network position, cache state (cold/warm — declared,
   not accidental), and the isolation rule: the measurement
   environment is not shared with other work during runs. What cannot
   be made representative is listed as a blind spot on the report,
   permanently.
3. **Design baseline management.** Baselines are per-measurement,
   per-environment-contract, versioned with the code (a baseline from
   last quarter's data volume is not a baseline), refreshed on
   deliberate change (an approved perf-affecting merge updates the
   baseline explicitly — silent drift is the anti-pattern), and
   stored where CI can diff against them.
4. **Design regression detection that respects variance.** Repeat
   runs (N per measurement, N stated), percentile-to-percentile
   comparison, and a noise band derived from observed run-to-run
   variance — a regression is a delta exceeding the band, not any
   delta. Warm-up runs discarded by policy. Single-run diffs are
   banned by design; flaky perf checks erode gates faster than no
   gates.
5. **Set thresholds by consumption.** Each gate's number cites its
   source: hop budgets (`latency-budget-architect`), journey targets
   (`slo-reliability-architect`), frontend budgets
   (`frontend-perf-engineer`), or an explicit team decision recorded
   where no owner-set number exists. The harness NEVER invents a
   threshold silently — an uncited number is a finding against the
   design itself.
6. **Place tiers in CI.** Per-PR: fast smoke (a bounded subset at
   light load — minutes, not hours) catching gross regressions;
   nightly: the full measured set at target load against baselines;
   pre-release: the heavier `load-test-planner` scenarios (soak/
   stress where planned) as release evidence. New gates start
   ADVISORY and are promoted to blocking after a stated stability
   window — the credibility ramp that keeps teams from deleting the
   gate the first noisy week.
7. **Design the report.** Every result carries: conditions stamp
   (the environment contract fields), baseline compared against,
   repeat count and variance, verdict per gate
   (PASS/FAIL/ADVISORY-FAIL), and UNRUN as a first-class status —
   a skipped perf tier is reported as UNRUN, never silently absent
   (a green pipeline that didn't run the perf tier is not perf
   evidence). Regression flags route to
   `profiling-methodology-designer` for attribution.
8. **State the execution posture.** The harness design targets
   dedicated measurement environments. Anything touching production
   (even read-mostly probes) or shared infrastructure at load is
   approval-gated per the repo's conventions — the design says so on
   its face, and running the harness is an operator/CI act, not this
   skill's.

Measurement catalogs per surface, the environment-contract template,
noise-band sizing, and the tier/report formats:
[references/harness-architecture-sheet.md](references/harness-architecture-sheet.md).

## Output Format

```
PERFORMANCE TEST HARNESS DESIGN — <product/scope>
Measured set: <surface → measurements → owner → decision informed>
Environment contract: <data volume/tenant shape (seeding ref), hardware class,
                       config, cache state policy, isolation rule>
Blind spots: <what cannot be representative — permanent report footnote>
Baselines: <per measurement; versioned with code; refresh-on-approved-change rule>
Detection: <repeat count N, percentile comparison, noise band derivation,
            warm-up discard policy; single-run diffs banned>
Thresholds: <each gate → cited source (budget|SLO|frontend budget|recorded decision)>
CI tiers: per-PR smoke <scope, minutes> | nightly full <scope> | pre-release <load-test-planner scenarios>
          advisory→blocking promotion rule: <stability window>
Report: <conditions stamp, baseline ref, variance, PASS/FAIL/ADVISORY/UNRUN;
         regression → profiling-methodology-designer>
Execution posture: dedicated environments; production/shared-infra touches
                   approval-gated; this design executes nothing.
```

## Validation Checklist

- [ ] Every measurement names an owner and the decision it informs;
      the set was ranked, not exhaustive by default.
- [ ] The environment contract exists and every result stamps it;
      blind spots are listed, not implied away.
- [ ] Baselines are versioned and refresh only on approved change —
      no silent drift path exists.
- [ ] Detection uses repeat runs with a variance-derived noise band;
      no single-run diff anywhere in the design.
- [ ] Every threshold cites its source; zero invented numbers.
- [ ] Per-PR tier fits its pipeline time budget; heavier tiers are
      placed where they can afford to run.
- [ ] New gates start advisory with a stated promotion rule.
- [ ] UNRUN is a reportable status and a skipped tier cannot read as
      green.
- [ ] The design executes nothing against production; approval gates
      are stated in the posture section.

## Gotchas

- The noise-ban paradox: gates tighter than the environment's noise
  band fail randomly, get muted, and then miss real regressions —
  the band is measured first, the gate set outside it. A flaky perf
  gate is worse than none.
- Baseline drift by kindness: "the baseline was old so I refreshed
  it" quietly ratifies last month's regression. Refresh is coupled
  to an APPROVED perf-affecting change, and the refresh is itself a
  reviewed diff.
- Empty-database heroics: measurements over toy data volumes produce
  numbers that flatter every query — volume is part of the
  environment contract because the planner and the plans change with
  it (`query-plan-reader`'s own capture rule, applied fleet-wide).
- Shared-runner sabotage: perf jobs on shared CI runners inherit
  neighbors' CPU steal — numbers move with the runner's mood.
  Dedicated/pinned runners for measured tiers, or the results are
  weather.
- Warm-cache flattery vs cold-start truth: both are real; blending
  them is the sin. The cache-state policy declares which state each
  measurement captures.
- The per-PR tier that grew: smoke tiers accrete measurements until
  they take 40 minutes and get skipped under deadline. The pipeline
  time budget is a hard constraint; overflow moves to nightly, not
  into developers' patience.
- Percentiles need samples: a p99 from 50 requests is a dice roll;
  minimum sample counts per percentile are part of detection design.
- Third-party stubs that lie politely: stubbed dependencies answer
  in 1ms; production's answer in 300ms. Stub latencies are shaped to
  observed distributions (the planner's data), or the blind spot is
  stamped on the report.

## Stop Conditions

- Asked to run the harness (or any load) against PRODUCTION or
  shared live infrastructure → stop; produce the approval-ready
  proposal (scope, load level, blast-radius statement, abort rule)
  and require explicit human approval per the repo's conventions.
  The design never self-executes there.
- No thresholds exist and the requester wants the harness to invent
  pass/fail numbers → refuse silent invention; route target-setting
  to `slo-reliability-architect` / `latency-budget-architect`, or
  record an explicit interim team decision as the cited source.
- The only available environment shares infrastructure with
  production tenants (noisy-neighbor risk flows TOWARD real users)
  → halt that tier's design and surface the isolation gap; a
  measurement that can degrade production is not a test, it is an
  incident with a dashboard.
- Data seeding at representative volume would require production
  data copies → stop and route to `test-data-architect`'s
  PII-safe synthetic/anonymization path; the environment contract
  never launders real personal data into test systems.
- Asked to also design the workload models, tenant mix, or
  stress/soak profiles → that is `load-test-planner`'s plan;
  compose it, don't absorb it.

## Supporting Files

- [references/harness-architecture-sheet.md](references/harness-architecture-sheet.md)
  — per-surface measurement catalogs, environment-contract template,
  noise-band sizing method, baseline lifecycle, CI tier table, and
  the report format with the UNRUN rule.
- `evals/evals.json` — behavior cases including the variance-band
  edge and the run-against-production refusal.
- `evals/trigger-evals.json` — discrimination against
  `load-test-planner` (the sibling), the D12.3 design-side skills
  (`latency-budget-architect`, `frontend-perf-engineer`),
  `slo-reliability-architect`, and `qa-automation-architect`.
