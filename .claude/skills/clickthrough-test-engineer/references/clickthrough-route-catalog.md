# Clickthrough Route Catalog

Detail file for `clickthrough-test-engineer`. Loaded on demand.

## Per-route interaction checklist

Apply the rows that exist on the route; mark N/A explicitly.

| Item | What to do | Common failures |
| --- | --- | --- |
| Direct navigation | hit the URL cold (new tab) | guard missing, infinite spinner, crash on no-state |
| In-app navigation | reach via menus/links | dead links, wrong active state |
| Forms — valid | submit realistic valid input | silent failure, no feedback, double-submit duplicates |
| Forms — invalid | empty required, over-length, wrong format, paste junk | no validation, cryptic errors, data loss on error |
| Dialogs/modals | open, ESC, backdrop click, cancel, confirm | focus lost, background scroll, state leak after cancel |
| Permission gates | try controls per persona (member vs admin) | hidden-but-callable actions, visible-but-broken controls |
| Empty states | route with zero data | raw "undefined", broken layout, no CTA |
| Loading states | throttle/first load | layout shift, spinner forever on error |
| Error states | trigger a failing action where safe | blank screen, unhandled rejection in console |
| Destructive actions | delete/remove on session fixtures ONLY | no confirmation, confirmation deletes wrong thing |
| Back/refresh | browser back after submit; F5 mid-flow | resubmission, lost state, auth loop |
| Console | check on every route | errors/warnings on "working" pages |

## Viewport set

Default: desktop 1280×800 + one mobile width (375×812) on customer-facing
routes. Deep responsive QA is its own effort; here mobile only needs to be
usable on the critical routes.

## Session evidence defaults

Used when no `screenshot-evidence-planner` policy exists:
- Name: `<route>--<step>--<pass|defect>--<yyyymmdd-hhmm>.png`
- Mask: emails, names, tokens, ids that look real — before storage.
- Store: the session's report directory, referenced from the defect table.
- Metadata: build id + persona + viewport in the report row, not burned into
  the filename beyond the pattern above.

## Severity rubric

- **Blocker:** journey cannot proceed / data loss / security-relevant.
- **Major:** feature broken with no workaround.
- **Minor:** broken with workaround, or wrong-but-recoverable.
- **Cosmetic:** visual/copy issues.

Security-relevant observations (cross-tenant data visible, hidden admin
control callable) are filed as blockers AND routed to the security skills —
never sat on until the report is done.
