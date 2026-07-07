---
name: audit-log-architect
description: Design a durable, tenant-scoped audit log system — an audit event taxonomy (authentication events, access-control changes, data access and exports, admin/support actions, security events, billing changes), a record schema (actor, tenant, action, target, outcome, correlation id, timestamp), integrity guarantees (append-only, tamper-evidence, an explicit audit-write-failure policy), retention and redaction rules, tenant-scoped access to audit data, and negative tests proving audit writes cannot be silently skipped and audit reads cannot cross tenants. Includes a migration path for introducing auditing to a live system with rollback. Use when building or overhauling audit logging, when compliance (SOC 2, ISO 27001, customer contracts) requires an audit trail, or when audit events are currently ad-hoc console logs. Do NOT use for API/webhook event contracts consumed by integrations (api-event-architect), for observability/tracing design, or for deciding who may do what (authorization-matrix-designer).
---

# Audit Log Architect

## Purpose

Produce an audit system that can answer "who did what, to what, in which
tenant, when, and what happened" — durably, provably, and without leaking one
tenant's activity to another. Deliverables: an event taxonomy, a record
schema, integrity and failure-policy rules, retention/redaction policy, a
tenant-scoped access model, negative tests, and a plan for introducing it to
a live system. An audit log differs from application logging in exactly the
properties people skip: completeness by taxonomy, immutability, and scoped
access — a grep-able stdout stream is not an audit trail.

## Use When

- Use when: compliance (SOC 2, ISO 27001, HIPAA-adjacent, enterprise
  contracts) requires demonstrable audit trails.
- Use when: audit-worthy actions are currently ad-hoc `logger.info` calls
  with no schema, durability, or access story.
- Use when: designing tenant-facing audit views ("show my workspace's
  activity") or staff-action accountability (support access must be
  auditable).
- Use when: an incident post-mortem revealed you cannot reconstruct who did
  what.
- Do NOT use when: designing events that INTEGRATIONS consume (webhooks,
  event feeds) — that is `api-event-architect`; audit events are a record,
  not an integration contract, even when one action produces both.
- Do NOT use when: the need is debugging/observability (traces, metrics,
  app logs) — different retention, different audience, different guarantees.
- Do NOT use when: deciding who is ALLOWED to act — that is
  `authorization-matrix-designer`; this skill records what they did.

## Inputs to Inspect

1. The authorization design (authorization-matrix-designer output): sensitive
   permissions, cross-tenant platform roles, and brokered-access rules — each
   implies required audit events.
2. The tenant model: tenant boundary, lifecycle states (audit retention must
   survive offboarding questions), membership semantics for actor identity.
3. Current logging: what is emitted today, from where, with what fields —
   the gap between it and the taxonomy is the work.
4. Compliance requirements naming specific events, retention periods, or
   access rules (SOC 2 criteria, contractual audit clauses).
5. Data-sensitivity constraints: what may never appear in an audit payload
   (secrets, credentials, full PII records).
6. Volume expectations: events/day at the taxonomy's scope — drives storage
   and the high-volume design decisions.

## Workflow

1. **Build the event taxonomy** from the starter set in
   [references/audit-event-taxonomy.md](references/audit-event-taxonomy.md):
   authentication, access-control changes, data access/export, admin and
   support actions, security events, billing/plan changes, lifecycle
   transitions. For each category: which concrete actions MUST be recorded.
   The taxonomy is the completeness contract — an unlisted action is a
   decision, not an oversight.
2. **Define the record schema**: actor (user/service/support-grant id, never
   just "admin"), on-behalf-of for impersonation, tenant id, action (from the
   taxonomy), target (type + id), outcome (success/denied/failed), timestamp,
   correlation/request id, origin (IP/user-agent where policy allows), and a
   redacted details payload. Schema versioned from day one.
3. **Set integrity rules**: append-only store — no update or delete API
   exists; tamper-evidence proportional to requirements (restricted DB
   permissions at minimum, hash-chaining/WORM storage where contracts demand
   it); clock source stated.
4. **Decide the write-failure policy per category** — the question that
   distinguishes audit from logging: if the audit write fails, does the
   action proceed? Security-critical categories (access-control changes,
   impersonation, exports) fail closed or queue-with-guarantee; lower
   categories may fail open with an alert. Write the policy down per
   category.
5. **Define retention and redaction**: retention per category (compliance
   floor, cost ceiling), what redaction removes from payloads before write
   (secrets always; PII per policy), and whether audit records survive tenant
   purge (usually yes, in de-identified or platform-scoped form — state it,
   it is a legal decision → flag to the human).
6. **Design the access model**: tenant admins read their own tenant's
   events only (scoped views); platform/staff audit access is itself an
   audited action; no general-purpose query access to the raw store.
   Support-facing and tenant-facing views may differ in fields — say how.
7. **Write the negative-test plan**: cross-tenant audit read denied;
   update/delete attempts on audit records fail at the store level; an
   audited action performed without a resulting event = test failure
   (completeness probe on the top sensitive actions); impersonation without
   an audit event fails.
8. **Plan the rollout to a live system**: emit-only first (no consumer),
   verify volume and schema against real traffic, then attach views and
   alerts; backfill is usually impossible — state the audit-coverage start
   date honestly rather than fabricating history. Rollback: emission can be
   disabled per category without touching business logic; already-written
   records are never deleted by a rollback.

## Output Format

```
AUDIT LOG DESIGN — <product/scope>
Event taxonomy: <category → concrete actions recorded; explicit exclusions
  with rationale>
Record schema: <fields, versioned; impersonation via on-behalf-of>
Integrity: <append-only mechanism; tamper-evidence level; clock source>
Write-failure policy: <category → fail-closed / queued-guaranteed /
  fail-open+alert>
Retention & redaction: <category → retention; payload redaction rules;
  post-purge policy (flagged as legal decision)>
Access model: <tenant-scoped views; staff access audited; raw-store access:
  none>
Negative-test plan: <test — attempted violation — expected result>
Rollout & rollback: <emit-only → verify → attach consumers; coverage start
  date; per-category disable; records never deleted>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every sensitive permission and brokered-access rule from the
      authorization design has a corresponding audit event.
- [ ] Actor is always a resolvable identity; impersonation carries both
      identities via on-behalf-of.
- [ ] No update/delete path exists to audit records; the mechanism is named.
- [ ] Write-failure policy is explicit per category — the fail-open/closed
      question is answered, not dodged.
- [ ] Payload redaction rules exist; secrets can never be written.
- [ ] Tenant admins can read only their tenant; staff audit reads are
      themselves audited.
- [ ] Negative tests cover cross-tenant reads, tampering, and completeness
      (action-without-event).
- [ ] Rollout starts emit-only and rollback never deletes written records.
- [ ] Audit events are not conflated with integration webhooks or app logs.

## Tenant Isolation Rules

- Every audit event carries the tenant id (or an explicit `platform` scope
  for tenant-less staff actions); there is no ambiguous scope.
- Tenant-facing audit queries are scoped at the store/view layer, not by
  application-side filtering of a global table.
- Cross-tenant audit access (staff, regulators) is enumerated, brokered, and
  produces its own audit events.

## Security Rules

- Append-only is a property of the store's permissions, not a code
  convention — the application role used for writes has no UPDATE/DELETE.
- Secrets, tokens, and credentials never enter payloads; redaction runs
  before write, not at read time.
- Security-critical actions (access-control changes, impersonation, exports)
  must not silently proceed when auditing is unavailable — per the stated
  fail-closed/queued policy.
- Negative tests are part of the deliverable; an audit system without a
  tamper test and a completeness probe is a logging system.

## Gotchas

- High-volume read events (every record view) can swamp the store; the
  taxonomy may record reads at coarser grain (search performed, export
  taken) — but that is a stated decision with compliance sign-off, not
  sampling by accident.
- Audit through the ORM inherits soft-delete and update paths you thought
  you removed; write via a dedicated append-only writer.
- "We'll backfill audit history later" is fiction; the coverage start date
  is what it is — document it.
- Correlation ids that never propagate to background jobs make job actions
  unattributable; the job context must carry actor + correlation from the
  triggering request.
- Tenant purge vs audit retention is a genuine legal tension — surface it;
  do not resolve it silently in either direction.

## Stop Conditions

- Compliance regime or contractual audit clauses unknown AND they would
  change taxonomy/retention → ask before designing to guesses.
- Post-purge audit retention (keep vs destroy) is a legal decision →
  `human-approval-boundary`; present both options with consequences.
- The system has no authorization design to hang events off → run
  `authorization-matrix-designer` first or in tandem; auditing undefined
  permissions records noise.
- Asked to implement the pipeline in the same pass → separate, scoped task;
  this skill delivers the design and test plan.

## Supporting Files

- [references/audit-event-taxonomy.md](references/audit-event-taxonomy.md) —
  starter taxonomy by category with must-record actions and grain guidance.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against
  `authorization-matrix-designer` and `api-event-architect` (access & events
  cluster).
