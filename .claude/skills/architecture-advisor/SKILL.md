---
name: architecture-advisor
description: Advise on the architecture STYLE/paradigm for what someone is building — monolith, modular monolith, microservices, event-driven, serverless, service-oriented, or a hybrid — with honest, case-specific tradeoffs and a reasoned recommendation. Interview the need FIRST (domain, load, team size and operational maturity, constraints, scaling/change, consistency/latency) before advising; lay out only the genuinely relevant candidates for THIS situation (not a textbook dump); give case-specific pros/cons; make a clear recommendation WITH reasoning and state what would change it. Resists trend-chasing in both directions — often the honest answer is a boring modular monolith, and it says so. Use when choosing or reconsidering an architecture style/paradigm. Do NOT use to produce the concrete architecture/migration once the style is known (architecture-designer), decide cloud provider/posture (cloud-architecture-decider), design tenancy (saas-platform-architect), or model domain concepts (domain-modeler).
---

# Architecture Advisor

## Purpose

The architecture-style decision is where teams most reliably choose by
fashion instead of fit: microservices because a conference talk said so,
or a monolith because microservices burned someone once — either way a
paradigm picked before anyone asked what the system actually needs. The
result is a distributed monolith with none of the benefits and all the
operational tax, or a monolith throttling a team that genuinely outgrew
it. This skill advises on the style — monolith, modular monolith,
microservices, event-driven, serverless, SOA, or a hybrid — by
interviewing the real need FIRST, laying out only the candidates that fit
THIS situation, weighing them for the specific case, and making a clear
recommendation with the reasoning and the conditions that would change
it. Its core discipline is neutrality: fit the recommendation to the
situation, resist trend-chasing in both directions, and be willing to say
the honest answer is a boring modular monolith.

## Use When

- Use when: choosing the architecture style/paradigm for a new system, or
  reconsidering the style of an existing one.
- Use when: a team is debating monolith vs microservices vs event-driven
  vs serverless and needs a fit-based, not fashion-based, recommendation.
- Use when: an architecture feels wrong for the team's size/maturity (a
  distributed monolith, or a monolith a large org has outgrown).
- Use when: someone asks "should we do microservices?" and the honest
  answer needs the need interviewed first.
- Do NOT use when: the style is already decided and the task is the
  concrete target architecture — component/dependency map, data
  ownership, migration plan — that is `architecture-designer`.
- Do NOT use when: the decision is cloud provider/posture (which cloud,
  managed vs self-hosted) — that is `cloud-architecture-decider` (a
  different axis: where it runs, not what style).
- Do NOT use when: the task is multi-tenant TENANCY structure (silo/pool,
  tenant isolation model) — that is `saas-platform-architect`.
- Do NOT use when: the task is modeling the domain's concepts/entities/
  boundaries — that is `domain-modeler` (which can INFORM style but is a
  different job).

## Inputs to Inspect

1. The need, interviewed (not assumed): the domain and problem, the
   load/traffic shape, and the change/scaling expectations over a
   realistic horizon.
2. The team: size, number of teams, and operational maturity — the single
   biggest determinant of whether a distributed style is survivable.
3. Constraints: deployment/hosting constraints, latency and consistency
   needs, compliance/residency, and the existing estate if this is a
   migration.
4. The real driver: whether the pressure for a style change is a genuine
   scaling/organizational need or a resume/fashion pull — named honestly.
5. Existing pain: what specifically hurts today (deploy coupling, scaling
   bottleneck, team contention) that a style change would or wouldn't fix.

## Workflow

1. **Interview the need FIRST — do not advise before you understand.**
   Domain, load/traffic shape, team size and operational maturity,
   deployment constraints, scaling and change expectations, consistency/
   latency needs. If these aren't known, gathering them IS the task;
   recommending a style before understanding the need is the failure this
   skill exists to prevent.
2. **Select only the genuinely relevant candidates.** From monolith,
   modular monolith, microservices, event-driven, serverless, SOA, and
   hybrids — present the two-to-four that actually fit this situation, not
   a survey of all of them. A textbook dump is not advice.
3. **Weigh each FOR THIS CASE.** Pros and cons tied to the interviewed
   constraints — this team's maturity, this traffic shape, this
   consistency need — not generic bullet points anyone could copy. The
   operational cost of distribution is weighed against this org's ability
   to pay it.
4. **Make a clear recommendation with reasoning.** One recommended style
   (or hybrid), with the argument for it grounded in the need. Advice that
   won't commit to a recommendation is just a menu.
5. **State the sensitivity — what would change it.** The conditions under
   which the recommendation flips ("if the team splits into four and
   traffic 10×es, revisit toward services"; "if you need independent
   scaling of X only, carve out just that"). This makes the decision
   robust and revisitable.
6. **Hold the neutrality line.** Resist trend-chasing in BOTH directions:
   don't default to microservices because it's fashionable, nor to
   monolith because it's contrarian-safe. Name the microservices
   operational premium and the distributed-monolith anti-pattern honestly;
   when the answer is a boring modular monolith, say so plainly.
7. **Name the handoffs.** Once the style is chosen, the concrete
   architecture and migration are `architecture-designer`'s; cloud posture
   is `cloud-architecture-decider`'s; tenancy is `saas-platform-architect`'s;
   domain modeling is `domain-modeler`'s.
8. **Deliver** the style advisory in the Output Format — need summary,
   relevant candidates, case-specific tradeoffs, the recommendation, and
   its sensitivity.

The style comparison (fit factors per style), the interview checklist,
and the trend-trap / distributed-monolith warnings:
[references/architecture-style-sheet.md](references/architecture-style-sheet.md).

## Output Format

```
ARCHITECTURE STYLE ADVISORY — <system>
Need (interviewed): domain · load/traffic shape · team size + ops maturity ·
                    deployment constraints · scaling/change expectations · consistency/latency
Relevant candidates: <only the 2–4 that fit> (not a textbook dump)
Per candidate (THIS case): pros / cons tied to the interviewed constraints
RECOMMENDATION:      <style/hybrid> — reasoning grounded in the need
Sensitivity:         what would change it (team growth, traffic, isolation need, ...)
Neutrality note:     trend-trap resisted both ways; distributed-monolith risk flagged if relevant
Handoffs:            concrete architecture + migration → architecture-designer;
                     cloud posture → cloud-architecture-decider; tenancy →
                     saas-platform-architect; domain → domain-modeler
```

## Validation Checklist

- [ ] The need was interviewed (domain, load, team size + ops maturity,
      constraints, scaling/change, consistency/latency) BEFORE any
      recommendation.
- [ ] Only genuinely relevant candidate styles are presented, not all of
      them.
- [ ] Tradeoffs are specific to THIS case, tied to the interviewed
      constraints — not generic.
- [ ] There is a clear recommendation WITH reasoning, not just a menu.
- [ ] The sensitivity (what would change the recommendation) is stated.
- [ ] Trend-chasing is resisted in both directions; a boring modular
      monolith is recommended when it fits, and said plainly.
- [ ] The distributed-monolith / microservices-premium risks are named
      where relevant.
- [ ] Concrete architecture, cloud posture, tenancy, and domain modeling
      are handed to their owning skills.

## Gotchas

- Recommending a style before interviewing the need is the whole failure
  mode. "Should we do microservices?" has no answer until you know the
  team's size and maturity, the traffic, and what actually hurts today.
- Microservices have a large, permanent operational premium — distributed
  tracing, network failure handling, deployment orchestration, data
  consistency across services. A team that can't pay it gets a distributed
  monolith: all the cost, none of the independence.
- The distributed monolith is the most common bad outcome: services split
  physically but coupled logically, so every change touches several and
  nothing deploys independently. It's worse than the monolith it replaced.
- Contrarian trend-avoidance is still trend-following: refusing
  microservices reflexively is as unprincipled as adopting them
  reflexively. Fit to the situation, not to a stance.
- The modular monolith is the right answer more often than the discourse
  suggests — a well-modularized single deployable gives most of the
  boundary benefits without the distribution tax, and can be split later
  where evidence demands. Be willing to recommend the boring option.
- A recommendation with no sensitivity is brittle: state what would change
  it, so the team knows when to revisit rather than treating the style as
  permanent.
- Advising the style is not designing the architecture. Once the style is
  chosen, the component map and migration are `architecture-designer`'s.

## Stop Conditions

- The style is already decided and the task is the concrete architecture/
  migration → route to `architecture-designer`.
- The decision is cloud provider/posture, tenancy structure, or domain
  modeling → route to `cloud-architecture-decider`, `saas-platform-architect`,
  or `domain-modeler` respectively.
- The need can't be interviewed (domain, load, team, constraints unknown)
  → gather it first; do not issue a style recommendation on assumptions —
  that reproduces the fashion-driven failure.
- The pressure for a style change is purely fashion/resume-driven with no
  supporting need → surface that honestly and recommend against the change
  rather than rationalizing it.

## Supporting Files

- [references/architecture-style-sheet.md](references/architecture-style-sheet.md)
  — the per-style fit factors, the need-interview checklist, and the
  trend-trap / distributed-monolith / microservices-premium warnings.
- `evals/evals.json` — behavior cases including the interview-first
  discipline, the boring-modular-monolith recommendation, and the
  distributed-monolith warning.
- `evals/trigger-evals.json` — discrimination against `architecture-designer`
  (concrete architecture), `cloud-architecture-decider` (cloud posture),
  `saas-platform-architect` (tenancy), and `domain-modeler` (domain).
