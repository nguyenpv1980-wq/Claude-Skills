# Audit Event Taxonomy (Starter)

Supporting detail for `audit-log-architect`. The taxonomy is a completeness
contract: an action not listed is an explicit exclusion, not an oversight.

| Category | Must-record actions | Grain guidance |
| --- | --- | --- |
| Authentication | Login success/failure, logout, MFA enroll/remove, password reset, session revocation, API key create/revoke | Per event; failures included (they are the security signal) |
| Access-control changes | Role grant/revoke, permission change, membership add/remove, invitation sent/accepted/revoked, ownership transfer | Per event, fail-closed category |
| Data access & export | Export requested/completed/downloaded, bulk read, report generation, search over sensitive scopes | Reads may be coarsened (export-level, not row-level) — stated decision |
| Admin & support actions | Impersonation grant/start/end, support view of tenant data, config change, feature-flag override per tenant | Per event, fail-closed; on-behalf-of mandatory |
| Security events | Isolation-denial hits, rate-limit trips on auth, anomalous access patterns flagged | Per event or aggregated-with-count; never dropped silently |
| Billing & plan | Plan change, entitlement override create/expire, payment method change, refund | Per event |
| Tenant lifecycle | Provision, suspend, resume, offboard start, export delivered, purge executed (with approval reference) | Per event; purge event survives the purge |

## Record schema (field starter)

`event_id` (unique, ordered), `schema_version`, `occurred_at` (authoritative
clock), `tenant_id` | `platform`, `actor` {type: user/service/support, id},
`on_behalf_of` (impersonation), `action` (taxonomy key), `target` {type, id},
`outcome` (success/denied/failed), `correlation_id`, `origin` {ip, agent — per
policy}, `details` (redacted, schema-versioned payload).

## Grain and volume notes

- Coarsen reads, never coarsen writes or access-control changes.
- Aggregation (e.g., "N failed logins in window") is acceptable for
  security-signal categories if the raw signal feeds detection elsewhere;
  record the aggregation rule in the design.
- Partition or roll storage by time; retention jobs delete whole partitions
  past retention — the ONLY sanctioned deletion path, running under a
  dedicated role, itself audited.
