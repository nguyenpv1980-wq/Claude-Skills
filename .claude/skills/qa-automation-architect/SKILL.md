---
name: qa-automation-architect
description: Design the test-automation architecture that implements a QA strategy — tool/runner selection per layer with rationale, test project structure and naming, fixture/helper/factory layers, auth-state handling, parallelization and isolation rules, reporting/artifact conventions, CI pipeline placement (what runs on PR vs merge vs nightly, sharding, retry policy), and the flake-management policy. Produces the automation blueprint and migration steps from the current setup — it does not write the individual tests. Use when asked to design or overhaul a test framework/harness, choose test tooling, structure a test codebase, fix an automation setup that is slow/tangled/unparallelizable, or wire test suites into CI properly. Do NOT use to define WHAT to test (qa-strategy-architect / test-plan-designer), implement specific tests (the engineer skills), or diagnose one flaky test (flaky-test-detective).
---

# QA Automation Architect

## Purpose

Produce the automation blueprint that turns layer decisions into a working,
maintainable machine: which tools run each layer, how the test code is
structured, how fixtures and auth state are shared without coupling, how
suites run in parallel without collisions, what artifacts they emit, and
exactly where each suite sits in CI. The blueprint includes migration steps
from the current setup; individual test implementation stays with the
engineer skills.

## Use When

- Use when: asked to design/set up/overhaul a test framework, harness, or
  automation stack.
- Use when: choosing tooling (runner, assertion, browser automation) for one
  or more layers.
- Use when: an existing automation setup is slow, serially-bound, tangled
  (shared mutable fixtures), or produces no useful artifacts.
- Use when: wiring suites into CI — tiers, sharding, retries, caching.
- Do NOT use when: deciding WHAT should be tested — `qa-strategy-architect`
  (product) or `test-plan-designer` (per change).
- Do NOT use when: implementing tests — `vitest-unit-component-engineer`,
  `playwright-e2e-engineer`, etc.
- Do NOT use when: diagnosing a specific flaky test — `flaky-test-detective`
  (this skill sets the flake POLICY; the detective works cases).
- Do NOT use when: designing test data itself — `test-data-architect`
  (this skill defines where fixtures LIVE, that skill defines what they ARE).

## Inputs to Inspect

1. The QA strategy layer decisions (`qa-strategy-architect` output) — the
   blueprint implements them; no strategy → note assumptions explicitly.
2. Current automation reality: existing runners, configs (vitest/playwright/
   jest configs), test directory layout, package scripts, how long suites take.
3. CI workflows: what runs where today, runtime, flake/retry settings,
   artifact upload.
4. App architecture constraints: monorepo vs single package, framework
   (affects component-test tooling), how auth works (affects auth-state
   strategy), database availability in CI.
5. Team conventions: naming, lint rules, existing helper patterns worth
   keeping.

## Workflow

1. **Confirm the layers to implement** from the strategy; list them with
   their risk owners. The blueprint covers exactly these — no speculative
   tooling.
2. **Select tools per layer with rationale** (default stack table in
   [references/automation-blueprint.md](references/automation-blueprint.md)):
   prefer tools already in the repo unless a named deficiency justifies
   change; every choice records the alternative rejected and why.
3. **Design the structure:** directory layout per layer, naming conventions,
   where fixtures/factories/helpers live, import boundaries (tests must not
   import app internals across layers). Auth-state strategy: how tokens/
   sessions per persona are minted once and reused safely.
4. **Design isolation & parallelization:** per-worker data namespacing
   (compose `test-data-architect` for the data design), no shared mutable
   state, port/resource allocation, DB strategy per layer (transaction
   rollback vs schema-per-worker vs truncation).
5. **Define reporting & artifacts:** report formats, failure artifacts
   (traces, screenshots, logs) per layer, retention, and where evidence
   conventions from `screenshot-evidence-planner` plug in.
6. **Place suites in CI:** PR / merge / nightly tiers with runtime budgets,
   sharding plan, cache strategy, retry policy (retries mask flakes —
   bounded, logged, and always fed to `flaky-test-detective`), and the
   quarantine mechanism governed by `regression-suite-curator`.
7. **Write the migration plan:** ordered, small steps from current state to
   the blueprint, each independently shippable and verifiable.

## Output Format

```
AUTOMATION BLUEPRINT — <repo/product>
Layers implemented: <layer → runner/tooling → rationale + rejected alternative>
Structure: <directory layout, naming, fixture/helper/factory placement>
Auth-state strategy: <persona token minting + reuse rules>
Isolation & parallelization: <per-worker namespacing, DB strategy, resource rules>
Reporting & artifacts: <per layer: report format, failure artifacts, retention>
CI placement: <tier map (PR/merge/nightly), runtime budgets, sharding,
              retry policy + flake routing>
Flake policy: <detection → quarantine (curator) → diagnosis (detective) → expiry>
Environment assumptions: <what CI/local must provide per layer>
Migration plan: <ordered steps from current state, each verifiable>
Handoffs: <test implementation → engineer skills; data design → test-data-architect>
```

## Validation Checklist

- [ ] Every tool choice has rationale and a named rejected alternative.
- [ ] Structure covers all strategy layers; no speculative extra tooling.
- [ ] Isolation rules make parallel runs collision-free (data, ports, state).
- [ ] Auth-state strategy avoids per-test re-login without sharing mutable
      sessions across workers.
- [ ] Artifacts named per layer; failure evidence is automatic, not manual.
- [ ] CI placement has runtime budgets and a bounded, logged retry policy.
- [ ] Flake policy routes to detection/quarantine/diagnosis owners.
- [ ] Migration plan is ordered small steps, each independently verifiable.
- [ ] No individual tests written here.

## Gotchas

- Tool churn is expensive: replacing a working runner for marginal DX gains
  costs more than it returns — bias to incumbent tools unless a deficiency is
  named.
- Unbounded CI retries convert flakes into invisible product risk; retries
  must be counted and reported or the flake policy is fiction.
- Shared login state across parallel workers causes heisenbugs (one worker's
  logout kills another's session) — persona state must be per-worker or
  immutable.
- A beautiful blueprint with a big-bang migration never lands — steps must be
  small enough to ship between feature work.
- Fixture layers that import application services couple tests to internals
  and break en masse on refactor — enforce import boundaries.

## Stop Conditions

- No strategy exists and layer choices would be arbitrary → run
  `qa-strategy-architect` first or record explicit layer assumptions and get
  them confirmed.
- The blueprint requires infrastructure decisions above this scope
  (provisioning CI runners, buying tooling) → present options via
  `human-approval-boundary` rather than assuming budget.
- Executing the migration (moving files, rewriting configs) is requested in
  the same pass → that is an implementation change; confirm scope and
  classification first.

## Supporting Files

- [references/automation-blueprint.md](references/automation-blueprint.md) —
  default stack table per layer, directory layout patterns, DB isolation
  options compared, and CI tier/sharding worksheets.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the strategy/plan/coverage
  cluster (architecture vs strategy vs plan vs audit).
