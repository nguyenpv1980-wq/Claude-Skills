---
name: operational-vs-analytical-splitter
description: Decide which workloads must leave the operational (transactional) store and how — classify queries by shape (OLTP point reads/writes vs OLAP scans/aggregations), find what is actually hurting the transactional path (long scans, lock pressure, dashboard fan-out, export jobs), choose the offload mechanism per workload (read replica, CDC into a warehouse/lake, materialized/pre-aggregated views, or a cache) against each consumer's stated freshness tolerance, and produce the split boundary with a staged cutover and a stop-doing list for the operational store. The DECISION skill: destination design is warehouse-lake-architect, CDC transport design is streaming-event-architect, and single-query tuning is query-plan-reader. Use when reports/dashboards/exports slow production, when analytics queries hit the primary, or when deciding replica vs warehouse vs cache for a read workload. Do NOT use to design the warehouse itself or to fix one slow query.
---

# Operational vs Analytical Splitter

## Purpose

The operational store exists to serve transactions in milliseconds; the
moment dashboards, exports, and month-end reports run against it, both
masters are betrayed — checkout latency inherits the reporting scan, and
reports still time out. This skill produces the split decision: which
workloads stay on the transactional path, which leave, what mechanism
carries each one out (replica, CDC into an analytical store,
materialization, cache), and what freshness each consumer actually
tolerates — because the whole tradeoff is latency-of-truth vs load. It
decides and sequences the split; it does not design the warehouse it may
prescribe (`warehouse-lake-architect`), the CDC pipeline it may prescribe
(`streaming-event-architect`), or the one bad query that may make the
whole split unnecessary (`query-plan-reader`).

## Use When

- Use when: reports, dashboards, admin exports, or analytics queries run
  against the operational store and transactional latency suffers — or
  will, at projected growth.
- Use when: deciding where a new read-heavy workload (customer-facing
  analytics, usage metering views, search-adjacent listing) should live.
- Use when: choosing between read replica, warehouse/CDC, materialized
  views, and cache for a specific workload, and the tradeoffs need
  stating.
- Use when: an incident review shows a reporting query caused
  transactional degradation and a standing boundary is needed.
- Do NOT use when: ONE query is slow and fixable — read its plan first
  (`query-plan-reader`); a missing index does not justify a warehouse.
- Do NOT use when: the split is decided and the analytical destination
  needs designing — zones, modeling, formats are
  `warehouse-lake-architect`.
- Do NOT use when: the split is decided and the CDC/event transport needs
  designing — that is `streaming-event-architect`.
- Do NOT use when: the pressure is write-path scaling — sharding or
  partitioning the operational store itself for write/size throughput is
  `data-partitioning-sharding-strategist`; re-sharding for tenant
  ISOLATION (pooled↔silo) is `multi-tenant-data-architect`. Offloading
  reads does not save a saturated write path.
- Do NOT use when: the workload is caching a computed result inside the
  request path — `caching-strategy-designer` owns cache design; this
  skill may PRESCRIBE "cache" as a mechanism and then hands over.

## Inputs to Inspect

1. The workload inventory on the operational store: top queries by total
   time and by peak concurrency, scheduled jobs, exports, dashboard
   refresh patterns — from query statistics, slow-query logs, or the
   store's activity views.
2. Evidence of interference: lock waits, replication lag spikes,
   transactional p99 correlated with reporting windows, connection-pool
   exhaustion during refreshes.
3. Each analytical consumer's freshness tolerance — asked, not assumed:
   real-time (seconds), operational reporting (minutes), BI/finance
   (hours/daily). This single number drives mechanism choice.
4. Data shape and volume: table sizes, growth rate, whether analytical
   queries need full history or recent windows.
5. What already exists: replicas and their lag, any warehouse/lake, any
   CDC, materialized views — the split should extend, not duplicate.
6. Tenant posture: whether analytical workloads are per-tenant-facing
   (customer dashboards) or internal — it changes isolation and freshness
   requirements.

## Workflow

1. **Classify every significant workload by shape.** OLTP: point
   reads/writes, short transactions, indexed access. OLAP: scans,
   aggregations, joins across large ranges, window functions. Hybrid
   symptoms (an "operational" endpoint doing a 9-table aggregate) get
   flagged individually — they are the usual culprits.
2. **Attribute the pain.** Tie observed degradation to specific workloads
   with evidence (lock waits, IO saturation windows, correlated p99).
   A split justified by vibes moves work without moving the problem.
   If the evidence points at ONE fixable query, stop — route to
   `query-plan-reader` and re-evaluate after the fix.
3. **Record freshness tolerance per consumer.** For each analytical
   consumer: the staleness it can actually accept, in seconds/minutes/
   hours, with the owner's sign-off. "Real-time" claims get interrogated
   — what decision changes in under a minute?
4. **Choose the mechanism per workload** from the decision table
   (details in references):
   - *Read replica:* same schema/engine, near-real-time, cheap to adopt —
     but carries the same query-shape mismatch and replica lag caveats.
   - *CDC → analytical store:* schema reshaped for analytics, history
     retained, minutes-fresh — the durable answer for true OLAP;
     prescribes `streaming-event-architect` (transport) and
     `warehouse-lake-architect` (destination).
   - *Materialized/pre-aggregated views:* seconds-to-minutes fresh for
     KNOWN query shapes; refresh cost and staleness stated per view.
   - *Cache:* for repeated identical reads with tolerance for staleness —
     prescribe and hand to `caching-strategy-designer`.
   State per workload: mechanism, freshness delivered vs tolerated,
   and why not the cheaper alternative.
5. **Draw the split boundary.** The workloads that STAY (transactional,
   plus operational lookups that genuinely need current-transaction
   visibility) and the stop-doing list: workloads banned from the primary
   once their offload lands, enforced by review convention and, where
   available, by connection/role separation (reporting roles that cannot
   reach the primary).
6. **Sequence the cutover.** Order by pain × ease; each move gets:
   dual-run window (old and new path compared), consumer sign-off on
   parity and freshness, then the primary-side access removed. Standing
   parity/freshness checks after cutover are `data-quality-monitor-designer`
   scope; a one-time heavy backfill is a `data-migration-runbook-author`
   runbook.
7. **State the residual load honestly.** What remains on the operational
   store after the split, projected headroom, and the trigger for the
   NEXT split review (growth threshold or new workload class).

Mechanism decision table, freshness-tier definitions, and the workload
classification worksheet:
[references/split-decision-worksheet.md](references/split-decision-worksheet.md).

## Output Format

```
OPERATIONAL/ANALYTICAL SPLIT DECISION — <store/system>
Workloads classified: <N OLTP-stay / M offload candidates, evidence per candidate>
Pain attribution:     <symptom → workload, with evidence source>
Per-workload verdict:
  <workload>: mechanism=<replica|CDC→analytical|materialized|cache|stay>
  freshness: tolerated=<t> delivered=<d>  rationale=<why not cheaper option>
  handoff=<warehouse-lake-architect | streaming-event-architect | caching-strategy-designer | n/a>
Split boundary:  stays=<list> stop-doing=<workloads banned from primary + enforcement>
Cutover order:   <sequenced moves, each with dual-run + sign-off gate>
Residual:        <load remaining on primary; next-review trigger>
Escape checked:  <the one-bad-query check was performed; result>
```

## Validation Checklist

- [ ] Every offload candidate has evidence tying it to real or projected
      transactional pain — no split by fashion.
- [ ] The one-bad-query escape was checked before any architecture: if a
      plan fix dissolves the problem, the verdict says so.
- [ ] Every consumer has a stated, owner-confirmed freshness tolerance;
      every mechanism choice delivers within it.
- [ ] Each mechanism choice explains why the CHEAPER option was rejected
      (replica before warehouse, view before pipeline).
- [ ] The stop-doing list exists with an enforcement mechanism — a split
      that lets new dashboards quietly return to the primary is temporary.
- [ ] Cutover moves have dual-run windows and consumer sign-off, not
      flag-day switches.
- [ ] Handoffs are named per prescription; this document designs no
      warehouse zones, no CDC topology, no cache keys.

## Gotchas

- Replica lag is a feature of physics, not a defect: consumers moved to a
  replica WILL occasionally read stale data — if a consumer cannot
  tolerate that, it either stays or needs the read-your-writes cases
  explicitly handled. Ask before moving.
- The replica inherits the query-shape problem: a 9-table aggregate that
  hammers the primary hammers the replica too, and its lag then poisons
  every other replica consumer. OLAP shapes need an OLAP home, not a copy
  of the OLTP one.
- "Real-time dashboard" usually means "refreshed while I watch": most
  claimed real-time needs dissolve under the what-decision-changes
  question into minutes — the cheapest mechanisms live there.
- The export nobody owns: scheduled full-table exports are the classic
  invisible primary load. The workload inventory step exists to find
  them; several usually die outright instead of moving.
- Hybrid endpoints resist the split: an API response mixing current
  transactional state with aggregates needs decomposing (current from
  primary, aggregate from the analytical path) — flag these, don't force
  them wholesale into either side.
- Materialized views quietly become load: refresh cost scales with
  frequency × view count; a hundred eager views recreate the problem they
  solved. Refresh budgets are part of the verdict.
- The split leaks back: without the stop-doing enforcement, next
  quarter's dashboard lands on the primary again because it was easiest.
  Role/connection separation outlasts good intentions.

## Stop Conditions

- The evidence shows the pain is ONE query with a broken plan → stop the
  split; route to `query-plan-reader`; re-evaluate only if pain persists
  after the fix. Do not prescribe architecture where an index suffices.
- No freshness tolerance can be obtained for a consumer (owner unknown or
  unwilling to commit) → hold that workload's verdict; a mechanism chosen
  against an assumed tolerance will be relitigated as an incident.
- The store's activity/query statistics are unavailable and interference
  cannot be evidenced → stop and say what instrumentation is needed
  first; splitting blind moves cost without proof of benefit.
- The real pressure is write-path/throughput scaling → route to
  `data-partitioning-sharding-strategist` (shard key, range/hash
  partitioning, resharding a hot key); tenant-ISOLATION re-sharding
  (pooled↔silo) is `multi-tenant-data-architect`. Offloading reads will
  not save a saturated write path.
- Asked to also design the destination warehouse, the CDC pipeline, or
  the cache in the same pass → decline those slices and hand off; the
  split decision must stay reviewable on its own.

## Supporting Files

- [references/split-decision-worksheet.md](references/split-decision-worksheet.md)
  — the mechanism decision table with tradeoff rows, freshness-tier
  definitions, workload classification worksheet, and the stop-doing
  enforcement options.
- `evals/evals.json` — behavior cases including the one-bad-query escape
  and the dashboard-on-primary refusal.
- `evals/trigger-evals.json` — discrimination against
  `warehouse-lake-architect`, `streaming-event-architect`,
  `query-plan-reader`, and `caching-strategy-designer`.
