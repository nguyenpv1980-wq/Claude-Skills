---
name: security-logging-alerting-architect
description: Design the security-event detection and alerting layer — DETECTION coverage (what must be logged: authn failures/anomalies, access-control denials, privilege/config changes, injection/abuse signals, sensitive-data access), ALERTING rules (alert vs ticket, thresholds justified against baselines, correlation, noise control), and response WIRING (every alert has an owner, severity, escalation, runbook link). Closes OWASP Top 10:2025 A09 (Security Logging and Alerting Failures). Use when designing security monitoring/detection/alerting or asking "would we notice this attack?". Do NOT use for the audit RECORD (audit-log-architect — records, never detects/alerts), system/perf telemetry or alert-config edits (observability-operator), reliability SLOs/paging (slo-reliability-architect), or the playbook AFTER an alert (incident-response-runbook — this designs what fires it).
---

# Security Logging & Alerting Architect

## Purpose

Produce the design that makes attacks visible and actionable: a security-event
DETECTION coverage map (which events must be logged, with the fields that make
them detectable), ALERTING rules per event class (what fires an alert vs a
ticket, thresholds justified against observed baselines, correlation and noise
control so real attacks are not buried), and response WIRING (every alert
routes to a named owner with severity, escalation path, and runbook link).
This closes OWASP Top 10:2025 A09 — Security Logging and Alerting Failures:
the failure class where a breach succeeds not because nothing was logged, but
because nothing DETECTED it, nothing ALERTED, or nobody was wired to respond.
Design-only and model-invocable: this skill edits no code and no live alert
configuration — implementation is handed to the operating skills.

## Use When

- Use when: designing or overhauling security monitoring — "what security
  events should we log, detect, and alert on?"
- Use when: asking "would we notice this attack?" — auditing existing
  security logging/alerting coverage against likely attacker behavior.
- Use when: security alerts exist but are ignored noise — redesigning
  thresholds, correlation, and alert-vs-ticket classification without
  silently losing detection coverage.
- Use when: an incident review found the attack was visible in logs but no
  alert fired — or the alert fired and no one owned it.
- Use when: compliance or a customer contract requires demonstrable security
  MONITORING (detection and alerting), beyond an audit record.
- Do NOT use when: designing the tenant-scoped audit RECORD — taxonomy,
  schema, integrity, retention — that is `audit-log-architect`; it records
  events but does not detect threats or alert. This skill designs detection
  and alerting ON TOP of those records, and feeds logging gaps back to it.
- Do NOT use when: instrumenting system/performance telemetry or EDITING
  live alert/dashboard config — `observability-operator` (manual-only)
  implements this skill's alerting design in the monitoring stack.
- Do NOT use when: defining reliability SLOs/SLIs, error budgets, or what
  pages for reliability — `slo-reliability-architect`; security alerting
  fires on attacker behavior, not on error-budget burn.
- Do NOT use when: writing what responders DO once paged —
  `incident-response-runbook` authors the reactive playbook; this skill
  designs the detection and alerting that FIRES it, and every alert in the
  design links to such a runbook.

## Inputs to Inspect

1. The threat model (`threat-modeler` / `ai-threat-modeler` output): each
   enumerated threat is a detection requirement — the design must answer
   "would we see this?" per threat, or record the blind spot.
2. The audit-log design (`audit-log-architect` output) and current logging
   reality: which security-relevant events are already recorded, with what
   fields — detection consumes these records; missing events or fields are
   logging gaps this skill feeds back as requirements.
3. The authorization matrix and tenant model: access denials, privilege/role
   changes, and cross-tenant attempts are first-class detection events, and
   tenant context is a mandatory field on every security event.
4. The current alert inventory and its noise level: what already fires,
   alerts/day, acknowledgment and action rates — thresholds set without this
   baseline are guesses and must be labeled as such with a tuning date.
5. The incident-response reality: severity ladder, paging paths, runbook
   inventory, and who is actually on call — wiring targets must exist; a
   route to nobody is a gap, not wiring.
6. Regulatory or contractual monitoring obligations that name specific
   detections, retention, or response times.

## Workflow

1. **Derive detection requirements from attacker behavior, not from what is
   convenient to log.** Walk the threat model and the application's security
   surfaces; for each, state the observable event an attack would produce.
   Start from the standard security-event classes in
   [references/security-event-coverage-sheet.md](references/security-event-coverage-sheet.md):
   authentication (failures, anomalies, credential stuffing patterns),
   access control (denials, object-level failures, cross-tenant attempts),
   privilege and security-config changes, input attacks (injection attempts,
   abuse-signal spikes), and sensitive-data access/export.
2. **Map required events against what is actually logged.** For each required
   event: does a record exist, does it carry the fields detection needs
   (actor, tenant, target, outcome, source, correlation id, timestamp)?
   Missing events/fields become logging requirements handed to
   `audit-log-architect` or the owning service — with the rule that security
   events must be structured, not prose log lines.
3. **Classify each event class into a detection posture:** log-only (needed
   for investigation), ticket (aggregated review), or alert (a human reacts
   now). The default for a new class is ticket until a justified threshold
   exists — alerting on everything is how alerting fails.
4. **Design the alert rules.** Per alerting class: the trigger condition
   (single event or threshold/correlation over a window), the threshold and
   its justification against the observed baseline, and the noise controls —
   deduplication, aggregation by actor/source, and suppression rules that
   are bounded and owned. State explicitly what each rule will NOT catch.
5. **Wire every alert.** Owner (a role that exists), severity on the
   incident ladder, escalation path, and the runbook it links to — missing
   runbooks become named requirements for `incident-response-runbook`.
   An alert without an owner and runbook is not done.
6. **Design the coverage tests.** For each alert: a safe, synthetic way to
   prove it fires end-to-end (test event → detection → alert → route), plus
   a negative check that the noise controls do not silently swallow the
   real pattern. Alert rules that cannot be exercised are listed as
   unverifiable.
7. **State the blind spots honestly.** Threats with no detection, events
   that cannot be logged today, thresholds set without baselines — each with
   a reason and a follow-up owner. An honest blind-spot list beats implied
   full coverage.
8. **Hand off implementation.** The alert/dashboard configuration is
   implemented by `observability-operator` (manual-only); logging changes go
   to the owning service or `audit-log-architect`; response procedures to
   `incident-response-runbook`. This skill changes nothing itself.

## Output Format

A security detection & alerting design containing:

1. **Detection coverage map** — event class × required events × source ×
   required fields × current status (logged / partial / missing).
2. **Alerting rules table** — per rule: trigger condition, threshold +
   justification (baseline or "unbaselined — tuning date"), correlation/
   dedup/suppression, severity, owner, runbook link, and what it will not
   catch.
3. **Response wiring table** — alert → owner → escalation → runbook, with
   gaps named (missing runbook, unowned route).
4. **Coverage test plan** — per alert, the safe synthetic exercise proving
   it fires and routes.
5. **Blind-spot register** — undetected threats and unverifiable rules,
   each with reason and follow-up owner.
6. **Handoff list** — logging requirements (to `audit-log-architect` /
   service owners), implementation items (to `observability-operator`),
   runbook items (to `incident-response-runbook`).

## Validation Checklist

- [ ] Every threat-model threat has a detection answer: covered, ticketed,
      or an explicit blind-spot entry — none silently skipped.
- [ ] Every alert rule has: trigger, threshold justification (or an
      "unbaselined" label with a tuning date), severity, owner, escalation,
      and a runbook link.
- [ ] Noise controls (dedup/aggregation/suppression) are bounded and owned —
      no unbounded suppression that could hide a real attack.
- [ ] Tenant context is a required field on every security event in the
      coverage map.
- [ ] Each alert has a defined safe way to prove it fires end-to-end, or is
      listed as unverifiable.
- [ ] The design changed no code and no live alert config; every change is
      in the handoff list with an owning skill or human.
- [ ] OWASP category claims are scoped to the concrete risks covered; exact
      category text is flagged for confirmation against the OWASP source,
      not asserted from memory.

## Gotchas

- **Recording is not detecting.** A complete audit log with no rules watching
  it fails A09 exactly as hard as no log — the breach is reconstructable
  but not noticed. The audit trail is an input here, never the deliverable.
- **Alert-on-everything is alert-on-nothing.** Unjustified thresholds and
  unaggregated per-event alerts train responders to ignore the channel; the
  design must show the noise math (expected fires/day) per rule.
- **Deleting noisy alerts loses coverage silently.** Noise redesign must
  show what each removed/retuned rule stops catching and where that
  detection moved (ticket, correlation rule) — otherwise it is coverage
  loss dressed as hygiene.
- **Security alerting ≠ reliability alerting.** Error-budget burn pages on
  user-visible symptoms; security detection fires on attacker behavior that
  may be invisible to users (slow credential stuffing, low-and-slow export).
  Reusing reliability thresholds for security events misses both ways.
- **Fields decide detectability.** "Login failed" without actor, source, and
  tenant cannot support a credential-stuffing rule; field requirements are
  part of detection design, not an implementation detail.
- **Wiring rot.** Routes to a person (not a role), to a channel nobody
  reads, or to a runbook that was never written — wiring must reference
  things that verifiably exist at design time.
- **OWASP text drift.** This skill's A09 mapping uses the category name as
  recorded in the repo's D8 coverage audit of OWASP Top 10:2025; when
  quoting category text or scope, confirm against the OWASP source first
  (verify-don't-assert) — editions revise, and `framework-edition-tracker`
  owns detecting that drift.

## Stop Conditions

- No threat model and no statable attack concerns exist — detection
  requirements would be invented; run `threat-modeler` first or get the
  human's concern list.
- Asked to EDIT live alert/dashboard/monitoring configuration — that is
  `observability-operator` (manual-only); this skill designs and hands off.
- Asked to weaken or delete alerting/suppression in a way that removes
  detection coverage without a documented, human-approved tradeoff.
- The organization has no incident-response path at all (no owner, no
  severity ladder): alert wiring would route to nobody — surface this as
  the blocking gap instead of designing unroutable alerts.
- Monitoring obligations are contractual/regulatory and their exact
  requirements are unavailable — confirm the obligation text with the human
  rather than guessing detections into a compliance claim.

## Supporting Files

- [references/security-event-coverage-sheet.md](references/security-event-coverage-sheet.md)
  — starter security-event classes with example events, required fields,
  default detection posture, and noise-control patterns.
- [evals/evals.json](evals/evals.json) — behavior cases: coverage design,
  noisy-alert redesign, refusal to edit live config, source-honesty on
  OWASP text, and the audit-record boundary.
- [evals/trigger-evals.json](evals/trigger-evals.json) — discrimination
  against `audit-log-architect`, `observability-operator`,
  `slo-reliability-architect`, and `incident-response-runbook`.
