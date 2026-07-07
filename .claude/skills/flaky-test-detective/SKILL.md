---
name: flaky-test-detective
description: Drive a flaky (intermittently failing) test to its root cause and proven stability through the fixed sequence CLASSIFY (ordering, shared state, timing/race, environment, infrastructure, or real intermittent product bug) → REPRODUCE deterministically (repeat runs, order shuffling, parallel stress, seed/timezone control) → FIX ONE CAUSE → PROVE stability with repeated runs and real counts. Never fixes by adding retries, sleeps, or looser assertions; distinguishes test bugs from product bugs (a race the test exposes may ship to users). Manages quarantine only with owner, ticket, and expiry. Use when a test fails intermittently, passes on retry, fails only in CI or only in parallel, or a suite's trust is eroding from random red. Do NOT use for tests that fail consistently (systematic-debugger for the product bug, or fix the test), for setting suite-wide retry/flake policy (qa-automation-architect), or for deciding suite membership (regression-suite-curator).
---

# Flaky Test Detective

## Purpose

Convert "it fails sometimes" into a named root cause, one targeted fix, and
statistical evidence of stability — instead of the usual retries, sleeps,
and eroding trust. The deliverable is a case report: classification with
evidence, a deterministic reproduction (or an honest account of why not),
the single cause fixed, before/after stability counts from real repeated
runs, and a prevention note. Flakes are also triaged honestly: some "flaky
tests" are real intermittent product bugs wearing a test's name.

## Use When

- Use when: a test fails intermittently — locally, in CI, on retry, only in
  parallel, only at certain times.
- Use when: CI passes-on-retry are accumulating (retry telemetry from the
  automation blueprint's policy) and cases need working.
- Use when: a quarantined test's expiry arrives and it needs diagnosis or
  release.
- Do NOT use when: the test fails EVERY run — that's a plain failure:
  product bug → `systematic-debugger`; test bug → fix at its layer's
  engineer skill.
- Do NOT use when: setting suite-wide retry/quarantine POLICY — 
  `qa-automation-architect`; this skill works individual cases under that
  policy.
- Do NOT use when: deciding whether a test belongs in the suite at all —
  `regression-suite-curator` (a chronic flake may be a curation candidate,
  flagged as this skill's output).

## Inputs to Inspect

1. Failure history: CI runs, frequency, pass-on-retry counts, first
   appearance (what merged around then), failure message VARIANTS (multiple
   distinct errors = possibly multiple causes).
2. The test code and its fixtures: shared state, module-level setup, data it
   assumes, timers/awaits, network/mocks.
3. Execution context of failures vs passes: parallel workers, order/seed,
   CI runner class vs local, timezone/locale, resource pressure.
4. The code under test: async paths, caches, background effects — candidate
   real races.
5. The flake policy in force (quarantine rules, retry settings) so case
   handling conforms.

## Workflow

1. **Classify first** against the taxonomy in
   [references/flake-taxonomy.md](references/flake-taxonomy.md): ordering
   dependence, shared state (data/global/module), timing/race (test-side or
   product-side), environment (TZ/locale/CI-runner), infrastructure
   (network/container), or intermittent product bug. Evidence: failure
   variants, context diffs between passing and failing runs. State the
   leading hypothesis and what observation would refute it.
2. **Reproduce deterministically.** Escalate: repeat the single test N times
   (runner repeat flags / loop); shuffle order + fixed seeds to expose
   ordering; run the suite in parallel locally to expose shared state; pin
   TZ/locale/env to CI's values; add targeted delay/load at the suspected
   race point to make it reliable. Record exact commands + counts (e.g.,
   "fails 7/50 shuffled, 0/50 sequential" is a classification result in
   itself).
3. **Isolate the ONE cause** the reproduction demonstrates. Multiple
   suspected causes → separate cases, fixed one at a time (per
   `systematic-debugger` discipline — one change per attempt).
4. **Triage: test bug or product bug?** If the race lives in product code,
   the flake is a FINDING about production behavior — route the product fix
   (`systematic-debugger`/owner) and keep the test; do not "harden" the test
   into hiding a real race.
5. **Fix that one cause at the test layer** when it is a test bug: real
   isolation (own data per `test-data-architect` patterns), await the actual
   condition (web-first/waitFor semantics per the layer's engineer skill),
   control time/seed, remove order dependence. FORBIDDEN as fixes: retries,
   sleeps, widened timeouts without a named reason, weakened assertions,
   deletion-to-green.
6. **Prove stability with counts:** re-run the reproduction protocol —
   before (fails k/N under condition X) vs after (0/N under the same X,
   N ≥ the count that reliably reproduced). One green run proves nothing.
7. **Close the case:** report; if quarantined, release or extend WITH owner/
   ticket/expiry per policy; add the prevention note (pattern to lint/avoid);
   flag chronic offenders to `regression-suite-curator`.

## Output Format

```
FLAKE CASE — <test id/name>
History: <frequency, first seen, pass-on-retry counts, failure variants>
Classification: <category + evidence + refutable hypothesis>
Reproduction: <exact commands/conditions → counts (fails k/N under X)>
Cause: <the ONE demonstrated cause>
Triage: <test bug | product bug (routed with evidence) | infra (routed)>
Fix: <the one change made; forbidden-fix check passed>
Stability proof: <before k/N vs after 0/N under identical conditions, N=<n>>
Quarantine action: <none | released | extended (owner, ticket, expiry)>
Prevention: <pattern note; chronic-offender flag → regression-suite-curator>
```

## Validation Checklist

- [ ] Classification stated with evidence before any fix.
- [ ] Reproduction attempted with escalating techniques; commands + counts
      recorded (or the honest why-not).
- [ ] Exactly ONE cause fixed in this case.
- [ ] Product-side races routed as product bugs, test kept honest.
- [ ] No retries/sleeps/loosened assertions/deletions as "fixes".
- [ ] Stability proven by repeated runs under the reproducing condition,
      with counts, not one green run.
- [ ] Quarantine actions carry owner + ticket + expiry.

## Gotchas

- Pass-on-retry in CI is a flake SIGNAL being suppressed — treat retry
  telemetry as the case intake queue, not as the fix.
- "Fails only in CI" usually means resource pressure, TZ/locale, or worker
  parallelism — pin those locally before blaming infrastructure.
- Multiple distinct failure messages from one test = likely multiple causes;
  fixing one and seeing "still flaky" is expected — file separate cases.
- A sleep that "fixes" it confirms a race and fixes nothing — the condition
  the code awaits is the fix.
- Time bombs: tests failing near midnight, month-end, or DST transitions are
  environment flakes with a schedule — check failure timestamps for clustering.
- Deleting the flaky test deletes the coverage AND the evidence of a
  possible product race — curation is a decision for
  `regression-suite-curator` with the case report attached.

## Stop Conditions

- Cannot reproduce after the escalation ladder → report techniques tried
  with counts, park with enhanced logging/telemetry on next CI occurrences —
  do NOT guess-fix an unreproduced flake.
- Reproduction demonstrates a product-side race with user impact → stop
  test-side work; route immediately as a product bug with the reproduction.
- The "fix" would be a retry/sleep/weakened assertion because the real fix
  needs product refactoring → surface the tradeoff for a scoped decision
  instead of silently degrading the test.
- Flake source is shared CI infrastructure beyond the repo → route to the
  infra owner with evidence; don't mutate tests to mask infra.

## Supporting Files

- [references/flake-taxonomy.md](references/flake-taxonomy.md) — the
  classification taxonomy with signatures, the reproduction escalation
  ladder with runner-specific repeat/shuffle commands, and the
  forbidden-fix list with allowed alternatives.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the unit/build/flake/data
  cluster and against `systematic-debugger`.
