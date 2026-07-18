---
name: feature-flag-rollout-strategist
description: 'Design the ROLLOUT STRATEGY for shipping a change safely behind a flag — classify the flag by purpose (release, ops/kill-switch, experiment, permission — release flags stay separate from permanent entitlements), plan progressive delivery (internal → canary/% → cohorts → GA), define sticky targeting, set guardrail metrics with auto-rollback criteria and a tested kill switch, choose the fail-safe default when the flag service is down, and manage the lifecycle so release flags are removed after GA (flag debt). Owns HOW a change is de-risked — NOT the entitlement/permission model: WHO a plan or role includes is plan-entitlement-architect / authorization-matrix-designer, and an experiment''s DESIGN/readout is ab-test-designer. Use when planning a staged rollout, a canary or percentage ramp, a kill switch, or flag cleanup. Do NOT use to model plan/feature entitlements (plan-entitlement-architect), role permissions (authorization-matrix-designer), or design/analyze an A/B test (ab-test-designer).'
---

# Feature Flag Rollout Strategist

## Purpose

Feature flags are simultaneously the best way to ship safely and the
easiest way to create a permanent mess. Done well, a change reaches 1%
of internal users, bakes against guardrail metrics, expands to cohorts,
and hits GA — with a kill switch that has actually been tested. Done
badly, a "temporary" release flag becomes load-bearing config three
years later, a percentage rollout flip-flops users between variants
because assignment isn't sticky, and the flag is quietly conflated with
an entitlement so turning it off removes a paying customer's feature.
This skill designs the rollout STRATEGY: the flag's real purpose,
progressive stages with advance and rollback criteria, sticky targeting,
guardrails with automatic rollback, a fail-safe default, and the
lifecycle that removes the flag when it's done. It owns how a change is
de-risked into production — not who is entitled to it.

## Use When

- Use when: planning a staged/progressive rollout — internal → canary →
  percentage ramp → cohorts → GA — for a new or risky change.
- Use when: designing guardrail metrics and automatic-rollback criteria,
  or a kill switch for a change.
- Use when: choosing targeting/segmentation for a gradual release, or the
  fail-safe default if the flag service is unavailable.
- Use when: cleaning up flag debt — deciding which flags are temporary
  release flags to remove vs long-lived operational controls.
- Do NOT use when: the question is WHO gets a feature as a matter of
  PLAN — "does the Pro plan include X", usage limits, metered quotas —
  that is `plan-entitlement-architect` (permanent entitlement, not a
  rollout).
- Do NOT use when: the question is WHO may do something as a matter of
  ROLE/permission — that is `authorization-matrix-designer`.
- Do NOT use when: the flag hosts an EXPERIMENT and the task is the
  experiment's hypothesis, sample size, or reading the result — that is
  `ab-test-designer`; this skill can carry the flag it runs on, but not
  the experiment design.

## Inputs to Inspect

1. The change being rolled out: its blast radius, reversibility, and what
   "bad" would look like in production (errors, latency, wrong data,
   conversion drop).
2. The flag's REAL purpose: is it a temporary release flag, a long-lived
   operational kill switch, an experiment bucket, or — a common
   mislabel — actually an entitlement/permission?
3. The available metrics: which guardrail signals exist and are trustworthy
   enough to gate/rollback on (from `observability-operator` /
   `slo-reliability-architect` outputs if present).
4. The user/segment model: how users can be targeted and bucketed, and
   whether assignment can be made sticky by a stable id.
5. The flag platform's behavior: default/fallback when the service is
   unreachable, evaluation latency, and how flags are cleaned up today
   (or whether dead flags accumulate).

## Workflow

1. **Classify the flag — this decides everything.** Release (temporary,
   removed after GA), operational/kill-switch (long-lived control),
   experiment (A/B — design goes to `ab-test-designer`), or
   entitlement/permission (PERMANENT — if so, this is the wrong skill;
   route to `plan-entitlement-architect` / `authorization-matrix-designer`).
   Misclassification is the root of most flag pathologies.
2. **Design progressive stages.** internal/dogfood → canary or small % →
   cohort expansion → GA. For each stage: the population, the bake time,
   the advance criteria (guardrails green for long enough), and the
   rollback criteria. No stage advances on vibes.
3. **Make targeting sticky.** Bucket by a stable identifier so a user
   stays in one variant across sessions and surfaces — flip-flopping is
   both a UX bug and an analytics-invalidating one. Choose low-risk
   segments first; state exclusions.
4. **Set guardrails and automatic rollback.** A SMALL set of metrics that
   must not regress (error rate, latency, a key conversion/correctness
   signal), each with a threshold that triggers rollback — automatic
   where possible. Define the kill switch and require it to be TESTED,
   not assumed.
5. **Choose the fail-safe default.** What the flag evaluates to if the
   flag service is down or slow — the SAFE state (usually "old behavior"
   for a release flag; "protective" for a kill switch). A flag that fails
   open into unfinished code is an outage waiting for a network blip.
6. **Map interactions and consistency.** Combinatorial states when
   multiple flags overlap, consistency of a user's experience across
   pages/devices, and caching of flag values. Flag the risky combinations.
7. **Plan the lifecycle (flag debt).** Every release flag gets an owner
   and a removal trigger (post-GA + soak). The cleanup — delete the flag
   AND the dead code path — is part of THIS plan, not a someday ticket.
   Long-lived ops flags are documented as intentional.
8. **Name boundaries and deliver.** Entitlement/permission →
   `plan-entitlement-architect` / `authorization-matrix-designer`;
   experiment design/readout → `ab-test-designer`; executing the rollout
   and flipping flags on live systems follows the repo's approval path,
   not this design skill.

Flag-type classification table, stage/advance-criteria patterns, and the
fail-safe-default guide:
[references/flag-rollout-sheet.md](references/flag-rollout-sheet.md).

## Output Format

```
ROLLOUT STRATEGY — <change>
Flag type:    release | ops/kill-switch | experiment | (entitlement → WRONG SKILL, routed)
Stages:       internal → canary/% → cohorts → GA
  per stage:  population, bake time, ADVANCE criteria (guardrails green), ROLLBACK criteria
Targeting:    sticky by <stable id>; first segments; exclusions
Guardrails:   <small metric set> each with rollback threshold; automatic where possible
Kill switch:  <mechanism> — TESTED; who can trigger; how fast
Fail-safe:    flag-service-down default = <safe state> (release → old behavior)
Interactions: <risky flag combinations; cross-surface consistency; caching>
Lifecycle:    owner + removal trigger; cleanup = delete flag + dead code path
Boundaries:   entitlement → plan-entitlement-architect / authorization-matrix-designer;
              experiment → ab-test-designer; live execution → approval path
```

## Validation Checklist

- [ ] The flag is classified by purpose; if it's really an entitlement/
      permission, it's routed out, not designed here.
- [ ] Stages have explicit populations, bake times, and BOTH advance and
      rollback criteria — no advancing on vibes.
- [ ] Targeting is sticky by a stable id; a user doesn't flip variants
      across sessions/surfaces.
- [ ] A small guardrail-metric set has rollback thresholds, automatic
      where possible, plus a TESTED kill switch.
- [ ] The fail-safe default (flag service down) is the safe state, not
      unfinished code failing open.
- [ ] Risky flag interactions and cross-surface consistency are
      addressed.
- [ ] Every release flag has an owner and a removal trigger; cleanup of
      flag AND dead code is in the plan.
- [ ] Entitlement, experiment, and live-execution concerns are handed to
      their owning skills/processes.

## Gotchas

- The most expensive flag is the "temporary" one nobody removed: it
  becomes load-bearing config, doubles the code paths under test, and
  eventually someone flips it wrong. A removal trigger at creation is the
  only reliable cure.
- A release flag and an entitlement look identical in code and are
  opposite in meaning: one is meant to be deleted, the other is
  permanent product surface. Turning off a flag that was secretly an
  entitlement removes a paying customer's feature. Classify first.
- Non-sticky percentage rollouts flip users between old and new on every
  evaluation — infuriating UX and ruined analytics. Bucket by a stable
  id, always.
- A kill switch that has never been pulled is a hypothesis, not a safety
  mechanism. Test it before you need it, under load.
- Failing OPEN (flag defaults to the new code path when the flag service
  is unreachable) turns a flag outage into a feature outage — often into
  half-built code. Release flags fail to the OLD behavior.
- Guardrails with ten metrics and no thresholds don't gate anything.
  Pick the few that mean "this is going wrong" and give each a rollback
  number.
- Overlapping flags create a combinatorial state space nobody tested;
  two independent 50% rollouts make four populations. Map the
  interactions that matter.

## Stop Conditions

- The "flag" is actually an entitlement (plan/feature gating, quotas) or
  a permission (role can/can't) → route to `plan-entitlement-architect`
  or `authorization-matrix-designer`; these are permanent models, not
  rollouts, and designing them as flags creates drift.
- The flag hosts an experiment and the ask is the experiment design or
  result readout → route to `ab-test-designer`; this skill carries the
  rollout, not the statistics.
- No trustworthy guardrail metric exists to gate/rollback on → surface
  that the rollout would be blind and get the metric wired
  (`observability-operator`) before ramping beyond a tiny canary.
- Asked to actually flip flags / execute the rollout on live production →
  decline execution; this skill designs the strategy, and live changes
  follow the repo's human-approval path.

## Supporting Files

- [references/flag-rollout-sheet.md](references/flag-rollout-sheet.md) —
  the flag-type classification table, stage/advance-criteria patterns,
  guardrail selection, and the fail-safe-default guide.
- `evals/evals.json` — behavior cases including the staged rollout with
  guardrails, the sticky-bucketing fix, and the flag-vs-entitlement
  refusal.
- `evals/trigger-evals.json` — discrimination against `plan-entitlement-architect`
  and `authorization-matrix-designer` (the entitlement/permission seams)
  and `ab-test-designer` (the experiment seam).
