# Scoping Strategy Tradeoffs & Migration Patterns

Supporting detail for `multi-tenant-data-architect`. Read on demand.

## Scoping strategy tradeoff table (per store)

| | Pooled (tenant key) | Schema-per-tenant | Database-per-tenant |
| --- | --- | --- | --- |
| Isolation enforcement | Code/policy-enforced every query | Connection/search-path routing | Connection routing |
| Migration cost | One migration | × tenant count | × tenant count |
| Noisy neighbor | Shared everything; needs quotas | Shared instance resources | Isolated per DB |
| Cost floor per tenant | ~zero | Low | Instance/DB minimum |
| Tenant purge | DELETE + verify everywhere | DROP SCHEMA | DROP DATABASE |
| Fits | Many small tenants | Mid-count, moderate isolation optics | Few large/regulated tenants |
| Classic failure | One missing WHERE clause | Search-path bug routes to wrong schema | Fleet drift; forgotten tenant DB on old version |

Mixed is the common real answer: pooled default, database-per-tenant for the
few tenants whose contracts or size demand it, with a tenant→home routing
table that is itself treated as an isolation control.

## Tenant-context propagation mechanisms

| Mechanism | Where it binds | Watch for |
| --- | --- | --- |
| Middleware + scoped repository | Request middleware → repo constructor | Escape hatches: raw query access bypassing the repo |
| ORM default scope / global filter | Model layer | Code that disables the scope "temporarily"; bulk ops that skip hooks |
| DB session variable (+ policy) | Per-connection/session | Connection pooling resetting or leaking the variable across requests |
| Job context envelope | Queue message carries tenant id explicitly | Fan-out jobs that iterate tenants inside one context |

Whichever is chosen: one binding point, no data-path API accepts a tenant id
from the client, and the escape hatches are enumerated in the design.

## Retrofit migration pattern (expand → contract)

1. **Expand** — add nullable tenant key columns; no behavior change. Rollback:
   drop columns.
2. **Backfill** — derive tenant ownership; write keys in batches. Rollback:
   re-run or null out; no reads depend on it yet.
3. **Verify** — per-tenant row counts vs expected ownership; spot checksums on
   the ambiguous tables; unresolved rows go to a quarantine report, not a
   default tenant.
4. **Enforce** — scoped reads/writes behind a flag; dual-read comparison in
   shadow mode first. Rollback: flip the flag.
5. **Contract** — make keys NOT NULL, drop legacy unscoped paths. Only after
   enforcement has soaked. Rollback: restore the old path from the previous
   step, which is why it isn't deleted until now.

The verification gate (step 3) is the difference between a migration and a
mass mis-assignment of customer data.
