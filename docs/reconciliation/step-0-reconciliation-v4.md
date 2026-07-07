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
| `performance-test-harness` + `load-test-planner` | #205 (P1) + #206 (P2) | **Headline gap:** load/render/query/API/edge-function/background-job performance measurement plus realistic traffic/tenant/data-volume load planning — the largest uncovered risk for a multi-tenant SaaS (noisy neighbors, per-tenant degradation). May merge into ONE skill at build time; decide at the §4.2 pre-generation plan table. Pre-release counterpart to Phase 6 `slo-reliability-architect` (targets/alerting). |
| `regression-first-bug-fixer` | #190 (P0) | Failing test that reproduces the bug BEFORE the fix. `regression-suite-curator` cites #190 but owns suite membership, not the fix workflow; `tdd-engineer` owns new behavior, not bug reproduction. |
| `negative-path-test-mapper` | #192 (P0) | Systematic unauthorized/invalid/expired/missing/duplicated/conflicting/out-of-order enumeration per surface. `test-plan-designer`/`test-coverage-mapper` cite #192 as a source but own planning/audit; security negatives stay with Phase 4 `multi-tenant-security-tester`. |
| `test-tenant-provisioner` | #198 (P0) | Repeatable test tenants/users for auth, RLS, integration, and E2E runs. `test-data-architect` (source range #196–#199) owns the data catalog; provisioning the tenants/users themselves is unowned. |
| `ci-failure-classifier` | #214 + #215 (merged; both P0) | ONE skill: hidden runtime-marker scan (console errors, unhandled rejections, skipped tests, auth failures) + failure classification (product bug / test bug / missing secret / timeout-only / infra / skipped runtime). `flaky-test-detective` owns intermittence root-cause; this owns the every-run CI verdict. |
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

**BANKED batch (D9) — targeted AFTER Phase 7; nothing in it is built now.** This is
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
foundation is written once and projected per framework. The 9 candidates below are already the
merged set: evidence collection is ONE skill across all three frameworks (not per-framework),
gap auditing is ONE parameterized skill, and the SoA author serves both ISO standards.

| Candidate skill *(all: candidate — not built)* | Layer | Purpose |
|---|---|---|
| `compliance-control-foundation` | Shared foundation | One framework-agnostic common control set — access control, cryptography, change management, logging/monitoring, incident response, vendor management, risk assessment — written once, consumed by the projections |
| `compliance-evidence-collector` | Shared foundation | Operating-effectiveness evidence **over time** (cadence, retention, audit-window coverage) — SOC 2 Type 2's core demand, reused for ISO surveillance audits |
| `statement-of-applicability-author` | Shared foundation | The ISO-mandatory SoA — per-control inclusion/exclusion justification tied to the 6.1.3 risk-treatment process; the largest net-new ISO artifact SOC 2 lacks |
| `iso-27001-isms-architect` | Framework projection | ISMS per clauses 4–10; four-theme Annex A control selection; internal audit + management review cadence; Amd 1:2024 climate-context check |
| `iso-42001-aims-architect` | Framework projection | AIMS per clauses 4–10; AI risk assessment / treatment and AI system impact assessment; Annex A control-objective selection |
| `soc2-trust-criteria-mapper` | Framework projection | TSC scoping — Security baseline plus which optional categories to attest; Type 1 vs Type 2 decision and audit-window planning |
| `multi-framework-crosswalk` | Cross-cutting | One control → 27001 Annex A + SOC 2 TSC + 42001 Annex A (+ AI RMF function) — the do-the-work-once engine between foundation and projections |
| `compliance-gap-auditor` | Cross-cutting | Current state vs chosen framework(s) → prioritized gap list with remediation order and evidence gaps |
| `ai-lifecycle-risk-manager` | Cross-cutting | NIST AI RMF GOVERN/MAP/MEASURE/MANAGE across the AI lifecycle; pairs with `iso-42001-aims-architect` |

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

**Status: banked only (D9).** No skills built now, no phases renumbered, validator skill-count
targets unchanged; exact sequencing relative to Phase 7.5 and Phase 8 batches is left open.
This banks scope the same way the D6/D7 coverage maps did.

### Phase 8 — Backlog expansion (NEW in v4, ported from execution plan §8)
Convert the remaining 300-skill roadmap into executable skills **in validated batches** under
the batch rules in §4 below. Run only after Phases 0–7.5 validate cleanly.

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
  Type 2, with NIST AI RMF 1.0 as companion) is banked as a future batch targeted AFTER
  Phase 7.** Subsection in §3, after Phase 7.5. Rationale: as an AI SaaS vendor selling into US
  enterprise and EU markets, these converge into procurement requirements (SOC 2 in US
  enterprise sales; 27001 via EU NIS2 supply-chain demand on customers; 42001 emerging in EU
  public procurement) — vendor-market rationale, not a standards claim. Architecture: **one
  shared control foundation + framework-specific projections + a crosswalk** (9 candidate
  skills, already merged — one evidence collector, one gap auditor, one SoA author across
  frameworks), NOT three parallel skill sets; published crosswalks put cross-framework control
  overlap at ~60–80% (industry estimate, not a standard-derived number). The batch is
  substantially a **mapping + evidence layer** over controls already shipped in Phases 3/4
  (and the Phase 5 evidence pack) — it does not rebuild them. Precision: SOC 2 is an AICPA
  **attestation** (CPA examination); 27001/42001 are **certifiable** management-system
  standards. Distinct from Phase 1.5 (operational agent governance) and the OWASP maps
  (D6/D7/D8). No skills built now; no phases renumbered; validator skill-count targets
  unchanged. Sources fetched 2026-07-06 (<https://www.iso.org/standard/27001> and
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

---

## 6. Post-merge corrections

- **2026-07-07 — Phase 4 headline correction.** Squash commit `ee6515c` (PR #7) is titled "Phase 4: security & RLS pack (4 skills)" but actually delivered **all 9** canonical Phase 4 skills (`threat-modeler`, `appsec-implementer`, `multi-tenant-security-tester`, `rls-policy-auditor`, `secrets-identity-hardener`, `supply-chain-security-reviewer`, `security-pr-reviewer`, `secure-migration-reviewer`, `static-analysis-reviewer`); the stale "(4 skills)" headline was captured when auto-merge was armed on the 4-skill branch state, and the remaining 5 skills were pushed before the merge fired. `main` contains all 9 — validator reports 36 skills, exit 0.
