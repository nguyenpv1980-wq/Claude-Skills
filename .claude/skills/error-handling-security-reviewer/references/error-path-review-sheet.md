# Error-Path Review Sheet

The four lenses with the concrete patterns to hunt. Language-agnostic; the
shapes below appear in every stack.

## Lens 1 — Fail-open defaults

Hunt for a security decision whose failure branch is anything but DENY:

- `catch { return true; }` / `catch { return defaultAllow; }` around a
  permission, plan, or feature check.
- Authz lookup timeout → exception propagates past the check → handler
  returns a response as if authorized.
- Allowlist/denylist/policy fetched at runtime: what happens when the fetch
  fails or returns empty? Empty-list-means-allow is a finding.
- Cached "last known" decision served on backend failure — stale-allow after
  a revocation.
- Feature flags gating SECURITY behavior with a permissive default when the
  flag service is down.
- Rate limiter / quota backend unavailable → limiter becomes a no-op.

## Lens 2 — Error-path authorization

Follow every alternate branch end-to-end and re-ask "who is the caller and
was that checked HERE?":

- Fallback endpoints/degraded modes that skip middleware the primary path
  had (handler order: does the error handler sit BEFORE authz in the chain?).
- Retry queues / background re-execution running under a system identity
  after the caller's session expired — replay without re-authorization.
- Error pages / error controllers that render data fetched without the
  original request's tenant scope.
- Multi-step flows where a failure in step 2 re-enters step 3 with step 1's
  stale authorization.

## Lens 3 — Exception-driven bypass

For each try/catch/finally around security logic, ask what the exception
SKIPS while execution continues:

- Empty catch / log-only catch around validation, authz, signature
  verification, audit writes.
- Catch-and-continue "to keep the request alive" — the guarded action still
  happens after the guard threw.
- `finally` blocks that swallow or replace the security exception.
- Partial failure committed as success: transaction half-applied, audit
  write failed but the action stood (see audit-log-architect's
  audit-write-failure policy), rate-limit counter never incremented on the
  error path.
- Exception type-matching that lets unexpected exception classes sail past
  the deny branch.
- Input-triggered exceptions as a steering wheel: oversized payloads,
  malformed encodings, connection aborts used to reach the weak branch.

## Lens 4 — Leak-free error responses

Per failure class, what does the caller receive — in EVERY environment
configuration:

- Stack traces, exception class names/messages, SQL fragments, file paths,
  internal hostnames/IPs, dependency names and versions.
- Secrets/tokens echoed in messages or headers; request bodies reflected
  back verbatim.
- Existence oracles: 403-vs-404 asymmetry on enumerable resources;
  "wrong password" vs "no such user"; timing differences on valid vs
  invalid identifiers; verbose validation errors enumerating expected
  fields/formats.
- Debug/verbose error modes reachable via config drift, header tricks, or a
  non-production environment serving production data.
- Correlation-id discipline: generic message + correlation id OUT, rich
  detail in internal logs — the pattern to recommend, not detail out.

## Fail-closed matrix template

| Security decision | Exception | Timeout | Empty/null result | Dependency down |
|---|---|---|---|---|
| (e.g., permission check) | deny / ALLOW / skip / unverified | … | … | … |

Every non-deny cell is a finding or an explicitly human-accepted risk with a
reference. Cells you cannot determine are "unverified" — never assumed deny.

## Severity guide

Set severity by what the failed guard protects and who can trigger the
failure: attacker-triggerable + guards authz/tenant isolation → high;
attacker-triggerable + information oracle → medium-high; requires operator
error or rare infra state → lower, but named. A tiny catch block guarding a
tenant boundary is a high-severity finding regardless of its size.
