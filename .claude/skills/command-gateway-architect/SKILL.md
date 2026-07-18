---
name: command-gateway-architect
description: 'Design a single server-side-mediated write path — a command bus — for protected mutations in a multi-tenant SaaS: a command registry plus a per-command pipeline (validate payload → authenticate the actor from the token, never from client-supplied identity → authorize against policy → server-derive tenant/resource scope from trusted rows → idempotency → execute → emit audit + domain events → safe error envelope), plus the no-direct-client-writes invariant for protected actions. Produces the command catalog, the pipeline contract, and an enforcement-point map. Use when mutations are scattered across endpoints or client SDKs, when tenant scope is read from the request body, or when adding a sensitive write. Do NOT use for the external API/webhook contract (api-event-architect), the role/permission policy itself (authorization-matrix-designer), or the audit record schema (audit-log-architect) — this dispatches through them.'
---

# Command Gateway Architect

## Purpose

A multi-tenant SaaS leaks and corrupts data through the same door: writes
that skip a check because each endpoint re-implements its own. This skill
designs the opposite — one server-side-mediated write path (a command bus)
that every protected mutation flows through, so validation, actor
authentication, authorization, tenant-scope derivation, idempotency, audit,
and event emission happen in ONE ordered pipeline instead of being copied,
half-applied, and forgotten per route. The deliverable is a command catalog,
a per-command pipeline contract with the steps fixed in order, and an
enforcement-point map that proves no protected write reaches the datastore
around the gateway. The load-bearing invariant is the one attackers probe:
the actor and the tenant scope are derived server-side from trusted rows,
never accepted from the client.

## Use When

- Use when: mutations are scattered across many endpoints or a client SDK
  writes to the datastore directly, and the same checks are re-implemented
  (inconsistently) per write.
- Use when: a request supplies its own `tenant_id`, `user_id`, `role`, or
  `owner_id` on a write path and the server trusts it — the classic
  cross-tenant / privilege-escalation write.
- Use when: adding a sensitive or irreversible mutation (billing change,
  role grant, data export, deletion) and it needs a single audited,
  idempotent path rather than a bespoke handler.
- Use when: retries or double-submits cause duplicate side effects and the
  write path has no idempotency contract.
- Do NOT use when: the subject is the EXTERNAL contract — public REST/GraphQL
  shape, versioning, webhooks, partner rate limits — that is
  `api-event-architect`; the gateway is what those endpoints dispatch INTO.
- Do NOT use when: the question is WHO may do WHAT (roles × permissions ×
  resources) — that policy is `authorization-matrix-designer`; the gateway
  ENFORCES it at the authorize step, it does not author it.
- Do NOT use when: the subject is the audit record schema, taxonomy, or
  tamper-evidence — that is `audit-log-architect`; the gateway EMITS records
  into it.
- Do NOT use when: designing the INTERNAL event backbone (topics, partitions,
  DLQ) the emitted domain events ride — that is `streaming-event-architect`.

## Inputs to Inspect

1. The current write surface: every route/handler/RPC/client-SDK path that
   mutates state, and which of them re-derive checks locally vs share them.
2. Where tenant and actor context come from today on each write — token
   claims vs request body vs path param — flagging every client-supplied
   scope value on a write.
3. The authorization model in force (`authorization-matrix-designer` output
   if present): roles, object-level rules, deny-by-default posture — the
   policy the authorize step will call.
4. The audit taxonomy (`audit-log-architect` output if present): which
   actions must produce audit records and the required fields.
5. Existing idempotency handling: any dedup keys, unique constraints, or
   "retry made two charges" incident history.
6. The datastore access paths: can clients reach tables directly (e.g.
   client-side SDK + row policies) — which determines whether the gateway
   can be the ONLY write path or must be paired with datastore-level denial.

## Workflow

1. **Inventory commands, not endpoints.** Name each protected mutation as a
   command (`CreateInvoice`, `GrantRole`, `DeleteWorkspace`) with its inputs,
   the resource it touches, and its side effects. Group synonymous
   endpoints that do the same write into one command.
2. **Fix the pipeline order and make it non-optional.** Every command runs
   the same ordered stages; the order is the security property:
   1. **Validate** the payload against a schema (shape, types, required,
      bounds) — reject malformed input before any authz work.
   2. **Authenticate the actor** from the verified token/session ONLY. The
      client never states who it is on a write.
   3. **Authorize** the actor against policy for this command + target
      (deny-by-default; call `authorization-matrix-designer`'s rules).
   4. **Derive tenant/resource scope server-side** from trusted rows (look
      the target up, read its `tenant_id` from the DB, confirm it matches
      the actor's tenant) — never from the request body.
   5. **Idempotency**: an idempotency key per mutating command; a repeated
      key returns the first result without re-executing side effects.
   6. **Execute** the state change transactionally.
   7. **Emit** audit record + domain event(s) as part of (or committed with)
      the same transaction so a successful write cannot skip its audit.
   8. **Return a safe error envelope** (see step 5).
3. **State the no-direct-client-writes invariant and how it is enforced.**
   The gateway is only a security boundary if writes cannot go around it.
   Name the backstop: datastore write-deny for clients (RLS/permission so
   direct client writes fail) so the gateway is the sole write authority,
   not merely the polite one.
4. **Design idempotency concretely.** Key source (client-supplied UUID vs
   derived business key), the dedup store and its retention, what "same
   request" means, and the response for a replayed key. Distinguish
   idempotency (safe replay) from concurrency control (optimistic version /
   row lock) — name both where the command needs them.
5. **Design the error envelope.** One shape for all failures: a stable
   machine code + safe message; validation errors field-scoped; authz
   failures return the SAME not-found/forbidden shape regardless of whether
   the row exists in another tenant (no existence oracle); never leak
   stack traces, SQL, or other tenants' identifiers. Defer the error MODEL
   itself to `error-taxonomy-designer` and leak review to
   `error-handling-security-reviewer` — this pins the envelope contract.
6. **Map enforcement points.** A table: command → validated? → actor from
   token? → authz rule → scope-derivation source → idempotent? → audit
   event → around-gateway path (must be none). Any "scope from body" or
   "no audit" cell is a finding.
7. **Deliver** the catalog, the pipeline contract, and the enforcement-point
   map in the Output Format, with every handoff (policy, audit, event
   transport) named, not restated.

## Output Format

```
COMMAND GATEWAY DESIGN — <system/domain>
Invariant: all protected writes flow through the gateway; direct client
  writes DENIED at <datastore backstop>. Actor + tenant scope = server-derived.
Command catalog:
  <Command — inputs — target resource — side effects — sensitive? y/n>
Pipeline contract (fixed order, every command):
  validate → authenticate(actor from token) → authorize(<policy source>) →
  derive-scope(from trusted rows) → idempotency(<key, store, retention>) →
  execute(txn) → emit(audit + events) → safe-error-envelope
Idempotency: <key source, dedup store, replay response, concurrency control>
Error envelope: <shape, codes, no-existence-oracle rule, leak rules>
Enforcement-point map: <command × stage table; findings flagged>
Handoffs: policy → authorization-matrix-designer; audit schema →
  audit-log-architect; event transport → streaming-event-architect;
  external contract → api-event-architect
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every protected mutation appears as a command; no endpoint bypasses
      the pipeline.
- [ ] Actor identity is taken from the verified token on EVERY command —
      no command trusts a client-supplied actor/role.
- [ ] Tenant/resource scope is derived from trusted rows on every command;
      no command reads scope from the request body.
- [ ] Authorize is deny-by-default and delegates to the authorization
      model, not re-implemented per command.
- [ ] Every mutating command has an idempotency contract (key, store,
      replay response) — retries cannot double-apply side effects.
- [ ] A successful write cannot skip its audit record or event emission
      (same transaction / outbox).
- [ ] The around-the-gateway path is closed at the datastore, and that
      backstop is named — the invariant is enforced, not aspirational.
- [ ] Error envelope leaks nothing cross-tenant and gives no existence
      oracle; the error MODEL is deferred to `error-taxonomy-designer`.

## Gotchas

- A gateway that clients can bypass is documentation, not a control: if a
  client SDK can still write to tables directly, the pipeline's checks are
  optional. The datastore-level write-deny is the load-bearing half.
- Trusting `tenant_id` from the body "because the client already knows it"
  is the cross-tenant write bug in its purest form — the client knowing it
  is exactly why it cannot be trusted.
- Emitting the audit event AFTER the transaction commits, in a separate
  step, means a crash between them yields an unaudited write. Commit the
  record with the change (transactional outbox) or inside the same txn.
- Idempotency keyed on the whole request body breaks the moment a retried
  client adds a timestamp; key on a stable business identifier or a
  client-generated request id.
- Idempotency is not concurrency control: a replayed key and two DIFFERENT
  concurrent writers are different problems; the second needs a version
  check or lock, not a dedup store.
- Authorize-then-derive-scope in the wrong order authorizes against a
  client-claimed target: derive and confirm the real row's tenant, then
  authorize against THAT, or an attacker authorizes on their own object and
  acts on someone else's.
- A per-command bespoke error message is where existence oracles leak
  ("forbidden" vs "not found" tells the attacker the row exists) — one
  envelope, one shape.

## Stop Conditions

- The authorization policy the authorize step must call does not exist or is
  ambiguous → obtain it from `authorization-matrix-designer` or a human
  before fixing the pipeline; a gateway enforcing an undefined policy is a
  false assurance.
- Closing the around-the-gateway path requires changing live datastore
  permissions/RLS on a running system → this skill DESIGNS the backstop and
  the migration; executing permission changes against production follows the
  repo's approval path (`human-approval-boundary`) — do not run them here.
- A "make every write exactly-once end to end including external side
  effects" mandate survives → surface the honest decomposition
  (idempotent effects + at-least-once) and escalate; do not promise
  unqualified exactly-once.
- The write surface is so entangled that no single gateway can front it
  without a phased migration → present the migration sequence and the
  interim risk, and stop for a human to sequence it rather than declaring
  the invariant met.

## Supporting Files

- `evals/evals.json` — behavior cases: the scattered-writes design, the
  scope-from-body fix, the idempotency-vs-concurrency edge, and the
  exactly-once refusal.
- `evals/trigger-evals.json` — discrimination against `api-event-architect`
  (external contract), `authorization-matrix-designer` (policy vs
  enforcement), `audit-log-architect` (record schema vs emission), and
  `streaming-event-architect` (event transport).
- No `references/` — the pipeline contract and enforcement-point map above
  are the complete procedure; detail lives in the produced artifacts.
