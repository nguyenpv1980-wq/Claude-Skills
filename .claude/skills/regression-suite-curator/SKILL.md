---
name: regression-suite-curator
description: Curate WHAT belongs in the regression suite and at which tier — promotion criteria (every fixed bug gets a regression test; which tests earn smoke-tier status), retirement/demotion with written rationale (dead features, duplicated coverage, negative-value tests — never silent deletion), tier design (smoke/PR/full/nightly) against runtime budgets, duplicate-coverage detection, the quarantine registry (owner + ticket + expiry, enforced), and per-test ownership. Produces a curation decision list with evidence; permanent security regression tests retire only via the human-approval path. Use when asked what belongs in regression/smoke, to trim a slow or bloated suite, to formalize bug-fix→regression-test promotion, to clean up a quarantine graveyard, or when suite runtime outgrows its budget. Do NOT use to diagnose WHY a test flakes (flaky-test-detective), design the CI/retry machinery (qa-automation-architect), audit what tests cover (test-coverage-mapper), or write tests (engineer skills).
---

# Regression Suite Curator

## Purpose

Keep the regression suite worth its runtime: every test in it earns its
place, every fixed bug that matters is represented, tiers match their
budgets, quarantine is a workflow instead of a graveyard, and nothing
disappears silently. The deliverable is a curation decision list — promote /
retain / demote / retire / quarantine-action per test group, each with
evidence and rationale — plus the standing promotion and retirement rules
the team applies between curation passes.

## Use When

- Use when: asked what belongs in the regression or smoke suite, or which
  tests should gate a release.
- Use when: the suite is slow/bloated and needs trimming against a runtime
  budget without losing protection.
- Use when: formalizing bug-fix→regression-test promotion (roadmap #190
  regression-first thinking) or smoke-tier membership criteria.
- Use when: the quarantine list has become permanent storage — entries
  without owner/ticket/expiry.
- Use when: after an incident, ensuring the incident's regression tests are
  promoted to the right tier.
- Do NOT use when: a test fails intermittently and needs diagnosis —
  `flaky-test-detective` (its case reports are curation INPUT).
- Do NOT use when: designing CI mechanics, sharding, retry policy —
  `qa-automation-architect` (it sets tier budgets; this skill fills tiers).
- Do NOT use when: mapping what tests cover requirements —
  `test-coverage-mapper` (its gap list feeds promotion; its theater list
  feeds retirement).
- Do NOT use when: writing the tests being promoted — engineer skills.

## Inputs to Inspect

1. The suite inventory: tests per tier, runtimes, last-failure dates,
   pass-on-retry counts, quarantine tags — from CI history, not memory.
2. Coverage context: `test-coverage-mapper` output (theater tests, gaps),
   duplicate-coverage candidates (many tests through one behavior).
3. Bug/incident history: fixed bugs and whether each has a regression test;
   incident postmortems naming untested paths.
4. Tier budgets and gating rules from the automation blueprint / QA
   strategy.
5. Ownership signals: who maintains what (CODEOWNERS, git blame on test
   dirs).

## Workflow

1. **Build the evidence table first:** per test/group — tier, runtime,
   failure history (real catches vs flake noise vs never-failed), what
   behavior it guards, duplication candidates. Curation without CI-history
   evidence is taste, not curation.
2. **Apply promotion rules:** every fixed bug of severity ≥ threshold has a
   regression test at the layer that would have caught it (gaps become
   engineer-skill work items); smoke tier = the few tests proving critical
   journeys/invariants, each with a named reason; incident-derived tests
   promoted per postmortem. Rules catalog in
   [references/curation-rules.md](references/curation-rules.md).
3. **Apply retirement/demotion rules with written rationale per test:**
   dead-feature tests (feature removed → test retires WITH the feature's
   removal PR), duplicated coverage (keep the cheapest reliable
   representative, cite the survivor), theater tests (from the mapper —
   retire or repair), never-failed-and-unreachable tests (demote to nightly
   or retire with evidence they can't fail meaningfully). NO silent
   deletion: every retirement names what protection is lost and why that's
   acceptable.
4. **Guard the protected classes:** permanent security regression tests
   (from `multi-tenant-security-tester`, incident fixes) retire ONLY via
   `human-approval-boundary` with written rationale — flake or slowness is
   never sufficient cause on its own.
5. **Enforce the quarantine registry:** every quarantined test has owner +
   ticket + expiry; expired entries get a decision NOW (diagnose via
   `flaky-test-detective`, fix, or retire with rationale) — quarantine is a
   queue, not a destination.
6. **Fit tiers to budgets:** with the automation blueprint's budgets,
   assign/demote until tiers fit — by evidence (catch-rate per runtime),
   not alphabetically; record what moved and why.
7. **Publish the decision list + standing rules**, route implementation
   (test writing → engineer skills; deletions → normal review via
   `reviewable-diff-discipline`), and set the next curation cadence.

## Output Format

```
CURATION REPORT — <suite/scope> @ <date>
Evidence table: <test/group → tier, runtime, failure history, guards-what,
                duplication candidates>
Decisions:
  PROMOTE  <test/gap> → <tier> — <rule + evidence>
  RETAIN   <test> — <earns place because…>
  DEMOTE   <test> → <tier> — <evidence>
  RETIRE   <test> — <rationale + protection lost + why acceptable>
  QUARANTINE-ACTION <test> — <diagnose|fix|retire + owner/ticket/expiry>
Protected-class check: <security regressions touched? → human-approval path>
Tier fit: <tier → runtime before/after vs budget>
Standing rules: <promotion + retirement + quarantine rules going forward>
Handoffs: <new tests → engineer skills; flake cases → flaky-test-detective;
          deletions → review via reviewable-diff-discipline>
Next curation: <cadence/trigger>
```

## Validation Checklist

- [ ] Every decision cites CI-history evidence, not intuition.
- [ ] Every fixed bug ≥ threshold maps to a regression test or a work item.
- [ ] Smoke tier members each have a named critical-journey reason.
- [ ] Every retirement has written rationale naming the protection lost.
- [ ] Security regression retirements routed through
      `human-approval-boundary` — zero exceptions.
- [ ] Quarantine registry has owner + ticket + expiry on every entry;
      expired entries decided.
- [ ] Tier runtimes fit budgets after decisions.
- [ ] No tests deleted in this pass — decisions route to normal review.

## Gotchas

- "This test never fails, cut it" — never-failing tests include your best
  guards (they prevent the class of change that would fail them); retire on
  unreachability/duplication evidence, not on quietness.
- Trimming by runtime alone deletes slow-but-only protection for hairy
  paths; catch-rate-per-runtime needs the "what does it guard" column.
- Duplicate-looking tests may assert different failure modes of one
  behavior — read assertions (the mapper's rubric) before declaring
  duplication.
- Quarantine-with-expiry silently becomes quarantine-forever the first time
  an expiry passes unenforced — the registry check is the enforcement.
- A curation pass that lands as one giant deletion PR is unreviewable —
  batch retirements small, per `reviewable-diff-discipline`.

## Stop Conditions

- No CI history/runtimes are accessible → curation would be taste; get the
  data or reduce scope to the quarantine registry (which needs only its own
  records).
- A retirement candidate is a security regression test or guards a
  compliance obligation → `human-approval-boundary`, always.
- Suite runtime can't fit budgets without losing named protection →
  escalate the tradeoff (budget vs protection) to the strategy owner
  instead of quietly cutting.
- Asked to also delete the retired tests right now → deletions go through
  normal review as scoped diffs; hand off the decision list.

## Supporting Files

- [references/curation-rules.md](references/curation-rules.md) — promotion
  rule catalog (bug/incident/smoke), retirement evidence standards,
  quarantine registry schema, tier-fit worksheet.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the unit/build/flake/data
  cluster and against `test-coverage-mapper`.
