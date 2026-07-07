# Isolation Tactics

Supporting detail for `systematic-debugger`. Read on demand.

## Bisection recipes

- **Change bisection:** `git bisect start; git bisect bad HEAD; git bisect good <last-known-good>` with the reproduction as the test command (`git bisect run <cmd>` when it exits nonzero on failure). Preconditions: clean tree, deterministic repro — a flaky test makes bisect lie confidently.
- **Dependency bisection:** when the window spans a lockfile change, bisect the lockfile alone (checkout old lockfile on new code and vice versa) to split "our code vs their code" in one experiment.
- **Data bisection:** binary-search the failing input — half the file, half the rows, half the request body — keeping whichever half still fails.
- **Config bisection:** diff the failing environment's resolved config against a working one, then flip suspects one at a time toward the failing value.

## Intermittent-failure amplifiers

| Suspected class | Amplifier |
| --- | --- |
| Race/concurrency | Run under load; raise parallelism; add scheduler jitter (`stress`, repeat-runner); insert deliberate sleeps at suspected interleave points to force the ordering |
| Order dependence (tests) | Run the suite in random order with a printed seed; re-run with the failing seed; run the failing test alone vs after its predecessors |
| Resource exhaustion | Loop the repro while watching memory/fd/connection counts; failure iteration number ≈ leak rate |
| Time-dependent | Freeze/advance the clock (fake timers, `libfaketime`); test across midnight, month-end, leap day, DST transitions, non-UTC zones |
| Data-shape-dependent | Capture failing production payload shapes (sanitized); property-based fuzz around the boundary |

Reliability arithmetic: if the bug fails 1-in-20 runs, a 20-run green streak
after a fix is ~36% likely by luck alone. Run enough iterations that chance
survival drops below ~1% (for 1-in-20: ~90 runs).

## Environment-delta checklist (fails only in env X)

Compare, in order of payoff: runtime version → dependency resolution (lockfile
actually installed?) → env vars/secrets present and non-empty → data volume
and shape → permissions/roles → concurrency level → network topology
(proxies, DNS, TLS interception) → filesystem case-sensitivity and line
endings → locale/timezone → resource limits (memory, ulimits, container caps).

## Instrumentation patterns

- Instrument the BOUNDARY between suspect and victim (function entry/exit,
  queue publish/consume, request/response) — not the whole path; too many
  probes change timing and can hide races (heisenbug).
- Prefer structured one-line logs with a correlation id over print storms;
  you will diff two runs, not read one.
- For state corruption, log a checksum/invariant at checkpoints and find the
  first checkpoint where it breaks — that converts "somewhere before the
  crash" into a bisectable range.
- Remove every probe before the fix ships; grep for the probe marker string
  you used (pick a greppable marker like `DBG-<ticket>` when inserting).

## Hypothesis-ranking heuristics

Recent change beats old code. Code you wrote beats the framework; the
framework beats the compiler; the compiler beats the CPU (in that order of
prior probability). The hypothesis that explains ALL observations beats the
one that explains the loudest observation. And the hypothesis you can test in
one minute is worth testing first even if it ranks third.
