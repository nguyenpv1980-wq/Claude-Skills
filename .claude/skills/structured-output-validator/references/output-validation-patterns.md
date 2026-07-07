# Structured output validation patterns

Detail for `structured-output-validator`. The model response is untrusted
input; validate it against a contract before any code acts on it.

## Schema-definition patterns

- Use a real schema (JSON Schema, or a typed validator like zod/pydantic/io-ts)
  — not ad-hoc `if (x.field)` checks scattered at call sites.
- Specify per field: type, required vs optional, enum/allowed set, numeric
  min/max, string format/length/pattern, array min/max items, nested shape.
- Decide the unknown-fields policy: reject additional properties where extra
  keys could smuggle state; allow only where forward-compat is needed.
- Version the contract when the feature evolves; treat it like an API contract.

## Validate-before-use

- Parse AND validate on receipt, before reading any field or dispatching any
  action. The anti-pattern this closes: `const x = JSON.parse(resp); doThing(x.action)`
  with no validation between.
- Provider JSON-mode / structured-output / tool-schema constrains generation
  and reduces malformed output — but does NOT guarantee it (truncation,
  refusals, edge cases). Always validate on receipt anyway.

## Semantic validation catalog (beyond shape)

Shape checks types; semantic checks meaning:

- **Value allowlists** — `status` is one of the real statuses, not just "a
  string". `action` is a known action.
- **Tenant-scoped ids** — any id in the output that drives a lookup/action is
  verified to belong to the caller's tenant and to exist. A schema-valid
  `{"account_id": "..."}` can point at another tenant.
- **Cross-field consistency** — `end >= start`; `total == sum(items)`; a
  `type` that implies which other fields must be present.
- **Referential sanity** — referenced entities exist; counts match; no
  dangling ids.
- **Range/bound reality** — quantities, amounts, and limits within
  business-plausible bounds (a refund of $1e9 is shape-valid, semantically
  insane).

## Failure-handling strategies

Pick per use case; never silently coerce:

- **Reject (fail closed)** — safest default; the call errors and the caller
  handles it. Use when acting on bad data is worse than not acting.
- **Bounded repair-retry** — re-prompt the model with the validation error and
  ask for a corrected response, with a hard attempt cap (e.g. 1–2). Prevents a
  cost loop; compose `ai-cost-guardrail-designer` for the budget.
- **Fallback** — return a safe default/degraded response when validation fails
  and the feature can proceed without the model's structured answer.
- **Never:** silently default a missing field, truncate an out-of-range value,
  or partially use an invalid object — that produces confidently wrong behavior.

## Handoffs (shape ≠ safety)

- **To `agent-tool-safety-guard`:** validated tool arguments still need
  authorization — valid shape + wrong permission/tenant = blocked.
- **To `llm-output-safety-reviewer`:** validated output going to a render/
  exec/URL/store sink still needs context-correct encoding — a valid string
  field can hold an XSS payload.
- **To `ai-evaluation-harness`:** the schema-adherence dimension and the
  malformed-response test cases.

## Malformed-response test seeds

Each with expected handling:

- Missing required field → reject.
- Wrong type (number where string expected) → reject.
- Out-of-range / not-in-enum value → reject.
- Extra unexpected fields → reject (where policy is strict).
- Wrong-tenant / nonexistent id → semantic-check reject.
- Empty or truncated response → reject.
- Non-JSON / prose-wrapped ("Sure! {…}") → reject or extract-then-validate.
- Valid shape carrying an injection payload in a string → passes shape; flagged
  for `llm-output-safety-reviewer` at the sink.
