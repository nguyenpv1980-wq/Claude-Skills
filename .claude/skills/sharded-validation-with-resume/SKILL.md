---
name: sharded-validation-with-resume
description: Design full-tier validation as named functional shards with resume: a shard map assigning every test/check to exactly one shard, a persisted status file, resume that reruns ONLY unfinished shards after a timeout/infrastructure interruption (passes are kept; real FAILURES are never resumed-away), an "uncategorized" catch-shard that fails until new tests are assigned, and parallel shards funneling into ONE aggregate gate job as the sole required check — so docs-only conditional skips can't strand branch protection. Deliverables: shard map, status schema, runner modes, aggregate-gate spec, wiring handoff. Use when full validation times out or reruns from scratch after interruptions, when new tests escape unassigned, or when required checks break on skipped jobs. Do NOT use to choose the tier (risk-tiered-validation-selector), for the per-commit local mirror (local-ci-mirror-preflight invokes this runner), to design the pipeline (ci-pipeline-architect), or to diagnose flakes (flaky-test-detective).
---

# Sharded Validation With Resume

## Purpose

Make the full validation tier survivable and complete. Long full-tier runs
fail two ways: an infrastructure hiccup or timeout at minute 39 throws away
38 minutes of passes (so people stop running the tier), and new tests drift
in unassigned (so "full" quietly stops meaning full). The evidence pattern
(Repo B's shard runner, status file, resume flag, uncategorized shard, and
single aggregate required check) fixes both: named functional shards with
persisted status make interrupted runs resumable, the catch-shard makes
unassigned tests a FAILURE instead of a silence, and the one-aggregate-gate
CI shape keeps branch protection working when conditional skips (docs-only
paths) legitimately skip shard jobs. This skill designs that machinery for a
repo; running it is the preflight's and CI's job.

## Use When

- Use when: full validation exceeds timeout ceilings, or interruptions
  (runner death, network, timeout) force full reruns from scratch.
- Use when: new tests/checks keep landing without being wired into any
  validation bundle — coverage decays silently.
- Use when: branch protection breaks or blocks forever because required
  job names get conditionally skipped (docs-only PRs) — the aggregate-gate
  shape is the fix.
- Use when: designing the full tier's internals for a repo that already
  has (or is adopting) tier selection.
- Do NOT use when: choosing WHICH tier a change runs — that is
  `risk-tiered-validation-selector`; this skill is the full tier's
  internals.
- Do NOT use when: running checks locally before a commit — that is
  `local-ci-mirror-preflight`; where shards exist, the preflight invokes
  this runner rather than re-deriving checks.
- Do NOT use when: designing the pipeline's overall stage graph, secrets,
  or deploy gates — that is `ci-pipeline-architect`; this skill hands its
  CI wiring spec there.
- Do NOT use when: a test fails intermittently and needs diagnosis — that
  is `flaky-test-detective`; resume semantics must never be used to hide
  flakes.

## Inputs to Inspect

1. The current full-tier inventory: every suite/check that "full" is
   supposed to include, with real durations (the shard map is built from
   measured cost, not guesses).
2. Failure history: where timeouts/interruptions actually strike (which
   suites, what ceilings), and any evidence of tests existing in no bundle.
3. The CI system's semantics for required checks, conditional skips, and
   job-level timeouts — the aggregate-gate design must match how the
   platform actually evaluates skipped/required jobs.
4. The runner substrate: script conventions (shell, task runner), where a
   status file can live, and what "workspace persists between steps" means
   in this CI.
5. `risk-tiered-validation-selector`'s tier definitions where present —
   the full tier's contents are its input; the docs-only path explains
   which jobs will legitimately skip.

## Workflow

1. **Draw the shard map:** a small set (typically 3–6) of NAMED functional
   shards (e.g. `core-domain`, `api-integration`, `ui-e2e`, `platform`),
   each owning an explicit list/glob of suites. Every existing test/check
   lands in EXACTLY one shard; balance by measured duration so no shard
   dominates the critical path.
2. **Add the `uncategorized` catch-shard:** its membership rule is "matches
   no other shard's rules"; its content policy is that it must be EMPTY —
   any test landing there runs AND the shard reports failure-by-policy
   until the test is assigned. New tests cannot silently escape full
   validation.
3. **Design the status file** (schema in
   [references/shard-runner-design.md](references/shard-runner-design.md)):
   one persisted record per shard per run-id — `pending | running |
   passed | failed | interrupted(timeout/infra)` with timestamps,
   durations, and the failure class. The file is the resume contract and a
   closeout evidence artifact.
4. **Define runner modes:** full run (all shards, fresh status); `-Resume`
   (rerun ONLY shards not `passed` in the named run — and only when their
   state is `interrupted` or `pending`); single-shard (targeted rerun).
   **Resume law: a `failed` shard (real assertions) is NOT resumable-away —
   it reruns fully after a fix; only timeout/infra interruptions qualify
   for resume.** Completed passes are never re-derived within a run-id;
   a NEW run-id (new commit) invalidates all prior status.
5. **Spec the CI wiring:** shards as parallel jobs → ONE aggregate gate job
   (`needs:` all shards) that is the SOLE required status check. The
   aggregate evaluates shard results explicitly — including the platform's
   skipped semantics on docs-only paths (skipped-by-tier counts as
   satisfied only when the tier selector said so; a skipped shard on a
   full-tier run fails the aggregate). Job names stay stable; branch
   protection references only the aggregate.
6. **Hand the wiring off** to `ci-pipeline-architect`/the human for
   installation (required-check registration, workflow edits) — this skill
   delivers the spec and reference YAML shape, it does not edit pipeline
   files.
7. **Define the maintenance loop:** shard rebalancing triggers (a shard's
   p95 duration nears the ceiling), the rule that shard-map edits ride
   reviewed PRs, and the interaction note for `local-ci-mirror-preflight`
   (local full-tier = invoke this runner, resume included).

## Output Format

```
SHARDED VALIDATION DESIGN — <repo>
Shard map:
  | shard | contents (globs/suites) | measured duration | ceiling |
  | uncategorized | everything unmatched | must be empty — fails by policy |
Status file:     <path, schema, run-id semantics>
Runner modes:    full | -Resume (interrupted/pending only — never failed) | -Shard <name>
Aggregate gate:  sole required check; per-shard evaluation incl. skip semantics
Wiring handoff:  <spec + reference YAML → ci-pipeline-architect/human>
Maintenance:     rebalance triggers; shard-map edits via reviewed PRs
```

## Validation Checklist

- [ ] Every existing test/check maps to exactly one named shard; the
      uncategorized shard is empty at design handoff (or its contents are
      listed as assignment debts).
- [ ] Status file schema distinguishes `failed` from `interrupted` — resume
      eligibility is derivable mechanically.
- [ ] Resume reruns only unfinished/interrupted shards; a new commit/run-id
      invalidates prior passes; failed shards rerun fully after fixes.
- [ ] The aggregate gate is the sole required check; skipped-shard
      semantics are explicit for docs-only tiers AND treated as failure on
      full-tier runs.
- [ ] Shard durations measured, not guessed; no shard dominates the
      critical path.
- [ ] Wiring is a handoff spec; no pipeline files edited by this skill.
- [ ] Flake handling routes to `flaky-test-detective` — nothing in the
      design retries-until-green.

## Gotchas

- **Resume as failure laundering:** the seductive misuse — rerun with
  `-Resume` after a REAL failure so the red shard is skipped and the
  aggregate goes green. The status file's failed-vs-interrupted distinction
  and the resume law exist to make this impossible; any runner that can't
  tell the two apart is unsafe to ship.
- **Stale status across commits:** resuming a run whose passes were earned
  on a different SHA is validating the wrong code — bind the status file to
  run-id + commit.
- **Multiple required shard jobs:** registering each shard as a required
  check is exactly what breaks on conditional skips; the whole point of the
  aggregate is ONE stable required name. (In practice, a production repo's
  merge gate may run two required checks by design — the aggregate
  pattern applies when tiers conditionally skip jobs.)
- **The catch-shard that quietly passes:** an uncategorized shard that runs
  unmatched tests but reports green on empty just recreates the drift it
  was built to stop — empty-or-fail is its contract.
- **A "misc" functional shard** becomes uncategorized-with-a-nicer-name;
  shard names must describe FUNCTION so assignment has a right answer.
- **Hidden pass markers:** a shard "passing" because its runner exited 0
  with zero tests executed (bad glob) — the status file records test
  counts, and zero-executed on a non-empty shard is a failure. Skipped
  execution is not a pass.

## Stop Conditions

- Asked to make resume skip a shard that FAILED with real assertions
  ("resume past it so the gate goes green") → refuse; resume covers
  timeout/infrastructure interruptions only. A red shard reruns after a
  fix.
- Asked to design shards when the full-tier inventory is unknown (no list
  of what "full" contains) → stop; inventory first — sharding an unknown
  set produces an unknown gate.
- Asked to register per-shard required checks despite the conditional-skip
  reality → surface the branch-protection failure mode and deliver the
  aggregate design; installing a known-broken shape needs an explicit
  human override.
- Asked to edit `.github/workflows/**` to install the design → hand off to
  `ci-pipeline-architect`/human; pipeline definitions are outside this
  skill's write scope.

## Supporting Files

- [references/shard-runner-design.md](references/shard-runner-design.md) —
  status-file schema, runner-mode semantics (incl. the resume law),
  aggregate-gate YAML shape with skip semantics, shard-balancing guidance,
  and a worked interruption/resume trace.
- `evals/evals.json` — behavior cases incl. the catch-shard contract and
  refusing resume-past-failure.
- `evals/trigger-evals.json` — discrimination against
  `risk-tiered-validation-selector`, `local-ci-mirror-preflight`,
  `ci-pipeline-architect`, and `flaky-test-detective`.
