---
name: saas-cost-architect
description: Build the cost model for a multi-tenant SaaS — enumerate cost drivers (compute, storage, database, AI tokens, seats, third-party providers, support load), attribute costs to tenants and plans via tenant-tagged usage, compute unit economics (cost per tenant, per seat, per plan tier vs revenue), identify unbounded and variable-cost exposure (AI, egress, storage) and noisy-neighbor risk, and define cost guardrails (quotas, alerts, degradation ladders, per-tenant kill criteria) with a staged rollout and rollback. Use when asked what a tenant or plan actually costs, whether pricing covers cost, which tenants are unprofitable, before launching a feature with variable per-use cost, or when the cloud/AI bill grew and nobody knows which tenants drove it. Do NOT use for designing plan features and limit semantics (plan-entitlement-architect — this skill prices what that one gates), platform structure (saas-platform-architect), or general cloud architecture selection.
---

# SaaS Cost Architect

## Purpose

Produce a cost model that connects the bill to the tenants and plans that
generate it: a driver inventory grounded in real billing data, an attribution
map that says how each driver is tagged back to a tenant, per-plan unit
economics against revenue, named unbounded-cost exposures, and guardrails
with rollout and rollback. The discipline is attribution-or-admission: every
cost is either attributed to tenants by a stated mechanism or explicitly
listed as unattributable overhead — a model that "roughly allocates" the
biggest line item is fiction with a spreadsheet.

## Use When

- Use when: asked what a tenant, seat, or plan actually costs to serve — or
  which tenants are unprofitable at their current plan.
- Use when: validating that pricing covers cost before a launch, a plan
  change, or an enterprise deal ("can we afford this allowance?").
- Use when: launching a feature with variable per-use cost — AI inference,
  storage, egress, third-party API calls — and the exposure is unmodeled.
- Use when: the cloud or AI bill jumped and the question is which tenants,
  features, or plans drove it.
- Use when: designing cost guardrails — quotas, alerts, degradation, kill
  criteria — for expensive paths.
- Do NOT use when: defining what features/limits a plan CONTAINS — that is
  `plan-entitlement-architect`; this skill prices those decisions and feeds
  margin data back.
- Do NOT use when: choosing platform structure or deployment models —
  `saas-platform-architect` (though its pooled/siloed choices set each
  tenant's cost floor).
- Do NOT use when: general infrastructure right-sizing with no tenant/plan
  dimension — that is ordinary cloud engineering, not this skill.
- Do NOT use when: BUILDING the metering pipeline that produces the usage
  numbers — the append-only event table, rate-card versioning, idempotent
  cost entries, additive rollups, and invoice reconciliation are
  `usage-metering-and-cost-attribution-pipeline-designer`; this skill is the
  economic MODEL those numbers feed, not the ETL.

## Inputs to Inspect

1. Real billing data: cloud provider bills, AI provider usage exports,
   third-party invoices — by service, at least 1–3 months. The model is
   built from bills, not list prices.
2. Existing usage/metering data per tenant (plan-entitlement-architect's
   metering hooks, if they exist) and what is NOT yet tenant-tagged.
3. The entitlement matrix and price book: plans, prices, allowances,
   overrides — revenue side of unit economics.
4. Tenant population: count, plan distribution, size skew (the top tenant's
   share of usage), growth.
5. The platform's deployment model (pooled/siloed per component) — silos
   have per-tenant cost floors; pools need attribution keys.
6. Variable-cost feature paths in code: what calls the AI provider, what
   writes to storage, what egresses — and whether those paths carry tenant
   context.

## Workflow

1. **Inventory cost drivers from real bills.** Group by service, mark each
   driver fixed (exists at zero tenants), stepped (scales in chunks), or
   variable (scales per use). No bill available → the model is an estimate
   and is labeled as one (see Stop Conditions).
2. **Define the attribution map**: for each driver, the mechanism that ties
   it to a tenant — tenant-tagged usage events, resource tags, per-tenant
   storage prefixes, metering counters, or proportional allocation with the
   proxy named. Drivers with no mechanism go to the unattributable-overhead
   line, visibly.
3. **Fill attribution gaps worth filling**: specify the missing tenant
   tags/counters (often the same metering hooks
   `plan-entitlement-architect` needs) — a small build list, ranked by the
   dollars it would attribute.
4. **Compute unit economics**: cost per tenant (attributed + overhead
   share), per seat, per plan tier — against revenue per the price book.
   Present distributions, not just averages: the mean tenant is profitable
   in almost every broken model; the P95 tenant is the finding.
5. **Name the exposures**: unbounded variable costs (AI tokens, egress,
   storage growth) with worst-case-per-tenant math; noisy-neighbor cost
   concentration (top tenant's share); allowance arbitrage (plan allowances
   priced below cost at full utilization).
6. **Design guardrails**, proportional to exposure: per-tenant quotas tied
   to entitlements, budget alerts at attribution granularity, degradation
   ladders (cheaper model, throttle, queue) before hard stops, and
   per-tenant kill criteria for pathological cost — each guardrail with an
   owner and a tenant-visible behavior.
7. **Plan rollout and rollback**: guardrails ship observe-only first
   (alert, don't block), thresholds tuned on real distribution, then
   enforce — with a per-guardrail disable path as rollback. Enforcement
   that can degrade a paying tenant's service routes through
   `human-approval-boundary`.
8. **Define the validation loop**: model vs actual bill reconciliation
   monthly; drift beyond a stated tolerance reopens the model. A cost model
   nobody reconciles is decor.

## Output Format

```
SAAS COST MODEL — <product/scope>
Driver inventory: <driver — service — fixed/stepped/variable — monthly $ from
  real bills (or ESTIMATE label)>
Attribution map: <driver → mechanism (tag/counter/prefix/proxy) →
  unattributable overhead listed separately with total>
Attribution build list: <missing tag/counter — dollars it would attribute —
  ranked>
Unit economics: <per plan: revenue vs attributed cost + overhead share;
  distribution incl. P95 tenant; unprofitable tenants named by criteria>
Exposures: <unbounded drivers with worst-case math; noisy-neighbor
  concentration; allowance arbitrage>
Guardrails: <guardrail — threshold — behavior (alert/degrade/stop) —
  tenant-visible effect — owner>
Rollout & rollback: <observe-only → tune → enforce; per-guardrail disable;
  approval gates for service-degrading enforcement>
Validation loop: <reconciliation cadence, tolerance, reopen trigger>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Drivers come from real bills, or every affected number carries an
      ESTIMATE label — no silent list-price math.
- [ ] Every driver has an attribution mechanism or sits visibly in
      unattributable overhead; overhead is bounded and stated.
- [ ] Unit economics show distributions (incl. P95/top tenants), not only
      averages.
- [ ] Every variable-cost driver has worst-case-per-tenant math and a
      guardrail decision (including "accepted, no guardrail" as an explicit
      choice).
- [ ] Guardrails have owners, tenant-visible behaviors, observe-only
      rollout, and a disable path.
- [ ] The reconciliation loop exists with a cadence and tolerance.
- [ ] No plan/limit semantics were redesigned here — margin findings are
      handed to `plan-entitlement-architect`, not silently patched into
      entitlements.

## Tenant Isolation Rules

- Cost attribution rides on tenant-tagged usage; counters keyed by user
  alone mis-attribute the moment users span tenants.
- Tenant-facing cost/usage dashboards show only that tenant's data; internal
  cost dashboards that rank tenants by name are access-controlled like the
  sensitive data they are.
- Guardrail enforcement messages never disclose other tenants' usage,
  thresholds, or existence ("capacity" wording, not "tenant X used it all").

## Gotchas

- Shared-infrastructure allocation by tenant count flatters heavy tenants;
  allocate by a usage proxy (requests, rows, storage) and name the proxy.
- AI costs are input+output tokens times the model actually invoked —
  fallbacks and retries included; per-request averages hide retry storms.
- The most expensive tenant is routinely on a legacy/discounted plan with a
  grandfathered allowance — check overrides, not just list plans.
- Free-tier and trial cost is a real driver; leaving it out of the model
  makes conversion economics look better than they are.
- Hard-stop guardrails on paying tenants convert a cost problem into a churn
  problem; degradation ladders first, stops last, humans in the loop for
  enterprise tenants.
- Reserved-instance/committed-use discounts distort marginal-cost math; use
  marginal rates for "what does one more tenant cost."

## Stop Conditions

- No billing or usage data is accessible → produce only a labeled-estimate
  model with the data-access request list; do not present estimates as
  measurements.
- A guardrail would degrade or cut off a paying tenant's service →
  `human-approval-boundary` with the tenant impact before enforcement ships.
- Unit economics reveal pricing is underwater at scale → that is a
  commercial decision; present the math and options
  (`plan-entitlement-architect` for the entitlement side), do not quietly
  redesign plans.
- Attribution requires new tracking of user-level behavior with privacy
  implications → surface the privacy question before specifying the
  tracking.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against
  `saas-platform-architect` and `plan-entitlement-architect`
  (platform/commercial cluster).
- No references/ — the driver, attribution, and guardrail tables above are
  the complete procedure; detail lives in the output artifacts.
