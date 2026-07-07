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

---

## 6. Post-merge corrections

- **2026-07-07 — Phase 4 headline correction.** Squash commit `ee6515c` (PR #7) is titled "Phase 4: security & RLS pack (4 skills)" but actually delivered **all 9** canonical Phase 4 skills (`threat-modeler`, `appsec-implementer`, `multi-tenant-security-tester`, `rls-policy-auditor`, `secrets-identity-hardener`, `supply-chain-security-reviewer`, `security-pr-reviewer`, `secure-migration-reviewer`, `static-analysis-reviewer`); the stale "(4 skills)" headline was captured when auto-merge was armed on the 4-skill branch state, and the remaining 5 skills were pushed before the merge fired. `main` contains all 9 — validator reports 36 skills, exit 0.
