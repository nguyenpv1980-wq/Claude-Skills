---
name: cell-based-architecture-designer
description: Design cell-based (blast-radius) partitioning for a multi-tenant SaaS — a cell is a self-contained stack subset (compute + data + cache + queue) that serves a subset of tenants end to end, so a failure, bad deploy, or noisy tenant is contained to ONE cell instead of the whole fleet: cell definition, tenant→cell mapping and placement policy, a thin cell-router, cell-by-cell deployment/canary, cross-cell/global concerns, and cell migration/rebalancing. SCALE-STAGE — most SaaS never needs it; recommend cells ONLY when blast-radius reduction is the dominant lever, otherwise say so and stop. Use when a single shared stack's blast radius is the unacceptable risk or you need per-cell deployment isolation. Do NOT use for per-component pooled/siloed isolation of one store (saas-platform-architect), choosing the architecture STYLE (architecture-advisor, whose menu omits cells), or agent blast-radius (agent-containment-reviewer).
---

# Cell-Based Architecture Designer

## Purpose

Partition a platform into **cells** — self-contained stack subsets, each with
its own compute, primary data, cache, queue, and workers, each serving a
subset of tenants end to end — so that a failure, a bad deploy, or a noisy
tenant is contained to the blast radius of ONE cell instead of the whole
fleet. This is a **scale-stage** pattern: most SaaS never needs it, and the
first job of this skill is to say so honestly. The deliverable, when cells are
warranted, is a cell definition, a tenant→cell mapping with a placement
policy, a thin cell-router, a cell-by-cell deployment/canary plan, an
enumeration of cross-cell/global concerns, and a cell migration/rebalancing
runbook. The load-bearing property is containment: nothing a single tenant or
a single cell does should be able to take down another cell.

## Use When

- Use when: a single shared stack's blast radius is the unacceptable risk —
  one incident, one bad migration, or one hot tenant currently degrades ALL
  tenants at once, and that shared fate is the dominant problem.
- Use when: you need per-cell deployment isolation — canary a change to one
  cell of tenants and halt before it reaches the fleet.
- Use when: a shared stack has hit a real ceiling (connection limits,
  regional isolation, per-region residency) that per-component pooling or
  siloing of a single store cannot fix.
- Do NOT use when: the need is per-COMPONENT isolation of ONE store or
  service for one tenant tier (pooled vs siloed vs bridge) — that is
  `saas-platform-architect`; whole-stack cells are a far heavier hammer.
- Do NOT use when: the question is which architecture STYLE to build
  (monolith / modular monolith / microservices / event-driven) — that is
  `architecture-advisor`, whose style menu OMITS cells; it picks the
  paradigm, this skill partitions the chosen paradigm into cells.
- Do NOT use when: the blast radius in question is an AGENT's authority or
  failure propagation across an agent network — that is
  `agent-containment-reviewer`; infra cells are not agent blast radius.
- Do NOT use when: the honest answer is "you don't need cells" — a read
  replica, per-tenant siloing of the hot store, or a regional deploy
  addresses the real risk. Recommend the cheaper lever and stop.

## Inputs to Inspect

1. Current deployment topology: single shared stack, regional, or already
   partitioned — and what is stateful vs stateless within it.
2. The incident / blast-radius history that motivates cells: which real
   failures took down all tenants at once, and would a cell have contained
   them. No such history is itself a finding.
3. Tenant size distribution: the largest tenant's share of load and data —
   whether any single tenant is too big to fit in one cell.
4. Per-component isolation already in place (`saas-platform-architect`
   output): what pooling/siloing already exists, so cells are not re-solving it.
5. Cross-tenant / global features: a global directory, cross-tenant search,
   platform admin, aggregate billing/analytics — the things that CANNOT live
   inside a single cell.
6. Data residency / regional constraints that force physical placement.

## Workflow

1. **Test the premise before designing anything.** Is blast-radius reduction
   the DOMINANT lever? If a read replica (read pressure), per-tenant siloing
   of the hot store (one noisy tenant), or a regional deploy (residency)
   addresses the actual risk, recommend that instead and STOP. Cells multiply
   operational cost by cell count; adopting them for fashion is a finding.
2. **Define the cell.** Name exactly what a cell contains — the self-contained
   stack subset (compute + primary data + cache + queue + workers) — such that
   a tenant is served entirely within one cell. Everything NOT in a cell is a
   global concern (step 6).
3. **Design tenant→cell mapping and placement.** A tenant lives in exactly one
   cell. State the placement policy for new tenants (fill / balance / by-size /
   by-region) and where the mapping is stored — a global routing table, itself
   a global concern.
4. **Design the thin cell-router.** The ONLY global data-plane component:
   resolve tenant → cell from the routing table and forward. It must stay
   thin — no business logic, no per-tenant data — or it becomes the
   shared-fate component cells were meant to eliminate.
5. **Plan cell-by-cell deployment.** Deploy, migrate, and canary one cell at a
   time; a bad change is contained to one cell's tenants. State the rollout
   order, the per-cell health gate, and the halt rule that stops the fleet
   rollout on the first failing cell.
6. **Enumerate cross-cell / global concerns.** What cannot live in a cell —
   the routing table, global identity/auth, cross-tenant features, platform
   admin, aggregate billing/analytics — and how each is served WITHOUT
   becoming a single point of shared fate (replicated, cached per cell,
   degraded-mode tolerant).
7. **Design migration / rebalancing.** Moving a tenant between cells (drain →
   copy → verify → cut over → update routing), rebalancing a hot cell, and
   splitting a cell. This reshapes production data — this skill DESIGNS the
   runbook; it does not execute it.

## Output Format

```
CELL ARCHITECTURE DESIGN — <platform>
Premise check: <is blast-radius reduction the dominant lever? evidence /
  cheaper-lever recommendation if not>
Cell definition: <what one cell contains — compute/data/cache/queue/workers>
Tenant→cell mapping: <assignment, placement policy, routing-table location>
Cell-router: <thin resolve-and-forward; explicitly no business logic / no data>
Cell-by-cell deployment: <rollout order, per-cell health gate, halt rule>
Cross-cell / global concerns: <concern → how served without shared fate>
Migration / rebalancing runbook: <move a tenant; rebalance a hot cell;
  split a cell — DESIGNED, not executed>
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] The premise is tested first; if a cheaper lever suffices the design
      recommends NOT adopting cells and says why.
- [ ] A cell is fully self-contained — a tenant is served end to end within
      one cell, with no runtime dependency on another cell.
- [ ] Every tenant maps to exactly one cell; the placement policy and the
      routing-table location are stated.
- [ ] The cell-router carries no business logic and no per-tenant data — it
      cannot become the shared-fate component.
- [ ] Deployment is per-cell with a halt rule; a bad change cannot reach the
      whole fleet before a cell's health gate catches it.
- [ ] Every global/cross-cell concern is enumerated with how it avoids being
      a single point of shared fate.
- [ ] Migration/rebalancing is designed as a runbook, explicitly not executed
      here; production-data moves route through human approval.

## Gotchas

- The router quietly thickens: someone adds "just one" per-tenant lookup or a
  business rule to it, and now every cell shares fate through the router again.
- Global concerns become silent SPOFs: a "global" auth service or directory
  that every cell calls synchronously re-couples the fleet — cells contain
  failure only if the global path degrades gracefully.
- Cell count multiplies operational cost linearly: migrations, deploys,
  on-call, and observability all now run ×N. Cells trade efficiency for
  containment; if containment isn't the dominant need, it's a bad trade.
- A single tenant too big for one cell breaks the model — that tenant needs
  intra-cell sharding (`data-partitioning-sharding-strategist`), not more cells.
- Cross-cell queries (a report spanning tenants in different cells) defeat the
  purpose; keep them to named, asynchronous, aggregate paths, never the hot path.
- "We adopted cells" as a resume-driven decision with no blast-radius evidence
  is the most common failure — the premise check exists to catch it.

## Stop Conditions

- The premise fails — a cheaper lever addresses the real risk → recommend NOT
  adopting cells and stop; do not design a partition scheme nobody needs.
- Migration or rebalancing must run against production (moving a tenant's live
  data between cells, splitting a cell) → this skill DESIGNS the runbook;
  executing it against production follows `human-approval-boundary`. Do not run it.
- A tenant is too large to fit one cell → the problem is intra-cell write/size
  scale; route to `data-partitioning-sharding-strategist` before forcing a
  cell design around one giant tenant.
- The real need turns out to be per-component isolation or an architecture
  style choice → hand to `saas-platform-architect` or `architecture-advisor`
  rather than over-building whole-stack cells.

## Supporting Files

- `evals/evals.json` — behavior cases: the warranted-cells design, the
  don't-adopt-cells recommendation, the too-big-tenant edge, and the router
  staying thin.
- `evals/trigger-evals.json` — discrimination against `saas-platform-architect`
  (per-component isolation), `architecture-advisor` (style choice), and
  `agent-containment-reviewer` (agent blast radius).
- No `references/` — the cell definition and global-concern enumeration above
  are the complete procedure; detail lives in the produced artifacts.
