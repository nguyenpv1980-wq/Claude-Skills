---
name: incident-response-runbook
description: 'Author incident response runbooks a responder who didn''t write them can execute at 3am — a SEV1–SEV4 ladder with one-minute criteria (ambiguity classifies up), roles (incident commander, comms, ops — small-org collapse stated), triage from page to decision point, containment invoking the rollback runbook by reference (rollback-runbook-author), tenant-aware comms templates per severity (never leaking other tenants'' data), evidence capture DURING the incident, SLI-verified resolution, and a blameless postmortem where every finding lands: regression test (regression-suite-curator), alert fix (observability-operator), runbook or architecture fix, or an owned accepted risk. Authors documents only — never runs an incident. Use when asked to write or overhaul incident runbooks, on-call playbooks, severity definitions, or the postmortem process. Do NOT use to diagnose a live failure (systematic-debugger), author rollback steps (rollback-runbook-author), or design what pages (slo-reliability-architect).'
---

# Incident Response Runbook

## Purpose

Produce the incident machinery a team runs when production breaks: severity
classification a responder can apply in one minute, roles that survive a
two-person company and a forty-person org, triage and containment
procedures wired to the actual alerts and dashboards, comms templates that
inform without over-promising or leaking, evidence capture that makes the
postmortem writable, and a postmortem process whose findings land as tests,
alerts, and fixes rather than a document nobody reopens. The bar is the
`manual-test-case-creator` stranger bar under stress: the responder did not
write this, did not ship the change, and is reading it at 3am.

## Use When

- Use when: asked to write or overhaul incident response runbooks or
  on-call playbooks.
- Use when: defining or revising the severity ladder and escalation rules.
- Use when: authoring incident communication templates — internal, status
  page, customer notification — or their cadences.
- Use when: designing the postmortem process or turning a specific
  incident's chaos into a repeatable procedure.
- Use when: an alert exists but its runbook link points at nothing
  (`observability-operator` requires runbook links; this skill writes
  them).
- Do NOT use when: an incident is live and the need is diagnosis —
  `systematic-debugger` (the runbook's diagnosis pointers route there).
- Do NOT use when: authoring the rollback procedure itself —
  `rollback-runbook-author` (this runbook INVOKES that artifact as a
  containment action).
- Do NOT use when: deciding what pages or the severity of signals —
  `slo-reliability-architect` designs the paging policy this runbook
  answers.
- Do NOT use when: wiring the alerts/dashboards — `observability-operator`.

## Inputs to Inspect

1. The alert spec and SLO design (`slo-reliability-architect`): what
   pages, at what severity intent — the runbook answers these pages.
2. Existing dashboards/telemetry surface (`observability-operator`
   output): what a responder can actually see at 3am.
3. Rollback runbooks that exist (`rollback-runbook-author` artifacts) and
   deployment strategies — the containment actions available.
4. The org's real on-call shape: rotation size, escalation paths, who can
   actually be woken, admin-access reality.
5. Commercial/comms obligations: SLA notification clauses, status-page
   tooling, customer-notification requirements per contract or regulation.
6. Tenancy shape: whether incidents can be tenant-scoped and what
   disclosure rules apply (`tenant-isolation-reviewer` posture).
7. Past incidents and postmortems: recurring failure classes, what broke
   in previous responses (comms delays, unclear ownership).

## Workflow

1. **Define the severity ladder objectively**: SEV1–SEV4 with
   classification criteria a responder applies in one minute (user-facing
   impact scope, data integrity risk, security implication, SLO budget
   burn rate), 2–3 concrete examples per level, default response per
   level (who is paged, comms cadence, whether an incident commander is
   assigned), and the rule that ambiguity classifies UP with explicit
   downgrade allowed. Security-flavored incidents get their routing named
   (who else is pulled in) without duplicating security procedures.
2. **Define roles that fit the org**: incident commander (owns decisions
   and the clock), comms lead (owns messages), ops/diagnosis (hands on
   keyboard) — with the small-org rule stated (one person wears all hats
   until reinforcements arrive; the hats still exist so handoff is
   possible) and escalation triggers (when to wake the next ring).
3. **Write triage per alert family**: from the page → the dashboard the
   alert links to → the first three questions (what changed: deploys,
   flags, migrations; blast radius: which journeys/tenants; burn rate:
   how fast is budget going) → the decision point. Deep diagnosis routes
   to `systematic-debugger` method; the runbook gets the responder TO the
   decision, not through root cause.
4. **Specify containment actions with their invocation criteria**: the
   rollback decision (invoke the `rollback-runbook-author` artifact —
   cite its decision criteria and time-box, never restate its steps),
   flag kills, traffic shedding/degradation ladders, tenant-scoped
   isolation (disable one tenant's pathological workload), maintenance
   mode — each with when-to-use and authority (what the responder may do
   alone vs what needs `human-approval-boundary`-grade signoff, e.g.,
   destructive data actions always).
5. **Write comms templates and cadences per severity**: internal channel
   updates (cadence per SEV), status-page posture (acknowledge honestly
   without speculation or blame; update rhythm; resolution message),
   customer/tenant notification rules — tenant-aware disclosure: a
   tenant-scoped incident is communicated to THAT tenant; cross-tenant
   incidents never name other affected tenants; security incidents
   follow their legal-review path before external comms.
6. **Mandate evidence capture during the incident**: a timeline scribe
   habit (timestamps, observations, actions, decisions — the comms lead
   or IC captures as they go), what to snapshot before it rots (dashboards,
   logs about to rotate, the deploy/flag state), and where it lands —
   this is what makes the postmortem factual instead of reconstructed.
7. **Define resolution and stand-down**: verification that the symptom is
   gone against the SLIs (not just "the fix deployed"), monitoring window
   before declaring resolved, stand-down comms, and the postmortem
   scheduling rule (SEV1/2 always; within N days while memory is fresh).
8. **Design the blameless postmortem with enforced handoffs**: timeline
   from captured evidence, contributing factors over single root causes,
   what went well/poorly in the RESPONSE (not just the system), and the
   mandatory disposition of every finding: regression test
   (`regression-suite-curator` promotion path), alert/dashboard fix
   (`observability-operator`), runbook fix (this artifact), architecture
   item (`architecture-designer`), or named accepted risk with an owner —
   no finding evaporates. Action items get owners and dates; unowned
   action items are recorded as accepted risks, visibly.

## Output Format

```
INCIDENT RESPONSE RUNBOOK — <scope/system>
Severity ladder: <SEV1–4 — one-minute criteria — examples — default
  response (paging, comms cadence, IC assignment) — ambiguity-up rule>
Roles: <IC / comms / ops — responsibilities — small-org collapse rule —
  escalation triggers>
Triage (per alert family): <page → dashboard → first three questions →
  decision point — diagnosis handoff to systematic-debugger>
Containment actions: <action — when to use — authority (alone vs
  approval-gated) — rollback invokes <rollback-runbook artifact ref>>
Comms: <templates per audience (internal/status/customer) × severity —
  cadence — tenant-aware disclosure rules — security-incident legal gate>
Evidence capture: <timeline habit, snapshot list, storage location>
Resolution & stand-down: <SLI verification, monitoring window, stand-down
  comms, postmortem scheduling rule>
Postmortem procedure: <blameless structure — finding dispositions
  (regression test / alert fix / runbook fix / architecture / accepted
  risk) — owner+date rule — review of response itself>
Staleness triggers: <alert-spec changes, architecture changes, org
  changes that require runbook revision>
```

## Validation Checklist

- [ ] Severity classification is executable in one minute by someone who
      didn't write it — objective criteria + examples, ambiguity
      classifies up.
- [ ] Every alert family in the spec has a triage entry ending at a
      decision point; none dead-ends at "investigate".
- [ ] Rollback is invoked by reference to the `rollback-runbook-author`
      artifact — its steps are not restated here.
- [ ] Every containment action states its authority level; destructive
      actions are approval-gated in writing.
- [ ] Comms templates exist per audience × severity with cadences;
      tenant-aware disclosure rules present; security incidents have a
      legal-review gate before external comms.
- [ ] Evidence capture is a during-incident procedure, not a postmortem
      wish.
- [ ] Resolution requires SLI-verified symptom absence plus a monitoring
      window.
- [ ] Every postmortem finding disposition routes somewhere named —
      regression test, alert fix, runbook fix, architecture item, or
      owned accepted risk. No evaporating findings.

## Gotchas

- Severity ladders written by engineers classify by technical layer;
  responders need USER-impact criteria — "database primary down" might be
  SEV1 or a non-event depending on failover.
- The IC doing hands-on-keyboard diagnosis is the classic response
  failure: decisions and the clock get dropped. The hats exist even when
  one person wears them — the runbook says which hat is speaking.
- Status-page messages promising root causes early ("we've identified the
  issue") age badly; templates acknowledge, scope, and commit to the next
  update time only.
- Comms silence during a long diagnosis reads as abandonment — the
  cadence is a promise independent of progress.
- Postmortem action items without owners and dates are the mechanism by
  which the same incident happens twice; the regression-test handoff is
  the single highest-value discipline in the loop.
- Runbooks rot at org speed: the escalation contact who left, the
  dashboard that moved. Staleness triggers and a review cadence are part
  of the artifact.

## Stop Conditions

- An incident is live NOW and the request is to handle it → stop
  authoring; route to the existing runbook + `systematic-debugger`;
  afterwards, this skill turns the experience into procedure.
- No paging/alert design exists to answer → the runbook would be
  fiction; route to `slo-reliability-architect` first (or scope the
  runbook to the alerts that do exist, gap named).
- Comms templates require legal/regulatory commitments (breach
  notification timelines, SLA credits) → draft with placeholders and
  route the commitments to `human-approval-boundary`; the runbook does
  not invent legal obligations.
- The org's on-call reality cannot execute the procedure (single
  engineer, no status page tooling) → write the runbook the org CAN run,
  and name the gap between it and the target state — a runbook for a
  fictional org protects nobody.

## Supporting Files

- `references/incident-runbook-template.md` — severity-ladder table,
  comms template skeletons per audience × severity, postmortem structure
  with the finding-disposition table.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the reliability
  cluster (`slo-reliability-architect`, `observability-operator`), against
  `rollback-runbook-author` (delivery cluster), and shipped
  `systematic-debugger` / `regression-suite-curator`.
