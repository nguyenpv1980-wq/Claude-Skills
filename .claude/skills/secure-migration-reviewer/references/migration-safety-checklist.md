# Migration Safety Checklist

Progressive-disclosure detail for `secure-migration-reviewer`. Cover security,
destructiveness, deploy order, and locking. Deep RLS policy correctness is
`rls-policy-auditor`'s job — flag and route it.

## Security checklist

- [ ] New tenant-owned table: `ENABLE ROW LEVEL SECURITY` present AND a
      restrictive policy exists? (RLS on with no policy = denies all; no RLS =
      wide open). `FORCE ROW LEVEL SECURITY` if the owner role touches it.
- [ ] `GRANT`/`REVOKE`: does it widen access? `GRANT ALL`, grant to
      `anon`/`public`, new role with `BYPASSRLS`, `ALTER DEFAULT PRIVILEGES`
      broadening future grants → finding.
- [ ] New `SECURITY DEFINER` function → route to `rls-policy-auditor`
      (search_path pinned? minimal privilege? returns caller-scoped rows?).
- [ ] Unsafe defaults: privileged default on a role/flag column
      (`is_admin default true`), nullable `tenant_id` on a tenant table,
      permissive default policy.

## Tenant-scope data-op checklist

- [ ] Backfills / `UPDATE … SET` / `INSERT … SELECT` carry correct tenant
      scope — no cross-tenant population.
- [ ] Data ops running as service-role/superuser bypass RLS: scoping
      correctness is on the QUERY; verify it explicitly.
- [ ] Idempotent/resumable for large backfills (safe to re-run after failure).

## Destructiveness checklist

| Operation | Risk | Note |
|---|---|---|
| DROP TABLE/COLUMN | data loss | irreversible data even if schema reversible |
| TRUNCATE | data loss | not transactional in some engines |
| NOT NULL w/o default on populated table | fails / locks | backfill first, then constrain |
| Type narrowing (text→int, larger→smaller) | truncation/failure | validate data first |
| Rename table/column | breaks live code | expand→contract instead |
| Non-concurrent index on hot table | write lock during build | use concurrent/online build |

## Deploy-order: expand → migrate → contract

1. **Expand:** add new column/table (nullable/defaulted, non-breaking).
2. **Migrate:** backfill data (scoped, idempotent).
3. **Switch:** deploy code that writes/reads the new shape.
4. **Contract:** only after all pods run new code, drop the old column/table.

Never drop/rename in the same deploy as the code change — old instances still
use the old shape during rollout.

## Lock / downtime checklist

- Adding an index → concurrent (`CREATE INDEX CONCURRENTLY` in PG) off a
  transaction.
- Adding a FK → add `NOT VALID` then `VALIDATE CONSTRAINT` to avoid a long lock.
- Adding a column with a volatile default on a big table → may rewrite;
  prefer nullable + backfill in batches.
- Big `ALTER`/rewrite on a hot table → schedule / online tooling
  (pg_repack, gh-ost, pt-online-schema-change) per engine.

## Rollback assessment

State clearly which is true:
- **Reversible cleanly** — down migration restores prior schema AND data.
- **Forward-fix only** — down restores schema but data is lost/changed.
- **Irreversible** — must be explicitly accepted via `human-approval-boundary`.

## Required negative tests (tenant/authz changes)

Any migration touching RLS, policies, grants, roles, or tenant columns must
ship negative tests before "safe": route to `rls-policy-auditor` (DB layer)
and `multi-tenant-security-tester` (app layer). The verdict is not "go" until
those tests exist.
