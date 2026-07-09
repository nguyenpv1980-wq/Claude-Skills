---
name: api-event-architect
description: Design external API and event contracts for a multi-tenant SaaS — tenant context derived from credentials (never client-supplied tenant ids on data paths), resource/route conventions, versioning and deprecation policy with sunset windows, idempotency for mutations, per-tenant and per-plan rate limits, and webhook/event-feed contracts (versioned envelope schemas, tenant-scoped subscriptions, at-least-once delivery with retries, signing and replay protection). Produces API contract conventions, an event taxonomy with schemas, a webhook delivery policy, and a contract migration/rollback plan. Use when designing or overhauling a public API, adding webhooks or an event feed for integrations, when partners keep breaking on contract changes, or when API rate limiting needs a tenant/plan dimension. Do NOT use for the internal audit trail (audit-log-architect), internal service-to-service architecture (architecture-designer), or role/permission design (authorization-matrix-designer).
---

# API & Event Architect

## Purpose

Produce the external contracts of a multi-tenant SaaS — the API surface and
the event/webhook feed — designed so that tenant context is structural,
change is survivable, and delivery is honest about its semantics.
Deliverables: API conventions (auth-derived tenant context, idempotency,
errors, rate limits), a versioning/deprecation policy, an event taxonomy
with versioned schemas, a webhook delivery policy (retries, ordering,
signing, replay), and a migration/rollback plan for contract changes. A
public contract is a promise with a support burden; this skill makes the
promise explicit before integrations harden around accidents.

## Use When

- Use when: designing a public/partner API for a multi-tenant product, or
  imposing conventions on one that grew endpoint by endpoint.
- Use when: adding webhooks or an event feed that integrations subscribe to.
- Use when: partners break on releases — versioning and deprecation policy
  is missing or unenforced.
- Use when: rate limiting needs a tenant/plan dimension (limits as
  entitlements, noisy-neighbor protection).
- Use when: planning a breaking contract change and its migration window.
- Do NOT use when: designing the internal audit record — that is
  `audit-log-architect`; one action may feed both, but audit is a record
  with integrity guarantees, a webhook is a best-effort notification
  contract.
- Do NOT use when: structuring internal services and their dependencies —
  `architecture-designer`.
- Do NOT use when: deciding which roles/scopes may call what — the matrix
  comes from `authorization-matrix-designer`; this skill binds it into
  token scopes.
- Do NOT use when: the concern is internal rather than the external
  contract — the streaming backbone between services
  (`streaming-event-architect`), live push to client connections
  (`realtime-subscription-architect`), or the internal mediated write path
  (`command-gateway-architect`); nor for analytics measurement events
  (`event-schema-architect`), notification/webhook UX
  (`notification-webhook-ux-designer`), or the generated reference docs for
  this contract (`api-doc-generator-designer`).

## Inputs to Inspect

1. The current API surface: routes, auth mechanism, where tenant context
   enters today, existing consumers and their observed usage (the de facto
   contract).
2. The tenant model (tenant boundary, membership — for whom tokens act) and
   the authorization matrix (permissions → token scopes).
3. The entitlement matrix: which limits are plan-derived (rate limits,
   feature access on API paths).
4. Existing integration pain: partner bug reports, breakage history from
   past releases, support tickets about webhooks.
5. Domain events already modeled (domain-modeler output) — the event feed
   exposes a curated subset, not the internal event bus.
6. Compliance/data-sensitivity constraints on what payloads may leave the
   platform (webhooks are data egress).

## Workflow

1. **Pin the tenant-context contract.** Tenant identity derives from the
   credential (token claims / key binding), resolved server-side. No data
   endpoint accepts a tenant id from the client; multi-tenant-capable
   credentials (partner/aggregator tokens) name the tenant explicitly per
   call against an allow-list bound to the credential — the exception is
   designed, not defaulted.
2. **Set resource conventions**: naming, ids (opaque, non-enumerable where
   resources are tenant-owned), pagination, filtering, error shape
   (machine-readable codes; error detail must not leak other tenants'
   existence), and the 404-vs-403 policy consistent with the isolation
   posture.
3. **Define idempotency**: mutation endpoints accept idempotency keys;
   retried requests return the original result within a stated window.
   Webhook handlers on the consumer side are told to expect duplicates
   (documented, not implied).
4. **Design rate limits with a tenant/plan dimension**: per-credential and
   per-tenant limits, plan-derived tiers resolved from the entitlement
   matrix, standard limit-headers, and 429 behavior. Per-tenant limits are
   noisy-neighbor protection — they exist even for "unlimited" plans.
5. **Write the versioning and deprecation policy**: what counts as breaking
   (field removal/retyping, semantics changes — additive is non-breaking by
   contract), how versions are expressed, support window per version, and
   the deprecation sequence: announce → dual-run → sunset header/warnings →
   enforce, with minimum notice stated.
6. **Build the event taxonomy and schemas** using
   [references/api-event-contract-conventions.md](references/api-event-contract-conventions.md):
   versioned envelope (event id, type, occurred-at, tenant id,
   schema version, payload), curated event types with clear semantics
   (created/updated/deleted + domain milestones), payload minimization
   (ids + changed fields; consumers fetch detail via API — thin events
   unless a stated reason).
7. **Define the webhook delivery policy**: subscriptions are tenant-scoped
   (a subscription belongs to a tenant and receives ONLY that tenant's
   events; partner/aggregator subscriptions enumerate tenants explicitly);
   at-least-once delivery with documented retry schedule and backoff;
   ordering non-guaranteed (or per-key if actually guaranteed — no false
   promises); signing with rotatable secrets, timestamped signatures for
   replay protection; failure handling (dead-letter after N, disable-and
   -notify policy); a redelivery mechanism.
8. **Plan contract migration and rollback**: for any breaking change —
   dual-run window with both versions live, consumer migration telemetry
   (who is still on the old contract), staged enforcement, and rollback =
   re-extend the old version's sunset (which is why it is not deleted at
   the deadline but after a quiet period). Event schema changes follow the
   same policy via envelope versioning.

## Output Format

```
API & EVENT CONTRACT DESIGN — <product/scope>
Tenant-context contract: <credential → tenant resolution; client-supplied
  tenant ids forbidden on data paths; aggregator exception design if needed>
API conventions: <resources, ids, pagination, error shape, 404-vs-403 policy,
  idempotency mechanism + window>
Rate limits: <per-credential / per-tenant / plan-derived tiers; headers; 429
  behavior>
Versioning & deprecation policy: <breaking definition; version expression;
  support window; announce → dual-run → sunset sequence with minimum notice>
Event taxonomy: <event type — semantics — payload (thin/full + why)>
Envelope schema: <fields, versioned>
Webhook delivery policy: <subscription scoping; delivery semantics; retry
  schedule; signing + replay protection; failure/dead-letter; redelivery>
Migration & rollback plan: <dual-run, telemetry, staged enforcement,
  sunset-extension rollback>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] No data endpoint trusts a client-supplied tenant id; the aggregator
      exception (if any) is allow-list-bound and explicit.
- [ ] Error responses and 404-vs-403 policy leak no other tenant's
      existence; ids are non-enumerable for tenant-owned resources.
- [ ] Every mutation has idempotency semantics with a stated window.
- [ ] Rate limits exist per tenant (noisy-neighbor floor) and map to the
      entitlement matrix where plan-derived.
- [ ] "Breaking" is defined; deprecation has a minimum-notice number and a
      dual-run window, not just an announcement.
- [ ] Webhook subscriptions are tenant-scoped; delivery semantics
      (at-least-once, retry schedule, ordering honesty) are documented.
- [ ] Webhooks are signed with rotatable secrets and timestamped against
      replay; payloads pass the data-egress/minimization check.
- [ ] Rollback for contract changes is sunset-extension — old versions are
      removed after a quiet period, never at the moment of deadline.
- [ ] Audit events were not conflated into the integration feed.

## Tenant Isolation Rules

- Tenant context comes from the credential, resolved server-side; a
  subscription or token belongs to a tenant and reaches only that tenant's
  data and events.
- Partner/aggregator access across tenants is an enumerated allow-list on
  the credential, granted by each tenant, revocable per tenant — never a
  wildcard.
- Webhook payloads and error bodies are data egress: minimized, scoped to
  the subscribing tenant, and never carrying another tenant's identifiers.
- Per-tenant rate limits are an isolation control (one tenant cannot starve
  the API for others), not just a billing feature.

## Security Rules

- Webhooks are signed (HMAC or asymmetric) with per-subscription rotatable
  secrets; signatures cover a timestamp; consumers are given a verification
  recipe including replay rejection.
- Webhook target URLs are validated against SSRF (no internal address
  ranges); redirects are not followed on delivery.
- Token scopes bind to the authorization matrix; a leaked events-read scope
  must not permit data mutations.
- Negative tests accompany the design: cross-tenant subscription attempts
  rejected, unsigned/stale-signature deliveries rejected by the reference
  consumer, client-supplied tenant id on a data path rejected.

## Gotchas

- Whatever your API returns becomes the contract — partners depend on field
  order, undocumented fields, and error typos; conventions must exist
  BEFORE the first partner, or the accidents are the spec.
- Fat webhook payloads become a second, unversioned API; thin events
  (ids + change summary, fetch via API) keep authorization checks at the
  API where they already exist.
- At-least-once + no consumer idempotency guidance = every partner has a
  duplicates bug; the docs' consumer checklist is part of the contract.
- Retry storms after a consumer outage can hammer recovered endpoints;
  backoff with jitter and a dead-letter threshold are delivery-policy
  decisions, not implementation details.
- Sequential integer ids on tenant-owned resources are an enumeration
  vulnerability AND a business-intelligence leak (order counts).
- "We'll never break the API" is not a versioning policy; it is the absence
  of one, discovered at the first unavoidable breaking change.

## Stop Conditions

- The tenant model or authorization matrix is undefined → those run first;
  token scopes and subscription scoping have nothing to bind to.
- A planned change breaks live consumers and no deprecation policy exists
  yet → the policy comes first, and the change routes through
  `human-approval-boundary` with the affected-consumer count.
- Webhook payload contents raise data-egress/compliance questions
  (regulated data leaving the platform) → surface before designing the
  payload.
- Asked to implement endpoints/dispatchers in the same pass → separate,
  scoped task (`docs-first-implementer` for framework specifics); this
  skill delivers contracts.

## Supporting Files

- [references/api-event-contract-conventions.md](references/api-event-contract-conventions.md) —
  envelope schema, event-type naming, delivery-policy table, consumer
  checklist, and deprecation-sequence template.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `audit-log-architect`
  and `authorization-matrix-designer` (access & events cluster).
