# Domain Artifact Definitions & Quality Bars

Supporting detail for `domain-modeler`. Read on demand.

## Entity vs. value object — the two-question test

| Question | Entity | Value object |
| --- | --- | --- |
| If every attribute matched, are two instances still different things? | Yes (identity) | No (equal by value) |
| Does it change over time while staying "the same thing"? | Yes (lifecycle) | No (replace, don't mutate) |

`Invoice` is an entity (Invoice #1042 stays #1042 as lines change). `Money`,
`DateRange`, `Address` are value objects — if you find yourself giving an
Address an id and an updated_at, ask whether you actually have a `Location`
entity or just relational-database habit.

## Aggregate sizing

An aggregate is the largest cluster that must be transactionally consistent —
and no larger. Quality bar:

- **Names its invariant.** "Order total equals sum of its lines" justifies
  Order owning OrderLines. No invariant → not an aggregate, just a query shape.
- **Referenced by id across boundaries.** Other aggregates hold `OrderId`, not
  an Order object.
- **Small by default.** If an aggregate would hold unbounded collections
  (a Tenant owning all its Documents), the invariant is probably eventual, not
  transactional — split it and use a domain event or a repair job.

## Domain events

A domain event is a past-tense fact (`InvoiceIssued`, `TrialExpired`) that
other contexts may react to. Quality bar: named in business language, carries
the ids needed to act, and does not leak the emitting context's internals.
If no consumer exists or is plausibly planned, note the event but don't design
infrastructure for it.

## Context relationship patterns

| Pattern | Use when | Cost to note |
| --- | --- | --- |
| Shared kernel | Two contexts co-own a small model subset | Coupled releases; needs joint ownership |
| Customer–supplier | Downstream can negotiate upstream's contract | Upstream planning must include downstream |
| Conformist | Downstream just adopts upstream's model | Upstream churn propagates unfiltered |
| Anticorruption layer | Upstream model is foreign/legacy/external | Translation code to build and maintain |
| Separate ways | Integration cost exceeds value | Duplication, eventual divergence |

Every arrow between contexts gets one of these names. "They talk to each
other" is not a relationship.

## Subdomain classification consequences

- **Core** — model deeply: aggregates, invariants, events, the works. This is
  where the business differentiates.
- **Supporting** — model enough to keep boundaries clean; simplest thing that
  works inside.
- **Generic** (auth, billing rails, notifications) — name it, define the
  contract to it, and recommend adopt/buy. Hand-modeling a generic subdomain
  in depth is the most common way to spend the whole budget on the wrong thing.

## Worked micro-example (naming collision)

Requirements say "customer"; the billing tables say `account`; support tooling
says "client". Resolution recorded in the language table:

| Term | Definition | Aliases | Context |
| --- | --- | --- | --- |
| Customer | The organization that pays and owns tenants | account (billing code), client (support docs) | Billing context |
| User | A person who signs in, belongs to a Customer | — | Identity context |

The collision row is the deliverable — silently picking one term reproduces
the confusion the model was meant to fix.
