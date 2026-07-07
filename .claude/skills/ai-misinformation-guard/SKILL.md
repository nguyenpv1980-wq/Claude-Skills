---
name: ai-misinformation-guard
description: Design controls against LLM misinformation and overreliance (OWASP LLM09) — require grounding (answer from retrieved/authoritative sources, not model memory, for factual claims), verifiable citations checked to actually support the claim, calibrated uncertainty and refusal-to-answer when evidence is thin, validation of consequential facts before they drive a decision or action, and UX that signals confidence and limits so users don't over-trust. Covers package/API hallucination (recommending nonexistent dependencies an attacker can register) and human-oversight for high-impact outputs. Composes rag-security-architect for grounded retrieval and ai-governance-risk-reviewer for oversight tiering. Use when wrong-but-confident output could mislead users or drive decisions. Do NOT use for unsafe output HANDLING (llm-output-safety-reviewer), output SHAPE (structured-output-validator), injection (prompt-injection-defender), or training-data integrity (model-poisoning-reviewer).
---

# AI Misinformation Guard

## Purpose

Design the controls that keep an LLM feature from confidently producing false
information that misleads users or drives bad decisions (LLM09). The
deliverable: a grounding strategy (factual claims answered from
retrieved/authoritative sources, not the model's parametric memory),
citation verification (cited sources actually support the claim), calibrated
uncertainty and refusal when evidence is thin, validation of consequential
facts before they act, and UX that communicates confidence and limits so users
don't over-rely. It also covers the security-flavored slice — package/API
hallucination (an invented dependency an attacker can register) — and routes
high-impact outputs to human oversight.

## Use When

- Use when: an AI feature makes factual claims, gives advice, or produces
  output that users or systems act on, and wrong-but-confident output would
  cause harm.
- Use when: designing grounding, citations, uncertainty signaling, or
  fact-validation for an AI feature.
- Use when: an AI feature recommends code dependencies, APIs, or commands
  (package/slop-squatting hallucination risk).
- Do NOT use when: the concern is unsafe HANDLING of output (XSS/exec) —
  `llm-output-safety-reviewer`; or output SHAPE — `structured-output-validator`
  (this skill is about whether the content is TRUE, not well-formed or safe to
  render).
- Do NOT use when: the concern is injection (`prompt-injection-defender`) or
  training-data integrity (`model-poisoning-reviewer`).

## Inputs to Inspect

1. What the feature asserts and what depends on it: are outputs factual
   claims/advice/decisions, and what's the consequence of a confident error.
2. Grounding today: does it answer from retrieved authoritative sources or from
   model memory; is retrieval present (compose `rag-security-architect`).
3. Citation handling: are sources cited, and does anything check the citation
   actually supports the claim (or are citations themselves hallucinated).
4. Uncertainty/refusal behavior: does the feature ever say "I don't know" or
   signal low confidence, or does it always answer confidently.
5. High-impact paths: outputs that drive money, legal, medical, safety, or
   code-execution decisions — where a hallucination is worst.
6. UX framing: does the interface encourage blind trust (authoritative tone,
   no sourcing, no confidence signal) or support verification.

## Workflow

1. **Classify claims by consequence.** Separate low-stakes generation
   (brainstorming, drafts) from consequential factual claims (advice,
   decisions, code, citations). No feature/output behavior to inspect → Stop
   Conditions. Controls scale with consequence.
2. **Ground consequential claims** using
   [references/grounding-controls.md](references/grounding-controls.md):
   factual answers come from retrieved authoritative sources, not parametric
   memory. Where there's no retrieval and the claim matters, that's a finding —
   add grounding (compose `rag-security-architect` for secure retrieval).
3. **Verify citations.** If the feature cites sources, check that each citation
   exists and actually supports the claim — models fabricate plausible
   citations. Require citation-to-claim checking, not just presence of a
   footnote.
4. **Calibrate uncertainty and enable refusal.** The feature must be able to
   signal low confidence and to decline when evidence is insufficient, rather
   than always producing a confident answer. "I don't know / not enough
   information" is a valid, required output for thin-evidence cases.
5. **Validate consequential facts before they act.** Where an output drives a
   decision or action, the fact is checked (against a source, a deterministic
   lookup, or human review) before it takes effect — compose
   `structured-output-validator` for existence/consistency checks and
   `agent-tool-safety-guard` for the action gate.
6. **Handle package/API hallucination.** For features that suggest
   dependencies, APIs, commands, or config: recommended packages/APIs are
   verified to exist (registry/allowlist) before being surfaced or installed —
   an invented package name is a supply-chain foothold (slopsquatting). Route
   install-time trust to `supply-chain-security-reviewer`.
7. **Design overreliance-aware UX.** Signal confidence, show sources, and mark
   AI-generated content so users can verify rather than blindly trust; for
   high-impact tiers require human review (route oversight tiering to
   `ai-governance-risk-reviewer`).
8. **Design eval cases.** Known-answer factual sets (accuracy), adversarial
   "make it hallucinate" prompts (fabrication rate), citation-support checks,
   and refusal cases (does it decline when it should). Hand to
   `ai-evaluation-harness` (groundedness dimension).

## Output Format

```
AI MISINFORMATION REVIEW/DESIGN — <feature>
Claim consequence tiers: <low-stakes | consequential | high-impact>
Grounding: <memory vs retrieved authoritative source per claim type> (→ rag-security-architect)
Citation verification: <cited? checked-to-support-claim?>
Uncertainty/refusal: <can it signal low confidence / decline on thin evidence?>
Fact validation before action: <source/lookup/human check> (→ structured-output-validator, agent-tool-safety-guard)
Package/API hallucination: <recommended deps verified to exist?> (→ supply-chain-security-reviewer)
Overreliance UX: <confidence signal | sourcing | AI-marking | human review tier> (→ ai-governance-risk-reviewer)
Eval cases: <accuracy | fabrication | citation-support | refusal> (→ ai-evaluation-harness)
Residual risk: <what remains + named acceptor>
```

## Validation Checklist

- [ ] Claims are tiered by consequence; controls scale with impact.
- [ ] Consequential factual claims are grounded in retrieved authoritative
      sources, not model memory; ungrounded consequential claims are flagged.
- [ ] Citations (if used) are verified to exist and support the claim, not
      just present.
- [ ] The feature can signal uncertainty and refuse on thin evidence — it does
      not always answer confidently.
- [ ] Consequential facts are validated before they drive a decision/action.
- [ ] Recommended packages/APIs/commands are verified to exist before being
      surfaced or installed (hallucination → supply-chain foothold).
- [ ] UX signals confidence/sources and routes high-impact outputs to human
      oversight.

## AI Security Rules

- Confident and correct are independent: a fluent, authoritative answer is not
  evidence it's true. Ground consequential claims; don't trust tone.
- Refusal is a feature: "I don't know / insufficient evidence" must be an
  available output — a system that always answers will confidently fabricate.
- Hallucinated dependencies are a security risk: an invented package/API name
  an attacker can register turns a "helpful suggestion" into a supply-chain
  compromise (slopsquatting) — verify existence before recommend/install.
- Consequential facts are validated before they act — a wrong fact that drives
  money/legal/medical/code decisions is gated by a source check or a human.

## Gotchas

- Fabricated citations are worse than none: a made-up but plausible source
  citation manufactures false credibility. Check the citation supports the
  claim; don't just require that one exists.
- Grounding is not automatic from RAG: retrieving documents doesn't force the
  model to answer FROM them — it can still blend in memory. Require the answer
  to be supported by the retrieved context and flag unsupported claims.
- The overreliance trap: the better and more confident the feature gets, the
  more users stop checking — exactly when a rare hallucination does the most
  damage. UX must keep verification easy.
- Package hallucination is exploitable at scale: models repeatedly invent the
  same plausible package names; attackers pre-register them. Verify against the
  registry.
- Not a shape or safety problem: valid JSON (structured-output-validator) that
  renders safely (llm-output-safety-reviewer) can still be entirely false —
  truth is a separate axis.
- Don't over-apply to creative tasks: a brainstorming or fiction feature
  doesn't need citations; scope grounding to consequential factual claims.

## Stop Conditions

- No feature or output behavior is available to review — stop; this skill needs
  concrete claims/consequences to assess.
- A high-impact feature (medical/legal/financial/safety advice) ships ungrounded
  confident answers — flag as blocking and route oversight tiering to
  `ai-governance-risk-reviewer` / `human-approval-boundary`.
- The concern is output handling, output shape, injection, or training-data
  integrity — hand to the owning skill.
- A hallucination is already causing harm in production (a fabricated fact
  acted on, a hallucinated package installed) — route to
  `incident-response-runbook`.

## Supporting Files

- [references/grounding-controls.md](references/grounding-controls.md) — the
  consequence-tiering rubric, grounding and citation-verification patterns,
  uncertainty/refusal design, package/API hallucination checks, overreliance-UX
  guidance, and groundedness eval seeds.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the output & agency
  cluster and against `llm-output-safety-reviewer`, `structured-output-validator`,
  and `model-poisoning-reviewer`.
