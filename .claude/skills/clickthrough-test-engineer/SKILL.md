---
name: clickthrough-test-engineer
description: Execute a systematic interactive clickthrough of a RUNNING app — a route-by-route walkthrough plan covering navigation, forms (valid + invalid input), dialogs, permission-gated controls, empty/loading/error states, and destructive-action confirmations, then drive the UI through it, recording per-step observations with severity-rated defects and screenshot evidence at named checkpoints. One-session verification pass, not a permanent scripted suite. Use when asked to click through the app and report what's broken, smoke-check the UI before a demo/release, verify a deployed build interactively, or sanity-check changed routes after a merge. DRIVES a browser against a live app — manual invocation only. Do NOT use to build permanent automated journeys (playwright-e2e-engineer), write reusable manual test-case documents (manual-test-case-creator), run keyboard/contrast/screen-reader passes (accessibility-test-harness), or define which screenshots releases require (screenshot-evidence-planner).
disable-model-invocation: true
---

# Clickthrough Test Engineer

## Purpose

Perform a disciplined interactive walkthrough of a running application and
come back with evidence: what was clicked, what happened, what's broken and
how badly, with screenshots at named checkpoints. The deliverable is a
clickthrough report — coverage of the planned routes, per-step observations,
severity-rated defects, and evidence — from ONE session against ONE build.
This is systematic verification-by-driving, not a permanent test suite and
not exploratory wandering.

## Use When

- Use when: asked to "click through the app and see what's broken",
  smoke-check the UI before a demo or release, or verify a deployed build.
- Use when: a merge changed several routes and someone wants an interactive
  pass over the affected screens.
- Use when: manual cases don't exist yet and a structured pass must find the
  obvious breakage fast.
- Do NOT use when: the ask is a PERMANENT automated journey —
  `playwright-e2e-engineer`; a clickthrough is one session, not a suite.
- Do NOT use when: the ask is reusable step-by-step case documents for other
  testers — `manual-test-case-creator` (this skill may EXECUTE those cases,
  but writing them is that skill).
- Do NOT use when: the focus is keyboard/focus/contrast/screen-reader —
  `accessibility-test-harness` owns the a11y pass.
- Do NOT use when: deciding evidence/naming/masking policy —
  `screenshot-evidence-planner` defines it; this skill follows it.

## Inputs to Inspect

1. The running target: URL/environment, build/commit identity (record it —
   a report against "some build" is worthless), and which account(s)/roles
   are safe to use.
2. Scope: all routes, or the routes affected by a change (diff/PR list);
   route inventory from the router config where available.
3. Personas/roles available and the permission expectations per route
   (authorization matrix if present).
4. Evidence rules in force (`screenshot-evidence-planner` output): naming,
   masking, storage; defaults in the reference if none exist.
5. Known issues/quarantines, so the report doesn't re-file them as new.

## Workflow

1. **Pin the target and build the walkthrough plan.** Record environment +
   build id. Enumerate routes in scope; per route, list the interaction
   checklist items that apply (nav, forms, dialogs, permissions, states,
   destructive confirmations) from
   [references/clickthrough-route-catalog.md](references/clickthrough-route-catalog.md).
   The plan is written BEFORE clicking so coverage is checkable afterward.
2. **Establish session safety:** test accounts only; no real-customer data
   entered; destructive actions exercised only on disposable fixtures
   (compose `test-data-architect` seeds where available) — otherwise
   verify the confirmation dialog appears and CANCEL.
3. **Drive each route:** navigate (direct URL and in-app nav), exercise each
   planned interaction — forms with valid AND invalid input, dialogs
   open/close/escape, permission-gated controls per persona, empty/loading/
   error states where reachable.
4. **Observe like an instrument:** per step record expected vs observed;
   capture the browser console for errors on every route (silent console
   errors are findings); screenshot at plan-named checkpoints and at every
   defect, masked per the evidence rules.
5. **Rate and file defects:** severity (blocker/major/minor/cosmetic) +
   reproduction steps + evidence reference. A defect without repro steps and
   a screenshot is a rumor, not a finding.
6. **Report coverage honestly:** routes/interactions completed vs planned vs
   skipped (with why — auth wall, data unavailable, time). Unvisited ≠
   passing.
7. **Hand off:** blockers → `systematic-debugger`/owner immediately; recurring
   passes worth automating → `playwright-e2e-engineer` candidates (with the
   journey named); evidence bundle → release closeout (`ai-closeout-reporter`).

## Output Format

```
CLICKTHROUGH REPORT — <app> @ <env> / build <id> / <date>
Session: <persona(s)/roles used, viewport(s)>
Plan: <routes × interaction checklist — written before execution>
Results per route:
  <route> — <steps executed> — <pass | defects found> — console <clean|errors>
Defects:
  <id> — <severity> — <route/step> — expected vs observed — repro steps
       — evidence <screenshot ref>
Checkpoints captured: <named screenshots per evidence rules, masked>
Coverage: executed <n/n routes, n/n interactions> | skipped <what + why>
Automation candidates: <journeys worth a permanent Playwright spec + why>
Handoffs: <blockers → owner/systematic-debugger; evidence → closeout>
```

## Validation Checklist

- [ ] Environment + build id recorded; test accounts only.
- [ ] Walkthrough plan existed BEFORE execution; coverage measured against it.
- [ ] Forms exercised with invalid input, not just valid.
- [ ] Permission-gated controls checked per persona in scope.
- [ ] Console checked on every route; errors filed as findings.
- [ ] Every defect has severity, repro steps, and evidence.
- [ ] Screenshots follow naming/masking rules; sensitive data masked.
- [ ] Skipped items listed with reasons — no silent coverage inflation.
- [ ] No permanent spec files written (that's Playwright's lane).

## Safety Rules

- Never enter real customer data, real payment instruments, or production
  credentials during a clickthrough.
- Destructive actions on non-disposable data: verify the confirmation
  appears, then CANCEL — deletion is only completed on fixtures created for
  this session.
- If the target turns out to be production with live customers, downgrade to
  read-only navigation and flag writes for `human-approval-boundary`.

## Gotchas

- Clicking only the happy path through forms finds nothing — invalid input,
  double-submit, and back-button-after-submit are where UIs break.
- A clean-looking page with console errors is not a pass; the console is
  part of the observation surface.
- Direct-URL navigation catches missing route guards that in-app nav hides —
  always try both.
- Session bleed between personas (testing admin then member in one browser
  profile) produces false permission results — separate profiles/contexts.
- Reporting "everything works" when three routes were skipped for missing
  data is coverage inflation — the skipped list is mandatory.

## Stop Conditions

- The app won't run / can't authenticate / no safe test account → report the
  blocker; do not click through with real user credentials.
- Scope says "everything" but the route inventory is huge → propose a
  risk-ranked route subset for this session and get it confirmed.
- A blocker defect makes downstream routes untestable → file it, mark the
  affected coverage as blocked, and continue elsewhere rather than forcing.
- The target is production and the plan includes writes → stop for
  `human-approval-boundary` before any mutating step.

## Supporting Files

- [references/clickthrough-route-catalog.md](references/clickthrough-route-catalog.md)
  — the per-route interaction checklist (nav, forms, dialogs, permissions,
  states, destructive), viewport set, and default evidence conventions.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the UI/manual cluster
  and against `playwright-e2e-engineer`.
