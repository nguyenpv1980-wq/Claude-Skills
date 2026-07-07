# Rollback Runbook Template

Detail file for `rollback-runbook-author`. Loaded on demand.

## Per-layer primitive table

| Layer | Primitive options | Verify with |
| --- | --- | --- |
| Traffic | blue/green flip back; canary abort to stable; LB weight to 0 | request mix by version in dashboards |
| Artifact | redeploy previous artifact BY ID | running version endpoint/label |
| Feature flag | kill-switch off (state expected propagation time) | flag evaluation telemetry |
| Config | revert config version via its own deploy path | config version endpoint/checksum |
| Schema | expand-phase: usually NO action needed (old code reads expanded schema); contract-phase: per `secure-migration-reviewer` reversal or NOT reversible | migration table state |
| Data | repair/reconciliation scripts; restore points | row counts / checksums against expectations |

Reversal order default: freeze deploys → traffic/flags (fastest, least
destructive) → artifact → config → schema/data (slowest, approval-gated).
State deviations and why.

## Runbook skeleton

```
ROLLBACK RUNBOOK — <change id> — status: CURRENT | STALE (<trigger hit>)
Last rehearsal: <date — executor — env — result>

WHEN TO USE (decision criteria)
- Roll back if: <symptom/threshold list, tied to dashboards>
- Fix forward if: <criteria>
- Time-box: if not diagnosed in <N> min → roll back. Decider: <role>.

PRECONDITIONS
- Access: <systems + permission level the executor must confirm FIRST>
- Tools: <CLI/console paths>
- Freeze: halt concurrent deploys via <mechanism>. Verify: <how>.

STEPS
1. <action> — command: `<exact command>` — expect: <observable result>
   — verify before continuing: <check>
2. ...
N. Post-rollback verification: <SLI/dashboard — expected reading>
N+1. Stand-down: unfreeze deploys, comms completion message.

BAD-WINDOW DATA
- New version wrote: <what>
- Old version reads it: <safely / unsafely because …>
- Repair: <steps / "none needed" + reason>. Destructive repair requires
  human approval AT EXECUTION TIME.

COMMS
- At start: <who/channel/template>
- At completion: <who/channel/template>
- Status page: <posture>

STALENESS TRIGGERS (this runbook must be re-validated when…)
- schema migration lands on <tables>; deploy strategy changes;
  artifact registry/retention changes; access model changes.
```

## Rehearsal log format

| Date | Executor | Environment | Steps run | Result | Gaps found |
| --- | --- | --- | --- | --- | --- |

A runbook with an empty rehearsal log is DRAFT, not CURRENT — say so at
the top. Tabletop rehearsals count only when every command was actually
resolved (paths exist, ids resolve, access confirmed).
