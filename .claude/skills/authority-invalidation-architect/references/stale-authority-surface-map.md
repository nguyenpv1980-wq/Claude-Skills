# Stale-Authority Surface Map

The working reference for Workflow steps 2 (inventory), 3 (differential),
5 (per-surface design), and 6 (verify battery). Each surface lists: where
the old copy of authority lives, the diagnostic tell that implicates it,
the invalidation options, the verify probe, and the owner — OWNED means
this skill designs it; a skill name means compose that skill and route.

An inventory pass walks all eleven surfaces and dispositions each one:
holder (with evidence), ruled out (with how), or absent from this app.

---

## 1. Server session records

- **Old copy:** the session record minted at sign-in — role/tenant
  resolved then and snapshotted — plus the cookie/session id referencing
  it.
- **Tell:** logout or removal "works" in the UI, but replaying the old
  cookie or session id still authenticates; wrong on every device until
  the record dies.
- **Invalidation:** delete or version-bump the record server-side on
  logout AND on authority change; re-resolve authority per request
  instead of trusting the record's snapshot where the bound demands it.
- **Verify probe:** replay the pre-change session cookie → rejected
  within the bound.
- **Owner:** OWNED (design); custody implementation →
  `secrets-identity-hardener` (manual-only).

## 2. JWT / token claims

- **Old copy:** role/tenant/plan claims inside the signed access token,
  honored until `exp` by anything that trusts the token — including RLS
  policies reading claim context.
- **Tell:** the problem fixes itself after a consistent interval (that
  interval is the access TTL) or after sign-out/sign-in.
- **Invalidation:** the SKILL.md step-5 menu — short TTL + refresh
  rotation / session-version (epoch) check per request / denylist until
  natural expiry — with the resulting latency stated.
- **Verify probe:** use the pre-change token after the change → rejected
  or re-scoped within the bound.
- **Owner:** OWNED.

## 3. Client stores & data caches

- **Old copy:** query/data-cache entries, state stores, and persisted
  storage holding lists, entities, permission flags, plan badges.
- **Tell:** works correctly in an incognito window; other users see the
  change; a hard refresh fixes it.
- **Invalidation:** purge on logout AND on an authority-change signal
  (realtime event, response-stamped authority version, or re-check on
  focus/refetch); persisted keys scoped per user.
- **Verify probe:** shared-device sign-in as another user renders nothing
  of the previous user; the removed entity disappears without a hard
  refresh within the bound.
- **Owner:** OWNED (display posture of the in-between state →
  `edge-state-ux-designer`).

## 4. Shared HTTP/CDN caches

- **Old copy:** cached API/page responses whose keys lack (or hold stale)
  authority discriminators.
- **Tell:** wrong for everyone, or per-region; fixes at a fixed TTL;
  response headers show shared-cache hits.
- **Invalidation:** → `caching-strategy-designer` (keys, purge design,
  envelopes, and its personalized-responses rule).
- **Verify probe:** post-change request serves fresh; authenticated
  responses are absent from shared caches.
- **Owner:** `caching-strategy-designer`.

## 5. In-process / distributed server caches

- **Old copy:** memoized permission, membership, or entitlement lookups
  in app memory or a shared cache.
- **Tell:** wrong on one app instance only (in-process), or fixes on
  deploy/restart.
- **Invalidation:** → `caching-strategy-designer`; whether authz results
  may be cached AT ALL is its Safety Rule's call, not this map's.
- **Verify probe:** post-change read is correct on EVERY instance within
  the bound.
- **Owner:** `caching-strategy-designer`.

## 6. Database session context (the RLS input)

- **Old copy:** the session settings or claims snapshot policies read;
  a pooled connection's leftover context from the previous request.
- **Tell:** the policy SQL audits correct, yet results are wrong for the
  changed principal — or intermittently wrong per connection.
- **Invalidation:** fresh claims per request (surface 2's policy decides
  how fresh); the pool resets session context on checkout.
- **Verify probe:** the changed principal's post-change query returns
  zero rows / is rejected — the per-command negative-test shape
  `rls-policy-auditor` produces, run against the CHANGED principal.
- **Owner:** policy correctness → `rls-policy-auditor`; context
  FRESHNESS and pool reset → OWNED.

## 7. Live realtime subscriptions

- **Old copy:** an open channel authorized at subscribe time, before the
  change.
- **Tell:** the removed user keeps receiving live events until they
  disconnect or reconnect.
- **Invalidation:** → `realtime-subscription-architect` (the
  re-authorization trigger and teardown of now-forbidden subscriptions).
- **Verify probe:** events stop within the bound without waiting for a
  natural reconnect.
- **Owner:** `realtime-subscription-architect`.

## 8. Share links

- **Old copy:** a bearer link token whose grant outlives the revocation —
  or a cached response for it (check surfaces 3 and 4 before blaming the
  token).
- **Tell:** a revoked link still resolves.
- **Invalidation:** → `share-link-access-architect` (revocation checked
  server-side on every use).
- **Verify probe:** the revoked link yields the uniform denial within the
  bound.
- **Owner:** `share-link-access-architect`.

## 9. Entitlement / plan resolution

- **Old copy:** a cached entitlement answer, or plan state lagging the
  billing provider's webhook.
- **Tell:** upgraded but still the old tier for minutes; UI and API
  disagree about the plan.
- **Invalidation:** → `plan-entitlement-architect` (invalidation on
  plan-change events; which state is authoritative during the webhook
  gap).
- **Verify probe:** the entitlement answer flips within the bound in BOTH
  directions — upgrade grants, downgrade denies.
- **Owner:** `plan-entitlement-architect`.

## 10. Search indexes

- **Old copy:** the indexed document for a deleted, moved, or
  re-permissioned item — titles and snippets leak even when the click
  404s.
- **Tell:** gone in the app, still present in search results.
- **Invalidation:** → `search-architecture-designer` (deletion
  propagation to the index; permission filtering at query time).
- **Verify probe:** the changed principal's search returns no hit within
  the bound.
- **Owner:** `search-architecture-designer`.

## 11. Signed URLs / file CDN

- **Old copy:** a signed GET URL or CDN object outliving the deletion or
  revocation.
- **Tell:** the file is "deleted" but the old URL still downloads.
- **Invalidation:** → `file-upload-storage-architect` (short-lived
  signatures, deletion propagation, invalidation on replacement).
- **Verify probe:** the old signed URL fails once its short lifetime and
  the bound pass; no new signature is issuable to the changed principal.
- **Owner:** `file-upload-storage-architect`.

---

## Verify-battery template

Run for the ACTUAL changed principal — their real session, token, device,
and subscriptions — not a fresh test account, which skips every stale
copy by construction.

**Deny direction (first):**

| Surface | Probe | Expected within the bound |
| --- | --- | --- |
| API | read/write a resource the change removed | denied |
| Session | replay the pre-change cookie/session id | rejected |
| Token | use the pre-change access token | rejected / re-scoped |
| Client | observe the app without a hard refresh | stale view purged |
| Realtime | hold the pre-change subscription open | events stop |
| DB/RLS | changed principal's query (negative-test shape) | zero rows |
| Search | query for the removed/deleted item | no hit |
| Files | fetch the old signed URL | fails |
| Links | open the revoked share link | uniform denial |
| Plan | call a feature the downgrade removed | denied |

**Grant direction (second):** the newly added/upgraded principal gains
access on each applicable surface without signing out and back in — or
the designed grant latency is explicitly stated and accepted.

**Positive control (always):** an unaffected user on the same surfaces is
unaffected — a battery that can only fail is as untrustworthy as one that
can only pass.

These probes extend the app-layer isolation suites
(`multi-tenant-security-tester`) with the actor class those suites lack:
the FORMERLY-authorized principal. Design-time revoked-membership negative
tests from `authorization-matrix-designer` are the DB/API subset; this
battery is their cross-surface completion, run at design sign-off and as
regression after auth changes.
