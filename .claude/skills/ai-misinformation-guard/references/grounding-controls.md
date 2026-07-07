# Grounding & anti-misinformation controls

Detail for `ai-misinformation-guard`. OWASP LLM09 (Misinformation), 2025.
Truth is a separate axis from shape (`structured-output-validator`) and safety
(`llm-output-safety-reviewer`).

## Consequence-tiering rubric

Controls scale with what a confident error would cost:

| Tier | Examples | Control level |
|---|---|---|
| Low-stakes generation | brainstorming, drafts, fiction, tone | minimal; grounding not required |
| Consequential factual | answers, advice, summaries acted on | grounding + uncertainty + citation |
| High-impact | medical/legal/financial/safety advice, decisions, code that runs | grounding + validation before action + human oversight |

Scope grounding to consequential/high-impact — don't force citations on
creative tasks.

## Grounding patterns

- Answer factual claims from RETRIEVED authoritative sources, not the model's
  parametric memory. Compose `rag-security-architect` for secure retrieval.
- Retrieval alone is not grounding: the model can still blend memory with
  retrieved context. Require the answer to be SUPPORTED by the retrieved
  context; detect/flag claims not supported by any source.
- Where no authoritative source exists for a consequential claim, prefer
  refusal/uncertainty over a memory-based guess.

## Citation verification

- If citations are shown, verify each: it exists AND it supports the specific
  claim. Models fabricate plausible-looking citations — presence is not
  support.
- Prefer linking to the retrieved chunk actually used, so the citation is
  traceable to context, not invented post-hoc.
- Don't let citation UX manufacture false credibility for an ungrounded answer.

## Uncertainty & refusal

- The feature MUST be able to output "I don't know / insufficient evidence"
  and to signal low confidence — a system tuned to always answer will
  confidently fabricate on thin evidence.
- Calibrate: low retrieval support / conflicting sources / out-of-scope query
  → hedge or refuse, don't assert.
- Expose confidence honestly; avoid uniformly authoritative tone.

## Fact validation before action

- Where an output drives a decision or side effect, validate the consequential
  fact first: against a source, a deterministic lookup, or human review.
- Compose `structured-output-validator` for existence/consistency checks (does
  the referenced id/entity exist?) and `agent-tool-safety-guard` for the
  action gate.

## Package / API hallucination (slopsquatting)

- Features that recommend dependencies, APIs, commands, or config can invent
  names that don't exist — and models invent the SAME plausible names
  repeatedly, which attackers pre-register (slopsquatting).
- Verify every recommended package/API/command exists against a registry/
  allowlist BEFORE surfacing or (worse) installing it.
- Route install-time trust to `supply-chain-security-reviewer`.

## Overreliance-aware UX

- Signal confidence and show sources so users can verify.
- Mark AI-generated content (transparency; ties to `ai-governance-risk-reviewer`
  disclosure).
- For high-impact tiers, require human review before the output is acted on;
  the better the feature gets, the more users stop checking — keep verification
  easy exactly when a rare hallucination is most damaging.

## Groundedness eval seeds (→ ai-evaluation-harness)

- Known-answer factual set → accuracy score.
- Adversarial "make it state a confident falsehood" prompts → fabrication rate.
- Citation-support check → cited source actually backs the claim.
- Thin-evidence / unanswerable prompts → does it refuse/hedge instead of
  fabricating.
- Package-recommendation prompts → recommended names all exist.
