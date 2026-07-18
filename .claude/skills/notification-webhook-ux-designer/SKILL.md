---
name: notification-webhook-ux-designer
description: 'Design the human-facing UX around outbound notifications and webhooks. For END USERS — the notification model across channels (in-app, email, push), per-category preferences, digest-vs-realtime batching for noise control, read/unread state, quiet hours, and opt-out that truly stops the messages (security/transactional still send). For DEVELOPER integrators of your webhooks — the management surface: register/edit endpoints, pick event types, a delivery log with payloads + status, test-send, replay a failed delivery, rotate the signing secret, and failing-endpoint alerts. Owns how a PERSON experiences and controls these; the wire delivery CONTRACT (envelope, signing, retry/at-least-once, versioning, subscriptions) stays with api-event-architect. Use when designing a notification center/preferences, notification noise control, or a webhook management surface. Do NOT use for the webhook delivery contract itself (api-event-architect) or generic empty/loading/error states (edge-state-ux-designer).'
---

# Notification & Webhook UX Designer

## Purpose

Two outbound channels, one recurring failure: the product either says
too much or gives no control over it. Users get seven emails for one
thread and no way to turn them off, or a critical alert lands in a
digest a day late; integrators get a webhook that fires but no way to
see whether it was delivered, no test button, no replay when their
server was down, and a secret they can't rotate without downtime. This
skill designs the HUMAN experience of both surfaces — for end users, a
notification model with real preferences, noise control, read-state, and
opt-out that works; for developer integrators, a webhook management
surface with a delivery log, test-send, replay, and secret rotation. It
owns how a person experiences, controls, and observes these events. The
wire contract underneath — envelope schema, signing, retry semantics,
versioning, subscription scoping — is `api-event-architect`'s, and this
skill designs the UX on top of it.

## Use When

- Use when: designing a notification center, notification preferences, or
  the channel strategy (in-app / email / push) for a product.
- Use when: users are drowning in notifications and you need batching,
  digests, dedup/collapse, frequency caps, or quiet hours.
- Use when: designing read/unread state, badges, dismissal, or cross-
  device notification sync.
- Use when: designing the DEVELOPER webhook surface — endpoint
  registration, event-type selection, delivery logs, test-send, manual
  replay, failing-endpoint alerts, or signing-secret rotation UX.
- Use when: designing unsubscribe/opt-out flows that must actually stop
  messages while still delivering security/transactional notices.
- Do NOT use when: the task is the webhook DELIVERY CONTRACT — envelope
  schema, signing algorithm, retry/at-least-once policy, event
  versioning, tenant-scoped subscription semantics — that is
  `api-event-architect`; this skill designs the UX over it.
- Do NOT use when: the task is generic empty/loading/error state
  rendering for these screens (the delivery-log's loading skeleton, the
  preference page's error toast) — that is `edge-state-ux-designer`.
- Do NOT use when: the "notifications" are internal system alerts to
  on-call engineers (severity, runbook, threshold) — that is
  `observability-operator` / `slo-reliability-architect`, not product UX.

## Inputs to Inspect

1. The event inventory: what happens in the product that a user or
   integrator might want to know about, and how time-sensitive each is
   (a security alert vs a "someone commented" nudge).
2. The channels available and their constraints: in-app center, email
   (deliverability, legal opt-out rules), push (permission, platform
   limits), and any SMS.
3. The webhook contract from `api-event-architect` (if present): the
   event types offered, retry/at-least-once policy, signing scheme, and
   subscription model — this skill's developer UX surfaces and controls
   exactly those, and must not contradict them.
4. Current pain: complaints of notification overload or missed critical
   notices; integrator support tickets about "did the webhook fire?",
   "can I replay?", "how do I rotate the secret?".
5. Legal/compliance constraints on messaging: unsubscribe obligations,
   the transactional-vs-marketing distinction, and consent records.

## Workflow

### End-user notifications

1. **Map events to channels and defaults.** For each notification-worthy
   event, decide default channel(s) and default on/off. Separate
   transactional/security (largely non-optional) from informational and
   marketing (opt-out, sometimes opt-in). State the default posture per
   category.
2. **Design the preference model.** Granularity users can actually reason
   about — per-category × per-channel, with sane grouping (not one
   toggle, not two hundred). One discoverable preference center; changes
   take effect immediately and are recorded.
3. **Design noise control.** Batching (realtime vs periodic digest),
   collapse/dedup ("3 people reacted" as one item, not three), frequency
   caps, and quiet hours honoring the user's timezone. This is the
   difference between a notification system people keep on and one they
   mute entirely.
4. **Design read-state and the center.** Seen vs read vs acted-on,
   mark-all-read, dismissal, badge/count semantics, and cross-device
   sync so reading on one device clears the badge on another.
5. **Design opt-out integrity.** Unsubscribe honors per-category, applies
   immediately, and is one-click where required by law; security/
   transactional notices remain deliverable and are labeled as such so
   opt-out expectations are clear. Record consent state.

### Developer webhook management

6. **Design endpoint management.** Register/edit/delete endpoints, select
   event types per endpoint, enable/disable, and separate test vs live
   environments. Surface the subscription model `api-event-architect`
   defined; do not invent a second one.
7. **Design delivery observability.** A delivery log per endpoint: event,
   timestamp, response status, latency, attempt count, and payload
   inspection with filtering. This is the first thing an integrator needs
   and the most commonly missing.
8. **Design self-service reliability tools.** Test-send / ping to a new
   endpoint, MANUAL replay of a specific failed delivery (with the
   idempotency reminder — safe replay depends on the consumer being
   idempotent, which is the contract's requirement), and failing-endpoint
   handling: alert the integrator, and surface any auto-disable-after-N-
   failures policy `api-event-architect` set (display it; don't redefine
   it).
9. **Design signing-secret UX.** Show the current secret (or its
   presence), support rotation with an overlap window so in-flight
   deliveries verifying against the old secret don't break, and make the
   verification instructions discoverable.

### Both

10. **Name the boundaries and deliver.** Delivery contract →
    `api-event-architect`; generic state rendering of these screens →
    `edge-state-ux-designer`; internal on-call alerting →
    `observability-operator`. Produce the two sub-specs in the Output
    Format.

Channel/default matrix, digest-vs-realtime decision guide, and the
webhook delivery-log field list:
[references/notification-webhook-sheet.md](references/notification-webhook-sheet.md).

## Output Format

```
NOTIFICATION & WEBHOOK UX — <product/surface>
== End-user notifications ==
Channels:      <in-app | email | push | sms> per event category
Preferences:   granularity=<per-category × per-channel>; defaults per category
               (transactional/security = non-optional, labeled)
Noise control: batching=<realtime|digest cadence>; collapse/dedup rules; freq caps; quiet hours (tz)
Read-state:    seen/read/dismiss; badges; cross-device sync
Opt-out:       per-category, immediate, one-click where required; consent recorded
== Developer webhooks (UX over api-event-architect's contract) ==
Management:    register/edit/disable; event-type selection; test vs live env
Delivery log:  event, ts, status, latency, attempts, payload view, filter
Reliability:   test-send; manual replay (idempotency noted); failing-endpoint alert +
               displayed auto-disable policy
Secret UX:     rotation with overlap window; verification docs discoverable
Boundaries:    delivery contract → api-event-architect; state rendering →
               edge-state-ux-designer; on-call alerts → observability-operator
```

## Validation Checklist

- [ ] Each event category has a default channel and on/off posture, with
      transactional/security separated from informational/marketing.
- [ ] Preferences are granular but reasonable (per-category × per-channel),
      in one center, effective immediately.
- [ ] Noise control exists: batching/digest, collapse/dedup, frequency
      caps, and timezone-aware quiet hours.
- [ ] Read-state (seen/read/dismiss), badges, and cross-device sync are
      designed.
- [ ] Opt-out honors per-category immediately and one-click where
      required; security/transactional notices remain deliverable and
      labeled.
- [ ] The webhook surface has a delivery log with payload inspection,
      test-send, and manual replay (with the idempotency caveat).
- [ ] Secret rotation uses an overlap window so in-flight deliveries
      don't break.
- [ ] The delivery contract, generic state rendering, and internal
      alerting are handed to their owning skills, not redefined here.

## Gotchas

- One master notifications toggle is not a preference model — users who
  want the one critical alert but none of the chatter are forced to pick
  all or nothing, and most pick nothing. Granularity is what keeps the
  channel alive.
- An unsubscribe link that "processes within 10 days" or silently keeps
  sending is a legal and trust failure. Opt-out is immediate and
  per-category; only genuinely transactional/security notices are exempt,
  and they must be labeled as such.
- A webhook with no delivery log is a black box: the integrator's only
  debugging tool becomes a support ticket asking you to grep your logs.
  The log is the feature.
- Manual replay without stating the idempotency requirement invites
  double-processing — replay is only safe because the consumer is
  idempotent, which is the contract's job to require and yours to
  remind.
- Rotating a signing secret with no overlap window breaks every in-flight
  and just-queued delivery still verifying against the old secret. Dual-
  valid rotation windows are the difference between a rotate button and
  an outage button.
- Digesting a time-critical alert (a security event, a failed payment)
  into tomorrow's summary is worse than no digest. Criticality overrides
  batching — decide it per category.
- Badge counts that don't sync across devices train users to distrust the
  badge; a read on the phone must clear the web badge.

## Stop Conditions

- The request is to design the webhook DELIVERY CONTRACT — envelope/
  payload schema, signing algorithm, retry and at-least-once policy,
  event versioning, subscription scoping → route to `api-event-architect`;
  this skill designs the UX over that contract and must not invent a
  conflicting one.
- The request is generic empty/loading/error state rendering for these
  screens → route to `edge-state-ux-designer`.
- The "notifications" are internal alerts to on-call engineers (severity,
  runbook, thresholds) → route to `observability-operator` /
  `slo-reliability-architect`.
- A proposed opt-out design would suppress security or legally-required
  notices, or a marketing message would be sent without consent → halt
  and surface the compliance risk to a human; do not ship a
  non-compliant messaging default.

## Supporting Files

- [references/notification-webhook-sheet.md](references/notification-webhook-sheet.md)
  — channel/default matrix, digest-vs-realtime decision guide, collapse/
  dedup patterns, and the webhook delivery-log field list.
- `evals/evals.json` — behavior cases including notification noise
  control, the opt-out-integrity refusal, and the webhook delivery-log/
  replay surface.
- `evals/trigger-evals.json` — discrimination against `api-event-architect`
  (THE contract seam), `edge-state-ux-designer`, and `observability-operator`.
