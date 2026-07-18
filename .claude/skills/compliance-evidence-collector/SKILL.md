---
name: compliance-evidence-collector
description: 'Design the operating-effectiveness evidence program SOC 2 Type 2 demands and ISO surveillance audits reuse — evidence OVER TIME, not point-in-time. Per control (from compliance-control-foundation): evidence type, cadence matched to control operating frequency, population for auditor sampling, named collector, retention, and audit-window coverage with a hole map. Formalizes the Phase 5 evidence pack (screenshot-evidence-planner, manual-test-case-creator), audit-log-architect trails, and agent-governance-audit reports into auditor-consumable registers. Design and coverage audit only — never mutates a live evidence store. Use when planning a Type 2 window or ISO surveillance cycle, asked how to collect and retain compliance evidence, or when evidence cannot cover a period. Do NOT use for QA evidence policy (screenshot-evidence-planner), audit-log design (audit-log-architect), one change''s process evidence (agent-governance-audit), or readiness gaps (compliance-gap-auditor).'
---

# Compliance Evidence Collector

## Purpose

Turn "we have controls" into "we can prove the controls operated across the
whole period." SOC 2 Type 2 examines operating effectiveness over an audit
window, and ISO surveillance audits re-check an operating management system
— both die on evidence holes: a control with no artifact for March is a
finding even if it ran perfectly. This skill produces the evidence program:
per-control evidence specs (type, cadence, population, collector, retention,
integrity), the register that accrues them, and a window-coverage audit that
exposes holes before an auditor does. It formalizes what already exists —
the Phase 5 evidence pack, `audit-log-architect` trails, CI results,
`agent-governance-audit` reports — rather than inventing a parallel evidence
world. It designs and audits coverage; it never mutates a live evidence
store.

## Use When

- Use when: planning a SOC 2 Type 2 audit window or an ISO 27001/42001
  surveillance/recertification cycle and evidence must cover the period.
- Use when: asked what evidence to collect for compliance controls, at what
  cadence, with what retention — or to build an evidence register.
- Use when: evidence exists ad hoc (screenshots, tickets, CI runs) but
  nobody can show continuous coverage for a window.
- Do NOT use when: defining screenshot naming/masking/storage policy for QA
  — `screenshot-evidence-planner` (this skill consumes that policy).
- Do NOT use when: designing the audit trail itself —
  `audit-log-architect`; or auditing ONE change's process evidence —
  `agent-governance-audit` (its reports are inputs here).
- Do NOT use when: assessing which controls/artifacts are missing overall —
  `compliance-gap-auditor` (it consumes this skill's coverage output).

## Inputs to Inspect

1. The control catalog with evidence hooks (`compliance-control-foundation`)
   — every evidence spec traces to a control; no control, no spec.
2. The target window: Type 2 period or ISO surveillance cycle, from
   `soc2-trust-criteria-mapper` / the ISO projections.
3. Existing evidence sources: screenshot evidence policy
   (`screenshot-evidence-planner`), manual test cases and results
   (`manual-test-case-creator`), audit-log extracts (`audit-log-architect`),
   CI/validator runs, review records, `agent-governance-audit` reports,
   closeouts (`ai-closeout-reporter`), access-review and management-review
   minutes where they exist.
4. Where evidence currently lives (repos, ticket systems, drive folders),
   who can write there, and whether anything is immutable.
5. Control operating frequency — continuous (logging), per-change (review),
   periodic (access review, backup restore test) — cadence derives from it.

## Workflow

1. **Fix the window.** Start/end dates of the audit period or surveillance
   cycle. No window and no control catalog → Stop Conditions.
2. **Spec evidence per control** using
   [references/evidence-cadence-catalog.md](references/evidence-cadence-catalog.md).
   For each catalog control: evidence type (system config, log extract,
   screenshot, ticket, review minutes, test run, signed approval), source
   system, cadence matched to operating frequency, named collector, and
   the population it belongs to.
3. **Define populations for sampling.** Auditors sample from populations
   ("all production changes in the window", "all access reviews"). Each
   evidence spec names its population and how the complete population is
   enumerated (e.g. merged-PR list, audit-log query) — evidence that can't
   be tied to a complete population invites "how do we know this is all of
   them?"
4. **Reuse existing artifacts.** Map each spec to what already accrues:
   PR reviews, CI runs, validator output, screenshot evidence per the
   Phase 5 policy, audit-log extracts, governance-audit reports. Net-new
   collection is the exception and gets a named owner.
5. **Set retention and integrity.** Retention at least covering
   window + audit completion (typically longer per contract/policy);
   evidence write path, who can modify/delete, and tamper posture — an
   editable folder of screenshots is weak evidence; prefer append-only or
   versioned storage. Personal/tenant data inside evidence follows
   `screenshot-evidence-planner` masking before storage.
6. **Audit window coverage.** Build the control × window matrix from what
   the register ACTUALLY holds: covered / partial / hole per control per
   interval. Holes get either remediable collection now (if the artifact
   still exists at source) or an honest carried exception — never
   backfilled fabrication.
7. **Hand off.** Register design + coverage map → `compliance-gap-auditor`
   (evidence gaps), projections (audit prep), `soc2-trust-criteria-mapper`
   (window feasibility). Store changes (creating buckets, moving files,
   permissions) are proposals for a human operator — this skill never
   executes them.

## Output Format

```
EVIDENCE PROGRAM — <org/system>, window <start>–<end>
Per control (from compliance-control-foundation):
  [CC-<id>] <control>
    Evidence: <type> from <source system>
    Cadence: <continuous | per-change | monthly | quarterly | annual> (matches operating frequency: <freq>)
    Population: <definition + how enumerated completely>
    Collector: <named human/automation> | Retention: <duration> | Integrity: <append-only|versioned|weak — flagged>
    Reuses: <existing artifact (screenshot policy | audit log | CI | governance audit | ...) or NET-NEW>
Coverage matrix: <control × interval → covered | partial | HOLE>
Holes: <control, interval → recoverable-at-source | carried exception (owner)>
Store-change proposals (human-executed): <none | list>
Never claimed: that evidence "passes" an audit — the examiner/auditor decides.
```

## Validation Checklist

- [ ] Every evidence spec traces to a catalog control; no orphan evidence,
      no evidence-less control without an explicit flag.
- [ ] Cadence per spec matches the control's operating frequency; a
      quarterly artifact for a continuous control is flagged.
- [ ] Every spec defines its population and complete enumeration method.
- [ ] Existing artifacts reused where they exist; net-new collection has a
      named owner.
- [ ] Retention covers window + audit completion; integrity posture stated
      per store, weak stores flagged.
- [ ] Coverage matrix built from actual register contents; holes listed
      with recover-or-except disposition — never silently backfilled.
- [ ] No live evidence store was written to or reorganized.

## Compliance Precision Rules

- SOC 2 is an AICPA **attestation** — a CPA's examination, never a
  "certification." Type 2 = design + **operating effectiveness over a
  period**; Type 1 = design as of a date. These Type definitions come from
  CPA-firm sources, not AICPA's fetchable pages — verify against the AICPA
  SOC 2 guide before citing them in customer-facing text.
- Evidence coverage is a fact claim about the register; "we will pass the
  audit" is never a claim this skill makes.
- ISO surveillance reuse is a design goal of this program, not an ISO
  requirement citation — verify surveillance expectations with the chosen
  certification body.

## Gotchas

- Point-in-time thinking is the classic Type 2 failure: a beautiful
  screenshot from audit-prep week proves nothing about February. Cadence
  and window coverage are the whole game.
- Populations beat samples: auditors pick the sample; you must produce the
  complete population. A hand-curated "evidence folder" without population
  enumeration reads as cherry-picking.
- Evidence rot: screenshots without metadata (build, env, date — the
  `screenshot-evidence-planner` rules) or logs without retention quietly
  expire mid-window. Retention shorter than the window is a pre-booked
  hole.
- Backfill temptation: recreating "March evidence" in July from memory is
  fabrication. If the source system still holds the artifact, extract it
  (dated honestly); otherwise carry the exception.
- Editable stores: anyone-can-edit drive folders undermine integrity.
  Flag them; prefer versioned/append-only.
- Over-collection is real: evidence nobody specified burdens collectors
  and dilutes reviews. Specs come from controls, not enthusiasm.

## Stop Conditions

- No control catalog exists — run `compliance-control-foundation` first;
  evidence without controls is a folder of screenshots.
- No audit window or cycle can be stated — stop; cadence and coverage are
  undefined without a period.
- Asked to write into, reorganize, or delete from a live evidence store —
  propose the change for a human operator (`human-approval-boundary`);
  never execute it.
- Asked to fill a coverage hole with reconstructed/backdated artifacts —
  refuse; offer source-system extraction or a carried exception.
- Evidence would contain unmasked personal/tenant data — apply the
  `screenshot-evidence-planner` masking policy before storage or stop.

## Supporting Files

- [references/evidence-cadence-catalog.md](references/evidence-cadence-catalog.md)
  — evidence types, cadence-by-operating-frequency table, population
  patterns, retention/integrity postures, and reuse map to shipped
  artifacts.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance cluster
  and against `screenshot-evidence-planner`, `audit-log-architect`, and
  `agent-governance-audit`.
