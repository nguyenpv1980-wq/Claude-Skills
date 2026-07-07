---
name: tenant-isolation-reviewer
description: Review an existing multi-tenant system or design for cross-tenant leakage across EVERY surface — identity, data, API, storage, logs, analytics, support tooling, exports, imports, background jobs, search, AI retrieval, billing, feature flags, and audit — not just the database. Produces severity-ranked isolation findings with file:line evidence, an isolation test matrix per surface, negative tests proving tenant A cannot reach tenant B's data, and an explicit not-inspected list. Use when asked whether tenant isolation is sound, before onboarding a security-sensitive customer, before exposing a new surface (export, search, AI feature, support view) to tenants, or after an isolation incident. Do NOT use to define what a tenant is (tenant-modeler) or to design the data layer (multi-tenant-data-architect); this skill reviews real systems — no code or concrete design, no review.
---

# Tenant Isolation Reviewer

## Purpose

Produce an evidence-based verdict on whether tenants can reach each other's
data, across every surface the system exposes — not only the database. The
deliverables are severity-ranked findings with evidence, an isolation test
matrix, negative tests that prove denial, and — just as important — an honest
list of surfaces NOT inspected. A surface never examined is reported as
not-inspected, never assumed safe; "we use tenant_id everywhere" is a claim,
not a finding.

## Use When

- Use when: asked "is our tenant isolation sound?" — before an enterprise or
  regulated-customer onboarding, a security questionnaire, or a pen test.
- Use when: a new tenant-facing surface ships — export, import, search, AI
  retrieval/chat, support console, analytics dashboard, webhook feed.
- Use when: after a cross-tenant incident or near-miss, to find the siblings
  of the known hole.
- Do NOT use when: tenant semantics are undefined — run `tenant-modeler`
  first; you cannot review isolation against an undefined boundary.
- Do NOT use when: designing the data layer or scoping strategy — that is
  `multi-tenant-data-architect`.
- Do NOT use when: there is no code, schema, or concrete design to inspect —
  this skill never reviews imagined systems.
- Do NOT use when: the ask is a full security review beyond tenancy (authn,
  injection, secrets) — delegate to the `secure-saas-reviewer` subagent; this
  skill goes deep on the tenancy axis only.

## Inputs to Inspect

1. The tenant model and declared isolation boundary (tenant-modeler output or
   equivalent) — the review is against THIS definition.
2. The data layer: schemas, tenant keys, scoping mechanism (query filters,
   RLS, schema/db separation) and where tenant context is derived.
3. API layer: route handlers, middleware where tenant context binds, any
   endpoint accepting tenant or resource ids from the client.
4. The full surface list in
   [references/isolation-surface-checklist.md](references/isolation-surface-checklist.md)
   — mark each surface applicable / not-applicable / not-inspectable.
5. Privileged paths: support/admin tooling, service-role or superuser DB
   access, background jobs and their credentials.
6. Prior incidents, existing isolation tests, and pen-test reports if any.

## Workflow

1. **Confirm there is something real to review.** Identify the repo, schema,
   or design doc under review. No artifact → stop (see Stop Conditions).
2. **Pin the boundary.** State the tenant definition and where isolation is
   supposed to be enforced. If undefined, stop and route to `tenant-modeler`.
3. **Enumerate surfaces** from the checklist; classify each as applicable,
   not-applicable (say why), or applicable-but-not-inspectable (goes to the
   not-inspected list). This inventory comes before any finding.
4. **Trace each applicable surface** from entry point to data access: where
   does tenant context come from, is it server-derived or client-supplied,
   and does every query/read/write on the path carry the scope? Sample real
   code paths; cite file:line.
5. **Probe the classic holes** per surface (catalog in the checklist):
   client-supplied tenant ids, unscoped by-id lookups (IDOR), service-role
   bypasses in jobs, unscoped search indexes, cross-tenant AI retrieval
   corpora, logs/analytics carrying another tenant's data, export jobs
   running with platform credentials.
6. **File findings** with severity, evidence (file:line or design-section),
   the concrete leak scenario (tenant A does X → sees tenant B's Y), and a
   remediation direction. Severity floor: any confirmed cross-tenant read of
   business data is critical.
7. **Build the isolation test matrix**: surface × operation × expected
   denial. Every applicable surface gets at least one row.
8. **Write the negative-test plan**: concrete tests where tenant A attempts
   tenant B's resource and the expected result is deny/404/empty — including
   at least one per privileged path (support, jobs). Tests that only prove
   the happy path do not count.
9. **Report** confirmed findings, suspected findings (with what would confirm
   them), the test matrix, and the not-inspected list. Recommend fixes; do
   not implement them in this pass.

## Output Format

```
TENANT ISOLATION REVIEW — <system/scope>
Boundary reviewed against: <tenant definition + declared enforcement point>
Surface inventory: <surface — applicable / n-a (why) / not-inspected (why)>
Findings (severity-ranked):
  [CRITICAL|HIGH|MEDIUM|LOW] <surface> — <leak scenario: tenant A → tenant B's data>
    Evidence: <file:line or design section>   Remediation: <direction>
Suspected (unconfirmed): <finding — what would confirm it>
Isolation test matrix: <surface × operation × expected denial>
Negative-test plan: <test — actor — attempted access — expected result>
NOT inspected: <surface — reason — risk of leaving it uninspected>
Verdict: <sound for the inspected surfaces / not sound — with the one-line why>
```

## Validation Checklist

- [ ] Surface inventory completed BEFORE findings; every checklist surface
      classified, none silently skipped.
- [ ] Every finding has evidence (file:line or design section) and a concrete
      tenant-A-reaches-tenant-B scenario — no vibes-based findings.
- [ ] Confirmed vs suspected findings are separated; suspected ones name what
      would confirm them.
- [ ] Every applicable surface has at least one test-matrix row and the
      privileged paths (support, jobs) have negative tests.
- [ ] The not-inspected list is present — an empty one means everything was
      actually inspected, not that the section was dropped.
- [ ] The verdict claims soundness only for inspected surfaces.
- [ ] No fixes implemented — this skill reviews and specifies tests.

## Tenant Isolation Rules

- Tenant isolation is not only database isolation: identity, data, API,
  storage, logs, analytics, support tooling, exports, imports, background
  jobs, search, AI retrieval, billing, feature flags, and audit are ALL in
  scope, every review.
- Client-supplied tenant identifiers trusted anywhere on a data path is a
  finding, regardless of whether an exploit is demonstrated.
- Privileged paths (support tooling, service-role jobs, admin consoles) are
  reviewed as leak surfaces, not exempted as "internal."

## Security Rules

- Severity floor: confirmed cross-tenant read of tenant business data =
  CRITICAL; confirmed cross-tenant write or delete = CRITICAL; leakage of
  tenant existence/metadata = at least MEDIUM.
- Negative tests are mandatory deliverables — an isolation claim without a
  test that attempts the forbidden access and observes denial is unverified.
- Findings are never suppressed or downgraded for convenience; accepted risk
  requires the human's written rationale via `human-approval-boundary`.

## Gotchas

- The database can be perfectly scoped while search indexes, AI embedding
  stores, and analytics pipelines — populated by unscoped batch jobs — leak
  everything.
- 404-vs-403 responses and per-tenant error detail leak tenant existence;
  decide the policy, then test against it.
- Background jobs and webhooks often run with platform-wide credentials;
  "the API is scoped" says nothing about them.
- Caches keyed without tenant context serve tenant A's cached response to
  tenant B under load — invisible in code review, visible in the test matrix.
- Reviews that only sample "the interesting files" miss the boring importer
  that loads rows with no tenant column; the surface inventory exists to
  prevent exactly this.

## Stop Conditions

- No code, schema, or concrete design artifact is available → stop; this
  skill does not review descriptions of systems from memory.
- The tenant boundary itself is undefined or contested → stop; route to
  `tenant-modeler` (or `source-of-truth-reconciler` if sources conflict).
- A CRITICAL confirmed leak is found in a live system → report immediately
  with the minimal reproduction; do not continue the full review before the
  human decides on containment (`human-approval-boundary`).
- Asked to fix findings in the same pass → fixes are a separate, scoped
  change (classify via `change-classification-gate`); confirm before editing.

## Supporting Files

- [references/isolation-surface-checklist.md](references/isolation-surface-checklist.md) —
  the fifteen-surface checklist with what-to-check and classic holes per
  surface.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `tenant-modeler` and
  `multi-tenant-data-architect` (tenant cluster).
