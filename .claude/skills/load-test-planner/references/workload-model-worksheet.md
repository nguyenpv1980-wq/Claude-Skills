# Workload Model Worksheet

Templates and tables backing the plan. Driver-agnostic: express in
whatever load tool the team operates; the model is the contract.

## Workload-model worksheet

```
Evidence window: <source (access logs / gateway metrics / APM), period>
Endpoint mix:    <endpoint: % of traffic; TOP-N covering ≥90%>
WRITE SHARE:     <% of requests that mutate — the most load-bearing number>
Arrival model:   OPEN (arrivals keep coming — internet-facing, surge scenarios)
                 | CLOSED (fixed virtual users with think times — session systems)
                 chosen because: <what saturation must look like>
Think times:     <distribution for session flows | n/a for open model>
Payload sizes:   <distribution per heavy endpoint — imports/exports especially>
Assumption flags:<every number NOT from evidence, listed>
```

## Test-type selection table

| Question | Type | Load shape | Verdict form |
|---|---|---|---|
| Do we meet our numbers at expected peak (× growth)? | load-at-target | ramp to target, hold ≥ stabilization | PASS/FAIL vs cited thresholds |
| Where does it break, and how? | stress-to-break | staircase past target until failure | knee point + failure mode + first-saturated resource (no pass/fail) |
| What leaks or drifts over hours? | soak/endurance | sustained realistic load, hours | drift curves on NAMED resources (memory, pools, disk, queues) |
| What do the first 90 seconds of a surge do? | spike | step to N× in seconds (open model, cold-cache stated) | survival behavior + recovery time |
| Does one tenant degrade the rest? | noisy-neighbor | baseline + single-tenant burst | OTHER tenants' bounds hold (per-tenant metrics) |

## Tenant-mix template

```
Distribution (observed): <e.g., 2 whale tenants = 35% of traffic;
                          ~50 mid; ~1,500 small = long tail>
Modeled as: <whales individually scripted with their real behavior
            (imports, exports, API bursts); tail as classes>
Per-tenant measurement: REQUIRED outputs — per-tenant p95/error rate for
                        whales + sampled tail tenants (aggregate hides collapse)
Data skew: whale rows CONCENTRATED (their tables/partitions), not uniform
```

## Noisy-neighbor scenario template

```
NOISY-NEIGHBOR — <system>
Baseline: full tenant mix at observed rates
Burst:    <tenant class> ramps to <worst observed behavior: import storm /
          export batch / API burst> over <ramp>
PASS =    all OTHER tenants' p95 ≤ <cited bound> AND error rate ≤ <floor>
          throughout burst + recovery within <t> after burst ends
Instrument note: per-tenant series required (performance-test-harness)
Absence rule: a multi-tenant system's plan without this scenario justifies
              the omission in writing
```

## Ramp & abort profile

```
Ramp:      <step (finds knees) | linear (smooth capacity)> to <plateau(s)>
Hold:      ≥ <minutes> per plateau (percentile stabilization; 10s holds prove nothing)
Cool-down: <observation window — does the system RECOVER unaided?>
Abort:     error rate > <x>% | p99 > <y> for > <d> | infra signal <z>
           → SAFE STOP = remove load (never mid-run reconfiguration)
Coordinated omission: driver must account by arrival-time accounting —
           a stalling system's latency is measured from intended send time
```

## Extrapolation-honesty rules

- Results claim the TESTED environment at the TESTED scale; scaling
  statements list their assumptions (connection limits, partition
  counts, cache sizes step — they do not scale linearly).
- Half-size environments: state the known non-linear boundaries
  between test scale and production scale; where unknown, the claim
  is bounded ("validated to X on environment Y; production margin
  unquantified beyond Z").
- Stub latency shaping: third-party stubs answer with the OBSERVED
  latency distribution (median + tail), or the report carries the
  blind-spot stamp.

## Safety envelope checklist (per scenario)

- [ ] Target environment named; isolation from real users stated
- [ ] Third parties: stub-shaped | sandbox | rate-agreed (in writing)
- [ ] Blast radius: worst case if the test misbehaves
- [ ] Production / live-3P touches: explicit human approval recorded
      BEFORE scheduling (the plan never self-authorizes)
- [ ] Abort criteria + safe stop rehearsed with the operator
