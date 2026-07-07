# AI governance & risk framework

Detail for `ai-governance-risk-reviewer`. Companion method: NIST AI RMF 1.0
(GOVERN/MAP/MEASURE/MANAGE). Regulatory tiering language mirrors the EU AI Act
risk tiers. This is a mapping scaffold, NOT legal advice — flag items for
counsel.

## Risk-tiering rubric

Score the feature on each axis, then take the highest:

| Axis | Low → High |
|---|---|
| Who is affected | internal tool → customers → the public / vulnerable groups |
| Number affected | one user → a tenant → everyone |
| Reversibility | easily undone → costly → irreversible harm |
| Autonomy | advisory → acts with approval → fully autonomous |
| Data sensitivity | public → business → personal/sensitive/special-category |
| Rights/safety | convenience → access/opportunity → safety/legal rights |

Tier bands (mirrors EU AI Act framing):
- **Minimal** — low on all axes; standard controls suffice.
- **Limited** — user-facing; transparency obligations (tell users it's AI).
- **High** — affects rights/access/safety, or autonomous with real
  consequence; needs strong oversight, documentation, evaluation, accountability.
- **Unacceptable** — prohibited practice (e.g. manipulative or rights-violating
  use). Escalate; do not bless.

## Oversight-to-tier matrix

| Tier | Minimum oversight |
|---|---|
| Minimal | advisory; monitoring |
| Limited | advisory + AI disclosure to users |
| High | human-in-the-loop OR human-on-the-loop with real intervention capability, accountable owner, incident path |
| Unacceptable | not permitted |

Oversight is real only if the human sees the decision, has the information and
time to intervene, and is not rubber-stamping (cross-ref
`human-agent-trust-reviewer` for consent fatigue). Gate design →
`human-approval-boundary`.

## Model / feature card template

- **Intended use** — what it's for, in-scope inputs/users.
- **Out-of-scope use** — explicitly what it must NOT be used for.
- **Known limitations & failure modes** — where it's wrong, biased, or
  uncertain.
- **Evaluation summary** — results from `ai-evaluation-harness` (quality,
  safety, groundedness).
- **Data** — what it uses, provider retention/training terms, PII handling,
  retention/deletion.
- **Oversight model** — advisory/HITL/HOTL and the accountable owner.
- **Version** — model/prompt/retrieval version this card describes.

## Obligation → control mapping (NIST AI RMF frame)

| RMF function | Governance question | Example control (or GAP) |
|---|---|---|
| GOVERN | Is there a policy, accountable owner, roles? | AI policy + named owner |
| MAP | Is context/risk/impact identified? | this risk tiering + `ai-threat-modeler` |
| MEASURE | Is it evaluated for quality/safety/bias? | `ai-evaluation-harness` results |
| MANAGE | Are risks treated, monitored, incident-handled? | guardrails, `observability-operator`, `incident-response-runbook` |

For each applicable obligation (regulatory, contractual, internal policy),
name the concrete control that satisfies it and where it lives, or record a
GAP with an owner. Do not assert regulatory conclusions ("this is compliant")
— that is a legal determination; map and flag.

## Data-governance checks

- What data leaves to the provider; is it personal/sensitive/tenant data.
- Provider terms: retention window, training-on-your-data, sub-processors,
  region/residency.
- Lawful basis / consent for the use; user rights (access, deletion).
- Retention and deletion of prompts, outputs, and logs.
- Mechanism checks handed to `sensitive-disclosure-guard` (leak surface) and
  `tenant-isolation-reviewer` (tenant data); governance decides PERMITTED, they
  check ENFORCED.

## Verdict discipline

PASS (governed, ship) / CONDITIONAL (ship after named gaps close) / BLOCK
(high/unacceptable gap open). Every residual risk shipped has a named human
acceptor via `human-approval-boundary`. Cross-check claimed controls against
`agent-governance-audit` — a policy with no enforcing mechanism is a gap.
