---
name: qa-strategy-architect
description: Define the product- or repo-level QA strategy — a risk inventory ranked by business/security impact, the test-layer split (what gets unit, integration, contract, E2E, manual coverage and WHY), ownership per layer, environment and test-data posture, required evidence per change class, and CI gate placement. QA starts from risk, and every layer choice picks the cheapest reliable layer for that risk. Use when asked how a product should be tested overall, to define or overhaul a test strategy, to decide which test layers a codebase needs, or when testing effort is ad-hoc and nobody can say what must pass before release. Do NOT use for a single feature/release test plan (test-plan-designer), auditing which tests exist today (test-coverage-mapper), or designing the automation tooling/framework itself (qa-automation-architect).
---

# QA Strategy Architect

## Purpose

Produce the governing QA strategy for a product or repository: what risks
exist, which test layer owns each risk at the cheapest reliable cost, who owns
each layer, what environments and data those layers assume, and what evidence
must exist before a change ships. The strategy is the document every other QA
skill in this pack composes against — test plans instantiate it per change,
coverage mapping audits against it, and automation architecture implements it.

## Use When

- Use when: asked "how should we test this product/repo" or to define/overhaul
  a QA or test strategy.
- Use when: test effort exists but is ad-hoc — no one can say which layers are
  required, what must pass before release, or why a test belongs where it is.
- Use when: a new product/major subsystem is starting and QA posture must be
  set before test code accumulates.
- Do NOT use when: the ask is a test plan for ONE feature or release — that is
  `test-plan-designer` (it instantiates this strategy).
- Do NOT use when: the ask is "what do our tests cover today" — that is
  `test-coverage-mapper` (audit, not strategy).
- Do NOT use when: the ask is to design the automation framework, tooling, or
  CI mechanics — that is `qa-automation-architect` (it implements this
  strategy's layer decisions).
- Do NOT use when: the ask is a whole-repo health audit — that is the shipped
  `full-codebase-auditor`; this skill governs testing, not general code health.

## Inputs to Inspect

1. What the product does and for whom: README, docs, routes/commands, the
   domain model if one exists (`domain-modeler` output).
2. Existing test reality: test directories, runners in use, CI workflow files,
   what currently gates a merge.
3. Risk sources: security-sensitive surfaces (auth, tenant boundaries,
   payments, exports), prior incidents/bug history, compliance obligations.
4. Change classes in use (`change-classification-gate` output if present) —
   the strategy maps each class to a validation floor.
5. Team/ownership signals: CODEOWNERS, who fixes broken tests today.

## Workflow

1. **Build the risk inventory first.** Enumerate failure modes that matter:
   data loss/corruption, cross-tenant leakage, broken auth, money errors,
   broken critical journeys, regressions in integrations. Rank by impact ×
   likelihood. No layer decisions before this exists — QA starts from risk.
2. **Assign each risk to the cheapest reliable layer.** Use the decision
   table in [references/risk-and-layer-catalog.md](references/risk-and-layer-catalog.md):
   pure logic → unit; boundary behavior (service/DB/auth) → integration;
   schema/shape compatibility → contract; critical user journeys (few) → E2E;
   visual/judgment checks → manual + screenshot evidence. A risk covered at
   a more expensive layer than necessary is a finding, not a virtue.
3. **Declare the layer split explicitly** — automation vs manual is a named
   decision per risk area, never an accident. Security negative testing
   (cross-tenant, authorization) is delegated to the shipped
   `multi-tenant-security-tester` and `rls-policy-auditor`, not re-owned here.
4. **Define environments and data posture per layer:** what runs against
   in-memory fakes, what needs a seeded database, what needs a deployed
   environment; where test data comes from (delegate design to
   `test-data-architect`).
5. **Define required evidence per change class:** which checks are blocking,
   which artifacts (reports, screenshots per `screenshot-evidence-planner`)
   must exist, and what "green" means for docs-only vs schema vs UI changes.
6. **Place the CI gates:** which layers run on PR, on merge, nightly; what is
   allowed to be non-blocking and why; flake policy pointer
   (`flaky-test-detective` owns diagnosis, `regression-suite-curator` owns
   suite membership).
7. **Name ownership and exit criteria:** who owns each layer, who fixes red,
   and the strategy's own review date.

## Output Format

```
QA STRATEGY — <product/repo>
Risk inventory: <ranked risks, each with impact and likelihood rationale>
Layer decisions: <risk → layer → why this is the cheapest reliable layer>
Automation/manual split: <explicit, per risk area>
Environments & data: <per layer: env assumption + data source (test-data-architect)>
Evidence per change class: <class → blocking checks + required artifacts>
CI placement: <PR / merge / nightly per layer; non-blocking exceptions + why>
Ownership: <layer → owner; red-build policy>
Delegations: <security negatives → multi-tenant-security-tester / rls-policy-auditor;
             per-change plans → test-plan-designer; tooling → qa-automation-architect>
Exit criteria & review date: <when this strategy is met; when it is re-reviewed>
```

## Validation Checklist

- [ ] Risk inventory exists and every layer decision traces to a named risk.
- [ ] Every layer choice states why a cheaper layer was insufficient.
- [ ] Automation/manual split is explicit per risk area.
- [ ] Environment assumptions and test-data source named per layer.
- [ ] Evidence requirements defined per change class, including artifacts.
- [ ] CI placement defined (PR/merge/nightly) with named non-blocking exceptions.
- [ ] Ownership and exit criteria stated; review date set.
- [ ] Security negative testing delegated, not duplicated.

## Gotchas

- A strategy written from the org chart ("we have QA engineers, so manual
  everything") instead of the risk inventory produces expensive, slow
  coverage — always derive layers from risks.
- Inverted pyramids (everything E2E) usually come from missing seams; flag the
  architectural cause, don't just prescribe "write more unit tests."
- "100% coverage" as a goal is a smell — coverage percentage is an input to
  `test-coverage-mapper`, not a strategy objective.
- Strategies that omit manual/judgment testing entirely leave visual, UX, and
  exploratory risks unowned — the split must be explicit even when the answer
  is "none, because X".
- A strategy nobody can violate is a strategy nobody follows: every rule needs
  a blocking check or a named owner.

## Stop Conditions

- The product's purpose or critical journeys cannot be determined from the
  repo and no one has described them → ask; a risk inventory cannot be
  invented.
- Risk ranking requires business context (revenue impact, compliance scope)
  that is not available → present the inventory with explicit assumptions and
  ask for ranking confirmation instead of guessing.
- The ask turns into implementing the strategy (writing tests, CI changes) →
  that is `qa-automation-architect` / the engineer skills; confirm scope
  before proceeding.

## Supporting Files

- [references/risk-and-layer-catalog.md](references/risk-and-layer-catalog.md) —
  risk taxonomy, the layer decision table, and evidence-class examples.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the strategy/plan/coverage
  cluster and against the shipped `full-codebase-auditor`.
