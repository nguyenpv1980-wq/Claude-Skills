# Playwright Patterns

Detail file for `playwright-e2e-engineer`. Loaded on demand.

## Locator ladder (stop at the first rung that works)

1. `page.getByRole('button', { name: 'Save invoice' })` — role + accessible
   name; survives markup churn, doubles as an a11y signal.
2. `page.getByLabel('Email address')` — form controls.
3. `page.getByText('Invoice #1042')` — static, user-visible text only.
4. `page.getByTestId('invoice-row')` — last resort; log it as a semantics gap
   (the control has no role/name a user could target either).

Never: CSS descendant chains (`.card > div:nth-child(2)`), XPath, class-name
selectors — they encode implementation, not intent.

## Web-first assertion catalog

- Visibility/content: `await expect(locator).toBeVisible()`,
  `toHaveText`, `toContainText`, `toHaveValue`, `toHaveCount`.
- Navigation: `await expect(page).toHaveURL(/\/invoices\/\d+/)`.
- Explicit response wait when the UI signal is insufficient:
  `page.waitForResponse(resp => resp.url().includes('/api/invoices') && resp.ok())`
  — scoped, never `networkidle`.
- Banned: `page.waitForTimeout(...)`, polling loops, `networkidle` waits.

## Auth-state project setup recipe

```ts
// playwright.config.ts (shape, adjust to repo)
projects: [
  { name: 'setup', testMatch: /auth\.setup\.ts/ },
  { name: 'member', dependencies: ['setup'],
    use: { storageState: '.auth/member.json' } },
  { name: 'admin', dependencies: ['setup'],
    use: { storageState: '.auth/admin.json' } },
]
```

`auth.setup.ts` logs in each persona (UI or API), saves storageState to a
gitignored path. Personas come from seeded fixtures (`test-data-architect`).
One login per persona per run — tests never re-login.

## Data determinism patterns

- Seed per test via API/fixture with worker-unique identifiers
  (`test.info().parallelIndex` in names).
- Assert against the data you created, not ambient records.
- Cleanup structurally (delete by the unique prefix / fixture teardown).

## CI wiring

- `trace: 'on-first-retry'`, `screenshot: 'only-on-failure'`,
  `video: 'retain-on-failure'`.
- `retries: 1` on CI only; report pass-on-retry as flake intake
  (`flaky-test-detective`).
- Shard with `--shard=i/n` against the runtime budget; upload
  `playwright-report/` + traces with the run id.
