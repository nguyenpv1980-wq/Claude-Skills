# Security Review Passes

Progressive-disclosure detail for `security-pr-reviewer`. Run these passes over
an obtained diff; anchor every finding to file:line and give HIGH+ an exploit
path.

## Pass 1 — Authentication & authorization

- Every new/changed endpoint requires authentication? Anonymous reach intended?
- **Object-level authorization:** the handler checks the caller owns / is
  scoped to *this* object, not just that it's a valid member. (anti-IDOR)
- **Tenant scope (SaaS, mandatory):** tenant id server-derived (session/JWT),
  never taken from a client field on a data path; applied to EVERY query the
  diff adds.
- Role/permission checks at the resource, consistent with the authorization
  matrix — not only hidden in the UI.
- Any parallel route to the same data (GraphQL/REST/RPC) that skips the check?

## Pass 2 — Injection & untrusted input

- Untrusted input into SQL/NoSQL/shell/template/`eval`/deserialization?
  Parameterized / contextually encoded / safe-parsed?
- Dynamic query parts (ORDER BY, column names, LIMIT) allowlisted, not
  interpolated.
- **Mass assignment:** can the client set restricted fields (role, tenant_id,
  owner_id, status, price) through the changed write path?
- File handling: content-type/size validation, generated storage names, no
  path traversal.

## Pass 3 — Secrets & config

- Secrets added to source, config, test fixtures, or log statements?
- Server-only secret exposed to the client bundle (prefix leak)?
- Tokens/PII logged? Errors echoing sensitive data?
- New user-supplied URL used server-side (SSRF) or in a redirect (open
  redirect) without allowlisting?

## Pass 4 — Security-relevant change detection

- Does the diff LOOSEN an existing control: broadened CORS, relaxed policy,
  removed check, widened permissions/token scope, disabled validation?
- Report control weakening as its own finding even if the feature still works.

## Exploit-path template (required for HIGH/CRITICAL)

```
<persona: anonymous | wrong-tenant authenticated | lower-role | insider>
does <concrete steps against file:line> and gains <asset + blast radius>.
```
Missing persona/steps/payoff → cap the finding at MEDIUM and mark
"needs-verification: <what would confirm it>".

## Test adequacy

- Is the security behavior pinned by a test that would FAIL if the control were
  reverted? If not, that's a gap to name.
- A security fix in the diff without a negative test is unverified — call it.

## Handoffs

- DB migration / RLS policy portion → `secure-migration-reviewer` /
  `rls-policy-auditor`.
- Dependency/CI issue → `supply-chain-security-reviewer`.
- SAST/CodeQL output to triage → `static-analysis-reviewer`.
- Fixing findings → `appsec-implementer` (separate, approved change).
