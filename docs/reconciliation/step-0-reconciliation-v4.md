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
| A09:2025 Security Logging and Alerting Failures | — no Phase 4 skill | gap |
| A10:2025 Mishandling of Exceptional Conditions | — no Phase 4 skill | gap |

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
- **A09/A10 gaps:** tracked as named candidate skills in the Phase 8 backlog per D8. Nearest
  existing mitigation for A09 is Phase 3 `audit-log-architect`, which records tenant-scoped
  audit trails but does not design detection or alerting.
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
| **D12.4 Technical writing / docs engineering (P1)** | `readme-craftsman`, `adr-sequencer` (extends shipped `adr-writer` with longitudinal ADR management), `diataxis-doc-organizer`, `docs-as-code-architect`, `api-doc-generator-designer`, `contribution-guide-author`, `onboarding-doc-designer`, `docs-retention-index` (report P1, added by D15: numbered index governing every workflow doc's lifecycle — retention category, reason-to-keep, superseded-by, cleanup rule — mirrored by per-doc retention frontmatter; documentation retirement as an approvable operation) | Durable documentation as its own discipline. |
| **D12.5 PM / product engineering interface (P2) — ✅ all 6 built (D24, 2026-07-07)** | `requirements-gathering-facilitator`, `product-spec-writer` (a product spec, distinct from an ADR), `roadmap-under-uncertainty-planner`, `prioritization-frame-picker`, `feature-flag-rollout-strategist`, `sunset-deprecation-communicator` | The engineering/PM boundary. Two hard seams pinned both ways in trigger-evals: `product-spec-writer`≠`adr-writer`, and `sunset-deprecation-communicator`≠`skill-deprecation-planner` (product-feature sunset vs library-skill retirement). `feature-flag-rollout-strategist`≠`plan-entitlement-architect`/`authorization-matrix-designer`. |
| **D12.6 Growth / analytics engineering (P2) — ✅ all 4 built (D24, 2026-07-07)** | `event-schema-architect` (analytics counterpart to `api-event-architect`), `funnel-definition-designer`, `ab-test-designer` (design AND reading of results), `product-analytics-instrumenter` | User-facing product analytics, distinct from system-facing observability (Phase 6 `observability-operator` / `slo-reliability-architect`). Two THREE-way seams pinned in trigger-evals: `event-schema-architect`≠`api-event-architect`≠`streaming-event-architect`; `product-analytics-instrumenter`≠`observability-operator`≠`skill-usage-instrumenter`. |
| **D12.7 Staff+ IC craft (P2)** | `tech-spec-writer` (broader than an ADR), `design-review-facilitator`, `cross-team-dependency-negotiator`, `roadmap-to-commitments-translator`, `staff-scope-selector`, `promotion-packet-writer`, `phased-work-handoff-designer` (multi-stage sequenced work with binding decisions carried forward as evidence — distinct from `ai-closeout-reporter`, which reports ONE turn, and from `ai-sdlc-operating-model`, which frames the whole lifecycle) (build spec substantiated by report P9: decision-ID register carried across stages, changed-files + explicit not-touched lists, proven-invocation-command sections with tell-tale output, deviation flags) | Technical leadership without management authority. |

**D12.8 Operational workflow patterns — evidence-extracted (P1)** *(pack added by D15,
2026-07-07; **all 10 built 2026-07-07, D21** — the concrete, invocable rules of the
Zero-Trust Engineering Discipline, D16)*: patterns extracted from a read-only audit of two
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

**D12.9 Architecture advisory** *(pack added by D20, 2026-07-07)*: the library's
`architecture-designer` produces a concrete target architecture and migration plan once the
rough shape is known, and `cloud-architecture-decider` advises on cloud provider/posture —
but nothing advises on the architecture STYLE/PARADIGM itself (monolith vs modular monolith
vs microservices vs event-driven vs serverless vs SOA, and hybrids). This pack fills that
gap:

- `architecture-advisor` *(candidate — not built)* — an ADVISOR that recommends an
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

**BANKED scope (D14, 2026-07-07) — 3 candidate skills; nothing in it is built now.** The
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

- `security-logging-alerting-architect` *(candidate — not built)* — closes A09:2025 Security
  Logging and Alerting Failures: security-event detection coverage, alerting rules, and
  response wiring; complements Phase 3 `audit-log-architect` (which records, but does not
  detect or alert).
- `error-handling-security-reviewer` *(candidate — not built)* — closes A10:2025 Mishandling
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
- **D16 (2026-07-07) — Zero-Trust Engineering Discipline coined and documented** at
  [`docs/ZERO_TRUST_ENGINEERING_DISCIPLINE.md`](../ZERO_TRUST_ENGINEERING_DISCIPLINE.md).
  Tagline "Never trust, always verify — every step of the lifecycle. / Assume drift. Demand
  evidence. Track everything.", deliberately mirroring the Zero Trust security motto. Applies
  "never trust, always verify" to the whole SDLC to prevent drift and rot; its concrete rules
  are the D12.8 patterns; it is the doctrine Aegis itself operates under. Distinct from
  classic network Zero Trust. No skills built; this is doctrine, not a skill.
- **D17 (2026-07-07) — README reframed to present Aegis as an operating system for
  engineering software with AI, governed by Zero-Trust Engineering Discipline,** with a
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
  `gated-deployment-prompt-template`) — the concrete, invocable rules of the Zero-Trust
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

---

## 6. Post-merge corrections

- **2026-07-07 — Phase 4 headline correction.** Squash commit `ee6515c` (PR #7) is titled "Phase 4: security & RLS pack (4 skills)" but actually delivered **all 9** canonical Phase 4 skills (`threat-modeler`, `appsec-implementer`, `multi-tenant-security-tester`, `rls-policy-auditor`, `secrets-identity-hardener`, `supply-chain-security-reviewer`, `security-pr-reviewer`, `secure-migration-reviewer`, `static-analysis-reviewer`); the stale "(4 skills)" headline was captured when auto-merge was armed on the 4-skill branch state, and the remaining 5 skills were pushed before the merge fired. `main` contains all 9 — validator reports 36 skills, exit 0.
