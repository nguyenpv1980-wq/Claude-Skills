---
name: tech-spec-writer
description: 'Write a TECHNICAL SPEC / design doc for a non-trivial engineering effort — broader than an ADR: problem/context, goals and non-goals, the proposed technical design (architecture, data model, APIs, components and how they interact), alternatives considered, cross-cutting concerns (security, privacy, performance, observability, migration/rollout, testing), risks and open questions, and a review/sign-off path. A tech spec covers the WHOLE design of a change (often several decisions); an ADR records ONE decision; a PRODUCT spec is the user-facing what/why. Composes adr-writer for embedded decisions and architecture-designer for structure. Use when writing a design doc/RFC for a substantial change, or when an effort needs design review before build. Do NOT use to record ONE decision (adr-writer), write the user-facing product spec (product-spec-writer), or produce the system structure itself as the deliverable (architecture-designer — the spec presents that).'
---

# Tech Spec Writer

## Purpose

A substantial change built without a technical spec is a change whose
design lives in one person's head and surfaces, contradicted, at code
review. The tech spec is where the design gets written down and agreed
BEFORE the build: the problem and why now, the proposed technical
approach with its data model and interfaces, the alternatives weighed,
the cross-cutting concerns teams forget until production (security,
privacy, performance, observability, migration, testing), the risks, and
the sign-off path. This skill writes that document — broader than an ADR
(which records one decision) and different from a product spec (which is
the user-facing what/why). It composes `adr-writer` for the individual
binding decisions inside it and `architecture-designer` for the structural
work; it presents and integrates them into a reviewable design.

## Use When

- Use when: writing a technical design doc / RFC / design proposal for a
  non-trivial change before implementation.
- Use when: an effort needs design review and sign-off across engineers
  before build starts.
- Use when: a change spans multiple components/decisions and needs a
  single coherent design others can review.
- Use when: cross-cutting concerns (migration, rollout, observability,
  testing) must be designed up front, not discovered late.
- Do NOT use when: the artifact is ONE architecture decision with its
  alternatives and consequences — that is `adr-writer` (a tech spec may
  embed/cite several ADRs).
- Do NOT use when: the artifact is the user-facing PRODUCT spec (problem,
  scope, user stories, acceptance) — that is `product-spec-writer`.
- Do NOT use when: the task is DECIDING the system structure itself
  (component/dependency map, tradeoffs) — that is `architecture-designer`;
  the tech spec presents and consumes that, it doesn't re-derive it.

## Inputs to Inspect

1. The change and its driver: the problem, the product requirement or
   incident behind it, and why now — the spec's opening.
2. The current system: the components, data, and interfaces the change
   touches, inspected (not imagined), so the design is grounded.
3. Existing decisions and structure: relevant ADRs (`adr-sequencer` corpus)
   and any `architecture-designer` output the spec must respect or extend.
4. The requirements: the product spec (`product-spec-writer`) or
   requirements brief the technical design must satisfy.
5. The reviewers and bar: who signs off, and the concerns they'll raise
   (security, data, ops) so the spec addresses them proactively.

## Workflow

1. **Frame problem, goals, non-goals.** Open with the problem and why
   now, the goals (what the design must achieve), and explicit non-goals
   (scope boundary). A spec without non-goals invites scope creep in
   review.
2. **Present the proposed design.** The technical approach: the
   architecture/structure (from `architecture-designer` where it changes),
   the data model, the APIs/interfaces, the key components and how they
   interact — concrete enough to build from, with diagrams where they
   help.
3. **Show the alternatives.** The main options considered and why the
   proposal wins — the reasoning reviewers need. Individual binding
   decisions get recorded as ADRs (`adr-writer`) and cited, not re-argued
   inline.
4. **Design the cross-cutting concerns.** Security and privacy
   (authz, data handling, PII), performance (budgets, hot paths),
   observability (what's logged/metered), migration and rollout
   (staged? reversible?), and testing strategy. These are where specs
   earn their keep — the concerns that bite in production if unplanned.
5. **State risks and open questions.** The real risks with mitigations,
   and the open questions blocking or needing a decision — named, with
   owners, not buried.
6. **Define the review/sign-off path.** Who reviews, what approval means,
   and how the spec becomes the agreed design. A spec nobody signs is a
   suggestion.
7. **Compose, don't duplicate.** Cite ADRs for decisions,
   `architecture-designer` for structure, the product spec for the what/
   why. The tech spec integrates them into one reviewable design; it
   doesn't re-author them.
8. **Deliver** the spec in the Output Format, with known/assumed/open
   separated and cross-cutting concerns explicitly addressed.

The tech-spec template, the cross-cutting-concerns checklist, and the
spec-vs-ADR-vs-product-spec discriminator:
[references/tech-spec-sheet.md](references/tech-spec-sheet.md).

## Output Format

```
TECH SPEC — <effort>
Problem & why now: <context, driver>
Goals / Non-goals: <what the design achieves / explicit out-of-scope>
Proposed design:   architecture (→ architecture-designer if structural), data model, APIs,
                   components + interactions (diagrams where useful)
Alternatives:      <options + why the proposal wins>  (decisions → ADRs, cited)
Cross-cutting:     security/privacy · performance · observability · migration/rollout · testing
Risks & open Qs:   <risks + mitigations; open questions with owners>
Review/sign-off:   <reviewers; what approval means>
Known / assumed / open separated
Boundaries:        one decision → adr-writer; user-facing → product-spec-writer;
                   structure → architecture-designer
```

## Validation Checklist

- [ ] Problem, goals, and explicit non-goals open the spec.
- [ ] The proposed design is concrete (data model, APIs, components/
      interactions) and grounded in the current system.
- [ ] Alternatives are shown with why the proposal wins; binding decisions
      are cited as ADRs, not re-argued.
- [ ] All cross-cutting concerns are addressed: security/privacy,
      performance, observability, migration/rollout, testing.
- [ ] Risks have mitigations; open questions have owners.
- [ ] A review/sign-off path is defined.
- [ ] Structure, single-decision, and product-spec content are composed
      from their owning skills, not duplicated.
- [ ] Known/assumed/open are separated; the spec isn't confident fiction
      over unresolved design.

## Gotchas

- A tech spec with no non-goals expands in review until it's a re-
  architecture; the boundary is half the document's value.
- The concerns that sink projects — migration, rollout, observability,
  data privacy — are exactly the ones specs skip because they're not the
  "fun" design. Design them up front or debug them in production.
- Re-arguing a decision inline that belongs in an ADR bloats the spec and
  loses the record; cite the ADR (`adr-writer`) and move on.
- A design doc that presents only the chosen approach, with no
  alternatives, gives reviewers nothing to push on and hides the
  reasoning. Show the roads not taken.
- A spec nobody is required to sign off is a suggestion that gets ignored
  the first time it's inconvenient. Name the reviewers and what approval
  means.
- Writing the technical design over an unclear product requirement builds
  the right thing wrong; if the what/why is fuzzy, that's
  `product-spec-writer`/`requirements-gathering-facilitator` first.
- A tech spec is not the architecture decision. If you're deriving the
  component/dependency structure from scratch, that's
  `architecture-designer`; the spec presents its result.

## Stop Conditions

- The artifact is ONE architecture decision (context/decision/
  alternatives/consequences/rollback) → route to `adr-writer`.
- The artifact is the user-facing product spec → route to
  `product-spec-writer`.
- The task is deciding the system STRUCTURE itself → route to
  `architecture-designer`; the spec consumes that output.
- The product requirement the design must satisfy is unclear or contested
  → route to `product-spec-writer` / `requirements-gathering-facilitator`
  before designing; a technical spec can't rescue an undefined goal.

## Supporting Files

- [references/tech-spec-sheet.md](references/tech-spec-sheet.md) — the
  tech-spec template, the cross-cutting-concerns checklist, and the
  spec-vs-ADR-vs-product-spec discriminator.
- `evals/evals.json` — behavior cases including the cross-cutting design,
  the cite-don't-re-argue-ADR discipline, and the fuzzy-requirement
  refusal.
- `evals/trigger-evals.json` — discrimination against `adr-writer` (one
  decision), `product-spec-writer` (user-facing), and `architecture-designer`
  (structure).
