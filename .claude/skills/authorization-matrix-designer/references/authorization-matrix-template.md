# Authorization Matrix Templates & Negative-Test Catalog

Supporting detail for `authorization-matrix-designer`. Read on demand.

## Permission naming convention

`<verb>:<resource>` — e.g. `read:project`, `export:dataset`, `manage:billing`,
`invite:member`. Verbs from a closed set (read, create, update, delete,
export, share, invite, manage, impersonate). No role names inside permission
names; no plan names anywhere (that axis belongs to entitlements).

## Matrix template

| Permission ↓ / Role → | owner | admin | member | guest | support (brokered) | service-account |
| --- | --- | --- | --- | --- | --- | --- |
| read:project | ✓ | ✓ | ✓ | ✓(shared only) | ✓(grant) | ✓(scoped) |
| update:project | ✓ | ✓ | ✓(own) | — | — | — |
| export:dataset | ✓ | ✓ | — | — | — | — |
| manage:billing | ✓ | — | — | — | — | — |
| invite:member | ✓ | ✓ | — | — | — | — |
| impersonate:user | — | — | — | — | ✓(grant, time-boxed) | — |

Empty cell = denied. Parenthetical = object-level rule that further narrows
the allow. Every ✓ in the support column requires an active brokered grant
and emits an audit event.

## Enforcement-point map template

| Surface | Check location | Authoritative? |
| --- | --- | --- |
| UI | Hide/disable controls | No — UX only |
| API | Middleware + shared decision point | Yes |
| Service layer | Object-level rules at repository/service | Yes (object rules) |
| Background jobs | Job context carries actor + tenant; same decision point | Yes |
| Integrations/webhooks | Token scopes mapped to permissions | Yes |
| Admin console | Same shared decision point — no parallel logic | Yes |

## Negative-test catalog (minimum set)

- **IDOR probe:** member of tenant A requests tenant B's resource by id on
  every resource type → deny/404 per stated policy.
- **Vertical escalation:** member attempts admin-only action (invite, export,
  billing) via direct API call, not UI → denied.
- **Horizontal reach:** member A attempts update on member B's owned object
  where matrix says own-only → denied.
- **Revocation:** remove membership/role, then replay a previously successful
  request with the still-live session and API token → denied.
- **Impersonation expiry:** support acts after grant expiry / without grant →
  denied AND the attempt is audited.
- **Machine actor:** service account attempts an action outside its scoped
  permissions → denied (service accounts don't inherit human roles).
- **Disabled tenant:** any role attempts writes in a suspended tenant →
  denied per lifecycle posture.
