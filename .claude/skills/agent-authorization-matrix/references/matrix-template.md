# Agent Authorization Matrix — taxonomy and template

## Action taxonomy

Classify every cell by what the action TRIGGERS, not what the git verb is
called (a push that auto-deploys is a deploy).

| Class | Actions |
|---|---|
| Observe | read files, search, run read-only commands, plan |
| Build | edit working-tree files, run tests/builds/linters locally |
| Record | commit on a feature branch, push a feature branch |
| Propose | open PR, update PR description, comment, request review |
| Decide | approve review, MERGE to protected branch, ARM/DISARM auto-merge |
| Release | tag, publish, deploy any environment |
| Sensitive | production data, secrets/credentials, history rewrites, billing |
| Steering | edit instruction files, memory stores, or this matrix itself |

## Context axis

`scratch/worktree · feature branch · protected branch · CI · staging · production`

## Default template (floor pre-filled)

Legend: **A** = AUTONOMOUS · **R** = APPROVAL-REQUIRED · **F** = FORBIDDEN.
Unlisted action = **R** by definition (deny-by-default).

| Action | scratch | feature branch | protected branch | staging | production |
|---|---|---|---|---|---|
| Observe / plan | A | A | A | A | A |
| Edit / test | A | A | R | R | F |
| Commit / push | A | A | R | — | — |
| Open PR / comment | — | A | — | — | — |
| Merge | — | R | **R — named human, always** | R | R |
| Arm auto-merge | — | **F (agents)** | **F (agents)** | F | F |
| Tag / release / deploy | F | F | R | R | R |
| Prod data / secrets / history rewrite | R | R | R | R | R |
| Edit instruction files / memory / this matrix | R | R | R | R | R |

Every **A** cell in a real matrix carries a one-line rationale; every deviation
from this floor carries the approving human's name and date inside the artifact.

## Approval semantics

- **One-time** — covers exactly the named action, once. Default.
- **Durable** — covers a class of actions; valid only when the human's wording
  says so, applied no wider than that wording, with an expiry or review date.
- Record approvals where the audit stage can find them (PR thread, approval
  log) — an approval that cannot be cited later does not exist for governance
  purposes (see `agent-governance-audit`).

## Case study — the auto-merge incident

A session armed auto-merge on a security-relevant PR while checks were still
running, then ended. In a later session the checks went green and GitHub merged
the PR to `main` — zero human review, and `mergedBy` looked routine. Two rules
in the floor exist because of this:

1. **Arming auto-merge IS the merge decision**, exercised early — so it is
   forbidden to agents outright, not merely approval-gated.
2. **Armed state outlives sessions**, so agents re-check
   `gh pr view <n> --json autoMergeRequest` after every push to their PRs and
   treat an armed state with no recorded human decision as a hazard: disarm
   (`gh pr merge --disable-auto <n>`), then flag.

The agent's terminal action on any PR into a protected branch is
**open-PR-and-STOP**.
