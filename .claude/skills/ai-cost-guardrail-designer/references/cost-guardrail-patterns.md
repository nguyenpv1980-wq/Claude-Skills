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
- **Limit on tokens/cost, not request count.** A request-count limiter is
  cost-blind — one request (a multi-step agent run) can cost hundreds of times
  another (a cache hit), so counting requests lets an attacker drive the
  expensive paths while staying under the cap.
- **Estimate then true-up.** Exact cost is only known after the response.
  Before the call, reserve a provisional cost from input tokens + the
  `max_tokens` cap; after the response, true-up the reservation to the actual
  output tokens and settle the budget.
- **Per-principal FIFO queue.** Give each user/tenant its own queue against the
  shared budget so one principal's burst can't starve everyone else.

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
- A request-count rate limiter that ignores per-request cost (trigger the most
  expensive path while staying under the count).
- A stolen or leaked provider API key driving inference on your account
  (LLMjacking) — see AI credential custody below.
- Any cost/rate/budget check an attacker can force to ERROR if it fails open
  (the limiter becomes the vector — CWE-636).

The cheapest attacker action that maximizes your spend is the thing to bound.

## Fail-safe degraded modes

At a limit, fail SAFE (bounded), never open (unbounded):

- Serve a cached/previous answer.
- Downgrade to a smaller/cheaper model.
- Queue with backpressure and a user-visible "busy, try later".
- Refuse with a clear message and a retry-after.
- NEVER "on budget-check error, allow" — that converts a bug into unlimited
  spend. Budget-check failure denies.

## Fail-closed guardrails (CWE-636)

Every cost/rate/budget check must fail CLOSED: if it errors, times out, or its
backing store is unreachable, DENY the call — never allow it through. A
guardrail that fails open is not a guardrail; an attacker (or a bug) that can
force the check to error has disabled your limiter and turned it into the
denial-of-wallet vector (CWE-636, "Not Failing Securely").

- The kill switch inherits the rule: a broken budget-state check ENGAGES the
  switch, it does not disengage it.
- "Never block a paying customer" is not a reason to fail open — degrade
  (cached / smaller-model / retry-after) instead, which bounds spend without
  allowing unbounded calls.
- The general fail-closed / error-path discipline is
  `error-handling-security-reviewer`'s (OWASP A10); this is its AI-spend-
  specific application.

## Kill switch

- Granularity: disable a feature, a model, a provider, or a single tenant.
- Trigger: manual, or automatic on a burn-rate threshold.
- Must be fast and not require a deploy. Compose `ai-router-architect` /
  `observability-operator` for the plumbing; confirmed abuse →
  `incident-response-runbook`.

## Provider-side backstop

Application controls are not the last line of defense — the provider account
itself needs a backstop:

- **Hard spend cap** — a ceiling on the provider account that STOPS inference,
  independent of your application's budgets.
- **Billing-anomaly / spike alerts** — fire before a large invoice lands, on
  the account's own spend curve.
- Most major LLM providers offer both, but they are typically OPTIONAL and OFF
  BY DEFAULT. An org that set up its account once and never revisited billing
  is exposed by default — the design must explicitly VERIFY they are on.
- Honest scope: these are configuration actions the skill FLAGS as
  verify-at-design-time, not architecture the skill builds.

## AI credential custody (LLMjacking)

A stolen provider key lets an attacker spend on YOUR account. Keys scraped from
public repos, leaked CI logs, or client bundles are exploited within minutes
and resold cheaply.

- **Server-side only** — the key never ships in a client bundle or sits on any
  browser-reachable path.
- **Least-privilege / per-model scope** — restrict what a key can invoke (which
  models, which endpoints) so a leak's cost blast radius is bounded.
- **Short-lived / rotatable** — prefer short-lived scoped credentials; a leaked
  key must be revocable fast.
- **Logging-tampering is a compromise signal** — an attacker disabling or
  tampering with invocation/usage logging to hide spend is a near-certain
  indicator; telemetry must alert on it.
- Custody, storage, classification, and rotation MECHANICS are
  `secrets-identity-hardener`'s. This skill owns the AI-specific slice: the
  per-model invocation restriction and the cost blast radius of a leaked AI
  key.

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
- **Attribution decides intent** — a denial-of-wallet attacker, a looping
  agent, and an honest-but-expensive workload look IDENTICAL on the invoice.
  Per-tenant/user/feature attribution is what tells them apart; do not label a
  spike malicious (or benign) without it.
- **Tamper-alerting** — treat a gap in, or tampering with, invocation/usage
  logging as a compromise signal and alert on it (an attacker disables cost
  logging first).

## Residual exposure

State the worst-case spend that can still occur with all guardrails active
(e.g. every tenant maxes its budget simultaneously), and record the named
human acceptor via `human-approval-boundary`.
