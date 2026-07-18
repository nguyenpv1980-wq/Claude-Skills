---
name: compliance-gap-auditor
description: 'Run ONE parameterized compliance gap audit — current state vs the chosen framework(s): ISO 27001:2022, ISO 42001:2023, SOC 2 (TSC), optionally a NIST AI RMF profile — never a per-framework fork. Consumes the compliance-control-foundation catalog, multi-framework-crosswalk rows, the SoA, and compliance-evidence-collector coverage; verdicts per requirement: MET / PARTIAL / GAP / UNVERIFIABLE from cited evidence — missing evidence is never MET (agent-governance-audit discipline, org-wide). Output: remediation order — engagement blockers first (mandatory ISO artifacts, SoA, window feasibility), then control gaps, then evidence gaps. A readiness assessment, never an audit opinion — CPAs examine SOC 2, accredited bodies certify ISO. Use for where-do-we-stand against a framework, pre-audit readiness, or drift after material change. Do NOT use for one change''s process compliance (agent-governance-audit), whole-repo code health (full-codebase-auditor), or designing the target systems (the projections).'
---

# Compliance Gap Auditor

## Purpose

Answer "where do we actually stand against the framework(s) we chose, and
what do we fix first" — as one parameterized audit, not three parallel
ones. The auditor walks the chosen framework's requirements against what
verifiably exists (the `compliance-control-foundation` catalog with
statuses, `multi-framework-crosswalk` rows and their PARTIAL residues, the
SoA, `compliance-evidence-collector` coverage, and the underlying shipped
artifacts) and files a verdict per requirement: MET with cited evidence,
PARTIAL with the residue, GAP, or UNVERIFIABLE — and missing evidence is
never MET, the same discipline `agent-governance-audit` applies to one
change, applied org-wide. The output is a remediation order a human can
execute: blockers that stop the audit/certification cold first, control
gaps second, evidence gaps third. This is readiness assessment; it never
issues or simulates an audit opinion.

## Use When

- Use when: asked "how far are we from ISO 27001 / SOC 2 / ISO 42001
  readiness?", "what's missing before we book the audit?", or for a gap
  assessment against any subset of the supported frameworks.
- Use when: something material changed (architecture, vendor, AI system,
  team) and compliance drift needs re-assessment.
- Use when: prioritizing remediation across frameworks — what to fix
  first when 27001 and SOC 2 deadlines compete.
- Do NOT use when: auditing whether ONE change/PR followed governance
  process — `agent-governance-audit` (per-change, primary evidence).
- Do NOT use when: auditing whole-repo code health/debt —
  `full-codebase-auditor`.
- Do NOT use when: designing the management system, scoping the
  engagement, or building the evidence program — the projections,
  `soc2-trust-criteria-mapper`, and `compliance-evidence-collector`
  design; this skill measures against their designs.

## Inputs to Inspect

1. **Parameters:** which framework(s) to audit against (any subset:
   27001, 42001, SOC 2, + AI RMF profile), and the target event/date
   (stage 1 audit, Type 2 window start, surveillance).
2. The framework requirement source in hand: licensed clause/Annex A
   text, TSC text, AI RMF Core — requirements audited without their text
   in hand are automatically UNVERIFIABLE, not improvised.
3. Current-state artifacts: the foundation catalog (statuses), crosswalk
   rows (satisfaction levels + verification status), SoA (if any),
   evidence coverage matrix, and management-system artifacts (risk
   register, internal audit reports, management review minutes, impact
   assessments).
4. The underlying shipped-artifact reality for spot verification: does
   the mechanism the catalog claims actually exist and run (the same
   don't-trust-self-claims posture `agent-governance-audit` takes toward
   closeouts).
5. Prior gap audits — deltas matter more than re-derivation.

## Workflow

1. **Fix parameters.** Framework(s), edition pins, target date, and scope
   (org/system boundary). No framework chosen → Stop Conditions.
2. **Assemble the requirement list** from the texts in hand: management-
   system clauses (ISO), Annex A applicability per the SoA (ISO), TSC
   criteria for the scoped categories (SOC 2), RMF
   functions/categories (profile). Requirements without text in hand →
   UNVERIFIABLE with "text not in hand" noted.
3. **Walk requirements against current state.** Per requirement, cite the
   evidence: catalog control + status, crosswalk cell (+ verification
   status), evidence coverage, or the artifact itself. Spot-verify
   load-bearing claims — a catalog row saying "implemented" with no
   locatable mechanism is a finding about the catalog AND a gap.
4. **File verdicts.** MET (cited, verified evidence) / PARTIAL (residue
   named — crosswalk PARTIALs land here) / GAP (nothing satisfies it) /
   UNVERIFIABLE (cannot be checked from available inputs — never
   silently upgraded). Missing evidence is never MET.
5. **Classify gaps by blocking power.**
   - **Blockers:** things that stop the engagement cold — missing
     mandatory ISO management-system artifacts (risk register, SoA,
     internal audit, management review), SOC 2 window infeasibility,
     unscoped system boundary.
   - **Control gaps:** required/selected controls with no mechanism —
     each routed to its owning shipped skill (via the foundation) or
     named as net-new with an owner.
   - **Evidence gaps:** mechanism exists, proof doesn't —
     routed to `compliance-evidence-collector`.
6. **Order remediation.** Blockers → control gaps on the critical path of
   the target date → evidence gaps that need lead time (windows accrue,
   they can't be rushed) → the rest. Cross-framework: fix shared
   (crosswalk-mapped) gaps once, first — that's the do-the-work-once
   payoff.
7. **Report** with per-requirement verdicts, the ordered remediation
   list (owner + owning skill per item), UNVERIFIABLE backlog, and the
   explicit non-opinion disclaimer.

## Output Format

```
COMPLIANCE GAP AUDIT — <org/system>
Parameters: frameworks <27001 [+Amd1] | 42001 | SOC 2 (categories) | +AI RMF profile> | target <event/date> | editions pinned
Requirement sources in hand: <which texts; absent text ⇒ UNVERIFIABLE>
Verdicts (per requirement):
  <req id/name> — MET (evidence: <cited>) | PARTIAL (<residue>) | GAP | UNVERIFIABLE (<why>)
Summary: MET <n> | PARTIAL <n> | GAP <n> | UNVERIFIABLE <n>  (per framework)
Remediation order:
  1. BLOCKERS: <item → owner → owning skill → needed by>
  2. CONTROL GAPS: <item → owner → owning skill (via compliance-control-foundation)>
  3. EVIDENCE GAPS: <item → compliance-evidence-collector → lead time>
  4. Remainder
Shared-gap dividend: <gaps closing multiple frameworks at once (crosswalk-mapped)>
Catalog corrections: <claimed-but-unfound mechanisms — status downgrades to propose>
Disclaimer: readiness assessment — not an audit opinion; CPAs examine SOC 2, accredited bodies certify ISO.
```

## Validation Checklist

- [ ] Parameters (frameworks, editions, target, scope) recorded before any
      verdict.
- [ ] Every verdict cites evidence or is UNVERIFIABLE; zero MET verdicts
      on missing/unlocatable evidence.
- [ ] Requirements without framework text in hand filed UNVERIFIABLE —
      none improvised from memory.
- [ ] Load-bearing catalog claims spot-verified; unfound mechanisms
      produce both a gap and a catalog-correction proposal.
- [ ] Every gap carries an owner and an owning skill; evidence gaps carry
      lead-time notes.
- [ ] Remediation order puts engagement blockers first and names the
      shared-gap dividend across frameworks.
- [ ] The non-opinion disclaimer is present verbatim in the report.

## Compliance Precision Rules

- This skill produces a **readiness assessment**, never an audit opinion:
  SOC 2 is an AICPA **attestation** issued by an independent CPA; ISO
  27001/42001 certification is decided by an accredited body. "You will
  pass" is never in the vocabulary.
- Requirements are audited only from framework text in hand; public
  summaries of Annex A (27001 counts secondary-sourced, 42001 counts
  conflicting) are not requirement sources.
- Cross-framework dividend claims come from the org's own crosswalk rows,
  not the ~60–80% industry overlap estimate.
- UNVERIFIABLE is a first-class verdict — the pressure to convert it to
  MET before an audit date is precisely the failure this skill exists to
  resist.

## Gotchas

- Self-assessment optimism is the default failure: catalogs say
  "implemented," closeouts say "done." Spot-verify like
  `agent-governance-audit` does — the mechanism must be locatable and
  running.
- Evidence gaps have physics: a Type 2 window or a year of access-review
  records cannot be remediated in a sprint. Surface lead times early or
  the remediation order lies.
- The blocker class is small but absolute: no risk register, no SoA, no
  internal audit, no management review = no ISO certification regardless
  of technical excellence. Don't let a long tail of control gaps bury
  four blockers.
- Framework text drift: auditing 27001 against a 2013-era checklist (or
  42001 against a blog summary) produces confident wrong verdicts —
  pin editions and require text in hand.
- Double-counting across frameworks inflates effort: crosswalk-mapped
  shared gaps are ONE remediation. Un-mapped duplicates in the gap list
  mean the crosswalk needs rows, which is itself a finding.
- A gap audit that changes the catalog silently is overreach — catalog
  corrections are proposals routed back to
  `compliance-control-foundation`'s owner.

## Stop Conditions

- No framework parameter can be established — stop and ask; "audit our
  compliance" without a target framework is unanswerable.
- No current-state inputs exist at all (no catalog, no artifacts) — run
  `compliance-control-foundation` first; a gap audit against nothing is
  just the framework's table of contents.
- Asked to issue, simulate, or pre-write an audit opinion, certification
  statement, or attestation language — refuse; readiness assessment
  only.
- Asked to upgrade UNVERIFIABLE/GAP verdicts on assurance ("it's
  basically done") — refuse; verdicts move on evidence.
- The audit surfaces an actively exploited control failure (not just a
  gap) — route to `incident-response-runbook`; compliance reporting
  resumes after containment.

## Supporting Files

- None — self-contained by design: the requirement sources are the
  framework texts in hand, and the current-state sources are the other
  compliance-cluster artifacts (`compliance-control-foundation`,
  `multi-framework-crosswalk`, `statement-of-applicability-author`,
  `compliance-evidence-collector` outputs).
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance
  cluster and against `agent-governance-audit` and
  `full-codebase-auditor`.
