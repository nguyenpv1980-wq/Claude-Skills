---
name: data-partitioning-sharding-strategist
description: Design OLTP partitioning and sharding for WRITE/size scale in a multi-tenant SaaS — shard-key selection (tenant-as-shard-key and its hot-tenant limit), range/hash/list partitioning of large tables, resharding/rebalancing a hot tenant, and the cross-shard query/transaction costs you inherit — all gated behind the DON'T-SHARD-PREMATURELY rule: a single well-indexed primary plus read replicas serves a very large SaaS, so shard ONLY on evidence of a real write or size ceiling. Use when a primary has hit (or has a dated forecast to hit) a write/size ceiling that indexing and replicas cannot fix, when one hot tenant dominates a shared table, or when choosing a shard key/partitioning scheme. Do NOT use for per-store ISOLATION scoping (multi-tenant-data-architect), ANALYTICAL-estate partitioning (warehouse-lake-architect), or deciding WHAT leaves the OLTP store (operational-vs-analytical-splitter). Reshapes production data — DESIGNS the plan, does not run it.
---

# Data Partitioning & Sharding Strategist

## Purpose

Design OLTP partitioning and sharding for **write and size scale** — and,
just as often, prove it isn't needed yet. The deliverable is a shard-key
decision (with tenant-as-shard-key and its hot-tenant limit spelled out), a
range/hash/list partitioning scheme per large table, the inherited cross-shard
query/transaction cost, and a resharding/rebalancing runbook — all gated
behind the discipline that governs the whole skill: **don't shard
prematurely.** A single well-indexed primary plus read replicas serves a very
large SaaS; sharding is a one-way door that multiplies operational complexity,
so it is justified only by evidence of a real write or size ceiling, never by
anticipation. This skill designs the reshape; it does not execute it against
production.

## Use When

- Use when: a primary has hit — or has a dated, evidenced forecast to hit — a
  real WRITE-throughput or table-SIZE ceiling (write TPS at saturation, table
  too large for maintenance windows, vacuum/index pain, connection ceiling)
  that indexing and read replicas cannot fix.
- Use when: one hot tenant's data has grown so large it dominates a shared
  table and needs its own partition/shard.
- Use when: choosing a shard key and partitioning scheme (range / hash / list)
  for a large, still-growing table.
- Use when: the current shard key is skewed and a reshard/rebalance is on the
  table.
- Do NOT use when: the concern is tenant ISOLATION/scoping per store (pooled
  vs siloed, the tenant boundary) — that is `multi-tenant-data-architect`;
  isolation scoping is not throughput sharding.
- Do NOT use when: partitioning the ANALYTICAL estate (warehouse/lake zones,
  marts, reporting tables) — that is `warehouse-lake-architect`.
- Do NOT use when: deciding WHAT workload should leave the OLTP store (replica
  vs warehouse vs cache) — that is `operational-vs-analytical-splitter`; this
  skill shards what STAYS on the operational store.
- Do NOT use when: there is no evidence of a ceiling — the honest answer is
  DON'T SHARD; recommend the single-primary + replicas + indexing path and stop.

## Inputs to Inspect

1. Write and read throughput at peak, and how close each is to the primary's
   demonstrated ceiling — the evidence that decides whether to shard at all.
2. Table sizes and growth rates; which tables cause maintenance pain (vacuum,
   reindex, backup windows) and which are merely large.
3. The largest tenant's share of the biggest tables — the hot-tenant signal.
4. Current indexes and the real query patterns against the hot tables; whether
   indexing, partial indexes, or read replicas have actually been tried.
5. The concrete pain: lock contention, slow writes, replication lag, or just
   size — different pains have different cheaper fixes.
6. Cross-table transaction boundaries and any global-uniqueness / foreign-key
   requirements — the things sharding makes expensive.

## Workflow

1. **Prove the ceiling first.** Demand evidence: write TPS at saturation, a
   table size causing real maintenance pain, or a dated growth forecast to a
   hard limit. No evidence → recommend the single-primary + read-replica +
   indexing path, name exactly what to measure to revisit, and STOP. This gate
   is the skill's core, not a formality.
2. **Exhaust the cheaper levers.** Indexing and partial indexes, read replicas
   for read pressure, and declarative table PARTITIONING within one node
   (range/hash/list partitions — a table-SIZE and maintenance lever) all come
   before SHARDING (distribution across nodes). Distinguish the two explicitly:
   partitioning splits a table on one node; sharding splits data across nodes.
3. **Select the shard key.** `tenant_id` is the natural key for multi-tenant
   SaaS — it co-locates a tenant's data and keeps most queries single-shard.
   State its limit up front: a single hot tenant then cannot be split by
   `tenant_id` alone and needs a composite/sub-key. Evaluate cardinality,
   skew, and query-locality for any candidate key.
4. **Choose the partitioning scheme per table.** Range (time/id ranges — good
   for time-series, risks hotspotting the newest partition), hash (even
   distribution, loses range-scan locality), or list (explicit buckets, e.g.
   region). Pick per table against its dominant query pattern, not globally.
5. **Price the cross-shard cost.** Name what breaks: cross-shard joins,
   cross-shard transactions (no cheap two-phase commit), global uniqueness and
   foreign keys, and fan-out aggregate queries. A design where common queries
   hit every shard has the wrong key — say so and revisit step 3.
6. **Design the reshard/rebalance runbook.** Splitting or moving a hot tenant:
   dual-write or backfill → verify (per-key counts/checksums) → cut over →
   update routing, each step reversible. This reshapes production data — this
   skill DESIGNS the runbook; it does not run it.

## Output Format

```
PARTITIONING / SHARDING DESIGN — <store/domain>
Ceiling evidence: <write TPS / table size / forecast — or "no evidence →
  DON'T SHARD; measure X" recommendation and stop>
Cheaper levers considered: <indexing / partial indexes / replicas / in-node
  partitioning — why each is or isn't sufficient>
Shard key: <chosen key; tenant_id + its hot-tenant limit; cardinality/skew>
Partitioning scheme per table: <table → range/hash/list → why, vs query pattern>
Cross-shard cost: <joins / transactions / uniqueness / fan-out — each named>
Reshard / rebalance runbook: <dual-write|backfill → verify → cut over → route;
  reversible per step — DESIGNED, not executed>
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] The write/size ceiling is evidenced (numbers or a dated forecast), not
      assumed; with no evidence the design recommends NOT sharding.
- [ ] Cheaper levers (indexing, replicas, in-node partitioning) are considered
      and explicitly ruled sufficient or insufficient before sharding.
- [ ] Partitioning (one node) and sharding (across nodes) are not conflated.
- [ ] The shard key is justified against cardinality, skew, and query-locality;
      the tenant_id hot-tenant limit is stated.
- [ ] The partitioning scheme is chosen per table against its query pattern.
- [ ] Cross-shard joins, transactions, uniqueness, and fan-out costs are named,
      and common queries stay single-shard.
- [ ] The reshard/rebalance plan is reversible per step and is designed, not
      executed; production-data moves route through human approval.

## Gotchas

- Sharding chosen before the primary is even well-indexed: the expensive fix
  applied before the cheap one. The ceiling check exists to stop exactly this.
- A hash shard key kills range scans; a range key hotspots the newest
  partition. There is no free key — every scheme trades away some access pattern.
- `tenant_id` sharding is defeated by one giant tenant: that tenant's data
  still lands on one shard. Plan the sub-key (or a cell/silo) before it happens.
- Cross-shard transactions silently lose atomicity — code that assumed one
  ACID commit now spans shards and can half-apply. This is a correctness bug,
  not a performance one.
- Resharding is a migration project, not a config change; teams routinely
  underestimate it by an order of magnitude.
- Global uniqueness (a unique email across all tenants) stops being free once
  the space is sharded — it needs a separate global index or a different key.

## Stop Conditions

- No evidence of a write/size ceiling → recommend the single-primary +
  replicas + indexing path and stop; do not shard on anticipation.
- The reshard/rebalance must run against production (dual-write, backfill,
  cutover on live tables) → this skill DESIGNS the runbook; executing it
  follows `human-approval-boundary`. Do not run it.
- A single hot tenant is the whole problem → the answer may be a dedicated
  silo/cell (`multi-tenant-data-architect` / `cell-based-architecture-designer`)
  rather than sharding the shared space; surface that before designing shards.
- The workload is analytical (scans/aggregations) rather than transactional →
  route to `operational-vs-analytical-splitter` and `warehouse-lake-architect`;
  do not shard the OLTP store to serve reporting.

## Supporting Files

- `evals/evals.json` — behavior cases: the evidenced-ceiling shard design, the
  don't-shard-prematurely refusal, the hot-tenant/tenant_id-limit edge, and the
  cross-shard-transaction correctness catch.
- `evals/trigger-evals.json` — discrimination against `multi-tenant-data-architect`
  (isolation scoping), `warehouse-lake-architect` (analytical partitioning), and
  `operational-vs-analytical-splitter` (what leaves the OLTP store).
- No `references/` — the shard-key and scheme guidance above is the complete
  procedure; detail lives in the produced artifacts.
