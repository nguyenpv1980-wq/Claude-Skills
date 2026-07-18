---
name: admin-console-architect
description: 'Design the internal ops/support/superadmin CONSOLE for a multi-tenant SaaS — the surface operators act THROUGH: cross-tenant read/write with MANDATORY audit on every action, impersonation/support-mode with hard boundaries + consent + audit, least-privilege admin tiers (view-ops / write-ops / superadmin), break-glass elevation (time-boxed, approved, auto-expiring, logged), and the operator control-plane (health, manual failover/retry, data-repair). Produces the console architecture, the admin-tier + impersonation enforcement design, the break-glass workflow, and the audit contract. Use when building an internal admin/support/superadmin tool, adding cross-tenant support access, or designing impersonation/break-glass safely. Do NOT use for the authorization POLICY itself (authorization-matrix-designer — this ENFORCES it), operator TELEMETRY (observability-operator), AI-agent authority (agent-authorization-matrix), or the incident PLAYBOOK (incident-response-runbook).'
---

# Admin Console Architect

## Purpose

The internal admin console is the most powerful and least-scrutinized surface
in a SaaS: it reaches across every tenant, it can impersonate any user, and
it is usually built fast, for "just us," with none of the controls the
customer-facing app has. That is exactly where the breach and the insider-
misuse incident come from. This skill designs that surface deliberately:
cross-tenant access where every action is audited, impersonation that is
bounded and consented and logged, admin tiers that are least-privilege rather
than one god role, break-glass elevation that is time-boxed and approved and
self-expiring, and an operator control-plane whose dangerous actions
(failover, data-repair) are gated and reversible. The deliverable is the
console architecture, the admin-tier and impersonation enforcement design, the
break-glass workflow, and the audit contract. This skill designs the console
that ENFORCES the authorization policy; it does not author that policy, and it
does not grant anyone real production access.

## Use When

- Use when: building or overhauling an internal admin / support / superadmin
  / back-office console for operators, support agents, or engineers.
- Use when: adding cross-tenant support access — support needs to see or fix a
  customer's data — and it must be safe, scoped, and audited.
- Use when: designing impersonation / "log in as this user" / support-mode,
  and it needs boundaries, consent posture, and an audit trail.
- Use when: designing admin roles/tiers, break-glass/elevation for rare
  high-privilege actions, or an operator control-plane (manual failover,
  retry, data-repair) whose actions are dangerous.
- Do NOT use when: the task is authoring the authorization POLICY itself —
  the roles × permissions × resources model, the impersonation RULES — that
  is `authorization-matrix-designer`; this skill designs the console that
  ENFORCES that policy at its action surface.
- Do NOT use when: the task is operator TELEMETRY — dashboards, metrics,
  traces, logs to SEE system state — that is `observability-operator`; this
  console is the ACTION surface (telemetry may be embedded, but seeing is not
  acting).
- Do NOT use when: the authority in question is an AI AGENT's (what an agent
  may merge/deploy/do) — that is `agent-authorization-matrix`; this console is
  for HUMAN operators.
- Do NOT use when: the task is the incident response PLAYBOOK (the steps taken
  during an incident) — that is `incident-response-runbook`; the console's
  tools SERVE that playbook, but the runbook is separate.

## Inputs to Inspect

1. Who operates: the operator personas (support agent, ops engineer,
   billing admin, superadmin) and what each legitimately needs to DO — the
   basis for least-privilege tiers.
2. The authorization policy (`authorization-matrix-designer` output): the
   roles/permissions and especially the impersonation and support-access
   RULES this console must enforce; if absent, that is a Stop Condition.
3. The current admin surface, if any: whether it is one god role, whether
   actions are audited, whether impersonation exists and how, and any
   insider-access or over-broad-admin incident history.
4. The sensitive actions the console can take: cross-tenant reads/writes,
   impersonation, data export, refunds/credits, account deletion, failover,
   data-repair — ranked by blast radius and reversibility.
5. The audit substrate (`audit-log-architect` output): what admin actions
   must record, and whether admin actions currently write audit records at
   all.
6. Compliance/contract obligations on operator access to customer data
   (support-access consent, data-residency, who-may-see-what) that constrain
   the design.

## Workflow

1. **Define least-privilege admin tiers.** Replace "admin can do everything"
   with tiers mapped to operator personas: e.g. **view-ops** (read-only
   support visibility), **write-ops** (bounded corrective actions), and
   **superadmin** (rare, dangerous, few people). Each tier lists what it can
   see and do; the highest tier is small and its use is exceptional. Enforce
   against the authorization policy — the console does not invent permissions,
   it applies them.
2. **Make cross-tenant access audited-by-construction.** Every console action
   that touches a tenant's data — read OR write — emits an audit record
   (operator identity, tenant, action, target, reason/ticket, timestamp) via
   `audit-log-architect`'s schema, and the emission is not skippable. An
   operator reading a customer's data is itself an audited event, not just
   writes. State how a read cannot happen without its audit record.
3. **Design impersonation / support-mode with hard boundaries.** The security-
   critical surface:
   - **It is always clearly impersonation, never silent.** The session is
     unmistakably marked as "operator X acting as user Y" everywhere,
     including in every audit record and downstream action.
   - **Bounded**: define what impersonation may and may NOT do (e.g. view to
     reproduce a bug: yes; change the user's password / make a payment / read
     another tenant: gated or forbidden). Sensitive actions while impersonating
     are separately gated.
   - **Consented where required**: per policy/contract, support-access may
     require the customer's consent or a support ticket; encode that gate.
   - **Audited end to end**: the impersonation start/stop and every action
     under it record BOTH the real operator and the impersonated user.
   - **Time-boxed**: an impersonation session auto-expires; it is not a
     standing capability.
4. **Design break-glass / elevation.** For rare high-privilege actions,
   elevation is: explicitly requested with a reason, approved (a second
   person for the highest tier, per `human-approval-boundary`), TIME-BOXED and
   auto-expiring, and heavily logged with a post-hoc review expectation.
   Standing superadmin is the anti-pattern; break-glass makes the dangerous
   power available on demand and accountable, not always-on.
5. **Design the operator control-plane.** Health/status views (telemetry
   embedded from `observability-operator`, but this is the action surface),
   and the manual operations operators need: retry a stuck job, trigger a
   failover, run a scoped data-repair. Every dangerous action is: scoped
   (names its target explicitly, no "apply to all"), previewable (dry-run /
   shows what it will change), reversible or backed-up-first, and audited.
   Data-repair that mutates customer data is the highest-risk button — gate
   it like impersonation.
6. **Design tenant-isolation-safe UX.** An operator viewing tenant A must not
   accidentally act on tenant B; the current tenant context is explicit and
   confirmed on write. Cross-tenant list/search views that rank tenants are
   themselves sensitive and access-controlled. Operator error is a threat
   model, not just malice.
7. **State the design-not-grant posture.** This skill designs the console and
   its controls; it does not provision real admin accounts, grant production
   access, or run operator actions — those follow the repo's approval path.
8. **Deliver** the console architecture, admin-tier + impersonation design,
   break-glass workflow, and audit contract in the Output Format, with policy,
   telemetry, agent, and runbook handoffs named.

## Output Format

```
ADMIN CONSOLE DESIGN — <system/domain>
Posture:        DESIGN ONLY — enforces the authz policy; grants no real access;
  runs no operator actions (those follow the approval path).
Operator personas → tiers: <persona — tier (view-ops/write-ops/superadmin) —
  can see / can do; enforced against authorization-matrix-designer's policy>
Cross-tenant audit: <every action (READ and write) emits operator/tenant/action/
  target/reason record via audit-log-architect; emission not skippable>
Impersonation/support-mode: <always-marked; bounded (allowed vs gated/forbidden
  actions); consent/ticket gate; records real operator + impersonated user;
  time-boxed auto-expiry>
Break-glass/elevation: <request + reason → approval (2nd person for top tier,
  human-approval-boundary) → time-boxed auto-expiry → heavy log + post-hoc review>
Operator control-plane: <health (telemetry embedded → observability-operator);
  actions: retry/failover/data-repair — each scoped, previewable/dry-run,
  reversible/backed-up-first, audited; data-repair gated like impersonation>
Tenant-safe UX: <explicit current-tenant context; write confirms tenant;
  cross-tenant ranking views access-controlled>
Boundaries:     authz POLICY → authorization-matrix-designer; TELEMETRY →
  observability-operator; AI-agent authority → agent-authorization-matrix;
  incident PLAYBOOK → incident-response-runbook
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Admin access is tiered and least-privilege, not one god role; the top
      tier is small and its use is exceptional.
- [ ] Every cross-tenant action — READ and write — emits an unskippable audit
      record (operator, tenant, action, target, reason).
- [ ] Impersonation is always clearly marked, bounded, consent/ticket-gated
      where required, time-boxed, and records both the real operator and the
      impersonated user.
- [ ] Break-glass elevation is requested-with-reason, approved (second person
      for the top tier), time-boxed/auto-expiring, and logged for post-hoc
      review — no standing superadmin.
- [ ] Dangerous control-plane actions (failover, data-repair) are scoped,
      previewable/dry-run, reversible or backed-up-first, and audited.
- [ ] The UX prevents cross-tenant operator error (explicit tenant context,
      write confirmation); cross-tenant ranking views are access-controlled.
- [ ] The console ENFORCES the authorization policy and does not author it;
      audit uses `audit-log-architect`'s schema.
- [ ] The design-only posture is explicit: no real access granted, no operator
      action run here.

## Gotchas

- The admin console is the softest target with the hardest reach: it crosses
  every tenant and is built with the least scrutiny. Treat it as the highest-
  privilege surface in the product, not an internal convenience.
- Silent impersonation is an incident generator and a trust breach: if an
  operator can act as a user without it being unmistakably marked and audited
  on both identities, you cannot answer "who actually did this?"
- Reads are not free: an operator browsing a customer's private data
  unaudited is exactly the insider-access failure regulators and customers
  care about. Audit reads, not only writes.
- Standing superadmin is a breach waiting for a stolen laptop; break-glass
  (time-boxed, approved, expiring) gives the same power without the always-on
  liability.
- A data-repair button with no dry-run and no scope is a production-wide
  foot-gun; "fix this record" must not be able to become "fix every record."
- Impersonation that can change a password / make a payment / delete an
  account turns support access into account takeover; gate sensitive actions
  separately from view-to-reproduce.
- An operator with tenant A open and tenant B in another tab writes to the
  wrong one; the current tenant context and a write-time confirmation are
  controls against ordinary error, not just malice.
- Embedding telemetry is fine; letting the console become a shadow
  observability tool (or the observability tool become an action surface)
  blurs seeing and acting — keep the action surface auditable.

## Stop Conditions

- The authorization policy / impersonation rules the console must enforce do
  not exist or are ambiguous → obtain them from `authorization-matrix-designer`
  before designing enforcement; a console enforcing an undefined policy grants
  power nobody scoped.
- Asked to grant real admin/superadmin access, provision operator accounts, or
  RUN an operator action (impersonate, failover, data-repair) against
  production → STOP: this skill DESIGNS the console and its controls; granting
  access or running privileged operator actions follows the repo's approval
  path (`human-approval-boundary`).
- A requested capability would enable unaudited cross-tenant access or silent
  impersonation → refuse that shape and require the audited, marked, bounded
  design instead; the convenience is the vulnerability.
- The design implies AI-agent operators acting through the console → the
  standing authority of an agent is `agent-authorization-matrix`'s decision,
  not a human-admin tier; route it there rather than granting an agent a human
  break-glass path.

## Supporting Files

- `evals/evals.json` — behavior cases: the admin-console design, the
  break-glass/impersonation edge, the unaudited-cross-tenant / silent-
  impersonation refusal, and the authorization-policy non-trigger.
- `evals/trigger-evals.json` — discrimination against
  `authorization-matrix-designer` (policy vs the console enforcing it),
  `observability-operator` (telemetry vs action surface),
  `agent-authorization-matrix` (AI-agent vs human-admin authority), and
  `incident-response-runbook` (playbook the console serves).
- No `references/` — the tier/impersonation/break-glass/control-plane procedure
  above is complete; detail lives in the produced artifacts.
