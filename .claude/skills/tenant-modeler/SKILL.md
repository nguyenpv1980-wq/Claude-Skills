---
name: tenant-modeler
description: Define the tenant model for a SaaS product — what a tenant IS (organization, workspace, account), the hierarchy between those concepts, user-to-tenant membership (roles attached to membership, invitations, users in multiple tenants), ownership semantics, and the full tenant lifecycle from provisioning through suspension to offboarding and purge. Produces a tenant model definition, a lifecycle state machine with per-state access/billing/data posture, and a membership + invitation model. Use when tenant, organization, or workspace concepts are undefined or contested, when membership or invitation semantics keep causing confusion or rework, or BEFORE any multi-tenant schema, authorization, or platform design work. Do NOT use to review an existing system for cross-tenant leakage (tenant-isolation-reviewer) or to design tenant-scoped storage and query strategy (multi-tenant-data-architect) — this skill defines semantics; it does not design tables or audit code.
---

# Tenant Modeler

## Purpose

Produce the tenant model every other SaaS decision hangs off: a precise
definition of the tenant concept and its hierarchy, the membership model that
is the ONLY bridge between users and tenant data, ownership semantics, and a
lifecycle state machine where every state declares its access, billing, and
data posture. Schema, authorization, and platform design built on contested
tenant semantics get rebuilt; this skill exists so they are built once.

## Use When

- Use when: "tenant", "organization", "workspace", "team", or "account" mean
  different things to different people on the project — or nothing precise at
  all.
- Use when: membership questions keep recurring — can a user belong to two
  tenants, what happens to their content when they leave, who can invite whom.
- Use when: starting multi-tenant schema, authorization, or platform work and
  no written tenant model exists (run this first).
- Use when: lifecycle semantics are undefined — what suspension actually
  blocks, what offboarding exports, when purge is irreversible.
- Do NOT use when: checking whether an existing system leaks data across
  tenants — that is `tenant-isolation-reviewer`.
- Do NOT use when: choosing tenant_id-vs-schema-vs-database scoping — that is
  `multi-tenant-data-architect`, which consumes this skill's output.
- Do NOT use when: modeling the business domain broadly — `domain-modeler`
  owns general concept modeling; this skill owns the tenancy axis
  specifically.

## Inputs to Inspect

1. Existing code touching tenancy: models/tables named org, team, workspace,
   account; membership/join tables; invitation flows.
2. Existing docs and UI copy — what the product already calls these concepts
   in front of users (renaming shipped concepts is a migration, not an edit).
3. The domain model, if one exists (domain-modeler output).
4. Business facts from the human: who buys (company? individual?), who
   invites, whether users span tenants, what enterprise customers demand
   (SSO domains, seat pools, sub-organizations).
5. Billing shape: what the paying unit is — it is usually the tenant, and
   mismatches between paying unit and tenant unit are findings.

## Workflow

1. **Inventory candidate concepts** from code, docs, and UI. List every
   tenant-shaped noun and where each appears. Contradictions between code and
   docs are findings, not choices to make silently.
2. **Define the tenant.** One sentence: the unit of data ownership, billing,
   and administration. If those three units differ (e.g., billing per
   workspace but administration per org), model the hierarchy explicitly
   rather than overloading one concept.
3. **Fix the hierarchy.** Tenant → sub-units (workspaces/projects) → resources.
   State which levels own data, which merely group, and which level isolation
   is enforced at (usually the top; say so).
4. **Model membership.** Membership is an entity linking user ↔ tenant,
   carrying role and status — roles attach to the membership, never to the
   user. Decide: multi-tenant users, guest/external members, service
   accounts. Patterns in
   [references/tenant-lifecycle-catalog.md](references/tenant-lifecycle-catalog.md).
5. **Model invitations** as their own lifecycle (invited → accepted / expired
   / revoked), including re-invite, domain-capture, and who may invite.
6. **Define ownership semantics.** Every tenant has ≥1 owner; define owner
   departure (transfer, not orphan), last-owner protection, and what happens
   to a departing member's content (reassign vs tombstone — pick one).
7. **Draw the tenant lifecycle state machine**: provisioning → active →
   suspended → offboarding → purged (adapt as needed). Every state declares
   user access, data readability, billing behavior, and background-job
   behavior. Every transition names its trigger, side effects, and whether it
   is reversible — purge is the only irreversible one, and it is gated.
8. **Record assumptions and open questions**, each with risk-if-wrong and who
   answers. Then stop: hand to `multi-tenant-data-architect` for schema and
   `authorization-matrix-designer` for permissions — do not design those here.

## Output Format

```
TENANT MODEL — <product>
Tenant definition: <one sentence: unit of ownership, billing, administration>
Hierarchy: <tenant → sub-units → resources; which level owns data;
  which level isolation is enforced at>
Membership model: <entity, role-on-membership, statuses; multi-tenant users,
  guests, service accounts — each explicitly in or out>
Invitation model: <states, transitions, who may invite, expiry/revocation>
Ownership semantics: <owner rules, transfer on departure, last-owner guard,
  departing-member content policy>
Lifecycle state machine: <state — access posture — data posture — billing
  posture — jobs posture>; transitions with trigger, side effects, reversibility
Findings: <code/doc/UI contradictions discovered>
Assumptions & open questions: <each with risk-if-wrong / who answers>
Handoffs: multi-tenant-data-architect (schema), authorization-matrix-designer
  (permissions), saas-platform-architect (platform flows)
```

## Validation Checklist

- [ ] Tenant defined in one sentence covering ownership, billing, and
      administration — or an explicit hierarchy where they diverge.
- [ ] Roles attach to memberships, not users; the model works for a user in
      two tenants without contortion.
- [ ] Invitations have their own states, including expiry and revocation.
- [ ] Owner departure and last-owner cases are defined; no orphanable tenant.
- [ ] Every lifecycle state declares access, data, billing, AND jobs posture;
      no state where "suspended" is undefined for background work.
- [ ] Every transition names trigger, side effects, and reversibility; purge
      is explicitly gated and irreversible.
- [ ] No tables designed, no policies written — semantics only.

## Tenant Isolation Rules

- Membership is the ONLY bridge between a user and tenant data; any access
  path that skips membership (support, jobs, integrations) must be named in
  the model as a brokered exception, or it is a hole.
- Isolation is enforced at the declared tenant boundary — sub-unit "sharing"
  features stay inside it unless the model explicitly says otherwise.
- Suspension is an access change, not a data change; purge is a data change
  and is gated, logged, and irreversible by design.

## Gotchas

- The paying unit, the administering unit, and the data-owning unit drift
  apart as products grow enterprise features — model the divergence instead
  of overloading "organization."
- Personal/free workspaces are tenants too; leaving them implicit creates a
  shadow tenant type with undefined lifecycle and billing.
- Roles stored on the user table is the classic mistake this skill exists to
  prevent; it makes multi-tenant membership impossible to add later.
- Tenant rename/merge/split requests will arrive eventually; you need not
  design them now, but say explicitly they are out of scope if they are.
- "Delete the tenant" usually means offboard (suspend + export window), not
  purge; conflating them destroys data and trust.

## Stop Conditions

- The business cannot say who the paying/administering unit is → ask; the
  tenant definition cannot be assumed on their behalf.
- Code, docs, and UI contradict each other on core concepts → run
  `source-of-truth-reconciler` before modeling on top of the conflict.
- Tenant merge/split semantics are requested and genuinely ambiguous → stop
  and present options; both are data-destructive if guessed wrong.
- Asked to implement schema or permissions in the same pass → hand off per
  the output's Handoffs line; confirm scope before any code.

## Supporting Files

- [references/tenant-lifecycle-catalog.md](references/tenant-lifecycle-catalog.md) —
  lifecycle state/posture table, membership patterns (multi-tenant user,
  guest, service account), and the invitation state machine.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against
  `tenant-isolation-reviewer` and `multi-tenant-data-architect` (tenant
  cluster).
