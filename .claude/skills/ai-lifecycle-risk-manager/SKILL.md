---
name: ai-lifecycle-risk-manager
description: 'Operationalize the NIST AI RMF as the org''s AI risk program — the four Core functions (GOVERN cross-cutting, MAP context and risks, MEASURE analysis and tracking, MANAGE prioritization and response) applied across the AI lifecycle: design, development, deployment, operation, decommission. The AI RMF 1.0 is VOLUNTARY (released 2023-01-26, under revision per NIST; Generative AI Profile NIST-AI-600-1) — a risk method, NOT a certification target; the certifiable wrapper is its companion iso-42001-aims-architect. Composes ai-governance-risk-reviewer (per-feature tiering), ai-threat-modeler, ai-evaluation-harness, and incident-response-runbook rather than restating them. Use when adopting the AI RMF, standing up an org-level AI risk program across the lifecycle, or building an RMF profile. Do NOT use for one AI feature''s go/no-go (ai-governance-risk-reviewer), the certifiable AIMS (iso-42001-aims-architect), or a feature''s threat enumeration (ai-threat-modeler).'
---

# AI Lifecycle Risk Manager

## Purpose

Stand up the organization's AI risk program on the NIST AI RMF's four Core
functions — GOVERN (cross-cutting, "infused throughout AI risk
management"), MAP, MEASURE, MANAGE — operating across the whole AI
lifecycle: design, development, deployment, operation, decommission. The
RMF is a voluntary risk method, not something an org is certified against
— its role here is the risk machinery underneath the certifiable AIMS
(`iso-42001-aims-architect`, this skill's companion) and the org-level
program that per-feature reviews (`ai-governance-risk-reviewer`) plug
into. The skill's value is operationalization: each function lands as
concrete practices mapped to shipped skills and named owners with
lifecycle-stage triggers, instead of an RMF poster on the wall.

## Use When

- Use when: adopting the NIST AI RMF, asked to "set up AI risk
  management", or building an org/system AI RMF profile.
- Use when: AI risk practice exists in pieces (feature reviews, threat
  models, evals) and needs an org-level program with lifecycle triggers
  and owners.
- Use when: pairing a 42001 effort with its underlying risk method, or a
  customer/regulator asks how the org manages AI risk end-to-end.
- Do NOT use when: reviewing ONE AI feature's risk tier, oversight, and
  disclosure — `ai-governance-risk-reviewer` (this program aggregates
  those reviews).
- Do NOT use when: building the certifiable AI management system —
  `iso-42001-aims-architect` (the AIMS wraps this method in
  management-system clauses).
- Do NOT use when: enumerating a specific feature's technical threats
  (`ai-threat-modeler`) or running the evals themselves
  (`ai-evaluation-harness`).

## Inputs to Inspect

1. The AI system inventory with lifecycle stage per system (shared with
   `iso-42001-aims-architect` when both run): what AI exists, where each
   system sits (design → decommission), roles, and affected parties.
2. Existing risk practice to compose: `ai-governance-risk-reviewer`
   feature reviews, `ai-threat-modeler` outputs, `ai-evaluation-harness`
   datasets/thresholds, `ai-sdlc-operating-model` stage/authority
   contract, `agent-authorization-matrix`, incident history
   (`incident-response-runbook` postmortems), containment posture
   (`agent-containment-reviewer`).
3. The NIST AI RMF text in hand (AI RMF 1.0 and, when generative AI is in
   scope, the Generative AI Profile NIST-AI-600-1) — category-level
   detail comes from the text, not memory; NIST notes 1.0 is under
   revision, so check the current version.
4. Org risk appetite and escalation structure: who owns AI risk
   decisions, what boards/reviews exist.
5. The `compliance-control-foundation` AI-governance domain — the program
   lands as controls there (and crosswalk rows tag their RMF function).

## Workflow

1. **Scope the program.** Which AI systems, which lifecycle stages are
   live, and who owns the program. No inventory → build it first (with
   `iso-42001-aims-architect`'s scope step if that effort runs too) or
   Stop Conditions.
2. **Land GOVERN first — it is cross-cutting.** Accountability structure
   (named owners per system and for the program), risk appetite, policies,
   escalation paths, and the workforce/culture pieces — mapped to what
   exists: `ai-sdlc-operating-model` (stage authority),
   `agent-authorization-matrix` (standing agent authority),
   `ai-governance-risk-reviewer`'s accountable-owner discipline. GOVERN
   items recur inside every other function; that's the "infused
   throughout" property, not a section to complete once.
3. **Operationalize MAP per lifecycle stage** using
   [references/ai-rmf-function-map.md](references/ai-rmf-function-map.md):
   context establishment, categorization, and risk identification —
   feature intake via `ai-governance-risk-reviewer` (tier, affected
   parties), technical surface via `ai-threat-modeler`, third-party/model
   provenance via `supply-chain-security-reviewer`. Output: the AI risk
   register rows (shared with the AIMS 6.1.2 register when present).
4. **Operationalize MEASURE.** For each mapped risk: how it is analyzed,
   assessed, and tracked over time — `ai-evaluation-harness` (quality/
   safety/grounding/injection thresholds and regression gates),
   red-team cadence, drift/behavior monitoring in operation
   (`observability-operator` mechanics), with trackable metrics and
   review dates. Unmeasurable risks are named as such, not silently
   dropped.
5. **Operationalize MANAGE.** Prioritization against risk appetite,
   treatment decisions (avoid/mitigate/transfer/accept — acceptance by a
   named human via `human-approval-boundary`), response wiring
   (`incident-response-runbook`, kill-switch/containment authority via
   `agent-containment-reviewer`), and residual-risk communication.
6. **Wire lifecycle triggers.** Per stage transition (design→dev,
   dev→deploy, deploy→operate, material change, decommission): which
   function activities re-run, who signs. Decommission gets real steps —
   model retirement, data/memory disposition (`agent-memory-governance`
   hygiene), dependent-system checks.
7. **Emit the profile and register the controls.** The org's RMF profile
   (functions → practices → owners → triggers), program-level controls
   into `compliance-control-foundation` (AI domain), crosswalk rows
   tagged with their function, and the companion note for
   `iso-42001-aims-architect` (register and impact-assessment sharing).

## Output Format

```
AI RMF PROGRAM — <org> (AI RMF 1.0; GenAI Profile NIST-AI-600-1 if in scope; version-checked: <date>)
Status of source: voluntary framework; 1.0 under revision per NIST — current-version check recorded
Inventory: <AI systems × lifecycle stage × owner>
GOVERN (cross-cutting): <accountability, appetite, policies, escalation → mapped mechanisms (ai-sdlc-operating-model, agent-authorization-matrix, ...)>
Per lifecycle stage (design | development | deployment | operation | decommission):
  MAP:     <context/categorization/risk-identification practices → owners → feeding the AI risk register>
  MEASURE: <analysis/tracking practices → ai-evaluation-harness thresholds, monitoring, cadence>
  MANAGE:  <prioritization, treatment (acceptance = named human), response wiring>
Lifecycle triggers: <transition → re-run activities → signer>
Register: <AI risk register rows (shared with AIMS 6.1.2 where applicable)>
Controls registered: <→ compliance-control-foundation AI domain; crosswalk rows tagged with RMF function>
Companion: iso-42001-aims-architect (certifiable wrapper) — this program is NOT a certification
Unmeasurable/open risks: <named honestly>
```

## Validation Checklist

- [ ] GOVERN is designed as cross-cutting — its items appear inside MAP/
      MEASURE/MANAGE practices, not as a one-time section.
- [ ] Every function lands as concrete practices with named owners and
      lifecycle triggers — zero poster-level aspirations.
- [ ] Existing skills are composed by name (feature reviews, threat
      models, evals, incident machinery); nothing they own is restated.
- [ ] The AI risk register exists with per-risk measurement and treatment;
      acceptance decisions carry a named human.
- [ ] Decommission-stage practices are real (model retirement, data/memory
      disposition), not a placeholder.
- [ ] The program is labeled voluntary throughout; the current-version
      check of the RMF is recorded.
- [ ] Program controls registered in the foundation catalog with RMF
      function tags in the crosswalk.

## Compliance Precision Rules

- The NIST AI RMF is **voluntary** — released 2023-01-26; "The Core is
  composed of four functions: govern, map, measure, and manage," with
  GOVERN cross-cutting (verified on NIST/AIRC pages). It is a risk
  method, **not a certification target** — no org "passes" or "is
  certified against" the AI RMF, and this skill's outputs never imply it.
- NIST notes AI RMF 1.0 is **under revision** — record a current-version
  check date in every profile; category-level citations come from the
  text in hand, not memory.
- The Generative AI Profile is **NIST-AI-600-1 (2024-07-26)** — apply it
  when generative AI is in scope; it profiles the RMF, it does not
  replace it.
- The certifiable instrument is ISO/IEC 42001 (`iso-42001-aims-architect`)
  — pair them as method + management system; never present the RMF as the
  certificate.

## Gotchas

- Poster-ware is the RMF failure mode: four function names on a slide
  with no owners, triggers, or metrics. The test of every practice:
  who does it, when does it fire, what artifact does it leave.
- GOVERN-as-a-phase is a design smell — if governance items only appear
  at program setup, the "infused throughout" property is lost and drift
  is unmanaged.
- Per-feature reviews don't sum to a program: a folder of
  `ai-governance-risk-reviewer` reports without a register, thresholds,
  and lifecycle triggers is MAP without MEASURE/MANAGE.
- Decommission is the forgotten stage: retired models with live memory
  stores, orphaned agent credentials, and dependent systems silently
  breaking — plan disposition like a real deliverable.
- MEASURE honesty: some AI risks (societal effects, long-horizon misuse)
  resist metrics — name them unmeasured with review dates rather than
  inventing vanity metrics.
- Framework churn: 1.0 is under revision; profiles citing subcategory
  IDs from memory will rot. Cite from text in hand and re-check the
  version at each program review.

## Stop Conditions

- No AI system inventory can be established and no program owner exists —
  stop; a risk program needs both a subject and an accountable human.
- The AI RMF text is not in hand AND category-level citation is required
  — deliver function-level design with a verification-items list; do not
  cite subcategories from memory.
- Asked to certify, attest, or score the org "against the RMF" as
  pass/fail — reframe: voluntary method, profile + register + readiness;
  certification questions route to `iso-42001-aims-architect` /
  `compliance-gap-auditor`.
- MAP surfaces a likely prohibited or severely harmful use — escalate to
  the named accountable human and legal review (the
  `ai-governance-risk-reviewer` unacceptable-tier path); do not design
  around it.
- The task is one feature's review, one threat model, or running evals —
  hand to the owning skill and stop.

## Supporting Files

- [references/ai-rmf-function-map.md](references/ai-rmf-function-map.md)
  — the function × lifecycle-stage practice matrix, owning-skill map,
  register row shape, and the trigger table.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance
  cluster and against `ai-governance-risk-reviewer`,
  `iso-42001-aims-architect`, `ai-threat-modeler`, and
  `ai-evaluation-harness`.
