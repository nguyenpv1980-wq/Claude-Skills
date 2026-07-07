---
name: ai-cost-guardrail-designer
description: Design cost and consumption guardrails for an LLM feature covering both spend and unbounded-consumption abuse (OWASP LLM10 — denial-of-service and denial-of-wallet) — per-request token caps (input and output), per-user/tenant/plan budgets and rate limits, model selection by task, concurrency and queue limits, loop/recursion bounds for agents, input-size limits, a spend kill switch and degraded-mode fallback, and cost/usage telemetry with alerts before the budget is gone. Composes saas-cost-architect for unit economics and observability-operator for the metering. Use when adding budgets/quotas/rate limits to an AI feature, or defending against token-drain and denial-of-wallet. Do NOT use for whole-product cost modeling (saas-cost-architect), plan feature gating (plan-entitlement-architect), implementing the alerts (observability-operator), or model routing/fallback logic (ai-router-architect).
---

# AI Cost Guardrail Designer

## Purpose

Design the guardrails that keep an LLM feature from becoming a denial-of-wallet
or denial-of-service vector (LLM10) and keep its spend attributable and
bounded. The deliverable is a layered control set: per-request token caps,
per-user/tenant/plan budgets and rate limits, task-appropriate model
selection, concurrency/queue bounds, agent loop limits, input-size limits, a
kill switch, a degraded-mode fallback, and telemetry that alerts BEFORE the
budget is exhausted. Unit economics come from `saas-cost-architect` and the
metering implementation from `observability-operator` — this skill composes
both and focuses on the guardrail design.

## Use When

- Use when: adding token caps, budgets, quotas, rate limits, or concurrency
  limits to an AI feature.
- Use when: defending against unbounded consumption — token-drain,
  denial-of-wallet (attacker makes you spend), context stuffing, agent
  loops, retry storms.
- Use when: an AI feature's cost is unpredictable or a spend spike already
  happened and needs structural controls.
- Do NOT use when: modeling the whole product's cost drivers and unit
  economics — `saas-cost-architect` (this skill composes it for the numbers).
- Do NOT use when: deciding which PLAN includes which feature/limit —
  `plan-entitlement-architect`; implementing alert rules —
  `observability-operator`; or designing model fallback/routing —
  `ai-router-architect` (this skill sets the budget the router enforces).

## Inputs to Inspect

1. The feature's call pattern: how many model calls per user action, input and
   output sizes, whether it's agentic (loops/tool calls multiply cost).
2. Who can trigger inference and how: authenticated vs public endpoints,
   per-request cost, ability to trigger many calls cheaply.
3. Current limits (if any): token caps, rate limits, concurrency, timeouts,
   input-size validation — and where they're missing.
4. Cost model inputs: model prices, `saas-cost-architect` unit economics,
   the budget envelope per tenant/plan.
5. Existing telemetry: what token/cost/latency data is emitted per call and
   whether it's attributable to a user/tenant/feature.
6. Failure behavior: what happens at the limit today — hard error, silent
   drop, unbounded retry, or fail-open (the dangerous default).

## Workflow

1. **Map the consumption surface.** Per user action, count model calls, token
   sizes, tool calls, and any loops. Identify the cheapest way an attacker (or
   a bug) can maximize spend. No feature/call pattern to inspect → Stop
   Conditions.
2. **Set per-request bounds.** Cap input tokens (reject/ truncate oversize
   input) and max output tokens; bound context assembly; set a timeout. An
   uncapped request is an open-ended bill.
3. **Set per-principal budgets and rate limits** using
   [references/cost-guardrail-patterns.md](references/cost-guardrail-patterns.md):
   per-user, per-tenant, and per-plan token/spend budgets and request rates,
   with tenant-scoped enforcement so one tenant can't exhaust another's
   capacity (noisy-neighbor). Compose `plan-entitlement-architect` for the
   plan dimension.
4. **Bound concurrency and loops.** Concurrency/queue limits per tenant; for
   agents, a hard cap on iterations, tool calls, and recursion depth so a loop
   can't run away. Cap retries with backoff — no unbounded retry storms.
5. **Choose model by task.** Route cheap/simple tasks to smaller models;
   reserve expensive models for where they're needed (design intent handed to
   `ai-router-architect` to enforce). Over-using a frontier model is a
   self-inflicted cost.
6. **Design the kill switch and degraded mode.** A switch to disable the
   feature/model/tenant on a spend spike, and a degraded fallback (cached
   answer, smaller model, queue, or "temporarily unavailable") so hitting the
   limit fails safe, not open. Wire confirmed abuse to
   `incident-response-runbook`.
7. **Design telemetry and alerts.** Per-call emission of model, tokens
   (in/out), estimated cost, tenant/user/feature, latency, and error class —
   attributable. Alerts fire on budget burn rate BEFORE exhaustion (compose
   `observability-operator` to implement, `slo-reliability-architect` for
   burn-rate thinking). Redact prompt content from cost telemetry.
8. **State the residual exposure.** The worst-case spend with these guardrails
   in place, and the named acceptor for it via `human-approval-boundary`.

## Output Format

```
AI COST GUARDRAILS — <feature>
Consumption surface: <calls/action, token sizes, loops, cheapest abuse path>
Per-request bounds: <input cap | output cap | context cap | timeout>
Per-principal limits: <user | tenant | plan — token/spend budget + rate> (tenant-scoped)
Concurrency/loops: <concurrency cap | agent iteration/tool/recursion caps | retry policy>
Model selection: <task → model tier> (→ ai-router-architect enforces)
Kill switch / degraded mode: <trigger → switch | fallback behavior (fail-safe)>
Telemetry & alerts: <per-call metrics, attribution, burn-rate alert> (→ observability-operator)
Residual exposure: <worst-case spend + named acceptor>
```

## Validation Checklist

- [ ] Every request has input and output token caps and a timeout; oversize
      input is rejected/truncated, not silently processed.
- [ ] Per-user, per-tenant, and per-plan budgets/rate limits exist and are
      tenant-scoped (no cross-tenant exhaustion).
- [ ] Agent loops/tool calls/recursion and retries are hard-bounded.
- [ ] A kill switch and a degraded-mode fallback exist; the limit behavior
      fails SAFE (bounded), never fail-open (unbounded).
- [ ] Per-call cost telemetry is attributable (tenant/user/feature) and
      prompt content is redacted from it.
- [ ] Alerts fire on burn rate BEFORE the budget is exhausted, not after.
- [ ] Worst-case residual spend is stated with a named acceptor.

## AI Security Rules

- Denial-of-wallet is a security risk, not just a finance one: any path where
  an attacker can cheaply trigger expensive inference is a finding (LLM10).
- Limits fail safe: at the cap, the feature degrades or refuses — it never
  fails open into unbounded spend.
- Tenant isolation applies to capacity and budget: one tenant (or attacker)
  must not be able to consume another tenant's quota or starve the platform.
- Public/unauthenticated inference endpoints are the highest-risk surface —
  they need the tightest per-IP/per-session caps and a kill switch.

## Gotchas

- Output tokens are the expensive half and the easiest to forget to cap — a
  prompt that says "repeat forever" or a model that rambles runs up the bill.
- Agent loops multiply: one user action → N iterations × M tool calls ×
  tokens each. Cap the loop, not just the single call.
- Retry storms: a transient provider error plus naive retry-all can double or
  triple spend under load; use bounded retries with backoff and a circuit
  breaker.
- Fail-open is the silent killer: "if the budget check errors, allow the
  request" turns a bug into unlimited spend. Fail closed.
- A budget with no pre-exhaustion alert is a post-mortem, not a guardrail —
  alert on burn rate, not just at 100%.
- Blocking legitimate heavy users: guardrails tuned only to attackers can cut
  off a real power user — tier the limits (compose
  `plan-entitlement-architect`), don't just clamp globally.

## Stop Conditions

- No feature or call pattern is available to bound — stop; guardrails need a
  concrete consumption surface.
- The unit economics/budget envelope is undefined — get it from
  `saas-cost-architect`; caps need a number to enforce.
- A spend spike is happening NOW — route to `incident-response-runbook` and
  the kill switch; design follows containment.
- The ask is really plan feature-gating, whole-product cost modeling, alert
  implementation, or router logic — hand to the owning skill.

## Supporting Files

- [references/cost-guardrail-patterns.md](references/cost-guardrail-patterns.md)
  — the layered limit catalog (per-request/per-principal/concurrency/loop),
  denial-of-wallet abuse paths, fail-safe degraded-mode patterns, kill-switch
  design, and cost-telemetry/attribution requirements.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the AI-platform-ops
  cluster and against `saas-cost-architect`, `plan-entitlement-architect`,
  and `observability-operator`.
