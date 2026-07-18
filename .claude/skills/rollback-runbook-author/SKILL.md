---
name: rollback-runbook-author
description: 'Design the rollback STRATEGY for a change and author the rollback RUNBOOK a stranger can execute under pressure — roll-back-vs-fix-forward criteria with a time-box, the primitive per layer (artifact redeploy, blue/green flip, canary abort, flag kill, config revert), migration reversibility composed from secure-migration-reviewer (never re-derived), numbered steps with one observable verification each, bad-window data repair, comms, and a rehearsal requirement with staleness triggers. Absorbs rollback-strategy-designer: strategy and runbook ship together — an unexecutable strategy is a diagram. Authors documents only; never executes a rollback. Use when asked to write or design a rollback/backout plan for a release, migration, flag, or infra change, or when release-readiness-reviewer flags a missing rollback path. Do NOT use mid-incident to decide NOW (incident-response-runbook invokes this artifact), for migration safety review (secure-migration-reviewer), or the ship verdict (release-readiness-reviewer).'
---

# Rollback Runbook Author

## Purpose

Produce a rollback strategy and its executable runbook for a specific
change: when to roll back instead of fixing forward, which primitive
reverses each layer (code, config, flags, schema, data), the exact steps
with verification, and what happens to data written in the bad window. The
bar is stranger-executability under pressure — the person executing at
3am did not write the runbook, did not ship the change, and must not need
tribal knowledge. Strategy and runbook are one artifact: a strategy nobody
can execute is a diagram, and a runbook with no decision criteria executes
the wrong thing confidently.

## Use When

- Use when: asked to write or design a rollback/backout plan for a
  release, deployment, migration, feature flag, or infrastructure change.
- Use when: `release-readiness-reviewer` flags a missing or untested
  rollback path as a blocking item.
- Use when: a deployment strategy (canary, blue/green, flag-gated) needs
  its backout mechanics specified (`ci-pipeline-architect` hands the
  primitive here).
- Use when: an existing rollback runbook needs review against a new
  release shape (schema change, new dependency, new traffic pattern).
- Do NOT use when: an incident is live and the question is "roll back NOW
  or not" — `incident-response-runbook` procedures invoke THIS artifact;
  authoring during the fire is the failure this skill prevents.
- Do NOT use when: reviewing whether the migration itself is safe/
  reversible — `secure-migration-reviewer` (its analysis is consumed
  here).
- Do NOT use when: deciding whether the release ships —
  `release-readiness-reviewer`.
- Do NOT use when: asked to EXECUTE a rollback — this skill authors
  documents; execution is a human-gated operation.

## Inputs to Inspect

1. The change being protected: commits/artifact, migrations included,
   flags touched, config changes, infra changes.
2. The deployment strategy and its rollback primitive per environment
   (`ci-pipeline-architect` design: rolling redeploy / blue-green flip /
   canary abort / flag kill).
3. Migration reversibility analysis (`secure-migration-reviewer` output):
   expand→contract stage, irreversible operations, backfill status.
4. The artifact registry: is the previous known-good artifact still
   available, and what identifies it?
5. Data-write surface of the change: what does the new version write that
   the old version cannot read (schema, formats, queues, caches)?
6. Observability signals that define "rollback worked"
   (`slo-reliability-architect` SLIs, dashboards).
7. Who executes: on-call access/permissions reality — steps requiring
   access the executor lacks are decoration.

## Workflow

1. **Write the decision criteria first**: the symptoms/thresholds that
   trigger rollback vs fix-forward, a time-box ("if not diagnosed in N
   minutes, roll back"), and who decides (role, not name). Fix-forward is
   the right call sometimes — the runbook says when, so the 3am decision
   is a lookup, not a debate.
2. **Design the strategy — pick the primitive per layer**: code (redeploy
   previous artifact by id / traffic flip / canary abort), config (revert
   mechanism and its deploy path), flags (kill-switch flip with expected
   effect time), schema (per `secure-migration-reviewer`: which expand→
   contract stage is deployed and what that means for reversal), data
   (what the bad window wrote and the repair posture). Layers roll back
   in a stated order — traffic before schema, flags before artifacts —
   with the order's reason.
3. **Confirm the previous-good state is reachable**: the artifact exists
   and is identified by id (not "the previous build"), the old version
   tolerates the current schema (expand-phase compatibility), restore
   points/backups exist where data repair may need them
   (verification steps, not assumptions).
4. **Write the numbered steps**: each step = one action with the exact
   command/console path, the expected observable result, and the
   verification before proceeding. Include: preconditions (access,
   tools), the stop-deploys step (freeze concurrent releases —
   concurrency with a new deploy is the classic rollback race), the
   rollback actions per layer in order, post-rollback verification
   against the named SLIs/dashboards, and stand-down.
5. **Cover the bad-window data**: what was written between deploy and
   rollback, whether the old version reads it safely, the repair/
   reconciliation steps if not, and the explicit criteria for when data
   repair needs `human-approval-boundary` (destructive repair always
   does).
6. **Add comms steps**: who is told at rollback start and completion
   (channel, template pointer), status-page posture — aligned with
   `incident-response-runbook` comms structure when the rollback happens
   inside an incident.
7. **Require rehearsal and set staleness triggers**: the dry-run
   requirement (staging execution or tabletop with the actual commands),
   the rehearsal log line (date, executor, result), and the triggers that
   make this runbook stale (schema change, deploy-strategy change,
   artifact-registry change) — a stale runbook says so on page one.
8. **Hand off**: the artifact to `release-readiness-reviewer` as the
   rollback-path evidence, and the rollback-worked signals to
   `observability-operator` for dashboard/alert wiring.

## Output Format

```
ROLLBACK RUNBOOK — <change/release id> (strategy + runbook, one artifact)
Decision criteria: <rollback-vs-fix-forward symptoms/thresholds; time-box;
  decider role>
Strategy: <layer → primitive → order of reversal → why this order>
Previous-good state: <artifact id + registry path; old-version/schema
  compatibility statement; backup/restore points verified>
Preconditions: <access, tools, permissions the executor must have>
Steps (numbered): <action — exact command/path — expected observable
  result — verification before next step>
  [includes: freeze concurrent deploys; per-layer rollback; post-rollback
   verification against named SLIs; stand-down]
Bad-window data: <what the new version wrote; old-version read safety;
  repair steps or "none needed" with reason; approval gates for
  destructive repair>
Comms: <who/when/channel at start + completion; status-page posture>
Rehearsal: <dry-run requirement; log (date, executor, result); staleness
  triggers>
Handoffs: <release-readiness-reviewer (evidence); observability-operator
  (rollback-worked signals)>
```

## Validation Checklist

- [ ] Decision criteria exist with a time-box and a decider role — the
      runbook decides WHEN, not just HOW.
- [ ] Every layer in the change has a primitive, and the reversal order
      is stated with its reason.
- [ ] The previous-good artifact is identified by id and its
      schema-compatibility with the current database is stated, not
      assumed.
- [ ] Every step has one action, one observable expected result, and a
      verification — executable by someone who did not write it (the
      `manual-test-case-creator` stranger bar).
- [ ] The bad-window data question is answered explicitly — "none needed"
      carries its reason.
- [ ] Migration reversibility came from `secure-migration-reviewer`
      analysis, not re-derived here.
- [ ] Rehearsal requirement, log, and staleness triggers are present.
- [ ] Nothing was executed: this pass authored a document.

## Gotchas

- Rolling back the artifact but not the config (or vice versa) produces a
  hybrid state worse than either version — the layer order exists for
  this.
- The old version may not parse what the new version wrote (enum values,
  queue message formats, cache entries) — schema compatibility is
  necessary but not sufficient; check the write surface.
- Concurrent deploys during rollback are the classic race: the freeze
  step is not optional ceremony.
- Flag kills propagate on the flag system's schedule, not instantly —
  state the expected effect time or the executor will re-trigger.
- Runbooks rot fastest at the access layer: the on-call's permissions
  were narrowed since the last rehearsal, and step 3 now needs someone
  asleep. Rehearse with the executor's real access.
- A rollback that "worked" per deploy tooling but was never verified
  against user-facing SLIs has not been verified at all.

## Stop Conditions

- Asked to execute the rollback now → stop; authoring and executing are
  different authorities. Live execution routes through the incident
  process and `human-approval-boundary`.
- The change contains an irreversible migration stage
  (`secure-migration-reviewer` verdict) with no compensating path → the
  runbook cannot promise reversal; surface this as a release-blocking
  finding to `release-readiness-reviewer` instead of writing a fictional
  rollback.
- The previous-good artifact cannot be identified or no longer exists →
  stop and surface; a runbook pointing at a missing artifact is worse
  than none.
- Data repair for the bad window would be destructive (deletes,
  overwrites) → the repair steps require `human-approval-boundary` at
  execution time, stated in the runbook itself.

## Supporting Files

- `references/rollback-runbook-template.md` — the full runbook skeleton
  with per-layer primitive tables and the rehearsal log format.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the delivery cluster
  (`ci-pipeline-architect`, `release-readiness-reviewer`), against shipped
  `secure-migration-reviewer`, and the mid-incident boundary
  (`incident-response-runbook`).
