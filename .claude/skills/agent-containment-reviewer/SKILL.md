---
name: agent-containment-reviewer
description: 'Review whether a multi-agent system contains failure and drift (OWASP Agentic ASI08+ASI10 merged) — cascade half (ASI08): blast-radius isolation, bounded trust of upstream outputs, circuit breakers on inter-agent calls, checkpoints/rollback in multi-step pipelines, retry-storm and fan-out limits; rogue half (ASI10): drift detection against a behavioral baseline, agent inventory/lifecycle (no orphaned or shadow agents), and kill switches that sever authority (credentials revoked, not just processes killed), tested and reachable. Same inputs both halves: agent topology, autonomy boundaries, kill/rollback paths. Composes ai-cost-guardrail-designer (spend/loop bounds) + incident-response-runbook (execution). Use for multi-agent blast radius, drift detection, agent registries, or kill-switch design/review. Do NOT use for attacker-directed goal alteration (agent-goal-hijack-defender), spend/token caps alone (ai-cost-guardrail-designer), or running a live incident (incident-response-runbook).'
---

# Agent Containment Reviewer

## Purpose

Review whether an agent system can CONTAIN what goes wrong — one merged
review because its two halves share the same inputs (agent topology,
autonomy boundaries, kill/rollback paths). The **cascading-failure half
(ASI08)**: when one agent produces bad output, fails, or floods, does the
damage stay bounded, or does it propagate through every downstream agent,
retry storm, and fan-out? The **rogue-agent half (ASI10)**: when an agent's
behavior drifts from its intended pattern — no attacker required — is there
a baseline to detect it against, an inventory that even knows the agent
exists, and a kill switch that severs its AUTHORITY, not just its process?
The output is severity-ranked findings each with a propagation or drift
path and the isolation, breaker, checkpoint, inventory, and kill-switch
controls that close it. Spend containment composes
`ai-cost-guardrail-designer`; executing containment during an incident is
`incident-response-runbook`.

## Use When

- Use when: designing or reviewing a multi-agent system's blast radius —
  what happens downstream when one agent fails, hallucinates, or floods.
- Use when: adding circuit breakers, checkpoints, or rollback points to
  multi-step agent pipelines.
- Use when: reviewing drift detection, agent inventory/lifecycle
  (registration, ownership, decommissioning), or kill-switch design for an
  agent fleet.
- Use when: the Phase 7 backlog item "AI feature kill switch" is raised for
  an AGENT system — this skill owns that agentic slice.
- Do NOT use when: the deviation is attacker-directed goal alteration
  (`agent-goal-hijack-defender` — hijack has an adversary; drift does not).
- Do NOT use when: the only concern is spend/token/loop budgets
  (`ai-cost-guardrail-designer` — composed here for the cost dimension).
- Do NOT use when: an incident is live and needs running
  (`incident-response-runbook` executes; this skill designs what it will
  execute), or the question is message-layer security
  (`inter-agent-comms-reviewer`).

## Inputs to Inspect

1. The agent topology: which agents exist, who consumes whose output, where
   fan-out/fan-in happens, shared resources (queues, stores, APIs, budgets).
2. Autonomy boundaries per agent: what it may do without a human, its step/
   loop bounds, its tool blast radius (`agent-tool-safety-guard` matrix).
3. Failure handling today: retries and their bounds, timeouts, backpressure,
   what happens downstream when an agent emits garbage vs nothing.
4. The agent inventory: a registry of running agents with owner, purpose,
   version, credentials — or the absence of one.
5. Behavioral baselines and telemetry: what "normal" looks like per agent
   (actions/hour, tool mix, targets, cost) and what watches it
   (`observability-operator` wiring).
6. Kill/rollback paths: how an agent or the fleet is stopped, what a "stop"
   actually revokes, checkpoints a pipeline can resume/roll back from
   (`rollback-runbook-author` patterns).

## Workflow

1. **Map the topology and failure domains.** Draw agent→agent dependencies,
   fan-out points, and shared resources; group agents into failure domains
   (what fails together). No topology to inspect → Stop Conditions.
2. **Trace propagation paths (ASI08 half).** For each agent: if it emits
   bad output, who consumes it and acts on it? If it fails or slows, who
   retries/queues/blocks? If it fans out, what amplifies (N sub-agents × M
   retries × shared API)? Concrete propagation path required for HIGH
   severity.
3. **Design/verify isolation and breakers** using
   [references/containment-patterns.md](references/containment-patterns.md):
   bounded trust of upstream outputs (validation between agents, not just
   at the edge — compose `structured-output-validator`), circuit breakers
   on inter-agent calls, bulkheads around shared resources, bounded retries
   with backoff, queue depth limits and backpressure, and fan-out caps.
   Cost amplification wires to `ai-cost-guardrail-designer` budgets.
4. **Place checkpoints and rollback points.** Multi-step pipelines need
   durable checkpoints: a failed/contaminated run resumes from a known-good
   point or rolls back cleanly (side effects since the checkpoint
   enumerated — compose `rollback-runbook-author` discipline). All-or-
   nothing pipelines with side effects mid-stream are findings.
5. **Verify the inventory (ASI10 half).** Every agent is registered: owner,
   purpose, version, identity/credentials, autonomy level, kill path.
   Orphaned agents (owner gone), shadow agents (running but unregistered),
   and zombie agents (decommissioned but credentials alive) are findings —
   cross-check the identity inventory from
   `agent-identity-privilege-reviewer`.
6. **Define drift detection.** Per agent, a behavioral baseline (action
   rate, tool mix, target scope, cost, error profile) and deviation signals
   watched by `observability-operator` telemetry. Drift needs no attacker:
   a model update, prompt change, or data shift is enough. Detection
   latency matters — "we'd notice eventually" is the ASI10 containment gap.
7. **Design the kill switch so it severs authority.** Per-agent and
   fleet-level stops that: revoke/expire the agent's credentials and tool
   access (not just SIGKILL a process that a supervisor restarts), drain or
   fence its queued work, notify downstream consumers, and leave an audit
   record. Kill switches are TESTED (rehearsal cadence, staleness triggers)
   and reachable by named humans in bounded time. Execution during a real
   event is `incident-response-runbook`'s.
8. **Rank findings.** Each: propagation/drift path → concrete impact →
   control (isolate, break, checkpoint, register, baseline, kill). State
   what was not reviewed.

## Output Format

```
AGENT CONTAINMENT REVIEW — <system>
Topology & failure domains: <agents, dependencies, fan-out, shared resources>
Cascade findings (ASI08, severity-ranked):
  [SEV] <agent/edge> — Propagation path: <bad output/failure/flood → downstream impact>
    Controls: <bounded trust | circuit breaker | bulkhead | retry bound | backpressure | fan-out cap | checkpoint>
Rogue/drift findings (ASI10, severity-ranked):
  [SEV] <agent> — Gap: <no baseline | no inventory entry | kill switch doesn't sever authority | detection latency>
    Controls: <register+owner | baseline+signals | authority-severing kill | rehearsal>
Inventory: <registered / orphaned / shadow / zombie agents>
Kill switches: <per-agent + fleet: what each actually revokes; tested when; reachable by whom>
Checkpoints/rollback: <pipeline resume/rollback points; side-effect enumeration>
Composed: cost amplification → ai-cost-guardrail-designer | execution → incident-response-runbook
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] Topology mapped with failure domains, fan-out points, and shared
      resources; propagation paths traced per agent.
- [ ] Inter-agent trust is bounded: upstream outputs validated before
      downstream agents act; breakers/bulkheads/retry bounds/backpressure
      present where propagation paths demand them.
- [ ] Multi-step pipelines have durable checkpoints and a rollback story
      with side effects since checkpoint enumerated.
- [ ] Every running agent is in the inventory with owner, purpose,
      autonomy level, and kill path; orphaned/shadow/zombie agents flagged.
- [ ] Each agent has a behavioral baseline and drift signals wired to
      telemetry; detection latency stated, not implied.
- [ ] Kill switches sever AUTHORITY (credentials/tool access revoked),
      cover agent and fleet levels, are tested on a cadence, and are
      reachable by named humans.
- [ ] Cost amplification composed to `ai-cost-guardrail-designer`; findings
      carry concrete propagation/drift paths.

## AI Security Rules

- Multi-agent failure is contained by design: blast-radius isolation,
  circuit breakers, and checkpoints are architecture, not incident-day
  improvisation.
- An agent nobody inventoried is uncontained by definition — you cannot
  kill what you don't know is running.
- A kill switch that leaves credentials valid has not killed anything:
  stopping an agent means severing its authority.
- Drift detection is a containment control: the gap between "behavior
  changed" and "someone noticed" is the ASI10 risk, and it is measured, not
  assumed.

## Gotchas

- The hallucination cascade: agent A's plausible-but-wrong output becomes
  agent B's trusted input — bad data propagates faster than failures
  because nothing errors. Validation BETWEEN agents, not just at the edges.
- Retry storms amplify: one flaky downstream service × per-agent retries ×
  fan-out = self-inflicted DoS and a shredded budget. Bound retries at
  every level and give shared resources bulkheads.
- The supervisor-restart trap: killing the process of a misbehaving agent
  that a supervisor auto-restarts contains nothing — the kill path must
  reach the credential/authorization layer.
- Shadow agents accumulate: prototypes, cron-launched one-offs, and
  "temporary" agents outlive their owners. Inventory drift IS the ASI10
  containment gap; sweep for unregistered actors, not just registered ones.
- Drift hides in aggregate metrics: an agent can stay within normal volume
  while its tool mix or target scope shifts — baseline the SHAPE of
  behavior, not just the rate.
- Checkpoints without side-effect enumeration are false comfort: resuming
  from step 3 after steps 4–6 already sent emails is not a rollback —
  enumerate what fired since the checkpoint.
- Fleet-level kill switches that nobody rehearsed fail at the worst moment
  — test them like backups (`rollback-runbook-author` rehearsal
  discipline), and check they don't take down the humans' access too.

## Stop Conditions

- No topology, autonomy, or lifecycle information is available — stop; this
  skill reviews a concrete agent system, not the concept of containment.
- An agent is actively rogue or a cascade is in progress — route to
  `incident-response-runbook` (this skill's kill-switch design is what it
  invokes); do not run the incident from a review.
- Executing a kill switch, revoking credentials, or decommissioning agents
  now — side-effecting human calls via `human-approval-boundary`; this
  skill designs the paths.
- The deviation under review is attacker-directed goal alteration or a
  message-layer compromise — hand to `agent-goal-hijack-defender` /
  `inter-agent-comms-reviewer` and stop.
- Kill-switch design requires severing credentials but no identity model
  exists to sever — hand the prerequisite to
  `agent-identity-privilege-reviewer` and stop.

## Supporting Files

- [references/containment-patterns.md](references/containment-patterns.md)
  — failure-domain mapping, the propagation-path catalog (bad-output /
  failure / flood / cost cascades), breaker/bulkhead/backpressure patterns,
  checkpoint-and-rollback design, the agent inventory schema,
  drift-baseline signals, and the authority-severing kill-switch rubric.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the agentic cluster and
  against `ai-cost-guardrail-designer`, `incident-response-runbook`,
  `observability-operator`, and `llm-output-safety-reviewer`.
