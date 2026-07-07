---
name: systematic-debugger
description: Drive an unknown-cause bug to its root cause through the fixed sequence reproduce → reduce → isolate → fix one thing → verify → prevent, with evidence at every step and no shotgun fixes. Use when something fails and the cause is not yet known — an intermittent failure, a regression since a release, wrong output with no obvious source, an error only in one environment. Ranks hypotheses and proves or disproves them instead of guessing; changes exactly one thing per fix attempt; never calls a symptom a root cause without evidence. Do NOT use when the cause is already isolated (implement the fix with tdd-engineer) or for whole-repo health assessment (full-codebase-auditor).
---

# Systematic Debugger

## Purpose

Replace guess-and-check debugging with an evidence chain: a reliable
reproduction, a reduced minimal case, an isolated cause proven by prediction
("if this is the cause, then X will happen when I do Y"), a single-variable
fix, verification against the original reproduction, and a prevention step so
the class of bug does not return. The output is a root cause the reader can
check — not "it works now."

## Use When

- Use when: a failure's cause is unknown — wrong output, crash, hang,
  intermittent test, environment-specific error.
- Use when: something regressed after a release, upgrade, or config change
  and nobody knows which change did it.
- Use when: a previous "fix" didn't hold — symptom returned, cause was never
  actually found.
- Do NOT use when: the root cause is already isolated — go implement the fix
  (`tdd-engineer` turns the reproduction into the regression test).
- Do NOT use when: nothing is failing and the ask is overall code health —
  that is `full-codebase-auditor` or `principal-code-analyst`.
- Do NOT use when: the "bug" is a disagreement between docs and code about
  intended behavior — `source-of-truth-reconciler` decides what's intended.

## Inputs to Inspect

1. The exact symptom: verbatim error text, wrong-vs-expected output, when it
   started, who/what it affects (environment, tenant, user, data shape).
2. Recent changes: commits, merges, dependency bumps, config/infra changes,
   migrations in the suspicion window (`git log`, lockfile diff, deploy log).
3. Evidence streams: logs, stack traces, metrics, traces around failing
   instances — collected before forming a favorite theory.
4. The failing path's code and tests — read as-is, not as remembered.
5. Environment deltas when it fails only somewhere: versions, env vars,
   data volume, permissions, concurrency.

## Workflow

1. **Reproduce.** Build the smallest command/test/script that shows the
   failure on demand; record the exact invocation and failure output. For
   intermittent failures, find the frequency amplifier (loop it, add load,
   fix the seed) until reproduction is statistically reliable. If
   reproduction is impossible, say why (data gone, prod-only permissions) and
   continue on logs/traces with confidence explicitly downgraded.
2. **Reduce.** Shrink input, config, and code path until every remaining
   element is necessary for the failure. The minimal case usually names the
   suspect on its own.
3. **Isolate.** List candidate causes and rank by evidence fit and prior
   probability. Test the top hypothesis with a prediction it must satisfy
   (bisect the change window, toggle the suspect flag, pin the suspect
   dependency, instrument the suspect boundary). A hypothesis survives only
   if its prediction comes true; record disproofs — they are progress.
4. **Fix one thing.** Change exactly the isolated cause. No drive-by cleanup,
   no "also hardened X while there" — a multi-variable fix destroys the
   evidence chain and hides which change worked.
5. **Verify.** Re-run the original reproduction (not just the reduced case):
   red before the fix, green after, wider suite still green. For intermittent
   bugs, re-run enough iterations to beat the original failure rate.
6. **Prevent.** Add the regression test (the reproduction, kept), and where
   warranted an assertion, a lint rule, monitoring, or an alert. State the
   root cause in one sentence a reviewer can falsify.

## Output Format

```
DEBUGGING REPORT — <symptom>
Symptom: <verbatim error / wrong output, scope, since when>
Reproduction: <exact command + failure output> (reliability: n/n runs)
Reduction: <minimal failing case>
Hypotheses: <H1..Hn — ranked; each: prediction tested → confirmed/disproved,
            with evidence>
Root cause: <one falsifiable sentence, with file:line>
Fix: <the single change made>
Verification: <original repro red→green, suite result, iteration count if
              intermittent>
Prevention: <regression test added; monitoring/guard if any>
Unknowns kept: <what was not proven, and its risk>
```

## Validation Checklist

- [ ] Reproduction recorded with the exact command and real output (or the
      impossibility explained and confidence downgraded).
- [ ] Each hypothesis tested via a stated prediction; disproofs recorded.
- [ ] Root cause is falsifiable and cites code, not vibes ("race in X when Y"
      not "timing issue").
- [ ] Exactly one variable changed by the fix.
- [ ] Verification re-ran the ORIGINAL reproduction, plus the wider suite.
- [ ] Regression test (or explicit reason none is possible) added.
- [ ] No unrelated edits shipped with the fix.

## Gotchas

- The bug is rarely where the error surfaces; stack traces show the victim,
  not always the culprit — follow data flow upstream.
- "It stopped failing" after a change you didn't isolate is the most seductive
  false green — intermittent bugs pass runs all the time. Beat the base rate.
- Bisecting with a dirty working tree or flaky suite produces lying bisects;
  stabilize the test before trusting `git bisect`.
- Fixing the reduced case but never re-running the original reproduction
  ships a fix for the wrong layer.
- Two bugs can share one symptom; verification failing after a proven fix may
  mean bug #2, not disproof of bug #1 — re-reduce.
- Debugging output (prints, verbose flags, temp instrumentation) must be
  stripped before the fix ships; list it and remove it.

## Stop Conditions

- Reproduction or investigation would require production data access,
  destructive operations, or config changes in shared environments →
  `human-approval-boundary` first.
- The root cause lands in security/tenant-isolation behavior → stop and
  surface before fixing; the fix may need review as a security change.
- The isolated cause is a third-party defect → document the evidence, pin or
  work around with approval, report upstream; do not fork silently.
- Budget exhausted with hypotheses disproven and no reproduction → report the
  evidence map and unknowns honestly rather than shipping a speculative fix.

## Supporting Files

- [references/isolation-tactics.md](references/isolation-tactics.md) —
  bisection recipes, intermittent-failure amplifiers, environment-delta
  tables, and instrumentation patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `tdd-engineer` and
  `docs-first-implementer` (implementation cluster).
