---
name: merge-is-deploy-governance
description: 'When the platform auto-deploys every merge to mainline, author the standing governance that makes merge==deploy safe: document that reality (including what does NOT auto-deploy); promote PR-time validation to the AUTHORITATIVE pre-production gate; reclassify post-merge validation as verification, never a gate; record the branch-protection config in-repo with WHO may change it (a human, never agents); state the accepted-risk exposure window; define rollback as revert-PR-then-auto-redeploy (squash repos: git revert <sha> — the commit is ORDINARY; -m 1 fits only true merge commits). Standing PIPELINE governance, not a per-release verdict. Use when merge deploys mainline, when post-merge checks are treated as a gate, when protection config lives only in the web UI, or after a surprise deploy-on-merge. Do NOT use to gate one release (release-readiness-reviewer), author rollback runbooks (rollback-runbook-author), define who may merge (agent-authorization-matrix), or design stages (ci-pipeline-architect).'
---

# Merge-Is-Deploy Governance

## Purpose

Stop pretending there is a deploy step when there isn't one. On platforms
that auto-deploy every merge to mainline, "we'll validate before deploying"
is a fiction — the merge IS the deploy, and any validation that runs after
it runs in production's timeline. The evidence pattern (Repo B's rulebook
documents merge-is-deploy explicitly, records the branch-protection
configuration in-repo, and defines revert-based rollback) is standing
governance that aligns the paperwork with the physics: PR-time validation
becomes the authoritative pre-production gate, post-merge checks are
demoted to verification, the protection config that enforces all this is
recorded and human-owned, and the exposure window between merge and
verified deploy is an ACCEPTED, stated risk instead of an unnoticed one.

## Use When

- Use when: the platform (PaaS, serverless host, GitOps controller)
  auto-deploys mainline on merge and no document says so.
- Use when: post-merge validation is being treated as a gate ("we'll catch
  it after merge") on such a platform.
- Use when: branch-protection/required-check configuration exists only in
  the hosting UI — unrecorded, unreviewable, silently changeable.
- Use when: after a surprise deploy-on-merge, to codify what the pipeline
  actually does before it surprises anyone again.
- Do NOT use when: deciding whether ONE release/PR is safe to ship — that
  is `release-readiness-reviewer`; this skill sets the standing rules that
  such a review runs under.
- Do NOT use when: authoring the executable rollback runbook (numbered
  steps, verification per step) — that is `rollback-runbook-author`; this
  skill fixes the rollback PRIMITIVE (revert-PR-then-auto-redeploy) that
  the runbook elaborates.
- Do NOT use when: deciding WHO may merge or arm auto-merge — that is
  `agent-authorization-matrix`; this skill composes its floors and adds the
  pipeline-reality layer.
- Do NOT use when: designing CI stages, artifact flow, or deploy strategies
  — that is `ci-pipeline-architect`.

## Inputs to Inspect

1. The platform's actual deploy trigger: hosting config (e.g. the
   platform's project settings, `vercel.json`/`netlify.toml`-class files,
   GitOps sync rules) — verify merge→deploy is real and note WHAT deploys
   (app, functions, migrations — often not all of them; the differences
   matter and get documented).
2. Current branch protection, from the source of truth: read it via the API
   where permitted (e.g. `gh api repos/<owner>/<repo>/branches/<branch>/protection`
   — requires admin scope; `gh api repos/<owner>/<repo>/rulesets` for
   rulesets) or from the human's screenshot/dictation — labeled by source
   either way.
3. The PR-time validation inventory: which checks exist, which are
   REQUIRED, and whether they are sufficient to be the last line before
   production (compose `risk-tiered-validation-selector` /
   `sharded-validation-with-resume` outputs where present).
4. The merge strategy (merge / squash / rebase) — it determines the revert
   mechanics AND, where auto-merge auditing matters, which timeline event
   names apply (`auto_merge_enabled` / `auto_squash_enabled` /
   `auto_rebase_enabled` are strategy-specific).
5. Post-merge signals available for VERIFICATION: smoke checks, health
   endpoints, deploy-status APIs — and their latency (this sets the
   exposure window's floor).

## Workflow

1. **Verify and document the reality.** State, with the platform evidence:
   merging to `<branch>` deploys `<what>` to `<environment>` with no human
   step between. List what does NOT auto-deploy (e.g. migrations that an
   operator applies — route those to `gated-deployment-prompt-template`
   territory) — partial auto-deploy is the norm and the ordering hazards
   live in the gap.
2. **Promote PR validation to the authoritative gate — in writing.** The
   governance doc names the required checks (by exact check name) as the
   pre-production gate, and states the consequence: anything not validated
   at PR time is validated in production. Gaps found here are routed to
   the validation skills, not papered over.
3. **Demote post-merge validation to verification.** Post-merge smoke/
   health checks CONFIRM the deploy; they gate nothing (there is nothing
   left to gate). A post-merge failure is an INCIDENT-CLASS signal that
   triggers rollback/fix-forward — not a "gate failure" that implies the
   merge could have been stopped.
4. **Record the branch-protection configuration in-repo** (format:
   [references/governance-doc-template.md](references/governance-doc-template.md)):
   protected branch, required checks by name, strictness
   (up-to-date-before-merge and why), review requirements, who may merge —
   AND the ownership rule: **changing branch protection is a named human
   role's act, never an agent's**, with changes recorded as dated diffs to
   this doc. The recorded config is verified against the live config on a
   cadence (drift check), with API-vs-UI source labeled.
5. **State the accepted-risk exposure window:** from merge to verified
   deploy, `<duration>` where `<blast radius>` is exposed if PR validation
   missed something. Name who accepted it and when. An unstated window is
   an unaccepted risk being taken anyway.
6. **Define the rollback primitive: revert-PR-then-auto-redeploy.** The
   revert rides the same authoritative gate (a revert PR with required
   checks) and the platform redeploys on its merge. Mechanics must match
   the merge strategy: **squash-merged changes revert as ordinary commits —
   `git revert <sha>`; the `-m 1` flag applies only to true merge commits**
   (using it on a squash commit fails). Note what revert does NOT undo
   (applied migrations, external side effects) and route the full runbook
   to `rollback-runbook-author`.
7. **Deliver the governance doc + gap list:** the doc into the repo (dated),
   gaps (insufficient required checks, missing verification signals,
   unowned protection) as routed follow-ups.

## Output Format

```
MERGE-IS-DEPLOY GOVERNANCE — <repo> (<dated doc path>)
Reality:            merge to <branch> auto-deploys <what> to <env> (evidence: <platform config>)
                    does NOT auto-deploy: <migrations/etc → operator path>
Authoritative gate: PR-time required checks: <exact names> — pre-production's last line
Post-merge:         verification only (smoke/health <signals>); failure = incident → rollback
Branch protection (recorded <date>, source: <API|human-dictated>):
                    <required checks, strictness, reviews, who may merge>
                    changes: <named human role> only — never agents; dated diffs here
Exposure window:    merge → verified deploy ≈ <duration>; blast radius <scope>;
                    accepted by <who> on <date>
Rollback primitive: revert PR → gate → merge → auto-redeploy
                    (squash repo: git revert <sha>; -m 1 only for true merge commits)
                    does not undo: <migrations/external effects> → rollback-runbook-author
Gaps routed:        <check gaps, signal gaps, ownership gaps → owning skills/humans>
```

## Validation Checklist

- [ ] Merge→deploy verified from platform evidence, not assumed; the
      not-auto-deployed remainder is listed.
- [ ] Required checks named exactly; PR-gate sufficiency gaps routed, not
      ignored.
- [ ] Post-merge checks explicitly reclassified as verification with the
      incident-on-failure consequence stated.
- [ ] Branch protection recorded in-repo with source labeled, drift-check
      cadence set, and the human-only change rule (never agents) explicit.
- [ ] Exposure window stated with duration, blast radius, and a named
      accepter — no silent risk.
- [ ] Revert mechanics match the repo's merge strategy (squash ⇒ ordinary
      `git revert <sha>`); revert's limits stated and runbook routed.
- [ ] This doc changes only via reviewed PRs (it is itself an
      important-path artifact — pairs with `context-co-update-ci-gate`
      where that gate exists).

## Gotchas

- **The phantom deploy step:** teams on auto-deploy platforms keep writing
  process docs with a "deploy" stage no one performs; every gate attached
  to that phantom stage silently doesn't exist. Aligning docs to physics
  is the whole skill.
- **Partial auto-deploy:** commonly the app and serverless functions
  auto-deploy while database migrations do not — merging a PR whose code
  expects an unapplied migration deploys broken code. The
  ordering/ownership of the non-auto part must be in the doc.
- **Protection config drift:** UI-changed protection (a check renamed, a
  requirement dropped) silently rewrites the authoritative gate. The
  in-repo record + cadenced drift check is the countermeasure; reading via
  API needs admin scope — label human-dictated records as such.
- **Squash-revert confusion:** `git revert -m 1 <sha>` on a squash-merged
  commit errors out ("not a merge"); conversely reverting only one commit
  of a true merge without `-m` fails too. Match the mechanics to the
  strategy — a broken revert command in the rollback path is discovered at
  the worst possible time.
- **Revert theater:** a revert PR undoes the code but not the applied
  migration or the external webhook registrations; stating what revert
  does NOT undo is what keeps the primitive honest.
- **Auto-merge interaction:** with merge==deploy, ARMING auto-merge is
  arming auto-DEPLOY — the human-only rule from
  `agent-authorization-matrix` gets sharper teeth here, and armed-state
  checks use the strategy-specific event names.

## Stop Conditions

- Asked to reclassify post-merge validation as the gate ("we'll catch it
  after merge, keep PR checks light") → refuse: on this platform
  post-merge is production; strengthening the PR gate is the only lawful
  direction.
- Asked to change branch protection directly (API or UI) → refuse; the
  skill RECORDS and verifies protection. Changing it is the named human
  role's act — hand over the exact desired config.
- Merge→deploy cannot be verified from platform evidence and the human
  cannot confirm it → stop; governance written against a guessed pipeline
  misgoverns the real one.
- The platform deploys from something OTHER than mainline merges (release
  tags, manual promote) → this skill's premise fails; say so and route to
  `ci-pipeline-architect`/`release-readiness-reviewer` territory instead
  of forcing the pattern.

## Supporting Files

- [references/governance-doc-template.md](references/governance-doc-template.md)
  — the full governance-doc template with the branch-protection record
  format, drift-check cadence, exposure-window wording, and revert
  mechanics per merge strategy.
- `evals/evals.json` — behavior cases incl. partial-auto-deploy and
  refusing to demote the PR gate.
- `evals/trigger-evals.json` — discrimination against
  `release-readiness-reviewer`, `rollback-runbook-author`,
  `agent-authorization-matrix`, and `ci-pipeline-architect`.
