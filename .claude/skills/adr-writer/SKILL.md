---
name: adr-writer
description: Write an Architecture Decision Record for a significant technical choice — context, the decision itself, alternatives genuinely considered, consequences (good and bad), operational impact, a rollback/reversal plan, and a review date. Use when a decision has just been made and needs durable recording, when asked to "write an ADR" or "document why we chose X", or when architecture-designer hands over an ADR draft for completion. Also use to record a rejected option or a superseded decision. Do NOT use to MAKE the decision — open design questions go to architecture-designer; contested facts go to source-of-truth-reconciler first.
---

# ADR Writer

## Purpose

Produce a decision record that lets a future reader — including a future
agent — understand why the system is the way it is, what was rejected and
why, what it costs to operate, and exactly how to back out if the decision's
assumptions fail. The rollback/reversal plan and the review date are
mandatory: a decision with no reversal path is a bet, and one with no review
date silently becomes permanent.

## Use When

- Use when: a significant technical decision was just made (or formally
  proposed) and needs recording — framework choice, boundary placement,
  datastore, build-vs-buy, deprecation.
- Use when: `architecture-designer` hands over an ADR draft to complete.
- Use when: an old decision is being superseded or reversed — that gets its
  own ADR linking both directions.
- Do NOT use when: the decision has not actually been made and options are
  genuinely open — that is `architecture-designer` (or a human conversation).
- Do NOT use when: sources disagree about what was decided — run
  `source-of-truth-reconciler` first; an ADR must not launder a contested
  claim into official history.
- Do NOT use for trivial choices with no architectural consequence — an ADR
  per linting rule buries the decisions that matter.

## Inputs to Inspect

1. The decision statement from the human or the `architecture-designer`
   draft — exactly what was decided, by whom, when.
2. Existing ADRs: numbering scheme, directory (`docs/adr/` or repo
   convention), status vocabulary, and any ADR this one supersedes.
3. The code/config areas the decision touches — enough to describe
   operational impact concretely.
4. The alternatives that were actually on the table, with the real reasons
   they lost (ask if not stated; do not invent).

## Workflow

1. **Locate the ADR home and number.** Follow the repo's existing convention;
   create `docs/adr/` with `NNNN-title.md` naming only if none exists.
2. **State the context:** the forces, constraints, and the problem as it
   stood at decision time — written so it stays true even after the code
   changes. No solution language in the context section.
3. **State the decision** in one or two sentences, active voice ("We will…").
4. **Record alternatives** genuinely considered, each with the actual reason
   it was rejected. "Considered nothing" is a finding to raise, not a section
   to skip.
5. **Record consequences — both signs.** What gets easier, what gets harder,
   what new obligations appear (upgrades, licenses, training, coupling).
6. **Describe operational impact:** deployment, monitoring, on-call surface,
   failure modes, cost profile.
7. **Write the rollback/reversal plan:** the concrete conditions that would
   trigger reversal, the steps to back out, what data or contracts make
   reversal hard, and the point of no return if one exists. "N/A" is not
   acceptable; "reversal is impractical after X because Y" is.
8. **Set status and review date:** status (proposed | accepted | superseded)
   and a specific date to re-examine the decision against its assumptions.
   Link superseded ADRs both ways.
9. **Cross-check:** could a new team member reconstruct the decision's logic
   from this document alone, without hallway context?

## Output Format

A single markdown file following [assets/adr-template.md](assets/adr-template.md):

```
# ADR-NNNN: <title, imperative>
Status: proposed | accepted | superseded by ADR-MMMM
Date: <decision date>   Review by: <specific date>
## Context          <forces and problem, solution-free>
## Decision         <"We will …">
## Alternatives Considered   <option — why rejected>
## Consequences     <positive / negative / new obligations>
## Operational Impact        <deploy, observe, on-call, cost>
## Rollback / Reversal Plan  <trigger conditions, steps, hard parts,
                              point of no return>
```

## Validation Checklist

- [ ] Numbering, location, and status vocabulary match existing repo ADRs.
- [ ] Context section contains no solution language.
- [ ] Every alternative has the real rejection reason, not a strawman.
- [ ] Consequences include at least one genuine negative.
- [ ] Rollback plan has trigger conditions AND steps; impractical reversal is
      explained, never blank.
- [ ] Review date is a specific date, not "later".
- [ ] Superseded ADRs are linked in both directions.

## Gotchas

- ADRs written weeks later reconstruct a tidier story than reality; record
  the messy real reasons — they are the useful ones.
- The most common defect is a consequences section with only upsides; if no
  downside is listed, the alternatives were not taken seriously.
- A rollback plan that says "revert the commit" ignores data written, contracts
  published, and consumers migrated in the meantime — walk the actual state.
- Decision-by-momentum ("we already started using it") is a context fact worth
  recording honestly; hiding it makes the ADR read as more deliberate than it was.
- Do not renumber or rewrite historical ADRs to match new conventions;
  supersede them.

## Stop Conditions

- The "decision" turns out to be contested or unmade → stop; route to
  `architecture-designer` or the human. An ADR must record, not decide.
- Sources disagree on what was decided or why → `source-of-truth-reconciler`
  first.
- The decision crosses a security/data/tenant boundary that was never
  approved → flag via `human-approval-boundary` before recording it as
  accepted.
- No alternatives can be named even after asking → record status "proposed"
  and raise the gap; do not fabricate a comparison.

## Supporting Files

- [assets/adr-template.md](assets/adr-template.md) — the full ADR file
  template with section-by-section guidance comments.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `domain-modeler` and
  `architecture-designer` (design cluster).
