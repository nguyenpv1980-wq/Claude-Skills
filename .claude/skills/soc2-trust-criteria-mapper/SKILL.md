---
name: soc2-trust-criteria-mapper
description: 'Scope a SOC 2 engagement — an AICPA ATTESTATION (a CPA''s examination of controls against the Trust Services Criteria), NEVER a certification. Decides the system boundary, which TSC categories the report covers (Security baseline plus optional Availability, Processing Integrity, Confidentiality, Privacy — selected by customer commitments, not ambition), and Type 1 (design as of a date) vs Type 2 (plus operating effectiveness over a period), window planning handed to compliance-evidence-collector. Criteria map to existing controls via compliance-control-foundation and multi-framework-crosswalk. Flags: five categories + ASEC authorship AICPA-verified; Type 1/2 definitions and Security-as-required-baseline are CPA-firm-sourced — verify against the AICPA guide before citing. Use for SOC 2 readiness, category scoping, or the Type 1 vs Type 2 decision. Do NOT use for ISO management systems, the evidence program (compliance-evidence-collector), or readiness gaps (compliance-gap-auditor).'
---

# SOC 2 Trust Criteria Mapper

## Purpose

Scope the SOC 2 engagement correctly before anyone burns a quarter
preparing for the wrong report: what system is being described, which
Trust Services Criteria categories the report covers, and whether the
engagement is Type 1 (control design as of a specified date) or Type 2
(design plus operating effectiveness over a period). SOC 2 is an AICPA
**attestation** — an independent CPA examines and reports; nobody
"certifies" — and the report's scope is driven by what the org has
committed to customers, not by collecting categories. Criteria then map
onto existing mechanisms via `compliance-control-foundation` and
`multi-framework-crosswalk` (the D9 premise: for an org with the shipped
Phase 3/4 packs, much of the Security category exists — the work is
mapping, the system description, and the evidence window). Window
evidence design hands to `compliance-evidence-collector`.

## Use When

- Use when: US enterprise customers/procurement ask for a SOC 2 report and
  the org needs to scope what that takes.
- Use when: deciding which TSC categories to include, or Type 1 vs Type 2
  and how long the review period should be.
- Use when: drafting or reviewing the system description boundary, or
  mapping TSC criteria to existing controls.
- Do NOT use when: building an ISO management system
  (`iso-27001-isms-architect` / `iso-42001-aims-architect`) — different
  regime: certifiable standards, SoA, certification bodies.
- Do NOT use when: designing the evidence-over-time program for the chosen
  window — `compliance-evidence-collector` (this skill decides the window;
  that one covers it).
- Do NOT use when: assessing overall readiness gaps
  (`compliance-gap-auditor`) or designing a technical control (owning
  shipped skill via the foundation).

## Inputs to Inspect

1. Customer commitments and system requirements: contracts, SLAs, DPAs,
   security addenda, marketing claims — category selection derives from
   what was PROMISED (see workflow step 3).
2. The system boundary candidates: which product(s)/service(s),
   infrastructure, and supporting processes the report describes.
3. The `compliance-control-foundation` catalog + crosswalk rows — what
   mechanisms exist to satisfy criteria (Security baseline largely maps to
   the shipped Phase 3/4 packs).
4. Timeline pressure: when customers need a report — drives Type 1 first
   vs straight to Type 2 and the window length.
5. Subservice organizations (cloud provider, key vendors): carve-out vs
   inclusive treatment and complementary controls —
   `supply-chain-security-reviewer` context feeds this.

## Workflow

1. **Confirm the ask.** Who wants the report, for what system, by when.
   No customer-driver and no system named → Stop Conditions.
2. **Draw the system boundary.** The report describes A SYSTEM: services,
   infrastructure, software, people, procedures, data. Too broad
   multiplies evidence; too narrow (excluding the product customers buy)
   fails procurement review. Draft the boundary and the system-description
   skeleton using
   [references/tsc-scoping-map.md](references/tsc-scoping-map.md).
3. **Select categories by commitment.** Security (the common criteria) is
   the baseline engagement scope; add a category only when commitments
   demand it: Availability (SLAs/uptime commitments —
   `slo-reliability-architect` mechanisms), Confidentiality (NDAs,
   confidential-data commitments — `tenant-isolation-reviewer`,
   `secrets-identity-hardener`), Processing Integrity (processing
   completeness/accuracy commitments), Privacy (personal-information
   commitments — `sensitive-disclosure-guard` surface). Record WHY each
   category is in or out; "more categories looks better" is an
   anti-pattern that multiplies criteria and evidence.
4. **Decide Type 1 vs Type 2.** Type 1: design as of a date — faster
   first artifact, weaker assurance; Type 2: operating effectiveness over
   a period — what enterprise procurement usually wants. Common path:
   Type 1 now, Type 2 over the following window, when the timeline
   demands an early artifact; straight to Type 2 when controls have
   already operated. (Definitions are CPA-firm-sourced — see Precision
   Rules.) Window length balances customer expectation vs how long
   controls have actually operated; plan it WITH the CPA firm.
5. **Map criteria to mechanisms.** Per selected category, walk criteria
   against the foundation catalog via `multi-framework-crosswalk`:
   mechanism exists → map + evidence hook; genuine gap → owner + date
   (feeds `compliance-gap-auditor`). Never invent criteria IDs — work
   from the licensed/obtained TSC text.
6. **Handle subservice organizations.** Cloud/hosting and material vendors:
   carve-out (typical) vs inclusive; list complementary subservice-
   organization controls the description must state and customer-entity
   controls where relevant.
7. **Hand off.** Window + category scope → `compliance-evidence-collector`
   (evidence program); gaps → `compliance-gap-auditor`; the engagement
   itself → an independent CPA firm (this skill prepares, it never
   examines).

## Output Format

```
SOC 2 SCOPING — <org/system>
Driver: <customer/procurement ask + deadline>
System boundary: <services, infra, software, people, procedures, data> — description skeleton attached
Categories: Security (baseline) [+ Availability|Processing Integrity|Confidentiality|Privacy]
  Per category: IN/OUT + commitment trace (contract/SLA/DPA ref)
Type decision: Type 1 (date) | Type 2 (window <start>–<end>) + rationale; plan confirmed with CPA firm
Criteria → mechanism map: <criterion → foundation control/mechanism | GAP (owner, date)>
Subservice orgs: <carve-out|inclusive; complementary controls to state>
Handoffs: window → compliance-evidence-collector | gaps → compliance-gap-auditor | examination → independent CPA
Verification items: <claims pending the AICPA guide/TSC text>
Language check: "attestation/examination/report" — never "certification/certified"
```

## Validation Checklist

- [ ] Every included category traces to a named customer commitment;
      every exclusion is recorded with rationale.
- [ ] The system boundary names services, infrastructure, software,
      people, procedures, and data — and includes what customers actually
      buy.
- [ ] Type decision includes rationale and window feasibility (how long
      controls have operated), and is flagged for CPA-firm confirmation.
- [ ] Criteria mapping cites the TSC text in hand; no criteria IDs
      invented from memory.
- [ ] Subservice organizations dispositioned (carve-out/inclusive) with
      complementary controls noted.
- [ ] Zero occurrences of "certified"/"certification" in any SOC 2
      deliverable text.
- [ ] Evidence-window design handed to `compliance-evidence-collector`,
      not duplicated here.

## Compliance Precision Rules

- SOC 2 is an AICPA **attestation** — "Reporting on an Examination of
  Controls at a Service Organization" — performed by an independent CPA.
  ISO 27001/42001 are certifiable standards; SOC 2 is never
  "certification," and this skill's outputs must never say otherwise.
- **Verified on AICPA pages:** the five TSC categories (Security,
  Availability, Processing Integrity, Confidentiality, Privacy) and that
  the TSC are issued by the AICPA Assurance Services Executive Committee
  (2017 TSC with revised Points of Focus, 2022).
- **CPA-firm-sourced — verify against the AICPA SOC 2 guide before
  citing:** the Type 1 ("design as of a specified date") vs Type 2
  ("plus operating effectiveness over a period") definitions and
  "Security is the required common-criteria baseline; the other four are
  scoped per engagement." AICPA's fetchable pages do not define these;
  the defining text is the paywalled guide.
- "SOC 2 is the de-facto US enterprise procurement ask" is positioning,
  not a standards claim — usable in business rationale, not in the
  system description.
- This skill prepares scoping; only the CPA firm examines and reports.

## Gotchas

- Category greed: each added category adds criteria, controls, and
  evidence for the whole window. Scope from commitments; procurement
  rarely rewards Privacy-in-scope when no personal-info commitment
  exists.
- The system description is a deliverable, not paperwork: auditors test
  against it, and Type 2 reports open with it. A boundary that omits the
  actual product or hides material vendors fails review.
- Window arithmetic: a Type 2 window can't start before controls
  actually operated — a January-founded control cannot anchor a
  full-year window ending in June. `compliance-evidence-collector`'s
  coverage matrix is the truth source.
- Carve-out ≠ ignore: carved-out subservice organizations still require
  the description to state complementary controls you rely on (e.g.
  cloud physical security) — and your monitoring of them (vendor
  management domain).
- Report consumers read exceptions: a Type 2 with a hole reads worse
  than a slightly later clean window — surface the tradeoff to the
  human; don't default to "sooner."
- Bridge letters, report refresh cycles, and distribution rules are
  engagement-specific — plan them with the CPA firm, don't assert
  universal rules.

## Stop Conditions

- No system can be named and no customer driver exists — stop; scoping
  without a system or a consumer produces a report nobody accepts.
- Asked to include a category with no commitment basis (or exclude one
  that contracts demand) — surface the mismatch to the human; commitments
  win over preference.
- The TSC text / AICPA guide is unavailable AND criteria-level mapping is
  required — deliver category-level scoping with verification items; do
  not invent criteria.
- Asked to produce or sign the attestation, or to declare the org "SOC 2
  certified/compliant" — refuse the framing: an independent CPA examines
  and reports; this skill prepares.
- The window would start before key controls existed — flag the
  feasibility gap and re-plan with `compliance-evidence-collector`
  instead of proceeding.

## Supporting Files

- [references/tsc-scoping-map.md](references/tsc-scoping-map.md) — the
  category-by-commitment selection table, system-description skeleton,
  Type decision tree, window feasibility test, and subservice-organization
  disposition guide.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance
  cluster (SOC 2 vs ISO projections vs evidence vs gaps) and against
  `slo-reliability-architect`.
