---
name: ai-sdlc-operating-model
description: Define the end-to-end operating model for AI-assisted software work — the named stages (context, classify, plan, implement, validate, review, merge, close, learn), the authority holder at each (human, agent, or agent-with-approval), each stage's entry/exit gate, and its enforcing discipline skill — composing the Phase 1 pack plus agent-authorization-matrix, agent-memory-governance, and agent-governance-audit into one contract. Use when asked how humans and AI agents should plan, build, review, merge, and close work together, when adopting agents on a team or repo, when agent work is undisciplined (skipped review, surprise merges, missing evidence), or when writing or overhauling an AI-SDLC policy. Produces the operating-model document and a gap list against observed practice. Do NOT use to enforce a single stage in-flight (the stage skills own that), define standing agent permissions (agent-authorization-matrix), or audit one change's compliance (agent-governance-audit).
---

# AI-Era SDLC Operating Model

## Purpose

Turn ad-hoc human+agent collaboration into one named, auditable contract: which
stages software work moves through, who holds authority at each stage, what gate
must pass before the next stage, and which execution-discipline skill enforces
it. This is the umbrella over the Phase 1 pack — it COMPOSES those skills into a
lifecycle (each stage cites its enforcing skill) rather than restating their
procedures, and it is grounded in how work in the repo actually flows, observed
from PR history, not in an imagined team.

## Use When

- Use when: asked how humans and AI agents should work together end to end —
  plan, implement, validate, review, merge, close.
- Use when: adopting AI agents on a team or repo, or scaling from one agent to
  parallel sessions, and the workflow needs a defined shape.
- Use when: agent-assisted work shows discipline failures — skipped review,
  surprise merges, missing evidence, silent scope drift — and the fix is a
  defined operating model rather than one more incident patch.
- Use when: writing or overhauling an AI-SDLC / agent-workflow policy document.
- Do NOT use when: one stage needs enforcing in-flight — startup belongs to
  `agent-startup-context-gate`, scope to `change-classification-gate`, risky
  actions to `human-approval-boundary`, diffs to `reviewable-diff-discipline`,
  closeout to `ai-closeout-reporter`.
- Do NOT use when: the question is what an agent MAY do without approval —
  that standing policy is `agent-authorization-matrix` (this model cites it).
- Do NOT use when: judging whether a finished change followed the process —
  that is `agent-governance-audit`.

## Inputs to Inspect

1. Observed practice: the last 10–20 PRs — who opened, who reviewed, who
   merged, what evidence shipped, where auto-merge appeared (`gh pr list`,
   `gh pr view --json author,reviews,mergedBy,autoMergeRequest`).
2. Agent instruction files (`CLAUDE.md`, `AGENTS.md`, tool rules) and any
   existing workflow/policy docs — what the team CLAIMS the process is.
3. Branch protection and CI gates: required checks, review requirements,
   who can merge (`gh api repos/{owner}/{repo}/branches/<default>/protection`).
4. The installed skill inventory (`.claude/skills/`) — which stage enforcers
   already exist and can be composed rather than invented.
5. The standing `agent-authorization-matrix` and memory policy
   (`agent-memory-governance`) if present; their absence is a gap to record.
6. Incident history: past discipline failures and what each one bypassed.

## Workflow

1. **Inspect current practice first.** Reconstruct how the last N changes
   actually flowed from PR/commit history. Design from observed reality;
   claimed process that contradicts observed process is a finding.
2. **Name the stages.** Default: context → classify → plan/approve →
   implement → validate → review → merge → close → learn. Add or collapse
   stages only with a reason tied to this repo's work.
3. **Assign each stage its contract** — a row in the stage-gate map
   ([references/stage-gate-map.md](references/stage-gate-map.md)): entry
   condition, exit gate, authority holder (human | agent | agent-with-approval),
   the enforcing skill (cited by name, its body never restated), and the
   evidence the stage must leave behind.
4. **Define the authority summary.** Merge and deploy authority always resolves
   through `agent-authorization-matrix`; if no matrix exists, record the gap
   and the interim rule (agents open PRs and stop — a human merges).
5. **Define failure and escalation paths:** broken mid-task state routes to
   `agent-failure-recovery`; conflicting sources to `source-of-truth-reconciler`;
   unclear security impact to `human-approval-boundary`. Parallel-session
   hazards (shared worktrees, stale memory) get explicit rules.
6. **Define the learning loop:** closeouts feed memory under
   `agent-memory-governance` rules; `agent-governance-audit` spot-checks
   compliance on a stated cadence; audit findings feed model revisions.
7. **Gap analysis.** Model vs observed practice: each gap with severity, the
   observed evidence (PR number, incident), and the control that closes it.
8. **Deliver the operating-model document** with an incremental adoption
   sequence — highest-severity gaps first, never everything at once — and a
   review date.

## Output Format

```
AI-SDLC OPERATING MODEL
Scope:        <repo / team / fleet>
Grounding:    <N PRs + docs inspected, with identifiers>
Stages:       <stage → entry, exit gate, authority, enforcing skill, evidence>
Authority:    <summary; merge/deploy defer to agent-authorization-matrix or gap>
Failure paths:<failure class → route>
Learning loop:<memory rules ref, audit cadence>
Gaps:         <gap → severity → observed evidence → closing control>
Adoption:     <ordered steps, one gap-cluster at a time>
Review date:  <date>
```

## Validation Checklist

- [ ] Every stage has an entry condition, exit gate, authority holder,
      enforcing skill, and required evidence — no blank cells.
- [ ] No composed skill's procedure is restated — each is cited by name so the
      model cannot drift from the skill contracts.
- [ ] Merge/deploy authority defers to `agent-authorization-matrix` or the gap
      is recorded with an interim open-PR-and-stop rule.
- [ ] Gap list cites observed evidence (PR numbers, incidents), not vibes.
- [ ] Adoption plan is incremental with a review date.
- [ ] Model grounded in inspected practice, not an imagined team.

## Gotchas

- Restating skill bodies inside the model creates two copies that drift; the
  model composes by reference — that is the difference between an umbrella and
  a duplicate.
- The claimed process and the observed process usually differ; modeling only
  the claimed one produces a document nobody follows.
- Merge authority is where models go vague and incidents live — "the team
  merges after review" does not say WHO may press the button or arm auto-merge.
- Over-gating is a failure mode: a model that requires approval for everything
  gets bypassed, and then protects nothing.
- The model is versioned policy, not scripture — without a review date and a
  feedback loop from `agent-governance-audit`, it fossilizes.
- CI green is a validation signal inside a stage, not a substitute for the
  review and merge-authority gates.

## Stop Conditions

- Asked to remove or weaken a human authority point (merge, deploy, prod data)
  as part of "streamlining" → stop; that decision routes through
  `human-approval-boundary` and must be recorded in the matrix, not slipped
  into a workflow doc.
- Existing policy docs contradict each other about the current process →
  `source-of-truth-reconciler` first; model against the reconciled truth.
- Observed practice cannot be inspected (no PR history access) → say so and
  mark the model as ungrounded-draft rather than inventing observations.

## Supporting Files

- [references/stage-gate-map.md](references/stage-gate-map.md) — the full
  stage × gate × authority × enforcing-skill composition table with per-stage
  evidence requirements and adoption notes.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against
  `agent-authorization-matrix`, `agent-governance-audit`,
  `agent-memory-governance`, and the Phase 1 stage skills.
