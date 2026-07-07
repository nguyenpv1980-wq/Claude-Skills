# Entitlement Matrix & Transition Templates

Supporting detail for `plan-entitlement-architect`. Read on demand.

## Entitlement naming and typing

`<domain>.<noun>[.<qualifier>]` — e.g. `projects.max`, `api.access`,
`ai.credits.monthly`, `storage.gb`, `members.max`, `sso.enabled`.

| Type | Cell value | Needs |
| --- | --- | --- |
| Boolean feature | on / off | Enforcement check only |
| Numeric limit | max N (or ∞) | Current-count source + check at creation |
| Usage-metered quota | N per period | Metering event, idempotent counter, reset, over-quota behavior |

## Matrix template

| Entitlement ↓ / Plan → | Free | Pro | Enterprise | (Override column: data, not code) |
| --- | --- | --- | --- | --- |
| projects.max | 3 | 50 | ∞ | per-tenant row, owner + expiry |
| members.max | 2 | 20 | ∞ | |
| api.access | off | on | on | |
| ai.credits.monthly | 0 | 500 | 5000 | |
| storage.gb | 1 | 100 | 1000 | |
| sso.enabled | off | off | on | |
| audit.export | off | off | on | |

Every cell explicit. ∞ is a value, not an absent check — unlimited plans still
flow through the resolution point so a future cap is a data change.

## Plan-transition table template

| Transition | Trigger | Entitlement effect | Data effect | Communication |
| --- | --- | --- | --- | --- |
| Trial start | Signup | Trial column applies | — | Trial clock visible |
| Trial expiry | Clock | Drop to Free | Over-limit content read-only | Warn at T-7/T-1 |
| Upgrade | Payment | Immediate | Read-only content unlocked | Receipt + confirmation |
| Downgrade | User choice, period end | New plan at period end | Over-limit: read-only, never deleted | Explicit over-limit preview BEFORE confirm |
| Payment failure | Provider webhook | Grace period (full access), then suspend per lifecycle | Frozen, intact | Dunning sequence |
| Cancellation | User choice | End of paid period → offboarding posture | Export window per lifecycle | Confirmation + export link |

## Metering hook checklist (per metered entitlement)

- Counted event named, emitted at the service layer (not the UI), carrying
  tenant id + idempotency key.
- Counter storage tenant-scoped; period reset semantics (calendar month vs
  subscription anniversary) stated.
- Over-quota behavior chosen per entitlement: hard stop / soft warn /
  overage billing — and the API's over-quota status code documented.
- Retry/replay cannot double-count (idempotency key honored at the counter).
- Backfill/import paths count against quotas like any other path.
