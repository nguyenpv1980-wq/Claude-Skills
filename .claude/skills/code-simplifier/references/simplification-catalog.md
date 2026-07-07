# Known-Safe Simplification Move Catalog

Supporting detail for `code-simplifier`. Read on demand. Every move lists its
preconditions — a move applied without its preconditions is a rewrite.

## The catalog

| Move | Preconditions | Behavior-change tells to check |
| --- | --- | --- |
| **Dead-code removal** | No static refs AND no dynamic refs (reflection, string dispatch, DI, templates, cron/CLI entry points, external consumers) AND git history shows no recent "temporarily disabled" | Side effects at import/module-load time of the "dead" file |
| **Inline needless indirection** (wrapper that only delegates) | Single caller or all callers get identical behavior; wrapper adds no logging/retry/contract | Wrapper was a seam for tests/mocks; its name carried domain meaning |
| **Guard clauses / flatten nesting** | Conditions are side-effect-free; early return doesn't skip cleanup (finally/defer/unlock) | Changed evaluation order of conditions; skipped `finally` |
| **Deduplicate into one function** | The copies are the same *domain concept*, not coincidentally similar; call sites tolerate one shared change point | Copies were diverging on purpose; different error handling per copy |
| **Idiomatic replacement** (hand-rolled loop → stdlib/builtin) | Idiom has identical edge behavior (empty input, None, NaN, ordering, stability) | Sort stability; integer vs float division; lazy vs eager evaluation |
| **Dead-parameter removal** | All callers pass the same value or none; no keyword/optional external callers | Public API surface; serialized call formats (queues, RPC) |
| **Collapse trivial single-use temp variables** | Variable adds no name-as-documentation value | Evaluation order across the collapsed expression; debugger ergonomics |
| **Replace comment-explained block with named function** | The extraction is pure motion (no logic edits in the same step) | Closure capture (`this`, nonlocal) changes binding |

## Moves that look safe and are NOT (always "not done" or separate task)

- Changing exception types "for consistency" — callers match on types.
- Reordering object keys / log fields — anything downstream may parse them.
- Tightening input validation while simplifying — that's a behavior change.
- Swapping recursion↔iteration on user-controllable depth — stack behavior
  is observable (overflow vs completion).
- "Simplifying" concurrency primitives (removing a lock that "can't
  contend") — needs its own analyzed change.
- Renaming exported/public symbols — API change, own task.

## Characterization-test recipe (for uncovered targets)

1. Call the target with representative inputs: happy path, empty/None/zero,
   boundary sizes, and one malformed input.
2. Assert on whatever the current behavior IS (including current error types
   and messages) — the point is pinning, not judging.
3. Name them `characterization_*` so future readers know they encode
   "current" not "correct".
4. Suspected bugs discovered while pinning go in the report as findings;
   do not fix them inside the simplification (the fix would then be invisible
   in the diff noise).

## Complexity signals worth reporting

Lines of code, maximum nesting depth, branch count, number of returns, and
count of distinct abstractions a reader must hold. Report before→after for
the target only — repo-wide metrics are noise here. If a signal got worse
(e.g., lines up because a dense one-liner was expanded for readability), say
so and why that is the better trade.
