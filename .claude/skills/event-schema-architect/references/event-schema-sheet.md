# Event Schema Sheet

Detail for `event-schema-architect`. Read on demand.

## Which "event" skill owns this? (three-way)

| Kind of event | Consumer | Owner skill |
|---|---|---|
| Analytics / behavioral (for measurement) | Analysts, growth, experiments | **event-schema-architect** (this) |
| External API / webhook / partner feed | Integrators (a contract/promise) | api-event-architect |
| Internal stream / pipeline message | Internal services (transport) | streaming-event-architect |

Same word, different purpose, lifecycle, and guarantees. Designing one as
another is the classic expensive mistake.

## Naming convention

- **Object-Action**, past tense: `Order Completed`, `Signup Started`,
  `Invite Sent`.
- Consistent case (Title Case or snake_case — pick one, everywhere).
- Controlled vocabulary of objects (Order, Signup, Invite…) and actions
  (Started, Completed, Failed…). A new name is DERIVED, not invented.
- No synonyms: not `Purchase` and `Order Completed` and `checkout_done`
  for the same thing.

## Property schema template

```
Event: Order Completed
Properties:
  order_id        string   required
  amount          number   required   unit: cents
  currency        enum     required   [USD, EUR, GBP, ...]
  item_count      integer  required
  coupon_code     string   optional
  plan            enum     optional   [free, pro, enterprise]
PII flag: none (ids only)
```

Rules: type every property; required vs optional; enums for categoricals;
state units; no free-text where an enum belongs.

## Global / shared properties (every event)

- Identity: user_id / account_id / tenant_id (per identity model)
- Session: session_id
- Context: platform/device, app version, locale, referrer/context
- Time: event timestamp (and received timestamp if relevant)

Defined ONCE so every event joins and segments the same way.

## Identity stitching

- Anonymous events carry an anonymous_id before login.
- On identify, alias anonymous_id → user_id so pre-login events join the
  identified user (critical for top-of-funnel).
- Carry account_id/tenant_id for B2B multi-tenant analysis; guarantee
  tenant context is never missing.
- Keep keys stable; a churning user_id fragments the same person.

## Governance & versioning

- Tracking plan / registry = source of truth. New events go through it.
- Additive by default (new events/props don't break consumers).
- Deprecate events/props with a window; record owner.
- A property MEANING change is breaking → new property or new version,
  never a silent redefinition.

## PII minimization

- Capture ids and coarse enums, not raw name/email/address, unless a
  specific question requires it and consent covers it.
- Flag any sensitive property; hand retention/erasure to
  `pii-lifecycle-designer`.
- The schema is the cheapest place to prevent over-collection.
