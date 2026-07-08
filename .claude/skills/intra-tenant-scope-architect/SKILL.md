---
name: intra-tenant-scope-architect
description: Design a second mandatory data-scoping axis BELOW the tenant (location / site / region / org-unit / business-unit) for a multi-tenant SaaS — the per-user scope-grant model, the composite row-filter predicate on every scoped table (tenant_id AND scope), which roles are scope-restricted vs tenant-wide, server-derived propagation through app and edge layers, and the migration to add the axis to a live per-tenant schema. Presupposes the tenant boundary; this is a sub-tenant dimension inside ONE tenant, not a new tenant. Use when users in a tenant must see only a subset of its data by an org dimension (a store manager sees one store; a regional lead sees a region; admins see all). Do NOT use for tenant SEMANTICS or tenant hierarchy (tenant-modeler), tenant_id-axis storage strategy (multi-tenant-data-architect), or roles×permissions authz (authorization-matrix-designer). Reshapes live schema — DESIGNS the migration, does not run it.
---

# Intra-Tenant Scope Architect

## Purpose

Design a **second mandatory scoping axis below the tenant** — a location,
site, region, org-unit, or business-unit dimension by which users inside a
single tenant see only a subset of that tenant's data. The deliverable is the
scope model, a per-user scope-grant model, a classification of roles into
scope-restricted vs tenant-wide, the composite row-filter predicate that every
scoped table carries (`tenant_id = current_tenant AND (scope in
granted_scopes OR user is tenant-wide)`), the server-side propagation contract
through app and edge layers, and the migration to add the axis to a live
per-tenant schema. The discipline mirrors tenant scoping one level down:
deny-by-default on scope, scope derived server-side from a grant model, never
from the client. This presupposes the tenant boundary already works — it adds
a dimension inside a tenant, it does not define or replace the tenant.

## Use When

- Use when: within one tenant, users must be restricted to a SUBSET of that
  tenant's data along a stable organizational dimension — a store manager sees
  one store, a regional lead sees a region, HQ/tenant-admins see everything.
- Use when: retrofitting a site/region/org-unit filter onto an existing
  per-tenant schema where today every member of a tenant sees all of it.
- Use when: deciding which roles are scope-restricted vs tenant-wide and how a
  user's scope set is assigned and propagated to every query.
- Do NOT use when: the question is what a tenant IS, or a parent/child tenant
  hierarchy — that is `tenant-modeler`; a child tenant is a separate tenant
  with its own boundary, whereas a scope is a filter WITHIN one tenant.
- Do NOT use when: designing the tenant-scoped data layer around `tenant_id`
  itself (per-store pooled/siloed strategy, the tenant propagation contract) —
  that is `multi-tenant-data-architect`; this skill adds a subordinate axis and
  presupposes that layer.
- Do NOT use when: designing roles × permissions × resources — what a role CAN
  do, object-level authz — that is `authorization-matrix-designer`; a scope is
  a propagated ROW-FILTER dimension, not a permission. The same role can be
  held by two users with different scopes.
- Do NOT use when: the "scope" is really an ad-hoc share of one record with a
  colleague (`share-link-access-architect` / member sharing), not a standing
  organizational axis.

## Inputs to Inspect

1. The tenant model (`tenant-modeler` output): confirm the org dimension is a
   sub-tenant axis, not a separate tenant — and whether it already exists.
2. The existing per-tenant schema: which tables hold tenant data, where
   `tenant_id` enforcement lives today, and whether a site/unit column exists.
3. The role model: which roles should be scope-restricted (see only granted
   scopes) vs tenant-wide (see the whole tenant — admin, owner, auditor).
4. How a user is associated with a site/region/unit today, if at all — the
   raw material for the scope-grant model.
5. The app and edge layers that build queries (middleware, ORMs, an
   edge/gateway that constructs filters) — every place scope must propagate.
6. Reference/shared data within the tenant that is deliberately tenant-wide
   (not scoped) — so the predicate isn't wrongly applied to it.

## Workflow

1. **Confirm the axis is real, mandatory, and organizational.** It must be a
   stable dimension (site/region/unit), not an ad-hoc filter. If it is a
   separate legal/data boundary, it is a child TENANT (`tenant-modeler`); if it
   is "share this one record with a colleague," it is a sharing grant
   (`share-link-access-architect`/`authorization-matrix-designer`). Stop and
   reroute if either is true.
2. **Model the scope dimension.** The scope entity (site/region/unit), its
   relationship to the tenant (a scope belongs to exactly one tenant), and
   whether scopes nest (region → site) — nesting changes the predicate.
3. **Design the per-user scope-grant model.** A user is granted one or more
   scope values within their tenant; state how a new user gets a default scope
   and how grants are added/revoked. This grant set is the source of truth the
   predicate reads — it is not stored on the client.
4. **Classify roles.** Split roles into scope-restricted (filtered to granted
   scopes) vs tenant-wide (bypass the scope filter — admin/owner/auditor). This
   exception is load-bearing; name it explicitly and keep the tenant-wide set
   small and audited.
5. **Write the composite row-filter predicate.** Every scoped table carries
   the scope key and enforces
   `tenant_id = current_tenant AND (scope_id = ANY(current_user_scopes) OR
   current_user_is_tenant_wide)` — deny-by-default on scope exactly as tenant
   scoping is deny-by-default on tenant. List which tables are scoped vs
   deliberately tenant-wide.
6. **Define server-side propagation.** The user's scope set is derived
   server-side from the grant model, bound once per request/job like tenant
   context, and carried to every query — including any edge/gateway layer that
   builds filters. A client-supplied scope value is the intra-tenant IDOR;
   forbid it by contract.
7. **Plan the live migration.** Add the scope column (nullable → backfill →
   NOT NULL), assign existing users a scope set, add the composite predicate in
   shadow, verify per-scope counts, then enforce. This reshapes a live schema —
   this skill DESIGNS the migration; it does not run it. Defer the RLS policy
   SQL correctness to `rls-policy-auditor`; here the axis and predicate SHAPE
   are the deliverable.

## Output Format

```
INTRA-TENANT SCOPE DESIGN — <product/tenant model>
Axis confirmed: <site/region/unit; NOT a child tenant, NOT a sharing grant>
Scope model: <scope entity → belongs to one tenant; nesting? region→site>
Per-user scope-grant model: <how users are granted scopes; default; revoke>
Role classification: <scope-restricted roles | tenant-wide (bypass) roles>
Composite predicate (every scoped table): tenant_id = current_tenant AND
  (scope_id = ANY(current_user_scopes) OR current_user_is_tenant_wide)
Scoped vs tenant-wide tables: <which carry the scope key; which don't and why>
Propagation contract: <scope set derived server-side, bound once, carried to
  app + edge queries; client-supplied scope forbidden>
Live migration: <add column → backfill → assign scopes → shadow predicate →
  verify per-scope counts → enforce — DESIGNED, not executed>
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] The axis is confirmed a sub-tenant organizational dimension, not a child
      tenant and not an ad-hoc share.
- [ ] Every scoped table carries the scope key and the composite predicate;
      tenant-wide/reference tables are explicitly listed as not scoped.
- [ ] The predicate is deny-by-default on scope; tenant-wide roles bypass it
      through a named, small, audited exception — not an implicit hole.
- [ ] The user's scope set is derived server-side from the grant model and
      bound once per request; no query trusts a client-supplied scope value.
- [ ] Propagation reaches the edge/gateway layer too, not just the app layer.
- [ ] The migration is expand → backfill → shadow → verify → enforce, each step
      reversible; it is designed, not executed.
- [ ] RLS policy SQL correctness is deferred to `rls-policy-auditor`; this
      delivers the axis and predicate shape.

## Tenant Isolation Rules

- The scope axis is SUBORDINATE to the tenant axis — it filters within a
  tenant and never crosses one. The predicate always keeps `tenant_id =
  current_tenant` as the outer condition; scope is the inner one.
- Scope, like tenant, is derived server-side from the authenticated
  principal's grants — never from request bodies, query params, or headers.
- Deny-by-default on scope: a scoped row with no matching grant is invisible,
  the same posture as an out-of-tenant row.
- Tenant-wide bypass is an enumerated exception, not a default: the roles that
  see the whole tenant are listed, kept minimal, and their broad reads audited.
- A missed scoped table is an intra-tenant leak — the isolation test matrix
  covers every scoped table, mirroring the tenant-layer matrix one level down.

## Gotchas

- The tenant-wide exception is forgotten in the predicate, so admins get locked
  out of their own tenant — or it is written too broadly and every role bypasses
  scope. Get this one clause exactly right.
- One scoped table is missed and it becomes the intra-tenant leak — the same
  failure mode as an unscoped store at the tenant layer, one level down.
- A client-supplied scope value is trusted "because the UI already filters" —
  that is the intra-tenant IDOR in its purest form.
- Scopes that should nest (a region contains sites) but are modeled flat, so a
  regional lead can't see their own sites without a grant per site.
- Confusing a scope (a filter inside one tenant) with a child tenant (a
  separate boundary) — the two have opposite data-sharing defaults.
- The edge/gateway layer builds a query without the scope filter because
  propagation stopped at the app layer — every query-building layer must carry it.

## Stop Conditions

- The axis turns out to be a child TENANT (separate legal/data boundary) →
  stop; route to `tenant-modeler`. It is not a scope.
- The axis turns out to be an ad-hoc share of specific records → route to
  `share-link-access-architect` or member sharing in
  `authorization-matrix-designer`; a scope is a standing organizational axis.
- The migration must run against a live schema (add NOT NULL column, backfill,
  flip the predicate) → this skill DESIGNS it; executing follows
  `human-approval-boundary`. Do not run it.
- The tenant boundary itself is undefined or contested → `tenant-modeler`
  first; a subordinate axis on an undefined boundary is confident nonsense.

## Supporting Files

- `evals/evals.json` — behavior cases: the add-a-site-axis design, the
  child-tenant-not-a-scope refusal, the tenant-wide-bypass edge, and the
  client-supplied-scope IDOR catch.
- `evals/trigger-evals.json` — discrimination against `tenant-modeler` (tenant
  semantics/hierarchy), `multi-tenant-data-architect` (`tenant_id`-axis storage
  strategy), and `authorization-matrix-designer` (roles×permissions vs a
  row-filter dimension).
- No `references/` — the grant model, predicate, and migration above are the
  complete procedure; detail lives in the produced artifacts.
