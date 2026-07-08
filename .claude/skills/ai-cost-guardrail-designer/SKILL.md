---
name: ai-cost-guardrail-designer
description: Design cost and consumption guardrails for an LLM feature covering both spend and unbounded-consumption abuse (OWASP LLM10 — denial-of-service and denial-of-wallet) — per-request token caps (input and output), per-user/tenant/plan budgets and cost-aware (token-based, not request-count) rate limits, model selection by task, concurrency and queue limits, loop/recursion bounds for agents, input-size limits, a fail-closed spend kill switch and degraded-mode fallback, and cost/usage telemetry with alerts before the budget is gone. Composes saas-cost-architect for unit economics and observability-operator for the metering. Use when adding budgets/quotas/rate limits to an AI feature, or defending against token-drain, denial-of-wallet, or stolen-key LLMjacking. Do NOT use for whole-product cost modeling (saas-cost-architect), plan feature gating (plan-entitlement-architect), implementing the alerts (observability-operator), or model routing/fallback logic (ai-router-architect).
---

# AI Cost Guardrail Designer

## Purpose

Design the guardrails that keep an LLM feature from becoming a denial-of-wallet
or denial-of-service vector (LLM10) and keep its spend attributable and
bounded. The deliverable is a layered control set: per-request token caps,
per-user/tenant/plan budgets and rate limits, task-appropriate model
selection, concurrency/queue bounds, agent loop limits, input-size limits, a
kill switch, a degraded-mode fallback, and telemetry that alerts BEFORE the
budget is exhausted. Two disciplines run through all of it: every guardrail
must FAIL CLOSED — a cost/rate/budget check that errors DENIES the call, or it
becomes the denial-of-wallet vector it was meant to stop (CWE-636) — and a
STOLEN provider credential (LLMjacking) turns your own account into the
attacker's, so key custody and per-model restriction are in scope. Unit
economics come from `saas-cost-architect` and the metering implementation from
`observability-operator`; key-custody mechanics defer to
`secrets-identity-hardener` and the general fail-closed discipline to
`error-handling-security-reviewer`. This skill composes all four and focuses on
the guardrail design.

## Use When

- Use when: adding token caps, budgets, quotas, rate limits, or concurrency
  limits to an AI feature.
- Use when: defending against unbounded consumption — token-drain,
  denial-of-wallet (attacker makes you spend), context stuffing, agent
  loops, retry storms.
- Use when: a request-count rate limiter is not stopping cost abuse, or a
  stolen/leaked provider key (LLMjacking) could run up your inference bill.
- Use when: an AI feature's cost is unpredictable or a spend spike already
  happened and needs structural controls.
- Do NOT use when: modeling the whole product's cost drivers and unit
  economics — `saas-cost-architect` (this skill composes it for the numbers).
- Do NOT use when: the task is key custody/rotation/storage mechanics —
  `secrets-identity-hardener` (this skill composes it and owns only the
  AI-spend blast radius); or a general fail-closed review of error paths —
  `error-handling-security-reviewer`.
- Do NOT use when: deciding which PLAN includes which feature/limit —
  `plan-entitlement-architect`; implementing alert rules —
  `observability-operator`; or designing model fallback/routing —
  `ai-router-architect` (this skill sets the budget the router enforces).

## Inputs to Inspect

1. The feature's call pattern: how many model calls per user action, input and
   output sizes, whether it's agentic (loops/tool calls multiply cost).
2. Who can trigger inference and how: authenticated vs public endpoints,
   per-request cost, ability to trigger many calls cheaply.
3. Current limits (if any): token caps, rate limits (and whether they count
   REQUESTS or actual token/cost consumed), concurrency, timeouts, input-size
   validation — and where they're missing.
4. Cost model inputs: model prices, `saas-cost-architect` unit economics,
   the budget envelope per tenant/plan.
5. Existing telemetry: what token/cost/latency data is emitted per call and
   whether it's attributable to a user/tenant/feature.
6. Failure behavior: what happens at the limit today — hard error, silent
   drop, unbounded retry, or fail-open (the dangerous default).
7. Provider credential handling: where the key lives (server-only vs
   client-reachable), how narrowly it's scoped (per-model, least-privilege),
   and rotation posture — the LLMjacking surface (custody detail →
   `secrets-identity-hardener`).
8. Provider-account billing controls: whether a hard spend cap and
   billing-anomaly/spike alerts are configured — both are typically optional
   and OFF BY DEFAULT.

## Workflow

1. **Map the consumption surface.** Per user action, count model calls, token
   sizes, tool calls, and any loops. Identify the cheapest way an attacker (or
   a bug) can maximize spend. No feature/call pattern to inspect → Stop
   Conditions.
2. **Set per-request bounds.** Cap input tokens (reject/ truncate oversize
   input) and max output tokens; bound context assembly; set a timeout. An
   uncapped request is an open-ended bill.
3. **Set per-principal budgets and cost-aware rate limits** using
   [references/cost-guardrail-patterns.md](references/cost-guardrail-patterns.md):
   per-user, per-tenant, and per-plan token/spend budgets and rates — limit on
   TOKEN/COST consumed per window, not request COUNT, since one request can
   cost hundreds of times another. Estimate cost before the call (input tokens
   + `max_tokens` as a provisional reservation), then true-up to actual output
   tokens after the response (true cost is only known then). Give each
   tenant/user its own FIFO queue so one can't starve the shared budget.
   Tenant-scoped so one tenant can't exhaust another's capacity
   (noisy-neighbor). Compose `plan-entitlement-architect` for the plan
   dimension.
4. **Bound concurrency and loops.** Concurrency/queue limits per tenant; for
   agents, a hard cap on iterations, tool calls, and recursion depth so a loop
   can't run away. Cap retries with backoff — no unbounded retry storms.
5. **Choose model by task.** Route cheap/simple tasks to smaller models;
   reserve expensive models for where they're needed (design intent handed to
   `ai-router-architect` to enforce). Over-using a frontier model is a
   self-inflicted cost.
6. **Make every guardrail fail closed, and design the kill switch and degraded
   mode.** A switch to disable the feature/model/tenant on a spend spike, and a
   degraded fallback (cached answer, smaller model, queue, or "temporarily
   unavailable") so hitting the limit fails safe. If any cost/rate/budget check
   errors, times out, or its backing store is unreachable → DENY the call,
   never allow it through; a check that fails open turns your own limiter into
   the denial-of-wallet vector (CWE-636). The kill switch inherits the same
   rule: a broken budget-state check ENGAGES it, never disengages. The general
   fail-closed discipline is `error-handling-security-reviewer`'s; this is its
   AI-spend application. Wire confirmed abuse to `incident-response-runbook`.
7. **Add the provider-side backstop.** Application controls are not the last
   line: set a HARD spend cap on the provider account itself (a ceiling that
   stops inference) and billing-anomaly/spike alerts that fire before a large
   invoice lands. Most major LLM providers offer both, but they are usually
   OPTIONAL and OFF BY DEFAULT — an account set up once and never revisited is
   exposed — so the design must explicitly VERIFY they are configured. These
   are config actions the skill FLAGS as verify-at-design-time, not
   architecture it builds.
8. **Protect the provider credential (LLMjacking).** A stolen API key is a
   denial-of-wallet weapon: keys leaked from public repos or CI are exploited
   within minutes and resold cheaply. Hold the key server-side only (never in a
   client bundle or any browser-reachable path), and scope it per-model /
   least-privilege so a leak's cost blast radius is bounded to what that key
   may invoke. Custody, scoping, and rotation MECHANICS are
   `secrets-identity-hardener`'s; this skill owns the AI-specific angle — the
   per-model invocation restriction and the cost blast radius of a leaked key.
9. **Design telemetry, attribution, and alerts.** Per-call emission of model,
   tokens (in/out), estimated cost, tenant/user/feature, latency, and error
   class — attributable. That attribution is what tells a denial-of-wallet
   attacker, a looping agent, and an honest-but-expensive workload apart: they
   look IDENTICAL on the invoice, so don't judge a spike malicious (or benign)
   without it. Alerts fire on budget burn rate BEFORE exhaustion (compose
   `observability-operator` to implement, `slo-reliability-architect` for
   burn-rate thinking). Redact prompt content from cost telemetry; alert on
   tampering with invocation/usage logging itself — disabling cost logging to
   hide activity is a near-certain compromise signal.
10. **State the residual exposure.** The worst-case spend with these guardrails
    in place, and the named acceptor for it via `human-approval-boundary`.

## Output Format

```
AI COST GUARDRAILS — <feature>
Consumption surface: <calls/action, token sizes, loops, cheapest abuse path>
Per-request bounds: <input cap | output cap | context cap | timeout>
Per-principal limits: <user | tenant | plan — token/COST budget + rate, not request-count> (tenant-scoped)
Rate-limit mechanics: <pre-call estimate (input + max_tokens) → post-response true-up | per-tenant FIFO queue>
Concurrency/loops: <concurrency cap | agent iteration/tool/recursion caps | retry policy>
Model selection: <task → model tier> (→ ai-router-architect enforces)
Fail-closed: <check error/timeout/store-down → DENY | kill switch ENGAGES on broken budget-state check> (CWE-636)
Kill switch / degraded mode: <trigger → switch | fallback behavior (fail-safe)>
Provider backstop: <hard spend cap | billing-anomaly alert — configured? (off by default, verify)>
AI credential: <server-side-only | per-model/least-priv scope | logging-tamper alert> (custody → secrets-identity-hardener)
Telemetry & alerts: <per-call metrics, attribution that distinguishes attacker/loop/honest, burn-rate alert> (→ observability-operator)
Residual exposure: <worst-case spend + named acceptor>
```

## Validation Checklist

- [ ] Every request has input and output token caps and a timeout; oversize
      input is rejected/truncated, not silently processed.
- [ ] Rate limits are on TOKEN/COST per window, not request count; cost is
      estimated pre-call and trued-up to actual output post-response, and each
      principal has its own queue so one can't starve the shared budget.
- [ ] Per-user, per-tenant, and per-plan budgets/rate limits exist and are
      tenant-scoped (no cross-tenant exhaustion).
- [ ] Agent loops/tool calls/recursion and retries are hard-bounded.
- [ ] Every cost/rate/budget check FAILS CLOSED — an error, timeout, or
      unreachable store DENIES the call (never allows), and the kill switch
      ENGAGES on a broken budget-state check (CWE-636).
- [ ] A kill switch and a degraded-mode fallback exist; the limit behavior
      fails SAFE (bounded), never fail-open (unbounded).
- [ ] A provider-side hard spend cap and billing-anomaly/spike alerts are
      configured and VERIFIED on (they are optional and off by default).
- [ ] The provider credential is held server-side only, scoped
      per-model/least-privilege, and tampering with invocation/usage logging
      alerts as a compromise signal.
- [ ] Per-call cost telemetry is attributable (tenant/user/feature) so an
      attack, a loop bug, and honest heavy use can be distinguished; prompt
      content is redacted from it.
- [ ] Alerts fire on burn rate BEFORE the budget is exhausted, not after.
- [ ] Worst-case residual spend is stated with a named acceptor.

## AI Security Rules

- Denial-of-wallet is a security risk, not just a finance one: any path where
  an attacker can cheaply trigger expensive inference is a finding (LLM10).
- Every guardrail FAILS CLOSED. If a cost/rate/budget check errors, times out,
  or its store is unreachable, DENY the call — never let it through. A
  guardrail that fails open is not a guardrail: an attacker (or a bug) that can
  force the check to error has disabled your limiter and turned it into the
  denial-of-wallet vector (CWE-636). The kill switch obeys the same rule — a
  broken budget-state check ENGAGES it. `error-handling-security-reviewer` owns
  fail-closed generally; this is its AI-spend application.
- Rate-limit on tokens/cost, not request count. One request can cost hundreds
  of times another (a cache hit vs a multi-step agent run), so a request-count
  limiter lets an attacker drive the most expensive paths while staying under
  it — estimate cost before the call and true-up after.
- A stolen provider key is a denial-of-wallet weapon (LLMjacking). Keys leaked
  from repos or CI are exploited within minutes and resold — hold the key
  server-side only, scope it per-model/least-privilege to bound the blast
  radius, and alert on any tampering with invocation/usage logging (a
  near-certain compromise signal). Custody and rotation are
  `secrets-identity-hardener`'s; this owns the per-model restriction and the
  cost blast radius.
- Attribution decides intent — don't guess without it. A denial-of-wallet
  attacker, a looping agent, and an honest heavy user look identical on the
  invoice; only per-tenant/user/feature attribution tells them apart, so don't
  declare a spike malicious (or benign) until it can.
- Tenant isolation applies to capacity and budget: one tenant (or attacker)
  must not be able to consume another tenant's quota or starve the platform.
- Public/unauthenticated inference endpoints are the highest-risk surface —
  they need the tightest per-IP/per-session caps and a kill switch.

## Gotchas

- Output tokens are the expensive half and the easiest to forget to cap — a
  prompt that says "repeat forever" or a model that rambles runs up the bill.
- Request-count limiters are cost-blind: capping requests/minute does nothing
  when one request (a multi-step agent run) costs hundreds of times another (a
  cache hit) — an attacker just triggers the expensive path while staying under
  the count. Limit on tokens/cost.
- Agent loops multiply: one user action → N iterations × M tool calls ×
  tokens each. Cap the loop, not just the single call.
- Retry storms: a transient provider error plus naive retry-all can double or
  triple spend under load; use bounded retries with backoff and a circuit
  breaker.
- Fail-open is the silent killer: "if the budget check errors, allow the
  request" turns a bug — or an attacker who can force the check to error — into
  unlimited spend, making your own limiter the denial-of-wallet vector
  (CWE-636). Fail closed; defer the general discipline to
  `error-handling-security-reviewer`.
- Provider billing controls are off by default: an account set up years ago
  with no hard spend cap and no billing-anomaly alert is exposed until someone
  turns them on — verify, don't assume.
- A stolen key spends at machine speed: LLMjacking exploits leaked keys within
  minutes, and attackers disable cost logging first — so treat any
  invocation-logging gap or tampering as a compromise signal, not noise.
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
  the kill switch; design follows containment. If a leaked/compromised
  provider key is suspected, treat it as an incident and rotate via
  `secrets-identity-hardener`.
- The ask is really key custody/rotation/storage mechanics
  (`secrets-identity-hardener`) or a general fail-closed review of error paths
  (`error-handling-security-reviewer`) — hand to the owning skill; this skill
  sets the AI-spend requirement, not those mechanics.
- The ask is really plan feature-gating, whole-product cost modeling, alert
  implementation, or router logic — hand to the owning skill.

## Supporting Files

- [references/cost-guardrail-patterns.md](references/cost-guardrail-patterns.md)
  — the layered limit catalog (per-request/per-principal/concurrency/loop),
  cost-aware token-based limiting (estimate + true-up), fail-closed guardrails
  (CWE-636), the provider-side backstop, AI-credential/LLMjacking custody,
  denial-of-wallet abuse paths, fail-safe degraded-mode and kill-switch design,
  and cost-telemetry/attribution requirements.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the AI-platform-ops
  cluster and against `saas-cost-architect`, `plan-entitlement-architect`,
  `observability-operator`, `secrets-identity-hardener` (key custody), and
  `error-handling-security-reviewer` (fail-closed review).
