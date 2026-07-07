---
name: architecture-designer
description: Design or redesign system structure — components, dependencies, data ownership, integration points — grounded in an inspection of the CURRENT architecture first, never from an imagined one. Produces a component map, dependency map, coupling/cohesion risk list, data-ownership map, tradeoff analysis, an ADR draft for the key decision, and an incremental migration plan from current to target state. Use when asked how a system or feature should be structured, whether something should be a module or a service, where a new integration belongs, or when a proposed change has structural consequences. Do NOT use for pure domain-concept modeling (domain-modeler) or for recording an already-made decision (adr-writer).
---

# Architecture Designer

## Purpose

Produce a target architecture that is reachable from the real current one.
The deliverable is a set of maps (components, dependencies, data ownership),
named risks, an explicit tradeoff analysis, an ADR draft for the pivotal
decision, and a migration plan in reviewable increments. Designing from the
actual codebase — not from how the README says it works — is the core
discipline; the most expensive architecture documents are the ones describing
a system that does not exist.

## Use When

- Use when: asked "how should we structure X" — a new feature with structural
  weight, a subsystem redesign, a monolith/module/service question.
- Use when: a new integration or dependency needs a home and a boundary.
- Use when: a proposed change would alter who owns data or which direction
  dependencies point.
- Do NOT use when: the business concepts themselves are unclear — run
  `domain-modeler` first; structure follows meaning.
- Do NOT use when: the decision is already made and needs recording — that is
  `adr-writer` (this skill hands its ADR draft there).
- Do NOT use when: judging an existing design without proposing one — delegate
  to the `principal-architecture-reviewer` subagent.

## Inputs to Inspect

1. The actual code layout: top-level modules/packages, entry points, and the
   import/reference graph between them (sampled, not assumed).
2. Build and deploy artifacts: what actually ships together (workspaces,
   Dockerfiles, CI jobs) — deployment units are architecture facts.
3. Schema and data access: which modules read/write which tables or stores.
4. Existing ADRs, architecture docs, and diagrams — as claims to verify
   against the code, not as ground truth.
5. The domain model, if one exists; run `domain-modeler` first if core
   concepts are undefined.
6. Nonfunctional constraints stated by the human: scale, latency, team split,
   compliance, budget.

## Workflow

1. **Inspect current state first.** Map the real components, their
   dependencies (including direction), and data ownership from code and
   config. Where docs contradict code, record the drift as a finding.
2. **State the forces.** What is this design being asked to optimize —
   change isolation, team autonomy, latency, cost, operability? Rank them;
   an unranked list decides nothing.
3. **Draft the target component map:** components, responsibilities, allowed
   dependency directions, and the contract at each boundary (sync call,
   event, shared table — be honest about the last one).
4. **Assign data ownership:** every store/table gets exactly one owning
   component; readers go through its contract. Flag shared-write tables as
   the risks they are.
5. **Name coupling and cohesion risks** in the target: cycles, god
   components, chatty boundaries, distributed transactions, hidden coupling
   through the database.
6. **Run the tradeoff analysis:** at least two viable options compared across
   complexity, delivery speed, operability, cost, reversibility, and failure
   modes. Recommend one; say what would change the recommendation.
7. **Draft the ADR** for the pivotal decision (context, decision,
   alternatives, consequences) — hand to `adr-writer` for completion with
   rollback plan and review date.
8. **Write the migration plan:** ordered, individually shippable increments
   from current to target, each with a verification step and a stop point.
   "Big-bang rewrite" is not a migration plan.

## Output Format

```
ARCHITECTURE DESIGN — <scope>
Current state (inspected): components, dependencies, data ownership;
  drift found between docs and code
Forces (ranked): <what this design optimizes, in order>
Target component map: <component — responsibility — allowed deps — boundary contract>
Data ownership map: <store/table → owning component; flagged shared writes>
Coupling/cohesion risks: <each with consequence>
Options considered: <A vs B (vs C) across complexity, speed, operability,
  cost, reversibility, failure modes>
Recommendation: <option + what would change it>
ADR draft: <context, decision, alternatives, consequences> → adr-writer
Migration plan: <increment → verification → stop point>, order matters
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Current-state map cites real files/modules inspected — not reconstructed
      from docs or memory.
- [ ] Doc-vs-code drift, if found, is listed as a finding.
- [ ] Every target boundary names its contract type; shared-database coupling
      is declared, not hidden.
- [ ] Every data store has exactly one owner in the target map.
- [ ] At least two options genuinely compared; the recommendation names its
      reversal condition.
- [ ] Migration plan increments are individually shippable and verifiable.
- [ ] No implementation performed — this skill designs; it does not restructure
      code.

## Gotchas

- The README architecture and the import graph disagree more often than not;
  the import graph is the one running in production.
- "Extract a service" answers a team/deployment problem, not a code-quality
  problem — check which one the human actually has.
- Two components sharing write access to one table are one component with
  extra steps; no diagram fixes that until ownership is assigned.
- Designing for imagined scale adds real complexity for hypothetical load;
  tie every scale-driven choice to a stated number.
- A migration plan whose first increment is "refactor everything" will never
  ship increment two.

## Stop Conditions

- Core domain concepts are undefined or contested → stop; run
  `domain-modeler` (or `source-of-truth-reconciler` if sources conflict).
- The design would change security, tenant-isolation, or data-handling
  posture → surface via `human-approval-boundary` before recommending.
- Constraints are missing that would flip the recommendation (team size,
  latency budget, compliance) → ask; do not pick a default silently.
- The human asks to implement the design in the same pass → the migration
  plan's increment 1 becomes a separate, scoped task; confirm before touching
  code.

## Supporting Files

- [references/architecture-artifacts.md](references/architecture-artifacts.md) —
  quality bars for each map, contract-type catalog, tradeoff table template,
  and migration-increment patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `domain-modeler` and
  `adr-writer` (design cluster).
