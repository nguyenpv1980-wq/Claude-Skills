# Isolation Surface Checklist

Supporting detail for `tenant-isolation-reviewer`. Every review classifies all
fifteen surfaces; none may be silently skipped.

| # | Surface | What to check | Classic hole |
| --- | --- | --- | --- |
| 1 | Identity & session | Tenant context bound server-side at auth; token claims vs client params | Tenant id accepted from request body/header and trusted |
| 2 | Data layer | Every tenant-owned table scoped; scoping enforced (filters/RLS), not conventional | By-id lookup with no tenant predicate (IDOR at the SQL layer) |
| 3 | API | Middleware binds tenant before handlers; object-level checks on every resource id | Route checks the user is logged in but not that the resource is theirs |
| 4 | File/object storage | Per-tenant prefixes/buckets; signed URLs scoped and expiring | Guessable/global paths; signed URL grants wider prefix than the file |
| 5 | Logs | No tenant business data in shared logs; tenant-scoped log views if exposed | Debug logging dumps another tenant's payload into a shared stream |
| 6 | Analytics | Events tagged by tenant; dashboards scoped; small-cohort aggregation rules | Product-analytics tool receives raw cross-tenant events, exposed to staff or embedded back into the product |
| 7 | Support/admin tooling | Brokered, scoped, time-boxed, audited access | Support console = raw DB session with platform credentials |
| 8 | Exports | Export jobs run under the requesting tenant's scope; output stored scoped | Export worker uses service role and a WHERE clause someone edits |
| 9 | Imports | Imported rows forced to the importing tenant; no tenant column honored from file content | CSV with a tenant_id column that the loader trusts |
| 10 | Background jobs | Jobs carry explicit tenant context; fan-out iterates tenants with per-tenant scope | Nightly job queries all tenants, writes results to the wrong one on error |
| 11 | Search | Index entries carry tenant key; queries filtered at the engine, not post-filtered in app code | Shared index queried by keyword only; ranking leaks other tenants' titles |
| 12 | AI retrieval | Embedding/vector stores partitioned or filtered by tenant; retrieval runs under the requesting tenant's scope; prompts never mix tenants' documents | RAG corpus built tenant-blind; model happily quotes tenant B to tenant A |
| 13 | Billing | Usage events attributed to the right tenant; invoices/portal scoped | Metering aggregation keyed by user id where users span tenants |
| 14 | Feature flags | Tenant-targeted flags cannot be toggled or read cross-tenant; flag payloads carry no other tenant's config | Flag evaluation endpoint returns the full targeting rule list including other tenants' names |
| 15 | Audit | Audit events carry tenant id; tenant-facing audit views scoped; audit reads are themselves audited for staff | Tenant admin's audit page paginates the global audit table |

## Negative-test shapes (minimum set)

- Tenant A user requests tenant B resource by id → expect deny/404/empty (per
  the stated policy) on API, storage URL, export download, and search.
- Tenant A membership revoked/suspended → previously working reads now fail,
  including active sessions and API tokens.
- Support/staff access without an active brokered grant → denied and the
  attempt is audited.
- Background job or webhook processing for tenant A cannot write to tenant B
  (force an error mid-fan-out and assert no cross-write).
- AI retrieval query from tenant A returns zero chunks originating from
  tenant B's documents, verified against a seeded canary document.
