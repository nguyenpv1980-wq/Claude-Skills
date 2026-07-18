---
name: superadmin-observability-console-designer
description: Design the cross-tenant superadmin OBSERVABILITY/monitoring console for a multi-tenant SaaS — the surface operators use to SEE platform health (signups, DB health, security, cost, incidents): layered panel IA (one health answer first, drill-downs, escalation badges, restraint), the cross-tenant READ-security model (deny-all-RLS platform-admin registry, no self-service grant, three-layer server-side re-check, read-only-by-default with privileged-write-only telemetry, denied-access-as-metric, break-glass CONTENT reveal), a server-shaped read model, honest-gap typing (wired: false), and the DB/query-perf panel. Every panel's feed is COMPOSED from its owning skill, never restated. Use when designing a superadmin/platform-health monitoring console — what it shows, how it is secured. Do NOT use for cross-tenant ACTIONS/impersonation/break-glass ELEVATION (admin-console-architect), wiring/operating the telemetry backend (observability-operator), or deciding SLOs/what pages (slo-reliability-architect).
---

# Superadmin Observability Console Designer

## Purpose

The superadmin observability console is the surface platform operators use to
SEE a multi-tenant SaaS — signups, database health, security posture, audit
trails, cost, incidents — across every tenant at once. That reach makes it
the most dangerous read surface in the product: it is exempt from the tenant
scoping every other query lives under, and designed carelessly it defeats
every isolation guarantee the platform makes. It is also an ownership hole:
`admin-console-architect` owns the surface operators act THROUGH and
explicitly excludes telemetry; `observability-operator` operates the
telemetry backend and designs no console; `slo-reliability-architect` decides
what pages. Nobody designs the console itself. This skill fills that hole. It
produces the console architecture: the layered panel IA, the cross-tenant
READ-security model, the server-shaped read model, per-panel feed contracts
with honest-gap typing, the DB/query-performance panel spec, and the
break-glass content-reveal design. It is a DESIGN skill — it produces
architecture and enforcement designs, edits no live config, and grants no
access — so it is safe for model invocation.

## Use When

- Use when: designing or overhauling a superadmin / platform-admin
  MONITORING or observability console or dashboard — the in-product surface
  where operators see cross-tenant platform state.
- Use when: asked "what should my superadmin panel show, and how do I secure
  it?"
- Use when: building an operator console to SEE signups, DB/query
  performance, security events, audit logs, cost, or incidents across
  tenants.
- Use when: an existing admin area is accreting ad-hoc metrics pages and
  needs a deliberate IA and a read-security model.
- Do NOT use when: the task is cross-tenant ACTIONS — impersonation, support
  writes, break-glass ELEVATION (time-boxed approved access to ACT), or the
  operator control-plane (retry/failover/data-repair) — that is
  `admin-console-architect`: seeing is not acting, and the two consoles are
  different trust surfaces. The two break-glass clauses are complementary,
  not duplicates: that skill owns elevation to act; this skill owns the
  narrower CONTENT-reveal exception in the read path (Workflow step 7).
- Do NOT use when: the task is instrumenting a service or wiring/operating
  the telemetry stack — dashboards and alert rules in a Grafana-class
  backend — that is `observability-operator` (manual-only): it operates the
  stack; this skill designs the in-product console that surfaces it.
- Do NOT use when: the task is a panel's FEED rather than the console:
  deciding SLOs / what pages → `slo-reliability-architect`; the audit
  substrate (taxonomy, schema, integrity, retention) → `audit-log-architect`;
  which security events to detect and alert on →
  `security-logging-alerting-architect`; synthetic probes →
  `synthetic-monitoring-architect`; the metering/cost ETL →
  `usage-metering-and-cost-attribution-pipeline-designer`; the authorization
  POLICY → `authorization-matrix-designer` (this skill designs the read-path
  ENFORCEMENT of that policy).

## Inputs to Inspect

1. The tenancy model: what a tenant is, where the tenant key lives, and
   which tables are platform-scope (no tenant dimension) vs tenant-scope —
   the console reads across both.
2. What telemetry already exists and who owns each feed: audit tables,
   security-event logs, metering/usage tables, probe results, incident
   records — map each to its owning skill's artifact before designing a
   panel over it.
3. The platform-admin identity source: how "platform operator" is
   represented today (a dedicated registry table? a role flag on the user
   profile? nothing?) — a profile flag or a tenant-role escalation path is a
   finding to correct, not an input to preserve.
4. The authorization policy for platform roles
   (`authorization-matrix-designer` output): which platform roles exist and
   what each may see; if absent, that is a Stop Condition.
5. Which panels the operators actually need: interview for the operator's
   questions (is the platform healthy? who signed up? what does it cost? are
   we under attack?) rather than transplanting the full taxonomy.
6. The incident model and runbooks (`incident-response-runbook` output):
   break-glass content reveal links to an OPEN incident, so the incident
   object must exist first.
7. The database platform's own stats surfaces (for the DB panel): what the
   DB exposes about connections, cache behavior, table sizes, and live vs
   cumulative query activity.

## Workflow

1. **Define the platform-admin read-security model FIRST — before any
   panel.** The console's power is its read scope, so the read scope is
   designed before what it renders:
   - A dedicated **platform-admin registry**: a small table of user ids,
     SEPARATE from end-user/tenant roles — never a profile flag, never
     reachable by tenant-role escalation. Record grant provenance
     (granted_by, granted_at, note). Prefer **deny-all RLS**: even members
     cannot read the registry from the client; only the privileged server
     lane consults it — the God-mode roster is itself sensitive.
   - **No self-service grant path.** No API, command, or UI grants
     platform-admin; grants happen out-of-band through the privileged
     operational lane, under the repo's approval path
     (`human-approval-boundary`).
   - **Three-layer server-side re-check, independent at every layer:**
     (1) the UI guard is cosmetic (redirect only); (2) every privileged
     endpoint re-derives the actor FROM THE VERIFIED TOKEN — client-supplied
     ids are ignored — and re-checks the registry per request; (3) every
     platform-scope table ALSO gates SELECT on the same membership check, so
     a bypassed endpoint still hits the database wall. One SECURITY-DEFINER
     membership function (`is_platform_admin(uid)`-shaped) keeps all three
     layers consistent.
   - **Two caller lanes**: human admins (token → registry check) and machine
     callers (cron/schedulers via a dedicated secret or service identity),
     the machine lane fire-and-forget where possible. Destructive batch
     operations accept only NARROWING filters — a scoping parameter can
     shrink the affected set, never widen it.
2. **Design the panel taxonomy and layered IA — with restraint.** One health
   answer first: the top level answers "is everything OK" (counts, open
   incidents, breach badges). Grouped drill-down panels behind it — Overview
   / Customers & Billing / Security & Access / Operations & Reliability /
   Verification / Support — with collapsed groups showing an escalation
   badge so nothing urgent hides behind a closed section. RESTRAINT is the
   stated principle: the default view answers one question; walls of metrics
   are opt-in — the everything-at-once dashboard is the anti-pattern. Select
   panels from the menu in
   [references/panel-taxonomy-and-read-security.md](references/panel-taxonomy-and-read-security.md);
   it is a menu to select from, not a quota to fill.
3. **Design the server-shaped read model.** The console reads a
   purpose-built, server-composed summary — one privileged call returning
   typed panel blocks — not dozens of raw client queries. The server decides
   what an admin may see; no client-side privilege logic. Manage the
   tradeoff: a monolithic summary grows unbounded — split it by panel group
   once it exceeds a screen of type definitions.
4. **Per panel: name the feed owner, the read scope, and the gap type.**
   Every panel's DATA is produced by an owning skill — cite it and route to
   it; never re-derive its content here. Reliability panels display what
   `slo-reliability-architect` defined; the audit reader displays
   `audit-log-architect`'s substrate (this skill designs the platform-tier
   read rules and the viewer, not the schema); security panels display
   `security-logging-alerting-architect`'s detections; verification panels
   display `synthetic-monitoring-architect`'s probe results; cost panels
   display the `usage-metering-and-cost-attribution-pipeline-designer` ETL's
   rollups plus `ai-cost-guardrail-designer`'s AI-spend telemetry; growth
   panels display `product-analytics-instrumenter`'s events; the incident
   panel serves `incident-response-runbook`'s playbook. Type every panel
   `{feed-owner, read-scope, wired?}`: a panel with no data source ships as
   `wired: false` plus a message, and the console carries a known-gaps page
   — a console that silently omits what it cannot see teaches false
   confidence; "not wired" is itself a monitoring datum.
5. **Spec the DB/query-performance panel** (the most commonly missing one —
   full spec in the reference): connection-pool saturation (active vs max,
   ~70%/85% warn/crit), cache-hit ratio, DB size, top-N per-table rows +
   disk, slow queries (duration, state, truncated preview, user), and a
   capacity-runway forecast with statistical gating. Fed by privileged
   SECURITY-DEFINER routines over the DB's own stats views, snapshotted on a
   cron into history tables the console charts, with the producer pruning
   its own retention. State the two honest limits: sampling live activity
   misses queries that complete between ticks (pair with cumulative
   query-stats where available), and this panel is the one most often absent
   entirely.
6. **Design posture panels as verification results.** Security/QA posture
   panels DISPLAY scheduled verification OUTCOMES — isolation scans (the
   `rls-policy-auditor` / `tenant-isolation-reviewer` /
   `multi-tenant-security-tester` disciplines run on a schedule with
   recorded pass/fail), synthetic runs, regression results. Posture = the
   latest verification result, not an assertion. Surface the
   DB-native-vs-external-backend decision with the self-monitoring caveat
   named: telemetry in the product's own DB means a DB outage blinds the
   console exactly when it is needed; external synthetic probes are the
   mitigation.
7. **Design break-glass content reveal and denied-access-as-metric.** Seeing
   metrics is a role; seeing a user's CONTENT is an audited exception with
   five checkable properties: a non-executive operational role + a reason
   code and free-text note + a link to an OPEN incident + scope narrowed to
   that incident's subject + the audit row written BEFORE the content is
   returned. Corollary: RANK ≠ REACH — the most senior business role sees
   aggregates and is structurally barred from raw content. Every privileged
   action is audited — INCLUDING denials: denied privileged-access attempts
   are logged and surfaced as first-class console metrics ("denied
   superadmin requests" on the health panel). Watching the watchers is a
   display requirement, not just a logging one.

## Output Format

```
SUPERADMIN OBSERVABILITY CONSOLE DESIGN — <platform>
Posture:  DESIGN ONLY — read console; grants no access; edits no live config.
Read-security model:
  Registry:  <table, deny-all RLS, provenance columns, out-of-band grant path>
  Re-check:  <UI guard (cosmetic) / endpoint (verified token → registry) /
    table RLS — one SECURITY-DEFINER membership function across all three>
  Caller lanes: <human token lane / machine secret lane; narrowing-only
    filters on destructive batch ops>
  Write posture: <telemetry/audit/alert tables privileged-write-only>
IA: <the one health answer; groups + escalation badges; restraint statement>
Panel inventory: <per panel — {feed-owner (skill), read-scope, wired: bool}>
Read model: <the server-composed summary call(s); split plan once oversized>
DB/query-perf panel: <metrics + thresholds; snapshot cron + retention;
  honest limits (sub-tick sampling gap; cumulative stats pairing)>
Verification panels: <which scans/probes/runs are displayed as posture>
Break-glass content reveal: <the five properties, in enforcement order>
Denied-access metrics: <where denials surface in the console>
Known gaps: <the wired:false list + the known-gaps page>
Handoffs: <actions → admin-console-architect; backend wiring →
  observability-operator; feed changes → the named feed owners>
```

## Validation Checklist

- [ ] The platform-admin registry is a dedicated table with deny-all RLS and
      grant provenance; no profile flag, no tenant-role escalation path, no
      self-service grant.
- [ ] Every privileged read path re-checks membership server-side at all
      three layers (cosmetic UI guard, per-request endpoint check from the
      verified token, table-level RLS), via one shared membership function.
- [ ] The console is read-only by default: telemetry, audit, and alert
      tables are privileged-lane write-only — an admin session cannot
      fabricate or tamper with what the console displays; cross-tenant
      actions route to `admin-console-architect`'s mediated command path.
- [ ] Denied privileged-access attempts are logged AND surfaced as console
      metrics.
- [ ] Break-glass content reveal has all five properties (non-executive
      role, reason code + note, open-incident link, incident-scoped
      narrowing, audit-before-return).
- [ ] Every panel names its feed owner and read scope; no panel re-derives
      an owning skill's discipline inline.
- [ ] The DB/query-performance panel is present (or its absence is a typed
      known gap), with thresholds, snapshot/retention mechanics, and its
      honest limits stated.
- [ ] Unwired panels are typed `wired: false` with a message; the known-gaps
      page exists.
- [ ] The IA leads with one health answer; collapsed groups carry escalation
      badges.

## Security Rules

- The read console and the action console are different trust surfaces: this
  console's queries never mutate; anything that acts on a tenant routes
  through the mediated command path (`admin-console-architect`). A
  monitoring console with write access to what it displays is not a
  monitoring console.
- The console never fabricates what it displays: telemetry/audit/alert
  writes are privileged-lane only, so a compromised admin session can read
  dashboards but cannot rewrite history.
- RANK ≠ REACH: seniority grants aggregates, not content. Content access is
  an incident-scoped audited exception, never a standing role convenience.
- The server decides what an admin may see. The UI guard is cosmetic; any
  privilege logic that exists only in the client is a finding.

## Gotchas

- The UI guard is cosmetic — a redirect is not access control. If the
  endpoint and table layers don't independently re-check, a copied URL or a
  direct API call walks straight past the console.
- The monolithic server summary grows unbounded: every new panel adds to one
  payload and one type. Split by panel group once it exceeds a screen of
  type definitions, or the summary becomes the slowest, riskiest query in
  the platform.
- DB-native telemetry (first-party tables, no external APM) works — but the
  database is then monitoring itself: a DB outage blinds the console exactly
  when you need it most. External synthetic probes are the mitigation; the
  design must say so.
- Sampling live query activity on a cron misses everything that completes
  between ticks; pair the slow-query sample with cumulative query statistics
  where the platform offers them, and state the blind spot where it doesn't.
- Telemetry lives in the OLTP store, so producers own retention: every
  snapshot job prunes its own history, or the monitoring tables become the
  platform's next storage problem.
- Permissive CORS on admin endpoints is survivable ONLY because every
  request is independently authenticated — never let "it's an internal
  console" relax per-request auth.
- Console sprawl is the everything-at-once anti-pattern: mixing operator
  panels with engineering artifacts (threat models, architecture docs)
  buries the health answer. Restraint is a design deliverable, not a style
  preference.

## Stop Conditions

- Asked to design cross-tenant ACTIONS, impersonation, support-mode,
  break-glass ELEVATION, or the operator control-plane → STOP: that is
  `admin-console-architect`'s surface; this console only SEES.
- Asked to instrument services or wire/operate the telemetry backend (create
  dashboards or alert rules in the stack) → STOP: that is
  `observability-operator` (manual-only); this skill designs the in-product
  console.
- Asked to give admins WRITE access to displayed telemetry ("let admins
  correct bad metrics data") → refuse the shape: read-only-by-default with
  privileged-write-only telemetry is load-bearing; a console that can
  fabricate what it displays defeats its purpose.
- Asked to let the console read tenant/user CONTENT without the break-glass
  properties (open incident, reason, scope narrowing, audit-before-return)
  → refuse; metrics are a role, content is an exception.
- The platform-role authorization policy does not exist or is ambiguous →
  obtain it from `authorization-matrix-designer` before designing read-path
  enforcement.
- Asked to grant real platform-admin access or provision the registry in
  production → out-of-band via the repo's approval path
  (`human-approval-boundary`); this skill designs, it does not grant.

## Supporting Files

- `references/panel-taxonomy-and-read-security.md` — the full panel menu
  (seven groups), the read-security model in detail, server-shaped
  read-model split guidance, and the DB/query-performance panel spec.
- `evals/evals.json` — behavior cases: the console-design happy path, the
  self-monitoring blind-spot edge, the admin-writable-metrics refusal, and
  the content-without-incident refusal.
- `evals/trigger-evals.json` — discrimination against
  `admin-console-architect` (seeing vs acting), `observability-operator`
  (design vs operate), and the feed owners (`slo-reliability-architect`,
  `audit-log-architect`, `security-logging-alerting-architect`).
