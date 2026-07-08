---
name: funnel-definition-designer
description: Define product funnels and conversion/retention measurement rigorously — the ordered funnel steps grounded in the analytics event schema, the counting model (unique users vs sessions vs events) with an honest denominator, the conversion window (how long a user has to complete), strict-order vs any-order steps, attribution (first/last touch), drop-off and segmentation analysis, and cohort/retention curves — while keeping one metric to one definition so numbers stop drifting, and separating WHERE users drop (measurable) from WHY (a hypothesis, not the funnel's output). Consumes the events defined by event-schema-architect. Use when defining a funnel or conversion metric, measuring drop-off or retention, or when a conversion number is disputed because its definition is unclear. Do NOT use to design the event schema itself (event-schema-architect), to instrument where events fire (product-analytics-instrumenter), or to run a controlled experiment that TESTS a change's causal effect (ab-test-designer).
---

# Funnel Definition Designer

## Purpose

"Our conversion is 34%." Thirty-four percent of what, measured how, over
what window, counting users or sessions? A funnel that can't answer those
is a number two people will argue about forever because they're
computing different things and both are "right". This skill defines
funnels and conversion/retention metrics with the rigor that makes them
trustworthy: ordered steps grounded in real events, an explicit counting
model and denominator, a stated conversion window, order and attribution
semantics, and one canonical definition per metric so it stops drifting.
It insists on the honest boundary of what a funnel can say — it shows
WHERE users drop, never WHY — and hands the why to experiments and
research. It consumes the event schema from `event-schema-architect`.

## Use When

- Use when: defining a funnel, a conversion metric, or a retention/cohort
  curve for a product journey.
- Use when: measuring drop-off between steps or segmenting conversion by
  cohort/attribute.
- Use when: a conversion number is disputed because nobody agreed on its
  definition (denominator, window, unique-vs-event).
- Use when: a metric has drifted — the same "activation rate" means
  different things on two dashboards.
- Do NOT use when: the needed events don't exist or aren't consistently
  defined — go to `event-schema-architect` first; a funnel on undefined
  events measures noise.
- Do NOT use when: the task is WHERE/HOW events fire in code (client vs
  server, consent, tracking QA) — that is `product-analytics-instrumenter`.
- Do NOT use when: the task is to TEST whether a change CAUSES a
  conversion difference — that is `ab-test-designer`; a funnel measures
  the current state, it doesn't establish causation.

## Inputs to Inspect

1. The decision the funnel informs: what will be done differently
   depending on the number — this bounds the right definition.
2. The event schema (from `event-schema-architect`): the events and
   properties available to ground each step; gaps route back there.
3. The journey being measured: the real user path, including legitimate
   branches and re-entries, not an idealized straight line.
4. Existing definitions of this metric: prior funnels/dashboards and how
   their definitions differ — the drift to reconcile.
5. The population and time frame: who is in the denominator and over what
   window the measurement runs.

## Workflow

1. **State the question and the decision.** What conversion/journey, for
   what decision. A funnel built without a decision behind it becomes a
   vanity chart nobody acts on.
2. **Define steps from real events.** Each step is a specific event
   (optionally filtered by properties) from the tracking plan, in order.
   If a needed step has no event, stop and route to
   `event-schema-architect` — don't approximate with the wrong event.
3. **Choose the counting model and fix the denominator.** Unique users
   vs sessions vs event counts — pick per the question and state it. Then
   pin the denominator: conversion is X of WHAT population? A shifting or
   unstated denominator is the single most common funnel lie.
4. **Set the conversion window.** How long a user has to complete the
   funnel (same session, 24h, 7d, unbounded). Longer windows inflate
   conversion; state the window with the number, always — an unwindowed
   rate is uninterpretable.
5. **Decide order semantics.** Strict sequential (steps in order),
   any-order (all steps, any sequence), or "reached step N". Real journeys
   branch and revisit — choose the semantics that match the question and
   note how re-entries and skips are counted.
6. **State attribution where it matters.** For multi-touch entries,
   first-touch vs last-touch vs another model — stated, because it
   changes the answer. Don't leave attribution implicit.
7. **Design drop-off and segmentation honestly.** Where users fall out,
   by segment. Segment comparisons are correlational: the funnel shows
   the WHERE, and any WHY is a hypothesis to test (`ab-test-designer`) or
   research — never asserted as a finding from the funnel alone.
8. **Handle retention/cohorts explicitly.** If retention: define the
   return event, the cohort (by signup date/first action), the interval,
   and n-day vs unbounded/rolling retention — these are different curves,
   labeled as such.
9. **Lock one canonical definition.** Record the funnel's full definition
   (steps, counting, denominator, window, order, attribution) as the
   single source for that metric, versioned, so it stops drifting.
10. **Name boundaries and deliver** the funnel definition in the Output
    Format.

Counting-model and window guidance, order-semantics patterns, and the
retention-curve definitions:
[references/funnel-sheet.md](references/funnel-sheet.md).

## Output Format

```
FUNNEL DEFINITION — <journey/metric>
Question/decision: <what this informs>
Steps:         1. <Event + filter>  2. <Event>  3. <Event>  (grounded in tracking plan)
Counting:      unique users | sessions | events   (stated)
Denominator:   <the population conversion is measured against — pinned>
Window:        <same-session | 24h | 7d | unbounded>  (always stated with the rate)
Order:         strict | any-order | reached-step-N; re-entry/skip handling
Attribution:   first-touch | last-touch | other (if multi-touch)
Segmentation:  <segments>; comparisons are correlational (WHERE, not WHY)
Retention:     return event, cohort basis, interval, n-day vs rolling (if applicable)
Canonical def: recorded as the single source for this metric; versioned
Boundaries:    schema → event-schema-architect; firing → product-analytics-instrumenter;
               causal test → ab-test-designer
```

## Validation Checklist

- [ ] Each step maps to a specific, existing event; missing events route
      to `event-schema-architect`.
- [ ] The counting model (users/sessions/events) is stated.
- [ ] The denominator is pinned and stable — conversion is "of" a named
      population.
- [ ] The conversion window is stated with the rate; no unwindowed
      numbers.
- [ ] Order semantics and re-entry/skip handling are explicit.
- [ ] Attribution is stated where entries are multi-touch.
- [ ] Segment comparisons are labeled correlational; no WHY is asserted
      from the funnel alone.
- [ ] Retention curves specify return event, cohort, interval, and n-day
      vs rolling.
- [ ] One canonical, versioned definition is recorded to prevent drift.

## Gotchas

- The denominator is where funnels lie: quietly change the population
  (all signups vs signups who reached step 1) and the same event data
  yields wildly different "conversion". Pin it and state it.
- A conversion rate with no window is meaningless — over an infinite
  window nearly everyone eventually converts. Every rate carries its
  window.
- Users vs sessions vs events answer different questions and give
  different numbers; mixing them across steps produces a funnel that
  can't be reasoned about. Pick one, state it.
- A funnel shows WHERE users drop, not WHY. "They drop at checkout
  because it's confusing" is a hypothesis; the funnel didn't say
  "confusing". Route causal claims to an experiment.
- Real journeys aren't a straight line — people skip, revisit, and
  re-enter. Strict-order semantics silently drop legitimate conversions;
  any-order over-counts. Choose deliberately.
- Segment comparisons invite causal stories ("mobile users convert worse,
  so fix mobile") that confound selection effects. The segments differ in
  more than the one thing you're blaming.
- n-day retention, unbounded retention, and rolling retention are three
  different curves; labeling one as "retention" without saying which
  makes cross-team comparison meaningless.

## Stop Conditions

- The events needed for the steps don't exist or are inconsistently
  defined → route to `event-schema-architect`; a funnel on undefined
  events is measuring noise.
- The task is to establish whether a change CAUSES a conversion
  difference → route to `ab-test-designer`; a funnel cannot prove
  causation.
- The task is instrumentation (where/how events fire, consent, tracking
  QA) → route to `product-analytics-instrumenter`.
- A stakeholder insists the funnel proves a specific cause of drop-off →
  hold the line: the funnel locates the drop; the cause needs an
  experiment or research, and asserting it from the funnel alone is a
  correctness error to flag.

## Supporting Files

- [references/funnel-sheet.md](references/funnel-sheet.md) — counting-
  model and window guidance, denominator discipline, order-semantics
  patterns, and the retention-curve definitions.
- `evals/evals.json` — behavior cases including the disputed-denominator
  reconciliation, the windowing fix, and the correlation-not-causation
  refusal.
- `evals/trigger-evals.json` — discrimination against `event-schema-architect`
  (schema vs funnel), `product-analytics-instrumenter` (firing), and
  `ab-test-designer` (measure vs causal test).
