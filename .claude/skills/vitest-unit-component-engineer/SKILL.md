---
name: vitest-unit-component-engineer
description: Implement and run Vitest unit and component tests — pure logic, validators, reducers, mappers, state machines, and UI components in isolation. Chooses the test environment INTENTIONALLY per file (node for logic, jsdom/happy-dom only where DOM is real), uses Testing Library user-facing queries for components, mocks only at owned boundaries, asserts behavior not implementation, and reports the exact commands run with real pass/fail output. Use when asked to write or fix Vitest unit/component tests, add tests for utilities or components, or configure vitest environment/setup for a suite. WRITES test files and RUNS the suite — manual invocation only. Do NOT use for tests crossing real service/DB/auth boundaries (integration-test-designer), browser journeys (playwright-e2e-engineer), red-green implementation of NEW behavior (tdd-engineer), or build verification (vite-build-qa-engineer).
disable-model-invocation: true
---

# Vitest Unit & Component Engineer

## Purpose

Implement fast, deterministic Vitest tests at the isolated layer: pure
functions and small components, with the environment chosen deliberately per
file, mocks confined to owned boundaries, and assertions on observable
behavior. Deliverables are the test files, any config/setup changes they
required, and the real run output — never a claim of green without the
command and its result.

## Use When

- Use when: asked to write Vitest tests for utilities, validators, reducers,
  mappers, state machines, hooks, or components in isolation.
- Use when: an existing Vitest suite needs new cases, repair after refactor,
  or environment/setup configuration.
- Use when: a test plan (`test-plan-designer`) hands over its unit-layer items.
- Do NOT use when: the behavior under test crosses a real service, database,
  auth, or permission boundary — that is the integration layer
  (`integration-test-designer` designs it); mocking those boundaries here and
  calling it integration is the classic false-confidence bug.
- Do NOT use when: the ask is a browser user journey — `playwright-e2e-engineer`.
- Do NOT use when: implementing NEW behavior test-first — `tdd-engineer` owns
  the red-green-refactor loop; this skill builds out suites for existing
  behavior and hands new-behavior work there.
- Do NOT use when: verifying the production build — `vite-build-qa-engineer`.

## Inputs to Inspect

1. The code under test: exports, types, side-effect surface (what it imports
   — timers, fetch, storage, randomness).
2. Existing Vitest setup: `vitest.config.*` (environment, setupFiles,
   globals, coverage), existing test conventions and helpers.
3. The installed versions: vitest, Testing Library packages, jsdom/happy-dom
   (via lockfile — API differences matter; compose `docs-first-implementer`
   when uncertain).
4. The plan item or requirement each test verifies (risk-traced, per
   `test-plan-designer` if present).
5. Package scripts: how the suite is actually run locally and in CI.

## Workflow

1. **Classify each target: logic or component.** Logic → `node` environment
   (fastest, no DOM lies). Component → `jsdom`/`happy-dom`, declared per file
   (`// @vitest-environment jsdom`) or via config `environmentMatchGlobs` —
   an intentional, visible choice either way, never "jsdom everywhere because
   one test needed it."
2. **Design cases from behavior:** happy path, negative/error paths,
   boundaries (empty/one/many/max, dates, precision). Each case asserts an
   observable outcome; patterns in
   [references/vitest-patterns.md](references/vitest-patterns.md).
3. **Mock only owned boundaries:** module seams you control (API client,
   clock via fake timers, randomness via seed). Never mock the unit under
   test's internals; never deep-mock a third-party library's internals —
   wrap it instead. Restore all mocks/timers per test.
4. **Component tests query like a user:** Testing Library `getByRole`/
   `getByLabelText`; interactions via `userEvent`; assert rendered outcomes,
   not state internals or implementation calls. No snapshot-everything.
5. **Keep tests deterministic:** fake timers for time, fixed seeds, no real
   network (fail the suite on unmocked fetch), no order dependence.
6. **Run the suite and report honestly:** exact command, pass/fail counts,
   runtime. A new test must fail when the behavior it guards is broken —
   spot-check by mutating the subject or the assertion once (then restore).
7. **Wire coverage/CI only if in scope:** thresholds per the automation
   blueprint (`qa-automation-architect`), not invented here.

## Output Format

```
VITEST REPORT — <scope>
Environment decisions: <file/group → node|jsdom|happy-dom + why>
Tests added/changed: <file → cases, each traced to behavior/risk>
Mock boundaries: <what is mocked, why it is an owned seam>
Commands run: <exact commands>
Results: <real output summary — pass/fail counts, runtime>
Failure honesty: <any failing/skipped tests + why, or "none">
Verification: <how a guarded regression was confirmed to fail the test>
Handoffs: <boundary-crossing cases → integration-test-designer;
          new-behavior TDD → tdd-engineer>
```

## Validation Checklist

- [ ] Environment per file is intentional and stated (node vs DOM).
- [ ] Every test asserts observable behavior; zero assertion-free or
      render-only tests.
- [ ] Mocks confined to owned seams; all mocks/timers restored per test.
- [ ] Determinism: no real network/time/randomness dependence.
- [ ] Suite RUN with output included; failures reported, not hidden.
- [ ] At least one guarded behavior spot-checked to actually fail the test.
- [ ] No boundary-crossing test smuggled in as "unit with mocks".

## Gotchas

- jsdom is not a browser: layout, real navigation, and CSS visibility lie —
  tests needing real rendering belong in Playwright, not deeper jsdom hacks.
- `vi.mock` hoists — module-level state in the mocked module can leak
  between tests; prefer factory mocks and `vi.resetModules` when it bites.
- Fake timers left installed leak into other tests' async behavior — restore
  in `afterEach`, not at the end of the one test that needed them.
- Testing a hook by asserting on internal state couples the test to the
  implementation; render a consumer and assert what the user sees.
- `environment: jsdom` globally makes pure-logic tests slower and can mask
  node-only bugs (e.g., code that accidentally touches `window`).

## Stop Conditions

- The behavior needs a real DB/service/auth boundary to be meaningful → stop;
  route to `integration-test-designer` rather than mocking the boundary and
  overstating confidence.
- The subject has no testable seam (hard-wired singletons, ambient state)
  and testing requires refactoring product code → that is a separate change;
  surface it and get scope confirmed first.
- The suite cannot run (broken install/config) for reasons outside test files
  → report the blocker; do not "fix" unrelated tooling silently.
- Asked to delete or weaken failing tests to get green → refuse; failures are
  reported and routed (`flaky-test-detective` for flakes, product fix
  otherwise).

## Supporting Files

- [references/vitest-patterns.md](references/vitest-patterns.md) — environment
  selection table, mock-seam patterns, Testing Library query priority, and
  determinism recipes.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the test-level cluster
  (unit vs integration vs E2E vs contract) and against `tdd-engineer`.
