---
name: ai-router-architect
description: Design the centralized model-routing layer all AI calls flow through — one internal interface in front of every provider/model so credentials live server-side only (never in the client bundle), routing picks the model by task/cost/availability, per-call telemetry is emitted, and budgets/rate limits from ai-cost-guardrail-designer are enforced at the choke point, with failure handled by retries/backoff, provider fallback, degraded responses, and a kill switch. Composes secrets-identity-hardener for key custody and observability-operator for telemetry. Because it wires live providers/credentials, it is manual-only. Use when building or refactoring the AI provider/routing/gateway layer, adding a provider, or centralizing scattered model calls. Do NOT use for the cost policy itself (ai-cost-guardrail-designer), telemetry implementation (observability-operator), output schema (structured-output-validator), or prompt/injection design (prompt-injection-defender).
disable-model-invocation: true
---

# AI Router Architect

## Purpose

Design the single layer every model call flows through, so the AI system has
one place to enforce credential custody, model selection, cost controls,
telemetry, and failure handling — instead of scattered SDK calls each doing
their own thing. The deliverable: an internal routing interface in front of
all providers/models; server-side-only credentials; routing by task/cost/
availability; a per-call telemetry contract; enforcement of the budgets and
rate limits `ai-cost-guardrail-designer` defines; and resilient failure
handling (retry/backoff, provider fallback, cached/degraded responses, kill
switch). This skill **wires live providers and credentials**, so it is
**manual-only**. It composes `secrets-identity-hardener`, `observability-operator`,
and `ai-cost-guardrail-designer` rather than redoing their work.

## Use When

- Use when: building or refactoring the AI provider/routing/gateway layer, or
  centralizing model calls that are currently scattered across the codebase.
- Use when: adding a new provider/model and needing routing, fallback, and
  key custody for it.
- Use when: the system needs one choke point to enforce cost, telemetry, and
  kill-switch behavior across all AI calls.
- Do NOT use when: defining the cost/quota POLICY — `ai-cost-guardrail-designer`
  (this skill enforces it at the router).
- Do NOT use when: implementing the telemetry/alerts (`observability-operator`),
  validating output shape (`structured-output-validator`), or designing prompt/
  injection defenses (`prompt-injection-defender`).

## Inputs to Inspect

1. Current model-call sites: where the codebase calls providers today, whether
   keys are server-side, and how much logic is duplicated per call site.
2. Provider/model inventory: which providers and models, their pricing tiers,
   rate limits, and failure modes.
3. Credential handling: where API keys live now — a key in the client bundle
   or a public env var is a top finding (compose `secrets-identity-hardener`).
4. Cost/rate policy: the budgets, caps, and model-tier intent from
   `ai-cost-guardrail-designer` this layer must enforce.
5. Telemetry needs: the per-call metrics contract from
   `observability-operator` / `saas-cost-architect` (attribution).
6. Resilience requirements: acceptable degraded behavior when a provider is
   down or rate-limited; idempotency needs for retried calls.

## Workflow

1. **Inventory call sites and consolidate.** Find every place the code calls a
   model; design the single internal interface they will all route through.
   Scattered direct SDK calls are the anti-pattern this fixes. No call sites/
   provider design to inspect → Stop Conditions.
2. **Lock credential custody.** All provider keys server-side only, injected
   at runtime, never in the client bundle or a `VITE_`/`NEXT_PUBLIC_` var.
   Verify with a client-bundle-absence check (compose
   `secrets-identity-hardener`). Per-provider key rotation path.
3. **Design routing** using
   [references/ai-router-design.md](references/ai-router-design.md): select
   model by task type, cost tier, latency need, and availability. Encode the
   `ai-cost-guardrail-designer` model-tier intent (cheap model for simple
   tasks). Routing decisions are deterministic and logged.
4. **Enforce cost and rate limits at the choke point.** The router is where
   per-request token caps, per-tenant/plan budgets, rate limits, and
   concurrency bounds are applied — one enforcement point for all calls.
   Fail safe at the limit (degrade/deny), never fail open.
5. **Emit the telemetry contract.** Every call emits model, tokens (in/out),
   estimated cost, latency, tenant/user/feature, error class, and correlation
   id — attributable, with prompt content redacted. Hand implementation to
   `observability-operator`.
6. **Design failure handling.** Bounded retries with backoff and jitter (only
   for idempotent/safe calls); provider/model fallback order; cached or
   degraded responses when all providers fail; a circuit breaker per provider.
   Define what "degraded" returns to the caller.
7. **Design the kill switch.** Disable a provider, a model, a feature, or a
   tenant fast without a deploy — for incidents or cost spikes. Wire confirmed
   incidents to `incident-response-runbook`.
8. **Handle idempotency and side effects.** Retries must not duplicate
   side-effecting calls; carry an idempotency key where a call triggers an
   external effect (compose `api-event-architect` for the pattern).

## Output Format

```
AI ROUTER DESIGN — <system>  (manual-only; wires live providers/credentials)
Call-site consolidation: <scattered sites → single interface>
Credential custody: <server-side only proof | rotation> (→ secrets-identity-hardener)
Routing: <task/cost/latency/availability → model tier> (deterministic, logged)
Cost/rate enforcement: <caps/budgets/rate/concurrency at the choke point> (→ ai-cost-guardrail-designer)
Telemetry contract: <per-call metrics, attribution, redaction> (→ observability-operator)
Failure handling: <retry/backoff (idempotent only) | fallback order | degraded response | circuit breaker>
Kill switch: <granularity, no-deploy, trigger> (→ incident-response-runbook)
Idempotency: <key/dedup for side-effecting calls> (→ api-event-architect)
Residual risk: <what remains + named acceptor>
```

## Validation Checklist

- [ ] All model calls route through one internal interface; scattered direct
      SDK calls are consolidated.
- [ ] Provider credentials are server-side only with a client-bundle-absence
      proof and a rotation path.
- [ ] Routing selects model by task/cost/availability deterministically and
      logs the decision.
- [ ] Cost/rate/concurrency limits are enforced at the router and fail safe.
- [ ] Per-call telemetry is attributable and redacts prompt content.
- [ ] Failure handling covers bounded retries (idempotent only), provider
      fallback, degraded responses, and a per-provider circuit breaker.
- [ ] A no-deploy kill switch exists at provider/model/feature/tenant
      granularity.
- [ ] Retries cannot duplicate side-effecting calls (idempotency key).

## Security Rules

- Provider credentials are server-side only — a key reachable from the client
  bundle is a critical finding, not a convenience (compose
  `secrets-identity-hardener`).
- The router is a security choke point: budget, rate, and kill-switch
  enforcement live here so no call site can bypass them.
- Failure fails safe: a provider outage or budget-check error degrades or
  denies; it never falls open into uncapped spend or an unauthenticated path.
- Telemetry must not log prompts/responses containing secrets or PII — emit
  metadata, redact content.

## Gotchas

- The client-side key leak is the classic AI-router failure: calling the
  provider straight from the browser to "avoid a backend hop" ships the key to
  every user. Always route server-side.
- Retrying non-idempotent calls doubles side effects — a retried "send email"
  or a tool call fires twice. Retry only safe calls; use idempotency keys.
- Fallback can leak quality/cost silently: falling back to a cheaper model on
  every timeout can degrade output without anyone noticing — surface fallback
  in telemetry.
- One provider's rate limit becoming your outage: without a circuit breaker,
  retry storms against a limited provider make it worse. Break the circuit.
- A kill switch that needs a deploy is not a kill switch during an incident —
  make it runtime config.
- Centralizing is the point, but a god-object router that also does prompt
  construction, output parsing, and business logic becomes unmaintainable —
  keep it to routing/custody/telemetry/resilience; compose the rest.

## Stop Conditions

- No call sites or provider design exist to route — stop; this skill
  consolidates a concrete implementation.
- The layer wires live providers/credentials: this skill is manual-only —
  propose the design/diff; applying it is a classified, approved step
  (`human-approval-boundary`).
- A provider key is found in the client bundle or a public var — flag as a
  blocking finding and route rotation through `secrets-identity-hardener`.
- The ask is really the cost policy, telemetry implementation, output schema,
  or injection design — hand to the owning skill.

## Supporting Files

- [references/ai-router-design.md](references/ai-router-design.md) — the
  routing-decision rubric, credential-custody patterns, failure-handling and
  circuit-breaker design, the per-call telemetry contract, and kill-switch
  granularity.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the AI-platform-ops
  cluster and against `ai-cost-guardrail-designer`, `observability-operator`,
  and `secrets-identity-hardener`.
