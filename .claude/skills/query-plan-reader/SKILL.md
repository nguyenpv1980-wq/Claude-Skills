---
name: query-plan-reader
description: 'Read ONE query''s execution plan and turn it into a ranked tuning verdict — capture the plan with actual runtime statistics where safe (EXPLAIN-style, tool-agnostic), interpret operators (scans vs index access, join strategy, sort/spill, row-estimate vs actual divergence as the diagnostic core), name the dominant cost node, and rank fixes by evidence: statistics refresh, query rewrite, index add/change (write-amplification and storage price stated), or schema adjustment — each with a re-verification method at representative data volume. Multi-tenant note: tenant-scoping predicates and row-security policies appear IN the plan and are part of the cost being read. Use when one query is slow, when asked to interpret EXPLAIN output, or when an index decision needs evidence. Do NOT use for many-small-queries chatter (n-plus-one-detector), unattributed slowness (profiling-methodology-designer), or moving whole workloads (operational-vs-analytical-splitter).'
---

# Query Plan Reader

## Purpose

A slow query is interrogated, not guessed at: the execution plan says
exactly where the time goes — the scan that reads ten million rows to
return twelve, the join strategy chosen off a row estimate that is wrong
by four orders of magnitude, the sort spilling to disk — and almost every
"add an index?" debate dissolves once the plan is on the table. This
skill reads ONE query's plan and produces a ranked, evidenced verdict:
what dominates the cost, why the planner chose it, which fix removes it
(index, rewrite, statistics, schema), what each fix costs elsewhere, and
how to verify the fix actually took. It is deliberately the narrowest
tool in the performance pack — one query, its plan, its verdict.

## Use When

- Use when: one identified query is slow — from a slow-query log, an
  attribution verdict (`profiling-methodology-designer` handoff), a
  harness regression pinned to a query, or a user pointing at it.
- Use when: asked to interpret EXPLAIN / EXPLAIN ANALYZE-style output
  someone already captured.
- Use when: an index decision needs evidence — "should we add an index
  on X" is a plan-reading question, answered with the plan before and
  the predicted plan after.
- Use when: a query regressed after a data-volume change, statistics
  drift, or an upgrade, and the old/new plans need diffing.
- Do NOT use when: the problem is MANY small queries per request —
  query-count explosion is `n-plus-one-detector`; each individual query
  there is usually fine.
- Do NOT use when: nothing has attributed the slowness to a query yet —
  "the app is slow" goes to `profiling-methodology-designer`; this
  skill starts with a named query.
- Do NOT use when: the query is architecturally misplaced — an OLAP
  aggregation on the operational store may tune 2× when it needs 100×;
  read the plan, then route workload placement to
  `operational-vs-analytical-splitter` when the shape says so.
- Do NOT use when: writing or reviewing the MIGRATION that adds the
  recommended index — authoring follows the repo's change process and
  safety review is `secure-migration-reviewer`.
- Do NOT use when: designing tenant partitioning/indexing strategy for
  a store — that structural design is `multi-tenant-data-architect`;
  this skill reads how one query interacts with what exists.

## Inputs to Inspect

1. The query text, its parameters (the actual values matter — plans are
   parameter-sensitive), and its source (ORM-generated or hand-written;
   ORM queries may need capturing as actually emitted).
2. The plan, ideally with ACTUAL statistics (analyze-style execution,
   with the caveat below for writes): node costs/timings, row estimates
   vs actuals, access methods, join strategies, memory/spill indicators.
3. Schema context for the touched tables: existing indexes and their
   definitions, constraints, approximate row counts and growth, column
   cardinality/skew for the filtered columns.
4. Statistics state: when the planner's statistics were last refreshed
   for these tables (estimate-vs-actual divergence often ends here).
5. The multi-tenant overlay: tenant predicates and row-security
   policies that the store injects into this query's plan — they are
   real filter nodes with real cost, and an index that ignores the
   tenant key serves multi-tenant queries badly.
6. The query's write context: how hot the table is for writes (bounds
   the index appetite) and how often this query runs (a weekly report
   earns less optimization than a per-request path).

## Workflow

1. **Capture the plan honestly.** Prefer actual-execution statistics
   over estimates for reads; for INSERT/UPDATE/DELETE, analyze-style
   execution EXECUTES the write — use the store's rollback-wrapped
   analyze idiom or read-only equivalents, and never against production
   data paths without the repo's approval conventions. Capture at
   representative data volume — a plan over 100 rows says nothing
   about 100 million (the planner itself chooses differently).
2. **Find the dominant node.** Walk the plan for where cost/time
   concentrates: the deepest expensive scan, the join producing the
   row explosion, the sort/hash spilling to disk. Name ONE dominant
   cost; plans with two independent hotspots get sequenced (fix the
   dominant, re-plan, reassess).
3. **Read estimate-vs-actual divergence as the first diagnostic.**
   A node estimating 40 rows and producing 400,000 explains every bad
   downstream choice (wrong join strategy, wrong access method). Causes
   in order of likelihood: stale statistics, correlated predicates the
   planner multiplies independently, skewed data the histogram misses,
   parameter sensitivity. Statistics refresh is the cheapest fix in the
   entire catalog — check it before designing indexes.
4. **Interpret access methods against selectivity.** A full scan is
   WRONG only when the predicate is selective; a scan serving 80% of
   the table is the planner being right. An index access looping
   millions of times can be slower than one scan — read the loop
   counts, not the operator names.
5. **Rank the fixes with their prices.** In default order of
   cheapness: statistics refresh; query rewrite (predicate made
   sargable — no functions over the filtered column, no implicit type
   casts; unneeded columns dropped from the select; pagination made
   keyset instead of large offsets); index add/change (composite
   ordered by equality→range, covering where the store supports it,
   tenant-key-aware in multi-tenant tables) — priced in write
   amplification per mutation and storage; schema adjustment
   (generated/computed columns, denormalized read fields) — priced in
   consistency maintenance. Every recommendation states its price, not
   just its benefit.
6. **Predict, apply (via the change process), re-verify.** State the
   expected plan change per fix ("scan → index access on X, loops
   1→N"), then verify after application: re-capture the plan under the
   SAME parameters and volume, confirm the shape changed as predicted,
   and confirm wall-clock/percentile improvement at the calling
   surface (`performance-test-harness` gates where they exist). A fix
   that changes the plan but not the latency is a diagnosis error —
   loop back to step 2.
7. **Route what plan-reading cannot fix.** OLAP shape on the
   operational store → `operational-vs-analytical-splitter`; result
   cacheable and staleness-tolerant → `caching-strategy-designer`;
   the index migration itself → the change process +
   `secure-migration-reviewer`.

Operator-reading table, estimate-divergence causes, sargability
catalog, and the composite-index worksheet:
[references/plan-reading-guide.md](references/plan-reading-guide.md).

## Output Format

```
QUERY PLAN VERDICT — <query id/summary>
Captured: <actual|estimate>, params=<values>, volume=<rows in touched tables>
Dominant cost: <node, share of total, why the planner chose it>
Divergence:   <est vs actual at key nodes; statistics state>
Tenant overlay: <tenant/row-security predicates present + their cost note | n/a>
Fixes (ranked):
  1. <fix> — expected plan change: <shape> — price: <write amp/storage/maintenance>
  2. ...
Re-verify:    <re-plan under same params+volume; expected shape; surface-level timing check>
Routed out:   <splitter | caching-strategy-designer | secure-migration-reviewer | none>
Not addressed: <what this verdict deliberately leaves alone>
```

## Validation Checklist

- [ ] The plan was captured with actual statistics (or the write-safe
      idiom) at representative volume — not an estimate over a toy
      table.
- [ ] ONE dominant cost is named with its share; multi-hotspot plans
      are sequenced, not shotgunned.
- [ ] Estimate-vs-actual divergence was read and statistics state
      checked BEFORE any index was designed.
- [ ] Every recommended index states column order rationale and its
      write/storage price; no index-everything lists.
- [ ] Rewrites preserve semantics (stated) — a faster query returning
      different rows is a bug, not a fix.
- [ ] Tenant predicates/row-security cost was read, and recommended
      indexes serve the tenant-scoped access pattern.
- [ ] The re-verification method is stated with expected plan shape and
      a surface-level timing check.
- [ ] Fixes plan-reading cannot deliver are routed, not absorbed.

## Gotchas

- Parameter sensitivity: the plan for `status='rare_value'` and
  `status='common_value'` can differ completely; a fix verified on the
  wrong parameter fixes nothing. Capture with the SYMPTOMATIC values,
  and note plan-cache/prepared-statement effects where one cached plan
  serves all values.
- Analyze-style capture of writes executes them — the rollback-wrapped
  idiom is mandatory, and production data paths need approval. The
  plan you capture must never be the incident.
- Toy-volume plans lie twice: the planner picks different strategies
  at different volumes, AND the timings are cache-warm fictions.
  Representative volume is a capture requirement, not a nicety.
- Functions over filtered columns kill index use quietly — including
  implicit ones: type coercion on a mismatched parameter type is a
  function the plan shows as a scan nobody asked for.
- Index loops beat scans until they don't: nested-loop index access
  looping 10M times loses to one scan; the crossover is in the loop
  count, which the actual plan shows and the operator name hides.
- The covering-index tax: covering every query's columns bloats every
  write; composite order (equality first, then range, then includes)
  and the write-amplification price keep the appetite honest.
- Row-security predicates are invisible in the query text: the plan
  shows filters the developer never wrote. In multi-tenant stores,
  read them — an index without the tenant key in front often serves
  the policy-wrapped query badly.
- OFFSET pagination degrades linearly by design — no index fixes page
  4,000 of an offset paginator; that is a keyset-rewrite verdict.

## Stop Conditions

- Asked to capture analyze-style plans for mutating statements against
  production, or the capture itself would add dangerous load → stop
  and require the rollback-wrapped idiom / a replica / explicit human
  approval per the repo's conventions.
- The plan cannot be captured at representative volume anywhere (no
  environment has realistic data) → halt and say the verdict would be
  fiction; route to test-data provisioning before diagnosing.
- The requested outcome is "make it fast without changing the query or
  the schema and without any new index" and the plan shows the
  dominant cost is structural → present the honest options and stop;
  there is no incantation.
- The query's SHAPE is analytical on an operational store and tuning
  headroom is an order of magnitude short of the need → deliver the
  plan verdict AND route placement to
  `operational-vs-analytical-splitter`; do not promise tuning will
  carry an architectural burden.
- Asked to also apply the index/rewrite directly to a live store →
  decline execution; recommendations flow through the change process
  (`secure-migration-reviewer` for the migration).

## Supporting Files

- [references/plan-reading-guide.md](references/plan-reading-guide.md)
  — operator-reading table (scans, joins, sorts, spills), estimate-
  divergence cause list, sargability catalog, composite-index
  worksheet, keyset-pagination rewrite pattern.
- `evals/evals.json` — behavior cases including the estimate-divergence
  edge and the index-everything refusal.
- `evals/trigger-evals.json` — discrimination against
  `n-plus-one-detector`, `profiling-methodology-designer`,
  `operational-vs-analytical-splitter`, and `multi-tenant-data-architect`.
