---
name: synthetic-monitoring-architect
description: 'Design ongoing black-box PRODUCTION monitoring — scheduled synthetic probes/journeys against the LIVE app and third-party deps from outside: the probe catalog (critical journeys + dependency health + heartbeat/canary), a HARD prod-safety contract (probes never mutate real data, never leak test fixtures, use ring-fenced synthetic accounts, self-clean), synthetic SLIs + alert-on-failure, and result capture/routing to a runbook. Produces the probe catalog, prod-safety contract, synthetic-SLI + alerting design, and runbook link. Use when monitoring whether production actually works from the user''s perspective, adding uptime/journey/dependency probes, or catching outages before customers do. Do NOT use for pre-release load/perf MEASUREMENT (performance-test-harness / load-test-planner), CI E2E (playwright-e2e-engineer), SLO target-setting (slo-reliability-architect), or white-box instrumentation (observability-operator). This DESIGNS probes; it does not run them against prod.'
---

# Synthetic Monitoring Architect

## Purpose

The gap between "all our metrics are green" and "customers can't log in" is
where synthetic monitoring lives: internal white-box telemetry can look
healthy while the actual user journey is broken end to end — an expired
certificate, a dead third-party dependency, a broken deploy that the health
check still calls "up." This skill designs black-box production monitoring:
scheduled probes that exercise the real critical journeys and dependencies
from the outside, on the same path a user takes, and alert when THAT breaks.
The load-bearing part is safety: a probe runs against PRODUCTION, so it must
never mutate real data, never leak or leave test fixtures, and always clean
up after itself. The deliverable is the probe catalog, the prod-safety
contract, the synthetic-SLI and alerting design, and the routing to a
runbook. This skill DESIGNS the probes and their safety envelope — it does
not execute them against production.

## Use When

- Use when: monitoring whether PRODUCTION actually works from the user's
  perspective — login, checkout, core journey, API availability — on a
  schedule, from outside.
- Use when: adding uptime / journey / third-party-dependency / heartbeat /
  canary probes, or you keep learning about outages from customers instead
  of from monitoring.
- Use when: internal dashboards are green during a real user-facing outage
  and you need an external, user-path signal.
- Use when: designing the safety envelope for probes that touch a live
  system (synthetic accounts, no-mutation, fixture cleanup).
- Do NOT use when: the goal is PRE-RELEASE measurement of latency/throughput/
  capacity under load — `performance-test-harness` (instrument) and
  `load-test-planner` (traffic plan) measure before you ship; synthetic
  monitoring watches after you ship.
- Do NOT use when: the goal is CI end-to-end tests gating a PR against a test
  environment — that is `playwright-e2e-engineer`; those run in CI on
  ephemeral data, not as prod-safe scheduled probes against production.
- Do NOT use when: the goal is defining the SLO/SLI TARGETS and error budgets
  — that is `slo-reliability-architect`; this skill produces a synthetic SLI
  that feeds those targets, it does not set them.
- Do NOT use when: the goal is WHITE-box internal instrumentation — metrics,
  traces, logs from inside the app — that is `observability-operator`;
  synthetic monitoring is the external black-box complement.

## Inputs to Inspect

1. The critical journeys and surfaces that must work in production: the
   handful whose failure is an incident (auth, the core workflow, payment,
   the public API), not every page.
2. Third-party dependencies the product relies on (auth provider, payment,
   email, key APIs) whose outage looks like your outage to users.
3. The existing monitoring: white-box telemetry (`observability-operator`),
   any current uptime checks, and the specific blind spots (green internally
   during a real outage).
4. The SLO/SLI targets (`slo-reliability-architect` output) the synthetic
   signal should feed — availability/latency of the journeys being probed.
5. The environments and accounts available: whether ring-fenced synthetic
   test accounts/tenants exist in production, and what a probe is permitted
   to touch.
6. The incident/alert routing: where a synthetic failure should page, and the
   runbook it should link to (`incident-response-runbook`).

## Workflow

1. **Select probes by incident value, not coverage.** Catalog the few
   journeys whose failure IS an incident and probe those. Three probe kinds:
   (a) **journey probes** — a full critical path (log in → do the core action
   → verify result); (b) **dependency probes** — is each critical third party
   reachable and correct; (c) **heartbeat/canary** — a cheap liveness ping at
   high frequency. Avoid probing everything; a hundred noisy probes hide the
   one that matters.
2. **Write the prod-safety contract FIRST — it gates every probe.** A probe
   runs against production, so:
   - **No mutation of real data.** Read-only where possible. Where a journey
     is inherently a write (checkout, signup), it uses a ring-fenced synthetic
     account/tenant and a designated test path, and the write is isolated
     from real tenants and real billing/notifications.
   - **No fixture leak.** A probe never leaves test data visible to real
     users, never triggers real emails/charges/webhooks to real recipients,
     and CLEANS UP what it creates (and has a fallback sweep for crashed runs).
   - **Least privilege.** The probe's synthetic account has only the access
     the journey needs; a leaked probe credential must not be a breach.
   - **Fail safe, not destructive.** A probe that errors mid-journey must not
     leave the system or its own fixtures in a harmful state.
   Any journey that cannot be made prod-safe is NOT probed synthetically in
   production — it is verified pre-release instead (hand to the E2E/perf
   skills). State this explicitly.
3. **Define synthetic SLIs.** Each probe yields a signal: success/failure and
   duration. Turn those into SLIs (synthetic availability = probe success
   rate; synthetic latency = probe duration) that feed the SLOs
   `slo-reliability-architect` set — clearly labeled SYNTHETIC (a probe
   result, not real user traffic) so it is never confused with RUM.
4. **Design scheduling.** Frequency per probe (heartbeat frequent, expensive
   journeys less so), and multi-region/multi-vantage-point where "up from one
   region" is not "up." State the tradeoff between frequency (faster
   detection) and cost/load on production and third parties.
5. **Design alerting on synthetic failure.** What constitutes failure (N
   consecutive fails, not one flaky run, to avoid paging on a single blip),
   severity, who is paged, and the runbook link. A synthetic alert must
   distinguish "the probe broke" (probe bug / expired synthetic credential)
   from "production broke" — a probe failing itself is not an outage.
6. **Design result capture and routing.** Where probe results and failure
   artifacts (screenshots, response bodies WITH secrets/PII redacted) are
   stored, dashboards, and the escalation path to `incident-response-runbook`.
7. **Deliver** the probe catalog, prod-safety contract, synthetic-SLI +
   alerting design, and runbook routing in the Output Format, with the
   design-not-run posture stated.

## Output Format

```
SYNTHETIC MONITORING DESIGN — <system/domain>
Posture:        DESIGN ONLY — probes are not run against production here;
  execution requires human approval + a validated prod-safety contract.
Probe catalog:  <probe — kind (journey/dependency/heartbeat) — what it verifies
  — frequency — vantage point(s)>
Prod-safety contract (gates every probe):
  no-mutation: <read-only | ring-fenced synthetic account + isolated test path>
  no-fixture-leak: <no real emails/charges/webhooks; cleanup + crashed-run sweep>
  least-privilege: <synthetic account scope>
  fail-safe: <errored probe leaves nothing harmful>
  un-prod-safe journeys → verified pre-release (E2E/perf), NOT probed in prod
Synthetic SLIs: <availability = probe success rate; latency = probe duration;
  labeled SYNTHETIC; feeds slo-reliability-architect targets (consumed, not set)>
Scheduling:     <per-probe frequency; multi-region; frequency vs cost/load>
Alerting:       <failure = N consecutive fails; probe-broke vs prod-broke;
  severity; who pages; runbook link → incident-response-runbook>
Result capture: <storage; redacted artifacts; dashboards; escalation>
Boundaries:     pre-release measurement → performance-test-harness/load-test-planner;
  CI E2E → playwright-e2e-engineer; SLO targets → slo-reliability-architect;
  white-box telemetry → observability-operator
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Probes are selected by incident value (the few journeys whose failure
      is an incident), not by coverage; noise is minimized.
- [ ] The prod-safety contract is written and gates every probe: no mutation
      of real data, ring-fenced synthetic accounts for inherent writes, no
      fixture leak / real emails-charges-webhooks, cleanup + crashed-run sweep.
- [ ] Journeys that cannot be made prod-safe are explicitly NOT probed in
      production and are handed to pre-release verification instead.
- [ ] Synthetic SLIs are labeled SYNTHETIC and feed (do not set) the SLOs.
- [ ] Alerting fires on sustained failure (N consecutive), distinguishes
      probe-broke from prod-broke, and routes to a runbook with an owner.
- [ ] Captured artifacts are redacted of secrets/PII.
- [ ] The design-only posture is stated: probes are not executed against
      production without human approval.
- [ ] Pre-release measurement, CI E2E, SLO-setting, and white-box telemetry
      are deferred to their owning skills.

## Gotchas

- A synthetic write against production without a ring-fenced account pollutes
  real data, real billing, and real notifications — the classic "our uptime
  check signed up 50,000 fake users / emailed real customers."
- Probes that don't clean up leak fixtures forever; the cleanup step and a
  fallback sweep for crashed runs are part of the design, not an afterthought.
- A probe failing because ITS credential expired looks exactly like an outage
  and cries wolf; distinguish probe-health from prod-health or the team
  learns to ignore synthetic alerts.
- Paging on a single failed run trains responders to ignore the pager; require
  N consecutive failures (with the tradeoff: slower detection) or a smarter
  signal.
- "Up from us-east" is not "up": a region/CDN/DNS issue is invisible from a
  single vantage point. Probe from where users are.
- Storing raw probe response bodies captures secrets and PII into the
  monitoring system; redact before storing.
- Synthetic availability is not real availability: it is a sample of a few
  journeys on a schedule. Presenting it as THE availability number overstates
  coverage — label it, and pair it with RUM.
- A probe hammering a third party at high frequency can trip that provider's
  rate limits or run up cost; frequency is a design decision with a bill.

## Stop Conditions

- Executing probes against production is requested (not just designing them) →
  STOP: this skill designs the probes and the prod-safety contract; running
  them against production — especially any write path — requires human
  approval and a validated safety contract (`human-approval-boundary`). Never
  fire synthetic writes at production on your own initiative.
- No ring-fenced synthetic account/tenant exists and a critical journey is
  inherently a write → do not design a probe that writes as/against real
  tenants; flag the missing synthetic-account prerequisite and verify that
  journey pre-release instead until it exists.
- The real need is pre-release capacity/latency measurement or CI gating →
  route to `performance-test-harness`/`load-test-planner` or
  `playwright-e2e-engineer`; synthetic monitoring is post-ship watching, not
  pre-ship testing.
- The SLO targets the synthetic SLI should feed are undefined → obtain them
  from `slo-reliability-architect`; a synthetic signal with no target is a
  graph nobody acts on.

## Supporting Files

- `evals/evals.json` — behavior cases: the prod-journey-monitoring design,
  the canary/heartbeat + dependency edge, the mutate-production refusal, and
  the CI-E2E non-trigger.
- `evals/trigger-evals.json` — discrimination against `performance-test-harness`
  / `load-test-planner` (pre-release measurement), `playwright-e2e-engineer`
  (CI E2E vs prod-safe probes), `slo-reliability-architect` (targets), and
  `observability-operator` (white-box vs black-box).
- No `references/` — the probe/safety/SLI/alerting procedure above is complete;
  detail lives in the produced artifacts.
