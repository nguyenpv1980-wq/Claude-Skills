---
name: saas-platform-architect
description: Design the end-to-end structure of a multi-tenant SaaS platform — control-plane/data-plane split, per-component tenancy deployment model (pooled, siloed, or mixed), identity architecture, platform capability inventory (onboarding, billing, audit, support, feature flags, analytics), and an incremental rollout/rollback plan — grounded in inspection of the current system first. Use when asked how to structure a SaaS product for multiple tenants, whether to pool or isolate tenants, what belongs in the control plane, or when converting a single-tenant app to multi-tenant. Do NOT use for defining tenant semantics alone (tenant-modeler), plan/entitlement design (plan-entitlement-architect), per-tenant cost modeling (saas-cost-architect), or structural questions with no tenancy dimension (architecture-designer).
---

# SaaS Platform Architect

## Purpose

Produce a platform architecture for a multi-tenant SaaS that is reachable from
the real current system: which components are pooled and which are siloed (and
by what isolation mechanism), what lives in the control plane versus the data
plane, which platform capabilities exist or are missing, and an incremental
rollout plan with a rollback per step. The core discipline is that tenancy is
decided **per component** with a named isolation mechanism — "we're
multi-tenant" is a slogan, not an architecture.

## Use When

- Use when: asked how a product should be structured to serve many tenants —
  a new SaaS, a single-tenant app being converted, or a platform whose tenancy
  grew ad hoc and needs a deliberate shape.
- Use when: deciding pooled vs siloed vs mixed deployment, or what belongs in
  the control plane vs the data plane.
- Use when: a compliance, residency, or enterprise-isolation demand forces a
  deployment-model rethink.
- Do NOT use when: the question is what a tenant *is* — hierarchy, membership,
  lifecycle semantics — that is `tenant-modeler`, and it runs first if the
  tenant model is undefined.
- Do NOT use when: designing plans, limits, or feature gating
  (`plan-entitlement-architect`) or modeling per-tenant cost
  (`saas-cost-architect`).
- Do NOT use when: judging an existing system for cross-tenant leakage — that
  is `tenant-isolation-reviewer`.
- Do NOT use when: the task is whole-stack blast-radius partitioning — each
  partition running its own full stack with cell-by-cell rollout — that is
  `cell-based-architecture-designer`, a heavier partition layered on top of
  this skill's per-component pooled/siloed isolation.

## Inputs to Inspect

1. Current code layout and deployment units — what actually ships together
   (services, workspaces, Dockerfiles, CI jobs), not the diagrammed intent.
2. The tenant model, if one exists (tenant-modeler output or equivalent doc);
   if tenant semantics are undefined, stop and model first.
3. Identity configuration: IdP, session/token shape, where tenant context
   enters a request today.
4. Existing platform capabilities: onboarding flow, billing integration,
   audit logging, support tooling, feature flags, analytics — present, partial,
   or absent.
5. Tenant population facts from the human: expected count, size skew, largest
   tenant's share, compliance/residency demands, enterprise isolation asks.
6. Team topology and operational maturity — a silo-per-tenant model is an
   operational commitment, not just a diagram choice.

## Workflow

1. **Inspect current state first.** Map real components, deploy units, and
   where tenant context currently lives. For greenfield, say so explicitly —
   never pretend to have inspected a system that does not exist.
2. **Pin tenant assumptions.** Tenant count, size skew, residency, compliance,
   enterprise-isolation demands — each unstated one becomes a written
   assumption with risk-if-wrong. These flip deployment models late and
   expensively.
3. **Decide the deployment model per component** — pooled, siloed, or bridge —
   using the catalog in
   [references/platform-deployment-models.md](references/platform-deployment-models.md).
   Every pooled component names its isolation mechanism; every siloed one
   names its provisioning and upgrade story.
4. **Draw the control-plane/data-plane split.** Control plane: tenant
   management, identity, entitlements, billing, feature flags, support,
   platform audit. Data plane: tenant-facing workloads and tenant data. Assign
   every capability to exactly one plane; flag anything that straddles.
5. **Inventory platform capabilities** (onboarding, offboarding, billing,
   audit, support tooling, analytics, feature flags) as present / partial /
   missing, each marked build, buy, or defer.
6. **Define platform-level tenant flows**: onboard (provision → verify →
   activate) and offboard (suspend → export → purge), delegating detailed
   lifecycle semantics to `tenant-modeler`.
7. **Run the tradeoff analysis**: at least two viable platform options
   compared across isolation strength, operability, cost, delivery speed, and
   reversibility. Recommend one; name what would change the recommendation.
8. **Write the rollout plan**: ordered, individually shippable increments from
   current to target, each with a verification step and a rollback. For
   single-tenant conversions, identity and data scoping move first — never the
   UI.

## Output Format

```
SAAS PLATFORM ARCHITECTURE — <product/scope>
Current state (inspected): components, deploy units, where tenant context lives
Tenant assumptions: count, skew, residency, compliance — each with risk-if-wrong
Deployment model (per component): <component — pooled/siloed/bridge — isolation
  mechanism or provisioning story>
Control plane / data plane split: <capability → plane; straddlers flagged>
Capability inventory: <capability — present/partial/missing — build/buy/defer>
Tenant flows: onboard and offboard at platform level
Options considered: <A vs B across isolation, operability, cost, speed, reversibility>
Recommendation: <option + reversal condition>
Rollout plan: <increment → verification → rollback>, order matters
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Current state cites real files/deploy units inspected, or declares
      greenfield explicitly.
- [ ] Every component has a deployment-model decision AND a named isolation
      mechanism (pooled) or provisioning/upgrade story (siloed).
- [ ] Every platform capability is assigned to exactly one plane; no orphans,
      no straddlers left unflagged.
- [ ] Tenant assumptions are written down with risk-if-wrong — especially
      residency and enterprise isolation.
- [ ] At least two options genuinely compared; recommendation names its
      reversal condition.
- [ ] Every rollout increment is individually shippable with a verification
      step and a rollback.
- [ ] No implementation performed — this skill designs; it does not migrate.

## Tenant Isolation Rules

- A pooling decision IS an isolation decision: no component may be marked
  "pooled" without naming the mechanism that keeps tenants apart in it.
- The control plane never reads tenant business data directly; support and
  analytics access is brokered, scoped, and audited — the control plane is
  itself a leak surface.
- Shared infrastructure (queues, caches, search indexes, object storage)
  gets an explicit tenant-scoping statement each; "it's internal" is not one.

## Gotchas

- Pooled-vs-siloed is not one global choice — the common shape is a pooled
  data plane with siloed exceptions for a few large or regulated tenants, and
  a pooled control plane always.
- Residency requirements discovered late invert deployment models; ask about
  them in step 2, not after the design.
- Converting a single-tenant app by "adding a tenant dropdown" scopes the UI
  and nothing else; identity and data scoping are the real conversion.
- A silo-per-tenant model quietly multiplies every migration, upgrade, and
  incident by the tenant count — cost it operationally before recommending.
- The support/admin console is the most common cross-tenant surface; design
  it in the control plane with brokered access from day one.

## Stop Conditions

- Tenant semantics undefined or contested → stop; run `tenant-modeler` first.
- Residency/compliance facts unknown AND they would flip the recommendation →
  ask; do not pick a default silently.
- The design changes the isolation or security posture of a live system →
  route through `human-approval-boundary` before recommending.
- Asked to implement the migration in the same pass → increment 1 becomes a
  separate, scoped task; confirm before touching code.

## Supporting Files

- [references/platform-deployment-models.md](references/platform-deployment-models.md) —
  pooled/siloed/bridge catalog with isolation mechanisms, control-plane
  capability checklist, and single-tenant conversion patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against
  `plan-entitlement-architect` and `saas-cost-architect` (platform/commercial
  cluster).
