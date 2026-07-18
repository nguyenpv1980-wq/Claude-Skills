---
name: data-migration-runbook-author
description: 'Author the operator-executable runbook for a DATA move — backfill, re-shard, store cutover, tenant move, CDC initial load — that a stranger can run under pressure: preconditions gated on verified backups and dry-run evidence, batching with throttles and pause/resume, per-batch and per-stage verification queries (counts, checksums, sampled equality) with expected outputs, explicit abort criteria naming the safe halt state, rollback per stage composed from rollback-runbook-author conventions, and no-return points flagged for human approval. Authors the DOCUMENT only — never executes; destructive steps are human-run. Consumes an approved plan (schema-evolution-planner) and safety review (secure-migration-reviewer) rather than re-deriving them. Use when asked to write the runbook for a backfill/migration/cutover or to make a data move operator-safe. Do NOT use for the change SEQUENCE itself or general release rollbacks (rollback-runbook-author).'
---

# Data Migration Runbook Author

## Purpose

Data moves fail operationally more often than logically: the batch size
that melted the primary at hour two, the verification nobody ran because
it wasn't written down, the abort decision improvised at 3 a.m. by
whoever was awake. This skill authors the runbook — numbered steps with
per-step verification and expected output, batching and throttle values
with their rationale, abort criteria that name the safe halt state, and
rollback per stage — so executing a backfill, re-shard, cutover, or
tenant move is reading, not improvising. It writes the document; it runs
nothing. The change's staged design comes in as an approved
`schema-evolution-planner` plan (or equivalent), and its DDL safety
verdict from `secure-migration-reviewer` — the runbook cites both and
re-derives neither.

## Use When

- Use when: a backfill, re-shard, store-to-store cutover, tenant data
  move, or CDC initial load needs an operator-executable procedure.
- Use when: an approved evolution plan's migrate stage says "backfill
  with parity gate" and someone must now write HOW, batch by batch.
- Use when: a previous data move was improvised (or went wrong) and the
  next one must be runbook-governed.
- Use when: a data move will be executed by someone other than its
  designer — the handoff artifact is this runbook.
- Do NOT use when: the change SEQUENCE (expand/migrate/contract stages,
  compatibility windows) is still being designed — that is
  `schema-evolution-planner`; the runbook implements an approved plan.
- Do NOT use when: reviewing migration DDL for safety (locks,
  destructive ops, RLS gaps) — that is `secure-migration-reviewer`,
  whose verdict is a runbook PREREQUISITE.
- Do NOT use when: authoring the rollback plan for a general RELEASE
  (artifact redeploys, flag kills, blue/green) — that is
  `rollback-runbook-author`; this skill composes its conventions for the
  data-move case specifically.
- Do NOT use when: the tenant-scoping strategy of the move (which
  isolation model, how tenant context flows) is undecided — that design
  is `multi-tenant-data-architect`.
- Do NOT use when: what's needed is a reusable operator PROMPT TEMPLATE
  for a recurring gated operation — `gated-deployment-prompt-template`
  owns that form; this skill writes the specific move's full runbook
  (the two compose: a recurring data move may get a template derived
  from this runbook).

## Inputs to Inspect

1. The approved plan: stages, parity definition, read-switch condition,
   and abort philosophy from `schema-evolution-planner` (or the
   equivalent decision record for non-schema moves). No plan → stop.
2. The safety review: `secure-migration-reviewer`'s verdict on the
   migration/DDL involved, including its rollback assessment and
   required negative tests.
3. The operational facts: table/store sizes, write rates, peak/quiet
   windows, replication topology and lag behavior, maintenance-window
   policy, and the throttling levers that exist (batch size, sleep,
   concurrency).
4. Backup and restore reality: what backup exists, when it last
   succeeded, how long a restore takes at this size — restore time bounds
   the abort options.
5. The executor's context: who runs this (role, access level), from
   where (bastion, migration job, console), and what approval the repo's
   conventions require per destructive step (`human-approval-boundary`
   / the approval register where present).
6. Verification access: where counts/checksums can be run without adding
   dangerous load (replica for reads where lag permits — stated).

## Workflow

1. **Confirm the prerequisites or stop.** Approved plan, safety-review
   verdict, and a VERIFIED backup (not "backups are enabled" — evidence
   of a recent successful backup/restore test appropriate to the move's
   blast radius). Absent any of the three, the runbook is not writable
   yet; say which is missing.
2. **Write the preconditions section.** Concrete gates with commands'
   PURPOSE and expected output: backup evidence check, dry-run on a
   sampled/staging keyspace with its expected parity result, disk/
   headroom checks, replication-lag baseline, and the announced window
   with its stakeholders. Each gate is pass/fail — an operator can
   answer "did it pass?" without judgment calls.
3. **Design the batching.** Batch key and size with the RATIONALE
   (rows × row-width vs lock/undo budget), throttle (sleep or rate)
   with the signal that tunes it (replication lag threshold, p99 on the
   primary), concurrency (usually 1; more only with partition-disjoint
   proof), pause/resume mechanics (progress marker stored WHERE, resume
   idempotency — re-running a completed batch must be harmless), and
   the quiet-window preference stated.
4. **Write per-batch and per-stage verification.** Per batch: the
   verification query's intent (count parity for the batch range,
   checksum over normalized columns) and its EXPECTED output shape.
   Per stage: the full-keyspace parity gate from the plan, plus a
   business-level sample (N known entities compared field-by-field).
   Every verification states what PASS looks like — a query without an
   expected result is not verification.
5. **Define abort criteria and halt states per stage.** Numeric triggers
   (parity mismatch > 0, replication lag > threshold for > duration,
   error rate on the serving path, batch duration trending 2× baseline)
   → the abort ACTION (stop the loop, leave dual-writes on, do NOT
   revert schema) → the named SAFE HALT STATE (system serving from old
   path, partial new data inert, resumable from marker). Improvised
   aborts are how partial moves become corruption; the halt state is
   designed, not discovered.
6. **Write rollback per stage,** composing `rollback-runbook-author`
   conventions (roll-back-vs-fix-forward criteria with a time-box, one
   observable verification per rollback step): pre-cutover stages roll
   back by stopping the loop and cleaning inert copies (or leaving them,
   stated); post-read-switch rollback switches reads back (condition:
   dual-writes still on); the no-return point — old path
   decommissioned/contracted — is FLAGGED as requiring explicit human
   sign-off, with the plan's zero-reader evidence cited.
7. **Mark every human gate.** Steps that are destructive, irreversible,
   or production-facing get an APPROVAL marker per the repo's
   conventions (`human-approval-boundary`; recorded in the approval
   register where the repo keeps one). The runbook never instructs an
   agent to proceed through these autonomously.
8. **Assemble the runbook** in the Output Format: numbered, each step =
   action + verification + expected output + on-failure pointer;
   an execution log skeleton (timestamps, batch ranges, verification
   outputs, deviations) the operator fills as they go — the log is the
   move's evidence for `ai-closeout-reporter`-style closeout and any
   later audit.

Runbook skeleton, batching-rationale worksheet, verification-query
patterns, and abort/halt-state examples:
[references/runbook-skeleton.md](references/runbook-skeleton.md).

## Output Format

```
DATA MIGRATION RUNBOOK — <move> (vN, date)
Prerequisites: plan=<ref> safety-review=<ref/verdict> backup=<evidence + restore-time bound>
Preconditions: <numbered pass/fail gates with expected outputs>
Execution:
  Stage <n> — <name>
    Step n.m: <action (purpose-first; exact commands only where stable)>
              VERIFY: <check + EXPECTED output>
              ON FAIL: <abort ref | retry rule>
    Batching: key=<k> size=<n (rationale)> throttle=<signal-tuned> resume=<marker + idempotency>
    [APPROVAL REQUIRED] markers on destructive/irreversible steps
Abort criteria: <numeric triggers → action → SAFE HALT STATE, per stage>
Rollback:      <per stage, rollback-runbook-author conventions; no-return point flagged>
Execution log: <skeleton: timestamps, ranges, verification outputs, deviations>
Not covered:   <explicitly out of scope>
Execution posture: THIS DOCUMENT EXECUTES NOTHING — every step is operator-run;
                   destructive steps require the marked human approval.
```

## Validation Checklist

- [ ] All three prerequisites cited with evidence (plan, safety review,
      verified backup) — none assumed.
- [ ] Every step has a verification with an EXPECTED output; no
      verify-free destructive steps exist.
- [ ] Batching states rationale and the tuning signal; resume is
      idempotent from the stored marker.
- [ ] Abort criteria are numeric, per stage, and land in a NAMED safe
      halt state — never "stop and assess".
- [ ] Rollback exists per stage; the no-return point is flagged with its
      required human sign-off and cited evidence.
- [ ] Commands are purpose-first and platform-stable; nothing assumes
      one product's exact CLI where the store's generic interface
      differs.
- [ ] The execution-log skeleton exists so the run produces evidence,
      not memories.
- [ ] The document claims no execution authority anywhere.

## Gotchas

- Batch sizes calibrated at hour zero melt things at hour three: table
  hotspots, index bloat, and vacuum/GC debt accumulate. The throttle is
  signal-tuned (lag, p99), not a constant to set and forget.
- Resume-after-crash double-applies the last batch unless batches are
  idempotent (keyed upsert, range-replace) — the marker says where to
  resume; idempotency makes resuming SAFE.
- Verification on the replica lies during the move: the thing you are
  changing is what's replicating. State where each check runs and the
  lag it must tolerate.
- "Abort" that reverts schema mid-backfill turns a halt into an outage:
  the safe halt state usually keeps the expanded schema and inert
  partial data — removal is a separate reviewed step, not a reflex.
- The dry run that proved nothing: a staging dry-run on 1% synthetic
  data validates syntax, not behavior at volume. State what the dry run
  actually evidences and what it cannot.
- Progress markers stored in the table being migrated: the move's own
  writes then race the marker. Store progress OUTSIDE the moving data.
- Cutover on a Friday because the window was free: the runbook states
  window requirements including the days of hands-on-deck AFTER
  cutover, not just the hours during.
- A perfect runbook nobody rehearsed: for high-blast-radius moves, the
  rehearsal requirement (staging execution of THIS runbook) is a
  precondition gate, mirroring `rollback-runbook-author`'s rehearsal
  discipline.

## Stop Conditions

- No approved plan, no safety-review verdict, or no verified backup →
  stop; name the missing prerequisite. A runbook that papers over a
  missing prerequisite launders risk into procedure.
- Asked to EXECUTE the move (run the backfill, "just do the cutover")
  → refuse execution; this skill authors the document, and every
  destructive step is operator-run under the marked approvals.
- The plan's parity definition is missing or unverifiable (no way to
  state what PASS looks like) → stop and send the gap back to
  `schema-evolution-planner`; verification cannot be invented at the
  runbook layer.
- Restore time exceeds the tolerable outage for the worst-case abort
  (backup exists but is operationally useless at this size) → halt and
  surface: the move's risk envelope is a human decision that must be
  made with that fact on the table.
- Asked to fold the runbook's approval gates into "auto-proceed if
  checks pass" for an agent to run end-to-end → refuse; destructive
  data-move steps stay human-gated per `human-approval-boundary` and
  the repo's authorization conventions.

## Supporting Files

- [references/runbook-skeleton.md](references/runbook-skeleton.md)
  — full runbook skeleton, batching-rationale worksheet,
  verification-query patterns (counts/checksums/sampled equality),
  abort-trigger and safe-halt-state examples, execution-log format.
- `evals/evals.json` — behavior cases including the missing-backup gate
  and the just-run-it refusal.
- `evals/trigger-evals.json` — discrimination against
  `schema-evolution-planner`, `secure-migration-reviewer`,
  `rollback-runbook-author`, and `gated-deployment-prompt-template`.
