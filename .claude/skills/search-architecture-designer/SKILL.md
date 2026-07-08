---
name: search-architecture-designer
description: Design search/discovery for a multi-tenant SaaS — in-database full-text (tsvector / trigram) vs a dedicated search engine chosen by scale and relevance need; the indexing pipeline and its freshness lag; relevance/ranking; the per-tenant search-isolation boundary (every query AND every index scoped so results never cross tenants — the search leak); and the faceting/pagination seam. Produces the engine decision, indexing + freshness plan, ranking model, and the tenant-isolation contract. Use when adding search, autocomplete, or discovery, when search is slow, stale, or irrelevant, or when search results must be tenant-isolated. Do NOT use for AI/semantic vector retrieval and its security (rag-security-architect), the base data-store tenancy model (multi-tenant-data-architect), or cursor/pagination mechanics (pagination-cursor-designer) — this designs keyword/faceted search and defers those.
---

# Search Architecture Designer

## Purpose

Search is where a multi-tenant SaaS quietly leaks and disappoints: a query
that forgets its tenant filter returns another customer's records, an index
that lags hours behind makes "search" mean "search yesterday," and a ranking
nobody designed surfaces noise. This skill designs keyword/faceted
search/discovery end to end: the engine decision (in-database full-text vs a
dedicated search engine, by scale and relevance need), the indexing pipeline
and its freshness contract, the relevance/ranking model, and — the
load-bearing part for multi-tenant — the search-isolation boundary that
scopes every query AND every index so a result can never cross tenants. The
deliverable is the engine decision with its tradeoffs, an indexing + freshness
plan, a ranking model, and an explicit tenant-isolation contract. Semantic /
vector retrieval and its security belong to `rag-security-architect`; this
skill owns keyword and faceted search.

## Use When

- Use when: adding search, autocomplete/typeahead, or a discovery/browse
  surface over tenant data.
- Use when: search is slow, returns stale results, or ranks poorly, and the
  indexing pipeline or relevance model needs designing.
- Use when: search must be tenant-isolated and you need the boundary that
  guarantees results never cross tenants (query-side AND index-side).
- Use when: choosing between in-database full-text (Postgres `tsvector` /
  `pg_trgm`) and a dedicated search engine, and the tradeoffs need laying out.
- Use when: designing faceting/filtering and how it hands off to pagination.
- Do NOT use when: the retrieval is SEMANTIC / vector / embedding-based for
  an AI feature (RAG) — the store, its access control, and injection/leak
  risks are `rag-security-architect`; this skill designs lexical search, and
  the two may coexist (hybrid) with the vector half deferred there.
- Do NOT use when: the subject is the base data-store tenancy model — how
  `tenant_id` scopes the primary tables, pooled vs siloed storage — that is
  `multi-tenant-data-architect`; this skill consumes that model and extends
  isolation into the search index.
- Do NOT use when: the subject is cursor/pagination MECHANICS (stable
  cursors, deep-pagination, ordering ties) — that is
  `pagination-cursor-designer`; this skill designs the faceted result set and
  hands pagination to it.

## Inputs to Inspect

1. What is searched: the entities, their fields, corpus size per tenant and
   overall, expected query volume, and whether results are documents, rows,
   or mixed.
2. Relevance expectations: exact-match vs fuzzy/typo-tolerant, phrase,
   prefix/autocomplete, field boosting, recency weighting — what "good
   results" means for this product.
3. Freshness requirement: how soon after a write must the change be
   searchable — sub-second, seconds, minutes — which drives the indexing
   pipeline shape and the honest freshness lag.
4. The tenant model (`multi-tenant-data-architect` output): how tenancy
   scopes the source data, so the search layer can extend — not weaken — it.
5. The current search implementation (if any): `LIKE '%x%'` scans, an
   existing full-text setup, or an external engine, and its pain (slow,
   stale, leaky, irrelevant).
6. Operational constraints: appetite for running/operating a separate search
   engine vs staying in the primary database, and the cost of each.

## Workflow

1. **Decide the engine against real needs.** In-database full-text
   (`tsvector` + GIN, `pg_trgm` for fuzzy/typo) when the corpus and relevance
   needs are modest and staying in the DB avoids a sync pipeline; a dedicated
   search engine when scale, advanced relevance (custom analyzers, tuned
   ranking), faceting at scale, or query volume outgrow the database. State
   the tradeoff — a separate engine buys relevance and scale but adds an
   indexing pipeline, an eventual-consistency freshness lag, and an operational
   surface. Do not default to a heavy engine for a small corpus.
2. **Design the indexing pipeline and its freshness contract.** How a write
   becomes searchable: synchronous (index in-transaction — fresh but couples
   write latency) vs asynchronous (index via change feed / job — decoupled
   but lagged). State the freshness lag honestly ("searchable within N
   seconds"), the reindex/backfill procedure, and how deletes and permission
   changes propagate to the index (a deleted or now-forbidden record must
   leave search).
3. **Design the tenant-isolation boundary — the leak-critical step.** Two
   halves, both mandatory:
   - **Query-side**: every search query carries a server-derived tenant
     filter that cannot be omitted or overridden by the client — the tenant
     is not a client-supplied query param.
   - **Index-side**: the index itself is scoped (per-tenant index, or a
     mandatory tenant field on every document with a filter enforced at the
     engine). Prefer a design where forgetting the filter FAILS CLOSED
     (returns nothing) rather than returning everything.
   State how a misconfigured query cannot silently return cross-tenant hits,
   and how the isolation is negatively tested (a query as tenant A must never
   return tenant B's documents).
4. **Design relevance/ranking.** The ranking signals (text match score,
   field boosts, recency, popularity), tie-breaking, and how ranking is
   evaluated (a labeled query set or judgement calls) rather than tuned by
   vibes. Keep ranking deterministic enough to paginate stably.
5. **Design faceting and the pagination seam.** Facets/filters (their
   cardinality and counts), and the handoff to pagination: search results
   are ordered by relevance, which is not a stable key — hand cursor/deep-
   pagination design to `pagination-cursor-designer` and state the stable
   sort/tiebreak the cursor rides.
6. **Address operations.** Index size and growth per tenant, reindex cost,
   the freshness/lag and error signals to monitor (wiring to
   `observability-operator`), and the failure mode when the search engine is
   down (degrade to DB query, or a clear error — never silently return empty
   and imply "no results").
7. **Deliver** the engine decision, indexing + freshness plan, ranking model,
   and isolation contract in the Output Format, with deferrals named.

## Output Format

```
SEARCH ARCHITECTURE — <system/domain>
Engine decision: <in-DB full-text (tsvector/pg_trgm) | dedicated engine> +
  tradeoff (relevance/scale bought vs pipeline/freshness-lag/ops added)
Corpus:         <entities, per-tenant + total size, query volume, result type>
Indexing pipeline: <sync vs async; write→searchable path; FRESHNESS LAG stated;
  reindex/backfill; delete + permission-change propagation to index>
Tenant isolation (leak-critical):
  query-side: <server-derived tenant filter, non-overridable by client>
  index-side: <per-tenant index or mandatory tenant field + enforced filter>
  fail-closed: <forgetting the filter returns nothing, not everything>
  negative test: <query as A never returns B's docs>
Ranking:        <signals, boosts, tie-break, evaluation method, stable sort>
Faceting + pagination: <facets/counts; stable sort/tiebreak → pagination-cursor-designer>
Operations:     <index growth, reindex cost, freshness/error monitoring,
  engine-down degrade behavior>
Boundaries:     vector/semantic retrieval → rag-security-architect;
  base tenancy model → multi-tenant-data-architect; pagination → pagination-cursor-designer
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] The engine choice is justified against corpus size, relevance need,
      and operational appetite — not a reflexive heavy-engine default.
- [ ] The indexing pipeline states an HONEST freshness lag; deletes and
      permission changes propagate to the index (removed/forbidden records
      leave search).
- [ ] Tenant isolation is enforced BOTH query-side (server-derived,
      non-overridable filter) AND index-side (scoped index / enforced field).
- [ ] The isolation fails closed (forgetting the filter returns nothing) and
      has a stated negative test (A never sees B's documents).
- [ ] Ranking signals are named and evaluated by a method, with a stable
      sort/tiebreak that pagination can ride.
- [ ] Faceting hands pagination to `pagination-cursor-designer`; the cursor's
      stable key is stated.
- [ ] Engine-down behavior is defined and never silently returns empty as if
      "no results."
- [ ] Vector/semantic retrieval is deferred to `rag-security-architect`; the
      base tenancy model is consumed, not redesigned.

## Gotchas

- The tenant filter as a client-supplied query param is the search leak in a
  bow: the client omits or changes it and gets everyone's data. The filter
  is server-derived and non-overridable, or it is not isolation.
- Fail-open isolation is the silent breach: a missing tenant clause on a
  shared index returns ALL tenants' hits with no error. Design so a missing
  filter returns nothing, and negative-test it.
- Deletes that don't propagate to the index make search a resurrection
  service — the record is gone from the DB but still searchable, and clicking
  it 404s or, worse, still shows cached content.
- Permission changes must reach the index too: a document a user lost access
  to must stop appearing in their search, not just their direct fetch.
- `LIKE '%term%'` is not search — it is an un-indexable full scan that
  ignores relevance and dies at scale; name it as debt, not a baseline.
- Ranking by relevance and paginating by offset is unstable: as scores or
  data shift, page 2 duplicates or drops results. Paginate on a stable
  sort/tiebreak, not raw relevance offset.
- A dedicated engine for a 10,000-row corpus is operational cost with no
  payoff; in-database full-text is often the right, boring answer — say so.
- Async indexing means "searchable within N seconds," and users WILL notice
  the lag on their own just-created record; state it and consider read-your-
  writes for the creator.

## Stop Conditions

- The base tenant model (how `tenant_id` scopes source data) is undefined →
  obtain it from `multi-tenant-data-architect` before designing index
  isolation; search isolation must extend the data model, not invent a
  weaker one.
- The requirement is actually semantic/vector retrieval for an AI feature →
  route the vector store, its access control, and injection/leak risks to
  `rag-security-architect`; design only the lexical half here (or the hybrid
  boundary).
- A hard sub-second freshness requirement conflicts with the chosen async
  pipeline at the required scale → present the tradeoff (synchronous indexing
  cost vs freshness) and stop for a human decision rather than asserting both.
- Asked to build/operate the search engine against live data (create indexes,
  run a reindex on production) → this skill DESIGNS; executing index
  builds/reindexes against production follows the repo's approval path.

## Supporting Files

- `evals/evals.json` — behavior cases: the add-search design, the freshness/
  indexing edge, the cross-tenant search-leak refusal, and the vector/RAG
  non-trigger.
- `evals/trigger-evals.json` — discrimination against `rag-security-architect`
  (semantic/vector retrieval), `multi-tenant-data-architect` (base tenancy),
  and `pagination-cursor-designer` (pagination mechanics).
- No `references/` — the engine/indexing/isolation/ranking procedure above is
  complete; detail lives in the produced artifacts.
