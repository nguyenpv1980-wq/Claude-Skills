# AI evaluation harness design

Detail for `ai-evaluation-harness`. Absorbs the AI security test harness
(reconciliation §3). Manual-only: runs spend tokens/money.

## Dataset composition

Three case classes, versioned together:

- **Representative** — sampled from the real input distribution the feature
  serves. This measures whether it does its job. Keep it current with usage.
- **Adversarial / red-team** — injection, jailbreak, data-exfiltration,
  tool-misuse, and disclosure probes. Sourced from `ai-threat-modeler` abuse
  cases, `prompt-injection-defender`'s payload catalog,
  `agent-tool-safety-guard`'s out-of-scope-trigger cases, and
  `rag-security-architect`'s cross-tenant retrieval cases. This measures
  whether it stays safe under attack.
- **Regression** — every past production failure and every fixed bug, frozen
  with its expected correct behavior. This measures whether old failures stay
  fixed.

Each case: `id`, `inputs`, `expected` (assertion or reference), `dimension`,
`source`. Version the dataset; review changes like code.

## Dimensions & thresholds

| Dimension | Grader style | Pass bar example |
|---|---|---|
| Task quality | reference metric / judge | ≥ X% acceptable |
| Schema adherence | deterministic (validate) | 100% parse+conform |
| Safety / refusal | deterministic assertion | 100% refuse disallowed |
| Groundedness | reference / judge + citation check | ≤ X% unsupported claims |
| Injection resistance | deterministic (no side effect / no follow) | 100% SAFE |
| Latency | measured | p95 ≤ budget |
| Cost | measured | ≤ $ budget/run |

Safety, schema, and injection dimensions are pass/fail gates, not averages.

## Grader selection rubric

- **Prefer deterministic** — schema validation, exact/regex assertions,
  "the refund tool was NOT called", "no string matching a secret pattern in
  output". These are reliable and cheap.
- **Reference-based** — compare to a known-good answer (embedding similarity,
  ROUGE/exact for extraction). Good for quality where a reference exists.
- **LLM-as-judge (last resort for subjective quality)** — pin the judge model,
  give it a rubric, calibrate against human labels, and NEVER let it be the
  sole verdict on a safety-critical case. The judge can be prompt-injected by
  the content it grades and rewards fluent wrong answers.

## Security-suite assertion patterns

Assert the SAFE OUTCOME, verifiably:

- **Injection:** the injected instruction was not followed AND no gated side
  effect fired (check the action log, not just the text).
- **Jailbreak:** disallowed content was refused.
- **Exfiltration:** output contains no sensitive/secret/other-tenant data
  (deterministic pattern + known-canary checks).
- **Tool misuse:** the out-of-scope tool call was denied at the deterministic
  boundary (`agent-tool-safety-guard`).
- **Disclosure / prompt leakage:** system prompt / secrets not revealed
  (`system-prompt-leakage-reviewer` canaries).

Use canary tokens: plant a unique marker as a "secret" in context and assert
it never appears in output.

## CI gate design

- **Trigger:** any change to prompt, model/version, retrieval config, provider,
  or the output schema.
- **Blocking:** safety/schema/injection dimensions red = hard block; quality
  below bar = block or review per policy.
- **Report:** per-dimension score, before-vs-after diff against the baseline,
  and tokens/$ spent.
- **Cadence:** because runs cost money, gate on PR-to-AI-paths and/or nightly,
  not every commit. Size dataset to the budget.

## Non-determinism handling

- Sample N times per case; use tolerance bands, not exact equality, for
  stochastic outputs.
- Pin temperature/seed where the provider supports it.
- Distinguish a real regression from noise: a dimension that drops beyond the
  band across samples is a regression; a single-sample blip is not.

## Honesty (decision D3)

There is no shared runner; this harness is per-feature. Report only runs that
actually executed, with real numbers and real spend. Never claim "evals pass"
as a substitute for running them.
