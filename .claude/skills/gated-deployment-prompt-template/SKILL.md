---
name: gated-deployment-prompt-template
description: 'Author the reusable operator prompt template gating a RECURRING class of risky operations (migrations, production grants, backfills): operator-filled placeholders (<owner>/<repo>, <tenant-id> — never live identifiers; credentials as env-var names), hard rules with required inputs, stop conditions with safe halt states, backup-then-verify gating (verified backup BEFORE; expected deltas AFTER), per-phase smoke expectations, a required per-run report path, and ETA ranges calibrated from a deployment-history index where every anchor cites the prior run''s report. Uncited operational claims are labeled "unverified — recommend confirming." Authors template + index; NEVER executes the operation. Use to template a migration/grant/backfill prompt or when ETAs are asserted from memory. PROACTIVE — do NOT use for live-incident playbooks (incident-response-runbook), rollback steps (rollback-runbook-author), one migration''s safety review (secure-migration-reviewer), or pipeline governance (merge-is-deploy-governance).'
---

# Gated Deployment Prompt Template

## Purpose

Turn improvised risky operations into templated, evidence-calibrated ones.
When migrations, production grants, or backfills recur, each run improvised
from memory re-decides the safety rails under time pressure — and the rails
lose. The evidence pattern (Repo B's migration-deployment prompt template
plus its deployment-history index) is a reusable OPERATOR PROMPT: the human
fills placeholders, the prompt carries the hard rules, stop conditions,
backup-then-verify gating, smoke expectations, and report requirement — and
its ETA ranges are calibrated from the history index, where every anchor
cites the prior run's report. This skill authors that template and index
for a repo's recurring op class. It never executes the operation; it makes
every future execution start from discipline instead of recall.

## Use When

- Use when: a class of risky operations recurs (migrations, prod grants,
  backfills, data corrections) and each run is currently improvised.
- Use when: deployment ETAs, steps, or "how long does this take" claims are
  asserted from memory with nothing citable behind them.
- Use when: an operation class needs backup-then-verify gating and stop
  conditions written once, reused every run.
- Use when: setting up or back-filling the deployment-history index that
  calibrates future ETAs.
- Do NOT use when: an incident is live and needs a reactive playbook —
  that is `incident-response-runbook` (severity ladder, roles, comms);
  this skill is PROACTIVE templating for planned operations.
- Do NOT use when: authoring the rollback runbook for a change — that is
  `rollback-runbook-author`; this template REFERENCES the rollback artifact
  in its stop-condition paths, it does not write it.
- Do NOT use when: reviewing whether one specific migration is safe
  (reversibility, locks, data loss) — that is `secure-migration-reviewer`;
  the template's hard rules REQUIRE that review as an input, not replace it.
- Do NOT use when: documenting what merging deploys and who owns branch
  protection — that is `merge-is-deploy-governance`; the operator-applied
  remainder it identifies (e.g. migrations) is exactly what THIS template
  gates.

## Inputs to Inspect

1. The operation class as actually run: past run notes/reports, scripts
   involved, environments and tenants touched — the template must match the
   real procedure, not an idealized one.
2. Prior deployment reports, if any — the raw material for the history
   index and its ETA anchors. If none exist, ETAs start honest:
   "unverified — no prior run recorded."
3. The safety artifacts in force for this class: migration review output
   (`secure-migration-reviewer`), rollback artifact
   (`rollback-runbook-author`), authority floors
   (`agent-authorization-matrix` — who may run this at all), any recorded
   approvals (`scoped-approval-register`).
4. Backup and verification substrate: what backup is possible pre-run,
   what queryable signals verify success (expected row deltas, health
   endpoints, smoke queries per phase).
5. Identifier hygiene: which values in past run notes are LIVE (tenant
   ids, project refs, URLs) and must template as placeholders — source
   evidence for this pattern showed live identifiers embedded in the docs;
   the template must not repeat that.

## Workflow

1. **Fix the operation class and its unit** (one migration apply, one
   grant, one backfill run) — one template per class; a template for
   "deployments in general" gates nothing.
2. **Draft the placeholder block:** every run-specific value as
   `<placeholder>` — `<owner>/<repo>`, `<environment>`, `<tenant-id>`,
   `<migration-id>`, `<backup-id>`, `<report-path>`. Credentials appear as
   environment-variable NAMES only, never values. No live identifier
   survives into the template (full structure:
   [references/deployment-prompt-template.md](references/deployment-prompt-template.md)).
3. **Write the hard rules** — non-negotiables for every run of this class:
   validate-only before apply where modes exist; no scope beyond the named
   unit; required inputs present (migration review verdict, rollback
   artifact link, approval citation) or the run does not start.
4. **Write the stop conditions** — conditions that HALT the operation
   mid-run with the state to leave things in: backup unverifiable,
   pre-checks failing, unexpected deltas mid-run, smoke failing after a
   phase, ANY ambiguity about which tenant/environment is being touched.
5. **Encode backup-then-verify gating:** the backup is taken AND VERIFIED
   restorable/readable BEFORE the change (a backup you didn't verify is a
   hope, not a gate); after the change, verify against EXPECTED deltas
   (rows affected, objects created) — "it didn't error" is not
   verification.
6. **Define phase-specific smoke expectations:** per phase of the
   operation, the observable that proves that phase (query results, status
   endpoints) — with expected values, so the operator compares rather than
   interprets.
7. **Require the dedicated report path:** every run writes its report to a
   named location (dated, per-run) covering: placeholders as filled
   (minus secrets), timings per phase, verification outcomes, deviations.
   The report is what feeds the index — no report, no future calibration.
8. **Build/extend the deployment-history index:** one row per run — date,
   operation, duration per phase, outcome, report link. **Every ETA range
   in the template cites index rows (prior reports) as its anchor.** An
   ETA with no citable prior run is labeled
   `unverified — recommend confirming`, and the standing rule goes in the
   template: ANY uncited operational claim carries that label.
9. **Deliver template + index** into the repo docs; posture note: this
   skill authors them — executing a run happens under the template's own
   gates with a human operator, and any agent involvement in execution
   respects `agent-authorization-matrix` floors.

## Output Format

```
GATED DEPLOYMENT PROMPT TEMPLATE — <operation class> (<doc path>)
Placeholders:      <the operator-filled block — env-var NAMES for credentials>
Hard rules:        <non-negotiables incl. required inputs: review verdict,
                    rollback artifact, approval citation>
Stop conditions:   <halt triggers + safe-state-on-halt per trigger>
Backup gate:       verified backup BEFORE; expected-delta verification AFTER
Smoke per phase:   <phase → observable → expected value>
Report path:       <dated per-run location + required contents>
ETA ranges:        <range> (anchor: index rows <ids> → prior reports)
                   uncited claims labeled "unverified — recommend confirming"
DEPLOYMENT HISTORY INDEX — <index path>
  | date | operation | phase durations | outcome | report |
```

## Validation Checklist

- [ ] Zero live identifiers or secret values in template or index —
      placeholders and env-var names only.
- [ ] Hard rules name their required inputs (migration review, rollback
      artifact, approval) — a run cannot lawfully start without them.
- [ ] Every stop condition states the safe state to halt INTO, not just
      "stop".
- [ ] The backup step verifies the backup before the change; the
      verification step compares against expected deltas after.
- [ ] Each smoke expectation has an expected value, not "check it looks ok".
- [ ] Every ETA range cites its index anchor; every uncited operational
      claim carries the unverified label.
- [ ] The per-run report path is required by the template and feeds the
      index (the calibration loop closes).
- [ ] The template's execution posture is explicit: human operator, agent
      participation within matrix floors.

## Gotchas

- **Live identifiers fossilized in templates:** the source evidence for
  this pattern embedded a real tenant id in the deployment prompt —
  copy-paste convenience that leaks and rots. Placeholders are the rule;
  an example VALUES file can live separately under the repo's secrecy
  conventions.
- **ETA folklore:** "takes about 20 minutes" with no citable run behind it
  becomes a planning fact through repetition. The index + citation rule
  makes ETA claims auditable — and honest ("unverified") where history is
  thin.
- **The unverified backup:** taking a backup and proceeding without
  verifying it readable/restorable gates nothing; verification BEFORE the
  change is the gate.
- **Success-by-no-error:** an apply that didn't error but affected 0 rows
  is a failed run that looks green — expected-delta verification catches
  it.
- **Template drift:** the procedure evolves, the template doesn't; runs
  then deviate silently. Deviations recorded in run reports are the
  trigger to amend the template (via reviewed PR).
- **Scope creep mid-run** ("while we're in prod, also grant…"): the named
  unit + stop conditions exist precisely for this; a second operation is a
  second filled template.

## Stop Conditions

- Asked to EXECUTE the operation (run the migration, apply the grant) →
  refuse; this skill authors the template. Execution is the human
  operator's act under the template's own gates and the authorization
  matrix.
- Asked to embed a real tenant id, project ref, or credential value "so
  it's copy-paste ready" → refuse; placeholders and env-var names only.
- Asked to state ETA ranges with no prior-run evidence and no unverified
  label ("just estimate confidently") → refuse the unlabeled version;
  deliver the labeled one.
- The operation class has no possible backup/verification substrate
  (irreversible, unobservable) → stop and surface that this class cannot
  be safely templated as-is; the missing substrate is the finding.

## Supporting Files

- [references/deployment-prompt-template.md](references/deployment-prompt-template.md)
  — the full template skeleton (placeholder block, hard rules, stop
  conditions, backup gate, smoke tables, report format) and the
  history-index format with ETA-anchor citation rules.
- `evals/evals.json` — behavior cases incl. no-history ETAs and refusing
  live identifiers.
- `evals/trigger-evals.json` — discrimination against
  `incident-response-runbook`, `rollback-runbook-author`,
  `secure-migration-reviewer`, and `merge-is-deploy-governance`.
