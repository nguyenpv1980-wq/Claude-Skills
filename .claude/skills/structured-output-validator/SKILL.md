---
name: structured-output-validator
description: Design the schema and validation strategy for an LLM's structured output so downstream code never trusts an unvalidated model response — define the output contract (JSON Schema / typed shape with required fields, types, enums, ranges, formats), validate every response against it BEFORE use, and specify failure handling (reject, repair-and-retry with bounded attempts, or fall back) plus semantic checks beyond shape (values in allowed sets, ids tenant-scoped, referential sanity). Shape-valid is not safe-to-act: validated output still passes to llm-output-safety-reviewer for sinks and agent-tool-safety-guard for tool authorization. Use when a model returns JSON/structured data an app parses, or to make an AI output contract enforceable. Do NOT use for injection/execution sinks (llm-output-safety-reviewer), tool permissions (agent-tool-safety-guard), factual accuracy (ai-misinformation-guard), or the routing layer (ai-router-architect).
---

# Structured Output Validator

## Purpose

Make an LLM's structured output safe for code to consume by treating the model
response as untrusted input that must conform to an explicit contract before
anything acts on it. The deliverable is: the output schema (required fields,
types, enums, ranges, formats), the validate-before-use strategy, the failure
handling (reject / bounded repair-retry / fallback), and the semantic checks
that shape validation alone misses (value allowlists, tenant-scoped ids,
referential sanity). Crucially, shape-valid ≠ safe-to-act: this skill hands
validated output onward to `llm-output-safety-reviewer` (sinks) and
`agent-tool-safety-guard` (tool authorization), which own the harm-prevention
half.

## Use When

- Use when: a model returns JSON or other structured data that application
  code parses and acts on.
- Use when: defining an enforceable output contract for an AI feature so
  malformed/unexpected responses can't crash or mislead downstream logic.
- Use when: the model output becomes function/tool arguments and the shape
  must be guaranteed before dispatch.
- Do NOT use when: the concern is what happens at an injection/execution sink
  (`llm-output-safety-reviewer`) or the tool-permission boundary
  (`agent-tool-safety-guard`) — this skill guarantees SHAPE, they guarantee
  SAFETY.
- Do NOT use when: the concern is whether the content is TRUE
  (`ai-misinformation-guard`) or the provider/routing layer
  (`ai-router-architect`).

## Inputs to Inspect

1. What downstream code does with the output: fields it reads, actions it
   drives, assumptions it makes (a missing field that throws, an enum it
   switches on).
2. The current parsing: is the response `JSON.parse`d and used directly, or
   validated against a schema first (the former is the gap).
3. The output contract if any: existing schema/types, or the implicit shape
   the code expects.
4. Semantic constraints: which values are actually allowed (status enums,
   id formats), tenant scoping of any ids, cross-field/referential rules.
5. Provider capabilities: native structured-output / JSON-mode / tool-schema
   support that can constrain generation (helpful but not sufficient).
6. Failure tolerance: can the call fail closed (reject) or does it need a
   repair/fallback path; latency/cost budget for retries.

## Workflow

1. **Define the output contract.** Specify the schema: required vs optional
   fields, types, enums, numeric ranges, string formats/lengths, array bounds,
   nesting. Make "what the code assumes" explicit and enforceable. No
   downstream usage/contract to inspect → Stop Conditions.
2. **Validate before use, always.** Every model response is parsed AND
   validated against the schema before any field is read or acted on. Direct
   use of `JSON.parse` output without validation is the finding this closes.
   Use provider JSON-mode/tool-schema to constrain generation, but STILL
   validate — provider modes reduce, not eliminate, malformed output.
3. **Add semantic validation beyond shape** using
   [references/output-validation-patterns.md](references/output-validation-patterns.md):
   values in allowed sets (not just "is a string"), ids that exist and are
   tenant-scoped to the caller, cross-field consistency, referential sanity.
   A schema-valid response can still carry a wrong-tenant id.
4. **Specify failure handling.** On validation failure choose per use case:
   reject (fail closed — safest), bounded repair-retry (re-prompt with the
   error, capped attempts to avoid a cost loop), or fallback (default/degraded
   response). Never silently coerce or partially use invalid output.
5. **Guard the tool-argument case.** When output becomes tool/function
   arguments, validation is the precondition to dispatch — but authorization
   is still `agent-tool-safety-guard`'s job (valid shape, wrong permission =
   still blocked). State the handoff.
6. **Hand off the safety half.** Validated output going to a render/exec/URL/
   store sink goes to `llm-output-safety-reviewer` — shape validity does not
   sanitize an XSS payload in a string field. Make the handoff explicit.
7. **Design the validation tests.** Cases: missing required field, wrong type,
   out-of-range/enum value, extra/unexpected fields, wrong-tenant id, empty/
   truncated response, non-JSON text — each with the expected handling. Hand
   to `ai-evaluation-harness` for the schema-adherence dimension.

## Output Format

```
STRUCTURED OUTPUT CONTRACT — <feature>
Schema: <fields: required/type/enum/range/format | nesting | array bounds>
Validate-before-use: <where validation runs, before which action>
Semantic checks: <value allowlists | tenant-scoped ids | cross-field/referential>
Failure handling: <reject | bounded repair-retry (cap) | fallback> per case
Provider constraint: <JSON-mode/tool-schema used — still validated>
Handoffs: sinks → llm-output-safety-reviewer | tool args → agent-tool-safety-guard
Validation tests: <malformed cases → expected handling> (→ ai-evaluation-harness)
Residual risk: <what remains + named acceptor>
```

## Validation Checklist

- [ ] The output contract is explicit: required fields, types, enums, ranges,
      formats — matching what downstream code assumes.
- [ ] Every response is validated against the schema BEFORE any field is used;
      no direct use of parsed-but-unvalidated output.
- [ ] Semantic checks beyond shape are present (value allowlists, tenant-scoped
      ids, referential sanity).
- [ ] Failure handling is defined per case and never silently coerces or
      partially uses invalid output; repair-retry is bounded.
- [ ] Tool-argument outputs are validated pre-dispatch, with authorization
      explicitly handed to `agent-tool-safety-guard`.
- [ ] Sink-bound validated output is explicitly handed to
      `llm-output-safety-reviewer` (shape ≠ safety).
- [ ] Validation test cases cover missing/wrong-type/out-of-range/extra/
      wrong-tenant/truncated/non-JSON responses.

## AI Security Rules

- Model output is untrusted input: validate against a contract before use, the
  same way you'd validate an external API response or user input.
- Shape validity is necessary, not sufficient: a schema-valid response can
  carry an XSS payload (→ `llm-output-safety-reviewer`) or a wrong-tenant id
  (semantic check + `agent-tool-safety-guard`).
- Fail closed by default: reject invalid output; repair-retry is bounded to
  avoid a cost/latency loop; never partially act on an invalid response.
- Provider JSON-mode is a generation aid, not a validator — always validate
  on receipt.

## Gotchas

- "It's usually valid JSON" is where the outage lives: the one truncated or
  prose-wrapped response ("Sure! Here's the JSON: …") crashes an unvalidated
  parser. Validate every time.
- Schema-valid but semantically wrong is the subtle bug: `{"tenant_id":"other"}`
  passes a string check and leaks across tenants — validate values, not just
  types.
- Repair-retry loops burn money: re-prompting on every failure without a cap
  turns a bad response into a spend spike (compose
  `ai-cost-guardrail-designer`).
- Coercion hides failures: silently defaulting a missing field or truncating
  an out-of-range number produces confidently wrong behavior. Reject instead.
- Extra fields can smuggle: a response with unexpected keys the code later
  spreads into an object can inject state. Reject unknown fields where it
  matters.
- Shape validation is not output-handling: passing validation does NOT mean
  the string is safe to render or execute — that's a separate skill.

## Stop Conditions

- No downstream usage or output contract is available — stop; the schema is
  defined by what the code needs, which must be known.
- Validation would need to run inside application code and this is a design
  handoff — propose the contract and strategy; wiring it is a normal
  (classified) implementation step.
- The real concern is a sink (render/exec), tool authorization, factual
  accuracy, or routing — hand to the owning skill.
- Validated output is still driving harm because a sink trusts it — that's
  `llm-output-safety-reviewer`; route it there.

## Supporting Files

- [references/output-validation-patterns.md](references/output-validation-patterns.md)
  — schema-definition patterns, the semantic-validation catalog (allowlists,
  tenant-scoped ids, referential checks), failure-handling strategies with
  bounded repair-retry, and the malformed-response test seeds.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the output & agency
  cluster and against `llm-output-safety-reviewer` and `api-contract-test-designer`.
