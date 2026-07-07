---
name: ai-evaluation-harness
description: Design and run the evaluation harness for an LLM feature — a versioned dataset (representative, adversarial/red-team, and regression cases), graders per dimension (task quality, schema adherence, safety/refusal, groundedness/hallucination, injection resistance, latency, cost), pass/fail thresholds, and a CI gate that blocks a prompt/model/retrieval/provider change on regression. Absorbs the AI security test harness: injection, jailbreak, data-exfiltration, and tool-misuse suites are first-class dimensions. Running it spends tokens and money, so it is manual-only. Use when building AI evals, a golden dataset, regression gates for AI changes, or encoding red-team cases from ai-threat-modeler / prompt-injection-defender / agent-tool-safety-guard. Do NOT use for the code-change test pyramid (regression-suite-curator / qa-automation-architect), the threat model itself (ai-threat-modeler), or live production monitoring (observability-operator).
disable-model-invocation: true
---

# AI Evaluation Harness

## Purpose

Give an AI feature a repeatable, versioned evaluation harness so quality and
safety are measured, not asserted — and so a prompt, model, retrieval, or
provider change cannot silently regress behavior. The harness pairs a
versioned dataset (representative + adversarial/red-team + regression cases)
with per-dimension graders (task quality, schema adherence, safety/refusal,
groundedness, injection resistance, latency, cost), explicit thresholds, and a
CI gate. It **absorbs the AI security test harness** (reconciliation §3): the
red-team suites produced by `ai-threat-modeler`, `prompt-injection-defender`,
`agent-tool-safety-guard`, and the `ai-security-red-team-reviewer` subagent are
encoded here as first-class safety dimensions. Because executing the suite
sends real requests that **spend tokens and money**, this skill is
**manual-only**.

## Use When

- Use when: building AI evals, a golden/regression dataset, or a CI regression
  gate for an LLM feature.
- Use when: encoding red-team cases from `ai-threat-modeler`,
  `prompt-injection-defender`, `agent-tool-safety-guard`, or
  `rag-security-architect` into a runnable safety suite.
- Use when: a prompt/model/retrieval/provider change needs a before/after
  comparison to prove it didn't regress quality or safety.
- Do NOT use when: designing the code-change test pyramid
  (`qa-automation-architect`) or curating which regression tests belong
  (`regression-suite-curator`) — those are code tests, this is model behavior.
- Do NOT use when: producing the threat model (`ai-threat-modeler`) or
  monitoring live production traffic (`observability-operator`).

## Inputs to Inspect

1. The feature's intended behavior: the task, the success criteria, the
   refusal/safety policy, the output contract (schema from
   `structured-output-validator`).
2. Red-team material to encode: threat-model abuse cases, injection payloads,
   tool-misuse attempts, disclosure probes — from the Phase 7 design skills.
3. Existing evals/datasets, any production failure cases worth freezing as
   regressions, and known-good reference outputs.
4. The change surface the gate protects: which prompt/model/retrieval/provider
   knobs can move and must be re-evaluated.
5. Cost/latency budget for a run (this determines dataset size and CI cadence)
   — compose `ai-cost-guardrail-designer` / `saas-cost-architect`.
6. Grader availability: deterministic checks, reference-based metrics, and
   any LLM-as-judge graders (and their own reliability limits).

## Workflow

1. **Define dimensions and thresholds.** Enumerate what "good" means for this
   feature across quality, schema adherence, safety/refusal, groundedness,
   injection resistance, latency, and cost; set a pass threshold per
   dimension. No feature behavior spec available → Stop Conditions.
2. **Build the versioned dataset** using
   [references/eval-harness-design.md](references/eval-harness-design.md):
   representative cases (the real distribution), adversarial/red-team cases
   (injection, jailbreak, exfiltration, tool-misuse, disclosure), and
   regression cases (every past failure frozen). Version it; each case has an
   id, inputs, and expected behavior/assertion.
3. **Choose graders per dimension.** Prefer deterministic graders (schema
   validation, string/JSON assertions, tool-call-was-denied checks) over
   LLM-as-judge; where a judge is needed, pin its model and calibrate it, and
   record that judges are themselves fallible. Safety graders assert the SAFE
   outcome (refused, denied at the action boundary, no secret emitted).
4. **Encode the security suites.** Injection cases assert the model did not
   follow the injected instruction AND no side effect fired; exfiltration
   cases assert no sensitive data in output; tool-misuse cases assert the
   deterministic boundary blocked the call. These come from the design skills
   — this harness runs them.
5. **Wire the CI gate.** Define which changes trigger a run, the pass/fail
   thresholds that block merge, and the diff report (per-dimension before vs
   after). Gate is manual-triggered or scheduled given the cost; a red safety
   dimension is a hard block.
6. **Run and report (manual, spends money).** Execute the suite, collect
   per-dimension scores, flag regressions against the previous baseline, and
   record token/cost spend of the run. Never claim a run happened that didn't;
   report real numbers.
7. **Maintain the dataset.** New production failures become regression cases;
   stale/duplicate cases are retired with rationale (mirror
   `regression-suite-curator` discipline for the dataset). Dataset changes are
   reviewed like code.

## Output Format

```
AI EVAL HARNESS — <feature>  (manual-only; runs spend tokens/$)
Dimensions & thresholds: <quality|schema|safety/refusal|grounding|injection|latency|cost — pass bar each>
Dataset (versioned <vN>): representative <n> | adversarial <n> | regression <n>
Graders: <dimension → grader type (deterministic / reference / judge) + limits>
Security suites encoded: <injection|jailbreak|exfil|tool-misuse|disclosure — source skill>
CI gate: <trigger, blocking thresholds, diff report, cost cadence>
Run report (if executed): <per-dimension score vs baseline | regressions | tokens/$ spent>
Not run / deferred: <what and why>
```

## Validation Checklist

- [ ] Every dimension has an explicit pass threshold, including safety and
      cost, not just aggregate quality.
- [ ] Dataset is versioned and includes representative, adversarial/red-team,
      AND regression cases; each case has an id and an expected assertion.
- [ ] Deterministic graders preferred; any LLM-as-judge grader is pinned and
      its fallibility recorded.
- [ ] Security suites assert SAFE outcomes (refused / denied / no leak), not
      just "looks fine".
- [ ] CI gate names the triggering changes and the thresholds that block
      merge; a red safety dimension is a hard block.
- [ ] Run reports show real per-dimension scores and token/cost spend; no run
      is claimed that did not execute (decision D3 honesty).
- [ ] Dataset maintenance (add regressions, retire stale) is defined.

## AI Security Rules

- Safety dimensions are pass/fail gates, not advisory scores: an injection or
  exfiltration case that regresses blocks the change.
- Red-team cases assert the SAFE outcome verifiably — that the side effect did
  NOT fire, the secret was NOT emitted — not merely that the text looks safe.
- LLM-as-judge graders are untrusted for safety-critical verdicts unless
  cross-checked deterministically; a judge can be fooled by the same attack.
- Eval inputs may contain live attack payloads — treat the dataset as
  security-sensitive material; do not leak it into training or logs.

## Gotchas

- Evals that only measure average quality miss the tail where safety lives —
  a feature can score 95% helpful and still exfiltrate on the one crafted
  input. Weight adversarial coverage.
- LLM-as-judge is convenient and biased: it rewards fluent wrong answers and
  can be prompt-injected by the content it grades. Pin, calibrate, and
  deterministically cross-check safety verdicts.
- Non-determinism: model outputs vary run to run; use enough samples and
  tolerance bands, and pin temperature/seed where possible, or the gate
  flakes.
- Cost creep: a big dataset × every commit = a real bill. Size the dataset and
  cadence against the budget (`ai-cost-guardrail-designer`); this is part of
  why the skill is manual-only.
- A stale golden set gives false confidence — if the feature evolved and the
  dataset didn't, green means nothing. Maintain it.
- Don't confuse with code tests: 100% passing unit tests say nothing about
  model behavior, and vice versa.

## Stop Conditions

- No behavior spec, success criteria, or output contract exists — stop; an
  eval needs a definition of "good" to grade against.
- Running the suite would spend real tokens/money: this skill is manual-only —
  the run is a human-authorized step, and cost is disclosed first.
- The red-team material hasn't been designed yet — get it from
  `ai-threat-modeler` / `prompt-injection-defender` / `agent-tool-safety-guard`;
  this harness runs suites, it doesn't invent the threat model.
- A run reveals an active safety regression already shipped to production —
  route to `incident-response-runbook`.

## Supporting Files

- [references/eval-harness-design.md](references/eval-harness-design.md) —
  dataset composition (representative/adversarial/regression), grader
  selection rubric, the security-suite assertion patterns, threshold and
  CI-gate design, and non-determinism handling.
- `evals/evals.json` — trigger + behavior cases (this skill's own meta-evals).
- `evals/trigger-evals.json` — discrimination within the AI-platform-ops
  cluster and against `regression-suite-curator`, `qa-automation-architect`,
  `api-contract-test-designer`, and the `ai-security-red-team-reviewer` subagent.
