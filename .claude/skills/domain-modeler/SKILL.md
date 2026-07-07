---
name: domain-modeler
description: Model the business domain before any implementation — extract ubiquitous language, actors, workflows, subdomains, bounded contexts, entities, value objects, aggregates, domain services, domain events, and context relationships from requirements, docs, and existing code. Use when starting a new feature or system from prose requirements, when no domain model exists, when naming or entity confusion keeps causing rework, or when asked to map business concepts. Ends at a hard "do not code yet" gate — it produces the model, assumptions, and open questions, and implements nothing unless implementation is explicitly requested after the model is reviewed.
---

# Domain Modeler

## Purpose

Turn prose requirements and scattered code into an explicit domain model the
team can argue with: one shared vocabulary, named actors and workflows,
subdomains and bounded contexts with relationships, and the entity/value-object/
aggregate structure inside each context. The deliverable is the model plus its
assumptions and open questions — not code. A reviewed model prevents the
expensive failure mode of encoding a misunderstanding into schemas and APIs.

## Use When

- Use when: starting a new feature, module, or system and the requirements are
  prose, tickets, or a conversation — no model exists yet.
- Use when: the same business concept has three names across the codebase and
  rework keeps tracing back to entity confusion.
- Use when: asked to "model the domain," "map the business concepts," or
  identify entities/aggregates before schema design.
- Do NOT use when: the domain model already exists and the question is how to
  structure components and dependencies — that is `architecture-designer`.
- Do NOT use when: a decision between known options needs recording — that is
  `adr-writer`.
- Do NOT use when: the task is implementing against an already-agreed model —
  go straight to `docs-first-implementer` or `tdd-engineer`.

## Inputs to Inspect

1. The requirements source: user request, tickets, specs, PRDs — quote the
   phrases the business actually uses; they seed the ubiquitous language.
2. Existing code touching the same concepts: entity/model/table names, enums,
   status fields, service names — the de-facto model already embedded.
3. Existing schema and migrations: current entities, keys, and relationships.
4. Prior domain docs, glossaries, or ADRs, if any.
5. Tests: assertions often encode business rules nobody wrote down elsewhere.

## Workflow

1. **Extract the ubiquitous language.** List every business noun and verb from
   the inputs. Where two terms mean one thing (or one term means two), record
   the collision and pick one canonical term per concept, noting the aliases.
2. **Name actors and workflows.** Who initiates what, and what sequence of
   state changes follows? Write each workflow as trigger → steps → outcome.
3. **Identify subdomains** and classify each: core (differentiating), 
   supporting, or generic (buy/adopt, don't hand-build).
4. **Draw bounded contexts.** Group concepts whose definitions must agree;
   split where the same word legitimately means different things. Name the
   relationship between each context pair (shared kernel, customer–supplier,
   conformist, anticorruption layer, separate ways).
5. **Model inside each context:** entities (identity + lifecycle), value
   objects (equality by value, immutable), aggregates (consistency boundary +
   root), domain services (operations owned by no entity), and domain events
   (facts other contexts may react to). State the invariant each aggregate
   protects — an aggregate with no invariant is just a folder.
6. **Record assumptions and open questions** separately: assumptions carry a
   risk-if-wrong; open questions name who can answer them.
7. **Stop at the gate.** Emit the model and halt. Do not create schemas,
   classes, or migrations unless the human explicitly requests implementation
   after seeing the model.

## Output Format

```
DOMAIN MODEL — <scope>
Business capability summary: <2–4 sentences>
Ubiquitous language: <term — definition — aliases/collisions>
Actors: <actor — goals>
Workflows: <name: trigger → steps → outcome>
Subdomains: <name — core|supporting|generic — why>
Bounded contexts:
  <context>: entities, value objects, aggregates (+ invariant each protects),
             domain services, domain events
Context relationships: <A → B: pattern, translation needed>
Assumptions: <each with risk-if-wrong>
Open questions: <each with who can answer>
GATE: model only — no code, schema, or migration written. Implementation
      proceeds only on explicit request after review.
```

## Validation Checklist

- [ ] Every term in the model traces to the requirements or code inspected —
      no invented vocabulary.
- [ ] Naming collisions listed with a chosen canonical term, not silently merged.
- [ ] Every aggregate names the invariant it protects.
- [ ] Every context relationship is named with a pattern, not just an arrow.
- [ ] Assumptions and open questions are separate sections, neither empty by
      neglect ("None" written deliberately if so).
- [ ] No code, schema, DDL, or migration files were created or edited.

## Gotchas

- Code is a biased witness: existing table names may encode an old, abandoned
  understanding. Treat code vocabulary as evidence, not verdict.
- CRUD language ("manage records") hides workflows; push until you find the
  business verbs, or the model degenerates into anemic entities.
- One bounded context per team-noun is a smell in both directions — contexts
  follow meaning boundaries, not org charts or folder layout.
- A "status" enum with 10+ values usually hides two or more entities or a
  missing state machine — flag it, don't transcribe it.
- Modeling everything at equal depth wastes the budget: core subdomains get
  aggregates and invariants; generic ones get a name and a buy/adopt note.

## Stop Conditions

- Requirements conflict with each other or with existing code on what a core
  concept *is* → hand to `source-of-truth-reconciler` before modeling on sand.
- A core-subdomain question has no answerable owner → stop and ask rather than
  modeling on an assumption with high risk-if-wrong.
- The human asks for implementation in the same breath — confirm the model
  first unless they explicitly waive review; the gate exists on purpose.

## Supporting Files

- [references/domain-artifacts.md](references/domain-artifacts.md) — definitions
  and quality bars for each artifact (entity vs VO tests, aggregate sizing,
  context-relationship patterns), with compact examples.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `architecture-designer`
  and `adr-writer` (design cluster).
