# Funnel Sheet

Detail for `funnel-definition-designer`. Read on demand.

## Counting model

| Model | Counts | Answers |
|---|---|---|
| Unique users | Distinct users reaching each step | "What share of people convert?" |
| Sessions | Distinct sessions | "What share of visits convert?" |
| Events | Raw event counts | Volume, not conversion (rarely a funnel) |

Pick ONE and use it consistently across steps. Mixing models per step
makes the funnel unreasonable.

## Denominator discipline

Conversion is always "X of a POPULATION". Pin the population:
- All signups? Signups who reached step 1? Signups in a date range?
Changing it silently changes the rate on identical data. State it with
every number.

## Conversion window

| Window | Effect |
|---|---|
| Same session | Strictest; lowest rate |
| 24h / 7d | Common; state which |
| Unbounded | Inflates — nearly everyone eventually converts |

Never report a rate without its window. An unwindowed conversion is
uninterpretable.

## Order semantics

| Semantics | Meaning | Watch for |
|---|---|---|
| Strict sequential | Steps in exact order | Drops legitimate skips/re-entries |
| Any-order | All steps, any sequence | Over-counts; loses journey shape |
| Reached step N | Got at least this far | Good for drop-off location |

Real journeys branch and revisit. Choose to match the question; state
re-entry and skip handling.

## Attribution (multi-touch entries)

- First-touch: credit the first interaction.
- Last-touch: credit the last before conversion.
- Other (linear, position-based): only if justified.
State it — it changes the answer.

## Retention curves (label which)

| Curve | Definition |
|---|---|
| n-day retention | Returned on exactly day N |
| Unbounded retention | Returned on day N or later |
| Rolling retention | Active within a window around day N |

Specify: return event, cohort basis (signup date / first action),
interval, and which curve. "Retention = 40%" without these can't be
compared.

## WHERE vs WHY

The funnel locates drop-off. It does NOT explain it. Any cause
("confusing", "too slow") is a hypothesis for:
- `ab-test-designer` (controlled test), or
- user research.
Segment comparisons are correlational and confounded by selection — never
a causal finding on their own.
