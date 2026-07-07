# Negative Test Matrix — surfaces, actors, operations, expected denials

Progressive-disclosure detail for `multi-tenant-security-tester`. Use this to
build the matrix and the fixtures. Every row is a test whose PASS = denial.

## Two-tenant fixture recipe

Seed deterministically and record ids:

- **Tenant A** and **Tenant B**, each with: one owner/admin user, one regular
  member, and (if roles differ) one lower-privilege role.
- Each tenant owns representative resources across the surfaces under test
  (e.g. A-invoice-1, B-invoice-1; A-doc-1, B-doc-1).
- One **anonymous** (no token) caller.
- Record every resource id so tests as A can attempt B's ids and vice versa.
- Mint tokens through the REAL auth/login/token path per tenant+role — never
  by writing tenant_id into internal state.

## Actors

| Actor | How | Represents |
|---|---|---|
| Wrong-tenant authenticated | A's token, B's resource id | The canonical SaaS attacker |
| Wrong-role authenticated | low-role token, high-role action | Privilege escalation |
| Anonymous | no token | Missing-auth / public exposure |
| Service-role / job | job or platform credential path | Background bypass |
| Support/admin | support console path | Brokered-access misuse |

## Operations × expected result

For each surface: read (by id), list, create, update, delete, export.
Expected result for a forbidden actor: **deny** — 403 or 404 (per policy),
empty result set, or job no-op — and **no data** in body/headers/errors.

## Surface catalog (cover each or mark not-covered)

1. **REST/RPC by-id (IDOR):** A requests B's resource by id → deny. Enumerate
   adjacent ids.
2. **List endpoints:** A lists → result contains zero B rows (test bulk
   leakage, not just single-id).
3. **Create/update mass-assignment:** A submits `tenant_id`/`owner_id`/`role`
   of B or elevated → field ignored/rejected, not honored.
4. **Search:** A searches a term only present in B's data → zero B results.
5. **AI retrieval / vector store:** A's query → zero chunks sourced from B's
   documents (canary-document test).
6. **Exports/imports:** export run as A contains only A's data; import cannot
   attach rows to B.
7. **Background jobs / webhooks:** job/webhook with platform credentials
   processes only the owning tenant's data; cross-tenant fan-out denied.
8. **Support/admin tooling:** access is brokered/audited; un-brokered
   cross-tenant read denied.
9. **Files/storage:** signed URL / bucket path for B not reachable by A;
   expiry enforced.
10. **Billing/usage/analytics:** A cannot read B's usage or invoices.

## Positive control (mandatory per negative test)

Pair every deny test with an allow test: the legitimate owner performs the
same operation on their own resource and succeeds. Without it, a global outage
(everything denied) passes as perfect isolation.

## Leakage assertions

- **Existence:** 404 vs 403 consistency — a 403 on B's id where a nonexistent
  id returns 404 leaks that B's record exists. Assert the chosen policy.
- **Error body:** assert errors do not echo another tenant's field values.
- **Headers:** no cross-tenant ids/etags/cache keys leak.
- **Timing:** only where the policy specifies constant-time behavior.

## Handoffs

- Database-layer RLS negative plan → `rls-policy-auditor`.
- Failing paths / fixes → `appsec-implementer` (app layer) or
  `secure-migration-reviewer` (schema/policy).
