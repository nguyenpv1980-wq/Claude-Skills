---
name: local-ci-mirror-preflight
description: 'Before any commit, mirror CI locally: read the CI workflow definitions, derive the closest local equivalent of every PR-triggered check, run them, and verify the SAME checks pass on clean mainline FIRST via a separate git worktree (never by flipping a shared checkout). Classify every failure — PR-caused / pre-existing-on-main / CI-infrastructure / cannot-determine-locally; only PR-caused failures block; pre-existing ones are reported, not absorbed. Includes a declared docs-only lightweight path; the preflight record feeds the closeout. Runs only the repo''s own declared checks. Use before committing or pushing non-trivial work, when CI fails on things never run locally, or to distinguish your breakage from main''s. Do NOT use as the release ship/no-ship gate (release-readiness-reviewer), to choose validation DEPTH (risk-tiered-validation-selector picks the tier this mirrors), to architect shard/resume machinery (sharded-validation-with-resume), or to design the pipeline (ci-pipeline-architect).'
---

# Local CI Mirror Preflight

## Purpose

Never learn from CI what you could have learned at your desk — and never
blame your diff for main's breakage. This skill is the per-commit VERIFY
discipline from the extraction evidence (both source repos enforce it): CI
workflow definitions are the source of truth for what a PR must pass, so
before committing, derive the closest local equivalent of every PR-triggered
check, run the same set on clean mainline FIRST (the baseline), then on your
work, and classify every failure by cause. The output is a preflight record
good enough to paste into the closeout: what ran, how long, what failed, and
whose fault it is — with a fixed four-class taxonomy instead of vibes.

## Use When

- Use when: about to commit or push non-trivial work (the per-commit gate).
- Use when: CI keeps failing on checks that were never run locally, or
  local "it passes" keeps meaning a different command than CI runs.
- Use when: a failure appeared and you must distinguish PR-caused from
  pre-existing-on-main before touching anything.
- Use when: the change is docs-only — take the explicit lightweight path
  (see Workflow step 6), not a silent skip.
- Do NOT use when: gating a release/merge decision on evidence across
  migrations, rollback, flags — that is `release-readiness-reviewer`
  (release-scoped); this skill is per-commit.
- Do NOT use when: deciding how MUCH validation this change class needs —
  that is `risk-tiered-validation-selector`; it picks the tier, this skill
  mirrors and runs what the tier requires.
- Do NOT use when: designing shards, resume semantics, or the aggregate CI
  gate — that is `sharded-validation-with-resume`; where shards exist, this
  preflight INVOKES the shard runner locally rather than reinventing it.
- Do NOT use when: adding/changing CI stages or required checks — that is
  `ci-pipeline-architect`.

## Inputs to Inspect

1. The CI workflow definitions (e.g. `.github/workflows/*.yml`): which
   workflows trigger on `pull_request` (and on what paths), what each job
   actually runs (commands, versions, env), and which checks are REQUIRED
   by branch protection.
2. The repo's local runner conventions: package scripts, Makefile,
   validation scripts — the intended local equivalents where they exist.
3. Current mainline CI status (is main green right now?) — recent runs on
   the default branch inform the baseline expectation.
4. The working tree state: what is about to be committed (the preflight
   runs against exactly that), and whether OTHER sessions share this
   checkout (drives the worktree rule).
5. The change's tier if `risk-tiered-validation-selector` is in play —
   docs-only/fast/full changes which derived checks are in scope.

## Workflow

1. **Derive the check list from the workflow definitions** — not from
   memory, not from README claims. For each PR-triggered job, record: CI
   command → closest local equivalent → any honest gap (matrix versions,
   services, secrets you can't reproduce). A check with no derivable local
   equivalent is recorded as `cannot-determine-locally`, not skipped
   silently. (Derivation table format:
   [references/preflight-procedure.md](references/preflight-procedure.md).)
2. **Establish the mainline baseline FIRST — in a separate worktree.**
   `git worktree add <scratch-path> origin/main` (after `git fetch`), run
   the derived checks there, record results and durations, then
   `git worktree remove <scratch-path>`. Never flip a shared checkout to
   main and back — concurrent sessions in one checkout is a known collision
   hazard; the worktree makes the baseline non-destructive.
3. **Run the same derived checks on the work** (the exact tree state to be
   committed). Capture real output and durations — a check that produces no
   observable output did not run.
4. **Classify every failure** into exactly one:
   - `PR-caused` — fails on work, passes on baseline → yours; fix before
     commit.
   - `pre-existing-on-main` — fails on baseline too → NOT yours to absorb
     silently; report it (and do not "fix" it inside this PR — that is
     scope drift; route it to its own task).
   - `CI-infrastructure` — env/runner/network/tooling cause, not product
     code (rate limits, missing local service); state the evidence.
   - `cannot-determine-locally` — no faithful local equivalent; named as a
     residual risk the PR carries to real CI.
   A timeout is an infrastructure-class signal first — distinguish
   timed-out from failed-assertions before classifying (and never raise a
   timeout just to convert red to green).
5. **Gate the commit:** proceed when every PR-triggered check is green
   locally or classified non-blocking (pre-existing / infra /
   cannot-determine, each with evidence). A PR-caused failure blocks.
6. **Docs-only lightweight path (explicit, not silent):** when the diff
   matches the repo's docs-only definition (compose
   `risk-tiered-validation-selector`; workflow path-filters often encode
   it), the preflight reduces to: link/reference sanity + any docs-scoped
   CI jobs + confirmation that NO code path is touched. State "docs-only
   path taken" in the record — the path is a declared classification, not
   an exemption from having one.
7. **Record the preflight** (checks, baseline vs work results, durations,
   classifications, gaps) — this block is the closeout's validation
   evidence (`ai-closeout-reporter`).

## Output Format

```
LOCAL CI MIRROR PREFLIGHT — <branch> @ <sha> (vs origin/main @ <sha>)
Derived checks (from .github/workflows/):
  | CI job → local equivalent | baseline (main) | work | duration | gap |
Failures classified:
  <check> — PR-caused | pre-existing-on-main | CI-infrastructure |
  cannot-determine-locally — <evidence for the class>
Docs-only path: taken (<matching definition>) | not applicable
Verdict: COMMIT (all green / non-blocking classified) | BLOCKED (<PR-caused list>)
Residual risk to real CI: <cannot-determine items, matrix gaps>
```

## Validation Checklist

- [ ] Check list derived from the workflow files themselves — every
      PR-triggered job accounted for (run, or classified with a reason).
- [ ] Baseline ran on clean mainline in a separate worktree BEFORE judging
      the work's failures; worktree cleaned up after.
- [ ] Every failure carries exactly one class WITH evidence; nothing
      PR-caused is outstanding at commit time.
- [ ] Pre-existing failures reported, not silently fixed inside this PR.
- [ ] Durations captured; timeouts distinguished from assertion failures.
- [ ] Docs-only path, if taken, is declared with the matching definition.
- [ ] The preflight record exists in a form the closeout can cite.

## Gotchas

- **Mirroring the README instead of the workflows:** the repo's docs may
  say `npm test` while CI runs a coverage-gated variant with services. The
  workflow YAML is the contract; derive from it.
- **Skipping the baseline to save time** makes every failure ambiguous —
  you either absorb main's breakage into your PR or ship yours blamed on
  main. The baseline is what buys the classification.
- **Shared-checkout flipping:** `git checkout main && test && checkout -`
  in a checkout another session is using corrupts BOTH sessions' work. The
  separate worktree is non-negotiable in shared environments.
- **Local-green ≠ CI-green:** version matrices, OS differences, and
  secret-gated jobs make some checks unmirrorable — that is what
  `cannot-determine-locally` is FOR; claiming full local parity is
  overclaiming.
- **Fixing main's failures in your PR** feels helpful and is scope drift
  with a side of false attribution — report, route, keep your diff clean
  (`reviewable-diff-discipline`).
- **Timeout masking:** raising a timeout until red turns green converts an
  infrastructure signal into a fake pass; smallest-safe-fix (split, reduce
  setup, rerun) and record it.

## Stop Conditions

- Asked to commit despite an unexplained PR-caused failure ("CI will tell
  us") → refuse the shortcut; state the failing check and the fix path.
- Asked to skip the mainline baseline AND classification is needed (a
  failure exists) → stop: without a baseline the classes are guesses; run
  the baseline or downgrade all claims to `cannot-determine`.
- The workflow definitions themselves are unreadable/absent (no CI
  configured) → stop and say so; offer the repo's stated local checks as a
  declared substitute, labeled "no CI to mirror".
- Mirroring would require secrets or production services locally → never
  copy secrets to reproduce CI; classify those checks
  `cannot-determine-locally` and carry the residual.

## Supporting Files

- [references/preflight-procedure.md](references/preflight-procedure.md) —
  the derivation table format, worktree baseline commands, per-class
  evidence standards, duration capture, and a worked example.
- `evals/evals.json` — behavior cases incl. pre-existing-failure handling
  and refusing to skip the baseline.
- `evals/trigger-evals.json` — discrimination against
  `release-readiness-reviewer`, `risk-tiered-validation-selector`,
  `sharded-validation-with-resume`, and `ci-pipeline-architect`.
