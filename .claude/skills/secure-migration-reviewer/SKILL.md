---
name: secure-migration-reviewer
description: Review a database migration for security and deploy safety before it ships — privilege and GRANT changes, RLS/policy enablement gaps (a new tenant table with no policy), unsafe defaults, destructive or irreversible operations (DROP, non-nullable-without-default, type narrowing), data backfills that bypass tenant scope, lock/downtime risk, and forward/rollback safety with deploy-order coupling to code. Produces severity-ranked findings with evidence, a rollback assessment, and required negative tests for any tenant/authorization-affecting change. Use when reviewing a migration/DDL change or gating one before deploy. Delegates deep RLS-policy analysis to rls-policy-auditor. Do NOT use for app-code diffs (security-pr-reviewer), dependency/CI risk (supply-chain-security-reviewer), or SAST triage (static-analysis-reviewer).
---

# Secure Migration Reviewer

## Purpose

Decide whether a database migration is safe to deploy — on the security axis
(privilege, policy, tenant scope) and the operational axis (destructiveness,
locks, rollback, deploy order). The deliverable is severity-ranked findings
with evidence, a rollback assessment, and — for any change that affects tenant
scope or authorization — required negative tests. A migration that enables RLS
but adds no policy, adds a tenant table with no scoping, widens a GRANT, or
drops a column the currently-deployed code still reads is a finding here, not
after the incident. Deep RLS policy-text analysis is delegated to
`rls-policy-auditor`; this skill owns the whole-migration verdict.

## Use When

- Use when: reviewing a migration / DDL change (add/alter/drop table, column,
  index, policy, role, grant, function) before it merges or deploys.
- Use when: gating a schema change on safety, or asked "is this migration
  safe to run in production?".
- Use when: a backfill/data migration moves or transforms tenant-owned data.
- Do NOT use when: reviewing application-code changes for security — that is
  `security-pr-reviewer`.
- Do NOT use when: the task is deep RLS policy correctness (per-command
  USING/WITH CHECK, recursion, SECURITY DEFINER) — delegate to
  `rls-policy-auditor` (this skill flags that a policy needs that audit and
  routes it).
- Do NOT use when: the risk is dependency/CI supply chain
  (`supply-chain-security-reviewer`) or SAST output
  (`static-analysis-reviewer`).

## Inputs to Inspect

1. The migration itself: up and (crucially) down scripts, or the ORM
   migration files. No migration artifact → Stop Conditions.
2. The current schema state the migration transforms — what exists now, so
   destructiveness and compatibility can be judged.
3. The deployed application code's expectations: does live code read/write the
   columns/tables being changed? (deploy-order coupling — the classic
   expand/contract trap).
4. Security-relevant statements: `ENABLE/FORCE ROW LEVEL SECURITY`,
   `CREATE/ALTER POLICY`, `GRANT`/`REVOKE`, `CREATE ROLE`, `SECURITY DEFINER`
   functions, `ALTER DEFAULT PRIVILEGES`.
5. Data operations: backfills, `UPDATE`/`INSERT … SELECT`, and whether they
   carry tenant scope or run with elevated/service credentials.
6. Locking/volume characteristics: table size, index build strategy, whether
   the change takes a long lock on a hot table.

## Workflow

1. **Get both directions.** Read the up migration AND the down/rollback. A
   migration with no rollback path is a finding unless irreversibility is
   explicitly accepted.
2. **Classify the change** (`change-classification-gate`): schema/migration is
   high-validation and crosses `human-approval-boundary` for production.
3. **Security pass:**
   - New tenant-owned table → is RLS enabled AND a restrictive policy present?
     RLS enabled with no policy, or a table with no scoping, is a finding.
     Route policy-text correctness to `rls-policy-auditor`.
   - GRANT/REVOKE/role changes → does it widen access (e.g. `GRANT ALL`, grant
     to `anon`/public, new BYPASSRLS)? Least privilege preserved?
   - `SECURITY DEFINER` functions → flag for `rls-policy-auditor` (search_path,
     scope).
   - Unsafe defaults → a new `is_admin`/`role` column defaulting to a
     privileged value; a nullable tenant_id on a tenant table.
4. **Tenant-scope pass on data ops:** backfills and `INSERT … SELECT` must
   carry correct tenant scope; a backfill run as service-role that mislabels
   or cross-populates tenant rows is a critical data-integrity/isolation bug.
5. **Destructiveness pass:** `DROP TABLE/COLUMN`, `TRUNCATE`, type narrowing,
   `NOT NULL` without default on a populated table, renames — assess data loss
   and whether it's reversible.
6. **Deploy-order / compatibility pass:** does the currently-deployed code
   still use what's being dropped/renamed? Enforce expand→migrate→contract
   (add new, backfill, switch code, drop old) rather than a breaking
   single-step change.
7. **Lock/downtime pass:** will the change lock a hot table (adding a
   non-concurrent index, rewriting a large table, adding a validated FK)?
   Recommend concurrent/online strategies where the engine supports them.
8. **Rank findings, assess rollback, require negative tests** for any
   tenant/authorization-affecting change (hand implementable tests to
   `multi-tenant-security-tester` / `rls-policy-auditor`). Deliver a go /
   go-with-changes / no-go verdict.

## Output Format

```
SECURE MIGRATION REVIEW — <migration id/name>
Direction: up reviewed | down/rollback: <present? adequate?>
Change class: schema/migration — approval: <path / obtained?>
Findings (severity-ranked):
  [CRITICAL|HIGH|MEDIUM|LOW] <statement/line> — <security or safety issue>
    Evidence: <migration line / schema fact>   Fix: <remediation>
Security: RLS/policy <gap?> | GRANT/role <widened?> | defaults <unsafe?> | DEFINER <route to rls-policy-auditor>
Tenant-scope data ops: <backfill scope correct? credentials?>
Destructive ops: <op — data loss? reversible?>
Deploy order: <expand/contract respected? breaks live code?>
Lock/downtime: <hot-table lock risk + online alternative>
Rollback assessment: <reversible cleanly | forward-fix only | irreversible (accepted?)>
Required negative tests: <tenant/authz change → test> (→ rls-policy-auditor / multi-tenant-security-tester)
Verdict: go | go-with-changes | no-go — blockers: <...>
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] Both up and down (rollback) reviewed; missing rollback flagged.
- [ ] New tenant tables checked for RLS enablement AND a restrictive policy;
      policy-text audit routed to `rls-policy-auditor`.
- [ ] GRANT/REVOKE/role/DEFINER changes assessed for privilege widening.
- [ ] Backfills/data ops checked for correct tenant scope and credentials.
- [ ] Destructive ops assessed for data loss and reversibility.
- [ ] Deploy-order compatibility with currently-deployed code verified
      (expand→contract), not assumed.
- [ ] Lock/downtime risk on hot tables assessed with an online alternative.
- [ ] Tenant/authorization-affecting changes carry required negative tests.
- [ ] Verdict names blockers; not-reviewed list present.

## Security Rules

- A new tenant-owned table without RLS enabled and a restrictive policy is a
  finding — "we'll add the policy later" is an unprotected window.
- Widening GRANTs, granting to `anon`/public, or introducing BYPASSRLS on a
  request-path role is a finding; least privilege is the default.
- Backfills that touch tenant data must carry correct tenant scope; a
  service-role backfill that cross-populates tenants is critical.
- Any tenant-scope or authorization-affecting migration requires negative
  tests before it is called safe (master-prompt §6).
- Production migrations cross `human-approval-boundary`; this skill reviews
  and specifies — it does not run DDL on live systems.

## Gotchas

- Enabling RLS with zero policies denies all access (may break the app), while
  a single permissive policy can reopen everything — the security state
  depends on the full policy set, so route it to `rls-policy-auditor`.
- The migration that "just adds a column" breaks production when the column is
  `NOT NULL` without a default on a populated table, or when live code doesn't
  yet write it — sequencing matters as much as the DDL.
- Dropping a column/table in the same deploy as the code that stops using it
  races the rollout — the old pods still read it; use expand→contract.
- Adding an index non-concurrently locks writes on a hot table for the build;
  a big `ALTER TABLE` rewrite can lock for minutes — check volume.
- A down-migration that `DROP`s a column doesn't restore its data — "reversible
  schema" is not "reversible data"; say which you mean.
- Backfills running as a privileged role silently bypass RLS — correctness of
  the tenant scoping is on the query, not the policy, in that path.

## Stop Conditions

- No migration artifact (up/down or ORM files) is available → stop; do not
  review a migration from a description.
- The migration is about to run against production and its blast radius or
  rollback is unclear → stop for `human-approval-boundary`; do not bless it.
- Deep RLS policy correctness is the crux → route to `rls-policy-auditor` and
  gate the verdict on that audit.
- Asked to APPLY the migration to a live database → stop; this skill reviews;
  execution is a separate, approved operational step.

## Supporting Files

- [references/migration-safety-checklist.md](references/migration-safety-checklist.md)
  — the security/destructiveness/deploy-order/lock checklists, the
  expand→contract pattern, and per-engine online-DDL notes.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `security-pr-reviewer`,
  `rls-policy-auditor`, `static-analysis-reviewer`, and the shipped
  `code-reviewer` (security-review cluster).
