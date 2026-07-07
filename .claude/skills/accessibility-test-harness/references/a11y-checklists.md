# A11y Checklists & Split Table

Detail file for `accessibility-test-harness`. Loaded on demand.

## Automated vs manual split (core table)

| Check | Automated? | Notes |
| --- | --- | --- |
| missing accessible name/label | yes (axe/lint) | component + E2E layers |
| ARIA validity / role misuse | yes | lint + scan |
| duplicate ids, landmark presence | yes | scan |
| color contrast (flat backgrounds) | mostly | browser layer; tokens in CI |
| contrast over images/gradients/states | manual | judgment |
| tab order sensibility | manual | machine sees order, not sense |
| focus visible (practically) | both | token check + human judgment |
| keyboard traps / escape routes | mostly manual | scripted checks catch some |
| SR announcement quality | manual | correctness ≠ usefulness |
| focus management (dialogs, route changes) | both | assertable in E2E + judged manually |
| live-region behavior for async results | both | presence automated; timing/verbosity manual |
| zoom/reflow 200%/400% | manual | layout judgment |

## Keyboard-only checklist (WCAG refs)

1. Reach every interactive control by Tab/Shift+Tab (2.1.1).
2. Focus visible at every stop (2.4.7); order follows meaning (2.4.3).
3. No traps: can always Tab/ESC out (2.1.2); dialogs contain focus and
   return it to the trigger on close.
4. Activate everything with Enter/Space; arrow-key conventions in menus,
   tabs, radios (per ARIA patterns).
5. Skip link present and functional on long pages (2.4.1).
6. No keyboard-only-invisible functionality (hover-only affordances have
   focus equivalents — 1.4.13).

## Screen-reader smoke (per committed combo)

Default AT matrix (adjust to product commitment): NVDA+Chromium/Firefox,
VoiceOver+Safari; add JAWS when enterprise obligations exist.

1. Page title and landmarks announced; headings outline the page (1.3.1,
   2.4.6).
2. Form fields announce label, required state, and errors on submit
   (3.3.1/3.3.2); error focus lands usefully.
3. Dialog open: announced, focus inside, background inert; close returns
   focus.
4. Async results (search, save confirmations) announced via live region
   (4.1.3).
5. Images: informative ones described, decorative ones silent (1.1.1).
6. Data tables: headers associated (1.3.1).

## Severity rubric (a11y-specific)

- **Blocker:** journey impossible via keyboard or SR (login unreachable,
  trap in checkout).
- **Major:** journey possible but degraded/error-prone (unlabeled critical
  field, focus lost on route change).
- **Minor:** friction with workaround (illogical but complete tab order).
- **Cosmetic:** verbosity, redundant announcements.

## Baseline-and-ratchet policy

Existing violations: record per-rule baseline counts; CI fails on any NEW
violation or count increase; burn-down items become tracked work. Never
disable a rule to go green — exclusions need written rationale in the config.
