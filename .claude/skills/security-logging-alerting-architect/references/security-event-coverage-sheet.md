# Security-Event Coverage Sheet

Starter classes for the detection coverage map. Every event: structured, with
actor, tenant, target, outcome, source (IP/client), correlation id, timestamp.
Postures: **log** (investigation), **ticket** (aggregated review), **alert**
(human reacts now). Defaults below are starting points — justify against the
system's own baseline before promoting anything to alert.

## Event classes

| Class | Example events | Detection-critical fields | Default posture |
|---|---|---|---|
| Authentication | failed login, success after N failures, new device/location, MFA disabled/bypassed, token replay, password-reset burst | actor, source, outcome, factor | ticket; alert on threshold/correlation (e.g., distributed failures → few successes) |
| Access control | authz denial, object-level (IDOR-shaped) failures, cross-tenant attempt, repeated 403s on enumerable ids | actor, tenant, target object, rule that denied | log; alert on cross-tenant attempt or enumeration pattern |
| Privilege & security config | role grant/elevation, permission change, security setting toggled (MFA policy, RLS, allowlists), API key/secret created or scoped up | actor, before/after, approver if any | alert (low volume, high value) |
| Session & identity | concurrent-session anomaly, session fixation signals, impersonation/support-access start and end | actor, impersonated principal, session ids | ticket; alert on impersonation outside policy |
| Input attacks | validation-layer rejects (injection-shaped payloads), WAF-class blocks, deserialization failures, SSRF-shaped egress denials | source, endpoint, payload class (never raw secrets) | log; ticket on spike vs baseline |
| Sensitive-data access | bulk read/export, access to flagged records, download volume anomaly per actor/tenant | actor, tenant, dataset, volume | ticket; alert on volume/off-hours anomaly |
| Availability abuse | rate-limit trips, quota exhaustion bursts, cost/consumption anomalies (composes ai-cost-guardrail-designer telemetry for AI surfaces) | source, actor/tenant, limit hit | ticket; alert on sustained/multi-source pattern |
| Security tooling health | log pipeline drop/lag, detection rule failed to evaluate, alert route bounced | component, error | alert — a dead pipeline is a masked breach |

## Noise-control patterns

- **Deduplicate** identical (rule, actor, source) fires within a window;
  count, don't repeat.
- **Aggregate** per actor/source/tenant before thresholding — 500 failures
  from one IP and 5 each from 100 IPs are different attacks; rules should see
  both shapes.
- **Correlate** low-value events into one high-value pattern (failures →
  success; denial burst → privilege change) instead of alerting on the parts.
- **Suppress** only bounded and owned: every suppression has a scope, an
  expiry, an owner, and a reason — unbounded suppression is silent coverage
  loss.
- **Budget the channel:** expected fires/day per rule, summed per receiving
  rotation; if the sum exceeds what a human will actually triage, the design
  is dishonest — demote, correlate, or staff.

## Wiring minimums (per alert)

Owner (a standing role) · severity on the incident ladder · escalation path ·
runbook link (exists, not planned) · coverage test (safe synthetic exercise
proving fire + route) · review date for the threshold.
