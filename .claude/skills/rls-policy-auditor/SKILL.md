---
name: rls-policy-auditor
description: Audit and (where asked) author row-level-security policies for a tenant-scoped database — inspect SELECT/INSERT/UPDATE/DELETE policies per table for missing tenant scope, deny-by-default gaps, policy recursion, unsafe SECURITY DEFINER helpers, over-broad GRANTs, service-role/superuser leakage, and frontend-derived (client-supplied) tenant scope, and ALWAYS deliver a negative-test plan proving wrong-tenant/wrong-role/missing-auth access is denied per command. Use when asked to review, write, or fix RLS/tenant-scoping policies, when RLS is enabled but unverified, or before shipping a tenant table. Do NOT use for app/API-layer isolation tests (multi-tenant-security-tester), general migration review (secure-migration-reviewer), or non-database threat modeling (threat-modeler).
---

# RLS Policy Auditor

## Purpose

Produce a database-level verdict on whether row-level security actually
enforces tenant and role scope, plus the negative tests that prove it. This
skill absorbs both policy authoring and negative-test design (reconciliation
§3): it inspects each table's SELECT/INSERT/UPDATE/DELETE policies for the
classic failure modes, writes or corrects policies where asked, and ALWAYS
delivers a per-command negative-test plan. RLS enabled is not RLS enforced —
a table with RLS on and no restrictive policy, or a policy that trusts a
client-supplied tenant id, is a finding. The deliverable is severity-ranked
findings with the offending policy quoted, remediation, and executable
negative tests as SQL/session sequences.

## Use When

- Use when: asked to review, audit, write, or fix RLS policies or tenant
  scoping at the database layer.
- Use when: RLS is enabled on tenant tables but nobody has verified the
  policies deny cross-tenant access.
- Use when: before shipping a new tenant-owned table, or after adding
  `SECURITY DEFINER` helpers or new GRANTs.
- Use when: converting an RLS finding into a permanent negative test.
- Do NOT use when: the isolation tests belong at the app/API layer across
  many surfaces — that is `multi-tenant-security-tester` (DB and app layers
  are complementary; hand off the non-DB surfaces).
- Do NOT use when: reviewing a whole migration for privilege/destructive
  changes beyond RLS — that is `secure-migration-reviewer` (route the RLS
  portion here).
- Do NOT use when: the ask is design-time threat enumeration —
  `threat-modeler`.
- Do NOT use when: tenant semantics are undefined — `tenant-modeler` first.

## Inputs to Inspect

1. The schema and migrations: `CREATE TABLE`, `ALTER TABLE … ENABLE ROW LEVEL
   SECURITY`, every `CREATE POLICY`, `CREATE FUNCTION`, and `GRANT`. No policy
   text or schema → Stop Conditions.
2. How tenant/user context reaches the database: session settings
   (`current_setting`), JWT claims, `auth.uid()`/`auth.jwt()` equivalents,
   connection roles — and whether that context is server-established or
   client-influenced.
3. The tenant model (`tenant-modeler`) and authorization matrix
   (`authorization-matrix-designer`) — policies are audited against THESE
   definitions of tenant and role, not re-derived here.
4. Roles and their GRANTs: application role, service/`service_role`, anon,
   and any role that BYPASSRLS or owns the tables.
5. Helper functions used inside policies: their `SECURITY` mode, `search_path`,
   and whether they re-query the same table (recursion risk).
6. Existing RLS tests, if any, and prior incidents.

## Workflow

1. **Confirm real policy text exists** and pin the tenant/role definitions
   being enforced. Undefined boundary → stop and route to `tenant-modeler`.
2. **Inventory tables** that hold tenant-owned data; for each, record whether
   RLS is ENABLED, whether it is FORCED (owners bypass otherwise), and which
   policies exist per command. A tenant table with RLS disabled or unforced is
   an immediate finding.
3. **Audit each command separately — SELECT, INSERT, UPDATE, DELETE** — using
   [references/rls-audit-checklist.md](references/rls-audit-checklist.md):
   - **SELECT/USING:** does every row require the caller's tenant scope?
   - **INSERT/WITH CHECK:** can a row be written with another tenant's id, or
     with no tenant id? Missing `WITH CHECK` on INSERT is a write-side hole.
   - **UPDATE:** both `USING` (which rows) AND `WITH CHECK` (resulting row) —
     a missing `WITH CHECK` lets a row be moved to another tenant.
   - **DELETE/USING:** can a caller delete another tenant's rows?
4. **Hunt the classic failure modes:** missing tenant scope; deny-by-default
   gap (permissive policy that ORs open access); **recursion** (policy calls a
   function that selects the same table under RLS); unsafe **SECURITY DEFINER**
   (no fixed `search_path`, broader than needed, returns rows bypassing
   caller scope); over-broad **GRANT** (e.g. `GRANT ALL … TO anon`);
   **service-role leakage** (service role reachable from a client-influenced
   path, or BYPASSRLS role used in request handling); **frontend-derived
   scope** (tenant id taken from a client value the user controls rather than
   a server-established session/JWT claim).
5. **Rank findings.** A confirmed cross-tenant read or write via policy is
   CRITICAL; each needs the concrete path (which command, which caller, which
   client-controlled input). No demonstrable path → cap at medium and name
   the confirming test.
6. **Author/correct policies where asked** — deny-by-default, tenant scope
   from server context, `WITH CHECK` on write commands, `SECURITY INVOKER`
   helpers with fixed `search_path` unless a DEFINER is justified and minimal.
   Present as a migration for `secure-migration-reviewer` to gate; do not
   apply to a live DB from this skill.
7. **Write the negative-test plan (mandatory)** per command and per failure
   mode: set the session to tenant A, attempt B's rows for SELECT/UPDATE/
   DELETE (expect zero rows / zero affected), attempt INSERT/UPDATE writing
   B's tenant id (expect rejection), attempt as anon/service-role, and include
   the positive control (A affects only A's rows). Provide as runnable SQL
   session sequences.
8. **Deliver** findings, corrected policies (if authored), and the negative
   tests, with an honest list of tables/commands not audited.

## Output Format

```
RLS AUDIT — <database/scope>
Enforced against: <tenant + role definitions (from tenant-modeler / authz matrix)>
Context source: <server session/JWT — or client-influenced (finding)>
Table inventory: <table — RLS enabled? forced? policies per command>
Findings (severity-ranked):
  [CRITICAL|HIGH|MEDIUM|LOW] <table.command> — <failure mode>
    Policy: <quoted policy or "absent">
    Path: <command + caller + client-controlled input → cross-tenant effect>
    Fix: <corrected policy / direction>
Authored/corrected policies (if requested): <SQL — as a migration, ungated>
Negative-test plan (per command):
  <id> — SET context = tenant A; <attempt on B> — EXPECT <0 rows / rejected>
         + positive control: <A on A's rows> — EXPECT allow
Not audited: <tables/commands + why>
Handoffs: <secure-migration-reviewer to gate the migration; multi-tenant-security-tester for app-layer>
```

## Validation Checklist

- [ ] Every tenant table's RLS enabled/forced status recorded; unprotected
      tables flagged.
- [ ] SELECT, INSERT, UPDATE, DELETE audited SEPARATELY per table.
- [ ] INSERT and UPDATE `WITH CHECK` presence verified (write-side holes).
- [ ] Recursion, SECURITY DEFINER search_path, broad GRANTs, service-role
      leakage, and frontend-derived scope each explicitly checked.
- [ ] Every finding quotes the offending policy (or "absent") and states a
      concrete cross-tenant path; CRITICALs have a demonstrable path.
- [ ] A per-command negative-test plan exists with positive controls,
      including anon and service-role attempts.
- [ ] Authored policies are deny-by-default and use server-derived scope;
      delivered as a migration, not applied live.
- [ ] Not-audited list present.

## Security Rules

- RLS enabled ≠ enforced: a table with RLS on and no restrictive policy, or a
  permissive policy that ORs open access, is treated as unprotected.
- Client-supplied / frontend-derived tenant scope in a policy is a finding
  regardless of demonstrated exploit — tenant scope must come from
  server-established session/JWT context.
- `SECURITY DEFINER` helpers without a pinned `search_path` are a finding
  (search-path hijacking); DEFINER is used only where justified and minimal.
- Service-role / BYPASSRLS credentials must not be reachable from request
  handling influenced by end users.
- No RLS finding is suppressed without written rationale via
  `human-approval-boundary`; every audit ships negative tests
  (master-prompt §6).

## Gotchas

- A correct SELECT policy with a missing INSERT `WITH CHECK` lets tenant A
  create rows owned by tenant B — write-side holes hide behind read-side
  correctness.
- UPDATE needs BOTH `USING` and `WITH CHECK`; with only `USING`, a caller can
  update their own row to carry another tenant's id (tenant hopping).
- Policies calling a helper that selects the same table re-enter RLS and
  either recurse or silently return nothing under load — test, don't assume.
- `FORCE ROW LEVEL SECURITY` matters: without it the table owner (often the
  migration/app role) bypasses policies entirely.
- Postgres RLS is deny-by-default only once a policy exists; enabling RLS with
  zero policies denies all — but a single permissive policy can reopen
  everything, so read every policy, not just the first.
- A DEFINER helper that returns rows to the caller can launder around the
  caller's own RLS — audit what the helper returns, not just that it exists.

## Stop Conditions

- No policy text, schema, or migration is available → stop; this skill does
  not audit RLS from a description.
- Tenant/role semantics are undefined or contested → stop; `tenant-modeler` /
  `source-of-truth-reconciler` first.
- A CRITICAL cross-tenant policy hole is confirmed in a live database → report
  the minimal reproduction immediately; containment is the human's call
  (`human-approval-boundary`) before continuing.
- Asked to APPLY authored policies to a live database → stop; deliver them as
  a migration for `secure-migration-reviewer` and human approval — this skill
  audits and authors text, it does not run DDL on live systems.

## Supporting Files

- [references/rls-audit-checklist.md](references/rls-audit-checklist.md) —
  per-command audit questions, the seven failure-mode catalog with detection
  and fix, and the negative-test session-sequence templates.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against
  `multi-tenant-security-tester`, `secure-migration-reviewer`, and the shipped
  `tenant-isolation-reviewer` (tenant security cluster).
