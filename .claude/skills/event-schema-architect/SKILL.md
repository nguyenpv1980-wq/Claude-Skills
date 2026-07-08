---
name: event-schema-architect
description: Design the ANALYTICS event schema and tracking plan for product measurement — the event naming taxonomy (consistent object-action), a typed property schema per event (required/optional, enums), shared global properties (user/session/tenant/timestamp), the identity model (anonymous→identified stitching; user/account/tenant keys), a tracking plan/registry as the source of truth, additive versioning, cross-platform naming consistency, and PII minimization. These are BEHAVIORAL events for MEASUREMENT (funnels, metrics, experiments) — NOT the external API/webhook CONTRACT (api-event-architect) and NOT the internal streaming pipeline's transport events (streaming-event-architect). Use when defining a tracking plan, analytics event names/properties, or an event taxonomy for product analytics. Do NOT use for the external event/webhook contract (api-event-architect), the internal data-pipeline stream design (streaming-event-architect), or WHERE/HOW events fire in code (product-analytics-instrumenter).
---

# Event Schema Architect

## Purpose

Analytics dies of inconsistency. One team fires `Signup Completed`,
another `user_signed_up`, a third `completed-registration`; properties
are `plan` here and `subscription_tier` there; anonymous events never
stitch to the identified user, so half the funnel is invisible. Six
months in, every number needs a footnote and nobody trusts the
dashboard. This skill designs the ANALYTICS event schema — the naming
taxonomy, the typed property schema, the shared global properties, the
identity model that joins anonymous to known, and the tracking plan that
serves as the single source of truth — with versioning, governance, and
PII minimization built in. These are behavioral events captured for
MEASUREMENT. They are not the external API/webhook contract offered to
integrators (`api-event-architect`), and not the internal streaming
pipeline's transport events (`streaming-event-architect`) — three
different kinds of "event" that share a word and nothing else.

## Use When

- Use when: defining a tracking plan or analytics event taxonomy, or
  standardizing inconsistent event names/properties across the product.
- Use when: designing the property schema for events, the shared global
  properties, or the enum values a property may take.
- Use when: designing the analytics identity model — anonymous-to-
  identified stitching, and the user/account/tenant keys events carry.
- Use when: analytics is untrustworthy because event definitions drift,
  duplicate, or lack a registry/source of truth.
- Do NOT use when: the events are an EXTERNAL contract — public webhooks,
  partner event feeds, signed versioned envelopes, tenant-scoped
  subscriptions — that is `api-event-architect` (a promise to
  integrators, not a measurement schema).
- Do NOT use when: the task is the INTERNAL data pipeline — topics,
  partitions, delivery semantics, DLQ, retention — that is
  `streaming-event-architect` (transport, not analytics meaning).
- Do NOT use when: the task is WHERE/HOW to fire the events in code
  (client vs server, instrumentation points, consent gating, tracking
  QA) — that is `product-analytics-instrumenter`; this skill defines the
  schema it instruments against.

## Inputs to Inspect

1. The questions the business needs to answer: the funnels, metrics, and
   experiments analytics must support — the schema exists to serve these,
   not to log everything.
2. Existing tracking: current event names, properties, and their
   inconsistencies/duplicates; any tracking plan or schema registry
   already in place (a live contract for downstream consumers).
3. The identity reality: how users appear anonymous first (pre-login) and
   become identified, and the account/tenant structure each event should
   carry.
4. The platforms emitting events: web, mobile, backend, and how naming
   currently diverges across them.
5. Privacy constraints: consent regime, what counts as PII, and
   regional/retention obligations (from `pii-lifecycle-designer` outputs
   where present) that bound what analytics may capture.

## Workflow

1. **Start from the questions, not the events.** List the funnels,
   metrics, and experiments to be supported and derive the events needed.
   Logging everything "just in case" produces an unusable schema and a
   privacy liability.
2. **Define the naming taxonomy.** One convention, applied everywhere:
   object-action (`Order Completed`), consistent case and tense, a
   controlled vocabulary of objects and actions. Document it so a new
   event's name is derivable, not invented.
3. **Design the property schema per event.** Typed properties, required
   vs optional, enumerated value sets for categoricals, and units stated.
   No free-text where an enum belongs; no `plan` meaning three things.
4. **Standardize global/shared properties.** The set every event carries
   — user/account/tenant id, session, device/platform, timestamp, app
   version, and context — defined once so joins and segmentation work
   across all events.
5. **Design the identity model.** How anonymous events (pre-identify)
   stitch to the identified user once known; the keys used
   (user/account/tenant) and their stability; and how tenant context is
   guaranteed present for multi-tenant analytics. Broken identity is the
   most common reason funnels undercount.
6. **Establish the tracking plan as source of truth.** A registry that
   defines every event and property with its type, requiredness, and
   description — the artifact `product-analytics-instrumenter` implements
   against and QA validates. New events go through it, not straight into
   code.
7. **Set versioning and governance.** Additive-by-default (new events/
   properties don't break consumers); a deprecation path for events/
   properties with a window; an owner for the plan. Changing a property's
   meaning is a breaking change — treat it as one.
8. **Minimize PII at the schema level.** Decide what personal data (if
   any) an analytics event may carry; prefer ids and coarse enums over
   raw personal fields; mark sensitive properties and defer their
   handling to `pii-lifecycle-designer`. The schema is where
   over-collection is prevented, cheaply.
9. **Name boundaries and deliver.** External contract →
   `api-event-architect`; internal pipeline → `streaming-event-architect`;
   instrumentation/firing → `product-analytics-instrumenter`. Produce the
   tracking plan in the Output Format.

The naming convention reference, the property-schema template, the
identity-stitching patterns, and the three-way "which event skill" guide:
[references/event-schema-sheet.md](references/event-schema-sheet.md).

## Output Format

```
ANALYTICS TRACKING PLAN — <product/domain>
Supports:      <funnels/metrics/experiments this schema serves>
Naming:        <convention: object-action, case, tense, controlled vocab>
Global props:  <user/account/tenant, session, device/platform, timestamp, app version, context>
Events (per event):
  <Event Name>: purpose; properties [name:type req/opt enum? unit]; PII flag
Identity:      anonymous → identified stitching; keys (user/account/tenant) + stability
Registry:      tracking plan is the source of truth; new events go through it
Versioning:    additive default; deprecation window; owner
PII:           minimized set; sensitive props flagged → pii-lifecycle-designer
Boundaries:    external contract → api-event-architect; pipeline → streaming-event-architect;
               firing/instrumentation → product-analytics-instrumenter
```

## Validation Checklist

- [ ] Events are derived from the questions/metrics they must answer, not
      logged indiscriminately.
- [ ] One naming convention is defined and applied; a new event's name is
      derivable from it.
- [ ] Every event has a typed property schema with required/optional and
      enums for categoricals.
- [ ] Global/shared properties are standardized so cross-event joins and
      segmentation work.
- [ ] The identity model stitches anonymous to identified and guarantees
      tenant context.
- [ ] A tracking plan/registry is the single source of truth; changes go
      through it.
- [ ] Versioning is additive-by-default with a deprecation path; a
      meaning change is treated as breaking.
- [ ] PII is minimized at the schema; sensitive properties are flagged to
      `pii-lifecycle-designer`.
- [ ] External-contract, pipeline, and instrumentation concerns are
      handed to their owning skills.

## Gotchas

- Three unrelated things are called "events": the analytics behavioral
  event (this skill), the external webhook/API event
  (`api-event-architect`), and the internal stream message
  (`streaming-event-architect`). They have different consumers,
  guarantees, and lifecycles — designing one as another creates a mess
  that's expensive to unwind.
- Inconsistent naming is not cosmetic — it silently splits one metric
  across three event names, and the dashboard undercounts without error.
  The convention IS the data quality.
- Broken identity stitching makes funnels lie: anonymous top-of-funnel
  events never join to the identified conversion, so conversion looks
  worse than reality. Design identify/alias before trusting a funnel.
- "Log everything" is a privacy liability and an analysis swamp. A schema
  serving specific questions is smaller, cleaner, and defensible.
- Redefining what a property MEANS while keeping its name is the worst
  kind of breaking change: every historical number silently shifts and
  no consumer errors. Meaning changes are new properties or new versions.
- A tracking plan that lives in someone's head or a stale spreadsheet
  isn't a source of truth. Without a registry that instrumentation and QA
  check against, drift is guaranteed.
- Free-text where an enum belongs (`plan: "pro "` vs `"Pro"` vs
  `"professional"`) fragments every segmentation. Constrain categoricals
  at the schema.

## Stop Conditions

- The events are an external contract for integrators (webhooks, partner
  feeds, signed envelopes, subscriptions) → route to
  `api-event-architect`.
- The task is the internal streaming pipeline (topics, partitions,
  delivery semantics, DLQ, CDC) → route to `streaming-event-architect`.
- The task is instrumentation — where/how events fire, client vs server,
  consent gating, tracking QA → route to `product-analytics-instrumenter`;
  this skill defines the schema, not the firing.
- Required analytics would capture sensitive personal data with unclear
  consent/retention → stop and get the PII handling from
  `pii-lifecycle-designer` and consent from a human before baking it into
  the schema.

## Supporting Files

- [references/event-schema-sheet.md](references/event-schema-sheet.md) —
  the naming-convention reference, property-schema template, identity-
  stitching patterns, and the three-way "which event skill owns this"
  guide.
- `evals/evals.json` — behavior cases including the naming-standardization
  fix, the identity-stitching design, and the log-everything/PII refusal.
- `evals/trigger-evals.json` — the THREE-way discrimination against
  `api-event-architect` and `streaming-event-architect`, plus
  `product-analytics-instrumenter` (schema vs firing).
