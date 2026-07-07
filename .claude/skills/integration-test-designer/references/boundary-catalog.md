# Boundary Catalog

Detail file for `integration-test-designer`. Loaded on demand.

## Boundary classification table (template)

| Dependency | Class | In-suite status | Rationale |
| --- | --- | --- | --- |
| application service / command bus | owned | REAL | the wiring under test |
| database (schema + queries + constraints) | owned | REAL | persistence behavior is the point |
| auth middleware / session derivation | owned | REAL | context minting must traverse it |
| permission checks / guards | owned | REAL | functional enforcement under test |
| internal queue/jobs | owned | REAL or in-process driver | prefer real broker only if cheap |
| third-party HTTP (payments, email, LLM) | external | FAKED at owned adapter | nondeterministic, costs money |
| clock | ambient | FAKED (controllable) | determinism |
| randomness/ids | ambient | FAKED (seeded) | determinism |

Rule: fakes live at OWNED adapters (the repo's client wrapper), never by
patching a vendor SDK's internals.

## Isolation mechanisms compared

- **Transaction rollback per test:** open transaction in setup, roll back in
  teardown. Fast; breaks when code under test commits or uses multiple
  connections — know your stack.
- **Schema/DB per worker:** migrate once per worker into an isolated schema.
  Robust for parallelism; slower startup.
- **Truncation:** simple, serial-only; last resort.

Whichever is chosen: seed via real migrations + factories so constraint and
default behavior is production-shaped (a hand-inserted row that skips a
NOT NULL default hides bugs).

## Auth-minting recipes

1. Call the real signup/invite service in a fixture to create persona users.
2. Mint tokens through the real token issuer (test signing key), or login
   endpoint where cheap.
3. Cache per-persona context per worker; never share mutable sessions across
   workers.
4. Forbidden: constructing a session/claims object by hand and injecting it
   past the middleware — the test then proves nothing about derivation.

## Seam-failure case catalog

For every FAKED seam, include at least: timeout, 5xx/error shape, and
malformed-success (2xx with unexpected body). The behavior under test is the
module's handling, not the fake itself. Keep fake response shapes pinned to
recorded or documented provider fixtures; shape/version drift detection is
`api-contract-test-designer`'s layer.
