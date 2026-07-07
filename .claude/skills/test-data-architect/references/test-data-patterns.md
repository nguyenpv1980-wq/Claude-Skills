# Test Data Patterns

Detail file for `test-data-architect`. Loaded on demand.

## Persona catalog template

| Persona | Tenant | Role | Stable identifier | Notes |
| --- | --- | --- | --- | --- |
| owner-t1 | tenant-1 | owner | owner@t1.test | billing-capable |
| admin-t1 | tenant-1 | admin | admin@t1.test | |
| member-t1 | tenant-1 | member | member@t1.test | least privilege |
| owner-t2 | tenant-2 | owner | owner@t2.test | cross-tenant counterpart |
| anon | — | — | — | unauthenticated |

Two tenants minimum keeps the catalog compatible with the A/B fixture recipe
`multi-tenant-security-tester` requires — its negative-test assertions stay
in that skill; this catalog just guarantees the world supports them.

Reserved synthetic domains/names only (`*.test`, `*.example`), never
real-looking customer identities.

## Factory patterns

- **Single shape truth:** one factory definition per entity used by all
  layers; unit layer calls `build()` (in-memory), integration/E2E call
  `create()` (persisted through real paths).
- **Override-only variation:** `createInvoice({ status: 'overdue' })` —
  defaults are the simplest valid state; every override is visible at the
  call site.
- **Association discipline:** factories create their own parents by default
  but ACCEPT injected ones — tests composing scenarios stay explicit.
- **No raw-insert bypasses:** persistence goes through the app's write path
  or real migrations so constraints/defaults/hooks apply. Impossible states
  may be built ONLY for unit-level edge tests, in memory, labeled as such.

## Namespacing schemes (parallel isolation)

- Worker prefix: `w<index>-` on tenant slugs/emails/resource names
  (`test.info().parallelIndex`, `VITEST_POOL_ID`, or equivalent).
- Run id: `r<ci-run>-` prefix for E2E-created data on shared environments —
  enables TTL sweeps (`delete where name like 'r123-%'`).
- Baseline rows are READ-ONLY by convention AND (where possible) by
  role — the test user lacks permission to mutate catalog rows.

## Synthetic generation rules

- Names/emails/companies from fixed word lists with seeded selection —
  deterministic run-to-run.
- Realistic distributions only where behavior depends on them (long names
  for truncation tests are explicit fixtures, not lottery wins).
- Numbers/money: cover the boundary catalog (0, negative, max, precision)
  as named fixtures, not random draws.

## TTL & traceability

Every created record carries a marker (naming prefix or metadata column
where the schema allows): run id + test id. Orphan sweep: scheduled job or
suite-start sweep deleting expired `r*-` data older than TTL on shared envs.
Local ephemeral DBs skip TTL — recreate instead.
