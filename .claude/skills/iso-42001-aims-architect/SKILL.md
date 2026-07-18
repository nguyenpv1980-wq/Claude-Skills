---
name: iso-42001-aims-architect
description: 'Design ISO/IEC 42001:2023 certification readiness — the AI management system (AIMS) per harmonized clauses 4–10 plus the AI-specific machinery: AI risk assessment (6.1.2/8.2), AI risk treatment (6.1.3/8.3), and AI system impact assessment (6.1.4/8.4 — impact on individuals and societies, distinct from org risk), with Annex A control-objective selection (public Annex A counts CONFLICT across sources and are never stated; use the licensed text). Net-new is mostly management-system artifacts; AI operational controls MAP to the shipped Phase 1.5 governance pack and ai-governance-risk-reviewer via compliance-control-foundation. Composes statement-of-applicability-author, compliance-evidence-collector, and ai-lifecycle-risk-manager (NIST AI RMF as the risk method underneath). Use for ISO 42001 readiness or building an AI management system. Do NOT use for one AI feature''s posture (ai-governance-risk-reviewer), the RMF program (ai-lifecycle-risk-manager), the ISMS (iso-27001-isms-architect), or the SoA document.'
---

# ISO 42001 AIMS Architect

## Purpose

Design the AI Management System that ISO/IEC 42001:2023 certification
audits examine. The standard reuses the harmonized management-system
skeleton (clauses 4–10, same shape as 27001 — verified from the standard's
TOC) and adds AI-specific machinery: AI risk assessment (6.1.2/8.2), AI
risk treatment (6.1.3/8.3), and the AI system impact assessment
(6.1.4/8.4) that evaluates consequences for individuals and societies, not
just the organization. For this repo's operating model the D9 premise is
strong: the shipped Phase 1.5 governance pack and
`ai-governance-risk-reviewer` are exactly what a 42001 auditor points at
for AI operational control — this skill wraps them in the certifiable
management system (scope, policy, impact assessments, SoA via
`statement-of-applicability-author`, internal audit, management review)
rather than re-deriving them. Readiness design only; certification is the
accredited body's decision.

## Use When

- Use when: asked to design or build an AI management system, or to
  prepare for ISO 42001 certification.
- Use when: scoping 42001 — which AI systems fall in scope, what the AIMS
  requires beyond an existing ISMS, how AI risk/impact assessments are
  structured.
- Use when: an org with AI governance practice (risk reviews, agent
  governance) needs it formalized into certifiable management-system form.
- Do NOT use when: reviewing ONE AI feature's governance/risk posture —
  `ai-governance-risk-reviewer` (its per-feature reviews become AIMS
  operational evidence).
- Do NOT use when: operationalizing the NIST AI RMF functions as a risk
  program — `ai-lifecycle-risk-manager` (the voluntary risk method that
  pairs with, but does not certify, the AIMS).
- Do NOT use when: the information-security ISMS
  (`iso-27001-isms-architect`), the SoA document
  (`statement-of-applicability-author`), or readiness gaps
  (`compliance-gap-auditor`).

## Inputs to Inspect

1. The licensed ISO/IEC 42001:2023 text — clause wording, Annex A
   (normative, "Reference control objectives and controls"), Annex B
   (normative implementation guidance), Annex C/D (informative). Without
   it, design on verified structure only; finer claims become verification
   items.
2. The AI system inventory: which systems/features use AI, their roles
   (provider/user of AI), autonomy levels, and affected parties — seeded
   from `ai-governance-risk-reviewer` outputs where they exist.
3. Shipped AI governance artifacts to map, not rebuild: the Phase 1.5 pack
   (`ai-sdlc-operating-model` stages/authority, `agent-authorization-matrix`
   standing authority, `agent-memory-governance`, `agent-governance-audit`
   per-change audits), `ai-governance-risk-reviewer` feature reviews,
   `ai-threat-modeler` threat models, `ai-evaluation-harness` eval
   practice.
4. The `compliance-control-foundation` catalog (AI governance domain) and
   any existing ISMS — 42001 alongside 27001 shares context/leadership/
   support machinery; design the delta, not a duplicate.
5. Obligations landscape: AI-related legal/regulatory/contractual
   requirements (EU AI Act exposure via `ai-governance-risk-reviewer`'s
   obligation mapping — flagged for legal review, never asserted as legal
   conclusions).

## Workflow

1. **Define AIMS scope and context (clause 4).** Which AI systems and
   organizational roles (developer, provider, user of AI) are in scope;
   interested parties — including affected individuals/groups, which 42001
   weighs heavily; internal/external issues. Record the org's AI role per
   system: obligations differ by role.
2. **Establish leadership artifacts (clause 5).** AI policy, top-management
   commitment, named accountable roles — align with the accountable-owner
   discipline `ai-governance-risk-reviewer` already enforces per feature.
3. **Stand up the three-assessment machinery (clause 6 + 8)** using
   [references/aims-clause-map.md](references/aims-clause-map.md):
   - **AI risk assessment (6.1.2, operated via 8.2):** method and register
     for risks OF the AI systems (technical inputs from
     `ai-threat-modeler`).
   - **AI risk treatment (6.1.3, via 8.3):** treatment decisions selecting
     Annex A control objectives → SoA delegated to
     `statement-of-applicability-author` (it serves 42001 rows natively).
   - **AI system impact assessment (6.1.4, via 8.4):** per-system
     assessment of consequences for individuals and societies (fairness,
     safety, rights, societal effects) — the artifact orgs most often lack;
     define trigger points (new system, material change) and reviewers.
4. **Plan support (clause 7).** AI competence (who understands the models
   and their limits), awareness, documented information — model/feature
   cards from `ai-governance-risk-reviewer` slot in as documented
   information about AI systems.
5. **Design operation (clause 8).** How assessments and controls run in
   the AI lifecycle — map to `ai-sdlc-operating-model` stages and
   `ai-lifecycle-risk-manager` functions so the AIMS operates through
   existing machinery, not beside it. Third-party AI (providers, models)
   maps to `supply-chain-security-reviewer`'s AI/ML surface plus vendor
   management.
6. **Select Annex A control objectives via the foundation.** Map existing
   mechanisms (Phase 1.5 pack, Phase 7 AI-security skills) to objectives;
   genuine gaps get owners. Counts and identifiers come only from the
   licensed Annex A — public sources conflict.
7. **Build performance evaluation (clause 9) and improvement (clause 10).**
   Internal audit program covering the AIMS (per-change audits from
   `agent-governance-audit` are inputs, not substitutes — the AIMS audit
   examines the SYSTEM), management review cadence, nonconformity routing.
8. **Produce the readiness plan** with owners, dates, the
   ISMS-delta note where a 27001 system exists, evidence handoff to
   `compliance-evidence-collector`, and the verification-items list.

## Output Format

```
AIMS DESIGN — <org>, ISO/IEC 42001:2023
Scope: <AI systems in scope + org role per system (developer/provider/user)>
Context: <interested parties incl. affected individuals/groups; issues>
Clause artifacts:
  5: AI policy, named accountable roles
  6+8: AI risk assessment (6.1.2/8.2, register) | AI risk treatment (6.1.3/8.3 → SoA)
       | AI system impact assessment (6.1.4/8.4: individuals/societies, triggers, reviewers)
  7: AI competence, documented information (model/feature cards slot in)
  8: lifecycle integration (→ ai-sdlc-operating-model, ai-lifecycle-risk-manager); third-party AI (→ supply-chain-security-reviewer)
  9: AIMS internal audit program; management review cadence
  10: nonconformity + corrective action routing
Annex A selection: objective-by-objective map to compliance-control-foundation (mechanism | net-new+owner)
ISMS delta: <shared machinery reused vs AIMS-specific additions, if 27001 exists>
Evidence: → compliance-evidence-collector
Verification items: <licensed-text specifics — clause wording, Annex A entries; counts NEVER asserted>
Readiness plan: <artifact → owner → date>; certification decision belongs to the accredited body
```

## Validation Checklist

- [ ] AI system inventory with org role per system anchors the scope.
- [ ] All three assessments designed distinctly: risk (6.1.2), treatment
      (6.1.3 → SoA), impact on individuals/societies (6.1.4) — the impact
      assessment is not folded into org risk.
- [ ] Existing governance artifacts (Phase 1.5 pack,
      ai-governance-risk-reviewer) mapped as operational mechanisms, not
      re-specified.
- [ ] Annex A selection cites only licensed-text entries; no counts stated
      from public sources.
- [ ] Internal audit + management review designed with evidence hooks;
      per-change `agent-governance-audit` positioned as input, not
      substitute.
- [ ] ISMS-shared machinery reused where 27001 exists (one context/
      leadership/support spine, two standards served).
- [ ] Verification-items list present; no certified/will-pass claims.

## Compliance Precision Rules

- ISO/IEC 42001:2023 is a **certifiable** AI-management-system standard
  (first edition, 2023-12; harmonized clauses 4–10 incl. 6.1.2–6.1.4;
  Annex A normative "Reference control objectives and controls", Annex B
  normative guidance, C/D informative; developed by ISO/IEC JTC 1/SC 42 —
  structure verified from the standard's TOC). SOC 2 is an AICPA
  **attestation** — never conflate.
- **Never state 42001 Annex A control/objective counts**: secondary
  sources conflict ("38 controls / 9 objectives" vs "42 objectives") —
  the reconciliation record deliberately leaves them unstated; use only
  the licensed table.
- NIST AI RMF is a **voluntary companion** (the risk method underneath),
  not a certification target — `ai-lifecycle-risk-manager` owns it.
- EU-procurement demand for 42001 is positioning, not a standards claim;
  EU AI Act obligation mapping is flagged for legal review, never asserted
  as a legal conclusion.
- Readiness design only; the accredited certification body decides
  certification.

## Gotchas

- The impact assessment (6.1.4) is the distinctive artifact: orgs with
  mature security risk practice still miss "what does this AI system do to
  individuals and societies." Budget real design time for triggers,
  method, and reviewers.
- Role determines obligations: developing AI, providing AI to customers,
  and using third-party AI carry different control weight — an inventory
  without per-system roles produces a mis-scoped AIMS.
- Don't build a second management system beside an existing ISMS: the
  harmonized structure exists so context, leadership, documented
  information, audit, and review machinery can be shared. Design the
  delta.
- Per-feature reviews don't aggregate by themselves: a folder of
  `ai-governance-risk-reviewer` reports is operational evidence, but the
  AIMS needs the system-level register and assessment processes those
  reports feed.
- Fast-moving AI vendors churn the third-party surface: model/provider
  changes are AIMS-relevant changes — wire them into change management
  and impact-assessment triggers, or the system rots in a quarter.
- Annex B is normative guidance for the Annex A controls — design against
  it when licensed; don't improvise implementation depth from blog posts.

## Stop Conditions

- No AI system inventory can be established — stop; an AIMS without knowing
  which AI systems exist and in what role is fiction.
- Top-management sponsorship absent — surface before designing; clause 5
  cannot be retrofitted.
- The licensed standard text is unavailable AND clause-exact wording or
  Annex A entries are required — deliver structure-level design with
  verification items; never fabricate objectives or counts.
- Asked for one feature's go/no-go, the RMF program, the SoA document, or
  gap assessment — hand to `ai-governance-risk-reviewer`,
  `ai-lifecycle-risk-manager`, `statement-of-applicability-author`, or
  `compliance-gap-auditor` respectively.
- An impact assessment surfaces likely serious harm or a prohibited-use
  pattern — escalate to the named accountable human and legal review; do
  not design around it.

## Supporting Files

- [references/aims-clause-map.md](references/aims-clause-map.md) — the
  clause 4–10 artifact checklist with the 6.1.2/6.1.3/6.1.4 three-
  assessment design patterns, the shipped-artifact mechanism map, and the
  ISMS-delta guide.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance
  cluster and against `ai-governance-risk-reviewer`,
  `ai-lifecycle-risk-manager`, and `ai-sdlc-operating-model`.
