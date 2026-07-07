---
name: plan-entitlement-architect
description: Turn pricing plans into enforceable entitlements — map plan × feature × limit into an entitlement matrix (boolean features, numeric limits, usage-metered quotas), define one resolution point and a uniform enforcement-point map (UI, API, command paths, background jobs, integrations), specify metering hooks for usage-based limits, and design plan-transition behavior (trial expiry, upgrade, downgrade while over the new limit, cancellation, payment-failure grace) with grandfathering, staged rollout, and rollback for entitlement changes. Use when designing plans and limits, when limits are enforced inconsistently across surfaces (UI blocks but API allows), when adding a usage-metered feature, or when a plan change needs a safe migration for existing tenants. Do NOT use for role-based access — "can this ROLE do X" is authorization-matrix-designer — nor for infrastructure cost modeling (saas-cost-architect) or overall platform structure (saas-platform-architect).
---

# Plan Entitlement Architect

## Purpose

Produce an entitlement system where "what does this tenant get" has exactly
one answer, resolved in one place, enforced identically on every surface, and
changeable without breaking paying customers: an entitlement matrix, a
resolution rule with override precedence, an enforcement-point map, metering
hooks, a plan-transition table, and a grandfathering/rollback plan. The
failure this prevents is the classic one: the UI upsell-blocks a feature the
API happily serves, and limits enforced by scattered constants drift until
nobody knows what the Pro plan actually is.

## Use When

- Use when: defining plans/tiers and the concrete features and limits inside
  each.
- Use when: limits behave differently across surfaces — UI, API, background
  jobs, integrations — or live as scattered constants in code.
- Use when: adding a usage-metered feature (AI credits, storage GB, API
  calls) that needs quota enforcement and metering hooks.
- Use when: changing plans or limits for a live product — the grandfathering
  and rollback question.
- Use when: trial, downgrade, cancellation, or payment-failure behavior is
  undefined ("what happens to their 12 projects on a 3-project plan?").
- Do NOT use when: the gate is a role question — `authorization-matrix-designer`
  owns "can this role do X"; this skill owns "does this plan include X." A
  request touching both keeps the axes separate.
- Do NOT use when: computing what features cost to serve or per-tenant
  margins — `saas-cost-architect` (it consumes this skill's matrix).
- Do NOT use when: deciding pooled-vs-siloed or control-plane structure —
  `saas-platform-architect`.

## Inputs to Inspect

1. Current plan definitions wherever they live: pricing page, billing
   provider config (products/prices), constants in code — divergences among
   these are findings.
2. Existing enforcement sites: limit checks in UI, API, jobs; feature flags
   doing entitlement duty; hardcoded tier conditionals.
3. The tenant model (billing attaches to the tenant; lifecycle states carry
   billing postures — tenant-modeler output).
4. The billing provider's shape: subscription objects, proration behavior,
   webhooks that signal plan changes and payment failures.
5. Usage data availability for metered limits: what is already counted, per
   tenant, and where.
6. Commercial facts from the human: which limits are sales-negotiable
   (custom/enterprise overrides), trial policy, refund/grace expectations.

## Workflow

1. **Inventory features and limits** actually enforced or promised today —
   from code, billing config, and the pricing page. Reconcile divergences
   before designing on top of them (route hard conflicts to
   `source-of-truth-reconciler`).
2. **Type each entitlement**: boolean feature (on/off), numeric limit
   (max N), or usage-metered quota (N per period, requires metering).
   Naming and matrix template in
   [references/entitlement-matrix-template.md](references/entitlement-matrix-template.md).
3. **Build the entitlement matrix**: plan × entitlement, every cell explicit
   — including the Free/trial column and an "internal/staff" column if one
   exists in practice.
4. **Define resolution**: one resolution point answering
   `entitlement(tenant, key)`, with precedence: tenant-specific override >
   plan default > global default. Overrides are data with an owner and an
   expiry policy, not code branches. Per-tenant caching with invalidation on
   plan-change events.
5. **Map enforcement points**: every surface (UI, API, command paths,
   background jobs, integrations) enforces from the same resolution point.
   UI communicates limits; API/service enforces them; jobs and imports count
   against the same quotas — an import that creates 500 records is 500
   creations.
6. **Specify metering hooks** for usage-based entitlements: the counted
   event, where it is emitted, idempotency of counting, period reset
   semantics, and the over-quota behavior (hard stop vs soft warn vs
   overage billing — chosen per entitlement, written down).
7. **Write the plan-transition table**: trial start/expiry, upgrade
   (immediate, prorated?), downgrade — especially over-limit downgrade
   (retain-but-read-only vs block-new vs forced-archive; NEVER silent data
   deletion), cancellation, payment-failure grace and dunning. Each
   transition names its trigger, entitlement effect, data effect, and user
   communication.
8. **Plan migration and rollback for entitlement changes**: grandfathering
   policy (existing tenants keep old terms — for how long?), staged rollout
   (flag-gated, cohort by cohort), monitoring (support tickets,
   conversion), and a rollback that restores prior entitlements without
   data loss. Changes that reduce a live tenant's paid capability route
   through `human-approval-boundary`.

## Output Format

```
ENTITLEMENT DESIGN — <product/scope>
Entitlement inventory: <key — type (boolean/limit/metered) — today's
  enforcement sites — divergences found>
Entitlement matrix: plan × entitlement, every cell explicit
Resolution rule: <one resolution point; precedence override > plan > default;
  cache + invalidation on plan-change events>
Enforcement-point map: <surface → enforcement mechanism → same resolution
  point? — deviations flagged>
Metering hooks: <entitlement — counted event — emission point — idempotency —
  reset — over-quota behavior>
Plan-transition table: <transition — trigger — entitlement effect — data
  effect — communication>
Migration & rollback: <grandfathering policy — staged rollout — monitoring —
  rollback restoring prior entitlements>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every entitlement typed and every matrix cell explicit — no "ask sales"
      cells without an override mechanism behind them.
- [ ] Exactly one resolution point; all surfaces (including jobs, imports,
      integrations) enforce from it — deviations are listed, not hidden.
- [ ] Override precedence defined; overrides are owned, expiring data.
- [ ] Every metered entitlement has an idempotent counting event and defined
      reset + over-quota behavior.
- [ ] Downgrade-over-limit defined without silent data deletion.
- [ ] Payment-failure grace and dunning states map onto the tenant
      lifecycle's billing postures.
- [ ] Entitlement changes have grandfathering, staged rollout, and a tested
      rollback path.
- [ ] No role/permission logic in the matrix — the authorization axis stayed
      with `authorization-matrix-designer`.

## Tenant Isolation Rules

- Entitlements resolve per tenant; caches are keyed per tenant and
  invalidated on that tenant's plan events only.
- Usage counters are tenant-scoped at write time; metering keyed by user id
  alone mis-bills the moment users span tenants.
- Over-quota responses and upsell surfaces never disclose another tenant's
  plan, usage, or existence.

## Gotchas

- Feature flags doing entitlement duty rot fast: flags are for rollout
  (temporary), entitlements are commercial state (permanent). Migrate
  flag-as-plan-gate cases into the matrix.
- The billing provider's webhook lag means plan state and entitlement state
  disagree for minutes — decide which is authoritative during the gap and
  make the resolution point implement it.
- Downgrades are where data loss lawsuits live; over-limit content goes
  read-only or archived, never deleted by a plan change.
- Proration and immediate-vs-period-end effects differ per provider; the
  transition table must match the provider's actual behavior, not the ideal.
- Enterprise "custom plans" implemented as code branches become unqueryable;
  they are override rows in data, or sales will sell what the system can't
  represent.
- Counting non-idempotently (retried job double-counts an API call) burns
  quota trust; metering events carry idempotency keys.

## Stop Conditions

- Plan definitions in code, billing provider, and pricing page conflict and
  no source is authoritative → `source-of-truth-reconciler` before design.
- A change would reduce a live tenant's paid capability or delete/archive
  their data → `human-approval-boundary` with blast radius (how many
  tenants, what they lose).
- Commercial policy is genuinely undecided (trial length, grace period,
  overage pricing) → present options with consequences; do not invent
  pricing policy.
- Asked to implement billing-provider integration in the same pass →
  separate, scoped task (`docs-first-implementer` against the provider's
  current API docs).

## Supporting Files

- [references/entitlement-matrix-template.md](references/entitlement-matrix-template.md) —
  entitlement naming/typing, matrix and transition-table templates, metering
  hook checklist.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against
  `saas-platform-architect` and `saas-cost-architect` (platform/commercial
  cluster) plus the authorization axis.
