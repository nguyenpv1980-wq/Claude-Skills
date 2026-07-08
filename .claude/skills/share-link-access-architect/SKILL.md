---
name: share-link-access-architect
description: Design guest/public share-link access for a multi-tenant SaaS — a CAPABILITY model where possession of an opaque, high-entropy, expiring, revocable token grants a fixed narrow scope, distinct from member RBAC: token design, ephemeral guest sessions (not memberships), optional password/OTP gating, per-link scope (which resource, which permission), enumeration/abuse defense, and audit. The link must expose exactly the shared resource and never become a hole into the rest of the tenant. Use when adding anyone-with-the-link view/comment/edit access for non-members (often unauthenticated), or designing the share token's entropy, expiry, revocation, and gating. Do NOT use for MEMBER roles×permissions or impersonation/support access (authorization-matrix-designer), or for API credentials / webhook signing / partner keys (api-event-architect). Produces a design/spec; do not invent crypto primitives — use vetted ones.
---

# Share-Link Access Architect

## Purpose

Design **guest/public share-link access** — the "anyone with the link can
view / comment / edit" surface — as a capability model: possession of an
opaque, unguessable, expiring, revocable token grants a single fixed, narrow
scope, with no tenant membership and no role. The deliverable is the token
design (entropy, expiry, revocation), the ephemeral guest-session model, an
optional password/OTP gate, the per-link scope binding, an enumeration/abuse
defense, and the audit contract. The two load-bearing properties: the token is
a bearer capability (unguessable and least-privileged, because whoever holds
it is the actor), and the link exposes exactly the shared resource — never a
path into the rest of the tenant. This is a design/spec deliverable; it uses
vetted cryptographic primitives, it does not invent them.

## Use When

- Use when: adding share-link access to a resource for people who are NOT
  members of the tenant (often fully unauthenticated) — view, comment, or edit
  by anyone holding the link.
- Use when: designing the share TOKEN itself — entropy/unguessability, expiry,
  revocation, and an optional password/OTP gate.
- Use when: designing the guest SESSION a valid link mints — ephemeral,
  link-scoped, not a membership.
- Use when: an existing share feature uses guessable ids, has no expiry, or
  can't be revoked, and needs a real design.
- Do NOT use when: the subject is MEMBER roles × permissions × resources, or
  impersonation/support access — that is `authorization-matrix-designer`;
  member RBAC (identity → role → permission) is a different model from a
  bearer link, and a member "shared-with" grant is RBAC, not a public link.
- Do NOT use when: the credential is a MACHINE one — API keys, webhook
  signing, partner secrets — that is `api-event-architect`.
- Do NOT use when: the "guest" is really a member with a lightweight role —
  route to `authorization-matrix-designer`; a guest here holds a link, not an
  account.

## Inputs to Inspect

1. Which resources can be shared and at what permission (view / comment /
   edit) — the scope space each link draws from.
2. Whether guests may be fully unauthenticated, or a lightweight identity
   (name/email) is captured — this changes the session and audit design.
3. Existing token/session infrastructure: how tokens are minted, stored,
   verified, and revoked today (guessable ids and no-expiry are findings).
4. What the shared resource is connected to — related records, the owning
   tenant, sibling resources — so the link's blast radius is bounded to the
   one resource, not its neighbourhood.
5. Compliance/PII posture of shareable resources: whether exposing them to
   unauthenticated holders needs a human/compliance decision.
6. Abuse/rate-limit infrastructure available (per-IP, per-token throttling,
   bot defense) for the enumeration/brute-force defenses.

## Workflow

1. **Design the token.** Opaque and high-entropy (unguessable — never a
   sequential or derivable id), carrying no authority of its own (a lookup key
   whose scope lives server-side; if it must carry claims, it is signed and
   scoped). Default-on expiry with a maximum lifetime, and revocation that is
   immediate and checked server-side on every use.
2. **Bind per-link scope.** Each token maps to exactly ONE resource (or an
   explicit small set) and ONE permission level — least privilege. The scope is
   stored server-side keyed by the token, never inferred from the token or read
   from a client parameter. A view link cannot be escalated to edit by changing
   a request.
3. **Design the guest session.** A valid token mints an ephemeral, link-scoped
   session — NOT a tenant membership and NOT a role. It can touch only the
   link's resource at the link's permission and expires with the link. It never
   inherits the sharer's other access.
4. **Add optional gating.** For sensitive shares, a password or OTP on top of
   the link (the link is something-you-have; the password something-you-know).
   Rate-limit the gate and lock out on brute force.
5. **Defend against enumeration and abuse.** Token entropy makes enumeration
   infeasible; rate-limit link access per token and per IP; return ONE uniform
   response for invalid / expired / revoked / never-existed tokens (no oracle
   distinguishing "expired" from "never existed"); watch for scraping; cap link
   creation per user/tenant.
6. **Bound the tenant blast radius.** The guest session's scope IS the leak
   boundary: the link exposes exactly the shared resource and nothing else — no
   navigation to sibling records, no tenant-wide reads. A link that widens
   beyond its resource is the bug this skill exists to prevent.
7. **Specify the audit contract.** Record link creation (who, resource, scope,
   expiry), each access (token, time, IP within privacy limits), gate
   attempts, and revocation — emitted into `audit-log-architect`'s schema.

## Output Format

```
SHARE-LINK ACCESS DESIGN — <product/resource>
Token: <opaque, high-entropy source; carries-no-authority | signed+scoped;
  expiry default + max lifetime; revocation immediate, checked every use>
Per-link scope: <token → one resource(set) + one permission; stored
  server-side; no client-supplied scope; no view→edit escalation>
Guest session: <ephemeral, link-scoped; NOT a membership/role; expires with link>
Optional gating: <password/OTP; rate-limited; lockout on brute force>
Enumeration/abuse defense: <entropy, per-token+IP rate limit, uniform
  invalid/expired/revoked response, creation cap>
Tenant blast radius: <link exposes exactly the resource; no sibling/tenant reach>
Audit: <creation / access / gate attempts / revocation → audit-log schema>
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Tokens are opaque and high-entropy — enumeration is infeasible, not
      merely inconvenient; no sequential/derivable ids.
- [ ] Every link has an expiry and can be revoked, and revocation is checked
      server-side on every use (not just a hidden UI button).
- [ ] Scope is bound per link to one resource + one permission, stored
      server-side; a view link cannot be escalated to edit.
- [ ] The guest session is ephemeral and link-scoped — it is not a membership,
      inherits no other access, and expires with the link.
- [ ] Invalid / expired / revoked / never-existed tokens return one uniform
      response — no existence oracle.
- [ ] The link cannot reach sibling resources or tenant-wide data; the scope is
      the enforced leak boundary.
- [ ] Optional password/OTP gates are rate-limited with brute-force lockout.
- [ ] Creation, access, gate attempts, and revocation are audited via
      `audit-log-architect`.

## Security Rules

- The token is a bearer credential: whoever holds it is the actor, so it must
  be unguessable, least-privileged, expiring, and revocable — the four
  properties are non-negotiable, not options.
- Scope lives server-side keyed by the token; nothing about what a link can do
  is read from the client or inferred from the token value.
- No existence oracle: the response for a token that never existed and one that
  expired or was revoked is identical.
- The guest session never inherits the sharer's memberships, roles, or reach —
  it is exactly the link's one scope and nothing more.
- Use vetted cryptographic/token primitives (a CSPRNG, established token
  formats); this skill does not design new crypto.

## Gotchas

- Guessable or sequential link ids turn "anyone with the link" into "anyone
  with a for-loop" — enumeration is the classic share-link breach.
- No expiry means links live forever: one leaked link in an email thread or a
  cached URL is permanent access until someone remembers it exists.
- Revocation that only hides the UI button while the token still resolves is
  not revocation — the check must be server-side on every use.
- A view link that flips to edit by changing a client-side permission param is
  a scope-escalation bug; the permission is bound to the token server-side.
- The link becomes a hole into the whole tenant when the guest session can
  navigate from the shared resource to its neighbours — bound the blast radius.
- A password gate with no rate limit is a brute-force target; distinct error
  messages for wrong-password vs no-such-link leak existence.
- Guest access that isn't audited leaves no trail when a link is abused — the
  one actor you can't authenticate is the one you most need to log.

## Stop Conditions

- The "share link" actually needs full member identity, roles, or standing
  access → route to `authorization-matrix-designer`; this is a bearer link, not
  an account.
- The shared resource carries regulated/PII data whose exposure to
  unauthenticated holders needs a human or compliance decision → stop and
  escalate (`human-approval-boundary`, `pii-lifecycle-designer`); do not design
  public exposure of regulated data unilaterally.
- The request is to invent token cryptography or a bespoke signing scheme →
  stop; specify vetted primitives and defer novel crypto to security review.
- Revocation, expiry, or scope cannot actually be enforced server-side in the
  current architecture → surface that gap; a link you cannot revoke or bound is
  not shippable, and saying so is the deliverable.

## Supporting Files

- `evals/evals.json` — behavior cases: the opaque-token share design, the
  guessable-id/no-expiry fix, the view→edit escalation edge, and the
  regulated-data escalation refusal.
- `evals/trigger-evals.json` — discrimination against `authorization-matrix-designer`
  (member RBAC + impersonation) and `api-event-architect` (machine credentials /
  webhook signing).
- No `references/` — the token, scope, and abuse-defense guidance above is the
  complete procedure; detail lives in the produced artifacts.
