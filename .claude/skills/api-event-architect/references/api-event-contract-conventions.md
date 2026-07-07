# API & Event Contract Conventions

Supporting detail for `api-event-architect`. Read on demand.

## Event envelope schema (versioned)

```json
{
  "id": "evt_<unique>",
  "type": "<domain>.<resource>.<action>",
  "schema_version": "1",
  "occurred_at": "<RFC3339>",
  "tenant_id": "<the subscribing tenant's id — always>",
  "payload": { "resource_id": "…", "changed": ["field", "…"] }
}
```

- `type` naming: `billing.invoice.created`, `projects.project.archived` —
  past-tense facts, never imperatives.
- Thin payloads by default: ids + changed-field names; consumers fetch
  current state via the API (which re-runs authorization). Full payloads
  only with a stated reason and a data-egress review.
- Schema evolution: additive within a version; anything else bumps
  `schema_version` and follows the deprecation sequence.

## Webhook delivery policy table (template)

| Property | Contract |
| --- | --- |
| Semantics | At-least-once; duplicates possible; consumer idempotency required (documented) |
| Ordering | Not guaranteed (or: per-resource-key ordering, only if truly implemented) |
| Retry schedule | e.g. exponential with jitter: 1m, 5m, 30m, 2h, 12h → dead-letter |
| Failure policy | After N consecutive dead-letters → subscription disabled + notification |
| Signing | HMAC-SHA256 over timestamp + body; per-subscription secret, rotatable with overlap window |
| Replay protection | Reject signatures older than tolerance (e.g. 5 min) |
| Redelivery | Manual redelivery window (e.g. 7 days) via API/console |
| Target validation | HTTPS only; SSRF checks; no redirect following |

## Consumer checklist (ships with the docs — part of the contract)

- Verify the signature and timestamp before parsing.
- Deduplicate by event `id` (at-least-once delivery).
- Return 2xx fast; process async — slow handlers get retried as failures.
- Do not depend on ordering; fetch current state via API when it matters.
- Rotate secrets on schedule; support two active secrets during overlap.

## Deprecation sequence template

1. **Announce** — changelog + direct notice to consumers of the affected
   version/field; minimum notice period stated (e.g. 6 months major, 90 days
   field-level).
2. **Dual-run** — old and new contracts both served; migration telemetry
   tracks remaining old-contract consumers.
3. **Warn** — sunset headers / deprecation warnings in responses; direct
   outreach to holdouts.
4. **Enforce** — old contract returns migration-pointer errors.
5. **Remove** — after a quiet period (rollback = re-extend sunset, so removal
   is last and reversible until it happens).
