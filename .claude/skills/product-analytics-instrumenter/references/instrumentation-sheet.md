# Instrumentation Sheet

Detail for `product-analytics-instrumenter`. Read on demand.

## Which "instrumentation" skill? (three-way)

| Job | Consumer | Owner skill |
|---|---|---|
| Product analytics (user behavior) | Product, growth, experiments | **product-analytics-instrumenter** (this) |
| System telemetry (logs/metrics/traces) | Engineers, on-call | observability-operator |
| Skill-library usage (which skills fire) | Library maintainers | skill-usage-instrumenter |

Different consumers, privacy stances, and lifecycles. Don't blur them.

## Client vs server capture

| Capture | Use for | Risks |
|---|---|---|
| Server-side | Purchases, upgrades, state changes, anything billed/authoritative | Misses pure client interactions |
| Client-side | Clicks, views, hovers, scroll — UI-only signals | Ad blockers, crashes, tab close, lost on nav |
| Both (reconciled) | High-value events needing UI + authoritative view | Must de-dup / reconcile deliberately |

Rule of thumb: **if the number has to be right, capture it server-side.**

## Consent gating checklist

- [ ] No capture before consent where consent is required.
- [ ] Honor opt-out and Do-Not-Track.
- [ ] Drop/redact schema-flagged sensitive properties AT the source.
- [ ] Handle IP/geo per regional rules (truncate/avoid where required).
- [ ] Consent state itself recorded; capture path respects it at runtime.

Downstream scrubbing is unreliable and too late; minimize at capture.

## De-duplication patterns

- Fire-once guard per logical occurrence (component mount, not every
  re-render).
- Idempotency key on the event so client retries collapse.
- One authoritative source per event — never count the same purchase from
  both client and server.
- Reconcile the "both" case explicitly (e.g., server is source of truth,
  client view is diagnostic).

## Reliability techniques

- Batch events; flush on `visibilitychange`/`pagehide` (beacon path) so
  last-moment events aren't lost on navigation.
- Retry transient send failures; queue while offline.
- If sampling, state its effect on metrics; never silently sample events a
  funnel or experiment depends on.

## Tracking-QA workflow

1. Debug/verification mode: surface fired events + properties live.
2. Assert against the tracking plan: each expected event fires, with the
   right name, at the right moment, with typed/required properties.
3. Staging validation before release.
4. Regression guard: a refactor/schema change that breaks tracking fails
   loudly (test), not silently months later.

The schema being asserted against is `event-schema-architect`'s tracking
plan.
