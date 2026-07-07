# Evidence Rules Reference

Detail file for `screenshot-evidence-planner`. Loaded on demand.

## Checkpoint selection catalog

Evidence-worthy states (justify each against a consumer):

| State class | Why captured |
| --- | --- |
| Requirement-proving state | the visible outcome an acceptance criterion names |
| Before/after destructive action | proves confirmation + correct result |
| Permission-view difference | persona A vs persona B on the same route |
| Error/empty states under test | proves graceful handling shipped |
| Defect evidence | every filed defect gets its capture |
| Compliance-named states | whatever the obligation text actually requires |

Not evidence-worthy by default: every navigation step, every passing form,
duplicate states across viewports without a viewport-specific risk.

## Naming token table

Pattern: `<cp-id>--<route-or-case>--<persona>--<build>--<yyyymmdd-hhmmss>.png`

- `cp-id`: checkpoint id from the catalog (`CP-INV-03`) or `DEFECT-<id>`.
- `route-or-case`: kebab route (`settings-billing`) or case id (`MC-INVITE-004`).
- `persona`: role token (`admin`, `member`), never a real name/email.
- `build`: short commit SHA or build number.
- Counter-example: `Screenshot (47).png` — unlocatable, unattributable.

## Masking classes

| Class | Contents | Rule |
| --- | --- | --- |
| M0 public | synthetic seed data only | no masking needed — preferred path |
| M1 internal | internal test accounts, no PII | mask tokens/keys if visible |
| M2 sensitive | any real PII, financials, tenant names | block-out before storage; restricted store |
| M3 cross-tenant | any other tenant's data visible | do not store; recapture with seeded data; report as an isolation observation |

Method: opaque block-out. Blur/pixelation of text is recoverable; crop loses
context. Masking happens before the file reaches storage.

## Metadata schema (sidecar or report table)

`{capture_id, checkpoint_id, case_or_session_id, build, environment,
persona, viewport, captured_at, masked: bool, storage_class}`

Auto-derive everything derivable (build, timestamp, viewport); humans only
supply the checkpoint/case linkage.

## Storage-class matrix

| Class | Location | Retention | Access |
| --- | --- | --- | --- |
| PR artifact | CI artifact store | short (e.g. 30d) | repo access |
| Release evidence | release record/tag bundle | product policy (e.g. 1-2y) | team |
| Compliance archive | designated archive | per obligation text | restricted |
| Raw Playwright traces | CI artifacts only | shortest | restricted (unmasked by design) |
