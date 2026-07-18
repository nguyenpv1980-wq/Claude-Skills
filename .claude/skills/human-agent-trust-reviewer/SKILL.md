---
name: human-agent-trust-reviewer
description: 'Adversarially review the human-approval layer of an agent system for trust exploitation (OWASP Agentic ASI09) — consent fatigue (approval floods that train rubber-stamping; rate/latency as the signals), deceptive, over-polished justifications making a dangerous action look routine, self-reported summaries diverging from the actual action (approvers must see the real diff/blast radius, not the agent''s story), dangerous steps bundled in innocuous batches, urgency manipulation, and automation bias as trust accumulates. Counterpart to human-approval-boundary: that skill places the gates; this one attacks their resilience and fixes what folds. Use when reviewing agent approval UX/flows, when approvals feel like a formality, or when an agent''s explanations drive human sign-off. Do NOT use to place the gates (human-approval-boundary), audit whether approvals happened (agent-governance-audit), address overreliance on AI content (ai-misinformation-guard), or tier oversight (ai-governance-risk-reviewer).'
---

# Human-Agent Trust Reviewer

## Purpose

Adversarially review the human oversight layer of an agent system (ASI09):
the attacker here doesn't bypass the approval gate — they go THROUGH it, by
exploiting the human. Consent fatigue turns approvers into rubber stamps;
polished, confident justifications make dangerous actions read as routine;
self-reported summaries describe a different action than the one that will
run; bundling buries the bad step in a good batch; manufactured urgency
short-circuits scrutiny; and automation bias accumulates until nobody reads
the request at all. The deliverable is findings ranked by how the approval
can be gamed, plus fixes: verified (not self-reported) action summaries,
fatigue budgets and measurements, unbundled approvals for high-impact steps,
and friction proportional to blast radius. `human-approval-boundary` places
the gates and defines when to stop; this skill attacks whether the gates
actually hold against a manipulative or manipulated agent.

## Use When

- Use when: reviewing the approval UX/flow for an agent system — what the
  approver sees, how often they're asked, what a click authorizes.
- Use when: approvals have become a formality — high volumes, near-100%
  approval rates, seconds-long decision times.
- Use when: an agent's own explanation or summary is the main thing humans
  read before signing off on its actions.
- Use when: designing the human-oversight layer for a new agent and you
  want it resilient to fatigue and deception from day one, or after an
  incident where a human approved something they didn't understand.
- Do NOT use when: deciding WHICH actions need approval and where the stop
  boundaries are — `human-approval-boundary` (this skill reviews whether
  those gates resist exploitation).
- Do NOT use when: auditing retrospectively whether required approvals
  happened (`agent-governance-audit`), addressing users over-trusting AI
  CONTENT/answers (`ai-misinformation-guard`), or assigning oversight
  levels to risk tiers (`ai-governance-risk-reviewer`).

## Inputs to Inspect

1. The approval surface: every flow where a human authorizes agent actions —
   UI prompts, PR reviews, chat confirmations, ticket sign-offs — and
   exactly what each shows the approver.
2. What the approval request contains: the agent's self-description vs
   system-derived facts (actual diff, target, blast radius, reversibility).
3. Approval telemetry if any: request volume per approver, approval rate,
   time-to-decision, batch sizes — the fatigue evidence.
4. The gate inventory from `human-approval-boundary` /
   `agent-tool-safety-guard`: which actions gate, their triggers, and each
   gated action's blast radius.
5. Bundling and pacing behavior: can one approval cover many actions; can
   the agent time or batch requests; can it re-request after a denial.
6. UI affordances: defaults, button prominence, diff visibility,
   "approve all" options, whether denial is as easy as approval.

## Workflow

1. **Map the approval surfaces.** For each: what action classes flow
   through it, what the approver sees, what one click authorizes. No
   approval flow to inspect → Stop Conditions.
2. **Attack the request content** using
   [references/trust-exploitation-patterns.md](references/trust-exploitation-patterns.md):
   is the approver shown the agent's SELF-REPORTED story or
   system-verified facts? A summary the agent writes about its own
   proposed action is attacker-influenceable by construction (injection or
   drift upstream) — require the actual diff/command/target/blast-radius
   from the system, with the agent's narrative clearly labeled as its
   claim.
3. **Measure fatigue.** From telemetry (or design its collection via
   `observability-operator`): requests per approver per day, approval
   rate, median decision time, deny rate over time. Near-100% approval at
   seconds-per-decision is a rubber stamp — the gate exists on paper only.
4. **Check approval-necessity calibration.** Fatigue is usually
   manufactured by over-gating: if low-impact actions flood the queue,
   recalibrate with `human-approval-boundary` / `agent-tool-safety-guard`
   so friction concentrates on blast radius. Fewer, richer approvals beat
   many hollow ones.
5. **Attack bundling and pacing.** Can a dangerous action ride inside an
   innocuous batch under one approval? Can the agent split a dangerous
   action into individually-innocent steps? Can it re-ask until it gets a
   yes, or time requests for low-scrutiny moments? Require unbundled
   approvals for high-impact steps, deny-memory (a denial sticks and is
   visible on re-request), and batch contents enumerated.
6. **Attack tone, framing, and urgency.** Justifications that assert
   safety ("routine cleanup, fully reversible") get checked against
   system-derived reversibility; urgency claims ("must run before the
   window closes") get friction, not less scrutiny — urgency is the
   classic pretext. Confidence and polish must earn zero trust weight.
7. **Check trust calibration over time.** Automation bias: after N good
   approvals, humans stop reading. Design against it: periodic
   forced-detail reviews, spot-check sampling of approved actions after
   execution (feeds `agent-governance-audit`), rotating approvers for
   high-impact classes, and deliberate canary requests where feasible.
8. **Rank findings and hand off fixes.** Each finding: exploitation path
   (how the approval is gamed) → what a manipulated/deceptive agent
   achieves → fix (verified summaries, fatigue budget, unbundling,
   friction-by-impact, calibration controls). Red-team cases (deceptive
   request → expected SAFE outcome: approver sees verified facts /
   unbundled step / denial sticks) hand to `ai-evaluation-harness`.

## Output Format

```
HUMAN-AGENT TRUST REVIEW — <system>
Approval surfaces: <flow → action classes → what the approver actually sees>
Fatigue evidence: <requests/approver/day, approval rate, median decision time, trend>
Findings (severity-ranked):
  [SEV] <surface> — Exploitation path: <fatigue|deception|self-report gap|bundling|urgency|automation bias → what gets approved>
    Fix: <verified summary | fatigue budget + recalibrated gates | unbundle | deny-memory | friction-by-impact | calibration control>
Self-report vs verified: <per surface: agent narrative labeled? system facts shown?>
Bundling/pacing posture: <batch rules, re-request behavior, deny-memory>
Calibration controls: <spot-checks, forced-detail cadence, approver rotation, canaries>
Red-team cases: <deceptive/bundled/urgent request → expected SAFE outcome> (→ ai-evaluation-harness)
Handoffs: gate placement → human-approval-boundary | post-hoc audit → agent-governance-audit
Not reviewed: <surfaces + why>
```

## Validation Checklist

- [ ] Every approval surface is mapped with what the approver actually
      sees and what one click authorizes.
- [ ] Approvers see system-verified facts (actual diff, target, blast
      radius, reversibility); agent self-reports are labeled as claims,
      never the sole basis.
- [ ] Fatigue is measured (volume, approval rate, decision time) or its
      collection is designed; rubber-stamp signals are treated as gate
      failure, not human failure.
- [ ] Approval necessity is recalibrated so friction concentrates on
      blast radius — flooding findings route to gate-placement skills.
- [ ] High-impact steps cannot ride bundles; batch contents are
      enumerated; denials stick and are visible on re-request.
- [ ] Urgency/confidence in justifications carries no trust weight;
      reversibility claims are checked against system-derived facts.
- [ ] Automation-bias controls exist (spot-checks, forced-detail cadence,
      rotation); findings carry concrete exploitation paths.

## AI Security Rules

- Human approvers are protected from consent fatigue and deceptive
  justification — approval-layer design treats the human as a resource an
  attacker can exhaust or mislead, not as an infallible backstop.
- The approver decides on system-verified facts: an agent's self-reported
  summary of its own action is a claim, and a claim is not evidence
  (`agent-governance-audit`'s rule, applied before the action).
- Friction is proportional to blast radius: over-gating manufactures the
  fatigue that under-protects the actions that matter.
- A denial is state: re-requesting a denied action without new facts is an
  escalation signal, not a second chance.

## Gotchas

- The fix for rubber-stamping is rarely "tell humans to pay attention" —
  it's fewer, richer, better-scoped requests. Attention is a budget the
  system spends; design the spend.
- The self-report gap is the sharpest edge: the same model that plans the
  action writes the justification — an injected or drifted agent writes
  exactly the story that gets approved. Only system-derived facts break
  the loop.
- Polish reads as competence: teams extend more trust to fluent,
  well-formatted justifications. Calibrate on verification, not prose
  quality — the most dangerous request is the best-written one.
- Bundling exploits kindness to reviewers: "47 routine changes + 1 scope
  expansion" gets approved for the 47. Enumerate and unbundle by impact.
- Approval fatigue metrics can be gamed too: an agent that learns denials
  correlate with detailed requests will start writing vaguer ones —
  measure informativeness, not just volume.
- Don't destroy the channel's usefulness: maximal friction on everything
  is how you get shadow workflows around the gate entirely. The goal is
  calibrated trust, not zero trust theater.
- This review can offend: it treats approvers as exploitable. Frame
  findings at the system ("the gate lets X through"), not the person.

## Stop Conditions

- No approval flow, UX, or telemetry is available and none can be
  described — stop; this skill attacks a concrete oversight layer, not the
  idea of one.
- Evidence that deception already succeeded (an approved action whose
  verified effect diverges from what the approver was shown) — route to
  `incident-response-runbook` and `agent-governance-audit`; treat as a
  live trust incident, not a review finding.
- Fixes require changing approval UX, gate placement, or telemetry in a
  live system — propose them; applying is a classified, approved step
  (`human-approval-boundary`).
- The real gap is which actions gate at all (`human-approval-boundary` /
  `agent-tool-safety-guard`), retrospective compliance
  (`agent-governance-audit`), or content overreliance
  (`ai-misinformation-guard`) — hand off and stop.

## Supporting Files

- [references/trust-exploitation-patterns.md](references/trust-exploitation-patterns.md)
  — the exploitation catalog (fatigue, self-report gap, bundling, urgency,
  automation bias), fatigue metrics and budgets, the verified-summary
  request template, and calibration-control patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the agentic cluster
  and against `human-approval-boundary`, `agent-governance-audit`,
  `ai-misinformation-guard`, and `ai-governance-risk-reviewer`.
