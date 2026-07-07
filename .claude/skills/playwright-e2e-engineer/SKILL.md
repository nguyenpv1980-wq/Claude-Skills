---
name: playwright-e2e-engineer
description: Implement and run Playwright E2E tests for CRITICAL user journeys — resilient user-facing locators (getByRole/getByLabel, testid last), web-first auto-retrying assertions, zero arbitrary sleeps or networkidle waits, project-level auth-state setup, deterministic test data, and trace/screenshot artifacts on failure wired for CI. Each journey names why a cheaper layer was insufficient; E2E stays a small, stable suite, not a UI-tree crawler. Use when asked to write, fix, or harden Playwright tests, automate a login/signup/checkout-style journey in a real browser, or set up Playwright config/fixtures/auth state. WRITES spec files and DRIVES a browser — manual invocation only. Do NOT use for real-boundary tests without a browser (integration-test-designer), isolated component tests (vitest-unit-component-engineer), one-off interactive walkthroughs (clickthrough-test-engineer), or a11y-specific harnesses (accessibility-test-harness).
disable-model-invocation: true
---

# Playwright E2E Engineer

## Purpose

Implement the small, stable set of browser tests that prove business-critical
user journeys work end to end: real UI, real backend, deterministic data,
resilient locators, and web-first assertions that wait for the app instead of
sleeping at it. Deliverables are spec files, any config/fixture changes,
failure artifacts wiring, and the real run output.

## Use When

- Use when: asked to write or fix Playwright tests for a user journey
  (signup, login, checkout, core workflow).
- Use when: hardening an existing Playwright suite — flaky waits, brittle
  CSS/XPath selectors, sleep-ridden specs.
- Use when: setting up Playwright config, fixtures, auth-state projects, or
  CI artifacts for the E2E tier.
- Use when: a test plan hands over its E2E items (each with a named reason a
  cheaper layer was insufficient).
- Do NOT use when: the behavior needs no browser — `integration-test-designer`
  (real boundaries) or `vitest-unit-component-engineer` (isolated).
- Do NOT use when: the ask is a one-off interactive walkthrough with
  observations — `clickthrough-test-engineer`; this skill builds the
  PERMANENT scripted suite.
- Do NOT use when: the ask is keyboard/contrast/screen-reader verification —
  `accessibility-test-harness` (it may inject axe into E2E, but owns that
  design).
- Do NOT use when: diagnosing why an existing test flakes —
  `flaky-test-detective` first; this skill implements the proven fix.

## Inputs to Inspect

1. The journeys in scope and their business criticality (from the test plan
   or user) — every journey states why E2E is required.
2. Existing Playwright setup: `playwright.config.*` (projects, baseURL,
   retries, reporters, trace settings), existing fixtures and auth helpers.
3. The app's auth flow and test-account/bootstrap mechanism — how personas
   log in and how storageState can be minted per project setup.
4. Test data reality: how the journey gets deterministic data
   (`test-data-architect` fixtures, API seeding hooks) and how runs are
   isolated from each other.
5. The UI's accessibility surface: are there roles/labels to locate by?
   (Locator quality depends on it; gaps also feed `accessibility-test-harness`.)
6. Installed Playwright version (lockfile) — API and best-practice drift is
   real; compose `docs-first-implementer` when uncertain.

## Workflow

1. **Confirm the journey list is small and critical.** Each spec = one
   user-meaningful journey with a named risk. Reject UI-tree crawling —
   route breadth to `clickthrough-test-engineer` or component layers.
2. **Set up auth state once per persona:** project-dependency setup that logs
   in via the UI or API and saves `storageState`; tests reuse state, never
   re-login per test. Personas map to `test-data-architect` seeds.
3. **Make each journey data-deterministic:** create the entities the journey
   needs via API/fixture in setup (unique per run/worker), assert on that
   data, clean up structurally. No reliance on ambient shared records.
4. **Write specs with resilient locators:** `getByRole`/`getByLabel`/
   `getByText` (user-facing) first; `data-testid` only where semantics don't
   exist — and flag those as UI semantics gaps. No CSS chains, no XPath.
   Locator ladder in [references/playwright-patterns.md](references/playwright-patterns.md).
5. **Assert web-first, never sleep:** `expect(locator).toBeVisible()/
   toHaveText()` auto-retry; wait for a specific UI outcome or explicit
   response, never `waitForTimeout` and never `networkidle`. Any remaining
   fixed wait is a defect in the spec.
6. **Wire failure evidence:** `trace: on-first-retry` (or on-failure),
   screenshot + video per config policy, artifacts uploaded in CI with run
   id (naming per `screenshot-evidence-planner` conventions when used as
   release evidence).
7. **Run the suite and report honestly:** exact command, per-spec results,
   runtime, retry count (a pass-on-retry is reported as such and routed to
   `flaky-test-detective`, not celebrated).
8. **Place in CI** per the automation blueprint: smoke tier on merge, full
   tier nightly — runtime-budgeted, sharded when needed.

## Output Format

```
PLAYWRIGHT REPORT — <scope>
Journeys: <spec → journey → why E2E was required>
Auth/state setup: <persona → minting path → storageState reuse>
Data strategy: <per-journey deterministic setup + isolation + cleanup>
Locator posture: <role/label coverage; testid fallbacks flagged as semantics gaps>
Specs added/changed: <files, cases>
Commands run: <exact commands>
Results: <real output — pass/fail, runtime, retries (pass-on-retry called out)>
Artifacts: <traces/screenshots/videos + CI upload wiring>
CI placement: <tier, sharding, budget>
Handoffs: <flakes → flaky-test-detective; semantics gaps → accessibility-test-harness;
          non-browser items → integration-test-designer>
```

## Validation Checklist

- [ ] Every spec maps to a named critical journey with an E2E justification.
- [ ] Zero `waitForTimeout` / `networkidle` / manual polling — web-first
      assertions only.
- [ ] Locators are user-facing first; every `data-testid` fallback flagged.
- [ ] Auth via reused storageState from project setup, not per-test login.
- [ ] Test data unique per run/worker; no ambient-record dependence.
- [ ] Failure artifacts (trace at minimum) wired locally and in CI.
- [ ] Suite RUN with real output; pass-on-retry reported and routed.
- [ ] Suite runtime within the tier budget.

## Gotchas

- `networkidle` is explicitly discouraged and lies on apps with polling/
  websockets — wait for the UI outcome instead.
- Free-text `getByText` on dynamic content (dates, counts) flakes; anchor on
  stable accessible names or pass exact expected data you seeded.
- Reused storageState goes stale when auth/session format changes — mint in
  a setup project per run, don't commit long-lived state files.
- Parallel workers sharing one seeded account trip over each other's data —
  worker-scoped uniqueness is mandatory, not optional.
- Auto-retrying assertions can mask slow regressions — keep default timeouts
  honest; a journey that needs 60s timeouts has a product problem to report.
- Strict-mode locator violations (multiple matches) are design feedback:
  disambiguate by role/name, don't `.first()` your way past them.

## Stop Conditions

- No runnable environment (app won't start, no test accounts/bootstrap) →
  report the blocker; do not write specs that have never executed and call
  them a suite.
- The journey list balloons past the tier's runtime budget → stop and
  re-negotiate scope with the plan/strategy owner instead of shipping a slow
  suite.
- Required test hooks (API seeding, test-only routes) don't exist and would
  require product changes → surface as a separate classified change.
- A journey fails against the real app (product bug, not spec bug) → report
  the failure with trace; the fix is `systematic-debugger`/product work, not
  spec weakening.

## Supporting Files

- [references/playwright-patterns.md](references/playwright-patterns.md) —
  locator ladder, web-first assertion catalog, auth-state project setup
  recipe, sharding/CI wiring.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the test-level cluster
  and against `clickthrough-test-engineer`.
