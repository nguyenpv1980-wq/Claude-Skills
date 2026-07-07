---
name: manual-test-case-creator
description: Write full manual test cases executable by ANOTHER tester with zero tribal knowledge — each case has an id, requirement/risk trace, role/persona, environment, preconditions, exact test data, numbered steps with ONE observable expected result per step, screenshot checkpoints referenced to the evidence rules, pass/fail criteria, and cleanup. Cases cover happy, negative, and boundary paths and stay implementation-agnostic (what the user does, not what the code does). Use when asked to write manual test cases or scripts, turn acceptance criteria into an executable manual pass, build the manual regression checklist for judgment-dependent surfaces, or when a release needs a repeatable human verification pass. Do NOT use to EXECUTE a walkthrough now (clickthrough-test-engineer), define evidence naming/masking policy (screenshot-evidence-planner), write automated tests (engineer skills), or decide what should be manual vs automated (qa-strategy-architect / test-plan-designer).
---

# Manual Test Case Creator

## Purpose

Produce manual test cases that transfer: a tester who has never seen the
feature can pick one up, prepare, execute, and reach the same verdict the
author would. The bar is executability by a stranger — every case names its
data, role, environment, and per-step expected results, with screenshot
checkpoints where evidence is needed. Cases are documents (a reusable
library), not a live session.

## Use When

- Use when: asked to write manual test cases, manual QA scripts, or a manual
  regression checklist.
- Use when: a test plan marks items "manual" (visual quality, judgment calls,
  flows not worth automating) and those items need executable cases.
- Use when: acceptance criteria must become a repeatable human verification
  pass for each release.
- Do NOT use when: someone should click through the app NOW and report — 
  `clickthrough-test-engineer` (it may execute THESE cases).
- Do NOT use when: defining how screenshots are named/masked/stored —
  `screenshot-evidence-planner`; cases REFERENCE those rules.
- Do NOT use when: the ask is automated tests — the engineer skills.
- Do NOT use when: deciding the manual-vs-automated split — that decision
  arrives from `qa-strategy-architect`/`test-plan-designer`; this skill
  writes the manual side.

## Inputs to Inspect

1. The requirement/acceptance criteria/plan items each case will verify —
   every case traces to one; orphan cases are scope creep.
2. The actual UI as built (routes, labels, flows) — steps reference what a
   tester will really see; if the UI is unbuilt, cases target the spec and
   say so.
3. Personas/roles and how a tester obtains them (test accounts, seeds from
   `test-data-architect`).
4. Evidence rules (`screenshot-evidence-planner` output) for checkpoint
   references; note their absence if missing.
5. Environment(s) the pass runs against and any environment-specific
   behavior.

## Workflow

1. **List the cases before writing any.** From the plan/criteria: happy,
   negative, and boundary cases per behavior, each with an id and a
   requirement trace. Confirm the list covers the manual scope — then write.
2. **Write preconditions as setup a stranger can perform:** exact role,
   exact starting state, exact test data (values, not "some valid input"),
   environment, and how to get each (seed script, test account naming).
3. **Write numbered steps with one action and one observable expected result
   each.** "Click Save → the dialog closes and the invoice list shows the
   new row with status Draft." No compound steps, no "verify it works," no
   implementation language (API calls, DB rows) — observable UI outcomes
   only. Template in
   [references/manual-case-template.md](references/manual-case-template.md).
4. **Mark screenshot checkpoints** at the steps whose outcome is evidence-
   worthy (per the evidence rules): checkpoint id, what must be visible,
   masking note.
5. **Define the verdict:** pass = every step's expected result observed;
   fail = cite the first failing step + capture evidence; blocked = named
   missing precondition. No "partial pass".
6. **Write cleanup** returning the environment to neutral (delete created
   records, revoke invites) so the next case/run starts clean.
7. **Dry-run the case mentally as a stranger** (or execute via
   `clickthrough-test-engineer` if a session is in scope): every noun
   defined? every step observable? every datum provided? Fix gaps, then
   file the cases into the library with their traces.

## Output Format

```
MANUAL TEST CASES — <feature/scope>
Coverage summary: <requirement/risk → case ids (happy/negative/boundary)>
Case:
  ID: <MC-###>  Trace: <requirement/plan item>  Priority: <P0-P2>
  Role/persona: <exact>   Environment: <exact>
  Preconditions: <starting state + how to reach it>
  Test data: <exact values / seed reference>
  Steps:
    1. <one action> → Expected: <one observable result> [📸 CP-1: <what+mask>]
    2. ...
  Pass/fail criteria: <verdict rule>
  Cleanup: <restore-neutral steps>
Open gaps: <criteria that could not be cased + why>
Handoffs: <execution → clickthrough-test-engineer / testers;
          evidence policy gaps → screenshot-evidence-planner>
```

## Validation Checklist

- [ ] Every case traces to a requirement/risk/plan item.
- [ ] Happy, negative, and boundary paths represented per behavior in scope.
- [ ] A stranger could execute: roles, data values, environment, and
      preconditions all explicit — zero tribal knowledge required.
- [ ] Each step = one action + one observable expected result.
- [ ] Screenshot checkpoints marked with masking notes where applicable.
- [ ] Verdict rule stated; blocked ≠ failed ≠ passed.
- [ ] Cleanup returns the environment to neutral.
- [ ] No automation code written; no live session performed.

## Gotchas

- "Verify the page works correctly" is not an expected result — if the
  author can't name the observable outcome, the case isn't ready.
- Cases written from the spec while the UI diverged produce false failures —
  check the built UI, or label the case spec-derived explicitly.
- Shared test data across cases creates order dependence (case 3 passes only
  after case 1 ran) — either isolate data per case or declare the sequence.
- Steps that mention internals ("the API returns 200") aren't executable by
  a manual tester — translate to what the screen shows.
- A library without traces rots: when the requirement changes, nobody knows
  which cases to update — the trace field is load-bearing.

## Stop Conditions

- No requirement/criteria AND no built UI to derive behavior from → ask;
  cases invented from a feature name test nothing.
- Acceptance criteria are untestable as written ("intuitive", "fast") →
  return them for measurable restatement via `test-plan-designer` rather
  than writing judgment-free cases against them.
- The manual/automated split is undecided and the ask is "test cases for
  everything" → get the split from `test-plan-designer` first; manual cases
  for what should be automated waste tester time every release.
- Asked to also execute the pass now → that is a session
  (`clickthrough-test-engineer`); confirm and hand off.

## Supporting Files

- [references/manual-case-template.md](references/manual-case-template.md) —
  the full case template, step-writing rules, verdict/blocked semantics, and
  a worked example.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the UI/manual cluster.
