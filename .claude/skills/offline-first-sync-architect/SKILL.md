---
name: offline-first-sync-architect
description: Design the client OFFLINE data layer for a multi-tenant SaaS — write-while-offline queue, optimistic apply + rollback on server reject, conflict detection/resolution (last-write-wins / field-merge / CRDT / manual), local persistence (IndexedDB/SQLite), background sync when connectivity returns, and online↔offline reconciliation with integrity. Produces the sync-engine design, the conflict-resolution policy, the local-store + queue schema, and the reconciliation contract. Use when the app must work offline or on flaky networks, when queued offline edits conflict on reconnect, or when optimistic updates get lost or duplicated. Do NOT use for the offline/optimistic-rollback UX STATES themselves (edge-state-ux-designer — it renders the state; this is the engine behind it), the server/distributed CACHE (caching-strategy-designer), or live ONLINE server→client push (realtime-subscription-architect — the in-batch seam). This designs the sync engine; conflicts that silently lose data are refused.
---

# Offline-First Sync Architect

## Purpose

Offline-first is easy to demo and hard to get right: the demo shows an edit
made on a plane appearing after landing; the incident is two people editing
the same record offline and one silently losing their work, or a queued write
replaying twice and creating a duplicate, or an optimistic update that the
server rejected still sitting on screen as if it succeeded. This skill designs
the client offline data layer so those failure modes are handled by design:
the write-while-offline queue, optimistic apply with rollback on reject,
explicit conflict detection and a resolution policy chosen with eyes open,
local persistence, background sync, and reconciliation that preserves
integrity. The deliverable is the sync-engine design, the conflict-resolution
policy, the local-store and queue schema, and the reconciliation contract.
The single non-negotiable: a conflict that silently discards a user's data is
a bug, not a strategy — this skill refuses it.

## Use When

- Use when: the app must work offline or on flaky/intermittent networks —
  field apps, mobile, spotty-connectivity workflows — and needs a real sync
  layer, not just a spinner.
- Use when: queued offline edits conflict on reconnect and you need a
  detection + resolution policy (last-write-wins, field merge, CRDT, or
  manual).
- Use when: optimistic updates are getting lost, duplicated, or stranded on
  screen after a server reject, and the apply/rollback path needs designing.
- Use when: designing the local store (IndexedDB / SQLite / equivalent), the
  outbound write queue, and background sync semantics.
- Do NOT use when: the task is the UX of offline/loading/optimistic/error
  STATES — how "saved locally, will sync" or a rollback is presented to the
  user — that is `edge-state-ux-designer`; this skill is the sync ENGINE
  behind those states, and the two compose.
- Do NOT use when: the task is the SERVER-side or distributed cache (what to
  cache server-side, TTLs, invalidation) — that is `caching-strategy-designer`;
  a client offline store is not a server cache.
- Do NOT use when: the task is live server→client push while ONLINE
  (WebSocket/SSE channels, presence, subscribe-time authz) — that is
  `realtime-subscription-architect`; realtime is the online-delivery
  counterpart and can be the transport this engine syncs over, but it is a
  distinct concern (the in-batch seam, pinned both ways).

## Inputs to Inspect

1. The offline requirement: which operations must work offline (read only?
   create? edit? delete?), for how long a device may be offline, and whether
   full offline or just resilience to blips.
2. The data shape: what is edited offline, its size (can it fit on-device),
   ownership (single-user records vs shared/collaborative), and how often two
   actors edit the same thing.
3. Concurrency reality: whether concurrent edits to the same record are
   common (drives conflict strategy) or rare (drives how much conflict
   machinery is justified).
4. The server write path (`command-gateway-architect` if present): whether
   writes are idempotent, carry a version, and can accept a client-generated
   id / idempotency key — the sync engine depends on this.
5. The tenant/auth model: how offline data is scoped and encrypted at rest on
   the device, and what happens to queued writes if the session/authority
   changes before they sync.
6. Existing behavior/pain: current optimistic-update handling, any incident
   history of lost edits or duplicate creates, and what "sync" does today.

## Workflow

1. **Scope the offline surface honestly.** Not everything needs to work
   offline. Classify operations: read-offline (cache + serve), create-offline
   (queue + optimistic), edit-offline (queue + optimistic + conflict risk),
   delete-offline (queue + tombstone). The more write surface offline, the
   more conflict machinery — justify each. Full offline for shared,
   frequently-co-edited data is the hardest case; say so.
2. **Design the local store and write queue.** The on-device store
   (IndexedDB/SQLite) holding the working data set and an ordered, durable
   outbound queue of pending writes. Each queued write carries: a
   client-generated id (idempotency key), the intended change, a base version
   (what the client last saw), and a timestamp. The queue survives app
   restart and is scoped/encrypted per the tenant/auth model.
3. **Design optimistic apply + rollback.** An offline write applies to the
   local store immediately (optimistic) and enqueues. On sync, if the server
   ACCEPTS, the optimistic state is confirmed; if it REJECTS (validation,
   authz, conflict), the optimistic change is ROLLED BACK locally and the UX
   is told (hand the rendering to `edge-state-ux-designer`). An optimistic
   update that is never confirmed or rolled back — left on screen as if saved
   — is the core bug to avoid.
4. **Design conflict detection.** On sync, compare the write's base version
   against the server's current version. Same → clean apply. Diverged →
   conflict. Detection requires versioning (version number / vector clock /
   updated-at), so specify it. "No conflict detection" means silent
   last-writer-clobbers, which is the failure this skill refuses.
5. **Choose a conflict-resolution policy with eyes open.** Per data type:
   - **Last-write-wins** — simple, but DISCARDS the loser's edit; acceptable
     ONLY for low-stakes, single-owner, or naturally-idempotent data, and
     the discard must be acknowledged, never silent.
   - **Field-level merge** — non-overlapping field edits both survive;
     overlapping fields still need a tiebreak.
   - **CRDT** — automatic convergence for collaborative data, at real
     complexity/size cost; justify it, don't default to it.
   - **Manual resolution** — surface both versions to the user (UX via
     `edge-state-ux-designer`) when data is high-stakes and merge is unsafe.
   State the choice, the data it applies to, and what it costs the loser.
6. **Design background sync.** When connectivity returns: drain the queue in
   order, apply idempotently (the server dedups on the client-generated id so
   a retried sync never duplicates), handle partial-sync failure (some writes
   accepted, some rejected) transactionally per-write, and back off on
   repeated failure. Reconnection uses `realtime-subscription-architect`'s
   channel where present, but the queue drain is this engine's job.
7. **Design reconciliation + integrity.** After a sync, the local store
   converges to the server truth: pull server changes since the last sync
   cursor, merge with local per the conflict policy, and verify integrity
   (no duplicated creates, no resurrected deletes, tombstones honored). State
   the sync cursor mechanism and how a long-offline device catches up (full
   refresh vs incremental).
8. **Deliver** the sync-engine design, conflict policy, local-store + queue
   schema, and reconciliation contract in the Output Format, UX and transport
   handoffs named.

## Output Format

```
OFFLINE-FIRST SYNC DESIGN — <system/domain>
Offline surface: <per operation: read/create/edit/delete — offline? — conflict risk>
Local store + queue: <store tech; working set; durable ordered queue; per write:
  client-id (idempotency), change, base version, timestamp; scoped/encrypted>
Optimistic apply/rollback: <apply local immediately; on accept confirm; on reject
  roll back + notify UX (→ edge-state-ux-designer); never leave unconfirmed-as-saved>
Conflict detection: <versioning mechanism (version/vector-clock/updated-at);
  base-version compare; diverged = conflict>
Conflict resolution (per data type): <LWW (with acknowledged discard) | field-merge
  | CRDT (justified) | manual (surface both)>; what it costs the loser stated
Background sync: <ordered drain; server dedups on client-id (no duplicate creates);
  partial-failure per-write; backoff; transport → realtime-subscription-architect>
Reconciliation: <sync cursor; pull-since; merge; integrity (no dup creates, no
  resurrected deletes, tombstones); long-offline catch-up>
Boundaries:     offline/rollback UX STATES → edge-state-ux-designer;
  server/distributed cache → caching-strategy-designer;
  live online push → realtime-subscription-architect
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] The offline surface is scoped per operation with conflict risk stated;
      not everything is made offline by reflex.
- [ ] The write queue is durable (survives restart), ordered, scoped/encrypted,
      and each write carries a client-generated idempotency id and a base
      version.
- [ ] Optimistic changes are always eventually confirmed or rolled back —
      none left on screen as saved after a server reject.
- [ ] Conflict detection exists via an explicit versioning mechanism; there is
      no silent last-writer-clobbers path.
- [ ] The conflict-resolution policy is chosen per data type with its cost to
      the loser stated; any discard (e.g. LWW) is acknowledged, never silent.
- [ ] Background sync dedups on the client-generated id so a retried sync
      never creates duplicates, and handles partial-failure per write.
- [ ] Reconciliation converges to server truth with a cursor and verifies
      integrity (no duplicate creates, no resurrected deletes, tombstones).
- [ ] UX states, server caching, and live online push are deferred to their
      owning skills.

## Gotchas

- Silent last-write-wins is the offline-first data-loss classic: two people
  edit offline, whoever syncs last wins, the other's work vanishes with no
  trace. LWW is a choice with a victim — acknowledge the discard or pick
  another policy.
- No idempotency id on queued writes means a retried sync creates duplicates:
  the create succeeded server-side, the ack was lost, the client retries, and
  now there are two. The client-generated id is what the server dedups on.
- An optimistic update with no rollback path strands rejected writes on screen
  as if saved; the user edits, sees success, and the change never persisted.
- Conflict resolution without version detection is not resolution — it is
  overwriting; you cannot resolve a conflict you cannot detect.
- CRDTs are not free magic: they add real size and complexity and change the
  data model. Reach for them for genuinely collaborative concurrent editing,
  not for a single-user notes app.
- A long-offline device that only ever does incremental sync can miss a
  server-side compaction/retention boundary and desync; design the full-
  refresh catch-up path.
- Deletes need tombstones: without them, a record deleted on the server
  resurrects from a still-offline device's local copy on next sync.
- Encrypting the local store is not optional for tenant data on a device that
  can be lost or stolen — offline data at rest is a real attack surface.

## Stop Conditions

- The chosen conflict strategy would silently discard user data (e.g. blanket
  last-write-wins on high-stakes, co-edited records) → STOP and surface the
  data-loss consequence; require an acknowledged policy (manual/merge) for
  that data rather than shipping a silent clobber.
- The server write path cannot accept a client-generated id / cannot dedup, or
  is non-idempotent → the sync engine cannot prevent duplicates; flag the
  server-side prerequisite (route to `command-gateway-architect`) before
  promising duplicate-free sync.
- Full offline is demanded for large, shared, frequently co-edited data where
  the device cannot hold the working set or conflicts would be constant →
  present the honest cost and the alternatives (online-required, partial
  offline) and stop for a human scope decision.
- Asked to build/run the sync against live data or apply a bulk reconciliation
  to production → this skill DESIGNS; executing a reconciliation/backfill
  against production follows the repo's approval path.

## Supporting Files

- `evals/evals.json` — behavior cases: the offline-layer design, the
  conflict-resolution edge, the silent-data-loss (LWW) refusal, and the
  live-online-push non-trigger.
- `evals/trigger-evals.json` — discrimination against `edge-state-ux-designer`
  (UX states vs sync engine), `caching-strategy-designer` (server cache vs
  client offline store), and `realtime-subscription-architect` (live online
  push vs offline sync — the in-batch seam, pinned both ways).
- No `references/` — the queue/optimistic/conflict/reconciliation procedure
  above is complete; detail lives in the produced artifacts.
