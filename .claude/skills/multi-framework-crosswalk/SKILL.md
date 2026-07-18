---
name: multi-framework-crosswalk
description: 'Maintain the control crosswalk — the do-the-work-once engine between compliance-control-foundation and the framework projections: one row per control mapping it to ISO 27001:2022 Annex A, SOC 2 TSC, and ISO 42001:2023 Annex A references, plus optionally its NIST AI RMF function — with edition pinning and FULL/PARTIAL satisfaction honesty. Published crosswalks put cross-framework overlap at roughly 60–80% — an industry estimate, never a standard-derived figure. Every cell is a CLAIM verified against framework text in hand; rows are never filled from memory — unverified cells stay marked unverified. Use when mapping one control set to multiple frameworks, deduplicating compliance work across 27001/42001/SOC 2, or answering which frameworks a control satisfies. Do NOT use to define controls (compliance-control-foundation), decide applicability (statement-of-applicability-author), scope engagements (soc2-trust-criteria-mapper), or assess gaps (compliance-gap-auditor).'
---

# Multi-Framework Crosswalk

## Purpose

Make "write the control once, satisfy every framework" real. The crosswalk
holds one row per `compliance-control-foundation` control, mapping it to
its ISO 27001:2022 Annex A reference, SOC 2 TSC reference, ISO 42001:2023
Annex A reference, and — for AI controls — the NIST AI RMF function it
serves. It is the engine the projections consume (so the ISMS, AIMS, and
SOC 2 mapping never fork the control set) and the honest ledger of where
overlap actually holds: a row states FULL or PARTIAL satisfaction per
framework, because "roughly maps" is how orgs discover mid-audit that one
control satisfied a third of a criterion. Reference integrity is the whole
value: every cell is a claim against a pinned framework edition, verified
against the text in hand or marked unverified.

## Use When

- Use when: mapping an existing control set to multiple frameworks
  (27001 + SOC 2, adding 42001, + AI RMF) to avoid duplicate work.
- Use when: asked "which frameworks does this control satisfy?" or "what
  else does our 27001 work buy us?"
- Use when: a framework edition changes and the mapping layer must be
  re-verified without touching the control catalog.
- Do NOT use when: defining or cataloging the controls themselves —
  `compliance-control-foundation` (rows point at its IDs).
- Do NOT use when: deciding per-control applicability for ISO — that
  judgment (with 6.1.3 trace) is `statement-of-applicability-author`; the
  crosswalk records references, not applicability.
- Do NOT use when: scoping an engagement (`soc2-trust-criteria-mapper`,
  the ISO architects) or assessing readiness (`compliance-gap-auditor`).

## Inputs to Inspect

1. The `compliance-control-foundation` catalog — the row keys; no catalog,
   no crosswalk.
2. The framework reference texts in hand, edition-pinned: ISO/IEC
   27001:2022 Annex A table, ISO/IEC 42001:2023 Annex A table, the TSC
   (2017, revised Points of Focus 2022), NIST AI RMF 1.0 Core. What is not
   in hand cannot fill cells.
3. Existing crosswalk rows (if any) and their verification status —
   maintenance beats rewrite.
4. The projections' consumption points: which skills read which columns
   (`iso-27001-isms-architect`, `iso-42001-aims-architect`,
   `soc2-trust-criteria-mapper`, `ai-lifecycle-risk-manager`), so column
   changes don't silently break them.

## Workflow

1. **Pin editions.** Record the exact edition/version per framework column
   (27001:2022 [+Amd 1:2024], 42001:2023, TSC 2017 w/ 2022 PoF, AI RMF
   1.0). A crosswalk without pinned editions is unmaintainable — edition
   drift invalidates cells silently.
2. **Establish the row shape** from
   [assets/crosswalk-row-template.md](assets/crosswalk-row-template.md):
   control ID → per-framework reference + satisfaction level
   (FULL / PARTIAL <residue> / NONE) + verification status
   (verified-against-text / unverified).
3. **Fill cells only from text in hand.** Walk each control against each
   available framework table and record the reference(s) it maps to.
   Missing framework text → cells stay `unverified: text not in hand`,
   never guessed. Control IDs recalled from memory are forbidden — this
   is the rule that keeps the crosswalk trustworthy.
4. **Judge satisfaction honestly.** FULL only when the control as
   implemented covers the framework requirement's substance; PARTIAL
   names the residue (e.g. an access-control mechanism that covers
   provisioning but not periodic review). The 60–80% overlap folklore is
   an industry estimate — your rows are the actual number; expect
   AI-specific 42001 objectives and Privacy criteria to map thin.
5. **Mark one-to-many and many-to-one explicitly.** One control may serve
   several references; several controls may jointly satisfy one criterion
   (the joint set is listed together, or the criterion shows PARTIAL per
   contributor).
6. **Version and maintain.** The crosswalk is a maintained artifact:
   changes arrive as diffs (new control, edition change, verification
   upgrade), each re-verifying only affected cells. Edition changes
   re-open every cell in that column — schedule it, don't absorb it
   silently.
7. **Hand off.** Rows → projections (selection and criteria maps), SoA
   author (reference column for included controls), gap auditor
   (satisfaction levels expose thin coverage), evidence collector
   (one artifact can evidence several frameworks via the row).

## Output Format

```
CONTROL CROSSWALK — <org> v<n>
Editions pinned: ISO/IEC 27001:2022 [+Amd 1:2024] | ISO/IEC 42001:2023 | TSC 2017 (rev. PoF 2022) | NIST AI RMF 1.0
Texts in hand: <which framework tables are available; columns without text stay unverified>
Per row:
  [CC-<id>] <control name>
    27001 Annex A: <ref(s) | none> — FULL|PARTIAL(<residue>)|NONE — verified|unverified
    SOC 2 TSC:     <ref(s) | none> — FULL|PARTIAL(<residue>)|NONE — verified|unverified
    42001 Annex A: <ref(s) | none> — FULL|PARTIAL(<residue>)|NONE — verified|unverified
    AI RMF fn:     <GOVERN|MAP|MEASURE|MANAGE | n/a>
Joint satisfactions: <criterion/control-objective ← {control set}>
Coverage summary: <per framework: full/partial/none counts from THIS table — not the 60–80% folklore>
Unverified cells: <list — the verification backlog>
```

## Validation Checklist

- [ ] Every row keys to a foundation control ID; no orphan rows, no
      framework-first rows without a control.
- [ ] Every filled cell was verified against the pinned framework text in
      hand; every unfilled/unavailable cell says `unverified`, not a guess.
- [ ] Satisfaction levels are FULL/PARTIAL/NONE with residue named for
      every PARTIAL.
- [ ] Editions pinned per column; edition changes tracked as re-open
      events, not silent updates.
- [ ] Joint satisfactions listed explicitly; no criterion silently
      "covered" by an unstated set of controls.
- [ ] Coverage summary computed from the table itself; the 60–80% figure
      appears only as flagged industry context, if at all.

## Compliance Precision Rules

- The ~**60–80% cross-framework overlap** figure is an industry crosswalk
  estimate, **not a standard-derived number** — quote it only with that
  flag; your own table is the real figure.
- 27001 Annex A public counts are secondary-sourced; **42001 Annex A
  counts conflict across public sources and are never stated** — cells
  cite entries from the licensed tables only.
- SOC 2 columns reference an AICPA **attestation** framework (TSC
  criteria); never mix certification language into SOC 2 cells.
- A crosswalk row is a mapping claim, not an applicability decision (SoA)
  and not evidence the control operates
  (`compliance-evidence-collector`).

## Gotchas

- Memory-recalled control IDs are the classic crosswalk poison: they look
  authoritative, survive reviews, and fail the audit when the auditor
  opens the real Annex A. Text in hand or `unverified` — no third state.
- Vendor crosswalks (GRC tools, blog matrices) inherit their own edition
  and judgment errors — usable as hints, never as cell sources.
- PARTIAL inflation: marking FULL because "it mostly covers it" defers
  the residue to audit day. The residue list is where gap-auditor value
  lives.
- The 27001→SOC 2 direction feels easy and the 42001 column then gets
  cloned from 27001 — but 42001 Annex A is control OBJECTIVES with
  AI-specific substance; clone-mapping produces confident nonsense.
- Many-to-one hiding: a criterion satisfied by five controls jointly is
  fine — until one control is retired and nobody re-checks the criterion.
  Joint sets must be explicit so retirement re-opens them.
- Crosswalk ≠ catalog: adding "just one framework note" to the foundation
  catalog re-starts the drift this architecture exists to prevent.

## Stop Conditions

- No foundation catalog exists — stop; run
  `compliance-control-foundation` first (framework-first crosswalks
  invert the architecture).
- No framework text is in hand for a requested column — produce the
  column as `unverified` scaffolding and say so; never fill it from
  memory or vendor matrices.
- Asked to decide applicability, scope an engagement, or declare
  compliance from the crosswalk — hand to the SoA author, the scoping
  skills, or the gap auditor respectively.
- A framework edition changed since cells were verified — flag the
  column-wide re-open; do not patch single cells and call the column
  current.

## Supporting Files

- [assets/crosswalk-row-template.md](assets/crosswalk-row-template.md) —
  the row/column template with edition-pinning header, satisfaction
  vocabulary, and verification-status rules.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance
  cluster (crosswalk vs foundation vs SoA vs projections vs gaps).
