# Risk & Layer Catalog

Detail file for `qa-strategy-architect`. Loaded on demand.

## Risk taxonomy (starting checklist, not a ceiling)

| Risk family | Typical failure | Default owner layer |
| --- | --- | --- |
| Data integrity | corruption, silent loss, wrong math | unit (logic) + integration (persistence) |
| Tenant/authz | cross-tenant read/write, privilege escalation | delegated: `multi-tenant-security-tester`, `rls-policy-auditor` |
| Auth/session | login broken, session fixation, lockout | integration (auth boundary) + one E2E journey |
| Money | wrong charge, double charge, missed webhook | contract (provider) + integration (idempotency) |
| Critical journeys | signup/checkout/core workflow broken | E2E (few, stable) + smoke tier |
| External contracts | breaking API/webhook consumers | contract tests (`api-contract-test-designer`) |
| Build/deploy | secret in bundle, broken preview, bad base path | build QA (`vite-build-qa-engineer`) |
| Visual/UX | layout breakage, unusable flows | manual (`manual-test-case-creator`) + clickthrough + screenshots |
| Accessibility | keyboard traps, unlabeled controls | `accessibility-test-harness` |
| Regressions | fixed bugs returning | regression suite (`regression-suite-curator`) |

## Layer decision table — cheapest reliable layer wins

Ask in order; first "yes" picks the layer:

1. Can the risk be proven with pure inputs/outputs, no I/O? → **unit**.
2. Does the risk live at a real boundary (service, command, DB, auth,
   permissions) but not require a browser? → **integration**
   (`integration-test-designer`).
3. Is the risk "producer and consumer disagree on shape/version"? →
   **contract** (`api-contract-test-designer`).
4. Is the risk "a whole user journey breaks in the real UI" AND the journey is
   business-critical? → **E2E** (`playwright-e2e-engineer`) — budget these;
   each E2E journey must name why lower layers were insufficient.
5. Does verification require human judgment (visual quality, wording, UX)? →
   **manual** with screenshot evidence.

Anti-pattern: covering a unit-provable rule with an E2E test "to be safe" —
that doubles cost and halves signal.

## Evidence classes (map to change classes)

| Change class | Blocking floor | Artifacts |
| --- | --- | --- |
| docs-only | lint/link checks | none |
| logic/frontend | unit + affected integration | test report |
| API/contract | + contract suite | contract report, schema diff |
| schema/RLS | + migration review, security negatives | negative-test output |
| UI-visible | + smoke E2E, clickthrough on affected routes | screenshots per `screenshot-evidence-planner` |
| release | full regression tier | closeout via `ai-closeout-reporter` |

## CI placement defaults

- PR: unit, integration, contract, lint, build — blocking.
- Merge/main: smoke E2E — blocking.
- Nightly: full E2E, long suites, a11y scans — non-blocking but triaged daily.
- Anything non-blocking needs an owner and a triage cadence or it is noise.
