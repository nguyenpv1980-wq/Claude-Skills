---
name: risk-tiered-validation-selector
description: 'Machine-classify a change''s touched files into impact classes that select validation DEPTH — docs-only fast path, fast tier, or full tier — with a classifier that FAILS CLOSED: unmatched, ambiguous, or error cases escalate to full, never down. Ships tier check bundles, an explicit docs-only definition PLUS a "never docs-only" list (workflows, scripts, schema/migrations, auth/RLS, lockfiles, agent-instruction files), forced-full lists for high-risk surfaces, and diffable rules; aggregation is max-over-files, no averaging. Routes validation COST where change-classification-gate routes APPROVAL — compose, don''t merge. Use when picking fast vs full validation for a change, designing tiered validation, when docs-only changes waste full CI, or when risky files sneak through light checks. Do NOT use to set approval paths or scope lock (change-classification-gate), to run the selected tier (local-ci-mirror-preflight executes it), or to architect the full tier''s shards (sharded-validation-with-resume).'
---

# Risk-Tiered Validation Selector

## Purpose

Spend validation where risk lives — mechanically, and erring expensive. Flat
validation policy fails in both directions: full CI on a typo teaches people
to resent (and bypass) validation, while light checks on a migration is how
incidents start. The evidence pattern (Repo B's impact classifier + tier
protocol, corroborated by Repo A's docs-only rule) is a CLASSIFIER whose
input is the changed file set and whose output is a validation tier — with
the defining property that it FAILS CLOSED: a file no rule matches, an
ambiguous match, or a classifier error selects FULL validation. Cheap tiers
are earned by explicit rules; expensive is the default for the unknown. This
skill designs that classifier and its tier definitions as reviewable repo
artifacts.

## Use When

- Use when: deciding, for a concrete change, whether the docs-only path,
  fast tier, or full tier applies (running the classification).
- Use when: designing or overhauling a repo's tiered-validation scheme —
  the tiers, the rules, the lists.
- Use when: docs-only changes are burning full-CI minutes, or risky files
  keep riding through light validation.
- Use when: the docs-only definition is contested ("it's just a config
  tweak") and needs a written boundary.
- Do NOT use when: deciding approval paths, human sign-off, or scope lock —
  that is `change-classification-gate`; it routes changes to APPROVAL and
  this selector routes them to validation COST. A change gets both,
  independently.
- Do NOT use when: actually executing the selected tier before a commit —
  that is `local-ci-mirror-preflight` (it mirrors and runs; this skill only
  selects).
- Do NOT use when: the full tier's internals (shards, resume, aggregate
  gate) are the subject — that is `sharded-validation-with-resume`.
- Do NOT use when: adding the classifier job to CI — the wiring composes
  `ci-pipeline-architect`.

## Inputs to Inspect

1. The changed file set (for a live classification): `git diff --name-only`
   against the PR base — the classifier's only input is files, never the
   author's description of them.
2. The repo's risk topology (for design): where schema/migrations, auth/RLS,
   payment paths, CI workflows, agent-instruction files, generated code, and
   pure-docs trees live — these seed the lists.
3. The existing validation inventory: what checks exist and their costs/
   durations — tiers are bundles of real checks, not aspirations.
4. `change-classification-gate`'s class definitions where present — the two
   taxonomies should share vocabulary (a schema-migration class maps to
   forced-full) without merging responsibilities.
5. History of misroutes: past incidents where a light-validated change broke
   something (candidates for forced-full), and heavyweight runs on trivial
   diffs (candidates for explicit fast rules).

## Workflow

1. **Define the tiers as check bundles:** `docs-only` (reference/link sanity
   + docs-scoped jobs), `fast` (typecheck/lint/build + focused unit scope),
   `full` (everything, incl. the sharded suite where
   `sharded-validation-with-resume` exists). Name real commands/jobs per
   tier — a tier without a check list is a mood.
2. **Write the docs-only definition — positively and negatively.**
   Positive: which paths/extensions are documentation. Negative (the
   "never docs-only" list): CI workflows, scripts, schema/migrations,
   auth/RLS/policy paths, lockfiles/dependency manifests, agent-instruction
   files, generated code — matching ANY of these disqualifies the whole
   change from docs-only regardless of what else it touches.
3. **Write the forced-full list:** surfaces whose risk ignores diff size —
   schema/migrations, auth/RLS, payment/billing, tenant isolation, CI/CD
   definitions, the classifier's own rules file. Any hit → full, no
   averaging.
4. **Write the classification rules as a reviewable artifact** (rule table
   or script design — format:
   [references/classifier-rules.md](references/classifier-rules.md)): ordered
   glob → class mappings, most-specific first, with the LAST rule being the
   fail-closed catch-all: `* → full (unmatched)`.
5. **Fix the aggregation rule:** a change's tier is the MAX tier over its
   files (docs-only < fast < full). One workflow file in a 40-file docs diff
   makes the change full. No file-count thresholds, no averaging.
6. **Fail closed on classifier errors too:** diff unavailable, rules file
   unparseable, glob engine error → full. The classifier must never convert
   its own failure into a cheap tier.
7. **For a live classification, emit the record:** files → matched rule →
   per-file class → aggregate tier → the checks that tier requires (which
   `local-ci-mirror-preflight` then mirrors). Unmatched files are NAMED in
   the record — each is a rules-file gap to close, not an annoyance to
   suppress.
8. **Keep the rules honest over time:** every misroute (light-validated
   breakage) adds a rule or a forced-full entry; the rules file is
   change-controlled like the code it guards (and edits to it are
   themselves forced-full).

## Output Format

```
VALIDATION TIER SELECTION — <branch/PR> (<n> files vs <base>)
Per-file:
  | file | matched rule | class |
  | docs/guide.md | docs/** → docs-only | docs-only |
  | .github/workflows/ci.yml | never-docs-only list | full (forced) |
  | src/lib/util.ts | src/** → fast | fast |
  | tools/gen/output.g.ts | (no rule matched) | full (fail-closed) |
Aggregate tier: FULL (max over files) — because: <the deciding file(s)>
Tier contents: <the named checks/jobs this tier runs>
Rules-file gaps: <unmatched files to add rules for>
```

## Validation Checklist

- [ ] Every tier names its actual checks/commands; docs-only has BOTH a
      positive definition and a never-docs-only list.
- [ ] The rules artifact ends in the fail-closed catch-all; classifier
      errors also route to full.
- [ ] Aggregation is max-over-files; no rule averages, counts files, or
      trusts the PR description.
- [ ] Forced-full list covers the repo's genuinely high-risk surfaces,
      including the classifier's own rules file and CI definitions.
- [ ] For live runs: every file shows its matched rule; unmatched files are
      named as gaps.
- [ ] The selector's vocabulary aligns with `change-classification-gate`'s
      classes without absorbing its approval/scope duties.
- [ ] The rules are a diffable repo artifact, not prose folklore.

## Gotchas

- **Fail-open by generosity:** "it's obviously harmless, call it fast" for
  an unmatched file — the entire design collapses at the first exception.
  Unmatched means full; then ADD THE RULE so next time matches.
- **The renamed/moved file:** renames of risky paths must classify by BOTH
  old and new path (a migration moved is still a migration).
- **Deleted files count:** a deletion under a forced-full path is a
  forced-full change; classifiers that only look at additions miss it.
- **Generated-code blind spot:** generated output looks harmless, but the
  generator input that produced it may not be in the diff; classify
  generated trees explicitly (usually fast-or-full by what consumes them),
  never by "it's autogenerated, skip it".
- **Description trust:** classifying from the PR title/author claim instead
  of the file list re-opens the exact hole the machine classification
  closes.
- **Tier inflation:** if everything ends up full, the fast rules are too
  thin and the selector dies of uselessness — mine the full-tier runs on
  genuinely trivial diffs for safe fast rules. Fail-closed does not mean
  never-fast; it means EARNED-fast.

## Stop Conditions

- Asked to classify an unmatched or never-docs-only file into a cheaper
  tier "just this once" → refuse; fail-closed is the design's load-bearing
  property. The lawful path is a reviewed rules-file change.
- Asked to design tiers with no real check inventory to bundle (nothing to
  select between) → stop; the validation checks must exist first (or route
  to designing them).
- The diff/base cannot be computed (shallow clone, missing base) → the
  classification is FULL by fail-closed error handling; say so rather than
  guessing from filenames at hand.
- Asked to fold approval decisions into the tier output ("full tier implies
  human sign-off, so skip the gate") → refuse; approval routing stays with
  `change-classification-gate` — shared vocabulary, separate authorities.

## Supporting Files

- [references/classifier-rules.md](references/classifier-rules.md) — the
  rules-artifact format (ordered globs, forced-full, never-docs-only,
  catch-all), starter lists, aggregation and error-handling semantics, and
  a worked classification.
- `evals/evals.json` — behavior cases incl. fail-closed on unmatched files
  and mixed docs+workflow diffs.
- `evals/trigger-evals.json` — discrimination against
  `change-classification-gate`, `local-ci-mirror-preflight`, and
  `sharded-validation-with-resume`.
