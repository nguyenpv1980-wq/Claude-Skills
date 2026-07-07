---
name: ai-governance-risk-reviewer
description: Review the governance and risk posture of an AI feature — classify its risk tier by impact (who is affected, reversibility, autonomy, sensitive-data and rights exposure), assign accountable human ownership, require appropriate human oversight (advisory / human-in-the-loop / human-on-the-loop) matched to the tier, check user-facing AI disclosure and consent, data-use and retention posture, a model/feature card documenting intended use and known limits, and a map from applicable obligations (EU AI Act tiers, NIST AI RMF functions) to concrete controls. Composes ai-sdlc-operating-model, agent-governance-audit, and human-approval-boundary rather than restating them. Use for an AI risk assessment, an AI feature's go/no-go governance review, or AI-policy readiness. Do NOT use to audit one change's process compliance (agent-governance-audit), enumerate technical attack threats (ai-threat-modeler), or define the SDLC lifecycle (ai-sdlc-operating-model).
---

# AI Governance & Risk Reviewer

## Purpose

Review whether an AI feature is governed responsibly: is its risk understood
and tiered, is a named human accountable, is the human-oversight model matched
to the impact, are users told they're interacting with AI where it matters, is
data use and retention appropriate, is there a model/feature card, and do the
applicable regulatory obligations map to concrete controls that actually
exist. The output is a governance verdict — with the gaps that must close
before a high-risk feature ships. This is the organizational/risk layer, above
the technical attack surface (`ai-threat-modeler`) and distinct from auditing
one change's process compliance (`agent-governance-audit`); it composes the
governance pack rather than restating it.

## Use When

- Use when: performing an AI risk assessment, an AI feature's governance
  go/no-go, or checking AI-policy readiness before launch.
- Use when: deciding the required human-oversight level for an AI feature by
  its impact, or assigning accountable ownership.
- Use when: mapping regulatory obligations (EU AI Act risk tiers, NIST AI RMF
  GOVERN/MAP/MEASURE/MANAGE) to the feature's concrete controls.
- Do NOT use when: auditing whether ONE change/PR followed governance process
  — `agent-governance-audit` (evidence-based per-control audit).
- Do NOT use when: enumerating technical threats (`ai-threat-modeler`) or
  defining the human+agent SDLC lifecycle (`ai-sdlc-operating-model`).

## Inputs to Inspect

1. The AI feature's purpose and impact: what decision/action it drives, who is
   affected (internal, customers, the public), and the consequence of a wrong
   output.
2. Autonomy and oversight: does it advise, act with a human in the loop, or
   act autonomously; where a human can intervene or reverse.
3. Data posture: what data it uses (personal, sensitive, tenant), where it
   goes (provider retention), consent and lawful basis, retention/deletion.
4. Transparency: is the user told it's AI; are limitations disclosed; is there
   a model/feature card (intended use, known failure modes, out-of-scope use).
5. Accountability: who owns the feature's outcomes; escalation and incident
   ownership (`incident-response-runbook`).
6. Applicable obligations: regulatory/contractual/policy requirements
   (EU AI Act tiering, sector rules, internal AI policy, NIST AI RMF as the
   risk method) — and existing governance artifacts from the Phase 1.5 pack.

## Workflow

1. **Classify the risk tier.** Score impact by: who is affected and how many,
   reversibility of a wrong output, degree of autonomy, sensitivity of data,
   and effect on people's rights/access/safety. Land on a tier (e.g.
   minimal / limited / high / unacceptable) using
   [references/ai-governance-framework.md](references/ai-governance-framework.md).
   No feature purpose/impact available → Stop Conditions.
2. **Match oversight to tier.** Higher tiers require stronger human oversight:
   advisory-only (human decides) → human-in-the-loop (human approves each
   action) → human-on-the-loop (human monitors, can intervene). Verify the
   feature's actual oversight matches its tier; a high-impact autonomous
   feature with no human gate is a blocking gap (compose
   `human-approval-boundary` for the gate design).
3. **Assign accountability.** A named human owner accountable for outcomes,
   not a team abstraction. Escalation path defined and tied to
   `incident-response-runbook`.
4. **Check transparency and consent.** Users are told they're interacting with
   AI where it affects them; limitations are disclosed; consent/lawful basis
   for data use exists where required. Absent disclosure on a user-affecting
   feature is a gap.
5. **Check data governance.** What's sent to the model, provider retention and
   training-use terms, PII/sensitive handling, retention/deletion — compose
   `sensitive-disclosure-guard` for the leak surface and
   `tenant-isolation-reviewer` for tenant data. Governance says whether the
   use is permitted; those skills check the mechanism.
6. **Require a model/feature card.** Intended use, in-scope and out-of-scope
   use, known limitations and failure modes, evaluation summary
   (`ai-evaluation-harness`), and the human-oversight model. Missing card on a
   material feature is a gap.
7. **Map obligations to controls.** For each applicable obligation (EU AI Act
   tier duties, NIST AI RMF function, internal policy), name the concrete
   control that satisfies it and where it lives — or mark it a gap. Do not
   assert regulatory conclusions as legal advice; flag items needing legal
   review.
8. **Verdict and gaps.** Governance PASS / CONDITIONAL / BLOCK with the
   specific gaps that must close, each routed to an owning skill/owner and a
   named risk acceptor via `human-approval-boundary` for anything shipped with
   residual risk.

## Output Format

```
AI GOVERNANCE & RISK REVIEW — <feature>
Risk tier: <minimal|limited|high|unacceptable> — <impact/reversibility/autonomy/data/rights rationale>
Oversight model: <advisory | HITL | HOTL> — matches tier? <yes/gap>
Accountable owner: <named human> | Escalation: <path> (→ incident-response-runbook)
Transparency/consent: <AI disclosure | limitations disclosed | lawful basis>
Data governance: <data used | provider retention/training | PII | retention> (→ sensitive-disclosure-guard)
Model/feature card: <present? intended use, limits, eval summary, oversight>
Obligations → controls: <obligation (EU AI Act tier / NIST AI RMF fn) → control | GAP>
Verdict: <PASS | CONDITIONAL | BLOCK>
Gaps to close: <gap → owning skill/owner → blocking?>
Residual risk: <accepted-by named human via human-approval-boundary>
Needs legal review: <items>
```

## Validation Checklist

- [ ] Risk tier assigned from impact, reversibility, autonomy, data
      sensitivity, and rights exposure — not from feature size.
- [ ] Oversight model matched to tier; a high-impact autonomous feature with
      no human gate is flagged blocking.
- [ ] A named human owner is accountable for outcomes; escalation is defined.
- [ ] User-facing AI disclosure and consent/lawful basis checked for
      user-affecting features.
- [ ] Data-use, provider retention/training, and retention/deletion posture
      reviewed; mechanism checks routed to the owning skills.
- [ ] A model/feature card exists (intended use, limits, eval summary,
      oversight) for material features.
- [ ] Obligations map to concrete controls or explicit gaps; legal-review
      items flagged, not asserted as legal conclusions.

## Gotchas

- Risk tier is about impact, not sophistication: a simple model that auto-
  denies loan applications is higher-risk than a complex one that suggests
  playlists. Tier by consequence.
- "There's a human somewhere" is not oversight — oversight requires the human
  to see the decision, have time and information to intervene, and not be
  rubber-stamping (see `human-agent-trust-reviewer` for consent fatigue).
- Disclosure gaps hide in "helpful" UX: a support bot that never says it's a
  bot, an AI-written email sent as a person. Material AF interaction needs
  disclosure.
- Provider data terms are part of governance: sending customer data to a model
  that trains on it can breach contracts and privacy law even if technically
  secure. Check the terms, not just the transport.
- This is not legal advice: regulatory tiering (is this "high-risk" under the
  EU AI Act?) often needs counsel — map and flag, don't rule.
- Governance without evidence is theater: a policy that says "human oversight"
  with no gate in the code is a gap — cross-check against
  `agent-governance-audit` for actual compliance.

## Stop Conditions

- No feature purpose or impact is described — stop; risk tiering needs to know
  what the feature does and to whom.
- The review surfaces a likely unacceptable-risk use (e.g. prohibited
  practice) — escalate to a named human and legal; do not bless it.
- The question is really one change's process compliance, the technical threat
  model, or the SDLC lifecycle — hand to the owning skill.
- A governance gap corresponds to an active harm in production — route to
  `incident-response-runbook`.

## Supporting Files

- [references/ai-governance-framework.md](references/ai-governance-framework.md)
  — the risk-tiering rubric, the oversight-to-tier matrix, model/feature card
  template, and the obligation→control mapping scaffold (EU AI Act tiers,
  NIST AI RMF GOVERN/MAP/MEASURE/MANAGE).
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the AI-platform-ops
  cluster and against `agent-governance-audit` and `ai-sdlc-operating-model`.
