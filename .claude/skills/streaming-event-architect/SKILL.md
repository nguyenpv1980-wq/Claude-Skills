---
name: streaming-event-architect
description: Design the INTERNAL event/streaming data backbone between services and stores — topic/stream taxonomy, partitioning and key choice (ordering stated as "per key, unordered across keys"), delivery semantics stated honestly (at-least-once with idempotent consumers; "exactly-once" claims interrogated), consumer groups, retry/dead-letter policy with replay procedure, retention vs compaction, backpressure/lag handling, event-schema compatibility rules, and CDC ingestion from operational stores. This is the data PIPELINE inside the system; the external contract surface — public webhooks, partner event feeds, signed envelopes, tenant-scoped subscriptions — is api-event-architect and stays there. Use when designing internal event flow, choosing stream vs queue, fixing ordering/duplicate bugs, or designing CDC. Do NOT use for the audit trail (audit-log-architect) or deciding which workloads leave the operational store (operational-vs-analytical-splitter).
---

# Streaming Event Architect

## Purpose

Event pipelines fail in ways request/response systems never do: messages
arrive twice, out of order, late, or land in a dead-letter queue nobody
drains, and every one of those is a DESIGN outcome, not bad luck. This
skill produces the internal streaming backbone design — topics, keys,
partitions, delivery semantics, consumer layout, DLQ and replay, retention,
schema compatibility, and CDC ingestion — with each guarantee stated
honestly (what is ordered, relative to what key; what deduplicates, and
where). It owns the pipe BETWEEN internal components. The moment an event
crosses to an external consumer — a partner webhook, a public feed — the
contract belongs to `api-event-architect`, and this skill designs only how
the internal stream feeds it.

## Use When

- Use when: designing or overhauling how services exchange events
  internally — new event backbone, stream vs queue choice, topic layout.
- Use when: duplicate processing, out-of-order effects, growing consumer
  lag, or an overflowing dead-letter queue point to delivery-semantics
  design debt.
- Use when: designing CDC (change data capture) from an operational store
  into streams — including when `operational-vs-analytical-splitter`
  prescribed CDC and the transport now needs designing.
- Use when: event payload schemas keep breaking internal consumers and
  compatibility rules (registry, additive-only policy) need defining.
- Do NOT use when: the events are a PUBLIC or partner-facing contract —
  webhook delivery, signed envelopes, subscription scoping, external
  versioning/deprecation policy are `api-event-architect`; this skill stops
  at the boundary where the internal stream hands events to that layer.
- Do NOT use when: the "events" are the compliance audit trail — actor/
  action/outcome records with tamper-evidence and retention are
  `audit-log-architect`, even if they physically ride a stream.
- Do NOT use when: deciding WHETHER analytics/reporting workloads should
  move off the operational store — that decision is
  `operational-vs-analytical-splitter`; this skill designs the CDC/event
  transport after the split is decided.
- Do NOT use when: the payload evolution question is about DATABASE
  schema (tables/columns with deployed readers) — that is
  `schema-evolution-planner`.
- Do NOT use when: the concern is the worker EXECUTION model that consumes
  the stream — per-job retry/backoff, visibility timeouts, DLQ ownership,
  and tenant fairness are `background-job-orchestration-architect`; or live
  push to CLIENT connections (subscribe-time authz, fan-out,
  reconnect/replay) — that is `realtime-subscription-architect`. This skill
  designs the transport both consume, not what runs on top of it.

## Inputs to Inspect

1. The event inventory as it exists: what is published today, by whom,
   consumed by whom, at what volume and peak rate — from code, queue/topic
   configs, and any existing event docs.
2. Ordering and consistency requirements per flow: which effects must be
   sequenced (per entity? per tenant? globally?) and which are commutative.
3. Consumer failure behavior today: retry loops, DLQ existence and drain
   procedure (or absence), poison-message history.
4. The operational stores feeding CDC: write rates, transaction
   boundaries, and whether ordering across tables matters downstream.
5. Tenant model constraints (from `multi-tenant-data-architect` outputs if
   present): whether streams are tenant-mixed with keyed isolation or
   tenant-separated, and what tenant context every event must carry.
6. Existing schema/contract conventions: any registry or payload versioning
   already in force, and `api-event-architect` artifacts for events that
   ultimately feed external surfaces.

## Workflow

1. **Inventory flows and classify each.** For every producer→consumer
   flow: fire-and-forget notification, state-transfer (fact/event-carried
   state), or command. Volume, peak rate, and fan-out. Misclassified
   commands-as-events are a standing source of coupling — flag them.
2. **Choose the transport shape per flow.** Durable log/stream (replayable,
   multi-consumer, ordered per partition) vs work queue (competing
   consumers, ack/redeliver) — by fan-out, replay need, and ordering need.
   State the choice per flow, not one global answer.
3. **Design keys and partitions.** The partition key defines the ONLY
   ordering guarantee: state it as "ordered per <key>, unordered across
   keys". Key by the entity whose effects must sequence (commonly
   entity-id; tenant-id alone creates hot partitions for large tenants —
   note skew). Estimate partition counts from peak rate and consumer
   parallelism, with headroom for rebalancing.
4. **State delivery semantics honestly.** Default: at-least-once delivery
   with IDEMPOTENT consumers (dedup key = event id or business key;
   dedup-store retention stated). Interrogate any "exactly-once"
   requirement: end-to-end exactly-once across arbitrary side effects is
   not purchasable — what exists is transactional produce/consume within
   one platform plus idempotent effects at the edges. Design the
   idempotency mechanism per consumer.
5. **Design failure paths.** Retry policy (attempts, backoff, what
   distinguishes retryable from poison), dead-letter destination per
   consumer group, DLQ ownership (who is paged, drain SLA), and the REPLAY
   procedure: how a drained/fixed message re-enters, how a consumer replays
   a time/offset range, and what makes replay safe (the same idempotency
   from step 4).
6. **Set retention and compaction.** Per topic: time/size retention for
   event history vs compaction for latest-state-per-key; replay window
   consumers can rely on; storage cost note. Compaction changes semantics
   (intermediate events vanish) — mark topics where that is unacceptable.
7. **Define schema compatibility rules.** Registry discipline (schemas
   versioned and checked at produce time where tooling allows), additive-
   only within a major version, required-field addition = new major with a
   parallel-publish window, consumer tolerance rules (ignore unknown
   fields). Deprecation of an event version follows a stated window, and
   external-feeding events defer to `api-event-architect`'s contract.
8. **Design CDC ingestion where prescribed.** Capture mechanism
   (log-based preferred over polling — state why per store), transaction
   boundary handling, initial-snapshot + streaming handoff, and schema
   drift behavior (upstream DDL vs the stream schema — coordinate with
   `schema-evolution-planner` when the upstream table evolves).
9. **Address backpressure and lag.** Lag as a first-class signal per
   consumer group (alert threshold and owner — wiring via
   `observability-operator`), producer behavior when downstream is slow
   (buffer/block/shed, stated), and scaling rules for consumers.
10. **Deliver the design** in the Output Format, with per-flow guarantees
    and every handoff named.

Decision tables (stream vs queue, key choice, retention vs compaction,
CDC mechanisms) and the per-flow guarantee card format:
[references/backbone-decision-sheet.md](references/backbone-decision-sheet.md).

## Output Format

```
STREAMING BACKBONE DESIGN — <system/domain>
Flows:          <N producer→consumer flows, classified>
Per-flow card:
  <flow>: transport=<stream|queue> key=<key> ordering="per <key> only"
  delivery=at-least-once + idempotent consumer (dedup=<mechanism>)
  retry=<policy> DLQ=<dest, owner, drain SLA> replay=<procedure>
  retention=<time/size|compacted> schema=<version, compat rule>
Partitioning:   <counts, skew notes (tenant hot-key risk)>
CDC:            <sources, mechanism, snapshot policy, drift handling> | n/a
Backpressure:   <lag thresholds/owners; producer behavior when slow>
Boundaries:     external contracts → api-event-architect; audit trail → audit-log-architect;
                split decision → operational-vs-analytical-splitter (consumed, not made here)
Explicit non-guarantees: <what this design does NOT promise (e.g., cross-key ordering)>
```

## Validation Checklist

- [ ] Every flow has a stated ordering guarantee in "per <key>, unordered
      across <scope>" form — no unscoped "ordered" claims.
- [ ] No unqualified "exactly-once" anywhere; every consumer has a named
      idempotency mechanism with dedup-store retention.
- [ ] Every consumer group has retry policy, DLQ destination, DLQ owner,
      and a replay procedure — no dead-letter black holes.
- [ ] Retention/compaction stated per topic with the replay window
      consumers may rely on.
- [ ] Schema rules cover both directions: producer evolution policy and
      consumer tolerance policy.
- [ ] Tenant context: events carry it; hot-partition risk from tenant
      keying is assessed.
- [ ] The external boundary is explicit: which events feed
      `api-event-architect` surfaces and where the handoff happens.
- [ ] Explicit non-guarantees section is present and honest.

## Gotchas

- "Ordered" without a scope is a lie waiting to page you: streams order
  per partition key only. Cross-key and cross-topic sequencing requires
  design (sequence numbers, sagas), not assumption.
- Exactly-once marketing: platform transactions cover produce/consume
  within that platform; the moment a consumer touches an external system,
  you are back to at-least-once + idempotency. Say so in the design.
- Tenant-id as partition key concentrates your largest tenant on one
  partition — the noisy-neighbor problem reappears INSIDE the pipe. Key by
  entity within tenant, or accept and monitor the skew.
- DLQs without owners are where events go to die silently; a DLQ is only a
  safety mechanism if drain has an owner and an SLA.
- Replay without idempotency is an incident generator — replaying a day of
  events double-applies every non-idempotent effect.
- Compaction deletes history by design: a consumer needing every
  transition cannot read a compacted topic. Classify topics before
  enabling it.
- CDC initial snapshots on large tables can hammer the source store —
  snapshot strategy is part of the design, and its execution belongs in a
  `data-migration-runbook-author` runbook when it is a one-time move.
- Schema registries enforce shape, not meaning: a field renamed via
  delete+add passes additive checks while breaking every consumer
  semantically. Compatibility rules need review, not just tooling.

## Stop Conditions

- The events under design are actually a partner/public contract (signing,
  subscription management, external versioning) → stop and route to
  `api-event-architect`; designing them here creates a second, conflicting
  contract surface.
- A hard "exactly-once end-to-end" requirement survives interrogation as a
  business mandate → halt and surface the honest options (transactional
  scope limits + idempotent edges) to a human; do not paper over it with
  an unqualified guarantee.
- Ordering requirements conflict with throughput requirements (global
  ordering demanded at a volume one partition cannot carry) → present the
  tradeoff explicitly and stop for a human decision.
- The tenant-isolation posture for streams is undefined (mixed streams vs
  per-tenant separation has compliance implications) → obtain the tenant
  model from `multi-tenant-data-architect` outputs or a human before
  fixing keys and topics.
- Asked to also implement broker/platform configuration changes on live
  infrastructure → decline execution; this skill designs, and live config
  changes follow the repo's approval path.

## Supporting Files

- [references/backbone-decision-sheet.md](references/backbone-decision-sheet.md)
  — stream-vs-queue decision table, key-choice and skew analysis, retention
  vs compaction table, CDC mechanism comparison, per-flow guarantee card.
- `evals/evals.json` — behavior cases including the ordering-scope edge and
  the exactly-once refusal.
- `evals/trigger-evals.json` — discrimination against `api-event-architect`
  (THE seam), `audit-log-architect`, `operational-vs-analytical-splitter`,
  and `schema-evolution-planner`.
