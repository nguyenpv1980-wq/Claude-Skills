# AI Software Engineering & LLM Systems

Skills for AI routers, prompt contracts, safety, evals, RAG, redaction, cost controls, and autonomy.

These are product-agnostic, repeatable Claude skills. They are meant to become executable `SKILL.md` workflows, not one-off prompts.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 281 | AI Router Architecture | P0 | Centralize model calls, provider routing, secrets, cost controls, telemetry, and fallback behavior. |
| 282 | AI Provider Adapter Design | P0 | Wrap providers behind stable internal interfaces to reduce lock-in and isolate provider-specific behavior. |
| 283 | Prompt Contract Design | P0 | Define system instructions, input schema, output schema, refusal behavior, and validation rules. |
| 284 | Structured Output Validation | P0 | Validate AI outputs with schemas and reject malformed, unsafe, or untrusted responses. |
| 285 | AI Human-in-the-Loop Design | P0 | Design review, edit, approve, reject, and audit workflows before AI output becomes system state. |
| 286 | AI Advisory-Only Pattern | P0 | Keep AI recommendations separate from writes unless explicit autonomy is approved. |
| 287 | AI Autonomy Boundary Design | P0 | Define which actions AI can perform automatically, which need confirmation, and which are forbidden. |
| 288 | AI Prompt Injection Defense | P0 | Treat external content as untrusted data that cannot change tools, rules, identity, or access policy. |
| 289 | AI Redaction Pipeline | P0 | Remove secrets, PII, credentials, sensitive columns, and private tenant data before model calls. |
| 290 | AI Cost Guardrail Design | P0 | Apply token caps, model choices, request budgets, tenant quotas, and cost alerts. |
| 291 | AI Usage Telemetry | P1 | Log safe metadata such as model, feature, latency, tokens, estimated cost, error class, and correlation ID. |
| 292 | AI Evaluation Harness | P1 | Evaluate quality, safety, hallucination, schema adherence, refusal behavior, latency, and cost. |
| 293 | AI Golden Dataset Management | P1 | Maintain representative, adversarial, and regression examples for AI features. |
| 294 | AI Regression Testing | P1 | Detect behavior changes after prompt, model, retrieval, provider, or schema updates. |
| 295 | RAG Retrieval Boundary Design | P1 | Scope retrieval by tenant, user, role, document access, retention, and citation requirements. |
| 296 | AI Output Evidence Design | P1 | Show sources, confidence, extracted evidence, trace snippets, and reasoning summary without exposing hidden prompts. |
| 297 | AI Fallback and Degradation | P1 | Design model fallback, cached responses, manual review fallback, disabled states, and user messaging. |
| 298 | AI Rate Limit Handling | P1 | Handle provider limits with retries, backoff, queues, user feedback, and no duplicate side effects. |
| 299 | AI Feature Kill Switch | P1 | Disable provider, model, tenant, or feature behavior quickly during incidents or cost spikes. |
| 300 | AI Safety Review Checklist | P0 | Review data leakage, prompt injection, unsafe writes, hallucination, tool misuse, and cost blowups. |

## Skill implementation standard

When this category is converted into executable skills, each `SKILL.md` should include:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns / stop conditions
