---
name: product-spec-writer
description: 'Write a product specification for a feature — the problem and the user/job it serves, goals and explicit non-goals, scenarios and key flows, functional requirements with TESTABLE acceptance criteria, edge-case behavior, dependencies, rollout intent and success metrics, and open questions. Captures WHAT to build and WHY from the user''s perspective, at a level engineering and design can act on. Distinct from an ADR: a product spec describes a user-facing feature and how we know it is done; an Architecture Decision Record captures ONE technical decision (context → decision → alternatives → consequences → rollback). Use when requirements are understood and need to become a spec, when writing a PRD/feature spec, or when engineering asks "what exactly are we building?". Do NOT use to record a technical/architecture decision and its alternatives (adr-writer), elicit still-unclear requirements (requirements-gathering-facilitator), or plan flag-gated rollout mechanics (feature-flag-rollout-strategist).'
---

# Product Spec Writer

## Purpose

A product spec is the contract between "we agreed on the problem" and
"engineering builds the thing" — and when it's missing, the gap fills
with a dozen private assumptions that only collide at review. This skill
writes that spec: the problem and the user's job, goals and the
explicit non-goals, the scenarios and flows, functional requirements
with acceptance criteria a tester can actually check, edge-case and
error behavior, dependencies, and how success will be measured. It
captures WHAT to build and WHY from the user's perspective, at a level
design and engineering can act on without guessing. It is deliberately
not an ADR: a spec answers "what user-facing thing are we building and
how do we know it's done", whereas an Architecture Decision Record
answers "which technical option did we choose and why" — different
document, different author intent, and the spec routes any such
technical decision to `adr-writer`.

## Use When

- Use when: requirements are understood and need to become a written
  specification (PRD / feature spec) engineering and design can build
  from.
- Use when: engineering asks "what exactly are we building?" or "what
  counts as done?" and there is no crisp answer.
- Use when: a feature needs testable acceptance criteria, explicit
  scope/non-scope, and success metrics before work starts.
- Use when: `requirements-gathering-facilitator` has produced a
  requirements brief and it's time to turn it into a spec.
- Do NOT use when: the artifact needed is an ARCHITECTURE DECISION — a
  specific technical choice, its alternatives, and consequences — that is
  `adr-writer`; a spec may CITE such a decision but does not make or
  record it.
- Do NOT use when: requirements are still unclear, contradictory, or
  solution-first — go back to `requirements-gathering-facilitator`; a
  spec written on sand is confident fiction.
- Do NOT use when: the task is the flag/rollout MECHANICS (progressive
  delivery, targeting, guardrail auto-rollback) — that is
  `feature-flag-rollout-strategist`; the spec states the rollout INTENT
  and success metrics, not the flag plumbing.

## Inputs to Inspect

1. The requirements brief or equivalent (from
   `requirements-gathering-facilitator` if present): the problem, users/
   jobs, non-goals, constraints, and open questions.
2. The users and their context: who this is for and the job they're
   doing — the spec is written from their perspective, not the system's.
3. Existing product surfaces this touches: current flows, related
   features, and conventions the spec must fit or deliberately break.
4. Constraints and dependencies: platform, compliance/legal, other teams'
   work, and any technical decisions already recorded (ADRs) that bound
   the design.
5. How success will be judged: the metric(s) or observable outcomes the
   stakeholders named, and any guardrails (what must NOT get worse).

## Workflow

1. **Verify the ground is solid.** Confirm requirements are actually
   understood. If the problem is vague or stakeholders still disagree,
   stop and route to `requirements-gathering-facilitator` — do not paper
   over ambiguity with confident prose.
2. **State the problem and the why.** Open with the user's problem and
   job-to-be-done, the evidence it's real, and why now. A reader should
   understand the point before any solution appears.
3. **Set goals and non-goals.** Goals stated as outcomes (measurable
   where possible). Non-goals stated as explicitly as goals — the scope
   boundary is half the spec's value and where scope creep is prevented.
4. **Describe users, scenarios, and flows.** The roles/personas
   involved, the key scenarios (happy path plus the important
   alternates), and the primary flows. Use user stories or scenario
   narratives — concrete, not abstract capability lists.
5. **Write functional requirements with acceptance criteria.** Each
   requirement is specific and TESTABLE; pair it with acceptance criteria
   (given/when/then or a checklist) a QA engineer could verify without
   asking you. Vague requirements ("intuitive", "fast") are rewritten as
   observable behavior.
6. **Cover edge cases, errors, and states.** What happens on empty,
   invalid input, permission denied, partial failure. Name the behavior;
   hand the error MODEL to `error-taxonomy-designer` and the UI STATE
   design to `edge-state-ux-designer` rather than re-specifying them.
7. **List dependencies and open questions.** Cross-team, platform, and
   sequencing dependencies; and the open decisions still needed —
   including any technical decision that belongs in an ADR, routed to
   `adr-writer` by name.
8. **Define rollout intent and success.** How it should reach users
   (staged, to whom, gated on what) at the INTENT level, the success
   metrics, and the guardrails. Flag/rollout mechanics are
   `feature-flag-rollout-strategist`'s; the spec says what "success"
   means, not how the flag is wired.
9. **Deliver** the spec in the Output Format, with known/assumed/open
   clearly separated.

The spec template, the acceptance-criteria patterns, and the spec-vs-ADR
discriminator:
[references/product-spec-sheet.md](references/product-spec-sheet.md).

## Output Format

```
PRODUCT SPEC — <feature>
Problem & why:   <user problem, job-to-be-done, evidence, why now>
Goals:           <outcomes, measurable where possible>
Non-goals:       <explicit out-of-scope>
Users/roles:     <who>
Scenarios/flows: <key scenarios: happy + important alternates>
Requirements:    <specific, testable statements>
Acceptance:      <given/when/then or checklist per requirement — QA-verifiable>
Edge/error:      <empty, invalid, forbidden, partial-failure behavior>
                 (error model → error-taxonomy-designer; UI states → edge-state-ux-designer)
Dependencies:    <cross-team / platform / sequencing>
Rollout intent:  <staged? to whom? gated on what?>  (mechanics → feature-flag-rollout-strategist)
Success metrics: <what defines success + guardrails>
Open questions:  <decisions needed; technical ones → adr-writer>
Known / assumed / open separated
```

## Validation Checklist

- [ ] The problem and user job are stated before any solution; a reader
      grasps the "why" first.
- [ ] Goals AND explicit non-goals are present; scope boundary is
      unambiguous.
- [ ] Requirements are specific and testable; each has acceptance
      criteria a QA engineer could verify unaided.
- [ ] Vague qualities ("fast", "intuitive") are rewritten as observable
      behavior.
- [ ] Edge/error/permission behavior is specified, with the error model
      and UI states handed to their owning skills.
- [ ] Success metrics and guardrails are defined; rollout INTENT is
      stated without specifying flag mechanics.
- [ ] Any technical/architecture decision is routed to `adr-writer`, not
      decided inside the spec.
- [ ] Known, assumed, and open items are clearly separated; the spec
      isn't written over unresolved requirements.

## Gotchas

- A spec that opens with the solution and never states the problem lets
  every reader supply their own "why" — and they won't match. Lead with
  the problem.
- "Acceptance criteria" that restate the requirement ("the export works")
  test nothing. Criteria must name observable conditions and outcomes a
  tester can check without you in the room.
- Non-goals feel optional and are the first thing cut; they're what stops
  the feature from doubling in scope by week three. Write them with the
  same care as goals.
- A product spec that starts prescribing database tables, service
  boundaries, or which library to use has drifted into architecture —
  that's an ADR's job. Keep the spec at what-and-why; cite the ADR.
- Success metrics bolted on at the end are usually vanity numbers. Decide
  what would prove the problem is solved, and what must not regress
  (guardrail), while the goals are fresh.
- Writing a confident spec over unresolved requirements doesn't resolve
  them — it hides them until build time. If the brief has blocking open
  questions, they're the spec's open questions too.
- Specifying error copy and empty-state layouts inline duplicates (and
  will drift from) `error-taxonomy-designer` and `edge-state-ux-designer`.
  Name the behavior; delegate the design.

## Stop Conditions

- The needed artifact is an ARCHITECTURE DECISION RECORD — a technical
  choice with alternatives and consequences → route to `adr-writer`; the
  spec cites the decision but does not make it.
- Requirements are still unclear or contested → route back to
  `requirements-gathering-facilitator`; do not write a spec that invents
  agreement.
- The request is the flag/rollout mechanics (progressive %s, targeting,
  guardrail auto-rollback, kill switch) → route to
  `feature-flag-rollout-strategist`; the spec states rollout intent and
  success only.
- A requirement cannot be made testable because the desired outcome
  itself is undefined → surface it as a blocking open question for a human
  rather than shipping an unverifiable requirement.

## Supporting Files

- [references/product-spec-sheet.md](references/product-spec-sheet.md) —
  the full spec template, acceptance-criteria patterns (given/when/then),
  a testable-requirement rewrite guide, and the spec-vs-ADR discriminator
  table.
- `evals/evals.json` — behavior cases including testable acceptance
  criteria, the non-goal discipline, and the route-technical-decision-to-
  ADR case.
- `evals/trigger-evals.json` — discrimination against `adr-writer` (THE
  seam: product spec vs architecture decision), `requirements-gathering-facilitator`,
  and `feature-flag-rollout-strategist`.
