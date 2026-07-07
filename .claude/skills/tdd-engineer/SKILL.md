---
name: tdd-engineer
description: Implement behavior test-first with a strict red-green-refactor loop — write the failing test, run it, CONFIRM it fails for the intended reason (not a typo, import error, or wrong assertion), implement the minimal change to pass, and refactor only once green. Reports the exact commands run and their real output at every step. Use when the user asks for TDD or "tests first", when adding new behavior with a clear testable contract, when fixing a bug that should get a regression test proving the fix, or when changing code whose behavior must provably not regress. Do NOT use for exploratory spikes with no settled contract, or for pure test-suite cleanup with no behavior change.
---

# TDD Engineer

## Purpose

Deliver behavior changes where every line of production code exists to make
a previously-failing test pass. The load-bearing step is confirming the RED:
a test that fails for the wrong reason (import error, typo, tautological
assertion) proves nothing, and everything built on it is theater. The output
is a change plus a test that fails without it, passes with it, and a
transcript of the exact commands showing both states.

## Use When

- Use when: the user asks for TDD, "tests first", or a failing test before
  implementation.
- Use when: adding new behavior with a specifiable contract (inputs → 
  outputs, state transitions, error cases).
- Use when: fixing a bug — the reproduction becomes the regression test, red
  before the fix, green after.
- Do NOT use when: the contract is genuinely unknown and the task is an
  exploratory spike — say so and time-box the spike instead; TDD against a
  guessed contract hardens the guess.
- Do NOT use when: the failure's cause is unknown — `systematic-debugger`
  first; its reproduction hands off here as the regression test.
- Do NOT use when: only tests are being reorganized with no behavior change.

## Inputs to Inspect

1. The behavior contract: what inputs produce what outputs/errors/state — 
   from the request, ticket, or domain model. If it cannot be stated, stop
   (see Stop Conditions).
2. The project's test setup: runner, config, existing patterns for the module
   under change (fixtures, factories, mocking conventions), and the exact
   command that runs a single test file.
3. The code under change and its current tests — extend existing suites in
   their style rather than founding a parallel one.
4. CI configuration — what will run this test later must run it the same way.

## Workflow

1. **State the contract** as concrete cases: happy path, edges, error
   behavior. Each case becomes a test; pick the smallest that forces the
   change to exist.
2. **Write the failing test** in the project's established style, asserting
   on observable behavior (return values, state, emitted errors) — not on
   implementation details (call counts, private state), which weld the test
   to today's structure.
3. **Run it and confirm RED for the right reason.** Read the actual failure
   output: an assertion failure describing the missing behavior is confirmed
   red; an import error, name error, fixture crash, or an unexpectedly
   passing test means the test is wrong — fix the test, not the code, and
   re-run before proceeding. Record the failure line.
4. **Implement the minimal change** that makes that test pass. Minimal means
   no speculative parameters, no extra behavior "while here" — the next test
   earns the next behavior.
5. **Run the test — confirm GREEN.** Then run the module's wider suite to
   catch collateral damage. Record both results.
6. **Refactor only now**, with green as the invariant: rename, extract,
   deduplicate — re-running the suite after each move. Behavior changes are
   not refactoring; they need to return to step 1.
7. **Repeat** for the next case until the contract is covered.
8. **Report** the loop transcript: each red (with reason), each green, exact
   commands, final suite status.

## Output Format

```
TDD LOOP — <behavior>
Contract cases: <case → expected>
Iteration n:
  RED:   <test name> — command: <exact command>
         failed as intended: <the assertion message proving the right reason>
  GREEN: <command> — passing; wider suite: <result>
  REFACTOR: <moves made, suite re-run result> | none
Final: <suite command + full result>
Coverage of contract: <cases covered / deferred (with reason)>
```

## Validation Checklist

- [ ] Every red was confirmed to fail for the INTENDED reason, with the
      failure message quoted — no unread reds.
- [ ] No production code was written before its failing test existed.
- [ ] Tests assert observable behavior, not implementation internals.
- [ ] Each implementation step was minimal; speculative generality absent.
- [ ] Refactoring happened only under green, and the suite ran after it.
- [ ] Exact commands and real output reported — including any failures kept.
- [ ] New tests run under CI's invocation, not only via a local shortcut.

## Gotchas

- The most dangerous test is one that passes immediately: it means the
  behavior already exists, the assertion is tautological, or the wrong code
  path is exercised. Investigate; never shrug and move on.
- Failing for the wrong reason (missing import, bad fixture) looks like red
  and validates nothing — the failure MESSAGE is the evidence, not the exit
  code.
- Mock-heavy tests can go green while the real integration is broken;
  mock at the boundary the project already mocks at, and no deeper.
- Writing all the tests up front, then all the code, is not TDD — it loses
  the design feedback and usually produces untestable interfaces mid-batch.
- A "minimal" implementation that hardcodes the test's exact input is legal
  TDD only if the next test forces generalization — write that next test.
- Watch for the suite passing because the new test never ran (wrong file
  pattern, skipped marker); confirm the count of executed tests moved.

## Stop Conditions

- The contract cannot be stated as concrete cases even after asking → stop;
  the task is a spike or a modeling question, not TDD.
- The failing test requires touching shared fixtures/config whose blast
  radius exceeds the task → surface before editing them.
- The minimal implementation would change a public contract other code
  depends on → reclassify via `change-classification-gate`; that is not a
  "minimal change" anymore.
- The pre-existing suite is red before the work starts → report the baseline;
  do not build on, or "fix", unrelated failures without a decision.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `docs-first-implementer`
  and `systematic-debugger` (implementation cluster).
