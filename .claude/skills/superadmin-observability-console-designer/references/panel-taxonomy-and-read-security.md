# Panel taxonomy & the cross-tenant read-security model

Reference for `superadmin-observability-console-designer`. Generalized from
three independent production multi-tenant implementations that converged on
the same security core; product-agnostic by construction. Sections: the
read-security model (1), the panel menu (2), the server-shaped read model
(3), the DB/query-performance panel spec (4), posture-as-verification (5),
honest-gap typing (6).

## 1. The cross-tenant read-security model

The single most important part of the design. All elements below were
independently converged on; treat them as the core, not options.

### 1.1 The platform-admin registry

- A small dedicated table of user ids (optionally tiered roles), SEPARATE
  from end-user and tenant roles. Never a boolean flag on the user profile;
  never derivable from any tenant role — tenant-role escalation must be a
  dead end.
- Record grant provenance in the registry itself: `granted_by`,
  `granted_at`, and a free-text `note`.
- Prefer **deny-all RLS** on the registry: even members cannot read it from
  the client (`USING (false)` for all client roles); only the privileged
  server lane consults it. The weaker variant (members read their own row
  only) is acceptable; the roster of who holds God-mode is itself sensitive
  data, so prefer deny-all.
- The UI learns whether to render the console by ASKING the server (a
  status endpoint that answers from the registry) — the server tells the
  UI, never the reverse.

### 1.2 No self-service grant

No API, command, or UI grants platform-admin. Grants happen out-of-band
through the privileged operational lane (service credential / direct SQL by
an authorized human), under the repo's approval path. Any in-product
"promote to platform admin" button is a finding.

### 1.3 Three-layer server-side re-check

Checked independently at every layer, so bypassing one still hits the next:

1. **UI guard** — redirect/hide only. Cosmetic. Assume it is bypassed.
2. **Endpoint** — every privileged endpoint re-derives the actor FROM THE
   VERIFIED TOKEN (client-supplied user ids are ignored), then re-checks the
   registry per request. Deny → 403 + a logged denial event.
3. **Table** — every platform-scope table's SELECT policy gates on the same
   membership check, so a bypassed or buggy endpoint still hits the
   database wall.

One SECURITY-DEFINER membership function (`is_platform_admin(uid)`-shaped)
backs all three layers, so the check cannot drift between them. Prefer a
shared server-side auth helper over per-endpoint hand-rolled preambles —
dozens of hand-rolled copies of the same check WILL drift.

### 1.4 Read-only by default; privileged-write-only telemetry

- The monitoring console is overwhelmingly SELECT. Admins get SELECT-only
  policies on telemetry, audit, alert, and snapshot tables.
- ALL writes to those tables go through the privileged lane (service
  identity / SECURITY-DEFINER producers with EXECUTE revoked from client
  roles). An admin — or an attacker holding an admin session — cannot
  fabricate or tamper with what the console displays.
- Cross-tenant ACTIONS (suspend, provision, purge, config change) never
  ride the read console's queries; they route through the separate mediated
  command path (`admin-console-architect`), with their own per-command
  authorization and audit.

### 1.5 Audit everything — including denials

- Every superadmin action lands in a platform-scope audit trail (actor id
  and email snapshot, action, target, old/new values where applicable) —
  written only by the privileged lane, invisible to tenants. The substrate
  and schema are `audit-log-architect`'s; this console contributes the
  platform-tier read rules and the reader panel.
- Denied privileged-access attempts are logged AND surfaced as first-class
  console metrics ("denied superadmin requests" on the health panel).
  Watching the watchers is a display requirement.

### 1.6 Break-glass content reveal (the read path's exception)

Seeing metrics is a role; seeing a user's CONTENT is an audited exception.
Five checkable properties, enforced in order, server-side:

1. Caller's registry role is operational and NON-executive (rank ≠ reach —
   the most senior business role is structurally barred from raw content).
2. A reason code (from a small taxonomy) plus a free-text note.
3. A reference to an incident that EXISTS and is OPEN (resolved incident →
   blocked).
4. Scope narrowed to that incident's subject: an open incident for one
   account unlocks only that account's items.
5. The audit row (action, reason code, note, incident id, role) is written
   BEFORE the content is returned — audited-by-construction, not
   best-effort.

This is complementary to `admin-console-architect`'s break-glass ELEVATION
(time-boxed approved access to ACT): elevation grants action authority;
content reveal is the read path's own narrow exception. A design needs
both, and they must not be merged into one loose "break-glass" switch.

### 1.7 Two caller lanes

- **Human lane**: verified token → registry check, per request.
- **Machine lane**: cron/scheduled callers authenticate with a dedicated
  secret or service identity — never a human's token. Fire-and-forget where
  possible (the evaluator writes; it does not read back).
- Destructive batch operations (retention pruning, expiry sweeps) accept
  only NARROWING filters: a scoping parameter can shrink the affected set,
  never widen it.

## 2. The panel menu (select from it; do not fill it)

Grouped IA with one health answer first. Collapsed groups show an
escalation badge (e.g. a critical-incident dot) so nothing urgent hides.
The default view answers "is everything OK"; everything else is drill-down.

| Group | Panels (menu, not quota) | Feed owner to cite |
| --- | --- | --- |
| **Overview** | the one health answer: rollup counts, open incidents, breach badges; platform stats | composed from the groups below |
| **Customers & Billing** | signup/trial funnel, activation, per-tenant rollups, at-risk detection; infra + per-provider cost vs revenue; AI token spend | `product-analytics-instrumenter` (growth events), `usage-metering-and-cost-attribution-pipeline-designer` (metering ETL), `ai-cost-guardrail-designer` (AI spend), `saas-cost-architect` (unit economics) |
| **Security & Access** | security-event feed, denied-access counts, posture scans, the platform audit-log reader | `security-logging-alerting-architect` (detections/rules), `audit-log-architect` (substrate) |
| **Operations & Reliability** | health rollup, acknowledgeable alerts, incidents, capacity forecast, DB monitor (§4), cron/job liveness (heartbeats) | `slo-reliability-architect` (SLOs/what pages), `incident-response-runbook` (playbook), `observability-operator` (backend wiring) |
| **Verification** | synthetic-probe results, regression runs, isolation/posture scan results | `synthetic-monitoring-architect` (probes), `rls-policy-auditor` / `tenant-isolation-reviewer` / `multi-tenant-security-tester` (the scanned disciplines) |
| **Support** | account list, per-account detail, support notes (reason-carrying), entitlement grants | `plan-entitlement-architect` (entitlements); support ACTIONS → `admin-console-architect` |
| **Meta** | runbooks in-console; the known-gaps page (§6) | `incident-response-runbook`; this skill |

Tenant-ranking views (leaderboards, per-tenant drill-downs) are sensitive
panels in their own right — platform-scope access rules, never embedded in
tenant-facing surfaces.

## 3. The server-shaped read model

- One privileged call returns the console's data as typed panel blocks; the
  client renders, it never composes privileges. No client-side privilege
  logic; no dozens of raw table queries from the browser.
- Each block is typed, including its gap state (§6).
- **The growth tradeoff**: a monolithic summary accretes every panel and
  grows unbounded — in practice it becomes a screen-plus of type and the
  platform's heaviest query. Split by panel group (one call per group, same
  security model) once the summary exceeds a screen of type definitions.

## 4. The DB/query-performance panel spec

The most commonly missing panel — ask for it explicitly.

**Surface:**

- Connection-pool saturation: active vs max connections, warn ~70% / crit
  ~85% — the leading indicator of the classic serverless-meets-Postgres
  failure.
- Cache-hit ratio (warn <95%, crit <90%), total DB size, top-N tables by
  row estimate + disk size.
- Slow queries: in-flight queries above a threshold, with duration, state,
  a truncated query preview, user, and application name.
- Capacity runway: a forecast (e.g. weeks until connection exhaustion at
  current trend) with statistical gating (minimum samples, sustained-trend
  requirement, an emergency floor that bypasses the gate) so a single
  cron-aligned spike cannot page anyone.

**Mechanics:**

- Privileged SECURITY-DEFINER routines read the DB's own stats views
  (activity, database, table stats); EXECUTE revoked from client roles.
- A cron job snapshots into history tables the console charts; threshold
  breaches create acknowledgeable alert rows (severity, metric, current vs
  threshold, acknowledged_by/at).
- The producer prunes its own retention (e.g. days-scale history) — see
  Gotchas on OLTP-resident telemetry.

**Two honest limits (state them in the design):**

1. Sampling live activity on a tick misses queries that complete between
   ticks; pair with cumulative query-statistics infrastructure where the
   platform offers it, and name the blind spot where it doesn't.
2. This panel is the one most often absent entirely — its absence must be a
   typed known gap, not silence.

## 5. Posture-as-verification-results

Security/QA posture panels display scheduled verification OUTCOMES, not
assertions:

- Isolation scans: the RLS/tenancy verification disciplines run on a
  schedule, recording per-table pass/fail/warning under a scan id with
  who-ran-it.
- Synthetic probe results and their run history
  (`synthetic-monitoring-architect`'s prod-safety contract governs the
  probes themselves).
- Regression/test-run results where the platform records them.
- "Covered by tests" claims rendered as status, tied to the covering suite.

Posture = the latest verification result with its timestamp. A green badge
without a run date is an assertion, not posture. Surface the
DB-native-vs-external-backend decision here with the self-monitoring caveat
named: first-party telemetry in the product's own DB means a DB outage
blinds the console exactly when it is needed; external synthetic probes are
the mitigation lane.

## 6. Honest-gap typing

- A panel with no data source ships as `wired: false` plus a human-readable
  message — a typed, rendered placeholder, not an omission.
- The console carries a known-gaps page listing what it cannot see and why.
- "Not wired" is itself a monitoring datum: it tells the operator where
  confidence must NOT be placed. A console that silently omits what it
  cannot see teaches false confidence — the quietest failure mode a
  monitoring surface has.
