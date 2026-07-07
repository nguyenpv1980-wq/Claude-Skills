---
name: multi-tenant-security-tester
description: Design and specify an executable negative-test suite that PROVES tenant isolation and object-level authorization hold — cross-tenant reads/writes, IDOR by-id enumeration, privilege escalation, wrong-role and wrong-tenant access, and service-role/background-job bypasses — with a per-surface test matrix, seeded two-tenant fixtures, and pass = the forbidden action is denied. Use when asked to write or plan tenant-isolation / authorization security tests, to turn isolation-review or threat-model findings into regression tests, or to add a cross-tenant negative suite before a security-sensitive launch. Do NOT use to FIND leaks by inspection (tenant-isolation-reviewer), define tenant semantics (tenant-modeler), audit RLS policy text (rls-policy-auditor), or review a diff (security-pr-reviewer).
---

# Multi-Tenant Security Tester

## Purpose

Produce the executable proof that tenant isolation and object-level
authorization actually hold: a negative-test suite where every test attempts a
forbidden cross-tenant or cross-privilege action and passes only when that
action is DENIED. The deliverables are a per-surface test matrix, a
two-tenant (A/B) seeded fixture design, concrete test specifications (or
implemented tests where the runner is known), and a coverage statement of
which surfaces are proven vs still unproven. A suite that only exercises the
happy path proves nothing about isolation and is treated as absent.

## Use When

- Use when: asked to write or plan security tests for tenant isolation,
  authorization, IDOR, or privilege escalation.
- Use when: converting `tenant-isolation-reviewer` findings or
  `threat-modeler` abuse cases into permanent regression tests.
- Use when: a security-sensitive launch needs a cross-tenant negative suite as
  evidence.
- Use when: an isolation incident needs a regression test that would have
  caught it (and its siblings).
- Do NOT use when: the task is to FIND leaks by inspecting code/config — that
  is `tenant-isolation-reviewer`; this skill proves/refutes with tests.
- Do NOT use when: tenant semantics are undefined — `tenant-modeler` first;
  you cannot test a boundary that isn't defined.
- Do NOT use when: the ask is to audit RLS policy TEXT — `rls-policy-auditor`
  (which itself produces an RLS negative-test plan; this skill covers the
  application/API and cross-surface layers).
- Do NOT use when: reviewing a diff — `security-pr-reviewer`.

## Inputs to Inspect

1. The tenant model and the declared isolation boundary (`tenant-modeler`
   output) and the authorization matrix (`authorization-matrix-designer`
   output) — the suite tests THESE definitions. Undefined → Stop Conditions.
2. Findings/abuse cases to regress: `tenant-isolation-reviewer` findings,
   `threat-modeler` abuse cases, incident write-ups.
3. The surfaces to cover: API routes, exports/imports, search, AI retrieval,
   background jobs, webhooks, support tooling — and how each authenticates.
4. The test stack: runner, HTTP/client test harness, fixture/seed mechanism,
   how auth tokens for distinct tenants/roles are minted in tests.
5. How tenant/role context is established per request, so tests can
   impersonate the wrong tenant/role authentically (not by faking internals).

## Workflow

1. **Confirm a defined boundary and a real target.** Pin the tenant
   definition and the enforcement point. Undefined or no runnable system →
   stop.
2. **Design the two-tenant fixture.** Seed tenant A and tenant B each with
   owned resources, plus users at each relevant role in each tenant, plus an
   anonymous caller. Record ids so tests can attempt B's ids as A.
3. **Build the test matrix:** surface × actor (wrong-tenant, wrong-role,
   anonymous, service-role/job) × operation (read, list, create, update,
   delete, export) × expected result (deny: 403/404/empty). Every applicable
   surface gets rows; use the catalog in
   [references/negative-test-matrix.md](references/negative-test-matrix.md).
4. **Specify each negative test** so another engineer can implement it: setup
   (as tenant A), action (attempt tenant B's resource by id / cross-role
   action), and assertion (denied AND no data leaked in body, headers, or
   error). Include the positive control (A reaches A's own resource) so a
   blanket-deny bug can't masquerade as passing isolation.
5. **Cover the hard surfaces explicitly:** IDOR by-id enumeration, list
   endpoints returning cross-tenant rows, search/AI retrieval returning
   B's content to A, exports/jobs running with platform credentials,
   privilege escalation (role self-upgrade, mass-assignment of tenant_id/role).
6. **Assert on denial semantics AND leakage:** 404-vs-403 existence leaks,
   error bodies echoing another tenant's data, timing where specified — test
   against the declared policy.
7. **Implement or hand off.** If the runner and conventions are known,
   implement the suite and run it, recording real output. Otherwise deliver
   implementable specs and a coverage statement.
8. **State coverage honestly:** which surfaces are proven by a passing
   negative test, which are specified-but-unrun, and which are not covered
   (with why) — no implied uniform coverage.

## Output Format

```
MULTI-TENANT SECURITY TEST SUITE — <system/scope>
Boundary under test: <tenant definition + enforcement point>
Fixture: tenant A / tenant B seed — <resources, roles, ids>
Test matrix: <surface × actor × operation × expected denial>
Negative tests:
  <id> — as <actor> attempt <op on B's resource> — expect <deny/404/empty>
         + positive control: as owner attempt own resource — expect allow
Leakage assertions: <existence (404 vs 403), error body, headers, timing>
Privileged-path tests: <service-role/job/support attempts + expected>
Execution: <runner + commands + result> | <specs only — not run, why>
Coverage: proven <surfaces> | specified-unrun <surfaces> | not covered <surfaces + why>
Handoffs: <rls-policy-auditor for DB-layer negative plan; appsec-implementer for fixes>
```

## Validation Checklist

- [ ] Two-tenant (A/B) fixture with per-role users and recorded ids exists.
- [ ] Every negative test attempts a FORBIDDEN action and passes only on denial.
- [ ] Each negative test has a positive control so blanket-deny can't pass as
      isolation.
- [ ] IDOR/by-id, list endpoints, search/AI retrieval, exports, jobs, and
      privilege escalation are all represented or explicitly marked uncovered.
- [ ] Leakage (existence via 404-vs-403, error-body echo) is asserted, not
      just status codes.
- [ ] Privileged paths (service-role, background jobs, support) have tests.
- [ ] Coverage statement separates proven / specified-unrun / not-covered.
- [ ] No fixes implemented here — failing tests are handed off.

## Tenant Isolation Rules

- Isolation testing spans every surface, not just the database API: exports,
  imports, search, AI retrieval, background jobs, webhooks, support tooling,
  analytics, billing, and audit are all testable leak surfaces.
- The canonical attacker is the authenticated wrong-tenant user; tests
  impersonate real tenants/roles through the real auth path, never by mutating
  internal state to fake scope.
- Client-supplied tenant/role/owner identifiers are attacker-controlled in
  tests — every such input gets a mass-assignment / spoofing negative test.

## Security Rules

- A negative test PASSES only when the forbidden action is denied; a green
  happy-path test is not isolation evidence.
- Coverage is stated honestly — an untested surface is reported as not-covered,
  never assumed safe (master-prompt §6: verification evidence required).
- Regression tests for fixed isolation bugs are permanent; removing one needs
  written rationale via `human-approval-boundary`.

## Gotchas

- Tests that mint tokens by directly setting tenant_id in a fixture bypass the
  real auth path and prove nothing — impersonate via the login/token flow.
- A list endpoint can pass per-item IDOR tests yet still leak in bulk — test
  that A's list contains zero of B's rows, not just that A can't fetch one B id.
- Passing negative tests with no positive control can hide a total outage
  (everything denied) — always pair them.
- Search and vector/AI retrieval are populated by jobs that may ignore tenant
  scope; test the retrieval RESULT for B's content, not just the query filter.
- 404-vs-403 inconsistency leaks tenant/record existence; pick the policy and
  assert it uniformly.

## Stop Conditions

- Tenant semantics or the isolation boundary are undefined → stop; route to
  `tenant-modeler`.
- There is no runnable system or testable interface (only prose) → deliver
  implementable specs and say they were not executed; do not claim passing.
- A test reveals a real cross-tenant leak in a live system → report the
  reproduction immediately; containment is a human decision
  (`human-approval-boundary`) before broad test expansion.
- Asked to fix the failing paths in the same pass → fixes are a separate,
  classified change (`appsec-implementer` / `rls-policy-auditor`); confirm first.

## Supporting Files

- [references/negative-test-matrix.md](references/negative-test-matrix.md) —
  per-surface actor × operation × expected-denial catalog, the two-tenant
  fixture recipe, and leakage-assertion patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `tenant-isolation-reviewer`,
  `rls-policy-auditor`, and the shipped `tenant-isolation-reviewer` (tenant
  security cluster).
