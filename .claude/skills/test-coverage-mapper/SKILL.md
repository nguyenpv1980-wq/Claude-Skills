---
name: test-coverage-mapper
description: Audit what the EXISTING tests actually cover — map requirements, risks, and code surfaces (routes, commands, services, schema, jobs) to the tests that exercise them, then rank the uncovered critical paths by risk. Distinguishes real verification from tests that execute code without asserting behavior. Produces a coverage map, a risk-ranked gap list, and a recommended fill order at the cheapest reliable layer. Use when asked what the tests cover, what's untested, whether coverage is good enough for a change or release, or to find the riskiest untested paths. Coverage-tool percentages are an input, not the verdict. Do NOT use to define the product QA strategy (qa-strategy-architect), plan tests for one change (test-plan-designer), judge overall test-suite quality/flake patterns (qa-automation-lead agent), or audit whole-repo health (full-codebase-auditor).
---

# Test Coverage Mapper

## Purpose

Produce an evidence-based map of what the current test suite proves, and —
more importantly — what it does not: which requirements, risks, and code
surfaces have real verifying tests, which have execution-without-assertion
theater, and which have nothing. The deliverable is a coverage map with a
risk-ranked gap list and a fill order, so investment goes to the riskiest
uncovered path first, at the cheapest reliable layer.

## Use When

- Use when: asked "what do our tests cover", "what's untested", or "is
  coverage good enough" for an area, change, or release.
- Use when: prioritizing test investment and needing the riskiest gaps first.
- Use when: a release/audit needs a coverage statement grounded in evidence.
- Do NOT use when: defining product-wide testing rules — `qa-strategy-architect`.
- Do NOT use when: planning tests for one upcoming change — `test-plan-designer`
  (it may consume this skill's map as input).
- Do NOT use when: the ask is whole-repo health (dead code, dependencies,
  debt) — the shipped `full-codebase-auditor`.
- Do NOT use when: the ask is to review a specific diff — the shipped
  `code-reviewer`.

## Inputs to Inspect

1. The test suite itself: test directories, naming, what each file actually
   asserts (read assertions, not just filenames).
2. The surfaces to map against: routes/pages, API endpoints, commands,
   services, schema/migrations, background jobs, integrations. Build this
   inventory BEFORE judging coverage.
3. Requirements/risk sources: QA strategy risk inventory if present, acceptance
   criteria, incident history, bug tracker patterns.
4. Coverage tool output if available (lcov, istanbul, coverage.py) — as a
   lead generator for unexecuted code, never as the verdict.
5. CI config: which tests actually run and gate; a test excluded from CI
   covers nothing in practice.

## Workflow

1. **Inventory surfaces first.** List the mappable units (route, endpoint,
   command, table, job). An unlisted surface can't be honestly reported as
   covered or uncovered. Method details in
   [references/coverage-mapping-method.md](references/coverage-mapping-method.md).
2. **Map tests to surfaces by reading assertions.** For each surface record:
   verifying tests (assert observable behavior), theater tests (execute but
   assert nothing meaningful — snapshot-everything, expect(true), render-only),
   or none. Note the layer of each verifying test.
3. **Cross-check with coverage-tool output** where available: unexecuted
   lines confirm "none"; executed-but-unasserted code is theater, which
   percentage tools cannot see — say so explicitly.
4. **Classify each gap by risk** using the strategy's risk inventory (or a
   quick impact × likelihood pass if no strategy exists): critical-journey
   gaps, security-relevant gaps (delegate specification of cross-tenant/authz
   negatives to `multi-tenant-security-tester`), data-integrity gaps, edge
   gaps.
5. **Rank and recommend fill order:** riskiest gap first, each with the
   cheapest reliable layer and the engineer skill that would implement it.
6. **State coverage honestly:** covered (verifying) / theater / uncovered /
   not-inspected — with counts and file references. Never let a percentage
   stand in for the map.

## Output Format

```
COVERAGE MAP — <scope>
Surface inventory: <N surfaces by kind; source of inventory>
Map:
  <surface> — <covered|theater|uncovered> — <verifying tests file:line, layer>
Theater findings: <tests executing without meaningful assertions + why>
CI reality check: <tests present but not gating, skipped/quarantined>
Gap list (risk-ranked):
  <#> <surface/behavior> — risk <why it matters> — recommended layer
      — implementer <engineer skill>
Coverage statement: covered <n> / theater <n> / uncovered <n> / not-inspected <n + why>
Handoffs: <fill items → test-plan-designer or engineer skills;
          security negatives → multi-tenant-security-tester>
```

## Validation Checklist

- [ ] Surface inventory built before coverage judgments.
- [ ] Coverage claims cite the verifying test (file:line), not filenames or
      percentages.
- [ ] Theater tests identified and excluded from "covered".
- [ ] CI-excluded/skipped tests not counted as coverage.
- [ ] Every gap has a risk rationale and a recommended cheapest layer.
- [ ] Not-inspected areas listed explicitly with reasons.
- [ ] No fix implementation attempted — gaps are handed off.

## Gotchas

- Line-coverage percentage rewards execution, not verification — a 90% number
  full of assertion-free tests maps mostly to theater.
- Test filenames lie: `payments.test.ts` covering only formatting helpers
  leaves charge logic uncovered — read the assertions.
- Mocked-to-death integration tests can show a boundary as covered while the
  real query/permission path is never exercised; record the layer honestly.
- Suites green in CI but with `.skip`, `.todo`, or quarantine tags silently
  shrink real coverage — count them as uncovered.
- E2E tests "cover" many lines incidentally; incidental execution is not
  verification of those behaviors.

## Stop Conditions

- The scope is too large to map honestly in one pass → propose a sliced scope
  (per subsystem) and map the first slice; never emit an unverified whole-repo
  claim.
- No test suite exists at all → report that in one line and route to
  `qa-strategy-architect` (strategy) rather than producing an empty map.
- Requirements/risk context is entirely absent and gaps can't be ranked →
  present the unranked map and ask for risk input instead of inventing
  priorities.
- Asked to also write the missing tests → implementation belongs to the
  engineer skills per gap; confirm scope first.

## Supporting Files

- [references/coverage-mapping-method.md](references/coverage-mapping-method.md) —
  surface inventory recipe, verifying-vs-theater test rubric, and gap-ranking
  worksheet.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the strategy/plan/coverage
  cluster and against the shipped `full-codebase-auditor` and `code-reviewer`.
