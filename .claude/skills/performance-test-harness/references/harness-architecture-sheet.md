# Harness Architecture Sheet

Measurement catalogs, contracts, and formats backing the design.
Tool-agnostic: the driver/collector is whatever fills that role in your
stack.

## Measurement catalog per surface

| Surface | Measurements | Notes |
|---|---|---|
| API endpoint | p50/p95/p99 latency, error rate, throughput at target load | at TARGET load — idle-system latency is a different (also useful) number; label which |
| Database query | wall-clock at representative volume; regression vs baseline | plan-SHAPE verdicts belong to query-plan-reader; the harness times, it does not interpret |
| Frontend page | loading / interactivity / stability trio @ device class | device class from frontend-perf-engineer's definitions; lab conditions pinned |
| Background job | duration, queue wait at target depth | queue wait needs load present — an empty queue measures nothing real |
| Edge function | duration incl. cold-start share | cold/warm measured separately by policy |

Minimum sample counts: state per percentile (a p99 needs enough
requests that the 1% tail contains real samples — hundreds at minimum;
the sheet's rule: no percentile reported whose tail holds < 30 samples).

## Environment-contract template

```
ENVIRONMENT CONTRACT — <harness tier>
Data:      <volume per key table; tenant shape (many-small/few-large mix);
            seeding ref (test-data-architect conventions)>
Compute:   <instance/hardware class, pinned; dedicated runner rule>
Config:    <flags/limits mirroring production; deltas listed>
Network:   <position (same-region?); third-party handling (stub w/ shaped
            latency | sandbox | live-with-approval)>
Cache:     <cold | warm — per measurement, declared>
Isolation: <no co-tenants during runs; runner dedicated during window>
BLIND SPOTS (permanent report footnote): <fleet size, real third-party
            tails, production cache topology, ...>
```

## Noise-band sizing

1. Run the measurement N≥10 times on an UNCHANGED build under the
   contract.
2. Band = observed run-to-run spread at the gated percentile (e.g.,
   p95-of-runs ± max observed delta), padded by a stated margin.
3. Gate threshold must sit OUTSIDE the band; a wanted-tighter gate
   means fixing the environment first (dedicated runners, more
   repeats), not wishing.
4. Re-derive the band when the contract changes; the band's derivation
   date rides on the report.

## Baseline lifecycle

- Created: first stable run set under a contract → stored, versioned
  with code.
- Compared: every gated run diffs against the CURRENT baseline for its
  contract.
- Refreshed: only alongside an approved perf-affecting change; the
  refresh commit states the accepted delta ("accepts +12ms p95 on X
  for feature Y").
- Retired: contract change (data volume, hardware) retires old
  baselines explicitly — cross-contract diffs are meaningless.

## CI tier table

| Tier | Trigger | Scope | Load | Time budget | Gate mode |
|---|---|---|---|---|---|
| Smoke | per-PR | top endpoints + key page, bounded | light, self-generated | minutes (fits ci-pipeline-architect's stage budget) | advisory → blocking after stability window |
| Full | nightly | whole measured set | target load (load-test-planner primary scenario) | tens of minutes–hours | blocking on cited thresholds |
| Release | pre-release | full + soak/stress per plan | load-test-planner scenarios | scheduled window | release evidence; UNRUN blocks the evidence claim, per policy |

## Report format

```
PERF RUN — <tier> <date> <build>
Contract: <ref + stamp fields>   Baseline: <id/date>
Repeats: N=<n>  variance: <observed>
Results:
  <measurement>: <value> vs baseline <value> (Δ, band ±b) → PASS | FAIL | ADVISORY-FAIL
  <measurement>: UNRUN — <reason>          ← first-class status, never omitted
Verdict: <gate summary>; regressions → profiling-methodology-designer with
         contract + artifacts attached
Blind spots: <standing footnote>
```

The UNRUN rule: a tier or measurement that did not run appears as
UNRUN with a reason. Pipelines summarize perf evidence as
"<passed>/<failed>/<unrun>" — a green build with unrun perf tiers
cannot be read as perf-validated (the honesty rule this repo's D3
eval convention applies to itself).
