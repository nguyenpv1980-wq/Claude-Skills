# Manual Case Template & Step Rules

Detail file for `manual-test-case-creator`. Loaded on demand.

## Full case template

```
ID: MC-<area>-<###>        Trace: <REQ/plan-item id>      Priority: P0|P1|P2
Title: <behavior under test, one line>
Role/persona: <exact role + how to obtain the account>
Environment: <env name + URL + build note>
Preconditions:
  - <starting state, e.g. "workspace W1 exists with 2 members">
  - <how to reach it: seed script / setup case id>
Test data:
  - <field: exact value>  (never "a valid email" — give the email)
Steps:
  1. <ONE action, imperative> → Expected: <ONE observable result>
  2. ... [📸 CP-n: <what must be visible; mask <fields>>]
Pass/fail: pass = all expected results observed; fail = first failing step
cited + evidence captured; blocked = named precondition unavailable.
Cleanup:
  - <delete/revoke steps returning env to neutral>
```

## Step-writing rules

1. One action per step; one observable expected result per step.
2. Actions name what the tester sees: labels, buttons, menus as rendered.
3. Expected results are on-screen outcomes (visible text, navigation, state),
   never internals (API codes, DB rows, logs).
4. Boundary/negative steps state the exact invalid input to enter.
5. Timing-sensitive expectations get an explicit bound ("within 3 seconds")
   only when the requirement defines one; otherwise avoid time assertions.
6. If a step needs a judgment call (visual quality), state the criterion
   ("logo not clipped at 375px width"), not "looks right".

## Worked example (negative path)

```
ID: MC-INVITE-004   Trace: REQ-INVITE-2   Priority: P0
Title: Inviting an already-member email shows a non-destructive error
Role: workspace admin (account seed: admin@t1.test / seed-tenant-1)
Environment: staging, build <id>
Preconditions: workspace "T1" has member bob@t1.test
Test data: invite email = bob@t1.test
Steps:
  1. Open Members → Invite → Expected: invite dialog opens, Email focused
  2. Enter bob@t1.test, click Send → Expected: inline error "Already a
     member"; dialog stays open; no email badge increment [📸 CP-1: error
     visible; mask member emails]
  3. Click Cancel → Expected: dialog closes; member list unchanged (still
     shows exactly 2 members)
Pass/fail: per rules above.
Cleanup: none (no state created).
```

## Library hygiene

- Case ids stable across releases; supersede, don't renumber.
- On requirement change: query the trace field, update or retire affected
  cases in the same PR as the requirement/doc change.
- Retirement (case no longer needed) goes through `regression-suite-curator`
  rules if the case is part of the release regression pass.
