# Step 0 Reconciliation (v4 canonical)

**Prepared:** 2026-07-06
**Repo:** `nguyenpv1980-wq/Claude-Skills`
**Verified HEAD at reconciliation time:** `5f6f404a8e261c89b8264c3282acd32075f54411` — *"Merge PR #1: 300 repeatable Claude skills roadmap"* on `main`.

This document is the single source of truth for how the two overlapping planning tracks
were reconciled before any skills are generated. It is docs-only. It does not create skills.

---

## 1. Canonicalization

Two planning tracks existed in the repo:

- **v4 track** — [`docs/research/claude-skills-architecture-audit-findings-v4.md`](../research/claude-skills-architecture-audit-findings-v4.md)
  and [`docs/prompts/claude-skills-master-generation-prompts-v4.md`](../prompts/claude-skills-master-generation-prompts-v4.md).
- **Execution-plan track** — [`docs/prompts/senior-principal-claude-skills-execution-plan.md`](../prompts/senior-principal-claude-skills-execution-plan.md).

**Decision D1 — the v4 pair is canonical.** The senior-principal execution plan is
reclassified as **historical/reference input**. Everything unique and still valuable in
it (Phase 8 batch rules, the pre-generation plan table, extra validator checks, several
skill names) is **ported into the v4 pair** so nothing is lost. After this reconciliation,
generation follows the v4 prompts only.

Also historical (unchanged, kept as source inputs):
`docs/research/claude-skills-principal-architecture-findings.md`,
`docs/prompts/master-claude-skills-and-agents-development-prompt.md`,
`docs/prompts/phased-claude-skills-prompts.md`,
`docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md`,
`docs/150-claude-skills-roadmap.md`.

---

## 2. Stale claims removed / corrected

| Stale claim (where) | Reality (2026-07-06) | Action |
|---|---|---|
| "open PR #1", "Continue from or merge PR #1" (v4 audit §2.3, §3 F1, §9) | PR #1 is **merged** into `main` at `5f6f404`. | v4 audit updated to state PR #1 is merged and `main` is the product-agnostic baseline. |
| "`main` is still effectively empty" (execution plan §2.3) | `main` contains the full roadmap, category docs, research, and prompts. | Corrected here; execution plan is now historical so its body is left intact but superseded by this note. |
| Existing work lives on PR branch `docs/300-repeatable-software-saas-skills` (execution plan §2.3) | That branch was fully merged and has been **deleted**. Branch `x` (an older, superseded state) was also fully merged and **deleted**. | Both stale remote branches removed after confirming `git merge-base --is-ancestor` = merged and zero unmerged commits. `main` is the only remaining branch. |

---

## 3. Reconciled phase → executable-skill list (ONE list per phase)

The **v4 phase structure is canonical**. Each row shows the reconciled skill and how the
execution-plan track's names map onto it (merge / move / same). Every skill traces to a
`docs/skills/` category entry where applicable.

### Phase 0 — Foundation (P0) — *this phase*
Standard, templates, eval schema, catalog, validator, README, real subagents, `_template`.
No skills generated. (Both tracks agree.)

### Phase 1 — AI engineering operating-discipline pack (P0)
**Canonical = v4's 8.** The execution plan's Phase 1 mixed operating-discipline with
architecture; the architecture skills are **moved to Phase 2**.

| # | Reconciled skill | Roadmap ref (cat 08) | Merge / move note |
|---|---|---|---|
| 1 | `agent-startup-context-gate` | #262 | same in both tracks |
| 2 | `source-of-truth-reconciler` | #269 | absorbs execution-plan `no-silent-assumptions-protocol` (#270) assumption-surfacing behavior |
| 3 | `change-classification-gate` | #264 | absorbs execution-plan `phase-locked-execution` (#263) scope-lock behavior |
| 4 | `human-approval-boundary` | #265 | new canonical name (v4); also carries the "stop when unclear" half of #270 |
| 5 | `reviewable-diff-discipline` | #271 | absorbs execution-plan `exact-file-staging` intent (#272) |
| 6 | `ai-closeout-reporter` | #274 | same intent both tracks |
| 7 | `agent-failure-recovery` | #275 | v4 addition |
| 8 | `agent-instruction-consolidator` | #276 | #276 Agent Instruction Consolidation |

**Moved out of Phase 1 → Phase 2:** `adr-writer`, `system-context-mapper`, `domain-modeler`,
`bounded-context-identifier`, `architecture-designer`, `dependency-direction-guard`,
`refactor-safety-planner`.

### Phase 2 — Core architecture & engineering (P0)
**Canonical = v4's 10:** `domain-modeler`, `architecture-designer`, `adr-writer`,
`docs-first-implementer`, `tdd-engineer`, `systematic-debugger`, `code-reviewer`,
`code-simplifier`, `principal-code-analyst`, `full-codebase-auditor`.

Merges/moves from the execution plan: `grill-with-docs` **→ merged into** `docs-first-implementer`
(same skill, v4 name wins). Architecture skills moved from execution-plan Phase 1 land here.
Execution-plan Phase 2 extras (`api-contract-designer`, `idempotency-first-designer`,
`validation-boundary-designer`, `observability-by-design`, `operational-runbook-author`) and
the moved arch skills (`system-context-mapper`, `bounded-context-identifier`,
`dependency-direction-guard`, `refactor-safety-planner`) are **reconciled into the Phase 2
expansion backlog** (built in Phase 8 batches, not the initial Phase 2 pass), keeping the
first pass to v4's 10 for quality.

### Phase 3 — SaaS & tenant isolation (P0/P1)
**Canonical = v4's 9:** `saas-platform-architect`, `tenant-modeler`, `tenant-isolation-reviewer`,
`multi-tenant-data-architect`, `authorization-matrix-designer`, `plan-entitlement-architect`,
`audit-log-architect`, `saas-cost-architect`, `api-event-architect`.
Execution-plan equivalents merged: `rls-policy-author`/`rls-negative-test-designer` →
**deferred to Phase 4** (RLS pack) to avoid duplication; `tenant-provisioning-designer`,
`membership-invitation-designer`, `role-permission-architect`, `security-impact-note-author`
→ Phase 3 expansion backlog.

### Phase 4 — Security, RLS & supply chain (P0/P1)
**Canonical = v4's 9:** `threat-modeler`, `appsec-implementer`, `multi-tenant-security-tester`,
`rls-policy-auditor`, `secrets-identity-hardener`, `supply-chain-security-reviewer`,
`security-pr-reviewer`, `secure-migration-reviewer`, `static-analysis-reviewer`.
Execution-plan `rls-policy-author` + `rls-negative-test-designer` **→ merged into**
`rls-policy-auditor` (which per v4 includes the negative-test plan).

#### OWASP Top 10 (Web Application Security) coverage map

Gap audit (D8) of the nine **shipped** Phase 4 skills against the **OWASP Top 10:2025** for
web application security, A01:2025–A10:2025. Source: <https://owasp.org/www-project-top-ten/>
(verified 2026-07-06 — the project page states the current released edition is the 2025 list,
published at <https://owasp.org/Top10/2025/>). This map records coverage of already-shipped
work and tracks gaps as Phase 8 backlog items; it creates no skills and changes no phase list.

| OWASP Top 10:2025 (web app) | Covering shipped Phase 4 skill(s) | Status |
|---|---|---|
| A01:2025 Broken Access Control | `multi-tenant-security-tester` (IDOR, cross-tenant, privilege escalation), `rls-policy-auditor`, `security-pr-reviewer` (object-level/tenant-scope checks, SSRF hunting in diffs), `appsec-implementer` (authz checks, SSRF/redirect allowlists), `threat-modeler` | covered |
| A02:2025 Security Misconfiguration | `secure-migration-reviewer` (unsafe defaults, over-broad GRANTs, RLS-enablement gaps), `rls-policy-auditor` (deny-by-default posture), `secrets-identity-hardener` (env classification, client-bundle exposure) | partial |
| A03:2025 Software Supply Chain Failures | `supply-chain-security-reviewer` (dependencies, lockfiles, CI/CD, artifact provenance; extended to AI supply chain per D6/LLM03) | covered |
| A04:2025 Cryptographic Failures | `secrets-identity-hardener` (key/credential custody, rotation, exposure), `static-analysis-reviewer` (triage of weak-crypto findings) | partial |
| A05:2025 Injection | `security-pr-reviewer` (injection in diffs), `appsec-implementer` (parameterized queries, input validation, output encoding), `static-analysis-reviewer` (SAST injection triage) | covered |
| A06:2025 Insecure Design | `threat-modeler` (trust boundaries, STRIDE enumeration, abuse cases, mitigations each with a negative test); `appsec-implementer` builds the decided controls | covered |
| A07:2025 Authentication Failures | `secrets-identity-hardener` (session/token expiry, refresh, storage flags, revocation), `security-pr-reviewer` (authn gaps in diffs), `threat-modeler` (auth is a named design surface) | covered |
| A08:2025 Software or Data Integrity Failures | `supply-chain-security-reviewer` (CI/CD integrity, unpinned Actions, artifact provenance), `security-pr-reviewer` (unsafe deserialization) | covered |
| A09:2025 Security Logging and Alerting Failures | `security-logging-alerting-architect` (detection coverage, alerting rules, response wiring — built from the Phase 8 backlog, D28) | covered |
| A10:2025 Mishandling of Exceptional Conditions | `error-handling-security-reviewer` (fail-closed defaults, error-path authorization, exception-driven bypass, leak-free error responses — built from the Phase 8 backlog, D28) | covered |

- **Rubric:** *covered* = the category's core risk is named in at least one shipped Phase 4
  skill contract; *partial* = only a slice is named (residue listed below); *gap* = no
  Phase 4 skill owns it. Honest residue beats optimistic green.
- **A01 / SSRF:** the 2025 edition folds SSRF (A10:2021) into Broken Access Control. SSRF is
  covered at three points (`threat-modeler` enumeration, `appsec-implementer` allowlists,
  `security-pr-reviewer` diff hunting), so no standalone `ssrf-defense-reviewer` backlog item
  is opened.
- **A02 residue:** application/platform configuration — security headers, CORS, XML-parser
  hardening (XXE-class), default accounts, cloud posture — has no Phase 4 owner. Cloud
  posture is owed to Phase 6 (`iac-reviewer`, plus `cloud-security-baseline-reviewer` in the
  Phase 6 expansion backlog); the app-config slice remains open residue.
- **A04 residue:** encryption-in-transit/at-rest design and algorithm/library review are
  unowned; coverage today is custody of keys/credentials plus SAST-finding triage only.
- **A09/A10 gaps: CLOSED (D28, 2026-07-08).** Both categories now have an owning skill,
  built from the Phase 8 backlog items D8 recorded: `security-logging-alerting-architect`
  (A09) and `error-handling-security-reviewer` (A10). They are Phase-8-backlog builds, not
  additions to the Phase 4 list — the map cells cite them as D28 builds. Phase 3
  `audit-log-architect` remains the RECORD layer that A09 detection consumes (it records,
  but does not detect or alert).
- **Framework distinction:** this is a third OWASP framework, distinct from the OWASP LLM
  Top 10 (Phase 7 map below, D6) and from the separate OWASP Agentic framework (Phase 7.5
  map below, D7).

### Phase 5 — QA, E2E, manual QA & evidence (P0/P1)
**Canonical = v4's 13:** `qa-strategy-architect`, `test-plan-designer`, `test-coverage-mapper`,
`qa-automation-architect`, `playwright-e2e-engineer`, `clickthrough-test-engineer`,
`manual-test-case-creator`, `screenshot-evidence-planner`, `vitest-unit-component-engineer`,
`vite-build-qa-engineer`, `flaky-test-detective`, `test-data-architect`, `regression-suite-curator`.
Execution-plan extras merged: `acceptance-criteria-tester`, `e2e-test-architect`,
`qa-closeout-reporter` → Phase 5 expansion backlog (`qa-closeout-reporter` overlaps
`ai-closeout-reporter` + `screenshot-evidence-planner`; keep as backlog to avoid trigger overlap).

> Note: execution-plan ordering placed QA at Phase 4 and audit/troubleshooting at Phase 5.
> v4 ordering (Security at 4, QA at 5) is canonical. Whole-codebase audit / troubleshooting
> skills (`full-codebase-auditor`, `principal-code-analyst`, `senior-troubleshooter`,
> `code-quality-auditor`, `dependency-license-audit-reviewer`, `code-audit-orchestrator`)
> are absorbed into v4 Phase 2 (`full-codebase-auditor`, `principal-code-analyst`) with the
> remainder in the Phase 2/5 expansion backlog.

#### Phase 5 QA expansion backlog — prioritized (D10)

Gap audit (D10, 2026-07-07) of roadmap category 06
([`docs/skills/06-qa-test-engineering.md`](../skills/06-qa-test-engineering.md), scoped to
items #181–#230) against the **16 shipped Phase 5 skills** — the 13 canonical above plus
`integration-test-designer` (#184), `api-contract-test-designer` (#185), and
`accessibility-test-harness` (#204), pulled forward at ship time. Uncovered items land in
three build tiers; **every entry is (candidate — not built)**. This prioritizes the backlog
only: no skills created, no phases renumbered, validator targets unchanged.

**Already covered — mapped once, not re-listed as candidates:**

| Roadmap # (cat 06) | Owned by shipped skill |
|---|---|
| #181 Test Strategy Authoring | `qa-strategy-architect` (Phase 5) |
| #182 Risk-Based Validation Matrix | `change-classification-gate` (Phase 1) — validation-tier selection lives cross-phase |
| #183 Unit Test Design | `vitest-unit-component-engineer` (Phase 5) |
| #184 Integration Test Design | `integration-test-designer` (Phase 5, pulled forward) |
| #185 Contract Test Design | `api-contract-test-designer` (Phase 5, pulled forward) |
| #186 RLS Test Harness Design | `multi-tenant-security-tester` + `rls-policy-auditor` (Phase 4) — RLS testing lives cross-phase |
| #187 E2E Journey Design | `playwright-e2e-engineer` (Phase 5) |
| #196 Test Data Isolation / #197 Seed Fixture Governance | `test-data-architect` (Phase 5) |
| #204 Accessibility Test Harness | `accessibility-test-harness` (Phase 5, pulled forward) |
| #209 Flake Detection / #210 Flake Quarantine Governance | `flaky-test-detective` (Phase 5) |
| #221 Manual QA Script Authoring | `manual-test-case-creator` (Phase 5) |
| #222 Clickthrough Testing Protocol | `clickthrough-test-engineer` (Phase 5) |
| #223 Screenshot Evidence Capture | `screenshot-evidence-planner` (Phase 5) |

**Tier 1 — build first when the QA expansion runs** (uncovered roadmap P0s plus the
performance/load headline):

| Candidate *(all: candidate — not built)* | Roadmap ref (cat 06) | Note |
|---|---|---|
| `performance-test-harness` + `load-test-planner` — **✅ both built (D23, 2026-07-07)** | #205 (P1) + #206 (P2) | **Headline gap — now closed:** load/render/query/API/edge-function/background-job performance measurement plus realistic traffic/tenant/data-volume load planning — the largest uncovered risk for a multi-tenant SaaS (noisy neighbors, per-tenant degradation). Built as TWO skills per the D23 pre-generation plan table (instrument vs traffic plan — the sibling seam is pinned in both trigger-evals). Pre-release counterpart to Phase 6 `slo-reliability-architect` (targets/alerting); the designs-vs-measures seam against D12.3 is pinned from both sides. |
| `regression-first-bug-fixer` | #190 (P0) | Failing test that reproduces the bug BEFORE the fix. `regression-suite-curator` cites #190 but owns suite membership, not the fix workflow; `tdd-engineer` owns new behavior, not bug reproduction. |
| `negative-path-test-mapper` | #192 (P0) | Systematic unauthorized/invalid/expired/missing/duplicated/conflicting/out-of-order enumeration per surface. `test-plan-designer`/`test-coverage-mapper` cite #192 as a source but own planning/audit; security negatives stay with Phase 4 `multi-tenant-security-tester`. |
| `test-tenant-provisioner` | #198 (P0) | Repeatable test tenants/users for auth, RLS, integration, and E2E runs. `test-data-architect` (source range #196–#199) owns the data catalog; provisioning the tenants/users themselves is unowned. (broadened per report P12: test-row marker convention with never-mutate-unmarked rule, validate-only vs apply modes, env-var-name-only credentials, backup-gated capability grants with inline rollback, prod-safe static lint of QA automation) |
| `ci-failure-classifier` | #214 + #215 (merged; both P0) | ONE skill: hidden runtime-marker scan (console errors, unhandled rejections, skipped tests, auth failures) + failure classification (product bug / test bug / missing secret / timeout-only / infra / skipped runtime). `flaky-test-detective` owns intermittence root-cause; this owns the every-run CI verdict. (per report P14: duration as first-class evidence; TIMEOUT_FAILURE as a distinct class never conflated with regressions; resume-don't-rerun after timeout-only interruptions; no masking real failures by raising timeouts) |
| `acceptance-criteria-tester` | #226 + #227 (merged; both P0) | Testability/completeness/ambiguity review of acceptance criteria + definition-of-done check. **Already deferred once** (execution-plan extra → this backlog, note above); the deferral stands — it builds in this tier, not before. |

**Tier 2 — second wave** (roadmap P1 hardening, plus #203 promoted because UI drift is
otherwise invisible to the shipped suite):

| Candidate *(all: candidate — not built)* | Roadmap ref (cat 06) | Note |
|---|---|---|
| `visual-regression-test-designer` | #203 (P2) | Critical UI states with stable data, deterministic viewport, reviewable diffs. |
| `role-based-qa-matrix` | #229 (P1) | Behavior across anonymous/member/manager/admin/owner/support/platform roles; QA counterpart to Phase 3 `authorization-matrix-designer`. |
| `mobile-viewport-qa` | #230 (P1) | Critical journeys on mobile breakpoints, touch interactions, dialogs, navigation. |
| `exploratory-testing-charter` | #228 (P1) | Mission/risks/personas/data/paths/timebox charters for exploratory passes. |
| `mock-strategy-designer` | #200 + #201 (merged; both P1) | ONE skill: mock/fake/stub/adapter/recording/live selection + test-double contract review keeping doubles aligned with real provider/DB behavior (`api-contract-test-designer`'s fake-fidelity check is the contract-layer slice of this). |
| `ci-shard-parallel-isolation` | #211 + #212 (merged; both P1) | ONE skill: shard design (stable shards, run IDs, artifacts) + parallel isolation (no shared users/tenants/records/ports/browser state/queues). Extends `qa-automation-architect`'s blueprint into enforceable rules. |

**Tier 3 — specialized, defer** (all roadmap P2; build on demand only):

| Candidate *(all: candidate — not built)* | Roadmap ref (cat 06) | Note |
|---|---|---|
| `property-based-test-designer` | #194 (P2) | Generated input combinations for validation, parsing, math, state, transformations. |
| `mutation-testing-reviewer` | #195 (P2) | Mutation thinking to expose tests that pass without proving behavior. |
| `soak-test-planner` | #207 (P2) | Long-duration runs for leaks, queue buildup, token expiry, degradation. |
| `chaos-test-planner` | #208 (P2) | Safe injection of service failures, timeouts, retries, partial outages. |

- **Build timing (D10):** after the core phases (7, 7.5) or on demand; nothing here is
  built now.
- Category-06 items neither tiered nor mapped above (#188, #189, #191, #193, #199, #202,
  #213, #216–#220, #224, #225), plus the category tail outside this audit's #181–#230 scope
  (#231–#235), stay unprioritized backlog in the Phase 8 batch flow (D5). Several are already
  partially absorbed via shipped catalog source mappings (#191 → `test-coverage-mapper`,
  #199 → `test-data-architect`, #217 → `vite-build-qa-engineer`) and were counted neither as
  gaps nor as coverage. The execution-plan extras note above (`e2e-test-architect`,
  `qa-closeout-reporter`) is unchanged.

### Phase 6 — Cloud, DevOps, reliability & release (P1)
**Canonical = v4's 10:** `cloud-architecture-decider`, `azure-saas-architect`, `aws-saas-architect`,
`iac-reviewer`, `ci-pipeline-architect`, `release-readiness-reviewer`, `rollback-runbook-author`,
`observability-operator`, `slo-reliability-architect`, `incident-response-runbook`.
Execution-plan extras (`cloud-security-baseline-reviewer`, `resilience-architecture-reviewer`,
`rollback-strategy-designer`→merged into `rollback-runbook-author`, `migration-deployment-runbook`,
`environment-parity-reviewer`, `database-backup-verifier`) → Phase 6 expansion backlog.

### Phase 7 — AI security & LLM systems (P1)
**Canonical = 14 — v4's 10 + 4 OWASP-gap additions (D6):** `ai-threat-modeler`,
`prompt-injection-defender`, `rag-security-architect`, `agent-tool-safety-guard`,
`llm-output-safety-reviewer`, `ai-evaluation-harness`, `ai-cost-guardrail-designer`,
`ai-governance-risk-reviewer`, `ai-router-architect`, `structured-output-validator`,
`sensitive-disclosure-guard` *(NEW)*, `model-poisoning-reviewer` *(NEW)*,
`system-prompt-leakage-reviewer` *(NEW)*, `ai-misinformation-guard` *(NEW)*.
Execution-plan extras (`ai-provider-adapter-designer`, `prompt-contract-designer`,
`ai-human-in-the-loop-designer`, `ai-autonomy-boundary-designer`, `ai-security-test-harness`→merged
into `ai-evaluation-harness`, `ai-feature-kill-switch-designer`) → Phase 7 expansion backlog.

#### OWASP LLM Top 10 (2025) coverage map

Phase 7 is anchored to the **OWASP Top 10 for LLM Applications (2025)**, LLM01:2025–LLM10:2025.
Source: <https://genai.owasp.org/llm-top-10/> (verified 2026-07-06). This banks the coverage
target now; the skills themselves are still built at Phase 7, not before.

| OWASP LLM Top 10 (2025) | Covering Phase 7 skill(s) | Status |
|---|---|---|
| LLM01:2025 Prompt Injection | `prompt-injection-defender` | covered |
| LLM02:2025 Sensitive Information Disclosure | `sensitive-disclosure-guard` *(NEW)* | gap |
| LLM03:2025 Supply Chain | Phase 4 `supply-chain-security-reviewer`, **extended** to cover models, datasets, and fine-tuning adapters | extend-existing |
| LLM04:2025 Data and Model Poisoning | `model-poisoning-reviewer` *(NEW)* | gap |
| LLM05:2025 Improper Output Handling | `llm-output-safety-reviewer` + `structured-output-validator` | covered |
| LLM06:2025 Excessive Agency | `agent-tool-safety-guard` | covered |
| LLM07:2025 System Prompt Leakage | `system-prompt-leakage-reviewer` *(NEW)* | gap |
| LLM08:2025 Vector and Embedding Weaknesses | `rag-security-architect`, including cross-tenant vector-store access control | covered |
| LLM09:2025 Misinformation | `ai-misinformation-guard` *(NEW)* — grounding, citation, uncertainty signaling | gap |
| LLM10:2025 Unbounded Consumption | `ai-cost-guardrail-designer`, **extended** to cover denial-of-service and denial-of-wallet | extend-existing |

- `system-prompt-leakage-reviewer` must encode that **system prompts are NOT security
  controls**; enforcement must be deterministic and live outside the LLM.
- `ai-threat-modeler`, `ai-governance-risk-reviewer`, `ai-router-architect`, and
  `ai-evaluation-harness` are cross-cutting glue across all ten categories rather than
  mapped one-to-one.
- The **OWASP Top 10 for Agentic Applications is a separate framework** that the
  LLM Top 10 does not cover; agentic-specific skills are anchored in **Phase 7.5 below**
  (D7) — no longer a Phase 8 follow-on candidate — and are not part of this Phase 7 expansion.

### Phase 7.5 — Agentic AI security (OWASP Agentic Top 10) (P1)

**NEW phase (D7): canonical = 6 new skills + 3 extensions of existing skills.** Anchored to
the **OWASP Top 10 for Agentic Applications (2026)**, ASI01–ASI10. Source:
<https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/> (all ten
designations and names verified 2026-07-06 against the published framework document behind
that page). Rationale (D7): agentic risk builds on top of LLM risk (Phase 7, D6), so this
pack runs immediately after Phase 7; it is too central to this repo's agentic workflows to
defer into the generic Phase 8 backlog. Skills are **built at Phase 7.5, not now** — like
the Phase 7 map above, this banks the coverage target only; today's shipped validator
target (52 skills) is unchanged.

| OWASP Agentic Top 10 (2026) | Covering skill | Status |
|---|---|---|
| ASI01 Agent Goal Hijack | `agent-goal-hijack-defender` *(NEW)* — goal/plan integrity across multi-step runs; builds on `prompt-injection-defender` (LLM01), which owns the injection vector | new |
| ASI02 Tool Misuse and Exploitation | Phase 7 `agent-tool-safety-guard`, **extended** — per-tool authorization, argument validation, side-effect limits, tool-chain abuse paths | extend-existing |
| ASI03 Identity and Privilege Abuse | `agent-identity-privilege-reviewer` *(NEW)* — agent identities, scoped credentials, delegation chains, confused-deputy paths; complements Phase 4 `secrets-identity-hardener` (credential custody) | new |
| ASI04 Agentic Supply Chain Vulnerabilities | Phase 4 `supply-chain-security-reviewer`, **extended** again (after D6/LLM03) to MCP servers and manifests, tool/skill registries, plugin packages, A2A dependencies | extend-existing |
| ASI05 Unexpected Code Execution (RCE) | Phase 7 `llm-output-safety-reviewer` + `agent-tool-safety-guard`, **extended** — execution of agent-generated code, sandbox boundaries, natural-language-driven execution paths | extend-existing |
| ASI06 Memory & Context Poisoning | `memory-context-poisoning-reviewer` *(NEW)* — persistent corruption of stored context/long-term memory, cross-session and cross-tenant contamination; distinct from `model-poisoning-reviewer` (training-time, LLM04) and `rag-security-architect` (retrieval stores, LLM08) | new |
| ASI07 Insecure Inter-Agent Communication | `inter-agent-comms-reviewer` *(NEW)* — authn, integrity, and confidentiality of agent-to-agent messages (MCP/A2A transports); spoofing and replay | new |
| ASI08 Cascading Failures | `agent-containment-reviewer` *(NEW — merged, also owns ASI10)* — fault propagation across agent networks: blast-radius isolation, circuit breakers, checkpoints | new |
| ASI09 Human-Agent Trust Exploitation | `human-agent-trust-reviewer` *(NEW)* — consent fatigue, deceptive or over-polished justifications that mislead human approvers; adversarial counterpart to Phase 1 `human-approval-boundary` | new |
| ASI10 Rogue Agents | `agent-containment-reviewer` *(NEW — merged, same skill as ASI08)* — behavioral-drift detection, agent inventory/lifecycle governance, kill switches | new |

- **Merged overlaps — 6 new skills, not 7+:** ASI08 and ASI10 collapse into one
  `agent-containment-reviewer`. The source's own seam — ASI08 is fault *propagation* across
  interconnected agents, ASI10 is the "containment gap" once behavioral drift begins — makes
  them two halves of a single containment review (same inputs: agent topology, autonomy
  boundaries, kill/rollback paths). It also covers the agentic slice of the Phase 7
  expansion-backlog candidate `ai-feature-kill-switch-designer`. Nothing else collapses: the
  source explicitly distinguishes ASI01 vs ASI06 vs ASI10 (direct goal alteration vs
  stored-memory corruption vs autonomous drift without active attacker control).
- **Coverage counts:** 7 of 10 categories land on new skills (6 skills after the merge);
  3 of 10 are extensions (ASI02, ASI05 extend Phase 7 skills; ASI04 extends Phase 4
  `supply-chain-security-reviewer`); 0 are fully covered by already-planned work.
- **Framework relationship:** the Agentic Top 10 **extends — does not replace — the LLM
  Top 10 (D6)**: the source states agentic apps "will not exist in isolation and will be part
  of developing an LLM App," and its entries cross-reference LLM categories (e.g. ASI09
  builds on LLM06 Excessive Agency and can be caused by LLM01 Prompt Injection). Agent
  systems inherit every Phase 7 LLM-side risk; Phase 7.5 adds the autonomy, tool, identity,
  memory, and multi-agent risks layered on top.

### Compliance & Governance batch (ISO 27001:2022 + ISO 42001:2023 + SOC 2 Type 2)

**SHIPPED batch (D9) — banked 2026-07-06 targeted AFTER Phase 7; implemented 2026-07-07 and
merged via PR #21 (merge commit `2df96f1`) — all 9 skills.** This is
certification/attestation readiness for an AI SaaS vendor selling into US enterprise and EU
markets: SOC 2 is the de-facto US enterprise procurement ask, ISO 27001 is pulled through EU
supply chains by NIS2 obligations on customers, and ISO 42001 is emerging in EU public
procurement for AI vendors (vendor-market rationale, not a standards claim). **Distinct from
Phase 1.5** (operational agent governance — how agents behave inside the SDLC) **and from the
OWASP maps (D6/D7/D8)** (technical attack-surface coverage): this batch maps controls that
largely already exist and produces auditor-grade evidence on top of them.

**The frameworks, from fetched sources (fetched 2026-07-06; full source list + per-item
verification status in D9):**

- **ISO/IEC 27001:2022** — *Information security, cybersecurity and privacy protection —
  Information security management systems — Requirements*, third edition, 2022-10. A
  **certifiable ISMS** standard: management-system clauses 4–10 (Context of the organization,
  Leadership, Planning, Support, Operation, Performance evaluation, Improvement — verified
  against the standard's own TOC) plus **Annex A (normative) "Information security controls
  reference"**, applied through the 6.1.3 risk-treatment process (Statement of Applicability).
  Annex A groups controls into four themes — **A.5 Organizational, A.6 People, A.7 Physical,
  A.8 Technological** — totalling **93 controls (37/8/14/34)**; *counts are from secondary
  controls references, NOT verified against the paywalled Annex A table itself — verify before
  citing.* **ISO/IEC 27001:2022/Amd 1:2024 "Climate action changes"** amends clauses 4.1/4.2
  (the organization must determine whether climate change is relevant; interested parties can
  have climate-related requirements); *amendment existence and title verified from the ISO
  catalog entry; the exact inserted sentences are from secondary summaries.*
- **ISO/IEC 42001:2023** — *Information technology — Artificial intelligence — Management
  system*, first edition, 2023-12. A **certifiable AIMS** standard with the same harmonized
  clauses 4–10 (verified against the standard's TOC), adding AI-specific machinery: AI risk
  assessment (6.1.2/8.2), AI risk treatment (6.1.3/8.3), and **AI system impact assessment
  (6.1.4/8.4)** — plus **Annex A (normative) "Reference control objectives and controls"**,
  Annex B (normative, implementation guidance for AI controls), Annex C/D (informative).
  *Annex A control counts are deliberately NOT stated here: secondary sources conflict ("38
  controls / 9 objectives" vs "42 objectives"); verify against the standard text before using
  any number.*
- **SOC 2** — an **AICPA attestation (a CPA's examination), NOT a certification** — 27001/42001
  certify; SOC 2 attests. It reports on controls at a service organization under the **Trust
  Services Criteria** (2017 TSC with revised Points of Focus 2022, issued by the AICPA
  Assurance Services Executive Committee) across five categories: **Security, Availability,
  Processing Integrity, Confidentiality, Privacy**. **Type 1** = fairness of the system
  description + suitability of control **design as of a specified date**; **Type 2** = the same
  **plus operating effectiveness over a period**. *The five categories, ASEC authorship, and
  "examination" language are verified on AICPA pages; the Type 1/Type 2 definitions and
  "Security is the required common-criteria baseline, the other four are scoped per engagement"
  come from CPA-firm sources — AICPA's fetchable pages do not define them; the defining text is
  the paywalled AICPA SOC 2 guide.*
- **Companion, not a certification target: NIST AI RMF 1.0** (released 2023-01-26; voluntary;
  under revision per NIST). Core = **four functions: GOVERN, MAP, MEASURE, MANAGE**, with
  GOVERN "a cross-cutting function that is infused throughout AI risk management" (verified on
  NIST AIRC). Generative AI Profile NIST-AI-600-1 (2024-07-26). Pairs with 42001 as the risk
  method underneath the management system.

**Architecture (D9): ONE shared control foundation + framework projections + a crosswalk — NOT
three parallel skill sets.** Published crosswalks put cross-framework control overlap at
roughly **60–80%** (industry estimate, not a standard-derived figure): the same access-control,
crypto, change-management, logging, incident-response, vendor-management, and risk-assessment
controls satisfy 27001 Annex A, SOC 2 TSC, and much of 42001's non-AI-specific surface.
Consequence: **build TSC criteria and Annex A mapping together, not sequentially** — the
foundation is written once and projected per framework. The 9 skills below are already the
merged set: evidence collection is ONE skill across all three frameworks (not per-framework),
gap auditing is ONE parameterized skill, and the SoA author serves both ISO standards.

| Skill *(all: implemented — PR #21, 2026-07-07)* | Layer | Purpose |
|---|---|---|
| [`compliance-control-foundation`](../../.claude/skills/compliance-control-foundation/SKILL.md) | Shared foundation | One framework-agnostic common control set — access control, cryptography, change management, logging/monitoring, incident response, vendor management, risk assessment — written once, consumed by the projections |
| [`compliance-evidence-collector`](../../.claude/skills/compliance-evidence-collector/SKILL.md) | Shared foundation | Operating-effectiveness evidence **over time** (cadence, retention, audit-window coverage) — SOC 2 Type 2's core demand, reused for ISO surveillance audits |
| [`statement-of-applicability-author`](../../.claude/skills/statement-of-applicability-author/SKILL.md) | Shared foundation | The ISO-mandatory SoA — per-control inclusion/exclusion justification tied to the 6.1.3 risk-treatment process; the largest net-new ISO artifact SOC 2 lacks |
| [`iso-27001-isms-architect`](../../.claude/skills/iso-27001-isms-architect/SKILL.md) | Framework projection | ISMS per clauses 4–10; four-theme Annex A control selection; internal audit + management review cadence; Amd 1:2024 climate-context check |
| [`iso-42001-aims-architect`](../../.claude/skills/iso-42001-aims-architect/SKILL.md) | Framework projection | AIMS per clauses 4–10; AI risk assessment / treatment and AI system impact assessment; Annex A control-objective selection |
| [`soc2-trust-criteria-mapper`](../../.claude/skills/soc2-trust-criteria-mapper/SKILL.md) | Framework projection | TSC scoping — Security baseline plus which optional categories to attest; Type 1 vs Type 2 decision and audit-window planning |
| [`multi-framework-crosswalk`](../../.claude/skills/multi-framework-crosswalk/SKILL.md) | Cross-cutting | One control → 27001 Annex A + SOC 2 TSC + 42001 Annex A (+ AI RMF function) — the do-the-work-once engine between foundation and projections |
| [`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md) | Cross-cutting | Current state vs chosen framework(s) → prioritized gap list with remediation order and evidence gaps |
| [`ai-lifecycle-risk-manager`](../../.claude/skills/ai-lifecycle-risk-manager/SKILL.md) | Cross-cutting | NIST AI RMF GOVERN/MAP/MEASURE/MANAGE across the AI lifecycle; pairs with `iso-42001-aims-architect` |

**Already covered — the batch MAPS, it does not rebuild:** much of 27001's A.8 Technological
theme and SOC 2's Security category is already implemented by shipped skills — Phase 3
`tenant-isolation-reviewer`, `authorization-matrix-designer`, `audit-log-architect` (access
control, authz, logging substrate); Phase 4 `rls-policy-auditor`,
`multi-tenant-security-tester`, `secrets-identity-hardener` (access control and credential
custody), `secure-migration-reviewer` (change management), `supply-chain-security-reviewer`
(vendor/supply chain), `threat-modeler` (risk-assessment input), `static-analysis-reviewer` +
`security-pr-reviewer` (secure development). Phase 5's evidence pack is the raw material
`compliance-evidence-collector` formalizes into audit-window evidence; Phase 7's planned
`ai-governance-risk-reviewer` and the shipped Phase 1.5 governance pack are what a 42001 / AI
RMF audit points at for AI-specific operational control. The compliance skills produce the
mapping and auditor-consumable evidence on top of these; net-new implementation is mostly
limited to ISO management-system artifacts (SoA, internal audit, management review) and
evidence plumbing.

**Status: implemented (D9 — PR #21).** All 9 skills merged to `main` 2026-07-07 via PR #21
(merge commit `2df96f1`); validator target moved 86 → 95, exit 0. No phases renumbered. The
sequencing left open at banking time resolved as: after Phase 7.5 and the D11 rebrand,
before any Phase 8 batch.

### Engineering discipline expansion (D12) — candidate packs

**BANKED scope (D12, 2026-07-07) — 7 candidate packs, 42 named candidates; banked on-demand.
Built since banking: D12.1 (7 skills) and D12.3 (6 skills), both 2026-07-07 (D23); the
remaining packs stay candidates.** At 95 shipped skills the library covers the technical,
governance, and compliance stacks; this banks the engineering disciplines a senior/principal
engineer would compose alongside them that remain uncovered. **Standing rule recorded here
(D12): the library is NOT capped at 300 skills** — the 300-skill roadmap (D5) is the
strategic backlog the library was audited against, not a ceiling; packs open as coverage or
real engineering need demands, not to hit a count. Every skill below is *(candidate — not
built)*; pull-forward goes through the §4.1 batch rules and the §4.2 pre-generation plan
table like any other batch, and per D13 below, `skill-quality-reviewer` builds first if any
pack is pulled forward.

| Pack | Candidate skills *(all: candidate — not built)* | Pack rationale |
|---|---|---|
| **D12.1 Data engineering (P1) — ✅ all 7 built (D23, 2026-07-07)** | `schema-evolution-planner`, `streaming-event-architect`, `data-quality-monitor-designer`, `operational-vs-analytical-splitter`, `warehouse-lake-architect`, `pii-lifecycle-designer`, `data-migration-runbook-author` | Multi-tenant SaaS operational + analytical data as a first-class discipline. The `streaming-event-architect` ↔ `api-event-architect` internal-pipeline-vs-external-contract seam is pinned in trigger-evals on both directions. |
| **D12.2 Product engineering craft (P1) — ✅ all 5 built (D24, 2026-07-07)** | `pagination-cursor-designer`, `error-taxonomy-designer`, `edge-state-ux-designer`, `notification-webhook-ux-designer`, `mobile-viewport-craft` | API/UX craft distinct from contract design (Phase 3 `api-event-architect` owns the contract; these own the craft inside it). The `api-event-architect` seam is pinned in every skill's trigger-evals; `error-taxonomy-designer` (error MODEL) ↔ `edge-state-ux-designer` (rendering the error STATE) pinned both ways. |
| **D12.3 Performance engineering (P1) — ✅ all 6 built (D23, 2026-07-07)** | `profiling-methodology-designer`, `query-plan-reader`, `n-plus-one-detector`, `caching-strategy-designer`, `latency-budget-architect`, `frontend-perf-engineer` | Performance as an engineering discipline — distinct from the load-testing VALIDATION in D10 Tier 1 (`performance-test-harness` + `load-test-planner`, built in the same D23 batch): D12.3 designs for performance, D10 measures it — the seam is pinned in trigger-evals on BOTH sides. `latency-budget-architect` consumes (never sets) `slo-reliability-architect` targets. |
| **D12.4 Technical writing / docs engineering (P1) — ✅ all 8 built (D25, 2026-07-07)** | `readme-craftsman`, `adr-sequencer` (extends shipped `adr-writer` with longitudinal ADR management), `diataxis-doc-organizer`, `docs-as-code-architect`, `api-doc-generator-designer`, `contribution-guide-author`, `onboarding-doc-designer`, `docs-retention-index` (report P1, added by D15: numbered index governing every workflow doc's lifecycle — retention category, reason-to-keep, superseded-by, cleanup rule — mirrored by per-doc retention frontmatter; documentation retirement as an approvable operation) | Durable documentation as its own discipline. Three seams pinned in trigger-evals: `adr-sequencer` EXTENDS `adr-writer` (composes, no duplicate); `docs-retention-index`↔`skill-deprecation-planner` (DOC vs SKILL retirement, both ways); `api-doc-generator-designer`↔`api-event-architect` (generated reference vs contract). PART A of the D12.4+D12.7+D12.9+D14 two-PR batch. |
| **D12.5 PM / product engineering interface (P2) — ✅ all 6 built (D24, 2026-07-07)** | `requirements-gathering-facilitator`, `product-spec-writer` (a product spec, distinct from an ADR), `roadmap-under-uncertainty-planner`, `prioritization-frame-picker`, `feature-flag-rollout-strategist`, `sunset-deprecation-communicator` | The engineering/PM boundary. Two hard seams pinned both ways in trigger-evals: `product-spec-writer`≠`adr-writer`, and `sunset-deprecation-communicator`≠`skill-deprecation-planner` (product-feature sunset vs library-skill retirement). `feature-flag-rollout-strategist`≠`plan-entitlement-architect`/`authorization-matrix-designer`. |
| **D12.6 Growth / analytics engineering (P2) — ✅ all 4 built (D24, 2026-07-07)** | `event-schema-architect` (analytics counterpart to `api-event-architect`), `funnel-definition-designer`, `ab-test-designer` (design AND reading of results), `product-analytics-instrumenter` | User-facing product analytics, distinct from system-facing observability (Phase 6 `observability-operator` / `slo-reliability-architect`). Two THREE-way seams pinned in trigger-evals: `event-schema-architect`≠`api-event-architect`≠`streaming-event-architect`; `product-analytics-instrumenter`≠`observability-operator`≠`skill-usage-instrumenter`. |
| **D12.7 Staff+ IC craft (P2) — ✅ all 7 built (D26, 2026-07-07)** | `tech-spec-writer` (broader than an ADR), `design-review-facilitator`, `cross-team-dependency-negotiator`, `roadmap-to-commitments-translator`, `staff-scope-selector`, `promotion-packet-writer`, `phased-work-handoff-designer` (multi-stage sequenced work with binding decisions carried forward as evidence — distinct from `ai-closeout-reporter`, which reports ONE turn, and from `ai-sdlc-operating-model`, which frames the whole lifecycle) (build spec substantiated by report P9: decision-ID register carried across stages, changed-files + explicit not-touched lists, proven-invocation-command sections with tell-tale output, deviation flags) | Technical leadership without management authority. |

**D12.8 Operational workflow patterns — evidence-extracted (P1)** *(pack added by D15,
2026-07-07; **all 10 built 2026-07-07, D21** — the concrete, invocable rules of the
Zero Trust AI Engineering Discipline (Zet-AI Engineering for short), D16)*: patterns
extracted from a read-only audit of two
production multi-agent repositories ([`docs/research/aegis-workflow-extraction-report.md`](../research/aegis-workflow-extraction-report.md));
all HIGH confidence (multiple concrete artifacts each); product content stripped at
extraction; live identifiers templated as placeholders per report §6.3. The pack
(each **✅ built (D21)**, with the report pattern ID):

- `scoped-approval-register` (P2) — durable approval records with Status/Reason/Scope
  allowed/Scope FORBIDDEN/Evidence; the record format complementing `human-approval-boundary`
- `standing-approval-and-auto-advance` (P3) — governed anti-approval-fatigue layer: documented
  standing approval for the mechanical delivery loop within named scope, default-on merge
  after green with explicit opt-out phrase (as practiced in the source repos), phase-advance
  rule, reviewer-block path. MUST compose `agent-authorization-matrix` +
  `human-agent-trust-reviewer`; scope limit (house rule): standing approval may thin low-risk
  approvals (phase advance, the pre-merge mechanical loop) but never covers protected-branch
  merge or arming auto-merge — that authority stays human-only per
  `agent-authorization-matrix`, so a built skill must template default-on merge as an explicit
  opt-in deployment-profile choice, never its default; rationale cites the
  ungoverned-auto-merge incident already encoded in `agent-authorization-matrix` evals — the
  governance elements are what separate this pattern from that incident
- `local-ci-mirror-preflight` (P4) — derive local equivalents of every PR-triggered CI check,
  verify on clean mainline first, classify failures (PR-caused / pre-existing / infra /
  cannot-determine); per-commit, distinct from release-scoped review
- `risk-tiered-validation-selector` (P5) — machine classification of changes to VALIDATION
  depth with fail-closed-to-full default; routes validation cost where
  `change-classification-gate` routes approval
- `sharded-validation-with-resume` (P6) — named functional shards, persisted status,
  resume-after-timeout, uncategorized catch-shard, one aggregate required CI check
- `merge-is-deploy-governance` (P7) — standing pipeline governance when the platform
  auto-deploys on merge: PR validation as authoritative gate, branch-protection config
  recorded in-repo, accepted-risk window, revert-PR rollback
- `context-co-update-ci-gate` (P8) — CI fails PRs touching important paths without
  context-map updates; the write-back half of `agent-startup-context-gate`'s read loop
- `lane-authoring-guide` (P10) — pre-work evidence-cited authoring guide per parallel agent
  lane; planner-to-implementer knowledge transfer BEFORE work begins, distinct from handoffs
- `gated-deployment-prompt-template` (P11) — reusable operator prompt for risky operations
  with placeholders, stop conditions, backup-then-verify gating, and ETA ranges calibrated
  from a deployment-history index; uncited operational claims labeled unverified
- `chat-backlog-reconciliation` (P13) — cadenced extraction of chat-only decisions/backlog
  into dated repo docs, then audited against PR/source evidence per item

**Enrichment deltas for shipped skills** (recorded, to apply when each skill is next
touched — report §4 end + P15):

- `ai-closeout-reporter` — per-surface pass/fail + negative-path tables, skip decomposition,
  unqualified-complete only after every gap closed, preflight-evidence block; P15
  completion-baseline anchors — immutable PR/SHA/migration evidence pinned so finished work
  is never re-litigated
- `adr-writer` — certainty labels, status-column index
- `agent-memory-governance` — P15 anchors as memory content rule
- `ai-sdlc-operating-model` — hub-and-spoke vs per-tool-spoke topologies as documented
  options; one-tool-per-surface-per-phase collision rule
- cross-cutting certainty-label convention (confirmed / inferred / unknown /
  unverified-recommend-confirming) as a candidate shared writing rule

**D12.9 Architecture advisory** *(pack added by D20, 2026-07-07; ✅ `architecture-advisor` built (D26, 2026-07-07))*: the library's
`architecture-designer` produces a concrete target architecture and migration plan once the
rough shape is known, and `cloud-architecture-decider` advises on cloud provider/posture —
but nothing advises on the architecture STYLE/PARADIGM itself (monolith vs modular monolith
vs microservices vs event-driven vs serverless vs SOA, and hybrids). This pack fills that
gap:

- `architecture-advisor` *(✅ built — D26, 2026-07-07)* — an ADVISOR that recommends an
  architecture STYLE for what the user is building, with honest tradeoffs and a reasoned
  recommendation — NOT a mechanical selector. Its discipline:
  - Understand the need FIRST: interview for domain, load/traffic shape, team size and
    operational maturity, deployment constraints, scaling and change expectations, and
    consistency/latency needs — before advising.
  - Lay out only the GENUINELY RELEVANT candidate styles for that situation (from monolith,
    modular monolith, microservices, event-driven, serverless, service-oriented, and
    hybrids) — not a textbook dump of all of them.
  - Give pros and cons of each FOR THIS SPECIFIC CASE, not generic pros/cons.
  - Make a CLEAR recommendation WITH its reasoning, and state explicitly what would change
    the recommendation (the decision's sensitivity).
  - CORE NEUTRALITY PRINCIPLE: fit the recommendation to the actual situation; resist
    trend-chasing in BOTH directions — do not default to microservices because it is
    fashionable, nor to monoliths because it is contrarian-safe. Often the honest answer is
    a boring modular monolith, and the skill must be willing to say so.
  - Compose, do NOT overlap: `architecture-advisor` picks and justifies the PARADIGM;
    `architecture-designer` then designs the concrete target WITHIN that paradigm
    (component maps, boundaries, migration plan); `adr-writer` records the decision. Three
    distinct jobs in sequence. The advisor hands its recommendation to
    `architecture-designer`.
  - Likely auto-invocable (pure advisory/analysis, edits nothing) — to be confirmed at
    build time.
  - When built, to be checked by `skill-quality-reviewer` for trigger overlap against
    `architecture-designer`, `cloud-architecture-decider`, `saas-platform-architect`, and
    `domain-modeler`.

**D12.11 SaaS Architecture Depth** *(pack added by D30, 2026-07-08; STRONG
cluster of 10 ✅ built by D31, 2026-07-08 — ahead of the D12.10 SAST/DAST pack
as planned; the 4 LOW-PRIORITY candidates ✅ built by D32, 2026-07-08 (Build B),
pack now COMPLETE)*: net-new architecture-depth gaps surfaced by a private
read-only deep-audit of production multi-tenant SaaS patterns plus general
SaaS-architecture research (product-agnostic — evidenced by production
multi-tenant SaaS patterns; no product/vendor named). Two tiers: a **STRONG
cluster (10, build-first)** carrying strong real-world evidence, and a
**LOW-PRIORITY set (4, scale-stage or possibly-extension)**. Each candidate
records its scope and the exact seam(s) it must pin at build time; three
(`usage-metering-and-cost-attribution-pipeline-designer`,
`intra-tenant-scope-architect`, `share-link-access-architect`) are flagged
standalone-vs-extension for `skill-quality-reviewer` to confirm at build.
**Scheduling: this pack is positioned to build BEFORE the D12.10 SAST/DAST pack
that follows it** — the architecture-depth gaps are foundational product
surfaces, so when packs are pulled the strong cluster here runs first, ahead of
D12.10.

*STRONG cluster (10 — ✅ all built by D31, 2026-07-08):*

- `command-gateway-architect` *(✅ built — D31, 2026-07-08)* — design a single
  server-side-mediated write path (a command bus): a command registry + a
  per-command pipeline (validate → authenticate the actor from the token, never
  from the client → authorize → server-derive tenant/resource scope from trusted
  rows → idempotency → execute → emit audit + domain events → safe error
  envelope), plus the "no direct client writes for protected actions" invariant.
  SEAMS: `api-event-architect` (external contract, NOT internal dispatch),
  `authorization-matrix-designer` (the policy it ENFORCES), `audit-log-architect`
  (the records it emits); backlog components `validation-boundary-designer` /
  `idempotency-first-designer`.
- `realtime-subscription-architect` *(✅ built — D31, 2026-07-08)* — design real-time
  client delivery (WebSocket/SSE/DB-change subscriptions/presence): channel/topic
  model, authorize-at-subscribe-time (the per-tenant + per-user leak boundary),
  fan-out, scaling stateful connections, backpressure, reconnect/replay, presence.
  SEAMS: `streaming-event-architect` (server-internal backbone, NOT client push),
  `api-event-architect` (request/response + outbound webhooks),
  `notification-webhook-ux-designer` (UX, not transport).
- `background-job-orchestration-architect` *(✅ built — D31, 2026-07-08)* — design the
  async job/worker execution model: offload-from-request-path, worker pools,
  scheduled/cron jobs, job idempotency + resumability/checkpointing, retry/backoff,
  job DLQ, visibility timeouts, per-tenant fairness. SEAMS:
  `streaming-event-architect` (transport vs execution — pin hard),
  `performance-test-harness` / `load-test-planner` (they measure it).
- `horizontal-scalability-reviewer` *(✅ built — D31, 2026-07-08)* — review whether a
  system can scale out: statelessness / session externalization, connection
  pooling, sticky-session + in-memory-singleton smells, autoscaling +
  load-balancer config, graceful shutdown/draining. SEAMS:
  `slo-reliability-architect` (targets), `latency-budget-architect` (latency),
  `caching-strategy-designer` (caching).
- `search-architecture-designer` *(✅ built — D31, 2026-07-08)* — design
  search/discovery: full-text (pg `tsvector` / `pg_trgm`) vs external engine,
  indexing pipeline + freshness, relevance/ranking, per-tenant search isolation
  (leak boundary), faceting/pagination seam. SEAMS: `rag-security-architect`
  (AI/vector retrieval), `multi-tenant-data-architect` (data-store scoping),
  `pagination-cursor-designer` (pagination).
- `file-upload-storage-architect` *(✅ built — D31, 2026-07-08)* — design file/object
  storage & upload flows: direct-vs-proxied upload, signed URLs, tenancy by
  bucket/path prefix, size/type/content validation, malware scanning,
  image/derivative processing, retention/lifecycle, CDN, storage-cost posture.
  SEAMS: `pii-lifecycle-designer` (personal-data lifecycle), `rls-policy-auditor`
  (storage RLS).
- `usage-metering-and-cost-attribution-pipeline-designer` *(✅ built — D31,
  2026-07-08; resolved STANDALONE — not an extension of `saas-cost-architect`)* —
  design the metering → pricing → allocation → rollup → reconciliation
  data pipeline: a billing-safe usage-event table (no content), time-bounded rate
  cards, exact/estimated/allocated cost entries with idempotency keys, additive
  daily rollups, budgets + breach alerts, spend forecast, reconciliation. SEAMS:
  `saas-cost-architect` (unit-economics/drivers — NOT the ETL; **pin hard, the
  closest overlap**), `ai-cost-guardrail-designer` (AI budgets/rate-limits/
  kill-switch), `operational-vs-analytical-splitter` (the rollup is an analytical
  projection). **FLAG: standalone-vs-extension-of-`saas-cost-architect` —
  `skill-quality-reviewer` confirms at build time.**
- `synthetic-monitoring-architect` *(✅ built — D31, 2026-07-08)* — design ongoing
  black-box production monitoring: scheduled synthetic journeys/probes against the
  live app + third-party deps, a hard prod-safety contract (probes must not mutate
  prod or leak test fixtures), synthetic SLIs + alert-on-synthetic-failure,
  canary/heartbeat probes, result capture/routing. SEAMS:
  `performance-test-harness` / `load-test-planner` (pre-release measurement),
  `playwright-e2e-engineer` (CI E2E, not prod-safe scheduled probes),
  `slo-reliability-architect` (defines SLOs, not the probes),
  `observability-operator` (white-box instrumentation vs external black-box).
- `offline-first-sync-architect` *(✅ built — D31, 2026-07-08)* — design the client
  offline data layer: write-while-offline queue, optimistic apply + rollback on
  server reject, conflict detection/resolution (LWW/merge/CRDT/manual), local
  persistence, background sync, online↔offline reconciliation + integrity. SEAMS:
  `edge-state-ux-designer` (offline/optimistic-rollback UX STATES, not the sync
  engine), `caching-strategy-designer` (server/distributed cache),
  `realtime-subscription-architect` (live ONLINE push).
- `admin-console-architect` *(✅ built — D31, 2026-07-08; was HIGH PRIORITY
  pull-forward within the strong cluster, the most operationally mature pattern
  in the audited portfolio)* — design the internal ops/support/superadmin
  surface: cross-tenant read/write with mandatory audit, impersonation /
  support-mode-as-user with hard boundaries + audit, least-privilege admin tiers
  (view-ops vs write-ops vs superadmin), break-glass/elevation workflows, and the
  operator control-plane (health dashboards, manual failover/retry, data-repair
  ops). SEAMS: `authorization-matrix-designer` (owns the authz POLICY +
  impersonation policy — this owns the CONSOLE architecture that ENFORCES it),
  `observability-operator` (telemetry vs the action surface),
  `agent-authorization-matrix` (AI-agent authority, not human-admin),
  `incident-response-runbook` (reactive playbook the console's tools serve).

*LOW-PRIORITY set (4 — ✅ all built by D32, 2026-07-08; both standalone-vs-
extension flags resolved STANDALONE at build time):*

- `cell-based-architecture-designer` *(✅ built — D32, 2026-07-08; **LOW** —
  scale-stage only, most SaaS never needs it)* — cell / blast-radius partitioning
  (self-contained stack subset, tenant→cell mapping, thin router, cell-by-cell
  deploy, cross-cell concerns, migration). SEAMS: `saas-platform-architect`
  (per-component isolation, not whole-stack cells), `architecture-advisor` (its
  style menu omits cells — this fills that), `agent-containment-reviewer` (agent
  blast-radius).
- `data-partitioning-sharding-strategist` *(✅ built — D32, 2026-07-08; **LOW** —
  scale-stage, "don't shard prematurely")* — OLTP partitioning/sharding for write
  scale (shard-key selection, range/hash/list partitioning, resharding a hot
  tenant, cross-shard costs, don't-shard-prematurely gate). SEAMS:
  `multi-tenant-data-architect` (isolation scoping, not throughput sharding),
  `warehouse-lake-architect` (analytical partitioning),
  `operational-vs-analytical-splitter`.
- `intra-tenant-scope-architect` *(✅ built — D32, 2026-07-08; **LOW**; **FLAG
  RESOLVED STANDALONE (D32)** — ~60% distinct from `multi-tenant-data-architect`,
  well above the ~40% duplicate threshold)* — a second mandatory data-scoping axis
  below the tenant (location/site/org-unit): per-user scope assignment, an RLS
  predicate on scoped tables, scope-restricted vs tenant-wide roles, propagation,
  and migration to add the axis live. SEAMS: `tenant-modeler` (tenant hierarchy),
  `multi-tenant-data-architect` (`tenant_id` scoping),
  `authorization-matrix-designer` (roles×permissions, not a row-filter dimension).
- `share-link-access-architect` *(✅ built — D32, 2026-07-08; **LOW**; **FLAG
  RESOLVED STANDALONE (D32)** — ~60% distinct from `authorization-matrix-designer`,
  well above the ~40% duplicate threshold)* — guest/public share-link access (opaque
  expiring/revocable tokens, guest sessions, optional password/OTP gating,
  per-link scope, enumeration/abuse defense, audit). SEAMS:
  `authorization-matrix-designer` (member roles, not anyone-with-the-link),
  `api-event-architect` (API credentials/webhook signing).

**Pull-forward priorities (existing backlog, NOT new D12.11 candidates)** — the
same audit gives strong real-world evidence to pull these forward, HIGH priority,
from their existing expansion backlogs (they are prioritization signals here, not
part of the 14 D12.11 candidates): `idempotency-first-designer` (Phase 2 —
"table-stakes for any mutating API"; TOP pull-forward), the unnamed
**rate-limit-design** row (Phase 4 — general per-tenant/plan API rate limits +
noisy-neighbor defense; needs a NAME when pulled), and
`resilience-architecture-reviewer` (Phase 6 — circuit
breakers/bulkheads/timeouts/graceful degradation).

**D12.10 Security scanning & orchestration** *(pack added by D27, 2026-07-08; **all 3 BUILT by D44, 2026-07-16** — the LAST banked
capability, built after the library-wide `skill-quality-reviewer` sweep (D33) as planned)*: the library's existing security skills are
JUDGMENT skills — `static-analysis-reviewer` triages scanner findings it is handed,
`supply-chain-security-reviewer` covers dependencies/provenance — but nothing ORCHESTRATES
the scanning itself: running a SAST suite over a repo, dynamic testing against a running
app, or aggregating a whole-repo security scan into one report. This pack fills that gap.
Core principle for all three (per the Zero Trust AI Engineering Discipline, D16, and
`agent-authorization-matrix`): orchestrate-and-REPORT — an AI security scanner may READ a
repo and run scanners, but must never autonomously fix, open PRs, or change settings; every
action is handed to a human.

- `security-scan-orchestrator` *(built — D44)* — guides an assistant to
  clone/access a repo (READ-ONLY) and run the full security-scan suite (SAST +
  dependency/SCA + secret scanning + IaC/config scanning), then AGGREGATE findings into one
  prioritized report. Orchestrates and REPORTS; recommends fixes but NEVER applies them,
  opens no PRs, changes no settings — any action is handed to a human (per Zero Trust AI
  Engineering Discipline / `agent-authorization-matrix`). Composes with
  `static-analysis-reviewer` (which does the true-positive/false-positive judgment on the
  SAST output) and `supply-chain-security-reviewer` (dependency/provenance). Tool-agnostic
  (references scanner CATEGORIES, not one vendor's CLI).
- `sast-orchestration-designer` *(built — D44)* — selects and configures the
  right static-analysis approach for a codebase/language, runs it, and hands findings to
  `static-analysis-reviewer` for triage. Compose-don't-duplicate:
  `static-analysis-reviewer` JUDGES findings; this one PRODUCES them.
- `dast-safety-harness-designer` *(built — D44)* — designs dynamic (running-app)
  security testing with MANDATORY guardrails: only against systems the user owns and has
  WRITTEN authorization to test, never production without explicit human sign-off, scoped
  target allowlists, rate limits, and a documented blast-radius/rollback. DAST sends attack
  traffic at live software — treat it as a side-effecting operation requiring
  authorization; the skill DESIGNS the harness/plan, it does not autonomously attack
  anything. Discriminate from `multi-tenant-security-tester` (which tests tenant-isolation
  specifically).

### Library meta / self-application (D13) — candidate skills

**BANKED scope (D13, 2026-07-07) — 5 candidate skills; SCOPE COMPLETED: `skill-quality-reviewer`
built 2026-07-07 (first pull, D18); the remaining 4 built 2026-07-07 (D22).** The
library validates its own structure (`scripts/validate-skills.py`) but had no skills that
apply its own discipline to itself. These candidates turn the generation standard, the eval
convention (D3), and today's manual PR review flow into reusable skills.
`skill-quality-reviewer` is the highest-leverage candidate: **if any D12 pack is later pulled
forward, `skill-quality-reviewer` builds FIRST** so subsequent additions audit themselves —
satisfied ahead of any D12 pull (built 2026-07-07, D18).

| Candidate skill *(status per row)* | One-line rationale |
|---|---|
| `skill-quality-reviewer` — **✅ built (D18, 2026-07-07)** | Audits a skill against [`docs/skill-generation-standard.md`](../skill-generation-standard.md) as the JUDGMENT layer above the validator (which keeps the mechanical checks: sections, lengths, registration, name collisions): trigger quality, overlap/collision with colliders named, duplication/extension, eval integrity, section substance, scope, invocation posture — so every future addition gets the review the standard demands. |
| `eval-runner-designer` — **✅ built (D22, 2026-07-07)** | Specs what an eval runner should do (inputs, pass criteria, reporting); it does NOT build the runner — closes the design gap D3 left open ("there is no eval runner yet"). |
| `skill-usage-instrumenter` — **✅ built (D22, 2026-07-07)** | Telemetry design: which skills are invoked vs unused, trigger-match rate, false-positive-rate estimation — evidence for pruning and trigger fixes. |
| `skill-deprecation-planner` — **✅ built (D22, 2026-07-07)** | Safe skill sunset — mark deprecated, redirect triggers, remove from catalog — so the library can shrink as deliberately as it grows. |
| `library-diff-reviewer` — **✅ built (D22, 2026-07-07)** | Audits a skill-adding PR the way manual review does today: validator run, cluster-collision check, catalog integrity, incident-eval verification. |

### Framework refresh & source-currency discipline (D14) — candidate skills

**BANKED scope (D14, 2026-07-07) — 3 candidate skills; ✅ all 3 built (D26, 2026-07-07): `framework-edition-tracker`, `framework-mapping-refresher`, `source-currency-auditor`.** The
framework mappings banked and shipped so far (D6/D7/D8 OWASP maps, D9 compliance batch) are
point-in-time snapshots of external standards that revise on their own cadence. These
candidates give the library a refresh discipline so external-truth drift is detected instead
of silent — distinct from D12 (breadth) and D13 (self-quality): D14 governs currency with
EXTERNAL truth.

| Candidate skill *(all: candidate — not built)* | Purpose |
|---|---|
| `framework-edition-tracker` | Pins the editions cited by D6/D7/D8/D9; detects when a new edition ships; produces a delta report WITHOUT auto-updating any mapping. Highest-leverage of the three — pull forward when the first new edition drops. |
| `framework-mapping-refresher` | Given an edition delta, proposes the specific updates to affected skill descriptions, references, and coverage maps; human review required before any change lands. |
| `source-currency-auditor` | Audits skills citing external sources against a known-good source list; flags citations older than N months for re-verification. |

### Phase 8 — Backlog expansion (NEW in v4, ported from execution plan §8)
Convert the remaining backlog — the original 300-skill roadmap, per the D12 standing rule a
300+ target backlog (ship on demand and framework coverage, not count) — into executable
skills **in validated batches** under the batch rules in §4 below. Run only after
Phases 0–7.5 validate cleanly.

**Tracked backlog items — Phase 4 × OWASP Top 10:2025 (web app) gap audit (D8):**

- `security-logging-alerting-architect` *(✅ built, D28, 2026-07-08)* — closes A09:2025 Security
  Logging and Alerting Failures: security-event detection coverage, alerting rules, and
  response wiring; complements Phase 3 `audit-log-architect` (which records, but does not
  detect or alert).
- `error-handling-security-reviewer` *(✅ built, D28, 2026-07-08)* — closes A10:2025 Mishandling
  of Exceptional Conditions: fail-closed defaults, error-path authorization, exception-driven
  logic bypass, leak-free error responses.

Per D8, uncovered web-app categories land here as backlog items — not as a new phase and not
as changes to the shipped Phase 4 list.

---

## 4. Ported from the execution plan into v4

### 4.1 Phase 8 batch rules (now part of canonical v4)
- **Max 20 skills per pass.**
- **Merge** duplicate/overlapping skills instead of creating noisy variants; prefer one
  strong skill over five weak ones.
- **Add `evals/trigger-evals.json`** for any skill whose description overlaps an existing skill.
- **Update README + catalog after each batch; run the validator after each batch.**
- **Create a changelog entry** per batch.
- **Stop** if generated skills become repetitive, too long, or weakly differentiated.

### 4.2 Pre-generation plan table (required before writing any skill)
Both tracks require this; it is canonical. Before creating skills in any phase, emit:

| Skill name | Category | Purpose | Trigger description | User-invocable? | Auto-invocable? | Supporting files | Eval cases |
|---|---|---|---|---|---|---|---|

### 4.3 Validator checks (union of both tracks — now enforced by `scripts/validate-skills.py`)
- Each skill dir has `SKILL.md`; frontmatter parses; `name` matches directory.
- `description` present and < 1024 chars.
- `SKILL.md` < 500 lines.
- No broad `allowed-tools`.
- **Catalog integrity:** every real skill is listed in `docs/skills-catalog.md` and `README.md`;
  the catalog/README claim no skills that do not exist.
- **Eval convention:** every real skill has `evals/evals.json` (structural existence + JSON parse).
- **Trigger-evals:** `evals/trigger-evals.json` is validated as JSON when present (Phase 8 requires
  it for overlapping skills).
- Bundled-name collision: no skill name shadows a reserved bundled skill name; no duplicate names.

---

## 5. Recorded decisions

- **D1 — v4 pair is canonical.** Execution plan → historical (§1).
- **D2 — Real subagents live at `.claude/agents/` with a read-only default posture.** This
  supersedes v4's earlier suggestion to store agent prompts in `docs/agents/agent-orchestrator-prompts.md`.
  The seven real subagent files ARE the agent layer; they must **not** duplicate skill bodies —
  they compose skills. Mapping from v4's orchestrator roles to the real subagents:

  | v4 orchestrator role | Real subagent (`.claude/agents/`) |
  |---|---|
  | Principal Claude Architect Agent | `principal-architecture-reviewer` |
  | SaaS Security and Tenant Isolation Agent | `secure-saas-reviewer` |
  | QA Automation and Release Evidence Agent | `qa-automation-lead` |
  | Full Codebase Audit Agent | `full-codebase-auditor` |
  | Senior Troubleshooting Agent | `senior-troubleshooting-lead` |
  | AI Security and LLM Systems Agent | `ai-security-red-team-reviewer` |
  | Release Captain Agent | `release-readiness-reviewer` |

- **D3 — Evals are a repo convention, structurally validated only.** The validator checks that
  `evals/evals.json` exists and parses (and `trigger-evals.json` parses when present). **There is
  no eval runner yet.** Building/using a runner is deferred; do not claim evals "pass," only that
  they are present and well-formed.
- **D4 — Phase 1 is the operating-discipline pack** (the 8 in §3), not the execution plan's
  architecture-heavy Phase 1. Architecture skills move to Phase 2.
- **D5 — 300-skill roadmap is the backlog/capability map, not a batch command.** Executable skills
  are built phase-by-phase; the remainder flows through Phase 8 batches.
- **D6 (2026-07-06) — Phase 7 is anchored to the OWASP Top 10 for LLM Applications (2025).**
  Canonical Phase 7 list expands 10 → 14 (adds `sensitive-disclosure-guard`,
  `model-poisoning-reviewer`, `system-prompt-leakage-reviewer`, `ai-misinformation-guard`).
  Rationale: anchor the AI-security pack to a current published framework rather than an
  ad-hoc list. Source: <https://genai.owasp.org/llm-top-10/>. Coverage map in §3 Phase 7.
- **D7 (2026-07-06) — Phase 7.5 (Agentic AI security) is added after Phase 7, anchored to
  OWASP Agentic Top 10 (ASI01–ASI10); it extends the LLM Top 10 (D6).** Rationale: agentic
  risk builds on top of LLM risk, so the pack runs immediately after Phase 7, and it is too
  central to this repo's agentic workflows to defer into the generic Phase 8 backlog.
  Canonical Phase 7.5 = 6 new skills (ASI08 and ASI10 merge into `agent-containment-reviewer`)
  plus 3 extensions of existing skills, built at Phase 7.5 — not now. Phases 0–8 keep their
  numbers; the shipped validator skill-count target is unchanged. Source:
  <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>.
  Coverage map in §3 Phase 7.5.
- **D8 (2026-07-06) — Phase 4 is cross-checked against the OWASP Top 10 for Web Application
  Security; uncovered categories are tracked as Phase 8 backlog.** Audited against the current
  released edition, OWASP Top 10:2025 (A01:2025–A10:2025). Source:
  <https://owasp.org/www-project-top-ten/> (category list: <https://owasp.org/Top10/2025/>).
  Result: 6 covered, 2 partial (A02 Security Misconfiguration, A04 Cryptographic Failures),
  2 gaps (A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional
  Conditions) — gaps recorded as candidate skills in the §3 Phase 8 backlog
  (`security-logging-alerting-architect`, `error-handling-security-reviewer`). Coverage map
  in §3 Phase 4. This is a gap audit of shipped work: no skills created or changed, no phases
  renumbered, validator target unchanged. Third distinct framework: separate from the OWASP
  Top 10 for LLM Applications (D6) and from the OWASP Agentic Top 10 for 2026 (D7, Phase 7.5).
- **D9 (2026-07-06) — A Compliance & Governance batch (ISO 27001:2022 + ISO 42001:2023 + SOC 2
  Type 2, with NIST AI RMF 1.0 as companion) was banked as a future batch targeted AFTER
  Phase 7; implemented 2026-07-07 via PR #21 (merge commit `2df96f1`).** Subsection in §3,
  after Phase 7.5. Rationale: as an AI SaaS vendor selling into US
  enterprise and EU markets, these converge into procurement requirements (SOC 2 in US
  enterprise sales; 27001 via EU NIS2 supply-chain demand on customers; 42001 emerging in EU
  public procurement) — vendor-market rationale, not a standards claim. Architecture: **one
  shared control foundation + framework-specific projections + a crosswalk** (9 skills,
  already merged — one evidence collector, one gap auditor, one SoA author across
  frameworks), NOT three parallel skill sets; published crosswalks put cross-framework control
  overlap at ~60–80% (industry estimate, not a standard-derived number). The batch is
  substantially a **mapping + evidence layer** over controls already shipped in Phases 3/4
  (and the Phase 5 evidence pack) — it does not rebuild them. Precision: SOC 2 is an AICPA
  **attestation** (CPA examination); 27001/42001 are **certifiable** management-system
  standards. Distinct from Phase 1.5 (operational agent governance) and the OWASP maps
  (D6/D7/D8). All 9 skills built and merged via PR #21 (2026-07-07, merge commit `2df96f1`);
  no phases renumbered; validator target moved 86 → 95, exit 0. Sources fetched 2026-07-06
  (<https://www.iso.org/standard/27001> and
  <https://www.iso.org/standard/42001> returned HTTP 403 to automated fetch, so standard
  structure was verified from official-distributor preview PDFs of the standards themselves):
  - **ISO/IEC 27001:2022 preview PDF** (title page, TOC, Foreword/Introduction):
    <https://cdn.standards.iteh.ai/samples/82875/726bcf58250e43d9a666b4d929c8fbdb/ISO-IEC-27001-2022.pdf>
    — **verified:** third edition 2022-10; ISMS requirements; clauses 4–10; "Annex A
    (normative) Information security controls reference"; third edition replaces 27001:2013.
  - **ISO/IEC 42001:2023 preview PDF**:
    <https://cdn.standards.iteh.ai/samples/81230/4c1911ebc9a641fcb6ee21aa09c28ad3/ISO-IEC-42001-2023.pdf>
    — **verified:** first edition 2023-12; AIMS requirements ("requirements for establishing,
    implementing, maintaining and continually improving an AI management system"); clauses
    4–10 incl. 6.1.2–6.1.4 (AI risk assessment / AI risk treatment / AI system impact
    assessment); "Annex A (normative) Reference control objectives and controls"; Annex B
    (normative) / C, D (informative); drafted by ISO/IEC JTC 1/SC 42.
  - **Amd 1:2024:** ISO catalog entry "ISO/IEC 27001:2022/Amd 1:2024 — … Amendment 1: Climate
    action changes" <https://www.iso.org/standard/88435.html> — **title/existence verified via
    search listing (page itself 403); the exact 4.1/4.2 inserted text is from secondary
    summaries (CompliancePoint, High Table, Iseo Blue) — flagged, not fetched from ISO.**
  - **27001 Annex A counts** (93 = A.5×37 + A.6×8 + A.7×14 + A.8×34):
    <https://www.isms.online/iso-27001/annex-a-2022/> plus corroborating vendor references —
    **flagged: secondary sources; verify against the Annex A table before citing.**
  - **42001 Annex A counts:** secondary sources conflict (38 controls / 9 objectives vs 42
    objectives) — **deliberately not stated; unverified.**
  - **SOC 2 / TSC (AICPA):**
    <https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services>,
    <https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022>,
    <https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2>
    — **verified:** five categories (Security, Availability, Processing Integrity,
    Confidentiality, Privacy); TSC issued by the Assurance Services Executive Committee (2017
    TSC with revised Points of Focus 2022); use in "attestation or consulting engagements";
    SOC 2 titled "Reporting on an Examination of Controls at a Service Organization…".
    **Flagged:** Type 1 vs Type 2 definitions and "Security = required common-criteria
    baseline" are NOT on AICPA's fetchable pages — corroborated via CPA-firm sources
    (Schellman, Linford & Co); the defining text is the paywalled AICPA SOC 2 guide.
  - **NIST AI RMF:** <https://www.nist.gov/itl/ai-risk-management-framework> and
    <https://airc.nist.gov/airmf-resources/airmf/5-sec-core/> — **verified:** AI RMF 1.0
    released 2023-01-26, voluntary; "The Core is composed of four functions: govern, map,
    measure, and manage"; govern is cross-cutting; Generative AI Profile NIST-AI-600-1
    (2024-07-26); NIST notes AI RMF 1.0 is being revised.
  - The **~60–80% overlap** figure is an industry crosswalk estimate — **not a
    standard-derived number.**
- **D10 (2026-07-07) — Phase 5 QA expansion backlog is prioritized in three tiers from a gap
  audit of category 06 vs shipped skills; Tier 1 headlined by performance/load testing as the
  largest uncovered risk for a multi-tenant SaaS. Build timing: after the core phases (7, 7.5)
  or on demand; no skills built now.** Audit baseline: the 16 shipped Phase 5 skills (the 13
  canonical plus `integration-test-designer` #184, `api-contract-test-designer` #185, and
  `accessibility-test-harness` #204, pulled forward at ship time), plus QA coverage living
  cross-phase (#186 RLS testing → Phase 4 `multi-tenant-security-tester` /
  `rls-policy-auditor`; #182 validation-tier selection → Phase 1
  `change-classification-gate`). Overlapping roadmap items are merged, not multiplied:
  #205+#206 (may merge into one skill at build time), #214+#215, #226+#227, #200+#201,
  #211+#212. Items already owned by shipped skills are mapped once in the backlog section,
  not re-listed as candidates; `acceptance-criteria-tester` keeps its existing deferral note.
  Docs-only: no skills created, no phases renumbered, validator skill-count targets
  unchanged. Backlog + coverage mapping in §3 Phase 5.
- **D11 (2026-07-07) — Project identity adopted: "Project Aegis", identity line "Project
  Aegis — Shield of the agent fleet", tagline "Discipline before code. Evidence before
  merge."** The name carries three layers: the divine shield of Zeus and Athena; the Navy's
  Aegis, shield of the fleet — fitting for a veteran-founded project whose operating model
  is a fleet of agents; and a shield proven in use. Several skills' eval cases are drawn
  from real incidents this project absorbed during its own construction (an unauthorized
  auto-merge, stale-memory session collisions, an empty-directory build). Docs-only rebrand:
  README title/intro block, catalog header, and this entry; no skills created or changed; no
  phases renumbered; validator skill count unchanged (86). The GitHub repo rename
  (Claude-Skills → Project-Aegis) is a manual Settings action outside this change; the
  rename was observed already live during this pass (push to the old URL returned "This
  repository moved … Project-Aegis.git" and redirected automatically). README/catalog carry
  no badges or absolute repo URLs (verified); local git remotes still pointing at the old
  URL keep working via redirect but should be updated in a follow-up.
- **D12 (2026-07-07) — Seven engineering-discipline candidate packs (~40 candidate skills)
  are banked as on-demand scope; the library is NOT capped at 300 skills.** All on-demand:
  packs open as coverage or real engineering need demands, not to hit a count. Rationale: at
  95 skills the library covers the technical, governance, and compliance stacks; D12 records
  the engineering domains a senior/principal engineer would compose from that remain
  uncovered — data engineering, product engineering craft, performance engineering,
  technical writing / docs engineering, the PM/engineering interface, growth/analytics
  engineering, and Staff+ IC craft. Docs-only banking: no skills built now, no phases
  renumbered, validator skill-count target unchanged (95). Pack detail and per-pack
  rationales in §3.
- **D13 (2026-07-07) — Five library-meta / self-application candidate skills are banked**
  (`skill-quality-reviewer`, `eval-runner-designer`, `skill-usage-instrumenter`,
  `skill-deprecation-planner`, `library-diff-reviewer`). `skill-quality-reviewer` is the
  highest-leverage candidate; if any D12 pack is later pulled forward, build
  `skill-quality-reviewer` FIRST so subsequent additions audit themselves. Docs-only
  banking: no skills built now; validator skill-count target unchanged (95). Detail in §3.
- **D14 (2026-07-07) — Three candidate skills for framework refresh & source-currency
  discipline are banked** (`framework-edition-tracker`, `framework-mapping-refresher`,
  `source-currency-auditor`). Rationale: the D6–D9 mappings and any future framework skill
  are point-in-time — the underlying standards revise on their own cadence (the OWASP LLM
  Top 10 roughly annually, ISO standards periodically, the EU AI Act still finalizing);
  without a refresh discipline the compliance and security mappings drift silently.
  `framework-edition-tracker` is the highest-leverage candidate — pull it forward when the
  first new edition drops. D14 governs how the library stays current with EXTERNAL truth;
  distinct from D12 (breadth) and D13 (self-quality). Docs-only banking: no skills built
  now; validator skill-count target unchanged (95). Detail in §3.
- **D15 (2026-07-07) — Evidence-extracted operational workflow patterns banked:** 10 new
  candidates as pack D12.8, `docs-retention-index` added to D12.4, and enrichment notes
  recorded against 3 banked candidates and 5 shipped skills. Source: read-only audit of two
  production multi-agent repositories, report committed at
  [`docs/research/aegis-workflow-extraction-report.md`](../research/aegis-workflow-extraction-report.md);
  all extractions HIGH confidence except P15 (MEDIUM, recorded as enrichment not skill);
  product content stripped at extraction; live identifiers in source docs must be templated
  as placeholders in any derived skill (report §6.3). These patterns carry a stronger
  evidence tier than practice-from-memory: each cites concrete repo artifacts. No skills
  built; no shipped skill modified; validator target unchanged.
- **D16 (2026-07-07) — Zero Trust AI Engineering Discipline coined and documented** at
  [`docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`](../ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md).
  Tagline "Never trust, always verify — every step of the lifecycle. / Assume drift. Demand
  evidence. Track everything.", deliberately mirroring the Zero Trust security motto. Applies
  "never trust, always verify" to the whole SDLC to prevent drift and rot; its concrete rules
  are the D12.8 patterns; it is the doctrine Aegis itself operates under. Distinct from
  classic network Zero Trust. No skills built; this is doctrine, not a skill.
- **D17 (2026-07-07) — README reframed to present Aegis as an operating system for
  engineering software with AI, governed by Zero Trust AI Engineering Discipline,** with a
  "How to use this" operator guide and a "Map of the system" navigation section. Additive
  only; all prior README content (skill catalog, phase plan, validation, CI) preserved.
  No skills built.
- **D18 (2026-07-07) — `skill-quality-reviewer` built (first pull from the D13
  library-meta scope);** the judgment layer atop `scripts/validate-skills.py`, auditing
  trigger quality, overlap/collision, duplication, eval integrity, and section substance
  that the mechanical validator cannot check. Composes the manual skill-review discipline
  used across this project into an invocable skill. Pure review skill (verdict report only,
  edits nothing) → model-invocable. The other four D13 candidates
  (`eval-runner-designer`, `skill-usage-instrumenter`, `skill-deprecation-planner`,
  `library-diff-reviewer`) remain candidate — not built; the `library-diff-reviewer` seam
  (whole skill-adding PR vs ONE skill's quality) is pinned in the new skill's
  trigger-evals. 95→96 skills.
- **D19 (2026-07-07) — `agent-governance-audit` retrieval commands fixed and seams
  added,** per the first `skill-quality-reviewer` audit finding live-verified command
  failures in the skill's flagship merge-authority control: `timelineItems` removed
  from the `gh pr view --json` field list, `pulls/<n>/events` → `issues/<n>/timeline`,
  and the armed-auto-merge timeline event documented as strategy-specific
  (`auto_merge_enabled` / `auto_squash_enabled` / `auto_rebase_enabled` — on PR #7,
  the incident this control was built from, the actual event is `auto_squash_enabled`).
  `release-readiness-reviewer` (forward ship/merge gate vs retrospective
  did-it-follow-process verdict) and `agent-authorization-matrix` (audit-what-happened
  vs codify-the-authority-rule) seams added to the description/overlaps/trigger-evals;
  the should-not-soften eval retyped to the `_template` stop-condition convention
  (`should_trigger` / `triggers: true`). All fixed commands live-verified against this
  repo. No new skill; 96 skills unchanged. Neighbor follow-up (`ai-closeout-reporter`
  yield clause + trigger-evals) tracked separately.
- **D20 (2026-07-07) — `architecture-advisor` banked as a D12 candidate (candidate — not
  built):** an advisor that recommends an architecture style/paradigm (monolith / modular
  monolith / microservices / event-driven / serverless / SOA / hybrids) for what the user
  is building, with situation-specific pros/cons and a reasoned, neutrality-disciplined
  recommendation — NOT a mechanical selector. Fills the gap upstream of
  `architecture-designer` (which designs the concrete target within a chosen paradigm) and
  distinct from `cloud-architecture-decider` (provider/posture). Composes advisor →
  designer → adr-writer. Anti-trend-chasing neutrality is a core principle. On-demand; not
  built. Banked as pack D12.9 in §3; docs-only: no skill built, no phases renumbered,
  validator skill-count target unchanged (96).
- **D21 (2026-07-07) — D12.8 operational workflow patterns built:** 10 evidence-extracted
  skills (`scoped-approval-register`, `standing-approval-and-auto-advance`,
  `chat-backlog-reconciliation`, `context-co-update-ci-gate`, `lane-authoring-guide`,
  `local-ci-mirror-preflight`, `risk-tiered-validation-selector`,
  `sharded-validation-with-resume`, `merge-is-deploy-governance`,
  `gated-deployment-prompt-template`) — the concrete, invocable rules of the Zero Trust AI
  Engineering Discipline (D16). Product-agnostic, sourced from
  [`docs/research/aegis-workflow-extraction-report.md`](../research/aegis-workflow-extraction-report.md).
  96→106 skills. Every skill ships `evals/evals.json` + `evals/trigger-evals.json` with
  discriminating cases against its named composed neighbor (and against its in-batch
  siblings for the approval and validation clusters); 9 of 10 model-invocable,
  `standing-approval-and-auto-advance` manual-only (it authors standing autonomy — the
  `agent-authorization-matrix` reasoning); its merge-after-green is templated strictly as
  an opt-in deployment-profile choice per the D15 house rule, rationale citing the
  ungoverned-auto-merge incident. Embedded gh/git commands follow the D19 corrections
  (strategy-specific auto-merge events; squash commits revert as ordinary commits).
  `docs-retention-index` (P1, D12.4) and the enrichment deltas remain separate. To be
  checked by `skill-quality-reviewer` before final trust.
- **D22 (2026-07-07) — D13 library-meta scope completed:** 4 remaining meta-skills built
  (`library-diff-reviewer`, `eval-runner-designer`, `skill-usage-instrumenter`,
  `skill-deprecation-planner`) joining the earlier `skill-quality-reviewer` (D18).
  106→110 skills. These operate ON the skill library itself; product-agnostic (apply to
  any skill library). Seams honored and pinned in trigger-evals on both sides:
  `library-diff-reviewer` owns the whole skill-adding/modifying/retiring PR and composes
  `skill-quality-reviewer` as its single-skill inner loop (the D18 seam, now built);
  `eval-runner-designer` designs eval EXECUTION without claiming a runner exists (the D3
  convention stands until a built runner produces real runs); `skill-usage-instrumenter`
  designs the usage-evidence layer under strict minimization (skill names and coarse enums
  only — never prompt content or user identifiers) with a rare-but-critical exemption;
  `skill-deprecation-planner` stages skill retirement (mark → redirect → remove, rollback
  per stage, squash removal reverts as one ordinary commit per the D19 corrections) and
  pins the SKILL-vs-DOC seam against the still-banked `docs-retention-index` (D12.4). All
  four are pure review/design skills (edit nothing) → model-invocable.
  `skill-quality-reviewer`'s own description/trigger-evals annotations updated in the same
  change ("library-diff-reviewer — not built" would have become false on merge). To be
  checked by `skill-quality-reviewer` before final trust.
- **D23 (2026-07-07) — Data engineering (D12.1, 7 skills), Performance engineering
  (D12.3, 6 skills), and QA Tier 1 performance/load validation (D10, 2 skills) built.**
  110→125 skills, one PR (three pack commits: D12.1, D12.3, D10 — clean split boundaries;
  the batch was NOT split into multiple PRs). D12.1: `schema-evolution-planner`,
  `streaming-event-architect`, `data-quality-monitor-designer`,
  `operational-vs-analytical-splitter`, `warehouse-lake-architect`,
  `pii-lifecycle-designer`, `data-migration-runbook-author`. D12.3:
  `profiling-methodology-designer`, `query-plan-reader`, `n-plus-one-detector`,
  `caching-strategy-designer`, `latency-budget-architect`, `frontend-perf-engineer`.
  D10 Tier 1: `performance-test-harness`, `load-test-planner` — built as TWO skills
  (the §3 row's may-merge option declined at the pre-generation plan table: instrument
  vs traffic plan are different deliverables with a pinned sibling seam). **D12.3
  designs FOR performance; D10 MEASURES it — seam pinned in trigger-evals both sides**
  (harness thresholds are CONSUMED from `latency-budget-architect` /
  `slo-reliability-architect`, never invented). The highest external-collision seam —
  `streaming-event-architect` (internal pipeline) vs `api-event-architect` (external
  contract) — is pinned hard in both skills' trigger-evals. Product-agnostic (perf/data
  tool references kept generic/illustrative — EXPLAIN-style plans, stream platforms,
  load drivers by class, never one product's CLI). All 15 are design/analysis skills
  producing specs/plans/verdicts and editing nothing → model-invocable; the three that
  could touch live systems (profiling, harness, load) carry Stop Conditions forbidding
  execution against production without human approval. Embedded commands follow the D19
  corrections. To be checked by `skill-quality-reviewer` before final trust.
- **D24 (2026-07-07) — Product engineering craft (D12.2, 5 skills),
  PM/product-engineering interface (D12.5, 6 skills), and Growth/analytics
  engineering (D12.6, 4 skills) built.** 125→140 skills, one PR (three pack
  commits: D12.2, D12.5, D12.6 — clean split boundaries; the batch was NOT
  split into multiple PRs). D12.2: `pagination-cursor-designer`,
  `error-taxonomy-designer`, `edge-state-ux-designer`,
  `notification-webhook-ux-designer`, `mobile-viewport-craft` — the API/UX
  craft INSIDE the contract `api-event-architect` owns (pinned in every
  D12.2 trigger-eval). D12.5: `requirements-gathering-facilitator`,
  `product-spec-writer`, `roadmap-under-uncertainty-planner`,
  `prioritization-frame-picker`, `feature-flag-rollout-strategist`,
  `sunset-deprecation-communicator`. D12.6: `event-schema-architect`,
  `funnel-definition-designer`, `ab-test-designer` (design AND result
  reading), `product-analytics-instrumenter`. Key seams pinned in
  trigger-evals: `product-spec-writer`≠`adr-writer` (product spec vs
  architecture decision record);
  `event-schema-architect`≠`api-event-architect`≠`streaming-event-architect`
  (analytics schema vs external contract vs internal pipeline — a three-way
  seam); `product-analytics-instrumenter`≠`observability-operator`≠`skill-usage-instrumenter`
  (product analytics vs system telemetry vs skill-library usage — a
  three-way seam); `sunset-deprecation-communicator`≠`skill-deprecation-planner`
  (product-feature sunset communication vs library-skill retirement);
  `feature-flag-rollout-strategist`≠`plan-entitlement-architect`/`authorization-matrix-designer`
  (rollout vs entitlement/permission). Product-agnostic (no product/company/
  personal names or live identifiers; placeholder paths/ids only). All 15
  are design/facilitation/analysis skills producing specs/plans/verdicts and
  editing nothing → model-invocable (no `disable-model-invocation`); none
  performs side effects. Embedded commands (few — these are design skills)
  follow the D19 squash-merge corrections. The two three-way seams
  (`event-schema-architect`, `product-analytics-instrumenter`) are the
  highest mutual-overlap risks flagged for the reviewer pass. To be checked
  by `skill-quality-reviewer` before final trust.
- **D25 (2026-07-07) — Technical writing / docs engineering (D12.4, 8
  skills) built. PART A of the D12.4+D12.7+D12.9+D14 two-PR batch.**
  140→148 skills. D12.4: `readme-craftsman`, `adr-sequencer`,
  `diataxis-doc-organizer`, `docs-as-code-architect`,
  `api-doc-generator-designer`, `contribution-guide-author`,
  `onboarding-doc-designer`, `docs-retention-index`. Key seams pinned in
  trigger-evals: `adr-sequencer` EXTENDS `adr-writer` (longitudinal ADR
  corpus management — composes single-record authoring, does not duplicate
  it); `docs-retention-index`≠`skill-deprecation-planner` (DOC lifecycle/
  retirement vs library-SKILL retirement — pinned both ways, honoring the
  seam `skill-deprecation-planner` already referenced as "banked, not
  built", now built); `api-doc-generator-designer`≠`api-event-architect`
  (generated reference vs the API contract it documents). Within-pack
  seams pinned across `readme-craftsman`/`diataxis-doc-organizer`/
  `docs-as-code-architect`/`contribution-guide-author`/
  `onboarding-doc-designer` (entry doc vs corpus-by-mode vs pipeline vs
  contributor-guide vs new-hire onboarding). Product-agnostic (no product/
  company/personal names or live identifiers; placeholder paths/ids only —
  `contribution-guide-author` designs contribution guides generically, not
  one repo's CONTRIBUTING.md). All 8 are authoring/design skills producing
  docs/plans and editing nothing → model-invocable; `docs-retention-index`
  gates actual doc DELETION behind human approval (a Stop Condition), like
  `skill-deprecation-planner` for skills. PART B (D12.7 staff-IC 7 + D12.9
  architecture-advisor 1 + D14 framework refresh 3 = 11 skills) is a
  separate PR branched off main-as-it-is; it does not depend on this PR
  merging but should land after it for the count arithmetic. To be checked
  by `skill-quality-reviewer` before final trust.
- **D26 (2026-07-07) — Staff+ IC craft (D12.7, 7 skills), Architecture
  advisory (D12.9, 1 skill), and Framework refresh / source-currency
  (D14, 3 skills) built. PART B of the D12.4+D12.7+D12.9+D14 two-PR
  batch — 148→159 skills.** D12.7: `tech-spec-writer`, `design-review-facilitator`,
  `cross-team-dependency-negotiator`, `roadmap-to-commitments-translator`,
  `staff-scope-selector`, `promotion-packet-writer`,
  `phased-work-handoff-designer`. D12.9: `architecture-advisor` (the
  STYLE/paradigm advisor, per D20 — must discriminate from
  `architecture-designer`/`cloud-architecture-decider`/`saas-platform-architect`/
  `domain-modeler`, pinned all four). D14: `framework-edition-tracker`,
  `framework-mapping-refresher`, `source-currency-auditor` (a
  detect→propose→human-review pipeline; NONE auto-updates a mapping). Key
  seams pinned in trigger-evals: `tech-spec-writer`≠`adr-writer` (whole
  design vs one decision)≠`product-spec-writer`;
  `phased-work-handoff-designer`≠`ai-closeout-reporter` (one turn)≠`ai-sdlc-operating-model`
  (lifecycle); `staff-scope-selector`≠`promotion-packet-writer` (future
  scope vs past impact, both ways); `roadmap-to-commitments-translator`
  inverse of `roadmap-under-uncertainty-planner`;
  `framework-edition-tracker`≠`framework-mapping-refresher`≠`source-currency-auditor`
  (detect vs propose vs broad-staleness). **Build/count note:** built in
  parallel with PART A (D25/D12.4) off main@140, then REBASED onto the
  merged D25 (main@148) with the README/catalog/reconciliation
  pack-block, phase-table, count, and callout regions reconciled to
  include BOTH packs — 148→159 skills, decision log D25 then D26 in order.
  Merge order was PART A (D25) then PART B (D26). Product-agnostic (no product/company/
  personal names or live identifiers; placeholder paths/ids only; edition/
  price/model facts treated as verify-don't-assert per D14). All 11 are
  design/facilitation/advisory skills producing specs/plans/verdicts/
  reports and editing nothing → model-invocable;
  `framework-mapping-refresher` and `docs-retention-index`-style deletion
  is not in scope here, but `framework-edition-tracker`/`-mapping-refresher`/
  `source-currency-auditor` all gate any real change behind human review
  (Stop Conditions). To be checked by `skill-quality-reviewer` before final
  trust.

- **D27 (2026-07-08) — Security scanning & orchestration pack (D12.10)
  banked as candidates (candidate — not built):
  `security-scan-orchestrator`, `sast-orchestration-designer`,
  `dast-safety-harness-designer`.** Fills a real gap (SAST
  tool-running/orchestration, DAST against running apps, whole-repo
  security scan aggregation) distinct from the existing JUDGMENT skills
  (`static-analysis-reviewer` triages findings;
  `supply-chain-security-reviewer` covers deps). Core principle:
  orchestrate-and-REPORT, human approves any action — an AI security
  scanner may READ a repo but must not autonomously fix/PR/configure
  (Zero Trust AI Engineering Discipline). DAST requires written authorization
  + no-prod-without-sign-off guardrails. Build DEFERRED until AFTER the
  library-wide `skill-quality-reviewer` sweep and its corrections are
  complete. Not built.

- **D28 (2026-07-08) — OWASP Web-App Top 10:2025 gap closed:
  `security-logging-alerting-architect` (A09) and
  `error-handling-security-reviewer` (A10) built, the two remaining
  zero-coverage categories from the D8 audit. 159→161.** All 10 OWASP
  web-app categories now have at least one owning skill; A02/A04 remain
  "partial" by the D8 rubric (a slice covered, not the whole category —
  noted, not a gap). OWASP LLM (D6) and Agentic (D7) lists already
  complete. Category definitions per OWASP Top 10:2025 source.
  Product-agnostic. To be checked by `skill-quality-reviewer` in the
  deferred sweep. Seams pinned in trigger-evals:
  `security-logging-alerting-architect` ≠ `audit-log-architect` (records,
  never detects/alerts) ≠ `observability-operator` (system telemetry +
  alert-config implementation) ≠ `slo-reliability-architect` (reliability
  paging) ≠ `incident-response-runbook` (the playbook AFTER the alert this
  skill designs the firing of); `error-handling-security-reviewer` ≠
  `security-pr-reviewer` (broad diff gate vs the error-path lens) ≠
  `appsec-implementer` (builds the fix; the reviewer never edits) ≠
  `static-analysis-reviewer` (judges scanner output, not code directly) ≠
  `error-taxonomy-designer` (the error MODEL vs the security of its
  HANDLING). Both are design/review skills editing nothing →
  model-invocable (no `disable-model-invocation`).

- **D29 (2026-07-08) — `ai-cost-guardrail-designer` extended to cover the
  denial-of-wallet (DoW) + LLMjacking threat model (OWASP LLM10); enhancement,
  not a new skill — count stays 161.** Five evidence-backed defenses woven into
  the existing sections (no new skill, no rename): (1) cost-aware/token-based
  rate limiting — limit on token/cost per window, not request count (one
  request can cost hundreds of times another), with pre-call estimate +
  post-response true-up and per-tenant FIFO queues; (2) FAIL-CLOSED guardrails
  — a cost/rate/budget check that errors, times out, or loses its store DENIES
  the call, and the kill switch ENGAGES on a broken budget-state check; failing
  open turns the limiter into the DoW vector (CWE-636), composing
  `error-handling-security-reviewer` for the general discipline; (3)
  provider-side hard spending caps + billing-anomaly alerting — optional and
  OFF BY DEFAULT, flagged as a verify-at-design-time config action the skill
  flags, not architecture it builds; (4) AI credential-theft (LLMjacking)
  defense — server-side-only custody, short-lived/scoped/per-model keys to
  bound the cost blast radius, and invocation-logging tampering as a compromise
  signal; custody and rotation mechanics defer to `secrets-identity-hardener`,
  this skill owns the AI-spend angle; (5) attribution-under-attack — a DoW
  attacker, a looping agent, and an expensive-but-honest workload look
  identical on the invoice, so per-tenant/user/feature attribution is required
  before judging a spike malicious or benign. Description lightly touched (984
  chars < 1024) to signal the token-based / fail-closed / LLMjacking coverage;
  posture unchanged; product-agnostic (OWASP LLM10 + CWE-636 named by category,
  no vendor/product/incident names). Evals: +2 behavior cases (request-count
  cost-blindness; refuse to label a spike an attack without attribution) and +3
  trigger cases pinning the `secrets-identity-hardener` and
  `error-handling-security-reviewer` seams. Grounded in current DoW/LLMjacking
  research. To be checked by `skill-quality-reviewer` in the deferred sweep.

- **D30 (2026-07-08) — SaaS Architecture Depth pack (D12.11) banked as candidates
  (candidate — not built)**, from a private read-only audit of production
  multi-tenant SaaS patterns + SaaS-architecture research. STRONG cluster (10,
  build-first, scheduled AHEAD of D12.10 SAST/DAST): `command-gateway-architect`,
  `realtime-subscription-architect`, `background-job-orchestration-architect`,
  `horizontal-scalability-reviewer`, `search-architecture-designer`,
  `file-upload-storage-architect`,
  `usage-metering-and-cost-attribution-pipeline-designer`,
  `synthetic-monitoring-architect`, `offline-first-sync-architect`,
  `admin-console-architect` (HIGH/pull-forward). LOW-PRIORITY (4, scale-stage or
  possibly-extension): `cell-based-architecture-designer`,
  `data-partitioning-sharding-strategist`, `intra-tenant-scope-architect` (maybe
  extends `multi-tenant-data-architect`), `share-link-access-architect` (maybe
  extends `authorization-matrix-designer`). Each candidate carries its seam-pins
  for build-time. usage-metering + intra-tenant-scope + share-link flagged
  standalone-vs-extension for `skill-quality-reviewer` to confirm at build. ALSO:
  pull forward (HIGH) from existing backlogs — `idempotency-first-designer`
  (Phase 2, top), rate-limit-design (Phase 4, needs naming),
  `resilience-architecture-reviewer` (Phase 6). All product-agnostic. Build
  DEFERRED — this pack builds after the library-wide `skill-quality-reviewer`
  sweep, ahead of D12.10. Not built.

- **D31 (2026-07-08) — D12.11 SaaS Architecture Depth STRONG cluster built
  (10 skills). 161→171.** Built ahead of the D12.10 SAST/DAST pack as the D30
  schedule specified. The 10:
  `command-gateway-architect`, `realtime-subscription-architect`,
  `background-job-orchestration-architect`, `horizontal-scalability-reviewer`,
  `search-architecture-designer`, `file-upload-storage-architect`,
  `usage-metering-and-cost-attribution-pipeline-designer`,
  `synthetic-monitoring-architect`, `offline-first-sync-architect`,
  `admin-console-architect`.
  **`usage-metering-and-cost-attribution-pipeline-designer` resolved
  STANDALONE** (the build-time flag from D30): it is the metering→rollup→
  reconciliation DATA PIPELINE (event schema, idempotency keys, additive
  rollups, invoice reconciliation) — an ETL/schema deliverable, whereas
  `saas-cost-architect` is the unit-economics MODEL (driver inventory,
  attribution policy, profitability). They compose (the pipeline feeds the
  model); the only overlap is the word "attribution", so the surface is
  ~65% distinct — well above the ~40% duplicate threshold. Not a near-duplicate.
  Seams pinned per the D30 spec, in every skill's `trigger-evals.json` on both
  directions. Highest-overlap pins: usage-metering ≠ `saas-cost-architect`
  (pipeline vs cost model — hard); `background-job-orchestration-architect` ≠
  `streaming-event-architect` (execution vs transport — hard); the in-batch
  `realtime-subscription-architect` ↔ `offline-first-sync-architect` seam
  (live online push vs offline sync) pinned reciprocally both ways;
  `command-gateway-architect` ENFORCES `authorization-matrix-designer`'s policy
  and EMITS into `audit-log-architect`'s schema (not either);
  `admin-console-architect` is the CONSOLE that enforces the authz policy, ≠
  the policy / telemetry / agent-authority / incident-playbook it composes;
  `search-architecture-designer` (lexical) ≠ `rag-security-architect` (vector);
  `synthetic-monitoring-architect` (post-ship prod-safe black-box) ≠
  pre-release/CI/SLO/white-box neighbors. Product-agnostic (no product/company/
  personal names or live identifiers; placeholder paths/ids only; sweep for
  supabase/athena/lovable/aegis/onedrive/personal names/URLs came back clean
  except the standard evals `$schema` URL). All 10 are design/review skills
  producing specs/plans/verdicts and editing nothing → model-invocable (no
  `disable-model-invocation`); the three that DESIGN things that could run
  against live systems (`command-gateway-architect` datastore backstop,
  `synthetic-monitoring-architect` probes, `offline-first-sync-architect`
  reconciliation) carry Stop Conditions forbidding execution against production
  without human approval — they design, they do not run. Embedded commands
  follow the D19 squash-merge posture (few — these are design skills). The 4
  LOW-PRIORITY D12.11 candidates (`cell-based-architecture-designer`,
  `data-partitioning-sharding-strategist`, `intra-tenant-scope-architect`,
  `share-link-access-architect`) remain candidate — not built (Build B). To be
  checked by `skill-quality-reviewer` in the deferred sweep; highest mutual-
  overlap risks flagged for that pass: usage-metering ↔ `saas-cost-architect`
  and realtime ↔ offline-first. Validator: 171 skills, exit 0.

- **D32 (2026-07-08) — D12.11 SaaS Architecture Depth LOW-PRIORITY cluster
  built (4 skills). 171→175.** The deferred Build B, completing the D12.11
  pack. The 4: `cell-based-architecture-designer`,
  `data-partitioning-sharding-strategist`, `intra-tenant-scope-architect`,
  `share-link-access-architect`.
  **Both standalone-vs-extension flags resolved STANDALONE** (same
  author-then-judge circuit-breaker as D31's usage-metering):
  - `intra-tenant-scope-architect` vs `multi-tenant-data-architect`: the
    parent is explicitly SINGLE-AXIS (scoping decided around `tenant_id`,
    per-store pooled/silo strategy + propagation). The new skill adds a
    SUBORDINATE per-user scope axis below the tenant (site/region/org-unit):
    a per-user scope-grant model, a scope-restricted-vs-tenant-wide role
    split, the composite `tenant_id AND scope` row-filter predicate, and a
    live add-axis migration — none of which live in the parent. It
    PRESUPPOSES the tenant layer rather than restating it. Shared surface is
    the server-derived propagation + expand→contract migration pattern
    (~35%); distinct surface ~60% — well above the ~40% duplicate threshold.
    Not a near-duplicate; shipped standalone with the parent seam pinned hard.
  - `share-link-access-architect` vs `authorization-matrix-designer`: the
    parent is IDENTITY/RBAC for authenticated members (roles × permissions ×
    resources, impersonation/support). The new skill is a CAPABILITY model —
    possession of an opaque, unguessable, expiring, revocable token grants a
    fixed narrow scope to anyone-with-the-link, often unauthenticated, with a
    different actor, a different threat surface (token enumeration/leak/expiry,
    guest sessions, abuse defense), and a different lifecycle. The parent's
    one-line "sharing grant" is a MEMBER shared-with grant, not a public
    bearer link. Overlap (~30%: both authorization, both scope+audit+
    deny-by-default) is well below the distinct surface (~60%). Shipped
    standalone with the parent seam pinned hard.
  So both are new skills: 171→175 (not fewer). Seams pinned in every skill's
  `trigger-evals.json`, both directions. Highest-overlap pins: intra-tenant-
  scope ≠ `multi-tenant-data-architect` (subordinate axis vs tenant_id axis)
  and ≠ `command-gateway-architect` (standing read-side axis vs execute-time
  write scope — the D31 bleed guard); share-link ≠ `authorization-matrix-
  designer` (bearer capability vs member RBAC, incl. the member-shared-with-
  grant nuance case); `cell-based-architecture-designer` ≠ `saas-platform-
  architect` (per-component isolation) / `architecture-advisor` (style menu
  omits cells) / `agent-containment-reviewer` (agent blast radius), and its
  too-big-tenant edge routes to `data-partitioning-sharding-strategist`;
  sharding ≠ `multi-tenant-data-architect` (isolation) / `warehouse-lake-
  architect` (analytical) / `operational-vs-analytical-splitter` (what leaves
  OLTP). Product-agnostic (no product/company/personal names or live
  identifiers; placeholder paths/ids only; sweep for supabase/athena/lovable/
  aegis/onedrive/personal names/URLs came back clean except the standard
  evals `$schema` URL and one generic "Postgres" engine reference — neither a
  product/company name nor a live identifier). All 4 are design/review skills
  producing specs/plans/verdicts and editing nothing → model-invocable (no
  `disable-model-invocation`); the three that DESIGN a production-reshaping
  change (`cell-based-architecture-designer` cell migration/rebalancing,
  `data-partitioning-sharding-strategist` reshard, `intra-tenant-scope-
  architect` add-a-scope-axis migration) carry Stop Conditions forbidding
  execution against production without human approval — they design, they do
  not run. `share-link-access-architect` additionally Stop-Conditions
  inventing crypto (specify vetted primitives) and unilateral public exposure
  of regulated data (escalate). Embedded commands follow the D19 squash-merge
  posture (none needed — these are design skills). **D12.11 pack now COMPLETE:
  all 14 candidates resolved (10 strong built D31, 4 low-priority built D32).**
  To be checked by `skill-quality-reviewer` in the deferred sweep; residual
  overlap risks flagged for that pass: intra-tenant-scope ↔ `multi-tenant-
  data-architect` (the closest of the two flag decisions) and share-link ↔
  `authorization-matrix-designer`. Validator: 175 skills, exit 0.

- **D33 (2026-07-08) — Applied `skill-quality-reviewer` sweep corrections
  (19 REVISEs from the completed 8-batch / 80-skill sweep; all nit-level/
  soft, zero FAILs). Count stays 175 — edits only, no skill created/deleted;
  no skill logic/scope/posture changed.** Two mechanical classes:
  - **Built-before-neighbor back-references (Shape A, 8 older hubs):** older
    skills gained `overlaps_with` entries + discriminating trigger-eval
    cases + a one-line Use-When boundary for newer colliders that already
    named them — led by `api-event-architect`'s 6 (`streaming-event-
    architect`, `realtime-subscription-architect`, `command-gateway-
    architect`, `event-schema-architect`, `notification-webhook-ux-designer`,
    `api-doc-generator-designer`). Also `operational-vs-analytical-splitter`
    (stale write-path misroute retargeted from `multi-tenant-data-architect`/
    `architecture-designer` to `data-partitioning-sharding-strategist`,
    isolation-only kept on `multi-tenant-data-architect`; + usage-metering),
    `streaming-event-architect` (+background-job, +realtime),
    `multi-tenant-data-architect` (+sharding, +intra-tenant-scope),
    `saas-cost-architect` (+usage-metering), `architecture-advisor` (+cells),
    `saas-platform-architect` (+cells), `authorization-matrix-designer`
    (+admin-console, +intra-tenant-scope, +share-link).
  - **Eval-completeness nits (Shape A, 8 skills):** `lane-authoring-guide`
    (+scoped-approval-register), `sharded-validation-with-resume`
    (+qa-automation-architect, self-referential Gotcha de-housed),
    `risk-tiered-validation-selector` (+exact-prompt trigger case),
    `intra-tenant-scope-architect` (+share-link), `error-taxonomy-designer`
    (+error-handling-security-reviewer), `command-gateway-architect`
    (+intra-tenant-scope), `standing-approval-and-auto-advance`
    (+merge-is-deploy-governance), `horizontal-scalability-reviewer`
    (+data-partitioning-sharding-strategist).
  - **Staleness (Shape B, 2 skills):** `skill-deprecation-planner` and
    `context-co-update-ci-gate` had "banked / not built / until it ships /
    handled manually" wording about the now-SHIPPED `docs-retention-index`
    and `sunset-deprecation-communicator` replaced with shipped-state
    wording; all SKILL-vs-DOC and library-vs-product-PM discrimination kept
    verbatim.
  The sweep confirmed the library structurally sound — **0 FAIL, 0
  unroutable, 0 escalation** across 80 skills. Product-agnostic (swept
  supabase/athena/lovable/aegis/onedrive/personal names/URLs — clean except
  the standard evals `$schema` URL). Validator: 175 skills, exit 0. **To do
  next: D12.10 SAST/DAST build (deferred by D27).**

- **D34 (2026-07-10) — Documentation accuracy, coined-term rename, auto-merge
  reconciliation, and README readability pass (doc-only; count stays 175,
  validator exit 0; no skill created/edited/renamed/deleted).**
  - **Coined-term rename.** The project's doctrine term gained **"AI"** and
    dropped its hyphen — it now reads **"Zero Trust AI Engineering
    Discipline"** — updated at all 19 verified occurrences across 5 files
    (README, CONTRIBUTING, the catalog, this reconciliation doc, and the
    doctrine doc's H1 + definition). The classic network-security concept
    **"Zero Trust" is deliberately NOT renamed** — README:121, this doc's
    "Zero Trust security motto" / "classic network Zero Trust", the doctrine
    doc's "Distinction from classic Zero Trust" section, and the
    `human-agent-trust-reviewer` "zero trust weight/theater" idiom are all
    left verbatim. The doctrine file was likewise renamed (Option B — full
    consistency) to `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`, with all
    5 inbound links updated (README:120/184/453, CONTRIBUTING:3, this doc's
    D16 entry).
  - **Accuracy fixes.** CONTRIBUTING rule 8's stale "95 skills" reworded to
    "exit 0" (no longer hard-codes a count that keeps going stale);
    CONTRIBUTING "On self-auditing" updated from "banked D13 candidate …
    when built" to the shipped reality (`skill-quality-reviewer`, built
    D18). Catalog Status count chain extended through D31→171 / D32→175
    (current total **175**) and its "Implemented (Phases 0–5)" heading
    relabeled to "Implemented" (the section runs through D32). README About
    paragraph brought current through D33 (was stale at D28). README "Map of
    the system" skills bullet — which omitted 8 shipped packs
    (D12.2/D12.4/D12.5/D12.6/D12.7/D12.9/D14/D28) — superseded by a pointer
    to the new roster. Minor: README "~175" → "175"; the validator
    catalog-integrity claim softened to match actual behavior;
    `secure-saas-reviewer` subagent "a application" → "an".
  - **Auto-merge contradiction reconciled** (owner-confirmed truth: Aegis's
    development used MANUAL merge after green checks; auto-merge is never
    armed as policy). `auto-merge-policy.md` originally specified an opt-in
    per-phase auto-merge-*arming* mechanism (`gh pr merge --auto --squash`)
    that was never adopted; it is corrected forward to describe the actual
    manual-merge process (original text summarized in-doc for provenance,
    not silently deleted). README:701 ("Auto-merge is enabled per-phase …")
    corrected to manual-merge. CONTRIBUTING rule 3 and README:151 were
    already correct and kept. The one time auto-merge fired — PR #7 — was
    the unauthorized incident recorded in §6 and captured as an
    `agent-authorization-matrix` eval; that is the *rationale* for the
    manual-merge rule, not a counterexample to it.
  - **README readability.** The ~80-line About wall-of-text broken into
    digestible paragraphs; a new scannable **"What's in the library"** roster
    of the 19 shipped pack-families (purpose + example skills each),
    surfacing `requirements-gathering-facilitator` as the elicitation entry
    point that feeds `product-spec-writer`; and a concrete **"Getting
    started"** subsection with copy-pasteable git/Claude-Code steps plus the
    Claude.ai / non-CLI path.
  Doc-only: no skill file, validator, or CI config touched — the
  `secure-saas-reviewer` subagent grammar fix is the sole non-doc,
  non-skill file. Validator: 175 skills, exit 0.

- **D35 (2026-07-10) — Getting Started rewrite: real step-by-step onboarding
  + first-session entry point relocated (doc-only; README.md + this entry;
  count stays 175, validator exit 0; no skill file touched).**
  - **Problem (owner feedback).** The previous "Getting started" stopped at
    `git clone` plus a vague "open this folder in Claude Code" — a capable
    engineer who had never used Claude Code was left guessing. And the
    "Start a project here: `requirements-gathering-facilitator`" journey
    guidance was buried mid-paragraph in the D24 roster family (a catalog
    section) instead of living in Getting Started where a new user looks.
  - **Fix 1 — step-by-step onboarding.** Getting Started rewritten as
    numbered, copy-pasteable steps per environment: Step 1 get-the-repo
    (`git clone` / `cd` / `git pull`, one novice-friendly line each);
    Option 1 Claude Code CLI (install via the official docs at
    code.claude.com/docs — linked, not copied, because install commands
    drift; requires a Claude subscription or Console API access; run
    `claude` from the repo folder; `.claude/` auto-discovery of the 175
    skills + 7 subagents; the previously missing KEY explanation that
    skills are trigger-invoked, not slash-commanded, with two literal
    example prompts; `claude --continue`); Option 2 VS Code / Cursor
    (official Anthropic extension, Open Folder on the repo, Spark-icon
    panel, same engine as the CLI); Option 3 JetBrains plugin, with the
    honest note that Visual Studio (classic) has no native plugin — the
    CLI-in-terminal path is the way; Option 4 Claude.ai / apps kept with
    its honest no-auto-trigger framing; plus a labeled
    "Using the skills in your own project" copy-the-folders step.
    Deliberately NO `npm install -g` instructions (deprecated install
    method; the official page is the single source).
  - **Fix 2 — "Your first session" block added inside Getting Started:**
    start from questions with `requirements-gathering-facilitator`, a
    literal paste-ready first prompt, and the natural chain →
    `product-spec-writer` → architecture/tech-spec skills → build under
    the discipline loop.
  - **Fix 3 — roster cross-reference.** The buried "Start a project here:"
    sentence in the D24 roster family replaced with a one-line pointer to
    *Your first session* in Getting Started; the family still names
    `requirements-gathering-facilitator` as a member skill — only the
    journey instruction moved.
  Doc-only: README.md and this entry are the only files touched.
  Validator: 175 skills, exit 0.

- **D36 (2026-07-10) — Getting Started completion: beginner steps, all
  surfaces, Zero Trust AI Engineering Discipline emphasis (doc-only;
  README.md + this entry; count stays 175, validator exit 0; no skill file
  touched).**
  - **Why.** D35 shipped a good Getting Started rewrite, but an earlier
    draft of its spec ran; this entry completes the final spec. Everything
    is additive or a small in-place edit — D35's structure (Step 1, the
    options, "Your first session", the roster cross-reference) stands.
  - **Beginner-proofing (writing rule: ELI-beginner, never condescending).**
    Step 1 now says how to open a terminal (Windows key / Cmd+Space
    keystrokes) and links git-scm.com/downloads when `git` is missing.
    Version-prone specifics stay linked to code.claude.com/docs, never
    reproduced (the deprecated `npm install -g` method stays banned).
  - **All surfaces.** A "One engine, many surfaces" framing line added
    after Step 1 (terminal / VS Code + forks / JetBrains / Desktop / web,
    linking code.claude.com/docs/en/platforms; the old "Options 1–3 are the
    same engine" intro line trimmed so the two don't repeat). Option 2
    retitled to cover Cursor/Windsurf/VSCodium with the plain distinction
    that the skills are used by Claude Code, not the fork's own AI (Cursor's
    native chat/Composer does not auto-load `.claude/skills/`). Option 3
    (JetBrains) rewritten as numbered steps fixing a real gotcha — the
    plugin does NOT bundle the CLI, so the CLI installs FIRST — plus a
    generalized any-other-editor one-liner (Neovim/Emacs/Sublime/classic
    Visual Studio → run `claude` in a terminal). Two missing surfaces added
    and options renumbered: Option 4 Claude Code Desktop app (no terminal
    at all) and Option 5 Claude Code on the Web (claude.ai/code, zero
    install, honest cloud-copy caveat); Claude.ai manual-paste fallback is
    now Option 6. "Using the skills in your own project" gained one literal
    copy command per OS (PowerShell `Copy-Item -Recurse` / bash `cp -r`),
    each with a one-line explanation.
  - **Discipline emphasis.** New README section "The discipline behind it:
    Zero Trust AI Engineering Discipline" placed immediately after "What
    this is" — a pitch, not a second doctrine doc: two owner-voice
    paragraphs (security's never-trust-by-default lesson vs the blind trust
    AI-assisted development reintroduced; drift + rot and the
    speed-without-silent-decay payoff), six plain-language rules derived
    from the doctrine doc and CONTRIBUTING's operating rules (done-isn't-
    done-until-verified / evidence-not-assertion / assume-drift /
    small-reviewable-changes / human-is-the-gate / track-every-decision),
    the two-tier tagline, and one link to
    docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md.
  - **Standards placement check (verify-only, no edit).** ISO 27001 /
    ISO 42001 / SOC 2 already appear in the "What's in the library" roster
    family 10 line (Compliance & governance); OWASP appears in family lines
    8 (LLM Top 10), 9 (Agentic Top 10), and 17 (web-app gap closure).
    Confirmed in place; no edit made.
  - README's "Map of the system" decision-log range bumped D35→D36 to match
    this entry.
  Doc-only: README.md and this entry are the only files touched.
  Validator: 175 skills, exit 0.

- **D37 (2026-07-11) — Banked read-only discovery for `project-orchestrator`
  (verbal; no files touched; count stays 175).**
  - Ran a read-only discovery pass before the D38 build: read
    `docs/skill-generation-standard.md`, `scripts/validate-skills.py`,
    `ai-sdlc-operating-model` (SKILL.md + `references/stage-gate-map.md`),
    `requirements-gathering-facilitator`, `phased-work-handoff-designer`,
    `scoped-approval-register`, `human-approval-boundary`,
    `agent-authorization-matrix`, and `change-classification-gate` to fix the
    compose-not-restate boundary before writing anything.
  - **Key finding.** `ai-sdlc-operating-model` OWNS the per-change INNER
    lifecycle (context→classify→…→merge→close) and its stage-gate / authority /
    evidence table; a beginner-facing OUTER product arc (idea→discovery→…→
    release) that DELEGATES the inner loop back to that map is a genuine gap —
    and `ai-sdlc-operating-model` explicitly disclaims in-flight single-project
    navigation ("Do NOT use to enforce a single stage in-flight"). That
    disclaimed gap is what D38 builds.
  - Recorded so the D38 build's "grounded in the D37 read-only discovery"
    reference resolves and the §5 sequence stays gapless (no silent D36→D38
    jump — the Zero Trust AI Engineering Discipline applied to the decision
    log). No files changed in D37; count stays 175.

- **D38 (2026-07-11) — Built `project-orchestrator` — the beginner-facing,
  top-level lifecycle router (175→176; validator exit 0; one new skill).**
  - **What.** The library's front door: takes a non-developer from a vague idea
    to a shipped product via (1) runtime stage detection (reads
    `docs/project-state.md` + inspects the user's repo to locate the project on
    the lifecycle map — a vague prompt with no state file = stage zero →
    discovery; an approved spec but no code = ready for architecture), (2)
    next-skill routing along the library's existing hand-off seams (invokes the
    owning stage skill BY NAME — discovery→`requirements-gathering-facilitator`,
    product-def→`product-spec-writer`…, build-loop→`ai-sdlc-operating-model`'s
    inner lifecycle, release→`release-readiness-reviewer`; conditional skills
    invoked by evidence of the feature, not on the default path), (3)
    plain-language business-question translation (every technical fork surfaces
    as ONE business question about cost/time/risk/customer experience; the user
    answers business questions only, never engineering mechanics), and (4) a
    persistent, append-only, dated `docs/project-state.md` in the USER's product
    repo.
  - **Compose, never restate (the anti-duplication tripwire).** SKILL.md CITES
    `ai-sdlc-operating-model`'s `references/stage-gate-map.md` for the stage
    list / gates / authority model, and `change-classification-gate` for the
    change-rigor matrix — reproducing NEITHER inline (a grep confirms no inline
    stage-gate / authority-level / classification table). The
    `docs/project-state.md` schema COMPOSES `phased-work-handoff-designer`'s
    decision-ID register (still-binding flag; a changed decision is a new
    flagged deviation, never an overwrite) + `scoped-approval-register`'s
    approval-citation pattern (Status / Scope allowed / Scope FORBIDDEN /
    Evidence) + the house decision-log format.
  - **Human gate (composed, never relaxed).** Every irreversible step
    (migration, deploy, auth change, deletion, merge, release) routes through
    `human-approval-boundary` + `change-classification-gate` +
    `agent-authorization-matrix`; presents GO / CONDITIONAL-GO / NO-GO with
    plain-language reasons; the user authorizes. Model-invocable (fires on the
    cold vague prompt) but its output is proposals-and-questions.
  - **Trigger.** Wins the beginner meta-navigation framing ("I have an idea but
    don't know where to start / I'm not a developer / what do I do first / what
    comes next / take me from idea to shipped"). Defers (should_not_trigger
    trigger-evals + Use-When "Do NOT use"): elicitation →
    `requirements-gathering-facilitator` (INVOKED as stage 1), team AI-SDLC
    policy → `ai-sdlc-operating-model`, spec authoring → `product-spec-writer`,
    single-stage request → the owning skill (e.g. `code-reviewer`).
  - **Files.** New `.claude/skills/project-orchestrator/` — SKILL.md (286
    lines; description 941 chars < 1024), `references/project-state-template.md`
    (the one reference file — the state schema, with a generic maintenance-
    company worked example), `evals/evals.json` (happy cold-idea path +
    mid-flight state-file edge + refusals) and `evals/trigger-evals.json` (the 4
    deferrals). Registered in `docs/skills-catalog.md` and `README.md` (surfaced
    as the top-level "Start here" front door). Product-agnostic (generic
    domains only). Grounded in the D37 read-only discovery. To be checked by
    `skill-quality-reviewer` + `library-diff-reviewer` for the compose-not-
    restate condition (does it overlap `ai-sdlc-operating-model` or
    `requirements-gathering-facilitator` anywhere it shouldn't?).
  - Validator: 176 skills, exit 0.

- **D39 (2026-07-11) — README beginner-journey + "the roles Aegis can play" (doc-only;
  count unchanged at 176; validator exit 0; no skill file touched).**
  - **Why.** `project-orchestrator` (D38) shipped the beginner-facing *skill*, but the
    README still had no human-facing section that TELLS a non-developer the idea-to-shipped
    path is real and shows them the on-ramp. D39 adds that section — the repo's most
    important surface for its target audience (founders, non-developer "vibe coders",
    technical leaders evaluating whether the library is real).
  - **ADD 1 — `## From idea to shipped: the no-experience path`.** Placed high, immediately
    after `## The discipline behind it` and BEFORE `## How to use this` (a non-developer hits
    it early); deliberately distinct from and NON-colliding with the engineer-facing `## Start
    here (canonical reading order)` further down (which is untouched). Six parts: (a) the
    promise (you bring the business truth, Aegis brings the engineering discipline; you never
    need a skill name or a technical term); (b) THE paste-ready opening prompt in a quote block
    (the single most important thing on the page — `project-orchestrator` picks it up
    automatically, cross-linked to Getting started); (c) a tight 2–3-exchange worked example
    on the **generic maintenance-company** illustration, showing a technical decision (scoped
    revocable access link) arriving as a plain business question (how long should a customer's
    status link live?); (d) the **nine stages** in plain language (1–2 lines each — understand
    → define → design system → design security → plan build → build slice → test/accept →
    prepare deploy → decide to release), each naming what the USER decides; (e) a **you decide
    (business) vs. Aegis decides (engineering)** two-column table — the trust-building split;
    (f) one honest line on what this is NOT (doesn't remove judgment, doesn't guarantee market
    success, you remain the person who says yes).
  - **ADD 2 — `## The roles Aegis can play`.** Placed right after `## What this is` (the
    positioning hook a CTO/founder scanning the repo hits early). Intro line "In practical
    terms, Aegis can make Claude act as:" then the **16 roles VERBATIM** (owner's words) as a
    3-column table (role | plain-language meaning | 1–2 example skills). Forward-links to ADD 1
    for the non-developer path.
  - **Accuracy gate (Zero Trust — every claim verified against disk).** All 16 roles are
    backed by real shipped skills; every example skill named in the table was confirmed present
    on disk (`.claude/skills/<name>/SKILL.md`) before it was written — 31 distinct skills,
    all OK, zero missing. No role claims a capability the library can't back. Product-agnostic:
    the maintenance-company example is generic (no real product/company names — swept lines
    104–260, clean).
  - **Files.** `README.md` only (two new sections, lightly cross-linked; no existing section
    removed or restructured — Getting started, the discipline section, the roster, the phase
    plan, and canonical reading order all intact) + this §5 entry. No `.claude/skills/**`
    touched.
  - **Six grep confirmations (all pass).** (1) beginner-journey section (line 165) ABOVE
    `## How to use this` (line 261); (2) paste-ready opening prompt present; (3) all nine
    plain-language stages present; (4) the you-decide-vs-Aegis-decides split present; (5) all
    16 verbatim roles present (each ×1); (6) `## Start here (canonical reading order)` (line
    562) still intact and NOT collided with.
  - Validator: 176 skills, exit 0.

- **D41 (2026-07-15) — Doctrine extended with its inward-facing half: CONSTRAIN + CURATE
  pillars + "Zet-AI Engineering" shorthand (doc-only; count unchanged at 176; validator
  exit 0; no skill logic touched).**
  - **Why.** The Zero Trust AI Engineering Discipline's four pillars (TRACK / VERIFY /
    GOVERN / HAND OFF) all govern THE WORK from the outside — records, proof, gates,
    knowledge transfer — and were silent on the AI's own operating environment: the
    harness it runs in, the context it is fed, the loop it executes. Two independent
    real-production implementations, mined in the D40 read-only discovery, converged on
    the same extension — two inward-facing pillars. This closes the "engineering OF AI"
    half the title has always claimed (previously the doctrine governed engineering WITH
    AI only). Evidence-extracted, like the D12.8 patterns — not invented.
  - **ADD 1 — the two inward pillars** in `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`,
    after the four outward pillars, in the existing `### VERB — gloss` format:
    **CONSTRAIN** (build the operating environment so the AI cannot exceed its authority;
    the harness is the contract — authority as a property of the environment, not of
    obedience) citing `agent-harness-architect` (planned — D42), `agentic-loop-designer`
    (planned — D42), and shipped `agent-authorization-matrix`; **CURATE** (control what
    enters and leaves the context; an unverified input is an unverified output; the
    context window is a supply chain — a curated diet, not access) citing
    `model-context-designer` (planned — D42), shipped `structured-output-validator`
    (extended in D42), and shipped `ai-evaluation-harness`. A six-pillar half-framing
    added at the top of "The concrete rules" expresses the industry disciplines in the
    doctrine's voice (harness engineering ⇒ CONSTRAIN; context engineering ⇒ CURATE; the
    loop's bounds/stops ⇒ CONSTRAIN, its observe/validate step ⇒ CURATE) — superset
    framing, not competitors. New cross-cutting principle woven into VERIFY: *a verifier
    that cannot fail is theater with an exit code — every check must be proven able to
    fail before it counts.*
  - **ADD 2 — the "Zet-AI Engineering" shorthand** (pronounced "zet-eye"), introduced
    next to the FIRST occurrence of the full term in all 6 files that name the discipline
    (the doctrine doc's core definition, `README.md`, `CONTRIBUTING.md`, this
    reconciliation doc, `docs/skills-catalog.md`, and `project-orchestrator`'s SKILL.md —
    prose only). Deliberately and partially reverses D34's full-term-only
    standardization: the full term stays CANONICAL; the shorthand is ADDITIVE, placed
    next to the full term so it is repeatable and recognizable. No file renamed; no
    classic-"Zero Trust" security reference touched.
  - **Honesty gate (shipped vs planned).** The three new skills the pillars cite
    (`agent-harness-architect`, `model-context-designer`, `agentic-loop-designer`) are
    NOT built here — they are D42. Marked "(planned — D42)" in the doctrine; NOT added to
    `docs/skills-catalog.md` or README's shipped lists. `structured-output-validator`,
    `agent-authorization-matrix`, and `ai-evaluation-harness` exist on disk and are cited
    as shipped.
  - **Files.** `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md` (pillars + framing +
    shorthand + VERIFY principle), `README.md`, `CONTRIBUTING.md`,
    `docs/skills-catalog.md`, `.claude/skills/project-orchestrator/SKILL.md` (the one
    skill file touched — ONLY prose that names the discipline; no logic/workflow/eval
    change), + this §5 entry. Product-agnostic: pillar rules generalized from the D40
    patterns; no product/company names, private paths, or PR numbers.
  - Validator: 176 skills, exit 0.

- **D42 (2026-07-15) — Built the CONSTRAIN/CURATE design skills (176→179).**
  `agent-harness-architect` (CONSTRAIN — the governed operating environment: single
  mediation point, deny-by-default pre-flight ladder, closed registry, server-side
  instruction custody, fail-closed audit), `model-context-designer` (CURATE —
  server-side context assembly under caps, closed schemas, PII/secret minimization,
  designed exclusions, reconstructible context), `agentic-loop-designer` (CONSTRAIN —
  single-shot-vs-agentic decision, clamped iterations, typed retryability with
  policy-stops-terminal, honest empty-set termination), + extended
  `structured-output-validator` (CURATE — type-level policy encoding + banned-content
  scan ladder step). These are the DESIGN skills for harness/context/loop engineering —
  they PRODUCE what the agentic-security cluster REVIEWS (seam: design-not-review,
  yielded explicitly). Threads the "a verifier that cannot fail is theater with an exit
  code" principle. Generalized from a read-only audit of two real production
  implementations (D40). Doctrine's D41 planned markers now shipped. To be checked by
  `skill-quality-reviewer` + `library-diff-reviewer` for the design-vs-review seam.
  - Validator: 179 skills, exit 0.

- **D43 (2026-07-15) — Closed the README presentation-drift ENFORCEMENT gap (the
  discipline applied to its own repo; doc + validator only; count unchanged at 179;
  validator exit 0; no skill logic touched).**
  - **Why.** The library preaches TRACK ("keep the record and reality in sync") and
    "anything caught by hand twice becomes a machine check," yet README presentation-drift
    had been hand-caught repeatedly (stale skill counts, a stale skill name, and an
    auto-merge policy contradiction — corrected around D34 — and now the roles table had
    shipped without the D42 CONSTRAIN/CURATE design capability). Root cause: the validator's
    README enforcement was a SUBSTRING check only — `check_catalog_integrity` verifies each
    skill name appears *somewhere* in README, nothing more. So a skill could ship with stale
    counts, absent from its roster family, or missing from the roles table and still pass
    green. This closes BOTH the current drift AND the mechanism so it cannot silently recur.
  - **Part A — fixed the current drift.** Added the missing **"an AI agent
    operating-environment architect"** role row (the DESIGN side of the D42 CONSTRAIN/CURATE
    pack — `agent-harness-architect`, `model-context-designer`, `agentic-loop-designer`),
    placed adjacent to the AI-security *review* row so design and review read side by side.
    Audited the other presentation surfaces and CONFIRMED current, fixing none that were not
    stale: roster family 20 (CONSTRAIN/CURATE, D42, 3) complete (20 family lines, counts sum
    178 + 1 orchestrator = 179); the About/progression sentence already names the doctrine's
    inward-facing pillars as shipped; the "six rules" discipline summary is an accurate
    OUTWARD per-session summary (not a pillar enumeration, makes no false claim) and was left
    unchanged. Added authoritative `<!-- SKILL-COUNT -->`/`<!-- FAMILY-COUNT -->` markers
    around the counts in the "What's in the library" intro — the human-readable "179 skills"
    text stays; the markers wrap the authoritative instance so the check is unambiguous about
    which number is the current total (historical/aspirational numbers stay unmarked).
  - **Part B — made CONTRIBUTING a complete, followable rule.** Replaced the vague "Register
    the skill in the catalog and the README" with a numbered registration checklist (3a–3f)
    enumerating every surface a new skill must update — catalog; the Skills-(shipped) table;
    the roster family + its `*(Phase/D, N)*` count; the count claims/markers; the roles table
    (a JUDGMENT call, with the D42 pack as the worked "yes, this warranted a new role" example);
    and the doctrine pillar link (judgment) — stating which parts are validator-enforced vs
    judgment. Added a note under "On self-auditing" documenting WHY the checks exist (the
    hand-caught-twice rule).
  - **Part C — added mechanical enforcement to `scripts/validate-skills.py`.**
    `check_readme_counts` (HARD: the marked `SKILL-COUNT` must equal the real skills on disk);
    `check_readme_family_roster` (HARD: sum of family counts + 1 project-orchestrator front
    door == disk, and the number of family lines == the `FAMILY-COUNT` marker; degrades to a
    WARNING if the roster can't be parsed, so a benign format change doesn't hard-block every
    PR); plus WARN-level `check_roster_flagships_exist` (a renamed/removed flagship left stale
    in the roster — the reverse direction the substring check never caught) and
    `check_roles_table_present` (the curated section exists). Curated/judgment surfaces are
    WARN, never HARD, so a check cannot false-fire and get muted — a false-firing check would
    violate the discipline it enforces.
  - **Proof each hard check can fail (Part C6).** Seeded three drifts and confirmed each
    ERRORS (exit 1), then reverted atomically: `SKILL-COUNT` 179→178 (marked != disk);
    family-1 count 8→7 (sum + 1 = 178 != 179 disk); `FAMILY-COUNT` 20→19 (marker != 20 family
    lines). Per *"a verifier that cannot fail is theater with an exit code"* and *"anything
    caught by hand twice becomes a machine check."*
  - **Files.** `README.md` (roles row + count markers), `CONTRIBUTING.md` (registration
    checklist + self-audit note), `scripts/validate-skills.py` (four new checks + wiring +
    docstring), + this §5 entry. No `.claude/skills/**` logic/workflow/eval touched. The map
    is now held to the territory for README counts mechanically, not by memory.
  - Validator: 179 skills, exit 0 (new checks active and passing, 0 warnings).

- **D44 (2026-07-16) — Built the D12.10 Security scanning & orchestration pack
  (179→182), the LAST banked capability (banked D27, deferred until after the
  D33 `skill-quality-reviewer` sweep, now complete).**
  - **What.** Three skills that fill the ORCHESTRATION gap the library's JUDGMENT
    security skills left open (`static-analysis-reviewer` triages the findings it
    is handed; `supply-chain-security-reviewer` covers deps/provenance) — nothing
    RAN or AGGREGATED the scans themselves:
    - `security-scan-orchestrator` — orchestrate a WHOLE-REPO static scan (SAST +
      dependency/SCA + secret + IaC/config) and aggregate it into ONE prioritized
      report (scope, tool-agnostic coordination, cross-tool normalization/dedup,
      severity aggregation, coverage/GAP account).
    - `sast-orchestration-designer` — design HOW a SAST suite is RUN (category-
      level analyzer selection, ruleset/config, baseline + diff-scanning, a GOVERNED
      FP suppression list, incremental-vs-full, fail-closed CI integration).
    - `dast-safety-harness-designer` — design a SAFE DAST harness against a running
      app: written-authorization gate (composes `human-approval-boundary`, classified
      via `change-classification-gate`), staging-only unless prod is explicitly
      authorized, rate/impact limits + abort, no destructive probes without sign-off,
      data-handling; NOT a pen-test playbook (no exploit enumeration).
  - **The hard seam — orchestrate-and-REPORT, human-approves-action.** These skills
    RUN and AGGREGATE; they never fix, act on, or triage findings. Finding TRIAGE is
    yielded to `static-analysis-reviewer` (MANDATORY in the two static skills — pinned
    in Use When + a discriminating trigger-eval); dep/provenance judgment to
    `supply-chain-security-reviewer`; DAST authorization to `human-approval-boundary`.
    The in-batch `security-scan-orchestrator` ↔ `sast-orchestration-designer` seam is
    pinned both ways.
  - **Fail-closed threaded through all three:** a scanner/probe that errors, times out,
    or can't reach its target is a REPORTED GAP, never a silent pass — *a scan that
    cannot run is not a clean scan* — and each ships the designed proof its failure
    path surfaces (*a verifier that cannot fail is theater with an exit code*).
  - **Posture.** All three are DESIGN/orchestration skills producing scan plans/
    aggregated reports and edit nothing → model-invocable (no `disable-model-invocation`);
    Stop Conditions forbid acting on/fixing findings and running DAST without written
    authorization. No NEW doctrine pillar (they APPLY the orchestrate-and-report principle
    of the Zero Trust AI Engineering Discipline / `agent-authorization-matrix`, D16) — no
    doctrine change. Roles table: no new row — the pack is orchestration tooling that
    FEEDS the existing application-security role and whose defining seam is that it does
    NOT do the security JUDGMENT; a new row would blur that (judgment call, CONTRIBUTING 3e).
  - **Registration (D43 enforcement).** Catalog D44 section (+ intro), README
    Skills-(shipped) D44 table, a NEW roster family 21 (Security scanning & orchestration,
    D12.10, 3), phase-plan D44 row, and the count bumps: README `SKILL-COUNT` 179→182 and
    `FAMILY-COUNT` 20→21 (+ the human-readable 182-skills/21-families prose across
    About/roles/map/getting-started, and the D1–D42→D1–D44 decisions range). Banked
    D12.10 candidate block marked BUILT.
  - **Product-agnostic** (swept scanner vendors + supabase/athena/lovable/aegis/onedrive/
    personal/URLs — clean; tool CATEGORIES only). Validator: **182 skills, exit 0**, D43
    count/family checks passing. To be checked by `skill-quality-reviewer` +
    `library-diff-reviewer` for the orchestrate-vs-triage seam.

- **D45 (2026-07-16) — Extended `cloud-architecture-decider` to cover the full
  ABSTRACTION LADDER as a first-class decision axis (rung × provider × posture,
  was provider × posture only), fixing an enterprise-hyperscaler bias that
  mis-steered the repo's non-developer/founder audience. Skill-edit only; count
  stays 182.**
  - **The gap (from the read-only D45 discovery).** The decider is STRUCTURALLY
    provider-neutral (its logical-architecture step forbids product names) but
    CONCRETELY named only AWS/Azure, and its scoring space was provider ×
    deployment-posture {single/multi/hybrid/stay} — WHICH-hyperscaler ×
    HOW-MANY. The abstraction RUNG (IaaS vs container-PaaS vs managed-Jamstack/
    SSR vs Postgres-BaaS vs edge/serverless vs hyperscaler) was not a scoring
    dimension. For the repo's stated non-developer/founder audience (README
    no-experience path, whose on-ramp includes deployment), steering to AWS/
    Azure is the wrong default — the modern 2026 startup default is
    managed-Jamstack + Postgres-BaaS + edge, with container-PaaS between that
    and the hyperscalers.
  - **The fix (Option A from the discovery).** Added the abstraction ladder
    (IaaS/VPS → container-PaaS → managed-Jamstack/SSR → Postgres-BaaS →
    edge/serverless → hyperscaler) as a first-class axis: a new Workflow step 4
    *"Place the workload on the abstraction ladder"* (rule: **pick the highest
    rung the workload tolerates, then a provider within it**), scoring widened
    to **rung × provider × posture**, an Abstraction-rung line added to the
    Output Format, and the managed-vs-self-hosted step reframed as the
    per-capability refinement WITHIN the rung (the ladder generalizes that
    toggle). Named the modern 2026 tier — managed-Jamstack (e.g. Vercel,
    Netlify, Cloudflare Pages), container-PaaS (e.g. Render, Railway, Fly.io),
    Postgres-BaaS (e.g. Supabase, Neon), edge (e.g. Cloudflare Workers) — and
    added **GCP** as a named, decide-able hyperscaler option (was absent).
  - **Brands as refreshable EXAMPLES within durable categories (house style).**
    Every brand is named only as an "e.g." example inside a durable category
    label; the DECISION AXES carry the weight (abstraction rung · ops maturity ·
    workload shape · cost model · compliance/residency · lock-in/exit) and a
    line states brand pricing/free-tiers/runtime-limits are VOLATILE
    verification items, never asserted — the same treatment the skill already
    gives hyperscaler SKUs/regions. Precedent: `merge-is-deploy-governance`
    names `vercel.json`/`netlify.toml`-class files; `rls-policy-auditor`
    already names Supabase as a generic mechanism example. A future update
    swaps the brand list without touching the logic.
  - **Preserved the product-name-free logical architecture.** The concrete
    brands live only in the ladder explanation + options/scoring output;
    Workflow step 2 still bans product names (now says so explicitly), and the
    Validation Checklist keeps *"zero provider product names"* AND adds a check
    that brands appear only in the ladder/scoring, never in the logical
    architecture.
  - **Handoff asymmetry noted, not resolved.** Hyperscaler-rung mapping still
    hands off to `aws-saas-architect`/`azure-saas-architect`; the modern tier
    has NO mapping skill yet, so the handoff notes it is LOWER-TOUCH to map (the
    platform absorbs account topology, IAM, network, patching) and routes the
    parts that still need design to existing owners — tenancy to
    `saas-platform-architect`/`tenant-modeler`/`multi-tenant-data-architect`,
    Postgres-BaaS RLS to `rls-policy-auditor`, and push-to-deploy to
    `merge-is-deploy-governance` (auto-deploy-on-push makes merge==deploy MORE
    central here than on a hyperscaler). No `managed-platform-saas-architect`
    target was invented.
  - **Banked (deferred) future candidates** *(both: candidate — not built)*:
    - `managed-platform-saas-architect` — Option B: a single pattern-named
      mapping skill for the modern managed-platform tier (container-PaaS /
      Jamstack / Postgres-BaaS / edge), the modern-tier peer of the aws/azure
      architects. **Conditional trigger:** build if/when the modern-tier
      handoff asymmetry bites (a decision lands on the modern tier and the
      tenancy/RLS/deploy routing proves insufficient).
    - `gcp-saas-architect` — the parallel hyperscaler mapping skill for GCP
      (GCP is now a decide-able option here but has no mapper), mirroring
      `aws-saas-architect`/`azure-saas-architect`. Separate, lower-priority
      future item. **Banked content (D48) — the GCP security suite, recorded
      for IF this trigger ever fires:** Security Command Center (CSPM +
      threat, now Enterprise tier), Google Security Operations/SecOps
      (SIEM/SOAR, renamed from Chronicle — the rename is the durable fact),
      Cloud Armor (WAF/DDoS), Cloud IDS (network IDS), Sensitive Data
      Protection (formerly Cloud DLP — the Macie slot), Assured Workloads
      (compliance/residency), and AI Protection + Model Armor
      (name-and-place ONLY, design yielded to the AI-security/agent
      cluster — the one GCP item touching the D48 Gap-2 seam). Same
      discipline as the shipped mappers: name + place, tie to
      isolation/cost/maturity, volatile packaging = verification items.
  - **Files.** `.claude/skills/cloud-architecture-decider/SKILL.md` (description
    widened to name the ladder + GCP, still < 1024 chars; Purpose, Use When,
    Inputs #8 workload-shape, Workflow 7→8 steps, Output Format, Validation
    Checklist, Gotchas, Supporting Files) and its
    `references/decision-inputs.md` (new Abstraction-ladder section with the
    rung table + PlanetScale engine-heritage note; scoring rubric widened to
    rung × provider × posture; managed-vs-self-hosted table reframed as per-rung
    refinement). Evals checked — consistent, not edited (out of scope). No
    other skill and no validator/workflow file touched (→ `gate-guard` passes).
  - **Product-agnostic.** Brand names are generic market examples; "supabase"
    (on the standing privacy sweep list — the author's real backend) is named
    ONLY alongside its peer Neon as an industry Postgres-BaaS example, framed
    unambiguously as a market example, never as "our stack" — consistent with
    the existing generic `rls-policy-auditor` Supabase reference; no private
    project/path/URL named.
  - Validator: **182 skills, exit 0** (no skill added/removed; D43 count/family
    markers unchanged at 182/21). To be checked by `skill-quality-reviewer` for
    the decide-vs-map seam and the brands-as-examples framing.

- **D46 (2026-07-18) — Built `authority-invalidation-architect` (182→183), the
  symptom-triggered owner of the "change didn't take effect" access-bug class:
  a removed user still sees the data, a revoked role still works, logout
  doesn't end the session, a plan change still shows the old tier, a deleted
  item stays visible.**
  - **The gap (from the read-only D46 discovery, independently run twice —
    2026-07-17 and re-verified from scratch 2026-07-18, same verdict).** The
    MECHANISM existed as fragments across ≥8 skills — but every fragment is
    design-time, cause-vocabulary, or manual-only, and **no skill triggered on
    the symptom as the victim experiences it** (zero trigger-surface hits
    corpus-wide for "still has access" / "removed but still sees" / "didn't
    propagate"-class language). Three content blocks existed NOWHERE: (1)
    JWT/token-claims staleness — "JWT" appeared in exactly one skill
    (`rls-policy-auditor`, as trusted context source) and
    session-version/epoch/token-denylist had zero auth-context hits; (2)
    client-side state/data-cache purge on authority-change and logout (zero
    client-data-cache vocabulary corpus-wide); (3) the cross-surface verify
    battery for the CHANGED principal (`multi-tenant-security-tester` has no
    formerly-authorized actor class; the corpus DEMANDS the property three
    times — `authorization-matrix-designer`'s "state the mechanism",
    realtime's teardown, a `tenant-isolation-reviewer` reference probe — and
    designs it nowhere). Outcome A (widen existing descriptions) was rejected
    on measured arithmetic — the four candidates sit at 999/970/956/946 chars
    against the 1024 cap — and because N skills widened onto one symptom
    creates N-way routing ambiguity on exactly the attribution the victim
    lacks; Outcome C (adequately covered) was rejected because for the
    README's non-developer audience a fix reachable only through cause
    vocabulary is not coverage.
  - **What.** ONE skill owning the lifecycle CHANGE → PROPAGATE → VERIFY:
    classify the change and direction (deny first — revoked access must
    actually revoke; the removed user reports nothing, which is why the bug
    survives), inventory the eleven surfaces where old authority survives
    (per-surface map in `references/stale-authority-surface-map.md`: server
    sessions, JWT/token claims, client stores/data caches, shared HTTP/CDN
    caches, in-process/distributed caches, DB session context, realtime
    subscriptions, share links, entitlement resolution, search indexes,
    signed URLs), locate the holder by diagnostic tell ("works in incognito"
    → client copy; "fixes at a fixed interval" → token TTL), state an
    owner-confirmed revocation-latency bound (the sibling of
    caching-strategy-designer's consistency envelope, applied to authority),
    design invalidation per surface — OWNED: the token-policy menu
    (short-TTL+refresh vs session-version/epoch vs denylist, tradeoffs and
    resulting latency stated; a stateless token's revocation latency IS its
    access TTL unless a server-side check exists), server-session
    invalidation (replay rejected; clearing the client is presentation, not
    revocation), and client-state purge on logout AND authority-change
    (incl. the next-user-on-shared-device leak) — and verify with the
    deny-direction-first cross-surface battery for the CHANGED principal
    (not a fresh test user), grant direction and positive control included.
  - **The hard seam — compose, never restate (the D38 `project-orchestrator`
    pattern).** Cache mechanics stay with `caching-strategy-designer` — its
    authorization-caching Safety Rule is CITED as governing, never restated
    or re-approved; mid-connection re-auth/teardown with
    `realtime-subscription-architect`; plan resolution + webhook-lag with
    `plan-entitlement-architect`; link revocation with
    `share-link-access-architect`; RLS policy SQL with `rls-policy-auditor`
    (the new skill owns the FRESHNESS of the context feeding policies, plus
    pool reset); custody implementation with `secrets-identity-hardener`
    (manual-only — the new skill produces the named control it requires);
    the generic unknown-cause method with `systematic-debugger` (the new
    skill is the domain differential). Never-worked access routes to the
    correctness owners via the load-bearing discriminator *"did it behave
    correctly before the change?"* — pinned in Use When, Stop Conditions,
    and a trigger-eval. Per the discovery's anti-double-routing rule, NO
    existing skill's description was widened — the new skill is the single
    symptom-layer entry; the mechanism skills keep their cause-language
    triggers.
  - **Posture.** Design/diagnosis only — edits nothing, executes nothing
    against live systems → model-invocable (no `disable-model-invocation`).
    Stop Conditions: live purge/session-kill execution follows the ops
    approval path (`human-approval-boundary`); a proposed authz-result cache
    is never green-lit from here; an active cross-tenant leak routes to the
    isolation path immediately. Ships both eval files (evals + trigger-evals
    discriminating against 8 neighbors).
  - **Registration (D43 enforcement).** Catalog D46 section (+ intro
    narrative), README Skills-(shipped) D46 table, a NEW roster family 22
    (Authority invalidation & propagation, D46, 1), phase-plan D46 row,
    count bumps README `SKILL-COUNT` 182→183 and `FAMILY-COUNT` 21→22 (+ the
    human-readable prose across About/roles/map/getting-started, and the
    D1–D45→D1–D46 decisions range). Roles table: NEW row "an
    access-revocation and stale-authority specialist" (CONTRIBUTING 3e
    judgment, D42-row precedent: a genuinely new user-facing capability the
    table did not name — and the discovery's core finding was precisely this
    symptom's undiscoverability for the README's non-developer audience).
  - **Product-agnostic.** Brands appear only as house-style e.g. examples
    inside durable categories: "managed-auth platforms (e.g. Supabase,
    Firebase)" — Supabase named only alongside a peer, consistent with the
    D45 sweep rule and the existing `rls-policy-auditor` reference — and
    "query/data-cache libraries (e.g. React Query, SWR, Apollo)"
    (`secrets-identity-hardener`'s VITE_/NEXT_PUBLIC_ precedent). No private
    project names, paths, or URLs.
  - Validator: **183 skills, exit 0**; description 1021 chars (< 1024). To
    be checked by `skill-quality-reviewer` + `library-diff-reviewer` for the
    compose-vs-restate seam.

- **D47 (2026-07-18) — Built `superadmin-observability-console-designer`
  (183→184) — designs the cross-tenant superadmin OBSERVABILITY console
  (panel taxonomy + layered IA with restraint; the cross-tenant
  READ-security model: dedicated deny-all-RLS platform-admin registry, no
  self-service grant, three-layer server-side re-check,
  read-only-by-default with privileged-write-only telemetry,
  denied-access-as-metric, break-glass CONTENT-reveal; the server-shaped
  read model; honest-gap typing; the DB/query-perf panel spec;
  posture-as-verification-results + the DB self-monitoring caveat).**
  - Fills a genuinely UNOWNED gap (`admin-console-architect` punts telemetry
    → `observability-operator` operates backends → nobody designed the
    console; the three-way pointer had no owner). COMPOSES ~12 feed/adjacent
    skills rather than restating them.
  - Three seams: SEEING-vs-ACTING (`admin-console-architect` owns
    actions/elevation; this owns the read console + content-reveal
    break-glass), DESIGN-vs-OPERATE (`observability-operator`),
    CONSOLE-vs-FEED (slo / audit / security-logging / synthetic / metering /
    authz owners).
  - Grounded in a read-only discovery mining THREE real production
    implementations that independently converged on the read-security core;
    product-agnostic.
  - Roster: joins family 18 (SaaS architecture depth — strong cluster,
    D31, 10→11 — beside its acting-surface sibling
    `admin-console-architect`) rather than opening a second 1-skill family;
    FAMILY-COUNT stays 22. New roles-table row ("a superadmin console and
    platform-observability designer"). Count markers 183→184. No doctrine
    change.
  - To be checked by `skill-quality-reviewer` + `library-diff-reviewer` for
    the three seams.

- **D48 (2026-07-18) — Extended `aws-saas-architect` + `azure-saas-architect`
  security-posture coverage (skill-EDIT, count stays 184).**
  - **Azure:** added Microsoft Sentinel (SIEM/SOAR), Defender for Cloud CSPM
    + per-workload CWPP plans, Defender for Cloud Apps (CASB), Entra ID
    Protection + Conditional Access — a correctness fix (Azure's security
    suite is a primary enterprise-selection driver yet the mapper was
    weakest there, one posture-only mention).
  - **AWS parity:** added Inspector, Macie, Detective, IAM Access Analyzer,
    the Security Hub CSPM-vs-threat-correlation split, and Security Lake
    (OCSF) + Verified Permissions as first-class options.
  - Each service tied to the existing discipline (tenant isolation + cost +
    team maturity; SKU/tier/price = verification items); seam held
    (name/place services; deep threat-modeling →
    `threat-modeler`/`ai-threat-modeler`, detection-rule design →
    `security-logging-alerting-architect`, SIEM operation →
    `observability-operator`); provider product-naming (not
    brands-as-examples — these are the provider's own service names, the
    same class as Entra/Key Vault/GuardDuty already throughout both
    skills).
  - **Gap 2 (AI agent governance / Microsoft Agent 365): found ALREADY
    COVERED at the content level; no new skill, no agent-skill edits.** The
    Agent-365→skills map: agent registry/shadow detection →
    `agent-containment-reviewer`; agent identity/access/agent-to-agent →
    `agent-identity-privilege-reviewer` + `agent-harness-architect` +
    `agent-authorization-matrix` + `inter-agent-comms-reviewer`; fleet
    observability → `agent-containment-reviewer` (baselines) +
    `ai-cost-guardrail-designer` (spend), surfaced via
    `superadmin-observability-console-designer` (D47); agent data
    governance → `model-context-designer` +
    `memory-context-poisoning-reviewer` + `agent-memory-governance`; agent
    threat protection → the agentic-security cluster
    (`agent-goal-hijack-defender`, `agent-tool-safety-guard`,
    `prompt-injection-defender`, and peers). The agentic cluster +
    CONSTRAIN/CURATE + the D47 console ARE the vendor-neutral agent control
    plane; recorded a doctrine paragraph noting the equivalence
    (optional-b, `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`).
  - GCP security suite recorded as banked content on the D45
    `gcp-saas-architect` banked item above (SCC, Google SecOps née
    Chronicle, Cloud Armor, Cloud IDS, Sensitive Data Protection, Assured
    Workloads, AI Protection/Model Armor) — no skill file created.
  - Grounded in a read-only D48 discovery (verified); Gaps 1 and 2 kept
    strictly separate. Sourced from a 2026 cloud-security-portfolio
    research pass. Validator: **184 skills, exit 0** (edit-only; D43
    count/family markers unchanged at 184/22).

- **D49 (2026-07-18) — Codex/Agent-Skills portability (AGENTS.md
  doc-bridge + MANUAL-ONLY sentinels; skill-EDIT + docs, count stays
  184).**
  - Shipped repo-root `AGENTS.md` (doc-bridge — natively ingested by Codex
    CLI, verified 0.138.0-alpha.7; no hardcoded skill count by D43
    discipline — an unenforced count surface is exactly the drift D43
    exists to prevent).
  - README section "Using Aegis with Codex CLI and other Agent Skills
    tools": out-of-the-box AGENTS.md path recommended; optional native
    `.codex/skills` copy documented user-side only, with four verified
    caveats; no committed copy — drift + silent-drop + truncation +
    ignored manual-only field.
  - MANUAL-ONLY sentinel (`MANUAL-ONLY; never auto-invoke. `, 32 chars)
    prepended to all 18 `disable-model-invocation` skills: Codex ignores
    the field and truncates descriptions to ~92 chars at selection time,
    so the front sentinel is the only guaranteed-visible position
    (A/B-validated in the discovery); 7 descriptions trimmed to fit the
    validator's <1024-char cap (the discovery predicted 6 against Codex's
    ≤1024 cap; this repo's validator is stricter by one character, which
    pulled `agent-goal-hijack-defender` in). Inert in Claude Code (the
    field is enforced there and user /invocation is unaffected),
    protective everywhere else.
  - Grounded in the empirical D49 discovery run in Codex CLI itself.
  - **BANKED FOLLOW-ON (D50 candidate):** strict-YAML normalization of the
    67 out-of-spec descriptions (single-quoting proven Codex-side;
    PRECONDITION: verify Claude Code renders a single-quoted description
    identically before the mass edit) + a HARD strict-YAML parse check in
    `validate-skills.py` so the corpus stays portable (touches the
    validator → gate-guard will fire → D43-style admin-merge expected).
  - Validator: **184 skills, exit 0** (skill-EDIT + docs; D43 count/family
    markers unchanged at 184/22).

- **D50 (2026-07-18) — Portability enforcement (strict-YAML normalization
  ×67 + validator hard checks + portability contract; skill-EDIT +
  validator + docs, count stays 184).**
  - Normalized the 67 strict-YAML-invalid descriptions to single-quoted
    scalars (parsed values byte-identical — pure serialization; precondition
    verified: Claude Code renders quoted descriptions identically, tested on
    `code-reviewer` before the mass edit — and the current build goes
    further: it FALLS BACK to the H1 title for strict-invalid frontmatter,
    so normalization restores description visibility in Claude Code's own
    selection listing too, not just in Codex-class consumers).
  - Validator hardened: strict-YAML frontmatter parse (HARD,
    `check_frontmatter_strict_yaml`), description length measured on the
    PARSED value (matching Codex's counting — quoting chars and doubled
    apostrophes don't count), MANUAL-ONLY sentinel position check for all
    `disable-model-invocation` skills (HARD, `check_manual_only_sentinel`)
    — each proven able to fail on-branch before merge. Requires PyYAML
    (fail-closed; installed in the CI workflow).
  - Portability contract added to skill-generation-standard + `_template`
    (description now models the quoted, front-loaded shape) + CONTRIBUTING;
    README caveat 1 updated (silent-drop fixed; three live caveats remain).
  - The corpus is now portable BY CONSTRUCTION: any future skill either
    satisfies the contract or fails CI. Gate-guard fired by design
    (validator + workflow change); admin-merged after review per D43
    precedent.
  - Validator: **184 skills, exit 0** (D43 count/family markers unchanged
    at 184/22).
  - Post-review hardening (same PR): sentinel check made bidirectional +
    block-scalar descriptions rejected (both proven able to fail); PyYAML
    install documented for local runs; the retroactive D49 annotation
    reverted to keep §5 append-only. Source: Codex-review P2s on PR #59.

---

## 6. Post-merge corrections

- **2026-07-07 — Phase 4 headline correction.** Squash commit `ee6515c` (PR #7) is titled "Phase 4: security & RLS pack (4 skills)" but actually delivered **all 9** canonical Phase 4 skills (`threat-modeler`, `appsec-implementer`, `multi-tenant-security-tester`, `rls-policy-auditor`, `secrets-identity-hardener`, `supply-chain-security-reviewer`, `security-pr-reviewer`, `secure-migration-reviewer`, `static-analysis-reviewer`); the stale "(4 skills)" headline was captured when auto-merge was armed on the 4-skill branch state, and the remaining 5 skills were pushed before the merge fired. `main` contains all 9 — validator reports 36 skills, exit 0.
