---
name: authority-invalidation-architect
description: 'Diagnose and design the fix for the "change didn''t take effect" access-bug class — a removed user still sees the data, a revoked role still works, logout doesn''t end the session, a plan change still shows the old tier, a deleted item stays visible: inventory every place the old authority survives (server session records, JWT/token claims until expiry, client-side stores and data caches, server/CDN caches, live realtime subscriptions, database session context, search indexes, signed URLs), locate which holds the stale copy, design the invalidation or forced refresh per surface against a stated revocation-latency bound (deny direction first: revoked access must actually revoke), and verify with before/after tests that access changed. Composes caching-strategy-designer, realtime-subscription-architect, plan-entitlement-architect, share-link-access-architect, rls-policy-auditor. Do NOT use to design a cache, author the permission matrix, or when access never worked — this owns changes that failed to propagate.'
---

# Authority Invalidation Architect

## Purpose

The bug class this skill owns is silent by construction: an authority change
— a member removed, a role revoked, a logout, a plan change, a deletion —
that did not take effect somewhere, so old authority keeps working. The
removed user experiences nothing broken and reports nothing; the owner
believes the change worked; the app keeps honoring a copy of authority that
no longer exists in the database. That is unauthorized access to tenant data
arriving through time instead of through a query, and its victims cannot
name the mechanism — which copy, of the many the platform minted for them,
is the one still alive. This skill owns the lifecycle CHANGE → PROPAGATE →
VERIFY: classify the change and its direction, inventory every place old
authority survives, locate the holder, design the invalidation or forced
refresh per surface against a stated revocation-latency bound (deny
direction first), and prove the change took effect with a cross-surface
verify battery. The per-surface mechanism owners are composed, never
restated; this skill contributes the surfaces nothing else owns —
token-claims staleness, server-session versioning, client-state purge — and
the differential and verify battery no single-surface skill can see whole.

## Use When

- Use when: a removed user or member can still see or reach data, a revoked
  role or permission still works, or an access change "didn't take effect"
  or "didn't propagate".
- Use when: logout doesn't end the session — still signed in on another tab
  or device, or a replayed old cookie/token still works.
- Use when: a plan change doesn't show — upgraded but still the old tier,
  downgraded but the old limits still apply (triage starts here; the
  plan-resolution mechanics route onward).
- Use when: a deleted or archived item stays visible — in the app, in
  search results, or through an old link or URL.
- Use when: a change takes effect only after refresh or re-login, or works
  for the person who made it but not for other users or devices —
  propagation happening by accident, not by design.
- Use when: designing revocation propagation deliberately — the mechanism
  by which removing a membership kills its effect in active sessions and
  issued tokens (the mechanism `authorization-matrix-designer` requires you
  to state), a stale-claims policy, or purge-access-state-on-change.
- Do NOT use when: access never behaved correctly — there is no
  before-state in which it worked. That is authorization correctness, not
  propagation: `authorization-matrix-designer` (the matrix) or
  `rls-policy-auditor` (the policy SQL). The discriminator question: did it
  behave correctly before the change?
- Do NOT use when: adding or designing a cache, choosing TTLs, keys, or
  layers — `caching-strategy-designer`; its output is one surface in this
  skill's inventory, not the other way around.
- Do NOT use when: a live channel delivers another tenant's data — that is
  a cross-tenant leak, not a stale change: `realtime-subscription-architect`.
- Do NOT use when: designing plans, limits, and metering —
  `plan-entitlement-architect`.
- Do NOT use when: a credential leaked and needs rotation or custody fixes
  — `secrets-identity-hardener` (manual-only).
- Do NOT use when: an unknown-cause failure has no authority-change shape —
  `systematic-debugger` is the generic method; this skill is the domain
  differential for this symptom family and composes that method's evidence
  discipline where the holder is ambiguous.

## Inputs to Inspect

1. The auth mechanism, before anything else: server-side sessions or
   stateless tokens (JWT)? If tokens — exactly which claims are minted at
   sign-in (role? tenant? plan?) and the access/refresh TTLs. This one fact
   usually names the staleness window.
2. Every authority-change path: member-removal and role-change UI, billing
   webhooks, admin and support tooling, background jobs, bulk imports —
   each is either a propagation trigger or a propagation hole.
3. The client data layer: state stores, query/data-cache libraries (e.g.
   React Query, SWR, Apollo), persisted storage — and what, if anything,
   clears each on logout or on an authority change.
4. Server and shared HTTP/CDN caches in play, with their keys and TTLs
   (the design from `caching-strategy-designer`, where one exists).
5. Live surfaces: realtime channels and presence — their subscribe-time
   authorization and whether anything re-checks mid-connection.
6. The database's authorization context source: the session settings or
   token claims that RLS policies read, and connection-pool context reset
   behavior.
7. Secondary copies: search indexes, signed URLs and file CDN, share
   links, exports.
8. The incident specifics: who changed what, when, which surface still
   shows old authority, and the tells — works in incognito? fixes itself
   after re-login or "overnight"? wrong on one device only?

## Workflow

1. **Classify the change, and take the deny direction first.** Which
   event: member removal, role/permission revoke, logout, plan change,
   deletion, share revoke — and which direction failed: deny (the removed
   must LOSE access — the security case) or grant (the added must GAIN —
   the UX case). Deny gets designed and verified first. Run the
   discriminator now: if access never behaved correctly, stop and route
   (Stop Conditions).
2. **Build the surface inventory.** From
   [references/stale-authority-surface-map.md](references/stale-authority-surface-map.md):
   server session records; JWT/token claims; client stores and data
   caches; shared HTTP/CDN caches; in-process/distributed server caches;
   database session context; live realtime subscriptions; share links;
   entitlement resolution; search indexes; signed URLs. Mark which exist
   in THIS app — a surface that exists and is never dispositioned is the
   next incident.
3. **Locate the holder — the differential.** Use the tells: works in an
   incognito window → a client-side copy; fixes itself after a consistent
   interval → token claims (the interval is the access TTL) or a cache
   TTL; stops after reconnect → a live subscription; wrong on one app
   instance only → an in-process cache; wrong only in search → the index.
   Where evidence is ambiguous, compose `systematic-debugger`'s
   prediction-testing; this map supplies the hypotheses it ranks.
4. **State the revocation-latency bound.** Per change type, in writing,
   with an owner-confirmed number: "removed from a workspace means
   unreachable on every surface within N seconds." The deny-direction
   bound is the tightest and is a security parameter, not a tuning knob.
   This is the sibling of `caching-strategy-designer`'s consistency
   envelope, applied to authority — without the number, "immediately"
   silently becomes "at token expiry".
5. **Design propagation per surface — own the unowned, compose the
   owned.** The three surfaces this skill owns outright:
   - **Token/claims staleness.** If authority (role/tenant/plan) is baked
     into a stateless token, revocation latency equals the access-token
     TTL unless a server-side check exists. The menu, chosen against step
     4's bound: (a) short access TTL + refresh rotation — simplest;
     latency floor = the TTL; authority re-resolved at refresh time;
     (b) session-version / epoch — bump a per-user (or per-tenant)
     version on every authority change and check it server-side on each
     request — near-immediate; costs one indexed read per request, and
     that read must not itself be cached into staleness; (c) denylist the
     affected principal's tokens until natural expiry — targeted; needs a
     fast shared store; doubles as the logout kill. State the chosen
     latency; never imply immediate revocation from a stateless token
     alone.
   - **Server session records.** Logout and revocation invalidate
     server-side — the session record is deleted or version-bumped so a
     replayed cookie or token fails. Clearing the client is presentation,
     not revocation. Custody implementation hands to
     `secrets-identity-hardener` (manual-only) with the control named.
   - **Client-state purge.** On logout AND on received authority-change
     events: purge the query/data caches, state stores, and persisted
     storage carrying the old view. The server cannot reach these copies
     — design the signal (an authority-change event on an existing
     realtime channel, an authority version stamped on responses, or
     re-check on focus/refetch) plus the purge it triggers. The
     acceptance test is the shared-device case: sign in as a different
     user and nothing of the previous user's data renders.
   The per-surface owners are composed, never restated: shared/server
   cache purge mechanics → `caching-strategy-designer` (its
   authorization-caching Safety Rule governs any proposal to cache authz
   — cite it, never re-approve it here); mid-connection re-auth and
   subscription teardown → `realtime-subscription-architect`; plan
   resolution, plan-change invalidation, and billing-webhook lag →
   `plan-entitlement-architect`; share-link revocation →
   `share-link-access-architect`; RLS policy correctness →
   `rls-policy-auditor` (this skill owns the FRESHNESS of the claims and
   context feeding those policies, plus pool context reset); search-index
   deletion → `search-architecture-designer`; signed URLs and file CDN →
   `file-upload-storage-architect`.
6. **Design the verify battery — per surface, changed principal, deny
   first.** For the actual changed principal (not a fresh test user):
   before/after probes per inventoried surface — the API read is denied;
   the pre-change token/cookie is rejected within the bound; live events
   stop arriving; the client renders nothing stale after the purge
   signal; the search hit is gone; the old signed URL no longer resolves.
   Then the positive control (an unaffected user is unaffected) and the
   grant direction (a newly added member gains access without re-login,
   or the designed latency is stated). `authorization-matrix-designer`'s
   revoked-membership negative tests are the design-time DB/API subset of
   this battery; this step extends them across every live surface.
7. **Hand off implementation.** Deliver named controls: session/token
   custody changes → `secrets-identity-hardener`; cache, channel, plan,
   link, and index changes → their owners' outputs; anything touching
   live production state follows the ops approval path. This skill
   designs and specifies verification — it executes nothing against live
   systems.

## Output Format

```
AUTHORITY INVALIDATION DESIGN — <incident / change type>
Change: <removal|revoke|logout|plan-change|deletion|share-revoke> —
  direction: <deny|grant|both>; never-worked check: <behaved correctly
  before the change? yes → proceed | no → routed>
Revocation-latency bound: "<change> means <effect> on every surface within
  <N seconds>" (owner-confirmed)
Surface inventory (every row dispositioned):
  <surface> — exists? <y/n> — holder? <yes: evidence/tell | ruled out: how>
    invalidation: <owned design here | composed → owning skill>
    latency: <fits the bound? actual window>
    verify: <the before/after probe, deny direction>
Token/claims policy: <short-TTL+refresh | session-version/epoch | denylist>
  → revocation latency = <value>; logout kill = <mechanism>
Server sessions: <invalidated on logout/revoke; replay rejected>
Client purge: <signal → what is purged>; shared-device test: <designed>
Verify battery: <per-surface probes for the changed principal, deny then
  grant, plus the positive control>
Handoffs: <secrets-identity-hardener (custody impl) |
  caching-strategy-designer (cache mechanics) | realtime / plan /
  share-link / rls / search / file owners as routed>
```

## Validation Checklist

- [ ] The deny-direction revocation-latency bound is stated as a number
      and owner-confirmed — not "immediately", not implied.
- [ ] Every surface in the inventory is dispositioned — holder, or ruled
      out with evidence; none skipped because "we probably don't cache
      that".
- [ ] The token policy is chosen with its tradeoff and resulting latency
      stated; a stateless token is never presented as immediately
      revocable.
- [ ] Logout invalidates the server session, not just client state;
      replay of the old cookie/token is tested as rejected.
- [ ] Client purge fires on both logout and authority-change; the
      shared-device (next-user) case is in the battery.
- [ ] The battery tests the CHANGED principal per surface, deny direction
      first, then grant direction, plus a positive control.
- [ ] Composed surfaces are routed with their owner named — no cache-TTL,
      RLS-SQL, plan-resolution, or link-token content restated here.
- [ ] The never-worked discriminator was actually asked and recorded.

## Security Rules

- The deny direction is this skill's priority ordering: revoked access
  must actually revoke. Old authority honored after a change is
  unauthorized access to tenant data — the tenant-isolation harm arriving
  through time.
- A propagation design without a stated latency bound is not a design; it
  is the current bug with better documentation.
- UI disappearance is never propagation. Hiding the button, the menu
  item, or the list row while the session, token, or API still honors the
  old authority is the illusion of revocation.
- A stateless token's revocation latency is its access TTL unless a
  server-side check (session-version, denylist) exists — state which, and
  the resulting number, every time.
- Logout is a revocation event held to the same standard: it ends the
  server session and purges client state; anything less leaves the
  account open on the next shared device.

## Gotchas

- JWT claims are stale by design, not by bug: role/tenant/plan claims
  minted at sign-in do not observe the database change; managed-auth
  platforms (e.g. Supabase, Firebase) default access TTLs around an hour
  — the removal "not working" often just IS that TTL, chosen by nobody.
- The open-tab problem: a removed user's already-loaded app keeps a
  working token and rendered state; with no per-request server check and
  no purge signal, they retain full access until the token expires — no
  refresh needed on their part.
- The next-user-on-a-shared-device leak: persisted client caches survive
  logout, so signing in as user B briefly (or fully) renders user A's
  data. Purge on logout is a privacy control, not a nicety.
- Pooled database connections reuse session context: authorization
  context set for one request can leak into the next if the pool doesn't
  reset on checkout — the RLS policy is correct; its input is stale.
- Authority-change events not emitted from every change path — the admin
  bulk tool, the billing webhook, the support script: the
  missed-mutation-path class `caching-strategy-designer` names for caches
  applies equally to authority signals, and one missed path is a
  permanent hole.
- "Works in incognito" is diagnostic gold: a fresh profile has no client
  state and no cookies, so if incognito behaves correctly the holder is a
  client-side copy; if incognito is also wrong, the holder is
  server-side.
- The grant direction embarrasses quietly: the newly invited member can't
  see the workspace until they sign out and back in, because their claims
  were minted before the invite — the same mechanism as the security
  case, opposite direction, and usually the first symptom anyone actually
  reports.

## Stop Conditions

- Access never behaved correctly — no before-state in which the
  permission worked → stop; that is `authorization-matrix-designer` /
  `rls-policy-auditor` territory. This skill owns changes that failed to
  propagate, not authority that was never wired.
- Asked to execute the purge NOW against live systems — flush a
  production cache, kill live sessions, force-expire real users' tokens →
  stop; the design is the deliverable, execution follows the ops approval
  path (`human-approval-boundary`). Killing every session is a
  mass-logout event a human must own.
- A proposed "fix" is to cache an authorization result →
  `caching-strategy-designer`'s Safety Rule governs (an explicit approved
  envelope with a revocation-propagation bound); never green-light it
  from here.
- No owner will confirm a revocation-latency number → present the
  per-change default menu with consequences and stop; do not invent a
  deny-direction tolerance on anyone's behalf.
- The evidence shows a live cross-tenant leak (not stale authority of a
  formerly entitled principal) → stop and route to the isolation path —
  `rls-policy-auditor` / `tenant-isolation-reviewer` — that is an active
  incident, not a propagation design task.

## Supporting Files

- [references/stale-authority-surface-map.md](references/stale-authority-surface-map.md)
  — the per-surface map: where the old copy lives, the diagnostic tell,
  the invalidation options, the verify probe, and the owning skill to
  compose.
- `evals/evals.json` — behavior cases: the removed-user-still-sees
  diagnosis, the logout/shared-device edge, the cache-design non-trigger,
  and the live-purge stop.
- `evals/trigger-evals.json` — discrimination against
  `caching-strategy-designer`, `authorization-matrix-designer`,
  `rls-policy-auditor`, `realtime-subscription-architect`,
  `plan-entitlement-architect`, `share-link-access-architect`,
  `secrets-identity-hardener`, and `systematic-debugger`.
