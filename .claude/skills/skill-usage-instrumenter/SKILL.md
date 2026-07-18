---
name: skill-usage-instrumenter
description: 'Design usage instrumentation for a skill library — the evidence layer answering which skills actually FIRE in practice. Covers per-invocation signals (skill name, auto-trigger vs explicit call, coarse task class — never prompt content or user identifiers), wrong-fire/correction signals, never-fires detection over a stated window, evidence tiers (host-recorded vs self-reported), and thresholds turning counts into action (fix a trigger, split, or hand an evidence package to skill-deprecation-planner) — plus a rare-but-critical exemption: low usage alone never condemns a safety-net skill. Advisory/design only: adds no hooks, edits nothing. Use when asked which skills are used or unused, to instrument/measure skill invocation, or to ground pruning in evidence not assumption. Do NOT use for product/system telemetry (observability-operator), a skill definition''s quality (skill-quality-reviewer), eval execution design (eval-runner-designer), or the retirement plan itself (skill-deprecation-planner).'
---

# Skill Usage Instrumenter

## Purpose

Replace assumption with evidence about how a skill library is actually
used. A library grows on judgment — every skill shipped because someone
believed it would fire — but it can only be pruned and tuned on signal:
which skills trigger, which only ever run when explicitly named, which fire
on the wrong requests, and which have never fired at all. This skill designs
that signal layer: what to capture (and, just as firmly, what never to
capture), how to store and review it, and the thresholds at which counts
become actions — a trigger fix, a split, or an evidence package handed to
`skill-deprecation-planner`. The deliverable is an instrumentation design;
it changes no skill, adds no hook, and collects nothing itself.

## Use When

- Use when: asked which skills are actually used, unused, or misfiring —
  "do we know if anyone invokes these?", "half this library is probably
  dead."
- Use when: asked to design instrumentation, telemetry, or measurement for
  skill invocation and trigger behavior in real sessions.
- Use when: a pruning or consolidation effort needs a usage-evidence basis
  before anyone names removal candidates.
- Use when: trigger tuning needs field data — which skills fire only when
  explicitly named (a trigger-description failure smell), which fire and get
  corrected by the user (wrong-fire).
- Do NOT use when: designing telemetry for a product or system — metrics,
  logs, traces, alerting for services — that is `observability-operator`.
  This skill's subject is the library measuring ITSELF.
- Do NOT use when: judging whether a skill's definition is well-designed —
  that is `skill-quality-reviewer`; usage signal is the empirical complement
  to its structural judgment, not a replacement.
- Do NOT use when: designing how authored eval cases would be executed
  against a model — deliberate lab exercise is `eval-runner-designer`; this
  skill measures uncontrived, real-session behavior.
- Do NOT use when: planning the retirement of a skill the evidence already
  condemns — that is `skill-deprecation-planner`; this skill produces the
  evidence package that planner consumes.

## Inputs to Inspect

1. The host's invocation surface: what the harness records or could record
   about skill activation — session logs, invocation events, explicit
   skill-call records — and where those records live.
2. The library's shipped skill list and its overlap clusters (catalog +
   trigger-evals `overlaps_with` fields) — collision pairs are where
   wrong-fire signal matters most.
3. Any existing usage traces: session transcripts, closeout reports that
   name skills used, decision-log entries recording skill invocations.
4. The library's privacy/disclosure posture (for this repo, the
   product-agnostic rule: no live identifiers) — the minimization rules must
   be at least as strict.
5. The intended consumers: who reviews the signal, on what cadence, and
   which actions (trigger fix, split, deprecation handoff) they are
   authorized to take.

## Workflow

1. **Define the signal taxonomy.** Four families:
   - *Invocation:* skill name, auto-trigger vs explicit call, timestamp,
     coarse task class (e.g. "review", "build", "audit" — a small fixed
     enum, never free text).
   - *Correction (wrong-fire):* user overrode or redirected the skill
     choice; which skill won instead — the field counterpart of a
     trigger-evals discrimination case.
   - *Completion hint:* the skill's workflow ran to its deliverable vs was
     abandoned — coarse (delivered / abandoned / unknown), not a quality
     score.
   - *Non-events:* skills with zero invocations over the stated window —
     computed from the library list minus observed names, never from memory.
2. **Fix the minimization rules.** Capture skill NAMES and coarse enums
   only. Never captured, at any tier: prompt text, response content, user
   identifiers, repo/product names, file paths. The library measures itself,
   not its users — a usage record must be publishable inside the library
   repo without redaction.
3. **Map capture points and assign evidence tiers.** Host-recorded events
   (harness logs, invocation records) are tier 1. Self-reported mentions
   (closeout reports listing skills used) are tier 2 — subject to
   self-report bias and named as such. Anecdote ("we use that one a lot")
   is tier 3 and never sufficient for action. Where the host exposes no
   hook, design the tier-2 path honestly rather than pretending tier 1
   exists.
4. **Define aggregation and the review cadence.** Per-skill: fire count,
   auto-vs-explicit ratio, wrong-fire count, completion hints, last-fired
   date. Per-cluster: which sibling wins contested requests. Library-wide:
   never-fired list for the window. State the window explicitly; a
   never-fired verdict is only as good as the window is representative.
5. **Set thresholds that convert counts into actions.**
   - Fires only when explicitly named, never auto → trigger-description
     failure smell → re-review by `skill-quality-reviewer` (check 1/2).
   - Repeated wrong-fires against the same neighbor → collision evidence →
     discriminating trigger-evals + description fix on both sides.
   - Zero fires across N consecutive windows AND not exempt → deprecation
     candidate → evidence package to `skill-deprecation-planner`.
   Every threshold names its action and its consumer; a number with no
   consequence is decoration.
6. **Write the rare-but-critical exemption list.** Some skills exist for
   events that should be rare — incident response, recovery, refusal
   guards. Low usage is their success mode, not their failure mode. The
   design requires an explicit exemption list with a reason per entry, and
   the rule that usage alone never condemns an exempt skill.
7. **Specify the evidence-package format** for downstream consumers: window,
   tiers of the supporting signal, per-skill numbers with denominators,
   known blind spots — so `skill-deprecation-planner` receives evidence, not
   a verdict, and the human decision stays informed.
8. **Deliver the design** in the Output Format. Implementation (adding
   hooks, wiring storage) is a separate task for the host's owners.

Signal schema, minimization table, evidence tiers, threshold catalog, and
the exemption-list format:
[references/usage-signal-catalog.md](references/usage-signal-catalog.md).

## Output Format

```
SKILL USAGE INSTRUMENTATION DESIGN — <library / host>
Signals:       <invocation | correction | completion-hint | non-event — fields per family>
Minimization:  captured: <fields>; never captured: prompt/response content, user identifiers, live names/paths
Capture points:<host hook(s) found → tier 1 | self-report path → tier 2; honest statement of which exist today>
Aggregation:   <per-skill, per-cluster, library-wide views; window: <stated>>
Cadence:       <review rhythm + who reviews>
Thresholds:    <signal pattern → action → consumer (skill-quality-reviewer | trigger-evals fix | skill-deprecation-planner)>
Exemptions:    rare-but-critical list: <skill → reason> (usage alone never condemns these)
Evidence package: <format handed to skill-deprecation-planner>
Not designed:  <what this design deliberately leaves out, and why>
```

## Validation Checklist

- [ ] Every signal field is a name, enum, count, or date — no free text,
      no prompt/response content, no user identifiers anywhere in the
      schema.
- [ ] Every capture point carries an evidence tier, and tiers that don't
      exist today are stated as not existing (no imagined tier-1 hooks).
- [ ] The never-fired computation derives from the full library list minus
      observations, with the window stated.
- [ ] Every threshold names both its action and its consumer.
- [ ] The rare-but-critical exemption list exists with a reason per entry.
- [ ] Denominators are defined for every rate (fires per session, per task
      class) — and estimated denominators are labeled estimates.
- [ ] The design adds no hooks and edits no skills — implementation is
      explicitly handed off.

## Gotchas

- The seatbelt fallacy: pruning by usage alone removes exactly the skills
  you need on the worst day. Incident, recovery, and refusal-guard skills
  are rare-by-design — hence the exemption list, written before the first
  count is read.
- Self-report bias: closeout-mentioned skills skew toward the memorable
  and the flattering. Tier-2 evidence supports investigation, not
  deprecation on its own.
- The denominator problem: "fired 4 times" means nothing without "out of
  how many eligible requests" — and eligibility is genuinely hard to
  compute. Estimated denominators must say so, or rates will masquerade as
  facts.
- Unrepresentative windows: a quarter dominated by one kind of work
  condemns every skill the work didn't need. Never-fired verdicts need
  either a long window or explicit workload framing.
- Minimization creep: "just capture the prompt this once, for debugging"
  converts a self-measurement layer into user surveillance. The
  publishable-in-repo test is the line: if the record couldn't be committed
  openly, it captures too much.
- Wrong-fire vs preference: a user redirecting a skill choice sometimes
  means the trigger misfired, sometimes means the user wanted a different
  tool for a valid overlap. Correction events are evidence for review, not
  automatic trigger defects.
- Goodhart drift: once usage counts exist, "make the number go up" becomes
  a temptation — descriptions broadened to farm invocations. Usage signal
  feeds quality review; it must never become a target.

## Stop Conditions

- Asked to capture prompt content, response text, user identifiers, or
  live product/repo names in the usage schema → refuse; minimization is a
  design invariant, not a tunable. Offer coarse enums instead.
- Asked to implement the hooks or start collecting as part of this design →
  stop at the spec; instrumentation touches the host and needs its owners'
  approval as a separate task.
- Asked to name deprecation candidates from the design's hypothetical or
  not-yet-collected numbers → refuse; no data, no verdicts. The design
  defines how evidence WOULD accrue.
- Asked to skip the exemption list ("just rank everything by count") →
  refuse; a ranking that can condemn a safety-net skill is broken by
  construction.
- The host exposes no capture point at all and the requester wants tier-1
  claims anyway → stop and state the honest options: design the tier-2
  self-report path, or get a host-side hook built first.

## Supporting Files

- [references/usage-signal-catalog.md](references/usage-signal-catalog.md)
  — the signal schema field-by-field, the minimization
  capture/never-capture table, evidence-tier definitions, the threshold →
  action → consumer catalog, denominator guidance, and the exemption-list
  format.
- `evals/evals.json` — behavior cases including the no-host-hooks edge and
  the capture-prompt-content refusal.
- `evals/trigger-evals.json` — discrimination against
  `observability-operator`, `skill-deprecation-planner` (evidence vs
  retirement plan), `eval-runner-designer` (field vs lab), and
  `skill-quality-reviewer`.
