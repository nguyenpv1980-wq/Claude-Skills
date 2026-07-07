---
name: principal-code-analyst
description: Produce a principal-level analysis of a subsystem or codebase area that connects code-level findings upward to architecture, data ownership, security posture, tenant isolation, reliability, performance, operating cost, and maintainability — and outputs an executive summary, architecture map, risk register with evidence, tradeoffs, a small-step remediation sequence, and a validation plan. Use when asked for a strategic or "principal-level" read on a subsystem, why an area is slow/fragile/expensive to change, what to fix first with limited budget, or for technical due-diligence on a component. Do NOT use for merge-gating a single diff (code-reviewer), whole-repo inventory audits (full-codebase-auditor), or diagnosing one active failure (systematic-debugger).
---

# Principal Code Analyst

## Purpose

Answer the question a senior leader actually asks — "what is wrong here, what
does it cost us, and what do we fix first?" — by reading the code like an
engineer and reporting like a principal. Line-level observations are only
admitted when they ladder up to a systemic claim about architecture, risk, or
cost; the deliverable is a prioritized, evidence-backed remediation sequence
in small steps, each independently valuable, with a way to verify each step
worked.

## Use When

- Use when: asked for a principal-level / strategic / health assessment of a
  subsystem, service, or code area.
- Use when: a symptom is organizational — "every change here takes weeks,"
  "we're afraid to touch it," "cloud bill keeps climbing" — and the cause is
  suspected to live in the code and its structure.
- Use when: technical due diligence on a component (inherited, acquired,
  contractor-built) scoped narrower than the whole repo.
- Do NOT use when: one diff needs a merge verdict — `code-reviewer`.
- Do NOT use when: the scope is the entire repository inventory-first —
  `full-codebase-auditor` (this skill can consume its output).
- Do NOT use when: one concrete failure is being chased — `systematic-debugger`.
- Do NOT use when: the ask is to apply fixes — analysis hands off to scoped
  implementation tasks.

## Inputs to Inspect

1. The subsystem's code: entry points, core flows, boundaries with the rest
   of the system — read the top 2–3 flows end to end, not just file skims.
2. Change history: hotspot files (`git log` churn), bugfix density, authorship
   concentration (bus factor), recent incident/PR themes.
3. Data layer: schemas, ownership, migrations, query patterns of the hot
   flows — plus who else reads/writes the same data.
4. Tests: what is pinned, what is theater, coverage over the money paths.
5. Operational reality where available: incident notes, slow-query lists,
   error rates, infra cost drivers attributable to this code.
6. Constraints from the human: budget, team size, deadlines, appetite for
   change — priorities are meaningless without them.

## Workflow

1. **Fix the scope and the question.** Which subsystem, and what decision
   will this analysis feed (invest/rewrite/refactor/staff)? Write it down;
   the analysis answers it and nothing else.
2. **Map the architecture as-is:** components, dependency directions, data
   ownership, integration points — from code, with drift-vs-docs noted.
3. **Read the top flows end to end** (request → persistence → response;
   job → effect). Collect code-level findings ONLY as evidence: each must
   support a systemic claim or be dropped as noise.
4. **Ladder findings upward.** For each: which architectural property does it
   damage (coupling, ownership, isolation), which risk does it create
   (security, reliability, data), and what does it cost (incidents, slow
   delivery, infra spend, hiring drag)? A finding that ladders to nothing is
   a nit, not a strategic finding.
5. **Build the risk register:** severity × likelihood, blast radius, with
   file:line or history evidence per entry. Confirmed vs suspected marked.
6. **Name the tradeoffs honestly** — what the current design gets RIGHT and
   what any remediation would sacrifice (speed, simplicity, familiarity).
7. **Sequence remediation in small steps:** ordered by risk-reduction per
   unit of effort; each step independently shippable and valuable even if the
   sequence stops after it. "Rewrite it" is a last resort with its own
   justification burden.
8. **Attach the validation plan:** per step, the observable signal that it
   worked (test added, metric moved, incident class gone, change lead-time
   dropped).

## Output Format

```
PRINCIPAL ANALYSIS — <subsystem> (question: <decision this feeds>)
Executive summary: <≤5 sentences: state, top risks, recommended sequence>
Architecture map (as-is): <components, dep directions, data ownership;
  drift vs docs>
What this design gets right: <honest credits>
Risk register:
  R1 [confirmed|suspected] <systemic claim> — evidence <file:line / history /
     metric> — impact <security|reliability|cost|delivery> — blast radius
Tradeoffs: <what remediation sacrifices>
Remediation sequence: <step → effort → risk reduced → independent value>
Validation plan: <step → observable success signal>
Not analyzed: <exclusions + why>
```

## Validation Checklist

- [ ] The decision the analysis feeds is stated and answered.
- [ ] Every register entry ladders a code observation to a systemic claim
      with evidence; orphan nits were dropped or footnoted.
- [ ] Confirmed vs suspected marked on every risk.
- [ ] At least one "gets right" credit — an analysis with zero credits has
      not understood the design's constraints.
- [ ] Remediation steps are individually shippable and ordered by
      risk-reduction per effort, not by annoyance.
- [ ] Each step has an observable success signal.
- [ ] No fixes applied; scope exclusions stated.

## Gotchas

- Churn × complexity is where the bodies are: a stable ugly file is cheaper
  than a pretty file that changes weekly — prioritize by history, not gut.
- Unfamiliar ≠ wrong: a pattern the analyst dislikes but the team executes
  consistently is a convention, not a finding.
- The million-dollar findings are often boring: no index on the hot query,
  no timeout on the flaky vendor call, one table written by three services.
- Rewrite recommendations feel decisive and usually transfer risk rather
  than reduce it; the burden of proof sits on the rewrite, not the refactor.
- Cost claims need a mechanism ("N+1 on the dashboard × 40k daily loads ≈ 
  the RDS spike"), not adjectives ("expensive").
- Analysis paralysis is a failure mode too: time-box, mark suspected risks
  as suspected, and ship the register.

## Stop Conditions

- Scope creeps from a subsystem toward the whole repo → stop; that is
  `full-codebase-auditor`, run it and consume its inventory.
- A live security vulnerability or active data-integrity failure is found →
  pause analysis and surface immediately via `human-approval-boundary` — 
  a report deadline never queues behind an active leak.
- The decision the analysis should feed cannot be extracted from the human →
  deliver a bounded health snapshot but say the prioritization is provisional
  without constraints.
- Needed evidence (metrics, incident history) is inaccessible → mark affected
  risks suspected; do not fabricate operational impact.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `code-reviewer`,
  `code-simplifier`, and `full-codebase-auditor` (review/audit cluster).
