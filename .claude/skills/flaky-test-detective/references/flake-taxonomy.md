# Flake Taxonomy & Reproduction Ladder

Detail file for `flaky-test-detective`. Loaded on demand.

## Classification taxonomy with signatures

| Category | Typical signature |
| --- | --- |
| Ordering dependence | passes alone, fails in suite (or vice versa); fails only after a specific test; shuffle changes outcome |
| Shared state — data | fails only in parallel; failure mentions rows/records another test owns; unique-constraint violations |
| Shared state — global/module | fails after tests touching the same module; leftover mocks/timers/env vars; passes with isolated modules |
| Timing/race — test-side | assertion ran before the awaited effect; fixed by awaiting the real condition; failure at waits/timeouts |
| Timing/race — product-side | race reproducible against the app itself (double-submit, out-of-order responses) — a PRODUCT bug |
| Environment | fails on specific TZ/locale/runner class; timestamp clustering (midnight, month-end, DST) |
| Infrastructure | network blips, container OOM, port collisions; failure messages about infra, uncorrelated with code |
| Intermittent product bug | any of the above signatures rooted in shipped code paths |

Multiple distinct failure messages → assume multiple causes; split cases.

## Reproduction escalation ladder

1. **Repeat single test:** Vitest: run the file with repeats (loop or
   `--retry=0` + shell loop; some versions support `repeats` in config).
   Playwright: `--repeat-each=N`. Record k/N.
2. **Order shuffle:** Vitest `--sequence.shuffle --sequence.seed=<s>`;
   rerun with the failing seed to pin ordering deps.
3. **Parallel stress:** run with the CI worker count locally
   (`--pool=threads --poolOptions.threads.maxThreads=<n>` / Playwright
   `--workers=<n>`); shared-state flakes surface here.
4. **Environment pinning:** `TZ=<ci-tz> LANG=<ci-locale>`; match CI Node
   version; constrain CPU (e.g., run under load) to simulate runner
   pressure.
5. **Race amplification:** targeted small delay or load at the suspected
   await point (temporarily, in a branch) to make the window reliable —
   remove after diagnosis.

A reproduction statement is counts under conditions: "7/50 shuffled seed
1234, 0/50 sequential" — that sentence IS the ordering-dependence proof.

## Forbidden fixes → allowed alternatives

| Forbidden | Why | Allowed alternative |
| --- | --- | --- |
| add retry | hides the cause, erodes trust | fix the cause; retries only per suite policy for infra tiers |
| add sleep | converts race to slower race | await the actual condition (event, state, response) |
| widen timeout silently | masks slow regressions | if genuinely slow, widen WITH a named reason + issue |
| weaken/remove assertion | deletes the coverage | fix isolation/data so the strong assertion holds |
| delete the test | deletes evidence + coverage | curation decision via regression-suite-curator with the case report |

## Quarantine record (per policy)

`{test id, owner, ticket, quarantined date, expiry, reproduction status}` —
no owner/ticket/expiry → not a quarantine, just hidden red.
