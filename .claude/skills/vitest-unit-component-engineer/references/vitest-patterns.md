# Vitest Patterns

Detail file for `vitest-unit-component-engineer`. Loaded on demand.

## Environment selection table

| Subject | Environment | Why |
| --- | --- | --- |
| pure functions, validators, mappers, reducers | `node` | fastest; catches accidental DOM/window reliance |
| framework-free DOM utilities | `jsdom` or `happy-dom` | DOM APIs needed, no browser fidelity required |
| components (render + interact) | `jsdom` (default) / `happy-dom` (speed, check API gaps) | Testing Library needs a DOM |
| anything needing layout, real navigation, downloads | none — wrong layer | Playwright territory |

Declare per file with `// @vitest-environment jsdom` or per glob with
`environmentMatchGlobs` — visible intent either way.

## Mock-seam patterns

- **Clock:** `vi.useFakeTimers()` + `vi.setSystemTime()`; restore in
  `afterEach(() => vi.useRealTimers())`.
- **Network:** mock the repo's OWN api-client module, or use an interceptor
  (e.g., MSW) at the fetch boundary; add a setup guard that fails on
  unexpected real fetch.
- **Randomness/ids:** inject or seed; asserting on random output is flake
  authorship (`flaky-test-detective` will be back for you).
- **Never:** mocking the module under test, partial-mocking its private
  functions, or deep-mocking third-party internals (wrap the library in an
  owned adapter and mock the adapter).

## Testing Library query priority

`getByRole` (with accessible name) → `getByLabelText` → `getByPlaceholderText`
→ `getByText` → `getByTestId` (last resort, and a hint to improve the
component's semantics — which also feeds `accessibility-test-harness`).

Interactions: `userEvent` over `fireEvent` (real event sequences).
Async: `findBy*` / `waitFor` with a specific assertion — never sleep.

## Determinism recipes

- Freeze time zone in config (`TZ=UTC` in test env) or make code TZ-explicit.
- One assertion of truth per behavior; table-drive boundaries with
  `test.each`.
- Isolation check: run with `--sequence.shuffle` locally when touching suite
  structure — order dependence is a bug now, not later.

## Coverage stance

Thresholds come from the automation blueprint. Locally meaningful signal:
uncovered branches in the file you just tested. Repo-wide percentages belong
to `test-coverage-mapper`'s analysis, not to this skill's exit criteria.
