# RAG retrieval authorization & embedding-risk reference

Detail for `rag-security-architect`. OWASP LLM08 (Vector and Embedding
Weaknesses), 2025.

## Retrieval-time authorization patterns

The rule: the store must never RETURN a vector the caller can't see. Options,
best → worst:

1. **Filtered ANN query** — the vector search includes tenant + ACL
   predicates evaluated by the store during search (metadata filtering /
   pre-filtering). Only authorized candidates are ever scored.
2. **Namespace/collection per principal scope** — the query targets only the
   tenant's namespace, derived server-side from the authenticated tenant.
   Combine with per-document ACL filters for user-level control.
3. **Database/index per tenant** — strongest isolation, higher operational
   cost; still needs user/document-level filtering inside the tenant.
4. **Post-retrieval filtering (ANTI-PATTERN)** — fetch top-k across everything,
   drop unauthorized results in app code. Leaks via ranking, counts, latency,
   and a single filter-code bug. Treat as a finding.

## Why post-filtering leaks

- The ANN search already ranked all tenants' documents; the k it returns is
  distorted by documents you then hide (you asked for 10, showed 3 — the other
  7 existed).
- Result counts, "no results" vs "filtered to zero", and response latency are
  side channels.
- One missing filter branch (a new code path, a caching layer, an export job)
  exposes the whole store. Retrieval-time filtering fails closed.

## Tenant scoping — bypass conditions to check

- Is the tenant/namespace derived from the authenticated session server-side,
  or passed by the client? Client-supplied = IDOR.
- Can any code path issue a query WITHOUT the tenant predicate (admin tools,
  background re-index, analytics, debug endpoints)?
- Do caches, query logs, or re-ranking services see cross-tenant data?
- Compose `multi-tenant-data-architect` for the per-store decision and
  `tenant-isolation-reviewer` for the surface audit.

## Document-level ACL propagation

- Store authorization metadata (owner, tenant, allowed roles/groups,
  classification) with each chunk so it's a query predicate.
- On ACL change: re-index or update metadata so the filter reflects new
  permissions. Stale metadata = a document answering under its OLD rules.
- On deletion: delete the vectors too. A deleted source with a live embedding
  keeps surfacing in answers.
- On re-embedding (model upgrade, re-chunk): carry ACLs forward; don't reset
  to defaults.

## Embedding-specific risks (LLM08)

- **Inversion** — source text can be approximately reconstructed from
  embeddings. Don't expose raw vectors to clients; weigh sensitivity of what
  you embed; consider that a compromised store leaks content, not just IDs.
- **Membership inference** — an attacker probes whether a specific document/
  record was in the index. Mitigate with access control on query and rate
  limiting; recognize similarity scores as a signal.
- **Document poisoning** — an attacker plants a document crafted to rank
  highly for a target query (to inject instructions or misinformation). Trust
  the ingestion source; cross-reference `model-poisoning-reviewer` (corpus
  integrity) and `prompt-injection-defender` (payload once retrieved).
- **Chunk-overlap spill** — overlapping windows can include neighboring
  content from a different, unauthorized document. Bound snippets to the
  authorized chunk.

## Negative-test seeds (→ multi-tenant-security-tester)

- Tenant A queries for a phrase known to exist only in tenant B's docs →
  expect zero results.
- User without access to document D queries its unique content → expect zero.
- Document D's ACL is tightened / D is deleted → subsequent queries stop
  returning it (no stale-embedding leak).
- Client attempts to supply a namespace/tenant id in the query → rejected;
  scope is server-derived.
- Citations for a restricted document → its existence and metadata are not
  revealed.
