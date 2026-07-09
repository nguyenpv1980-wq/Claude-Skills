---
name: lane-authoring-guide
description: Author the pre-work, evidence-cited guide a parallel agent lane needs BEFORE its first task: the lane's slice of the request lifecycle, the contracts it may rely on and must honor, a step-by-step recipe for its repeating unit of work, a per-unit checklist, and an explicit "what this lane must NOT do" boundary — every load-bearing claim cited to source files/PRs or labeled unverified, so the implementing agent starts from distilled verified knowledge instead of re-deriving it. One guide per lane; boundaries mutually exclusive; shared surfaces get a named owner. Planner-to-implementer transfer at work's BEGINNING. Use when splitting an effort across parallel agents/lanes, before a lane's first unit, or when parallel agents collide on shared files. Do NOT use for the end-of-work report/handoff (ai-closeout-reporter — work's END), the whole-lifecycle contract (ai-sdlc-operating-model), aligning tool instruction files (agent-instruction-consolidator), or recording lane approvals (scoped-approval-register).
---

# Lane Authoring Guide

## Purpose

Give each parallel lane its knowledge before its work starts. When an effort
splits across parallel agents — backend read handlers in one lane, frontend
in another, AI routing in a third — each implementing agent either receives
distilled, verified knowledge of its lane, or spends its first hours
re-deriving that knowledge from source (differently from its neighbors, and
sometimes wrongly). The evidence pattern (Repo B of the extraction report ran
three parallel lanes, each with a pre-work authoring guide plus an
implementation contract) is planner-to-implementer transfer at work's
BEGINNING: an evidence-cited guide per lane covering lifecycle, contracts,
recipe, checklist, and — critically — the explicit boundary of what this lane
must NOT touch. The negative boundary is what makes parallelism safe.

## Use When

- Use when: splitting an effort across parallel agents/lanes and each lane
  needs its authoring guide before its first task.
- Use when: onboarding an agent (or a new session) to a specialized surface
  it will work repeatedly — the lane's unit of work recurs.
- Use when: parallel agents keep colliding on shared files or re-deriving
  the same architecture facts inconsistently.
- Use when: a lane guide exists but its claims are uncited — retrofit the
  evidence discipline.
- Do NOT use when: a stage or task is FINISHING and the next agent needs
  what-happened — that is a handoff/closeout (`ai-closeout-reporter`); this
  guide is authored before the lane's work begins.
- Do NOT use when: defining the whole team's lifecycle stages and authority
  — that is `ai-sdlc-operating-model`; a lane guide operates inside that
  contract for one lane's surface.
- Do NOT use when: aligning tool-instruction files (CLAUDE.md, AGENTS.md,
  Cursor rules) across tools — that is `agent-instruction-consolidator`; a
  lane guide is per-EFFORT knowledge, not standing tool instructions.
- Do NOT use when: recording what the lane is authorized to do — approvals
  and their scopes live in `scoped-approval-register`; the guide CITES them.

## Inputs to Inspect

1. The split itself: the lanes, their intended surfaces, and the plan of
   record that approved the split (phases, scope).
2. The source of the knowledge being distilled: the actual request
   lifecycle in code (entry points, handlers, data flow), the contracts the
   lane consumes/provides (API shapes, events, schemas), conventions and
   utilities the lane must reuse. Every claim in the guide traces here.
3. The neighboring lanes' surfaces — the boundary section is written
   against THEM; mutual exclusivity has to be checked, not assumed.
4. Any implementation contract shared by all lanes (interfaces frozen
   between lanes) — the guide cites it rather than restating it.
5. Approvals/authority in force (`scoped-approval-register`,
   `agent-authorization-matrix`) so the guide's recipe never instructs past
   what the lane may do.

## Workflow

1. **Fix the lane's identity:** name, surface (paths/modules), its repeating
   UNIT of work (e.g. "one read handler", "one route + component pair"), and
   which plan/phase approved it.
2. **Distill the request lifecycle for THIS lane** — from entry to exit as
   the code actually implements it, each hop cited (file:line or file+symbol).
   Uncitable lifecycle claims are labeled `unverified` or omitted; a guide
   with confident-but-wrong lifecycle is worse than none.
3. **Write the contracts section:** what the lane MAY RELY ON (interfaces,
   schemas, invariants frozen by the shared contract — cited) and what it
   MUST HONOR (what other lanes rely on from it). Changes to a shared
   contract are out-of-lane by definition and route to the coordinator.
4. **Write the step-by-step recipe** for one unit of work — ordered,
   concrete, referencing real utilities/conventions, from "read this first"
   to "definition of done for the unit". Include the validation the unit
   must pass (compose `risk-tiered-validation-selector` /
   `local-ci-mirror-preflight` where those disciplines exist).
5. **Write the per-unit checklist** — the short list the agent runs per unit
   (contract honored, tests, conventions, no out-of-lane files touched,
   evidence captured).
6. **Write the boundary: "what this lane must NOT do."** Explicit negatives:
   files/dirs not to touch, decisions not to make (schema, shared contracts,
   other lanes' surfaces), escalation path when the unit seems to require
   crossing. Check mutual exclusivity against the other lanes' guides; a
   shared surface gets a NAMED owner or a coordination rule, never dual
   ownership by silence.
7. **Cite or flag everything load-bearing.** Full guide template with the
   evidence-citation convention:
   [references/lane-guide-template.md](references/lane-guide-template.md).
8. **Deliver one guide per lane** into the repo's docs (dated), linked from
   the plan of record; the lane's first task starts by reading it.

## Output Format

```
LANE AUTHORING GUIDE — <lane name> (<dated doc path>)
Lane identity:    <surface paths/modules; repeating unit of work; approving plan/phase>
Request lifecycle: <entry → … → exit, each hop cited file:line / file+symbol>
Contracts:        may-rely-on: <cited> | must-honor: <cited> | changes route to <coordinator>
Recipe (per unit): <ordered steps with real utilities/conventions + unit definition-of-done>
Per-unit checklist: <short runnable list>
MUST NOT:         <explicit files/dirs/decisions out of lane + escalation path>
Evidence:         every load-bearing claim cited or labeled unverified
```

## Validation Checklist

- [ ] The lane's unit of work is named and the recipe walks exactly one
      unit end-to-end.
- [ ] Every lifecycle and contract claim carries a citation (file:line,
      file+symbol, or PR) or an explicit `unverified` label — no confident
      uncited claims.
- [ ] The MUST-NOT section names real files/dirs/decisions and an
      escalation path — not generic "stay in scope" advice.
- [ ] Lane boundaries checked against sibling lanes: mutually exclusive, or
      shared surfaces have a named owner/coordination rule.
- [ ] The guide cites the shared implementation contract instead of
      restating it (one source of truth for inter-lane interfaces).
- [ ] The guide is dated, committed, and linked from the plan of record.
- [ ] Nothing in the recipe instructs beyond the lane's recorded authority.

## Gotchas

- **The guide that's really a wish:** lifecycle described as the planner
  ASSUMES it works, uncited. The implementing agent then builds on a wrong
  map with the planner's confidence. Citation discipline is the antidote.
- **Boundary by omission:** listing what the lane does and assuming the
  complement is forbidden. Agents don't infer complements; the MUST-NOT
  list must be explicit.
- **Dual ownership by silence:** two lanes' guides each quietly claim the
  same shared file (types, router registry, fixtures). Check exclusivity
  across guides at authoring time — this is where parallel-agent collisions
  are actually prevented.
- **Restating the shared contract** in each guide: three copies drift; the
  guides must cite the single contract doc.
- **Guide rot across stages:** a guide written for stage 1 silently wrong
  by stage 3. Re-verify citations when a new stage starts, or mark the
  guide's valid-as-of baseline (date + SHA).
- **Swallowing the closeout's job:** the guide is pre-work; recording what
  a stage actually did, deviations included, is the closeout/handoff at
  work's end — keep the two documents distinct.

## Stop Conditions

- The lane split itself is undecided (which lanes, which surfaces) — stop;
  that is a planning decision for the human/`ai-sdlc-operating-model`
  conversation, and guides authored against a guessed split entrench the
  guess.
- Lifecycle or contract facts cannot be verified from source and the guide
  would be mostly `unverified` labels — stop and say so; distillation needs
  something verified to distill.
- Two lanes' surfaces overlap and no owner can be named for the shared
  piece — surface the conflict to the human; do not author both guides
  around an unowned collision zone.
- Asked to author the guide WITHOUT the MUST-NOT boundary ("the agent will
  figure it out") — refuse; the negative boundary is the load-bearing part
  of a lane guide in a parallel effort.

## Supporting Files

- [references/lane-guide-template.md](references/lane-guide-template.md) —
  the full guide template with section-by-section authoring notes, the
  citation convention, and a worked three-lane boundary example.
- `evals/evals.json` — behavior cases incl. refusing to omit the MUST-NOT
  boundary and labeling uncitable claims.
- `evals/trigger-evals.json` — discrimination against `ai-closeout-reporter`,
  `ai-sdlc-operating-model`, `agent-instruction-consolidator`, and
  `scoped-approval-register`.
