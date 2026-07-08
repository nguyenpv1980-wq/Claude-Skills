---
name: ab-test-designer
description: Design AND read A/B and controlled experiments honestly — a falsifiable hypothesis, ONE primary metric plus guardrails, the randomization unit (sticky, non-contaminating), a sample-size/power calculation from a minimum detectable effect, and a pre-set duration that respects weekly cycles and forbids peeking-to-significance; then the READOUT — statistical vs practical significance with confidence intervals, the peeking/early-stopping trap, multiple-comparison and segment-fishing caveats, sample-ratio-mismatch, Simpson's paradox and novelty effects, and a ship/kill/iterate decision stating residual uncertainty. Consumes metrics from funnel-definition-designer; can run on a feature-flag-rollout-strategist flag. Use when designing an experiment, sizing/powering a test, or interpreting results. Do NOT use to plan a flag-gated ROLLOUT for safety (feature-flag-rollout-strategist), define the metric measured (funnel-definition-designer), or design the event schema (event-schema-architect).
---

# A/B Test Designer

## Purpose

Most A/B tests are theater: a test stopped the day it hit significance, a
winner declared from the one metric out of twenty that moved, a "flat"
result from a test that never had the power to detect anything. This
skill designs experiments that can actually answer the question and reads
them without fooling anyone — a falsifiable hypothesis, one primary
metric with guardrails, a real power calculation that sets sample size
and duration up front, and assignment that's sticky and uncontaminated;
then a readout that respects the fixed horizon, reports effect size with
uncertainty, and navigates the traps (peeking, multiple comparisons,
Simpson's paradox, novelty, sample-ratio mismatch) to a ship/kill/iterate
decision stated with its residual uncertainty. It covers BOTH the design
and the analysis. It runs experiments; it does not plan safety rollouts
(`feature-flag-rollout-strategist`) or define the metrics it measures
(`funnel-definition-designer`).

## Use When

- Use when: designing an A/B test or controlled experiment — hypothesis,
  metrics, randomization, sample size, and duration.
- Use when: sizing/powering a test or deciding whether one is even worth
  running given available traffic.
- Use when: interpreting experiment results and making a ship/kill/
  iterate decision.
- Use when: a test result looks suspicious (stopped early, a segment
  "win", a flipped aggregate) and needs an honest re-read.
- Do NOT use when: the task is a safety ROLLOUT — progressive %s,
  guardrail auto-rollback, kill switch — that is
  `feature-flag-rollout-strategist`; an experiment and a rollout can
  share a flag but are different jobs.
- Do NOT use when: the task is DEFINING the metric/funnel being measured
  — that is `funnel-definition-designer`; the experiment consumes that
  definition.
- Do NOT use when: the task is the analytics event schema — that is
  `event-schema-architect`.

## Inputs to Inspect

1. The change under test and the decision it serves: what will be shipped,
   killed, or iterated based on the result.
2. The metric(s): the candidate primary metric and guardrails, grounded
   in `funnel-definition-designer` / `event-schema-architect` definitions
   (a fuzzy metric makes the whole test fuzzy).
3. The traffic and baseline: users/sessions per period eligible for the
   test, and the baseline rate and variance of the primary metric — the
   inputs to power.
4. The assignment mechanism: how users can be bucketed, stickily, and
   whether contamination/spillover between variants is possible (shared
   accounts, network effects).
5. Constraints: how long the test can run, weekly/seasonal cycles, and
   any results already collected (with their collection method, for a
   valid re-read).

## Workflow

1. **Write a falsifiable hypothesis.** A specific predicted change in a
   specific metric with a direction, tied to a decision — "changing X
   will increase primary metric M", not "let's see if X is better".
2. **Pick ONE primary metric and guardrails.** One metric decides the
   test (an Overall Evaluation Criterion); guardrails are what must not
   regress (revenue, latency, retention, error rate). Many co-equal
   "primary" metrics is how every test finds a "win".
3. **Choose the randomization unit and protect against contamination.**
   Usually the user; the account/cluster when within-unit interference
   exists. Assignment is sticky (a stable id) and consistent across
   surfaces. Note spillover/network effects that violate independence.
4. **Power the test.** Choose a minimum detectable effect that is
   PRACTICALLY meaningful (not the smallest detectable). With the
   baseline rate/variance, significance level, and target power, compute
   the required sample size and derive the DURATION from traffic. If the
   traffic can't power the MDE in a reasonable time, say so — running an
   underpowered test wastes weeks to learn nothing.
5. **Fix the horizon and forbid peeking.** Set the duration up front,
   covering full weekly cycles; analyze at the planned end. Do NOT stop
   early the moment it's significant — that inflates false positives
   badly. If interim looks are required, use a proper sequential/always-
   valid method with its correction, stated in advance.
6. **Read results honestly.** Report the effect size WITH a confidence
   interval, not just a p-value; contrast statistical significance
   against PRACTICAL significance (did it move enough to matter, per the
   MDE); check the guardrails. A non-significant result is "we couldn't
   detect an effect of size ≥ MDE", not "no effect" — distinguish
   underpowered from a true null.
7. **Navigate the traps.** Check sample-ratio mismatch (a skewed split
   invalidates the test). Correct or pre-register for multiple
   comparisons (many metrics/segments → inflated false positives);
   post-hoc segment "wins" are hypotheses, not findings. Watch Simpson's
   paradox (aggregate reverses within segments), and novelty/primacy
   effects (early behavior ≠ steady state).
8. **Decide with stated uncertainty.** Ship / kill / iterate, citing the
   effect, its interval, guardrail status, and what remains uncertain.
   "Ship — +2.1% [CI 0.5–3.7%], guardrails flat" beats "it won".
9. **Name boundaries and deliver** the design and/or readout in the
   Output Format.

Power/sample-size inputs, the peeking-inflation explanation, the
multiple-comparison corrections, and the validity-check list (SRM,
Simpson's, novelty):
[references/ab-test-sheet.md](references/ab-test-sheet.md).

## Output Format

```
EXPERIMENT — <change under test>   [DESIGN | READOUT]
Hypothesis:    <falsifiable, directional, tied to a decision>
Primary metric: <ONE> (from funnel/event definitions)  Guardrails: <must-not-regress set>
Unit:          user | account/cluster; sticky; contamination/spillover notes
Power:         MDE=<practically meaningful>; baseline=<rate/var>; α=<>, power=<>;
               required n=<>; DURATION=<derived, full weekly cycles>
Horizon:       fixed end date; peeking forbidden (or sequential method + correction stated)
-- READOUT (if analyzing) --
Result:        effect=<size> CI=[..]; statistical sig=<y/n>; practical sig vs MDE=<y/n>
Guardrails:    <status>
Validity:      SRM check; multiple-comparison handling; Simpson's/novelty checks
Decision:      ship | kill | iterate — with residual uncertainty stated
Boundaries:    safety rollout → feature-flag-rollout-strategist; metric def →
               funnel-definition-designer; schema → event-schema-architect
```

## Validation Checklist

- [ ] The hypothesis is falsifiable, directional, and tied to a decision.
- [ ] Exactly ONE primary metric; guardrails are named separately.
- [ ] Randomization unit is chosen for independence; assignment is sticky;
      contamination is assessed.
- [ ] Sample size is computed from a practically-meaningful MDE and
      duration derived from traffic; underpowered tests are flagged, not
      run blind.
- [ ] The horizon is fixed up front over full cycles; peeking-to-
      significance is forbidden (or a sequential method is used with its
      correction).
- [ ] Results report effect size with a confidence interval, not a bare
      p-value; practical vs statistical significance is distinguished.
- [ ] Validity checks run: sample-ratio mismatch, multiple comparisons,
      Simpson's paradox, novelty effects.
- [ ] A non-significant result is not reported as "no effect"; the
      decision states residual uncertainty.
- [ ] Rollout, metric-definition, and schema concerns are handed to their
      owning skills.

## Gotchas

- Stopping the moment it's significant is the most common way to ship a
  false winner: with continuous peeking, the false-positive rate climbs
  far past 5%. Fix the horizon, or use a method built for peeking.
- Twenty metrics and no correction guarantees a "win" by chance alone —
  one in twenty clears p<0.05 under the null. Pre-register the primary
  metric; treat the rest as guardrails or exploratory.
- A post-hoc "it worked great for mobile users in Canada" is a hypothesis
  generated by fishing, not a result. Slicing until something is
  significant is p-hacking with extra steps.
- "Not significant" is not "no difference" — an underpowered test can't
  tell a null from a missed real effect. Report the confidence interval;
  a wide one around zero means "we don't know", not "no effect".
- Sample-ratio mismatch (a 50/50 split that arrives 53/47) signals a
  broken experiment — differential bucketing or logging — and invalidates
  the result no matter how pretty. Check it first.
- Novelty and primacy effects make early data lie in both directions:
  users click the new thing because it's new, or resist it because it's
  unfamiliar. Steady-state needs enough time.
- Simpson's paradox: the variant can win overall while losing in every
  segment (or vice versa) when segment sizes shift. Look within, not just
  at the aggregate.
- Statistical significance without practical significance is a trap: a
  0.05% lift can be "significant" at huge n and worthless to the
  business. Judge against the MDE you set for a reason.

## Stop Conditions

- The task is a safety rollout (progressive %s, auto-rollback, kill
  switch), not a hypothesis test → route to
  `feature-flag-rollout-strategist`.
- The metric to be tested isn't rigorously defined → route to
  `funnel-definition-designer` first; an experiment on a fuzzy metric
  produces a fuzzy verdict.
- The available traffic cannot power the practically-meaningful MDE in a
  feasible time → surface that the test can't answer the question and
  offer alternatives (bigger effect, longer run, or a different method)
  rather than running it underpowered.
- Someone demands the test be stopped early on an interim "win" or
  re-sliced until a segment is significant → decline and explain the
  false-positive inflation; a valid decision waits for the fixed horizon
  and pre-registered analysis.

## Supporting Files

- [references/ab-test-sheet.md](references/ab-test-sheet.md) — power/
  sample-size inputs, the peeking-inflation explanation, multiple-
  comparison corrections, and the validity-check list (SRM, Simpson's,
  novelty, practical-vs-statistical).
- `evals/evals.json` — behavior cases including the powered design, the
  no-peeking refusal, and the honest null read.
- `evals/trigger-evals.json` — discrimination against `feature-flag-rollout-strategist`
  (experiment vs safety rollout), `funnel-definition-designer` (test vs
  metric definition), and `product-analytics-instrumenter` (test vs firing).
