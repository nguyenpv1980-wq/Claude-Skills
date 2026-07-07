# Test Plan Template & Behavior Catalog

Detail file for `test-plan-designer`. Loaded on demand.

## Behavior catalog — prompts per risk

For each risk, walk this list and keep what applies:

- **Happy path:** the documented success behavior, once, at the cheapest layer.
- **Negative paths:** unauthorized, invalid input, expired, missing, duplicate,
  conflicting, out-of-order (roadmap #192 thinking).
- **Boundaries:** empty, one, many, max size, date/timezone edges, precision.
- **State transitions:** create→edit→delete cycles, idempotent retries,
  concurrent modification where plausible.
- **Failure handling:** dependency down/slow/erroring — what the user sees.
- **Data visibility:** who can see the result; cross-tenant/roles → delegate
  to `multi-tenant-security-tester` line items.

## Plan item quality bar

A plan item is executable when a stranger can answer: what do I set up, what
do I do, what exactly should happen, and where do I record the result. Items
failing that bar get fixed at planning time.

## Exit-criteria patterns (objective)

- "All P0/P1 plan items pass; P2 failures triaged with owner + ticket."
- "Zero open sev-1/sev-2 defects in the changed area."
- "Contract suite green against provider version X."
- "Screenshots captured for checkpoints C1–C4 per evidence rules."
- Anti-pattern: "testing complete", "QA approves", "looks good".

## Layer assignment quick table

| Behavior | Layer | Implementer skill |
| --- | --- | --- |
| pure logic/validation | unit | `vitest-unit-component-engineer` |
| service/command through DB + auth | integration | `integration-test-designer` |
| API/webhook shape & compat | contract | `api-contract-test-designer` |
| critical journey in real UI | E2E | `playwright-e2e-engineer` |
| visual/UX judgment | manual | `manual-test-case-creator` + evidence plan |
| keyboard/focus/contrast/SR | a11y | `accessibility-test-harness` |

## Release-plan extras

For release-scope plans add: regression tier selection
(`regression-suite-curator`), build QA (`vite-build-qa-engineer` for Vite
apps), clickthrough pass on changed routes (`clickthrough-test-engineer`),
and closeout via `ai-closeout-reporter` with the evidence bundle.
