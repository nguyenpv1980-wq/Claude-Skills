# Control Implementation Patterns

Progressive-disclosure detail for `appsec-implementer`. Each pattern gives the
boundary the control belongs at, the minimal implementation notes, and the
shape of the negative test that proves it. Always reuse the project's existing
utilities; these are checklists, not copy-paste code.

## Input validation

- **Boundary:** server-side request handler, before the value is used.
- **Do:** validate type, length/range, format, and allowed set (allowlist, not
  denylist). Reject or normalize; decide which and be consistent.
- **Negative test:** send an over-long / wrong-type / out-of-set value → expect
  4xx/rejection. **Positive test:** a legitimate edge value (unicode name, plus
  in email) is accepted — over-strict validators are availability bugs.

## Output encoding (XSS)

- **Boundary:** at render/serialization, per output context (HTML body, HTML
  attribute, JS, URL, CSS) — context determines the encoder.
- **Do:** use the framework's contextual auto-escaping; treat any raw/`dangerouslySetInnerHTML`/`|safe` as a finding needing justification.
- **Negative test:** render a payload like `"><script>` and assert it appears
  inert/escaped in the output, not executed.

## Parameterized queries (SQL/NoSQL injection)

- **Boundary:** the data-access call.
- **Do:** bind parameters via the ORM/driver; never string-concatenate user
  input into a query, including ORDER BY / LIMIT / column names (allowlist those).
- **Negative test:** input `1; DROP` / `' OR '1'='1` → expect a bound literal,
  no injection; assert row count / error, not a stack trace.

## Object-level authorization (IDOR)

- **Boundary:** the resource handler, after authentication, before returning
  the object.
- **Do:** verify the authenticated principal owns / is scoped to *this* object
  (tenant + ownership + action), not just that the collection is theirs.
- **Negative test:** wrong-tenant / wrong-owner principal requests the object
  by id → expect 404/403 and no data. This is the row `multi-tenant-security-tester` also owns; coordinate.

## Session & cookie flags

- **Boundary:** session/cookie configuration.
- **Do:** `HttpOnly`, `Secure`, `SameSite` (Lax/Strict per flow), sane expiry,
  rotation on privilege change, server-side revocation.
- **Negative test:** assert the Set-Cookie header carries the flags; assert a
  revoked/expired session is rejected.

## Safe file handling

- **Boundary:** upload receipt and storage path construction.
- **Do:** validate content type/size, generate storage names (never trust the
  client filename), block path traversal, store outside web root or behind
  authz, scan if required.
- **Negative test:** upload `../../etc/passwd` name and an oversized/disallowed
  type → expect rejection; assert stored path cannot traverse.

## SSRF / open redirect

- **Boundary:** any server-side fetch or redirect using a user-supplied URL.
- **Do:** allowlist hosts/schemes; resolve and block internal/link-local ranges
  for SSRF; for redirects, allow only same-site/known targets.
- **Negative test:** supply `http://169.254.169.254/…` (SSRF) or
  `//evil.example` (redirect) → expect rejection.

## General rules

- One control per pass; note sibling instances of the same class for a
  follow-up rather than implying the class is closed.
- Reuse crypto/token/hash primitives from the platform — never hand-roll.
- Every pattern's negative test must FAIL before the control and PASS after;
  a test green on the first run did not reproduce the vulnerability.
