# AI router / model-gateway design

Detail for `ai-router-architect`. Manual-only: wires live providers and
credentials.

## Why centralize

Scattered direct SDK calls each reimplement (badly) key handling, retries,
cost tracking, and logging — and each is a place to leak a key or skip a
budget check. One router gives a single choke point for custody, cost,
telemetry, and kill-switch. Keep it focused: routing, credential custody,
telemetry, resilience. Prompt construction, output parsing, and business
logic stay OUT (compose the owning skills) or the router becomes a god object.

## Credential custody patterns

- Keys server-side only, injected from a secret store at runtime; never in the
  client bundle, never in a `VITE_`/`NEXT_PUBLIC_`/other public-prefixed var.
- Verify with a client-bundle-absence check (grep the built `dist/` for the
  key value AND pattern) — compose `secrets-identity-hardener`.
- Per-provider key with least-privilege scope; rotation path documented.
- If the browser must stream, proxy through the server; do not hand the key to
  the client.

## Routing-decision rubric

Select the model per request by:

- **Task type** — classification/extraction/simple rewrite → small model;
  complex reasoning/generation → larger model.
- **Cost tier** — enforce `ai-cost-guardrail-designer`'s task→tier intent.
- **Latency need** — interactive vs batch.
- **Availability** — current provider health / circuit-breaker state.

Make the decision deterministic and log which model was chosen and why
(for cost attribution and debugging).

## Cost & rate enforcement at the choke point

The router applies (from `ai-cost-guardrail-designer`): per-request token
caps, per-tenant/plan budgets, rate limits, concurrency bounds. One
enforcement point means no call site can bypass them. At a limit: degrade or
deny — fail safe. A budget-check ERROR denies (never allows).

## Failure-handling design

- **Retries:** bounded count, exponential backoff + jitter, ONLY for
  idempotent/safe calls. Non-idempotent (side-effecting) calls need an
  idempotency key or no retry.
- **Fallback order:** provider/model fallback list; define quality/cost impact
  of each fallback and SURFACE it in telemetry (silent downgrade hides
  regressions).
- **Circuit breaker:** per provider; open on sustained errors/rate-limits to
  stop retry storms making an outage worse; half-open probe to recover.
- **Degraded response:** define what the caller gets when all providers fail —
  cached answer, smaller-model answer, queue, or explicit "temporarily
  unavailable". Never an unhandled exception or a fail-open path.

## Telemetry contract (per call)

Emit: model, input tokens, output tokens, estimated cost, latency, tenant,
user, feature, error class, correlation id, chosen-route reason, fallback-used
flag. Attributable for chargeback/abuse detection. Redact prompt/response
content — metadata only. Implementation → `observability-operator`.

## Kill switch

- Granularity: provider / model / feature / tenant.
- Runtime config, NO deploy required (a deploy-gated switch is useless mid-
  incident).
- Trigger: manual or burn-rate-automatic (compose `ai-cost-guardrail-designer`).
- Confirmed incident → `incident-response-runbook`.

## Idempotency & side effects

If a routed call triggers an external side effect, retries must not duplicate
it. Carry an idempotency key end-to-end; dedup on it. Compose
`api-event-architect` for the idempotency pattern. This is where "retry made
it send the email twice" bugs live.
