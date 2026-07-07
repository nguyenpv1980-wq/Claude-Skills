---
name: code-simplifier
description: Apply behavior-preserving simplifications to explicitly named code — remove dead code and needless indirection, flatten nesting, deduplicate, replace hand-rolled logic with idiomatic equivalents — with tests proving behavior unchanged (green on the same suite before AND after every move). Manual-only by design; it edits working code, so it must never auto-trigger mid-task. Use when the user explicitly asks to simplify, clean up, reduce complexity of, or make more readable a specific file, module, or function. Do NOT use to report findings without editing (code-reviewer), to restructure architecture or change public contracts (architecture-designer + approval), or when the target has no test coverage — coverage comes first or the human accepts the risk explicitly.
disable-model-invocation: true
---

# Code Simplifier

## Purpose

Make named code simpler while provably changing nothing about its behavior.
Every edit is one of a known-safe move set, applied in small steps with the
same test suite green before and after each. The deliverable is the edited
code plus a proof trail: baseline run, per-step moves, final run, and a list
of tempting changes that were NOT made because they would alter behavior.
Simplification that "probably works the same" is a rewrite, and rewrites are
not this skill.

## Use When

- Use when: explicitly asked to simplify, clean up, de-tangle, or reduce the
  complexity of a specific file/module/function.
- Use when: review feedback says "works but convoluted" and the author wants
  it applied as a follow-up change.
- Do NOT use when: the ask is to *find* issues without editing — that is
  `code-reviewer`.
- Do NOT use when: the simplification would move module boundaries or change
  public contracts — that is architecture work with its own approval path.
- Do NOT use when: behavior is wrong — fix bugs first (`systematic-debugger`
  / `tdd-engineer`); simplifying broken code preserves the bug more legibly.
- This skill is **manual-only** (`disable-model-invocation: true`): it edits
  working code, so the human names the target and pulls the trigger — it
  never fires opportunistically mid-task.

## Inputs to Inspect

1. The named target code and everything that depends on it: importers,
   callers, subclass/override sites, reflection or string-based references.
2. The tests covering the target, and their actual coverage of it — run them
   first; note which behaviors are pinned and which are unprotected.
3. Repo conventions and idioms — "simpler" means simpler *in this codebase's
   dialect*, not the model's favorite style.
4. Version-control state: a clean tree, so each step is its own revertible
   commit-sized unit.
5. Git history of the target for traps: "weird" code with a bugfix commit
   behind it is load-bearing weirdness.

## Workflow

1. **Confirm scope with the human:** exactly which files/functions, and the
   no-go list (public API, behavior, dependencies, formatting-only sweeps).
2. **Run the covering tests — record the green baseline.** If coverage over
   the target is missing or thin: stop, report, and either add
   characterization tests first or get the human's explicit written
   acceptance of unprotected simplification.
3. **Plan the moves** from the known-safe catalog (dead-code removal, inline
   needless indirection, flatten nesting with guard clauses, deduplicate,
   idiomatic replacement, dead-parameter removal) — each with a blast-radius
   note. Anything not behavior-preserving goes on the "not doing" list.
4. **Apply one move at a time**; re-run the covering tests after each. A red
   test = revert the move, understand, reclassify (often the "dead" code
   wasn't).
5. **Watch the tells** that a move changes behavior: evaluation order,
   short-circuiting, exception type/timing, iteration order, float math,
   `this`/closure binding, lazy-vs-eager, side effects in removed "dead" code.
6. **Final verification:** full suite (not just the covering tests), plus
   lint/typecheck/build.
7. **Report** with before/after complexity signals (lines, nesting, branch
   count), the move list, and the explicit not-done list with reasons.

## Output Format

```
SIMPLIFICATION — <target>
Baseline: <test command + green result; coverage note>
Moves applied: <n. move — file:line — rationale — suite re-run: green>
Not done (would change behavior or exceed scope): <item — why>
Complexity delta: <lines A→B, max nesting A→B, branches A→B>
Final verification: <full suite / lint / build — real results>
Behavior changed: NONE (or: stop — see report)
```

## Validation Checklist

- [ ] Human explicitly requested simplification of this named target.
- [ ] Green baseline recorded BEFORE the first edit, on the same suite used
      after.
- [ ] Coverage gap handling: characterization tests added or explicit human
      acceptance recorded — never silently proceeded.
- [ ] Each move re-verified individually; no batch of unverified edits.
- [ ] Public contracts, exported names, and observable behavior unchanged
      (including error types and messages callers may match on).
- [ ] "Not done" list present — restraint is a deliverable.
- [ ] No formatting churn beyond edited lines; no drive-by edits outside the
      named scope (`reviewable-diff-discipline`).

## Gotchas

- Dead code that isn't: reflection, string-keyed dispatch, DI containers,
  template references, and external callers (public packages, cron invoking
  a "unused" script) all defeat static "no references" checks.
- Clever one-liners are not simpler — optimize for the next reader, not for
  line count; sometimes the simplification is *expanding* a dense expression.
- Removing a "redundant" try/except or null-check can convert a handled
  failure into a crash — the handler's absence is observable behavior.
- Exception messages, log lines, and dict/JSON key order are behavior when
  anything parses them; grep for consumers before "tidying" strings.
- Deduplicating two similar functions that serve different domains welds
  those domains together — similarity is not sameness.
- A characterization test written from current behavior pins bugs too; note
  suspected bugs found while writing them and report, don't fix in-band.

## Stop Conditions

- No or thin test coverage over the target, and the human has not explicitly
  accepted unprotected simplification → stop and present the two options.
- A planned move turns out to require a behavior or contract change →
  stop that move, list it under "not done", and report — changing it needs
  its own approved task.
- The target is entangled in security/tenant-isolation/money paths where a
  subtle behavior change is high-blast-radius → confirm via
  `human-approval-boundary` before any move.
- Tests are red at baseline → stop; simplification builds only on green.
- Mid-work discovery of an actual bug → report it; do not fix it inside the
  simplification diff.

## Supporting Files

- [references/simplification-catalog.md](references/simplification-catalog.md) —
  the known-safe move catalog with per-move preconditions and behavior-change
  tells; characterization-test recipe for uncovered targets.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `code-reviewer`,
  `principal-code-analyst`, and `full-codebase-auditor` (review/audit cluster).
