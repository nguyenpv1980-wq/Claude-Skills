# Automation Blueprint Reference

Detail file for `qa-automation-architect`. Loaded on demand.

## Default stack table (JS/TS SaaS baseline — adjust to repo reality)

| Layer | Default | Notes |
| --- | --- | --- |
| Unit/component | Vitest (+ Testing Library for components) | environment chosen per file — see `vitest-unit-component-engineer` |
| Integration | Vitest node environment + real DB (containerized) | boundaries per `integration-test-designer` |
| Contract | schema validation in CI (OpenAPI/zod/JSON Schema diff) | design per `api-contract-test-designer` |
| E2E | Playwright | patterns per `playwright-e2e-engineer` |
| A11y automated | axe-core wired into component/E2E layers | harness per `accessibility-test-harness` |
| Build QA | vite build + preview checks | per `vite-build-qa-engineer` |

Incumbent-tool rule: keep what exists unless a deficiency is named (speed,
parallel safety, maintenance status, missing capability).

## Directory layout pattern

```
tests/
  unit/          # or colocated *.test.ts next to source — pick ONE convention
  integration/
  contract/
  e2e/
    fixtures/    # playwright fixtures, auth state
  support/
    factories/   # data factories (design: test-data-architect)
    helpers/
```

Import boundary: `tests/**` may import from `src` public entry points and
`tests/support`; never from another layer's helpers.

## DB isolation options compared

| Option | Speed | Fidelity | Parallel safety | Use when |
| --- | --- | --- | --- | --- |
| Transaction-rollback per test | fast | high (same schema) | needs per-worker connection | integration default |
| Schema/database per worker | medium | high | excellent | heavy parallel suites |
| Truncate between tests | slow | high | poor in parallel | last resort |
| In-memory fake | fastest | low | excellent | unit only — never call it integration |

## CI tier worksheet

- PR tier budget: target < 10 min wall clock; shard when over.
- Merge tier: smoke E2E (critical journeys only).
- Nightly: full E2E, a11y scans, long suites — triaged every morning by a
  named owner.
- Retry policy: max 1 retry, only on E2E tier, every retry logged and
  reported weekly to `flaky-test-detective` intake; unit/integration retries
  are OFF (a flaky unit test is a bug, not weather).
- Artifacts: JUnit/JSON report per suite + failure traces/screenshots
  uploaded with run id; retention per evidence rules.
