---
name: realtime-subscription-architect
description: 'Design real-time client delivery for a multi-tenant SaaS — WebSocket / SSE / database-change subscriptions / presence: the channel/topic model, authorize-at-subscribe-time (the per-tenant AND per-user leak boundary, re-checked as authority changes — never trusting a client-named channel), fan-out, scaling stateful connections across nodes, backpressure and slow-consumer handling, reconnect with replay/resume, and presence/typing state. Produces the channel taxonomy, the subscribe-time authorization contract, and a connection-scaling plan. Use when adding live updates, presence, or a subscription feed to clients, or when a live channel leaks another tenant''s data. Do NOT use for the internal server-to-server event backbone (streaming-event-architect), the request/response API or outbound webhooks (api-event-architect), the offline write-sync engine (offline-first-sync-architect), or notification UX (notification-webhook-ux-designer).'
---

# Realtime Subscription Architect

## Purpose

Real-time features fail in two directions: they leak — a client subscribes
to a channel it names and receives another tenant's data — and they fall
over — stateful connections pile up on one node, a slow consumer backs up
the whole fan-out, and a reconnect storm after a blip takes the service
down. This skill designs live client delivery so neither happens: a channel
model whose authorization is checked at subscribe time (and re-checked as
authority changes), fan-out that scales across nodes, backpressure that
sheds or slows without collapsing, and reconnect with a defined replay/resume
window. The deliverable is a channel taxonomy, a subscribe-time
authorization contract naming the per-tenant AND per-user boundary, and a
connection-scaling plan. This skill owns the push to CLIENTS; the moment the
question is server-to-server event flow it belongs to
`streaming-event-architect`.

## Use When

- Use when: adding live updates, a subscription feed, collaborative
  presence, or typing/cursor state delivered to clients over WebSocket, SSE,
  or a database-change subscription.
- Use when: a live channel leaks data — a client receives events for a
  tenant, user, or resource it should not see — i.e. authorization is done
  at connect only, or not at all, or trusts a client-named channel.
- Use when: stateful connections do not scale — they pin to one node,
  reconnect storms overwhelm, or a slow client backs up delivery to others.
- Use when: designing reconnect semantics — what a client missed while
  disconnected and how much history it may replay on resume.
- Do NOT use when: the subject is the INTERNAL server-to-server event
  backbone — topics, partitions, consumer groups, DLQ, CDC — that is
  `streaming-event-architect`; this skill may CONSUME that backbone to push
  to clients, but it does not design it.
- Do NOT use when: the subject is request/response API design or OUTBOUND
  webhooks to partner servers — that is `api-event-architect`; webhooks are
  server-to-server push, not live client subscriptions.
- Do NOT use when: the subject is the client's OFFLINE write queue, optimistic
  apply, and conflict resolution — that is `offline-first-sync-architect`;
  this skill is live push while the client is ONLINE (the two compose: the
  realtime channel is a common online transport for the sync engine).
- Do NOT use when: the subject is the UX of notifications/toasts/in-app
  inbox — that is `notification-webhook-ux-designer`; this owns transport,
  not presentation.

## Inputs to Inspect

1. What must go live and to whom: the events, their audience (one user, a
   tenant, a shared resource's participants), volume, and per-client rate.
2. Current transport and authorization: WebSocket/SSE/DB-change subscription
   in use, and where (if anywhere) a subscription is authorized — connect
   only, per-subscribe, or per-message.
3. The tenant + authorization model (`multi-tenant-data-architect` /
   `authorization-matrix-designer` output): what defines whether an actor
   may see a given channel's stream, and whether authority can change
   mid-connection (role revoked, removed from a resource).
4. The connection topology: how many concurrent connections, on how many
   nodes, behind what load balancer, and whether any per-connection state
   lives in node memory today.
5. The event source feeding delivery: the internal backbone / DB change feed
   (from `streaming-event-architect` or the database) the channels fan out.
6. Reconnect reality: current reconnect behavior, whether clients miss
   events on a blip, and any incident history of reconnect storms.

## Workflow

1. **Model channels around authority, not convenience.** Define the channel
   namespace so the thing that is authorized IS the channel key — e.g.
   `tenant:<id>:resource:<id>`. The server derives the tenant/resource from
   trusted state; a client MUST NOT be able to subscribe to an arbitrary
   channel string it constructs. Enumerate channel types and their audience.
2. **Authorize at subscribe time — and re-check as authority changes.** The
   security property: a subscribe request is authorized server-side against
   the same policy the write path uses, at subscribe time. Connect-time-only
   authorization is insufficient because authority changes mid-connection
   (a user removed from a workspace must stop receiving its events). Define
   the re-authorization trigger (on authority-change event, on token
   refresh, or periodic) and the tear-down of now-forbidden subscriptions.
3. **State the leak boundary explicitly.** Per-tenant isolation is necessary
   but NOT sufficient: within a tenant, a user may see only channels they
   are entitled to. Write the boundary as "tenant AND per-user/per-resource"
   and make every fan-out filter honor it — never broadcast a tenant-wide
   stream and filter on the client.
4. **Design fan-out.** How an event reaches every entitled connection across
   nodes: a shared pub/sub or presence backbone that any node can publish to
   and every node subscribes to for its local connections. State the source
   (consume the internal backbone; do not re-invent it) and the delivery
   filter that applies the leak boundary at the edge.
5. **Scale stateful connections.** Connections are long-lived and pin
   resources: state the per-connection memory cost, the node fan-out limit,
   how the load balancer handles sticky vs any-node connections, and how a
   node draining (deploy/scale-in) hands its connections off — clients
   reconnect and resume, they are not silently dropped. (Statelessness /
   drain review composes `horizontal-scalability-reviewer`.)
6. **Handle backpressure and slow consumers.** A client that cannot keep up
   must not back-pressure everyone else: per-connection send buffer with a
   bound, and a policy when it overflows (drop-oldest for state-transfer
   channels, disconnect-and-let-resume for others, or coalesce). Name the
   choice per channel type; unbounded server-side buffering is a memory-leak
   outage waiting to happen.
7. **Design reconnect and replay.** On reconnect: does the client get a
   fresh snapshot, or replay events since a cursor/offset? State the resume
   window (how far back), the cursor mechanism, and dedup so replay does not
   double-apply. Add reconnect jitter/backoff to prevent thundering-herd
   reconnect storms after a blip.
8. **Design presence** where needed: how presence/typing state is tracked
   (heartbeat + TTL), that it is soft state (rebuilt on reconnect, never the
   source of truth), and its own per-tenant/per-resource authorization.
9. **Deliver** the channel taxonomy, subscribe-time authz contract, and
   scaling plan in the Output Format, with every source and handoff named.

## Output Format

```
REALTIME DELIVERY DESIGN — <system/domain>
Transport:      <WebSocket | SSE | DB-change subscription> + why
Channel taxonomy: <channel type — key format (server-derived) — audience>
Leak boundary:  tenant AND <per-user/per-resource>; filter applied at <edge>
Authz contract: authorize at SUBSCRIBE (policy source); re-check on
  <authority-change trigger>; tear down forbidden subscriptions on <event>
Fan-out:        <pub/sub backbone; source = internal backbone (consumed);
  cross-node delivery; edge filter enforcing the leak boundary>
Connection scaling: <per-conn cost; node limit; LB sticky/any-node; drain →
  reconnect-and-resume handoff>  (drain review → horizontal-scalability-reviewer)
Backpressure:   <per-conn buffer bound; overflow policy per channel type>
Reconnect/replay: <snapshot vs cursor replay; resume window; dedup;
  reconnect backoff/jitter>
Presence:       <heartbeat+TTL, soft-state, own authz> | n/a
Boundaries:     internal backbone → streaming-event-architect; API/webhooks →
  api-event-architect; offline sync → offline-first-sync-architect;
  notification UX → notification-webhook-ux-designer
```

## Validation Checklist

- [ ] Channel keys are server-derived from trusted state; a client cannot
      subscribe to an arbitrary channel string it constructs.
- [ ] Authorization happens at subscribe time and is re-checked as authority
      changes — connect-time-only is called out as insufficient.
- [ ] The leak boundary is stated as tenant AND per-user/per-resource, and
      the fan-out filter enforces it server-side (no client-side filtering
      of a tenant-wide broadcast).
- [ ] Fan-out crosses nodes via a named backbone; the internal event source
      is consumed, not re-designed here.
- [ ] Stateful connections have a per-node limit and a drain/handoff plan;
      clients reconnect-and-resume rather than being silently dropped.
- [ ] Backpressure has a bounded per-connection buffer and an overflow policy
      per channel type — no unbounded server-side buffering.
- [ ] Reconnect defines the resume window, cursor/dedup, and backoff to
      prevent reconnect storms.
- [ ] Presence is treated as soft state with its own authorization.

## Gotchas

- Authorizing at connect only is the classic realtime leak: the user removed
  from a workspace keeps receiving its live events until they disconnect.
  Authority is re-checked, or the boundary is a lie between refreshes.
- Broadcasting a tenant-wide stream and filtering on the client hands every
  client every tenant-mate's data over the wire — the filter must be
  server-side, at the fan-out edge.
- A client-constructed channel name (`subscribe("tenant:42:...")`) is IDOR
  over WebSocket; the channel key must be derived from the actor's trusted
  scope, not accepted from the frame.
- Unbounded per-connection send buffers turn one slow mobile client into an
  OOM: bound the buffer and define overflow behavior, or a bad network is a
  server outage.
- Reconnect without jitter is a thundering herd: a 2-second blip reconnects
  every client at once and the reconnect load exceeds the steady load.
- Presence treated as source of truth strands ghosts: a crashed client's
  presence lingers without a heartbeat TTL. Presence is soft state, rebuilt
  on reconnect.
- Sticky sessions "solve" stateful connections until a node dies with all
  its state; design the drain-and-resume path, don't assume the node lives.

## Stop Conditions

- The authorization model that decides who may subscribe to a channel does
  not exist or cannot express per-resource visibility → obtain it from
  `authorization-matrix-designer` / `multi-tenant-data-architect` before
  designing channels; a subscribe-time check against an undefined policy is
  a false assurance.
- The request is actually to design the internal server-to-server event
  backbone (topics, partitions, DLQ, CDC) → route to
  `streaming-event-architect`; designing it here creates a second,
  conflicting pipeline.
- Delivering the required volume with the required per-user isolation exceeds
  what the connection topology can carry (e.g. millions of concurrent
  connections with per-message authz) → present the scaling tradeoff and
  stop for a human infrastructure decision rather than asserting it scales.
- Asked to reconfigure live load-balancer/connection infrastructure → this
  skill DESIGNS the topology and drain plan; executing infra changes follows
  the repo's approval path.

## Supporting Files

- `evals/evals.json` — behavior cases: the live-feed design, the presence +
  fan-out edge, the authorize-only-at-connect leak refusal, and the
  internal-backbone non-trigger.
- `evals/trigger-evals.json` — discrimination against
  `streaming-event-architect` (THE seam — internal backbone vs client push),
  `api-event-architect`, `offline-first-sync-architect` (the in-batch
  online-push vs offline-sync seam), and `notification-webhook-ux-designer`.
- No `references/` — the channel/authz/scaling procedure above is complete;
  detail lives in the produced artifacts.
