---
name: phased-work-handoff-designer
description: 'Design the handoff artifact/protocol for MULTI-STAGE sequenced work where each stage carries its binding decisions forward as evidence — so a later stage (or a fresh agent/session) continues without re-deriving or contradicting what was decided. The discipline: a decision-ID register carried across stages (each decision''s ID, whether it still binds), per-stage changed-files AND NOT-touched lists, proven-invocation sections with tell-tale output (evidence the stage did what it claims), and deviation flags for departures from the plan. Reports across STAGES of one effort — distinct from ai-closeout-reporter (reports ONE turn) and ai-sdlc-operating-model (frames the whole lifecycle). Use when designing handoffs for staged/sequenced work, multi-session efforts, or agent-to-agent continuation. Do NOT use to report a single turn/task (ai-closeout-reporter), define the SDLC operating model/authority (ai-sdlc-operating-model), or guide parallel lanes at work''s start (lane-authoring-guide).'
---

# Phased Work Handoff Designer

## Purpose

Multi-stage work breaks at the seams between stages: stage 3 re-derives a
decision stage 1 already made (differently), a later session "cleans up" a
file stage 2 deliberately left alone, and a stage claims "tests pass" with
no evidence it ran anything. The handoff is where continuity lives or
dies. This skill designs the handoff artifact and protocol for sequenced
work so each stage carries its binding decisions forward as EVIDENCE — a
decision-ID register that later stages honor, explicit changed-files and
NOT-touched lists, proven-invocation sections with the tell-tale output
that shows a stage actually ran what it claims, and deviation flags where a
stage departed from the plan. It reports across STAGES of one effort — not
a single turn (that's `ai-closeout-reporter`) and not the lifecycle model
itself (`ai-sdlc-operating-model`).

## Use When

- Use when: designing handoffs for staged/sequenced work where each stage's
  decisions must carry forward to the next.
- Use when: work spans multiple sessions or agents and continuity depends
  on a trustworthy handoff (no re-derivation, no contradiction, no silent
  drift).
- Use when: agent-to-agent or session-to-session continuation needs a
  contract for what carries forward and what evidence proves each stage.
- Use when: staged work keeps losing decisions, touching files a prior
  stage intentionally left, or claiming steps without evidence.
- Do NOT use when: the task is reporting ONE turn/task's outcome (what
  changed, tests run, next step) — that is `ai-closeout-reporter`; this
  designs the CROSS-STAGE carry-forward.
- Do NOT use when: the task is defining the end-to-end SDLC operating model
  — the stages, authority holders, and gates for AI-assisted work — that is
  `ai-sdlc-operating-model`; this designs the handoff artifact within it.
- Do NOT use when: the task is a pre-work guide for PARALLEL lanes at the
  start of work — that is `lane-authoring-guide`; this is for SEQUENTIAL
  stages carrying decisions forward.

## Inputs to Inspect

1. The phased effort: the stages, their sequence, and the dependency of
   each stage on prior stages' decisions and outputs.
2. The binding decisions: what each stage decides that later stages must
   honor (interfaces, conventions, scope boundaries, chosen approaches).
3. The evidence the work produces: the commands/validations each stage
   runs, and what tell-tale output proves they ran.
4. The failure history: where prior staged work lost decisions, touched
   what it shouldn't, or claimed unproven steps — the concrete gaps to
   close.
5. The continuation context: who/what picks up the next stage (a later
   session, a different agent) and what they need to continue cold.

## Workflow

1. **Design the decision-ID register.** Every binding decision gets a
   stable ID and a one-line statement. The register is carried across
   stages; each stage declares which prior decisions still bind (and are
   honored) and which it changes — a changed decision is a DEVIATION, not a
   silent overwrite. This is what stops stage N from contradicting stage 1.
2. **Require per-stage changed-files AND not-touched lists.** Each stage
   records what it changed and, explicitly, what it deliberately did NOT
   touch. The not-touched list is the anti-cleanup guard: it tells the next
   stage the untouched surface is intentional, not forgotten, so nobody
   "helpfully" undoes a prior stage's restraint.
3. **Require proven-invocation sections.** A stage doesn't say "tests
   pass"; it shows the command it ran and the tell-tale output proving it
   ran (counts, IDs, timestamps, the distinctive line). Claims without
   evidence are the crack fabrication slips through; the handoff demands
   the receipt.
4. **Design deviation flags.** Where a stage departed from the plan or from
   a prior decision, it flags the deviation explicitly with rationale.
   Visible deviation is correctable; silent drift compounds across stages
   into an effort nobody can trust.
5. **Define the continuation contract.** What a later stage / fresh agent
   needs to pick up cold: the current register, the evidence, the
   changed/not-touched state, the open items, and the next stage's entry
   criteria. Continuation should require reading the handoff, not
   re-deriving the effort.
6. **Keep it verifiable, not narrative.** The handoff is evidence, not a
   story — a reader (human or agent) can check each claim against its
   proof. Cross-reference the register so a decision is traceable to the
   stage that made it.
7. **Deliver** the handoff protocol/template in the Output Format, with the
   register, per-stage evidence structure, and continuation contract.

The handoff template, the decision-ID register format, the proven-
invocation pattern, and the not-touched/deviation conventions:
[references/handoff-sheet.md](references/handoff-sheet.md).

## Output Format

```
PHASED-WORK HANDOFF PROTOCOL — <effort>
Decision-ID register (carried across stages):
  <D-id | decision | made in stage | still binding? | superseded-by (deviation)>
Per stage:
  Changed files: <list>   NOT touched (intentional): <list>
  Proven invocation: <command> → <tell-tale output proving it ran>
  Deviations: <departed from plan/decision — rationale, flagged>
  Open items → next stage
Continuation contract: what a fresh stage/agent needs to pick up cold (register + evidence + entry criteria)
Verifiable: every claim has its proof; decisions traceable to their stage
Boundaries: one turn → ai-closeout-reporter; lifecycle model → ai-sdlc-operating-model;
            parallel lanes → lane-authoring-guide
```

## Validation Checklist

- [ ] A decision-ID register carries binding decisions across stages; each
      stage declares which still bind.
- [ ] Each stage lists changed files AND an explicit NOT-touched list.
- [ ] Each stage's claims have proven-invocation evidence (command +
      tell-tale output), not bare assertions.
- [ ] Deviations from the plan or prior decisions are flagged with
      rationale, not silent.
- [ ] A continuation contract lets a fresh stage/agent pick up cold from
      the handoff without re-deriving.
- [ ] The handoff is verifiable evidence, not narrative; decisions are
      traceable to their stage.
- [ ] Single-turn reporting, the SDLC operating model, and parallel-lane
      guidance are handed to their owning skills.

## Gotchas

- The decision that isn't carried forward gets re-made — differently — by
  a later stage, and now the effort contradicts itself. The register is
  the single mechanism that prevents this; without it, staged work drifts.
- A missing NOT-touched list invites the "helpful cleanup" that undoes a
  prior stage's deliberate restraint. Silence reads as "forgotten"; the
  explicit list reads as "intentional".
- "Tests pass" with no evidence is where fabrication hides — a later stage
  builds on a claim that was never true. Demand the command and its
  tell-tale output; the receipt, not the assertion.
- Silent deviation is the expensive kind: a stage quietly departs from the
  plan, later stages assume the plan held, and the mismatch surfaces at the
  end. Flag deviations so they're correctable in-flight.
- A handoff written as narrative ("we did a bunch of stuff, looks good")
  can't be verified and can't be continued from cold. Structure it as
  checkable evidence.
- This is not a single-turn closeout. If you're reporting one PR/task's
  outcome, that's `ai-closeout-reporter`; this carries a decision register
  and evidence across MANY stages.
- This is not the operating model. Defining the stages, authorities, and
  gates of the whole lifecycle is `ai-sdlc-operating-model`; this designs
  the handoff that rides between stages.

## Stop Conditions

- The task is reporting a single turn/task's outcome → route to
  `ai-closeout-reporter`.
- The task is defining the SDLC operating model (stages, authority, gates)
  → route to `ai-sdlc-operating-model`.
- The task is a pre-work guide for parallel lanes → route to
  `lane-authoring-guide`.
- A stage's claimed step can't be backed by proven-invocation evidence →
  flag the unproven claim in the handoff rather than carrying it forward as
  fact; an unverifiable claim must not become a later stage's foundation.

## Supporting Files

- [references/handoff-sheet.md](references/handoff-sheet.md) — the handoff
  template, the decision-ID register format, the proven-invocation pattern,
  and the not-touched/deviation-flag conventions.
- `evals/evals.json` — behavior cases including the decision-register
  carry-forward, the not-touched guard, and the proven-invocation
  requirement.
- `evals/trigger-evals.json` — discrimination against `ai-closeout-reporter`
  (one turn), `ai-sdlc-operating-model` (lifecycle), and
  `lane-authoring-guide` (parallel lanes).
