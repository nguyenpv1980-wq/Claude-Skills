# AI cost & consumption guardrail patterns

Detail for `ai-cost-guardrail-designer`. OWASP LLM10 (Unbounded Consumption —
DoS and denial-of-wallet), 2025.

## Layered limit catalog

Defense in depth; each layer catches what the last missed.

### Per-request bounds
- **Input token cap** — reject or truncate oversize input BEFORE the call;
  validate input length at the edge.
- **Output token cap** (`max_tokens`) — the expensive half; always set it.
- **Context assembly cap** — bound retrieved-doc count and total context size.
- **Timeout** — a per-call deadline; no call runs unbounded.

### Per-principal budgets & rate limits
- Per-user, per-tenant, per-plan: token budget and/or spend budget per window
  (minute/day/month) and request rate.
- **Tenant-scoped** enforcement: one tenant's usage cannot consume another's
  budget or the shared capacity (noisy-neighbor). Compose
  `plan-entitlement-architect` for the plan dimension and
  `saas-cost-architect` for the numbers.
- Distinguish soft (warn/degrade) and hard (block) limits.

### Concurrency & loops
- Concurrency/queue cap per tenant; global concurrency ceiling.
- **Agent bounds:** max iterations, max tool calls per run, max recursion
  depth — a runaway loop is the biggest agentic cost risk.
- **Retry policy:** bounded retries with exponential backoff + jitter and a
  circuit breaker; never retry-all on provider errors under load.

### Model selection
- Task → model tier: small/cheap model for classification, extraction, simple
  rewrites; frontier model only where quality demands it. Hand the routing
  intent to `ai-router-architect` to enforce.

## Denial-of-wallet abuse paths (check each)

- Public/unauthenticated inference endpoint accepting large inputs.
- "Summarize this URL/file" with no size limit (attacker supplies a huge one).
- Output-length abuse ("repeat X 10000 times").
- Agent loop with no iteration cap triggered by crafted input.
- Retry storm amplification.
- One tenant scripting requests to exhaust shared quota (DoS on other tenants).

The cheapest attacker action that maximizes your spend is the thing to bound.

## Fail-safe degraded modes

At a limit, fail SAFE (bounded), never open (unbounded):

- Serve a cached/previous answer.
- Downgrade to a smaller/cheaper model.
- Queue with backpressure and a user-visible "busy, try later".
- Refuse with a clear message and a retry-after.
- NEVER "on budget-check error, allow" — that converts a bug into unlimited
  spend. Budget-check failure denies.

## Kill switch

- Granularity: disable a feature, a model, a provider, or a single tenant.
- Trigger: manual, or automatic on a burn-rate threshold.
- Must be fast and not require a deploy. Compose `ai-router-architect` /
  `observability-operator` for the plumbing; confirmed abuse →
  `incident-response-runbook`.

## Cost telemetry & attribution

Emit per call: model, input tokens, output tokens, estimated cost, tenant,
user, feature, latency, error class, correlation id. Requirements:

- **Attributable** — every cost ties to a tenant/user/feature for chargeback
  and abuse detection.
- **Redacted** — prompt/response content is NOT in cost telemetry; only
  metadata.
- **Alerting** — burn-rate alerts fire BEFORE exhaustion (e.g. 50%/75%/90% of
  budget, and fast-burn windows), not just at 100%. Compose
  `observability-operator` to implement and `slo-reliability-architect` for
  burn-rate windows.

## Residual exposure

State the worst-case spend that can still occur with all guardrails active
(e.g. every tenant maxes its budget simultaneously), and record the named
human acceptor via `human-approval-boundary`.
