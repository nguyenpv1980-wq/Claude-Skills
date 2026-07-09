---
name: context-co-update-ci-gate
description: Design the CI gate that FAILS any PR touching "important" paths without a matching context-map/notes update, plus the update protocol that keeps the map honest: every update stamps date + commit SHA scanned, status moves only on cited evidence, and an unresolved risk note is never deleted — only replaced by proof. Deliverables: important-paths list, co-update rule with a declared (never silent) no-change-needed escape hatch, check logic + failure message, protocol doc. The WRITE-BACK half of the context loop: agent-startup-context-gate makes sessions READ verified context; this gate makes changes write it back under CI enforcement. Use when the context map drifts from the code, when "update the docs" is aspirational, or to enforce context freshness on PRs. Do NOT use for session-start context loading (agent-startup-context-gate), to design or edit the pipeline itself (ci-pipeline-architect — wiring hands off there), or for the chat-history sweep (chat-backlog-reconciliation).
---

# Context Co-Update CI Gate

## Purpose

Make context freshness mechanical instead of aspirational. Every repo with a
context map, architecture notes, or living status docs has the same failure:
code changes merge, the map doesn't move, and three months later the map
describes a system that no longer exists — drift. The evidence pattern (Repo
A of the extraction report) closes the loop with CI: a workflow fails any PR
that touches important paths without also updating the context map or its
notes directory, paired with an update protocol so the forced updates are
honest rather than ritual. This skill designs both halves: the gate and the
protocol. It is the write-back complement of `agent-startup-context-gate` —
that skill makes sessions read the map; this one makes changes maintain it.

## Use When

- Use when: the repo has (or is adopting) a context map / living
  architecture-and-status doc, and it keeps drifting from the code.
- Use when: "remember to update the docs" is policy but nothing enforces it
  on PRs.
- Use when: defining which paths are "important" enough that changing them
  obligates a context update.
- Use when: forced context updates have become ritual noise ("updated map"
  with no content) — the update protocol half needs tightening.
- Do NOT use when: loading/verifying context at session START — that is
  `agent-startup-context-gate` (the read half of this loop).
- Do NOT use when: designing or editing the delivery pipeline, its stages,
  or its required checks in general — that is `ci-pipeline-architect`. This
  skill specs ONE policy gate (its trigger paths, check logic, failure
  message) and hands the pipeline wiring to that skill or a human.
- Do NOT use when: sweeping chat history into repo docs on a cadence — that
  is `chat-backlog-reconciliation`; this gate acts at PR time on code paths.
- Do NOT use when: governing documentation lifecycle/retirement (retention
  categories, cleanup rules) — that is `docs-retention-index` (now shipped),
  not this gate.

## Inputs to Inspect

1. The context artifact(s) the gate will protect: the context map file, a
   `docs/context/**` notes directory, or equivalent — and whether one even
   exists yet (if not, the map's minimal shape is part of the deliverable).
2. The repo's real change surface: which directories hold behavior that the
   map describes (source roots, schema/migrations, API routes, workflows,
   agent-instruction files). These become important-path candidates.
3. Recent drift evidence: PRs that changed important surfaces with no map
   update — they calibrate the paths list and justify the gate.
4. The CI system in play (e.g. GitHub Actions) and existing required checks
   — the gate must fit the repo's check conventions; wiring composes
   `ci-pipeline-architect`.
5. The map's existing update habits, if any — date stamps, SHA references,
   status vocabulary — so the protocol codifies rather than invents.

## Workflow

1. **Define the important-paths list** — explicit globs, reviewed by the
   human. Start narrow (schema, API surface, auth/RLS, workflows,
   agent-instruction files) and widen with drift evidence; a too-broad list
   turns the gate into noise and breeds ritual updates.
2. **Define what counts as a context update:** a diff to the context map or
   its notes directory in the SAME PR. State the honest escape hatch: a PR
   may declare "no context change needed: <reason>" via the mechanism the
   design chooses (PR-body marker or an explicit no-op note in the notes
   dir) — visible and reviewable, never silent. The declaration is a
   reviewable claim; a reviewer may reject it.
3. **Spec the gate's check logic** (reference implementation shape:
   [references/gate-design.md](references/gate-design.md)): compute the PR's
   changed files against its base; if any match important paths AND none
   match the context artifacts AND no declared escape hatch is present →
   FAIL with an instructive message (which paths triggered, what update or
   declaration would satisfy, link to the protocol). Fail-closed on
   classifier errors.
4. **Write the update protocol** the forced updates must follow:
   - every map/notes update stamps its DATE and the COMMIT SHA scanned —
     an undated update poisons later freshness checks;
   - status moves on cited evidence only (a section flips
     "risky → verified" only with the verifying artifact linked);
   - an unresolved risk note is NEVER deleted — it is replaced by proof of
     resolution or it stays;
   - updates append/amend surgically; no wholesale rewrites inside a
     feature PR.
5. **Hand off the wiring.** Deliver the gate spec (and reference YAML shape)
   to `ci-pipeline-architect` or the human for installation as a required
   check — this skill does not edit pipeline files itself. Note the
   interaction explicitly: if the repo uses a single aggregate required
   check (`sharded-validation-with-resume` pattern), this gate feeds that
   aggregate rather than adding a separate required name.
6. **Define the maintenance loop:** the paths list and protocol live in the
   repo; changing THEM is itself an important-path change (self-gating), and
   drift evidence reviews the list on a cadence.

## Output Format

```
CONTEXT CO-UPDATE GATE DESIGN
Protected context artifacts:  <map file, notes dir>
Important paths (globs):      <list + why each>
Co-update rule:               <what satisfies: map/notes diff | declared no-op with reason>
Escape hatch mechanics:       <marker/note format; reviewable, never silent>
Gate check logic:             <changed-files → decision; fail-closed on errors>
Failure message (verbatim):   <instructive text the failing PR sees>
Update protocol:              <date+SHA stamp, evidence-only status moves,
                               risk notes never deleted without proof>
Wiring handoff:               <to ci-pipeline-architect/human; required-check
                               placement incl. aggregate-gate interaction>
```

## Validation Checklist

- [ ] Important paths are explicit globs with a stated reason each — no
      "everything important" hand-waving.
- [ ] The escape hatch is declared, visible, and reviewable — no silent
      skip; its absence on a triggering PR fails the gate.
- [ ] The failure message tells the author exactly how to satisfy the gate.
- [ ] The protocol requires date + commit-SHA stamps on every update.
- [ ] Status moves require cited evidence; risk-note deletion without proof
      is forbidden in the protocol text.
- [ ] Gate fails closed on its own errors (cannot compute diff → fail, not
      pass).
- [ ] Pipeline wiring is a handoff, not an edit this skill performed; the
      aggregate-required-check interaction is addressed.

## Gotchas

- **Ritual updates:** a gate without the protocol produces "updated map"
  commits that touch a changelog line and say nothing. The protocol (date +
  SHA + evidence-cited status moves) is what makes forced updates real.
- **The over-broad paths list** makes every PR a context PR; authors then
  automate the ritual and the map rots with timestamps ON it.
- **Silent escape hatch:** allowing the gate to auto-pass on "small" diffs
  reintroduces drift through the small-change door — the no-op must be a
  declared, reviewable claim.
- **Deleting resolved-looking risk notes:** a risk note that no longer
  reproduces is not resolved, only unobserved; the protocol's
  replace-with-proof rule exists for exactly this.
- **Docs-only PRs that edit the map itself** must not require a second meta
  update — the gate passes when the context artifacts ARE the change.
- **Required-check naming:** if the gate is its own required status check,
  conditional-skip logic can strand branch protection; prefer feeding an
  aggregate gate where that pattern exists (see
  `sharded-validation-with-resume`).

## Stop Conditions

- Asked to design the gate for a repo with NO context artifact and no
  willingness to create one — stop; a gate protecting nothing is pure
  friction. Offer the minimal map shape first.
- Asked to weaken the protocol so status can move without evidence, or so
  stale risk notes can be deleted "for tidiness" → refuse; that converts
  the map from evidence into decoration.
- Asked to directly edit `.github/workflows/**` to install the gate →
  hand off instead: pipeline-definition edits are `ci-pipeline-architect`'s
  manual-only territory (behavior-steering config).
- The important-paths list cannot be agreed with the human (everything or
  nothing) → deliver the drift evidence and a starter list, and stop short
  of installing a gate that will be resented and bypassed.

## Supporting Files

- [references/gate-design.md](references/gate-design.md) — reference check
  logic (pseudocode + GitHub Actions shape), escape-hatch marker formats,
  failure-message template, and the full update-protocol text.
- `evals/evals.json` — behavior cases incl. the declared no-op path and
  refusing protocol weakening.
- `evals/trigger-evals.json` — discrimination against
  `agent-startup-context-gate`, `ci-pipeline-architect`, and
  `chat-backlog-reconciliation`.
