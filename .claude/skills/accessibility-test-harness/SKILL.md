---
name: accessibility-test-harness
description: Design the accessibility verification harness — WCAG-oriented coverage of keyboard operability (tab order, visible focus, no traps), accessible names/labels/roles, focus management in dialogs and route changes, color contrast, and screen-reader expectations (announcements, landmarks, live regions) — as BOTH automated tooling (axe-style scans in component and E2E layers, contrast checks in CI) AND a manual checklist for what automation cannot judge. Findings map to WCAG criteria with severity and evidence. Use when asked to test/verify accessibility, set up a11y checks or CI scanning, write a keyboard-only or screen-reader test pass, or when an a11y complaint/audit obligation lands. Produces harness design, configs, checklists; execution handed to the wired layers. Do NOT use for a general UI walkthrough (clickthrough-test-engineer), general manual cases (manual-test-case-creator), implementing a11y FIXES, or non-a11y evidence policy (screenshot-evidence-planner).
---

# Accessibility Test Harness

## Purpose

Produce the harness that verifies accessibility instead of asserting it:
automated scans placed at the right layers (component tests, E2E pass, CI)
for what machines can catch, plus a manual keyboard/screen-reader checklist
for what they cannot — with every check tied to a WCAG criterion, a severity
rubric, and evidence conventions. Automation finds roughly a third of real
a11y failures; the harness is honest about which third and covers the rest
manually.

## Use When

- Use when: asked to test, verify, or "check" accessibility of an app,
  feature, or component set.
- Use when: setting up automated a11y scanning (axe-style) in component
  tests, E2E, or CI.
- Use when: a keyboard-only or screen-reader verification pass is requested,
  or an audit/complaint/legal obligation (WCAG/EN 301 549/ADA-adjacent)
  needs a repeatable verification harness.
- Use when: a design system or form framework needs per-component a11y
  acceptance checks.
- Do NOT use when: the ask is a general UI walkthrough for breakage —
  `clickthrough-test-engineer` (this harness is the a11y-specialized pass).
- Do NOT use when: writing general manual test cases —
  `manual-test-case-creator` (a11y checklist items follow ITS
  stranger-executable format but live here).
- Do NOT use when: implementing the FIXES (component/markup changes) — that
  is product work reviewed by `code-reviewer`; this skill verifies.
- Do NOT use when: general screenshot policy — `screenshot-evidence-planner`
  (a11y evidence follows its rules).

## Inputs to Inspect

1. The target standard and obligation: WCAG version/level (2.1/2.2, AA
   typical) from compliance requirements, contracts, or default to AA —
   stated explicitly.
2. The surfaces in scope: routes, critical journeys, the component library
   (design-system components multiply coverage — one accessible Button fixes
   a thousand instances).
3. Existing automation layers to wire into: component test setup
   (`vitest-unit-component-engineer` conventions), E2E suite
   (`playwright-e2e-engineer`), CI tiers (`qa-automation-architect`
   blueprint).
4. Known a11y state: prior audit findings, existing lint rules
   (eslint-plugin-jsx-a11y-style), testid-fallback flags from the Playwright
   suite (each is a missing-semantics lead).
5. Assistive-tech expectations: which screen reader × browser combos the
   product commits to (defaults in the reference).

## Workflow

1. **Pin the standard and scope.** WCAG version + level + the surface list
   (critical journeys first, component library in parallel). Every later
   finding cites its criterion.
2. **Split checks: automated vs manual — explicitly.** Machines catch
   missing names/labels, role misuse, contrast (mostly), duplicate ids,
   ARIA validity; humans judge focus order sensibility, announcement
   quality, keyboard flow usability, context changes. The split table lives
   in [references/a11y-checklists.md](references/a11y-checklists.md); every
   check lands on exactly one side (or both, with reason).
3. **Design the automated tier:** axe-style scan assertions in component
   tests (fail on new violations per component), an E2E a11y pass scanning
   each critical-journey page state, contrast checking against the token
   palette in CI, and a11y lint at the PR tier. Baseline-then-ratchet for
   existing violations: freeze the count, forbid new ones, burn down.
4. **Design the manual tier as executable checklists:** keyboard-only pass
   (reach everything, visible focus, no traps, logical order, ESC/arrow
   conventions), screen-reader smoke per committed combo (landmarks, form
   labels/errors announced, dialog focus containment + announcement, live
   regions for async results), zoom/reflow at 200/400%, contrast spot
   checks automation can't see (text over images, states). Each item:
   steps, expected, WCAG ref — stranger-executable per
   `manual-test-case-creator` format.
5. **Define severity + evidence:** blocker (journey impossible by keyboard/
   SR) → cosmetic; evidence per finding (what, where, criterion, how
   reproduced, capture per evidence rules).
6. **Place in CI and cadence:** component scans on PR (blocking on NEW
   violations), journey scan on merge/nightly, manual passes per release and
   on a11y-relevant changes; wire ownership.
7. **Hand off execution:** scan wiring lands via the engineer skills
   (manual-only where they run browsers/builds); manual passes to testers /
   `clickthrough-test-engineer` sessions; fixes to product owners — this
   skill re-verifies after.

## Output Format

```
A11Y HARNESS — <scope>
Standard: <WCAG version/level + obligation source>
Scope: <journeys, routes, components>
Automated tier:
  <layer (component/E2E/CI-lint/contrast) → tool/config → violation policy
   (baseline + ratchet) → CI placement>
Manual tier:
  <checklist id> — <keyboard|screen-reader|zoom|contrast-judgment> —
  steps/expected/WCAG ref — cadence
AT matrix: <screen reader × browser combos committed>
Split rationale: <what automation covers vs cannot — explicit>
Severity rubric: <blocker→cosmetic with a11y-specific definitions>
Evidence: <per evidence-planner rules; finding format with WCAG citation>
Ownership & cadence: <who runs what, when; re-verification loop>
Handoffs: <wiring → engineer skills; fixes → product/code-reviewer>
```

## Validation Checklist

- [ ] WCAG version/level pinned and every check cites a criterion.
- [ ] Automated/manual split is explicit; nothing automation can't judge is
      claimed as automated coverage.
- [ ] Keyboard checklist covers reach-everything, visible focus, no traps,
      order, and dialog/ESC behavior.
- [ ] Screen-reader checks name the committed AT × browser combos.
- [ ] New-violation policy (baseline + ratchet) defined for automated scans.
- [ ] Severity rubric is a11y-specific (keyboard-impossible ≠ cosmetic).
- [ ] Findings format includes criterion, reproduction, and evidence.
- [ ] No component fixes implemented here.

## Gotchas

- Automated scans passing ≠ accessible: axe-style tools catch ~30-40% of
  WCAG failures; claiming "accessible, scans green" is the classic
  false-confidence failure — the manual tier is not optional.
- ARIA is a repair tool, not a feature: scan-driven ARIA sprinkling
  (role/aria-label on everything) often makes screen-reader UX worse;
  prefer native semantics findings.
- Focus "visible" per contrast math can still be practically invisible —
  human judgment item, not just a token check.
- Contrast tools miss text over images/gradients and state colors
  (hover/disabled) — keep them in the manual judgment list.
- jsdom-based scans can't evaluate visibility/contrast reliably — put those
  checks at the browser layer, not the component layer.
- Testid fallbacks in the E2E suite are missing-semantics leads: a control
  automation can't target by role, AT users can't target either.

## Stop Conditions

- No standard/level can be pinned (no obligation, no default accepted) →
  ask; findings without a criterion baseline are opinions.
- The committed AT matrix is unknown and screen-reader checks would be
  speculative → propose the default matrix and get it confirmed.
- Scan wiring requires running builds/browsers now → hand to the manual-only
  engineer skills rather than executing here.
- The scope is a full formal conformance audit (VPAT/legal) → that is a
  specialist engagement; this harness feeds it but doesn't replace it — say
  so.

## Supporting Files

- [references/a11y-checklists.md](references/a11y-checklists.md) — the
  automated-vs-manual split table, keyboard and screen-reader checklists
  with WCAG refs, AT matrix defaults, severity rubric.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the UI/manual cluster
  (a11y vs general walkthrough vs general cases).
