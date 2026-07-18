---
name: release-readiness-reviewer
description: 'Run the ship/no-ship gate for a specific release on EVIDENCE, not vibes — every dimension is answered by a verifiable artifact or recorded as MISSING: CI check states on the release commit (run links), artifact provenance, test signal meaningful for THIS change, migration review (secure-migration-reviewer), a rollback path naming its primitive and rehearsal status (rollback-runbook-author''s artifact), flag defaults, docs, observability readiness, and approvals per change class. Unknown on a blocking item is a No-Go with the evidence that would flip it, never a benefit-of-the-doubt pass. Produces go/no-go, blocking items, risks, and the evidence table. This skill is the PROCEDURE; the same-named read-only subagent composes it. Use when asked whether a release/deploy/merge is ready, to run a release checklist, or to gate a risky change. Do NOT use for line-level review (code-reviewer / security-pr-reviewer), pipeline design (ci-pipeline-architect), or writing the rollback plan (rollback-runbook-author).'
---

# Release Readiness Reviewer

## Purpose

Produce a go/no-go decision for a specific release that a stranger could
audit: an evidence table where every readiness dimension cites a verifiable
artifact (a CI run on the release commit, a migration review, a rollback
runbook, a dashboard) or is honestly recorded as missing — and missing
evidence on a blocking dimension is a No-Go with the exact evidence that
would flip it. The discipline is evidence-not-vibes: "the tests should be
green" and "rollback is just a revert" are the two sentences this gate
exists to catch.

## Use When

- Use when: asked whether a release, deploy, or merge to a
  production-bound branch is ready to ship.
- Use when: running a release checklist or pre-deploy gate for a specific
  change set.
- Use when: a risky change (migration, flag flip, infra change) needs a
  structured readiness pass before production.
- Use when: `ai-closeout-reporter` output for a release-class change needs
  its claims verified against artifacts (compose `agent-governance-audit`
  for full process audits).
- Do NOT use when: reviewing the code itself — `code-reviewer` /
  `security-pr-reviewer` (their findings are inputs here).
- Do NOT use when: designing which gates the pipeline should have —
  `ci-pipeline-architect` builds the gates; this skill demands their
  output for one release.
- Do NOT use when: authoring the rollback plan — `rollback-runbook-author`
  (this gate verifies that artifact exists and is executable, it does not
  write it).
- Note: the same-named read-only SUBAGENT (`.claude/agents/`) composes
  this skill for delegated reviews — same pattern as
  `full-codebase-auditor`.

## Inputs to Inspect

1. The exact release scope: commit range / PR set / artifact version going
   out. No identified scope, no gate.
2. CI state ON THE RELEASE COMMIT: which required checks ran, their
   results, run links — not the branch's general health.
3. The built artifact and its provenance (commit, run id) from the
   pipeline's artifact governance.
4. Migrations in the release: `secure-migration-reviewer` output or its
   absence.
5. The rollback path for THIS release: `rollback-runbook-author` artifact,
   the deployment strategy's rollback primitive, and whether it was ever
   rehearsed.
6. Feature-flag inventory for the change: new flags, their default states,
   kill-switch coverage.
7. Observability readiness: dashboards/alerts covering the new surface
   (`slo-reliability-architect` / `observability-operator` artifacts),
   plus the on-call/comms path if this release fails.
8. Docs/changelog for user-facing changes; approvals recorded for the
   change class (`change-classification-gate` mapping).

## Workflow

1. **Fix the release scope**: exactly what ships — commits, artifact
   version, migrations included, flags touched. Scope ambiguity is a stop,
   not a footnote.
2. **Verify CI evidence on the release commit**: enumerate required checks
   (from branch protection / pipeline design), confirm each ran on the
   shipping commit with its result and run link. A check that is required
   but did not run (renamed job, skipped stage) is a blocking finding, not
   an assumption of green. Retried-to-green runs are noted with their
   first-failure signal.
3. **Verify the artifact**: the thing deploying is the thing that was
   tested — provenance links artifact → commit → CI run. "We'll rebuild it
   during deploy" breaks that chain and is a finding.
4. **Assess test-signal meaningfulness for THIS change**: do the suites
   that ran actually exercise the changed surface (consult
   `test-coverage-mapper` output when available)? A green suite that never
   touches the changed module is recorded as weak signal, not readiness.
5. **Gate migrations**: any schema/data migration in scope requires
   `secure-migration-reviewer` evidence (deploy order, reversibility,
   lock risk). Unreviewed migration = No-Go.
6. **Verify the rollback path**: the runbook exists for this release
   shape, names its primitive (artifact redeploy, traffic flip, canary
   abort, flag kill), covers the migration's reversibility posture, and
   states rehearsal status. "Rollback = revert the commit" without the
   deploy/data story is a blocking finding.
7. **Check flags, docs, observability, approvals**: new behavior defaults
   safe (flag off unless decided otherwise, with the decision cited);
   user-facing changes documented with breaking changes called out;
   dashboards/alerts exist for the new surface and someone is on call;
   approvals match the change class and are recorded.
8. **Decide and report**: Go / No-Go with the single biggest reason first;
   blocking items each with the evidence that would flip them;
   ship-with-awareness risks with their monitoring plan; the full evidence
   table. Unknown on a blocking dimension is No-Go — the gate's job is to
   convert unknowns into named evidence requests, and the release's
   closeout claims route to `ai-closeout-reporter`.

## Output Format

```
RELEASE READINESS — <release/version/scope>
Verdict: <GO / NO-GO — single biggest reason>
Evidence table:
  <dimension — artifact cited (link/path/run id) OR "MISSING: <what would
   provide it>" — pass/blocking/risk>
  (dimensions: CI on release commit, artifact provenance, test signal,
   migrations, rollback path, flags, docs/changelog, observability,
   approvals)
Blocking items: <each: what, why blocking, the exact evidence that flips it>
Ship-with-awareness risks: <each: risk, monitoring plan, owner>
Rollback path check: <primitive named, migration posture covered,
  rehearsal status>
Not verified: <dimensions this review could not reach and why>
```

## Validation Checklist

- [ ] Every dimension cites a verifiable artifact or an explicit MISSING
      entry — zero dimensions passed on assertion ("should be", "usually
      is", "I'm told").
- [ ] CI evidence is from the release commit specifically, with run links;
      required-but-not-run checks were caught.
- [ ] Artifact provenance chains deploy → commit → CI run.
- [ ] Test signal was assessed against the changed surface, not just
      suite-level green.
- [ ] Migrations gated on `secure-migration-reviewer` evidence; rollback
      gated on the runbook artifact — neither re-reviewed inline here.
- [ ] Every unknown on a blocking dimension produced a No-Go, not a pass.
- [ ] Blocking items each name the evidence that would flip them.
- [ ] The verdict leads with the single biggest reason.

## Gotchas

- The branch being green is not the release commit being green — last-
  minute merges and cherry-picks ship untested combinations. Always pin
  evidence to the shipping SHA.
- Required checks silently stop running when jobs are renamed; branch
  protection reports them as pending/stale, and humans read the overall
  green tick anyway.
- Retry-to-green hides real signal: a check that failed twice and passed
  once is flake evidence (`flaky-test-detective`) or a real intermittent
  bug — record it, don't launder it.
- Rollback confidence decays: a runbook rehearsed against last quarter's
  schema may not survive this release's migration — check the runbook's
  assumptions against THIS scope.
- Friday-evening and holiday-eve releases fail the observability
  dimension socially: dashboards exist but nobody is watching; on-call
  coverage is part of readiness.
- A flag defaulted ON because "it's basically done" converts deploy risk
  into release risk with no kill switch decision on record.

## Stop Conditions

- The release scope cannot be pinned to exact commits/artifacts → stop;
  a gate on an ambiguous scope certifies nothing.
- Evidence systems are unreachable (no CI access, no artifact store) →
  report which dimensions are unverifiable and stop short of a verdict;
  an evidence-based gate without evidence access is theater.
- The verdict would be overridden ("we're shipping anyway, just sign it
  off") → decline to convert a No-Go into a Go; record the blocking items
  and route the override decision to `human-approval-boundary` — the
  override is a human's to make and to own on the record.
- A blocking item's fix is requested inline ("just write the rollback
  plan now") → hand off to the owning skill; the gate does not author
  the evidence it demands.

## Supporting Files

- `references/readiness-evidence.md` — the dimension-by-dimension evidence
  table template with pass/blocking criteria per dimension.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the delivery cluster
  (`ci-pipeline-architect`, `rollback-runbook-author`), against shipped
  `secure-migration-reviewer` / `code-reviewer`, and the skill-vs-subagent
  namespace note.
