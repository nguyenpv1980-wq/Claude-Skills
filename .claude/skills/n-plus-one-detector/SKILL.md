---
name: n-plus-one-detector
description: 'Detect and design out chatty data-access patterns — the N+1 (one query per row), repeated identical queries in one request, serial awaited calls in loops, and over-fetching. Detection is evidence-first: per-request query counts and logs, ORM instrumentation, static cues (lazy relation touched inside iteration); the fix is pattern-matched — eager/preload, batched IN-key or dataloader-style loads memoized per request scope, joins or denormalization with prices stated — plus the regression guard: query-count budgets asserted in tests so the pattern cannot return. Each individual query is usually FAST — that is why plan-reading finds nothing; the defect is the pattern. Use when a request issues suspiciously many queries, latency scales with result-set size, or lazy-load storms are suspected. Do NOT use for one slow query (query-plan-reader), unattributed slowness (profiling-methodology-designer), or caching design (caching-strategy-designer).'
---

# N-Plus-One Detector

## Purpose

The N+1 is the most reliably re-invented performance defect in software:
the list renders, each row lazily touches a relation, and a 50-row page
issues 51 queries — every one of them fast, the sum of them slow, and the
whole thing invisible to single-query tooling because no single query is
guilty. This skill detects chatty data-access patterns with evidence
(query counts per request, logs, ORM instrumentation), designs the
pattern-matched fix (eager loading, batching, joins, denormalization —
each with its price), and installs the regression guard: a query-count
budget asserted in tests, because N+1s return the moment someone adds a
field to a template. Latency that scales with result-set size is this
skill's signature symptom.

## Use When

- Use when: a request, page, or job issues suspiciously many queries —
  a query log, APM trace, or count shows tens-to-hundreds of similar
  statements per operation.
- Use when: latency scales with result-set size — 10 items fast, 100
  items 10× slower — the arithmetic signature of per-row access.
- Use when: an ORM's lazy loading is suspected of firing inside loops,
  serializers, or templates.
- Use when: designing the regression guard — query-count budgets in
  tests for endpoints that have been burned before.
- Use when: serial awaited calls in a loop (per-item remote/DB round
  trips) need batching design, even where no ORM is involved.
- Do NOT use when: ONE query is slow — its plan is the evidence and
  `query-plan-reader` the tool; here every query is typically fast.
- Do NOT use when: nothing has attributed the slowness yet — "the app
  is slow" starts at `profiling-methodology-designer`; a query-count
  explosion in its findings is what routes here.
- Do NOT use when: the fix under design is a CACHE — caching a chatty
  pattern hides it and adds invalidation debt; the pattern gets fixed
  here first, and genuine cache candidates route to
  `caching-strategy-designer`.
- Do NOT use when: the chatter is service-to-service (one API call per
  item against another service) and the design question is the
  inter-service contract — batch endpoint design belongs to
  `api-event-architect` (external) or `architecture-designer`
  (internal boundaries); this skill still applies for the caller-side
  batching pattern.

## Inputs to Inspect

1. Per-request query evidence: the query log / APM span list for one
   symptomatic operation — statement shapes, counts, and total time vs
   per-query time. This is the primary artifact; obtain it before
   theorizing.
2. The data-access layer's semantics: which ORM/query layer, its lazy
   vs eager defaults, its batching facilities (preload/include,
   IN-key loaders, dataloader equivalents), and its per-request scope
   (where memoization can safely live).
3. The code path: the loop/serializer/template touching relations per
   item; resolver structure in GraphQL-style APIs (the per-field
   resolver is the N+1's natural habitat).
4. Result-set characteristics: typical and worst-case item counts,
   pagination state (or its absence), and whether the endpoint's
   latency scales with them.
5. Existing test infrastructure: where query-count assertions can live
   (the test layer that owns integration-level checks), and any
   existing counter/instrumentation hooks.
6. Write/consistency context for fix pricing: how hot the touched
   tables are, and whether denormalized read fields are maintainable.

## Workflow

1. **Confirm the pattern with counts, not vibes.** For the symptomatic
   operation, produce the evidence table: distinct statement shapes ×
   repetitions × per-query time. The N+1 signature: one parent query +
   N near-identical child queries differing only in a key. Related
   signatures: repeated IDENTICAL queries (missing per-request
   memoization), serial awaits in a loop (wall-clock = N × round
   trip), and SELECT-everything over-fetch feeding two fields.
2. **Locate the injection site.** The loop, serializer, template, or
   per-field resolver touching a lazy relation per item. Name the file/
   path; the fix lands where the touch happens, not where the query
   runs. Static cues for review: relation access inside iteration,
   awaited calls in loops, missing `IN`-batching on keyed lookups.
3. **Choose the fix by pattern** (catalog in references):
   - *Known-ahead relations:* eager/preload declarations on the parent
     query — the default fix; price: over-eager loading drags unneeded
     data on paths that don't render the relation (scope eager-ness per
     use, not globally).
   - *Dynamic/conditional relations (resolvers, polymorphic):* batched
     loader — collect keys per request tick, one IN-key query,
     memoized per request scope; price: loader infrastructure and
     per-request cache lifecycle.
   - *Aggregates per row:* one grouped aggregate query joined back,
     never per-row COUNT calls.
   - *Serial awaits:* batch the keys into one call where an interface
     exists; otherwise bounded-concurrency fan-out as the lesser fix,
     with the batch-endpoint need routed to the contract owner.
   - *Truly relational shapes:* a join producing the composed row set —
     price: row-width multiplication on one-to-many joins
     (deduplication cost); prefer two batched queries over exploding
     joins.
   - *Read-path denormalization:* a maintained count/summary column —
     price: consistency maintenance; only with an owner and an update
     rule.
   Over-fetch fixes ride along: project the fields the path uses.
3½. **Reject the cache reflex explicitly.** Caching the chatty result
   is not on the fix menu here: it hides the pattern at the price of
   invalidation debt, and the first cache miss replays the storm.
   After the pattern is fixed, a genuine staleness-tolerant candidate
   may route to `caching-strategy-designer` on its own merits.
4. **Verify by re-measuring the count.** Same operation, same data
   shape: statement count drops to the designed number (typically 2–3),
   wall-clock drops accordingly, and — the check that catches over-
   correction — the replacement queries' plans are sane
   (`query-plan-reader` if the new IN-key or join query is itself
   heavy at volume).
5. **Install the regression guard.** A query-count budget assertion in
   the integration layer for the fixed operation: "renders with ≤ K
   queries" (exact-count where stable, small budget where seeding
   varies). The budget documents intent — the next lazy touch fails a
   test instead of shipping. Wire the counter via the ORM's
   instrumentation hook; keep budgets on the endpoints that matter,
   not everywhere (assertion noise erodes the guard).
6. **Report** in the Output Format: evidence table, injection sites,
   fix per site with price, measured before/after counts, and the
   guard's location.

Pattern catalog with fix templates, counter-instrumentation options,
and query-budget assertion patterns:
[references/chatty-access-patterns.md](references/chatty-access-patterns.md).

## Output Format

```
N+1 / CHATTY ACCESS REPORT — <operation>
Evidence: <statement shapes × repetitions × per-query time; total vs per-query>
Signature: N+1 | repeated-identical | serial-await | over-fetch (combinations common)
Injection site(s): <file/path — loop, serializer, resolver, template>
Fix per site:
  <site>: <eager|batched-loader|grouped-aggregate|batch-call|join|denormalize>
  — price: <over-eagerness / loader lifecycle / row-width / consistency>
Cache reflex: rejected here — pattern fixed first (candidates → caching-strategy-designer after)
Verification: queries <before> → <after (designed number)>; wall-clock <before> → <after>;
              replacement-query plan sanity: <checked | routed to query-plan-reader>
Regression guard: <test file/layer — budget K, exact|bounded, counter hook>
Residual: <paths with the same pattern not yet fixed — listed, not implied done>
```

## Validation Checklist

- [ ] The pattern is evidenced by a count table from a real operation —
      not inferred from code reading alone.
- [ ] The injection site is named at file/path level; the fix lands at
      the touch point.
- [ ] The chosen fix matches the pattern class and states its price;
      no global eager-loading, no reflexive cache.
- [ ] One-to-many joins were checked for row-width explosion; batched
      two-query shapes preferred where they explode.
- [ ] Before/after statement counts are measured, not estimated; the
      after-count equals the design.
- [ ] The replacement query's own plan was sanity-checked at realistic
      volume (large IN lists, big joins).
- [ ] A query-count budget assertion exists for the fixed operation,
      wired to a real counter hook.
- [ ] Unfixed sibling paths with the same pattern are listed as
      residual.

## Gotchas

- Fast queries hide slow requests: per-query time of 2ms × 400 queries
  is 800ms of pure round-trips — dashboards ranking slow QUERIES never
  surface it. Count per request, not per statement.
- Global eager loading is the overcorrection: preloading every
  relation everywhere fixes one page and bloats twelve — eager-ness is
  scoped per use path.
- The batched IN-query can become the new problem: a 10,000-key IN
  list has its own plan pathology; chunk the keys and sanity-check the
  batched query's plan at worst-case volume.
- One-to-many joins multiply row width: joining a parent to 200
  children repeats the parent 200 times on the wire; two batched
  queries beat the exploding join.
- Per-request memoization leaking across requests: a loader cache
  scoped wrong (process-global) serves user A's rows to user B —
  in multi-tenant systems this is a data leak, not just staleness.
  The request scope is a correctness boundary.
- GraphQL-style resolvers reinvent N+1 per field: each field resolver
  fetching independently is the architecture working as designed —
  batched loaders per entity type are the standing fix, not per-query
  patches.
- Exact-count assertions flake on seed drift: where fixture rows vary,
  assert a small budget (≤ K) instead of equality — the guard should
  catch a storm, not a seeding change.
- Pagination absence turns fixes moot: an unpaginated list of 50,000
  items is slow after every fix; pagination discipline (bounded page
  sizes) rides along with the pattern fix.

## Stop Conditions

- Asked to fix by caching ("just cache the page/result") → refuse the
  reflex: the pattern gets fixed first; caching a chatty pattern hides
  it and adds invalidation debt. Genuine cache candidates route to
  `caching-strategy-designer` after the count is sane.
- No per-request query evidence can be obtained (no logs, no
  instrumentation, no local reproduction) → stop and install the
  counter hook first; pattern fixes designed from code-reading alone
  misfire on framework internals.
- The evidence shows ONE heavy query, not many fast ones → route to
  `query-plan-reader`; this skill's fixes would restructure access
  that isn't the problem.
- The per-item calls are cross-service and the batch interface doesn't
  exist → design the caller-side batching AND route the batch-endpoint
  contract to its owner (`api-event-architect` / the owning team);
  do not invent another service's API unilaterally.
- Fixing the pattern requires schema change (denormalized counts,
  new keys) → the read-field design is this skill's output, but the
  migration itself follows `schema-evolution-planner` staging and the
  repo's change process — hand off, don't inline DDL.

## Supporting Files

- [references/chatty-access-patterns.md](references/chatty-access-patterns.md)
  — the pattern catalog with fix templates per ORM idiom class,
  counter-instrumentation options, IN-list chunking guidance, and
  query-budget assertion patterns (exact vs bounded).
- `evals/evals.json` — behavior cases including the resolver-storm edge
  and the cache-it-instead refusal.
- `evals/trigger-evals.json` — discrimination against
  `query-plan-reader` (the sibling seam), `profiling-methodology-designer`,
  and `caching-strategy-designer`.
