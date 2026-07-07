# Threat Catalog — STRIDE prompts, SaaS rows, abuse-case patterns

Progressive-disclosure detail for `threat-modeler`. Use these prompts to
enumerate threats per boundary. Every prompt is a question; the answer becomes
a threat row (or an explicit "not applicable, because…").

## STRIDE prompts per boundary type

### Client → server (any request boundary)
- **Spoofing:** Can a caller present as another user/tenant/service? Is the
  identity server-verified, not client-asserted? Are tokens validated (sig,
  expiry, audience, revocation)?
- **Tampering:** Can request fields the client shouldn't own (role, tenant_id,
  owner_id, price, status) be submitted and honored? (mass assignment)
- **Repudiation:** Is a security-relevant action audited with actor + tenant +
  outcome so it can't be denied later? (hand to `audit-log-architect`)
- **Information disclosure:** Do error messages/404-vs-403/timing reveal record
  or user or tenant existence? Are object-level reads authorized?
- **Denial of service:** Is the endpoint rate-limited per actor/tenant? Any
  unbounded input (page size, upload size, regex, zip/expansion)?
- **Elevation of privilege:** Can a normal user reach an admin action, escalate
  role, or act cross-tenant? Is authz checked at the resource, not just the UI?

### Server → data store
- Every query on this path carries tenant scope? Server-derived, never
  client-supplied? RLS or equivalent enforced (hand to `rls-policy-auditor`)?
- Service-role / superuser credentials confined to server runtime, never
  exposed to a path a tenant can influence?

### Tenant → tenant (the boundary most models forget)
- By-id lookups scoped to the caller's tenant (IDOR)? Search indexes, caches,
  vector stores, exports partitioned or filtered by tenant?
- Background jobs / webhooks running with platform-wide credentials that touch
  multiple tenants' data?

### App → third party / integration
- Outbound secrets scoped and rotated? Inbound webhooks signature-verified,
  replay-protected, tenant-mapped? SSRF via user-supplied URLs?

### CI / build → production (supply chain)
- Can a dependency, action, or build step inject code or exfiltrate secrets?
  (hand to `supply-chain-security-reviewer`) Are prod credentials reachable
  from PR-triggered CI?

## SaaS mandatory rows (master-prompt §6)

For every data-access boundary, always enumerate:
1. **Tenant isolation** — cross-tenant read/write reachable here?
2. **Object-level authorization** — is *this* object owned by / visible to the
   caller, or only the *collection* checked?

These are never "n/a" on a tenant-facing data path; if truly not applicable,
state why in one line.

## Attacker personas (use all that apply)

| Persona | Capability | Why it matters |
|---|---|---|
| Anonymous | No credentials | Public endpoints, signup, password reset, webhooks |
| Authenticated, wrong tenant | Valid login, different org | The most common real SaaS attacker; drives IDOR/isolation rows |
| Authenticated, lower role | Valid login, insufficient role | Privilege escalation, admin-action reach |
| Malicious insider | Support/admin console access | Brokered access, audit, blast radius |
| Compromised dependency | Runs in build/runtime | Supply-chain, secret exfiltration |

## Abuse-case pattern

```
<persona> does <concrete steps> and gains <payoff>.
```
Good: "An authenticated user in tenant A calls `GET /api/invoices/:id` with an
id enumerated from tenant B and receives tenant B's invoice, because the
handler filters by id only."
Bad: "Attacker exploits IDOR." (no persona, no steps, no payoff → not testable)

## Exploit-path requirement for HIGH severity

A HIGH-ranked threat states: **who** (persona), **from where** (surface/entry),
**doing what** (steps), **getting what** (asset + blast radius). Missing any
element → cap at MEDIUM and record "confirmed by: <experiment/test>".

## Mitigation → test mapping

Every mitigation row produces at least one negative test: execute the abuse
case, expect denial/failure. Implementable tenant/authz tests → hand to
`multi-tenant-security-tester`; control build → `appsec-implementer`.
