---
name: test-plan-designer
description: Design the concrete test plan for ONE feature, change, or release — the requirement/risk being verified, in-scope and out-of-scope items, the test-layer split for THIS change (what is automated at which layer, what is manual), test data needs, environment assumptions, entry/exit criteria, named artifacts, and CI placement. Every planned test traces to a requirement or risk; the plan is executable by someone who didn't write it. Use when asked to write a test plan for a feature/release/bugfix, to decide what testing a specific change needs before it ships, or to turn acceptance criteria into a verification plan. Do NOT use for the product-wide QA strategy (qa-strategy-architect), for auditing existing coverage (test-coverage-mapper), for writing the manual case steps themselves (manual-test-case-creator), or for implementing the tests (the engineer skills).
---

# Test Plan Designer

## Purpose

Produce an executable test plan for a single feature, change, or release: what
will be verified, at which layer, with what data, in which environment, and
what "done testing" means. The plan instantiates the product QA strategy
(`qa-strategy-architect` output) for one change — it names the tests to build
and hands each group to the right engineer skill; it does not implement them.

## Use When

- Use when: asked to write a test plan for a named feature, release, or fix.
- Use when: acceptance criteria exist and need to become a verification plan.
- Use when: a risky change (schema, auth, payment) needs its testing scoped
  before implementation starts.
- Do NOT use when: the ask is product-wide testing rules — that is
  `qa-strategy-architect`.
- Do NOT use when: the ask is "what do existing tests cover" — that is
  `test-coverage-mapper`.
- Do NOT use when: the ask is to write the step-by-step manual cases — the
  plan names WHICH manual cases exist; `manual-test-case-creator` writes them.
- Do NOT use when: the ask is to implement tests — hand off to
  `vitest-unit-component-engineer`, `integration-test-designer`,
  `api-contract-test-designer`, or `playwright-e2e-engineer` per the plan.

## Inputs to Inspect

1. The requirement: spec, ticket, acceptance criteria, or the diff/PR if the
   change already exists. No requirement and no diff → Stop Conditions.
2. The QA strategy (`qa-strategy-architect` output) if present — the plan must
   follow its layer rules and evidence classes; deviations are called out.
3. The change classification (`change-classification-gate` output if present)
   — it sets the validation floor.
4. Affected surfaces: routes, APIs, schema, jobs, integrations touched by the
   change; existing tests already covering adjacent behavior.
5. Test data and environment reality: what fixtures/seeds exist
   (`test-data-architect` output), what environments are actually available.

## Workflow

1. **Name the requirement and the risks.** Every plan starts with what could
   break and why it matters. Risks the change does NOT touch go in
   out-of-scope with a sentence of rationale.
2. **Derive test items from risks, not from the UI tree.** For each risk:
   the behaviors to prove (happy path, negative path, boundary), per the
   catalog in [references/test-plan-template.md](references/test-plan-template.md).
3. **Assign each item the cheapest reliable layer** (strategy rules): unit /
   integration / contract / E2E / manual. The automation-vs-manual split is
   explicit. Cross-tenant and authorization negatives are delegated to the
   shipped `multi-tenant-security-tester`, referenced as plan line items.
4. **Specify data and environment per item:** which fixtures/personas
   (delegate design gaps to `test-data-architect`), which environment, and
   any masking needs for evidence.
5. **Define entry and exit criteria:** what must be true to start (build
   green, migration applied) and to finish (all planned items pass, no open
   sev-1/2, evidence attached). Exit criteria are objective.
6. **Name artifacts and CI placement:** which items run in CI (and in which
   tier) vs pre-release manual passes; which artifacts each produces (reports,
   screenshots per `screenshot-evidence-planner` conventions).
7. **Hand off implementation:** map each plan group to its engineer skill and
   list open questions that block execution.

## Output Format

```
TEST PLAN — <feature/change/release>
Requirement & risks: <what is being verified; ranked risks>
In scope / out of scope: <items + rationale for exclusions>
Test items:
  <id> — <behavior to prove> — layer <unit|integration|contract|e2e|manual>
       — data <fixture/persona> — env <assumption> — expected <objective result>
Automation/manual split: <explicit summary + why per manual item>
Security negatives: <delegated items → multi-tenant-security-tester / rls-policy-auditor>
Entry criteria: <objective preconditions>
Exit criteria: <objective completion conditions>
Artifacts: <named outputs; screenshot checkpoints where applicable>
CI placement: <which items run on PR / merge / nightly / pre-release manual>
Handoffs: <plan group → engineer skill; open questions>
```

## Validation Checklist

- [ ] Every test item traces to a named requirement or risk.
- [ ] Out-of-scope list exists with rationale (empty scope-cuts are silent lies).
- [ ] Each item has layer, data, environment, and an objective expected result.
- [ ] Automation/manual split is explicit; each manual item says why manual.
- [ ] Entry and exit criteria are objective (a stranger could adjudicate them).
- [ ] Artifacts named; screenshot checkpoints listed where UI is affected.
- [ ] CI placement stated per item group.
- [ ] Security negative testing delegated, not re-specified.

## Gotchas

- Plans derived from the UI tree ("test every screen") instead of risks
  produce huge, shallow plans that miss the one migration that loses data.
- "Exit criteria: QA signs off" is not objective — name the passing items,
  severity threshold, and required evidence instead.
- A plan whose every item is E2E is a strategy violation — push items down to
  the cheapest reliable layer or record why not.
- Untestable acceptance criteria ("should be fast", "should be intuitive")
  must be flagged and made measurable, not silently planned around.
- Plans that assume environments or fixtures that don't exist fail at
  execution — verify availability during planning, not after.

## Stop Conditions

- No requirement, no acceptance criteria, AND no diff to infer behavior from →
  ask for the requirement; a plan cannot be invented from a feature name.
- Acceptance criteria contradict the observed code behavior → route to
  `source-of-truth-reconciler` before planning against either.
- The change is unclassified and touches schema/RLS/security → request
  classification (`change-classification-gate`) first; the validation floor
  changes the plan.
- Asked to also execute the plan in the same pass → execution is a separate
  step by the named engineer skills; confirm scope first.

## Supporting Files

- [references/test-plan-template.md](references/test-plan-template.md) —
  the full plan template, behavior catalog (happy/negative/boundary
  prompts), and exit-criteria examples.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the strategy/plan/coverage
  cluster and against `multi-tenant-security-tester` for security-test asks.
