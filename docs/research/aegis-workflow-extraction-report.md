# Aegis Workflow Extraction Report

**Date:** 2026-07-07
**Mode:** Read-only audit. No file in either source repository was created, modified, staged, committed, pushed, branched, or tagged. This report is the session's only output.

---

## 1. Scope Confirmation

**Working directory:** `C:\temp\claude-tmp` (scratch folder; confirmed not inside either source repo before any read).

**Repos read (verified to exist with `.git` subdirectories):**

| Label used below | Path |
|---|---|
| Repo A | `<local-path-to-repo-A>` |
| Repo B | `<local-path-to-repo-B>` |

**Repo A top-level (summary):** `.agents/`, `.github/workflows/`, `docs/` (20 subdirectories incl. `decisions/`, `runbooks/`, `context/`, `codex/`, `prompts/`), `scripts/` (~55 audit/lint/probe scripts), `e2e/`, `src/`, `supabase/`, plus root files `AGENTS.md`, `CLAUDE.md`, `Project_Guardrails.md`, `DOCS_SUMMARY.md`, `TEST_PLAN.md`, `BUG_REPORT.md`, `Makefile`.

**Repo B top-level (summary):** `.agents/`, `.athena/`, `.cursor/`, `.github/workflows/`, `agent-context/` (8 per-tool briefing files), `docs/` (numbered `000_` through `169_`), `scripts/` (15 validation/provisioning scripts), `tests/`, `validation-shard-logs/`, plus root files `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `GEMINI.md`, `PROJECT_GUARDRAILS.md`, `PROJECT_AUTOMATION_GUARDRAILS.md`, and ~40 phase/validation log files (`phase7-*` through `phase56-*`, pre-commit/pre-push readiness logs, post-merge closeout logs).

**What was actually read end-to-end or sampled:** root instruction/guardrail files in both repos; Repo A: `docs/REPO_CONTEXT_MAP.md` (first ~1,000 of 3,709 lines plus all section headers plus the update-protocol section), `docs/ai-workflow.md`, `docs/decisions/adr-template.md`, `docs/codex/CODEX_WORK_QUEUE.md`, `.agents/memory/project.md`, workflows `context-map.yml`, `migration-pr-gate.yml`, `post-deploy-validation-manual.yml`, and directory listings of `docs/{decisions,runbooks,context,codex,prompts,ops,testing}` and `scripts/`. Repo B: `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `GEMINI.md`, `PROJECT_AUTOMATION_GUARDRAILS.md`, `agent-context/UNIVERSAL_AGENT_CONTEXT.md`, `docs/000_DOCS_RETENTION_INDEX.md`, `docs/115_AUTONOMOUS_MERGE_DEFAULT_RULE.md`, `docs/150_MIGRATION_DEPLOYMENT_PROMPT_TEMPLATE.md` (head), `docs/169_AGENT2_STAGE0_HANDOFF.md`, heads of `docs/01_PHASE_HISTORY.md` and `docs/02_ACTIVE_BACKLOG_AND_NEXT_WORK.md`, `.github/workflows/pr-validation.yml` (head), `scripts/run-validation-shards.ps1` (head), `scripts/classify-validation-impact.ps1` (head), `scripts/provision-test-data.ts` (head). No product source code was read line-by-line for feature logic; no data files, migrations-with-data, or business documents (`.docx`/`.pdf`) were opened.

---

## 2. Findings — Repo A

Repo A runs a **per-tool spoke model**: `AGENTS.md` (for one coding agent) and `CLAUDE.md` (for another) are deliberately thin, point into a shared `docs/` tree, and an explicit file-ownership table in `docs/ai-workflow.md` states which files are tool-specific, shared, auto-generated (never edit), or append-only. `docs/ai-workflow.md` declares the repo "the long-term memory layer" and chat history ephemeral, defines branch naming, PR body requirements (summary / files / docs / testing / assumptions / risks / rollback), cross-platform handoff steps, and **certainty labels** (confirmed / inferred / unknown) for all documentation claims.

Its centerpiece is `docs/REPO_CONTEXT_MAP.md`: a 3,709-line durable context map with (a) a **full-context gate** whose status is explicit and evidence-closed (closeout criteria, evidence audit, known-unknowns, file inventory — all separate dated docs under `docs/context/`), and (b) roughly **sixty "Narrow Exception" blocks**, each recording one approved piece of work with Status / Reason / Scope allowed / Scope forbidden / Evidence. A CI workflow (`.github/workflows/context-map.yml`) fails any PR that touches important paths without also updating the context map or `docs/context/**`.

`Project_Guardrails.md` defines a **local CI-preflight gate**: inspect `.github/workflows/`, derive local equivalents of every PR check, run them before committing, verify the same checks on clean `main` first, and classify every failure as `PR-caused` / `pre-existing on main` / `unrelated CI infrastructure` / `cannot determine locally`. Docs-only changes get an explicitly-defined lightweight path. `docs/ai-workflow.md` adds duration capture for every check and a `TIMEOUT_FAILURE` classification distinct from product regressions, plus a **standing approval** section (pre-approved push/PR/merge loop within named scope, a required prompt pattern, a phase-advance rule, and a reviewer-block exception path).

Other artifacts: ADR index + template with alternatives-considered (`docs/decisions/`); ~30 runbooks (`docs/runbooks/`: incident response, release process, PR checklist, deployment, session handoff); a per-tool work queue (`docs/codex/CODEX_WORK_QUEUE.md`); **chat-backlog reconciliation docs** that extract and then audit chat-derived claims against PR/source evidence (`docs/codex/CHAT_BACKLOG_AUDIT_AGAINST_CODEBASE_*.md` and siblings); stored cross-tool implementation prompts (`docs/prompts/`); a scripts taxonomy of read-only `audit-*`, `probe-*`, and **`lint-*-safe.ts` scripts that statically verify QA automation is production-safe**; path-triggered hard CI gates (`migration-pr-gate.yml`); and a manual post-deploy validation workflow with an `expected_commit` input (`post-deploy-validation-manual.yml`). A third-party local skills pack lives under `.agents/skills/` with `memory/` and `references/` directories.

## 3. Findings — Repo B

Repo B inverts the topology: **one authoritative rulebook** (`AGENTS.md`, "Universal Source of Truth for All AI Coding Agents") with thin per-tool pointer files (`CLAUDE.md`, `CODEX.md`, `GEMINI.md`, `agent-context/*.md` for seven tools) that must not contain conflicting rules. The rulebook contains: a required startup reading list; a **Phase Lock Rule** (respond first with a 10-item plan — classification, build/not-build, files, impact, risks, rollback, test checklist — then wait for the exact phrase `APPROVED: IMPLEMENT PHASE [N]`); an **A–K change classification** where classes C–I force a written preflight and approval; a 10-item hard-stop list; an autonomous end-to-end pipeline definition (inspect → implement → test → validate → commit exact files → push → PR → monitor → fix → merge → pull → report); a **merge-is-deploy** section documenting that the hosting platform auto-deploys on merge to `main`, making PR validation the authoritative pre-production gate and post-merge validation mere verification, with the exact branch-protection configuration recorded in-repo (single aggregate required check, rationale for "require branches up to date," accepted-risk exposure window, revert-PR rollback); a **tiered local readiness gate** (Fast / Full / Auto by risk); a docs-only definition; and a two-way-sync **coordination rule** (one tool edits frontend surfaces per phase).

The `docs/` tree is a **numbered doc system** (`000`–`169`) governed by `docs/000_DOCS_RETENTION_INDEX.md`: eight retention categories (`KEEP_GUARDRAIL`, `KEEP_VALIDATION_RULE`, `KEEP_DEPLOYMENT_RULE`, `KEEP_HISTORICAL_CLOSEOUT`, `CLEANUP_CANDIDATE_AFTER_SUPERSEDED`, etc.), one row per document with reason-to-keep, superseded-by, and cleanup rule; individual docs carry matching retention frontmatter. Low numbers are living sources of truth (status, phase history, active backlog, testing, deployment runbooks); high numbers are dated phase plans, closeout reports, UAT reports, and handoffs.

Validation is **sharded and impact-classified**: `scripts/classify-validation-impact.ps1` maps changed files to impact classes and **fails closed** (unknown → full validation); `scripts/run-validation-shards.ps1` runs four named functional shards with a status file and `-All -Resume` semantics so timeout-only interruptions resume instead of rerunning; an `uncategorized` shard catches tests no rule claims. `.github/workflows/pr-validation.yml` mirrors this (classify job → docs-only path or parallel typescript/build/guard/shard jobs → one aggregate gate job that is the sole required status check). `PROJECT_AUTOMATION_GUARDRAILS.md` adds fail-closed rules (a "hidden runtime marker," timeout, or skipped execution is not a pass) with one narrowly-defined retry exception, and a package/lockfile-unchanged guard as a standing CI check. `docs/115_AUTONOMOUS_MERGE_DEFAULT_RULE.md` makes merge-after-green the default unless the prompt says `NO AUTONOMOUS MERGE`.

Multi-agent delivery is documented as a first-class workflow: a multi-agent project was split into three lanes (backend read handlers / frontend / AI-routing) with **pre-work evidence-cited authoring guides** per lane (`docs/158_…`, `docs/167_…`, `docs/168_…`), an implementation contract (`docs/147_…`), **staged handoff notes** (`docs/161`, `162`, `164`, `169`) that carry numbered binding decisions forward, define the contract surface for the next stage/agent, record proven invocation commands, verification evidence with honest skip accounting, and explicitly flagged deviations from the approved plan, and **verification closeouts** (`docs/165`, `166`) with per-surface pass/fail and negative-path tables ending in an unqualified "verified complete" statement only after every recorded gap closed. Deployments use a reusable **prompt template** (`docs/150_…`) with placeholders, hard rules, stop conditions, and ETA ranges calibrated from a **deployment history index** (`docs/151_…`) with evidence citations. Test isolation is handled by an **automated test tenant** in the shared environment: provisioning scripts (`scripts/provision-test-data.ts`, `verify-test-env.ts`, `setup-test-env.ts`) mark all test rows with a distinctive marker suffix, refuse to touch unmarked rows, run in validate-only vs. apply modes, and reference credentials by environment-variable name only; grants of extra capability to the test tenant are backup-gated with inline rollback SQL and before/after delta verification (`docs/163_…`).

---

## 4. Extracted Candidate Patterns

Aegis skills assumed to exist: `change-classification-gate`, `human-approval-boundary`, `ai-closeout-reporter`, `ai-sdlc-operating-model`, `agent-startup-context-gate`, `release-readiness-reviewer`, `incident-response-runbook`, `adr-writer`, and candidate `phased-work-handoff-designer`.

### P1. `docs-retention-index`
**Shape:** A single numbered index file that governs the lifecycle of every workflow document — retention category, reason to keep, superseded-by pointer, and an explicit cleanup rule per doc — mirrored by retention frontmatter on each document, so doc cleanup becomes an approvable, evidence-tracked operation instead of ad-hoc deletion.
**Sources:** Repo B `docs/000_DOCS_RETENTION_INDEX.md` plus retention headers across `docs/1xx_*.md`.
**Distinctness:** No listed Aegis skill governs documentation lifecycle/retirement; `adr-writer` covers decisions, not retention.
**Confidence: HIGH** (index + dozens of conforming docs).

### P2. `scoped-approval-register`
**Shape:** Every granted approval is recorded as a durable, append-style block with Status, Reason, **Scope allowed**, **Scope forbidden**, and Evidence — so agents can cite exactly what is and is not authorized long after the approving conversation is gone, and forbidden scope is as explicit as allowed scope.
**Sources:** Repo A `docs/REPO_CONTEXT_MAP.md` (~60 "Narrow Exception" blocks); echoed by Repo B's approval-phrase records inside stage handoffs (`docs/169_…` §1).
**Distinctness:** `human-approval-boundary` presumably defines *where* approval is required; this is the durable *record format* of approvals already granted, with negative-scope lists and evidence links.
**Confidence: HIGH.**

### P3. `standing-approval-and-auto-advance`
**Shape:** An anti-approval-fatigue layer: a documented standing approval for the mechanical delivery loop (push/PR/monitor/merge/pull) within named scope, a default-on autonomous merge after green validation with an explicit opt-out phrase, a phase-advance rule (continue to the next already-named-and-approved phase automatically), a required prompt pattern that must restate the standing approval, and a defined exception path when a reviewer still blocks.
**Sources:** Repo A `docs/ai-workflow.md` (standing-approval, phase-advance, reviewer-block sections); Repo B `docs/115_AUTONOMOUS_MERGE_DEFAULT_RULE.md`, `AGENTS.md` §2A.
**Distinctness:** Inverse of `human-approval-boundary` — it codifies what does *not* need re-approval; complements rather than duplicates.
**Confidence: HIGH** (both repos, multiple artifacts).

### P4. `local-ci-mirror-preflight`
**Shape:** Before any commit, inspect the repo's CI workflow definitions, derive the closest local equivalent of every PR-triggered check, run them, verify the same checks pass on clean mainline first, and classify every failure into a fixed taxonomy (PR-caused / pre-existing on main / CI infrastructure / cannot determine locally) — with a commit gate requiring the whole preflight to be documented in the closeout.
**Sources:** Repo A `Project_Guardrails.md` ("Mandatory local CI-preflight gate", "Failure classification", "Commit gate"); Repo B `scripts/pre-push-validation.ps1` + `AGENTS.md` §2C (PreCommit/PrePush modes).
**Distinctness:** Not covered by any listed skill; `release-readiness-reviewer` is release-scoped, this is per-commit.
**Confidence: HIGH.**

### P5. `risk-tiered-validation-selector`
**Shape:** A change is machine-classified into impact classes, and the classification chooses validation depth (docs-only fast path / fast tier / full tier), with the classifier **failing closed** to full validation for unmatched files, an explicit docs-only definition (and an equally explicit "never docs-only" path list), and forced-full lists for high-risk surfaces.
**Sources:** Repo B `scripts/classify-validation-impact.ps1`, `docs/121_VALIDATION_TIER_SELECTION_WORKFLOW.md`, `docs/156_LOCAL_TESTING_TIER_PROTOCOL.md`, `PROJECT_AUTOMATION_GUARDRAILS.md`; Repo A `Project_Guardrails.md` docs-only rule.
**Distinctness:** `change-classification-gate` presumably routes changes to approval; this routes them to *validation cost*, with an executable fail-closed classifier as the core artifact.
**Confidence: HIGH.**

### P6. `sharded-validation-with-resume`
**Shape:** Full validation is split into a small set of *named functional shards* with a persisted status file; after a timeout-only or infrastructure interruption, a resume flag reruns only unfinished shards; an "uncategorized" catch-shard forces new tests to be assigned; CI runs the shards in parallel and funnels them into **one aggregate gate job that is the only required status check** (so conditional job-skipping on docs-only PRs doesn't break branch protection).
**Sources:** Repo B `scripts/run-validation-shards.ps1`, `.github/workflows/pr-validation.yml`, `docs/105_…`, `docs/118_…`, `docs/157_…`, `validation-shard-logs/`.
**Confidence: HIGH.**

### P7. `merge-is-deploy-governance`
**Shape:** When the hosting platform auto-deploys on merge to mainline, document that reality explicitly, promote PR-time validation to the authoritative pre-production gate, reclassify post-merge validation as verification (not a gate), record the exact required branch-protection configuration in-repo (including who may change it — the human, not agents), state the accepted-risk exposure window, and define rollback as revert-PR-then-auto-redeploy.
**Sources:** Repo B `AGENTS.md` §2B.1–2B.2, `docs/151_DEPLOYMENT_HISTORY_INDEX.md`, `docs/157_…`.
**Distinctness:** `release-readiness-reviewer` reviews a release; this is standing *pipeline governance* for a platform constraint.
**Confidence: HIGH.**

### P8. `context-co-update-ci-gate`
**Shape:** A CI check fails any PR that changes "important" paths without also updating the repo's context map / context notes, making context freshness mechanically enforced rather than aspirational; paired with an update protocol (date + commit SHA scanned, evidence-only status moves, never delete an unresolved risk note without replacing it with proof).
**Sources:** Repo A `.github/workflows/context-map.yml`, `scripts/update-context-map.ps1`, `docs/REPO_CONTEXT_MAP.md` §10, `docs/context/context-map-update-protocol.md`.
**Distinctness:** `agent-startup-context-gate` makes agents *read* context; this makes them *write it back* under CI enforcement — the maintenance half of the same loop.
**Confidence: HIGH.**

### P9. `staged-handoff-note-format`
**Shape:** Each stage of a multi-stage effort ends with a numbered handoff doc containing: phase/approval metadata (including amendments to the approval), baseline commit, a changed-files table plus an explicit "not touched" list, *why-shaped-this-way* rationale, numbered binding decisions carried forward (decision IDs referenced across stages), the contract surface the next stage/agent may rely on, **proven invocation commands** (exact commands verified to work, with the tell-tale output that proves the run was real), verification evidence with honest skip accounting, and explicitly flagged deviations from the approved plan.
**Sources:** Repo B `docs/161_…`, `162_…`, `164_…`, `169_AGENT2_STAGE0_HANDOFF.md`; Repo A's platform-handoff section in `docs/ai-workflow.md`.
**Distinctness:** This is the concrete substantiation of the `phased-work-handoff-designer` candidate — if that skill ships, fold this format in; the decision-ID register, "not touched" list, proven-command section, and deviation flags are the differentiating elements.
**Confidence: HIGH.**

### P10. `lane-authoring-guide`
**Shape:** Before a parallel agent starts its lane of a multi-agent effort, produce an *evidence-cited authoring guide* for that lane — request lifecycle, contracts, a step-by-step recipe, a per-unit checklist, and a "what this agent must not do" boundary — so the implementing agent starts from distilled verified knowledge instead of re-deriving it from source.
**Sources:** Repo B `docs/158_…` (backend handler guide), `docs/167_…` (frontend guide), `docs/168_…` (AI-routing guide), `docs/147_…` (implementation contract).
**Distinctness:** Different from a handoff (P9): it is planner→implementer knowledge transfer authored *before* work begins, per specialization.
**Confidence: HIGH** (three parallel artifacts + a contract doc).

### P11. `gated-deployment-prompt-template`
**Shape:** Risky operations (migrations, production grants) run from a reusable operator prompt template with: operator-filled placeholders, hard rules and stop conditions, backup-then-verify gating, phase-specific smoke expectations, a required dedicated report path, and **ETA ranges calibrated from a deployment history index** where every ETA anchor cites the prior deployment report that justifies it — plus a rule to label any uncited operational claim "unverified."
**Sources:** Repo B `docs/150_MIGRATION_DEPLOYMENT_PROMPT_TEMPLATE.md`, `docs/151_DEPLOYMENT_HISTORY_INDEX.md`, `docs/152_AGENT_DEPLOYMENT_OPERATING_NOTES.md`, `docs/03A_…`.
**Distinctness:** `incident-response-runbook` is reactive; this is a proactive templated-prompt discipline with historical calibration.
**Confidence: HIGH.**

### P12. `test-tenancy-governance`
**Shape:** Automated tests run against a dedicated test tenant inside the shared environment, governed by: a marker convention on all test-created rows with a hard rule never to mutate unmarked rows, validate-only vs. apply provisioning modes with confirmation, credentials referenced by env-var *name* only (never printed), honest skips when env is absent, backup-gated capability grants to the test tenant with inline rollback SQL and before/after delta verification, and (Repo A variant) **static lint scripts that verify QA automation is production-safe before it may run**.
**Sources:** Repo B `scripts/provision-test-data.ts`, `verify-test-env.ts`, `docs/101_…`, `docs/163_…`; Repo A `scripts/lint-e2e-prod-safe.ts`, `lint-qa-*-safe.ts`, `docs/runbooks/qa-automation-production-tenant-interlock.md`.
**Confidence: HIGH.**

### P13. `chat-backlog-reconciliation`
**Shape:** On a cadence, decisions/bugs/backlog items that exist only in ephemeral AI-chat history are extracted into dated repo docs, then *audited against code and PR evidence* (each item classified completed / partial / active / not-active / unknown), with the standing rule "do not rely on stale chat history — use tracked repo docs."
**Sources:** Repo A `docs/codex/CHAT_BACKLOG_AUDIT_AGAINST_CODEBASE_*.md`, `FULL_CHAT_WORKFLOW_BACKLOG_CONSOLIDATION_*.md`, `MISSING_CHAT_BACKLOG_DETAILS_*.md`; Repo B `docs/137_…`, `docs/138_…`.
**Distinctness:** Not covered by listed skills; complements `ai-sdlc-operating-model`'s "repo is memory" principle with a concrete recurring procedure.
**Confidence: HIGH** (both repos, multiple dated artifacts).

### P14. `timeout-failure-classification`
**Shape:** Every validation command records expected vs. observed duration as first-class evidence; failures caused by timeout are classified `TIMEOUT_FAILURE` (never conflated with regressions), remediated with the smallest safe fix (extend / split / reduce setup), rerun, and recorded — with hard rules against masking real failures by raising timeouts, plus resume-don't-rerun semantics after timeout-only interruptions.
**Sources:** Repo A `docs/ai-workflow.md` ("Validation Duration and Timeout Handling"); Repo B `docs/84_GLOBAL_VALIDATION_TIMEOUT_POLICY.md`, `AGENTS.md` §2C, `run-validation-shards.ps1 -Resume`.
**Confidence: HIGH.**

### P15. `completion-baseline-anchors`
**Shape:** When a phase is done, a short "X is complete and must not be treated as pending" block with immutable evidence (PR number, commit SHA, applied-migration flag) is pinned in the agent rulebook/status docs, preventing future agents from re-litigating or re-implementing finished work.
**Sources:** Repo B `AGENTS.md` §8, `docs/02_ACTIVE_BACKLOG_AND_NEXT_WORK.md`; Repo A context-map status lines.
**Distinctness:** Small but distinct from `agent-startup-context-gate` (which mandates reading) — this is a specific *content element* worth standardizing.
**Confidence: MEDIUM** (clear artifacts, but a convention rather than a mechanism).

### Enrichment notes for existing Aegis skills (not new skills)
- **`ai-closeout-reporter`:** Repo B's verification closeouts add per-surface pass/fail *and negative-path* tables, explicit skip decomposition with reasons, and the discipline that an unqualified "verified complete" statement may only appear once every recorded gap is closed (`docs/165_…`, `166_…`). Repo A adds the required preflight-evidence block in the final report (`Project_Guardrails.md` "Commit gate").
- **`adr-writer`:** Repo A attaches certainty labels ("Accepted (confirmed)") and maintains an index table with status column (`docs/decisions/adr-template.md`).
- **`agent-startup-context-gate`:** both repos implement ordered startup reading lists (Repo B `AGENTS.md` §1A; Repo A "Before Every Task" sections) — useful corroboration, no new shape.
- **`ai-sdlc-operating-model`:** Repo A's platform-role table (which tool reads which entry file, and its role) and Repo B's hub-and-spoke "tool files MUST point back and MUST NOT conflict" rule are two proven topologies worth documenting as options, including Repo B's one-tool-per-surface-per-phase collision rule for two-way-sync platforms (`AGENTS.md` §2E).
- **Certainty-label convention** (confirmed / inferred / unknown; "unverified — recommend confirming" for uncited operational claims) appears in both repos and could be folded into several skills as a shared writing rule.

---

## 5. What Was Intentionally NOT Extracted

- **Product/domain patterns:** tenant-isolation and RLS policy design, role catalogs, device/PIN authentication campaign details, inventory/count/PO lifecycle material, command/event-bus architecture, AI-routing enforcement ladders. These are architecture content, not workflow shape.
- **The one-off "analysis trio"** in Repo A's root (`INVENTORY_WORKFLOW.md` + `TEST_PLAN.md` + `BUG_REPORT.md` — architecture doc / test plan / prioritized bug report generated as a set). Considered as a "deep-dive triptych" pattern but excluded: single occurrence, heavily product-bound (would be LOW confidence).
- **Third-party skills pack** under `.agents/skills/` in both repos (slash-command workflows, project memory, references). It is an installed vendor product, not an in-house convention; extracting it would republish someone else's IP. Only the observation that both repos subordinate it to the repo rulebook ("if a skill conflicts with this file, follow this file") is noted.
- **Patterns already fully covered by shipped Aegis skills:** ADR practice as such (`adr-writer`), incident-response and release runbooks as such (`incident-response-runbook`, `release-readiness-reviewer`), ordered startup reading lists (`agent-startup-context-gate`), and per-change classification-for-approval (`change-classification-gate`) — only their deltas are listed above as enrichments.
- **All concrete identifiers seen during reading:** hosted URLs, repository owner handles, cloud project references, tenant/user UUIDs (e.g., the approved-test-tenant ID embedded in Repo B's deployment template and grant reports), personal names, email addresses, store/device names, and the literal test-marker string (it contains the product name). None appear in this report.
- **Business documents:** `.docx`/`.pdf` PRDs, brand assets, `legal/`, `db_backup/`, and root-level bug/log files were identified by name only and never opened.

---

## 6. Read-Only Rule Tensions Encountered

1. **No write or state-change was attempted in either repo.** All access was via directory listings and file reads; no repo script was executed (several patterns — e.g., the context-map updater, validation classifiers — could only be *behaviorally* confirmed by running them, which would have written logs/status files inside the repos; I relied on reading their source and their committed evidence instead, which is why nothing above is rated below the tier its artifacts support).
2. **Repo A's `docs/REPO_CONTEXT_MAP.md` exceeded the read window** (3,709 lines). I read the first ~1,000 lines, all 80 section headers, and the update-protocol section rather than the full body. The Narrow Exception census (~60 blocks) comes from the header scan, not a full read — a completeness caveat, not a rules violation.
3. **Live identifiers inside workflow docs.** Several otherwise-extractable documents embed production identifiers directly in the workflow text (test-tenant UUID inside the deployment prompt template; project refs inside rulebooks). Noted here because any future Aegis skill derived from P11/P12 should template these as placeholders — the source docs themselves do not separate shape from instance.
4. One PowerShell listing interleaved outputs from batched commands (host vs. pipeline ordering), making a directory listing momentarily ambiguous; it was re-run as a read-only listing. No side effects.

— End of report —
