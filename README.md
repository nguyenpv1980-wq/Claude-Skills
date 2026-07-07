# Claude-Skills

Reusable planning + implementation repository for product-agnostic Claude Code **skills**
and read-only project **subagents**.

The goal is not a pile of prompts. The goal is reusable Claude Code Skills and agents that
make Claude behave like a disciplined senior/principal engineering partner: model before
code, docs before implementation, tests before changes, small diffs, tenant isolation and
security by default, QA evidence before release, and evidence-based troubleshooting.

The repo is built in **phases**. **Phase 0** established the foundation — authoring
standard, templates, eval convention, validator, catalog, the seven read-only reviewer
subagents, and the Step 0 reconciliation of the two earlier planning tracks. **Phase 1**
shipped the first real skills: the 8-skill AI engineering **operating-discipline pack**
(reconciled decision D4). **Phase 2** shipped the 10-skill **core architecture &
engineering pack**. **Phase 3** shipped the 9-skill **SaaS & tenant isolation pack**.
**Phase 4** shipped the 9-skill **security, RLS & supply-chain pack**. **Phase 5**
shipped the 16-skill **QA, E2E, manual QA & evidence pack** (the 13 canonical Phase 5
skills plus 3 pulled forward from the QA backlog: roadmap #184/#185/#204). **Phase 1.5**
shipped the 4-skill **AI-SDLC governance completion** (roadmap #261/#268/#279/#280),
completing the category-08 governance layer Phase 1 started. **Phase 6** shipped the
10-skill **cloud, DevOps, reliability & release pack**. **Phase 7** ships the
14-skill **AI security & LLM systems pack** (v4's 10 plus 4 OWASP LLM Top 10 gap
additions, D6) — see [Skills (shipped)](#skills-shipped) below.

## Start here (canonical reading order)

1. [`docs/reconciliation/step-0-reconciliation-v4.md`](docs/reconciliation/step-0-reconciliation-v4.md) — what was reconciled and why (read first).
2. [`docs/research/claude-skills-architecture-audit-findings-v4.md`](docs/research/claude-skills-architecture-audit-findings-v4.md) — canonical architecture audit.
3. [`docs/prompts/claude-skills-master-generation-prompts-v4.md`](docs/prompts/claude-skills-master-generation-prompts-v4.md) — canonical master + phase prompts.
4. [`docs/300-repeatable-software-saas-skills-roadmap.md`](docs/300-repeatable-software-saas-skills-roadmap.md) — the 300-skill backlog / capability map.
5. [`docs/skills/`](docs/skills/) — category-level backlogs.
6. [`docs/skills-catalog.md`](docs/skills-catalog.md) — implemented vs. backlog, priorities, skills-vs-agents.
7. [`docs/skill-generation-standard.md`](docs/skill-generation-standard.md) — the authoring standard the validator enforces.

**Historical / reference inputs** (superseded by the v4 pair + reconciliation; retained for provenance):

- [`docs/prompts/senior-principal-claude-skills-execution-plan.md`](docs/prompts/senior-principal-claude-skills-execution-plan.md) — earlier combined execution plan (now historical).
- `docs/research/claude-skills-principal-architecture-findings.md`
- `docs/prompts/master-claude-skills-and-agents-development-prompt.md`
- `docs/prompts/phased-claude-skills-prompts.md`
- `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md`
- `docs/150-claude-skills-roadmap.md` (superseded by the 300-skill roadmap)

## Reconciled phase plan (single source of truth)

The v4 phase structure is canonical. See [the reconciliation doc](docs/reconciliation/step-0-reconciliation-v4.md) §3
for the per-phase skill lists and how the older execution-plan names merge in.

| Phase | Pack | Priority | Status |
|---:|---|---|---|
| 0 | Foundation: standard, templates, eval convention, validator, catalog, README, 7 subagents, `_template` | P0 | ✅ merged |
| 1 | AI engineering **operating-discipline** pack (8 skills) | P0 | ✅ merged |
| 1.5 | AI-SDLC **governance completion** (4 skills: roadmap #261/#268/#279/#280) | P0/P1 | ✅ merged |
| 2 | Core architecture & engineering (10) | P0 | ✅ merged |
| 3 | SaaS & tenant isolation (9) | P0/P1 | ✅ merged |
| 4 | Security, RLS & supply chain (9) | P0/P1 | ✅ merged |
| 5 | QA, E2E, manual QA & evidence (16 = 13 canonical + 3 pulled forward from the QA backlog: roadmap #184/#185/#204) | P0/P1 | ✅ merged |
| 6 | Cloud, DevOps, reliability & release (10) | P1 | ✅ merged |
| 7 | AI security & LLM systems (14 = v4's 10 + 4 OWASP LLM Top 10 additions, D6) | P1 | ✅ this branch |
| 7.5 | Agentic AI security (OWASP Agentic Top 10, D7: 6 new + 3 extensions) | P1 | backlog |
| 8 | Backlog expansion in ≤20-skill validated batches | P2 | backlog |

## Subagents (read-only reviewers)

Real project subagents live under `.claude/agents/<name>.md` (reconciled decision D2),
read-only by default. Each maps to a v4 orchestrator role (see reconciliation §5):

| Subagent | Lens |
|---|---|
| `principal-architecture-reviewer` | Architecture boundaries, coupling, data ownership, scalability. |
| `secure-saas-reviewer` | Tenant isolation, RLS, authz, secrets, cross-tenant leakage. |
| `qa-automation-lead` | Test strategy, coverage gaps, flake risk, release evidence. |
| `full-codebase-auditor` | Whole-repo inventory, evidence-based risk, debt map. |
| `senior-troubleshooting-lead` | Reproduction, hypothesis ranking, root cause. |
| `ai-security-red-team-reviewer` | Prompt injection, tool/RAG abuse, data exfil. |
| `release-readiness-reviewer` | CI/build/test evidence, migrations, rollback, go/no-go. |

## Skills (shipped)

Phase 1 — AI engineering operating-discipline pack, under `.claude/skills/<name>/`
(full detail: [`docs/skills-catalog.md`](docs/skills-catalog.md)):

| Skill | What it does | Invocation |
|---|---|---|
| `agent-startup-context-gate` | Verifies repo identity and loads governing context before any work; halts when the location can't be verified (a path that exists is not proof it's the right repo). | auto + manual |
| `source-of-truth-reconciler` | Resolves conflicts between instructions, docs, code, tests, and memory by evidence-cited precedence; surfaces every assumption. | auto + manual |
| `change-classification-gate` | Classifies a change before work → validation floor + approval path; locks scope to the approved class. | auto + manual |
| `human-approval-boundary` | Halts for explicit approval before schema, RLS/security, prod-data, secrets, deploy, billing, or destructive work; stops when security impact is unclear. | auto + manual |
| `reviewable-diff-discipline` | Keeps diffs small and intentional; stages exact files only; staged set must equal declared intent. | auto + manual |
| `ai-closeout-reporter` | Terminal closeout report with a mandatory "intentionally not done / omitted" section — scope reductions are never silent. | auto + manual |
| `agent-failure-recovery` | Preserve-first recovery from broken git/tree state; destructive cleanup only with backup + explicit approval. | **manual only** |
| `agent-instruction-consolidator` | Aligns CLAUDE.md / AGENTS.md / Cursor / Copilot instruction files to one canonical source with rule-preservation proof. | **manual only** |

Phase 1.5 — AI-SDLC governance completion (roadmap #261/#268/#279/#280; completes the
category-08 layer Phase 1 started — composes the Phase 1 skills, never restates them):

| Skill | What it does | Invocation |
|---|---|---|
| `ai-sdlc-operating-model` | End-to-end human+agent lifecycle contract: named stages with entry/exit gates, per-stage authority (human / agent / agent-with-approval), enforcing skill per stage, failure routing, learning loop; grounded in observed PR practice with a gap list. | auto + manual |
| `agent-authorization-matrix` | Deny-by-default action × context matrix of standing agent authority — merge to protected branches requires a named human always; auto-merge arming is forbidden to agents (armed state re-checked after every push); approval scope/expiry semantics; proposal-first. | **manual only** |
| `agent-memory-governance` | Persistent-memory WRITE/TRUST/HYGIENE rules: confirmed durable facts with provenance and absolute dates, never secrets; remembered repo/PR state verified against live git/gh before acting; disposition-approved cleanups. | **manual only** |
| `agent-governance-audit` | Audits one AI-assisted change's process compliance from primary evidence (PR timeline incl. who armed auto-merge, commits, CI runs): per-control PASS/FAIL/UNVERIFIABLE verdicts; closeout claims cross-checked; missing evidence is never a PASS. | auto + manual |

Phase 2 — core architecture & engineering pack:

| Skill | What it does | Invocation |
|---|---|---|
| `domain-modeler` | Domain model from requirements/code — language, bounded contexts, aggregates with invariants; hard "do not code yet" gate at the end. | auto + manual |
| `architecture-designer` | Inspects the CURRENT architecture first, then component/dependency/data-ownership maps, tradeoffs, ADR draft, and an incremental migration plan. | auto + manual |
| `adr-writer` | Architecture Decision Records with honest alternatives, consequences, operational impact, mandatory rollback/reversal plan and review date. | auto + manual |
| `docs-first-implementer` | Pins the exact installed library version (lockfile), reads version-matching docs before coding, verifies with real commands; declares uncertainty instead of guessing. | auto + manual |
| `tdd-engineer` | Strict red-green-refactor: confirms each test fails for the intended reason before the minimal implementation; reports exact commands and results. | auto + manual |
| `systematic-debugger` | Reproduce → reduce → isolate → fix one thing → verify → prevent; prediction-tested hypotheses, single-variable fixes, regression test kept. | auto + manual |
| `code-reviewer` | Reviews actual diffs only — severity-ranked findings with file:line evidence and remediation; no diff, no review. | auto + manual |
| `code-simplifier` | Behavior-preserving simplification with the suite green before and after every move; coverage gate; restraint ("not done" list) is a deliverable. | **manual only** |
| `principal-code-analyst` | Subsystem-level strategic analysis laddering code findings to architecture, security, cost; risk register + small-step remediation with validation signals. | auto + manual |
| `full-codebase-auditor` | Whole-repo audit with inventory-first coverage; findings filed as confirmed / likely / hypotheses / missing information. (Skill = procedure; same-named subagent composes it.) | auto + manual |

Phase 3 — SaaS & tenant isolation pack:

| Skill | What it does | Invocation |
|---|---|---|
| `saas-platform-architect` | Platform structure: per-component pooled/siloed/bridge decisions with named isolation mechanisms, control-plane/data-plane split, capability inventory, rollout plan with per-step rollback. | auto + manual |
| `tenant-modeler` | Tenant semantics: definition, hierarchy, membership-as-entity (roles on membership), invitations, ownership, and a lifecycle state machine with per-state access/data/billing/jobs posture. | auto + manual |
| `tenant-isolation-reviewer` | Reviews real systems for cross-tenant leakage across all 15 surfaces (identity → audit, incl. AI retrieval); evidence-cited findings, isolation test matrix, negative tests, honest not-inspected list. | auto + manual |
| `multi-tenant-data-architect` | Per-store tenant scoping decisions (incl. caches, search, vector stores), server-derived tenant-context propagation, ownership map, expand→contract migration with verification and rollback. | auto + manual |
| `authorization-matrix-designer` | Deny-by-default roles × permissions × resources matrix, object-level rules, enforcement-point map, brokered support access, negative tests, additive role migration. | auto + manual |
| `plan-entitlement-architect` | Plan × entitlement matrix with one resolution point enforced uniformly on every surface; metering hooks; plan transitions with no silent data loss; grandfathering + rollback. | auto + manual |
| `audit-log-architect` | Audit event taxonomy, versioned record schema, append-only integrity with explicit write-failure policy, retention/redaction, tenant-scoped access, negative tests. | auto + manual |
| `saas-cost-architect` | Bill-grounded cost drivers, per-tenant attribution (or admitted overhead), distribution-based unit economics vs revenue, exposure math, guardrails with observe-first rollout. | auto + manual |
| `api-event-architect` | External API/event contracts: credential-derived tenant context, idempotency, per-tenant/plan rate limits, versioning with dual-run deprecation, tenant-scoped signed webhooks. | auto + manual |

Phase 4 — security, RLS & supply-chain pack:

| Skill | What it does | Invocation |
|---|---|---|
| `threat-modeler` | Design-time threat model: assets/actors/trust-boundaries, STRIDE per boundary, abuse cases, exploit-path-gated severity, mitigations mapped to negative tests; consumes tenant/authz outputs instead of re-deriving them. | auto + manual |
| `appsec-implementer` | Implements one NAMED security control test-first — negative test red→green, minimal server-side control, scoped diff, residual risk stated. | **manual only** |
| `multi-tenant-security-tester` | Executable cross-tenant/authorization negative suite: two-tenant fixtures, forbidden-action-denied assertions, positive controls, IDOR/list/mass-assignment/exports/jobs, honest coverage. | auto + manual |
| `rls-policy-auditor` | Per-command RLS audit/authoring (merges rls-policy-author + rls-negative-test-designer): recursion, unsafe SECURITY DEFINER, broad grants, missing tenant scope, service-role leakage, frontend-derived scope; mandatory negative-test plan; policies delivered as a migration, never run live. | auto + manual |
| `secrets-identity-hardener` | Env classification (catches VITE_/NEXT_PUBLIC_ leaks), moves secrets server-side with a client-bundle-absence proof, rotates leaked credentials, least-privilege service accounts, session/token flags. | **manual only** |
| `supply-chain-security-reviewer` | SLSA-style: lockfile-based dependency set, reachability triage of scanner output, install/build-script and CI compromise paths, SHA pinning, compromise-path-gated severity. | auto + manual |
| `security-pr-reviewer` | Security lens on an actual diff: authz/object-level/tenant-scope, injection, secrets, SSRF, control-weakening detection; exploit-path-gated findings; no diff, no review. | auto + manual |
| `secure-migration-reviewer` | Whole-migration deploy safety: RLS/policy gaps, GRANT widening, unsafe defaults, destructive/irreversible ops, tenant-scoped backfills, lock risk, expand→contract deploy order, rollback; delegates policy text to `rls-policy-auditor`. | auto + manual |
| `static-analysis-reviewer` | Triages SAST/CodeQL/SARIF on first-party code: dedup, confirm-against-code disposition (TP/FP/dup/accepted), five-axis ranking (reachability/exploitability/asset/tenant/business), written suppression policy. | auto + manual |

Phase 5 — QA, E2E, manual QA & evidence pack (13 canonical + 3 pulled forward from the
QA backlog, roadmap #184/#185/#204):

| Skill | What it does | Invocation |
|---|---|---|
| `qa-strategy-architect` | Product-level QA strategy: ranked risk inventory → cheapest-reliable-layer decisions, explicit automation/manual split, evidence per change class, CI gates, ownership. | auto + manual |
| `test-plan-designer` | Per-change test plan: risk-traced items with layer/data/environment, objective entry/exit criteria, named artifacts and CI placement, explicit out-of-scope list. | auto + manual |
| `test-coverage-mapper` | Coverage audit: surface inventory first, maps tests by reading assertions (theater ≠ coverage), risk-ranked gaps with cheapest fill layer, honest not-inspected list. | auto + manual |
| `qa-automation-architect` | Automation blueprint: tools per layer with rationale, structure/fixtures/auth-state, parallel-safe isolation, CI tiers with bounded logged retries, flake policy, migration steps. | auto + manual |
| `playwright-e2e-engineer` | Critical-journey Playwright specs: role/label locators, web-first assertions, zero sleeps/networkidle, storageState per persona, failure traces, honest run reports. | **manual only** |
| `clickthrough-test-engineer` | Pre-planned interactive walkthrough of a running app (forms with invalid input, dialogs, permissions, states, console), severity-rated defects with masked evidence, honest coverage. | **manual only** |
| `manual-test-case-creator` | Stranger-executable manual cases: exact data/roles/environment, one observable expected result per step, screenshot checkpoints, verdict rules, cleanup. | auto + manual |
| `screenshot-evidence-planner` | Evidence policy: risk-justified checkpoints, deterministic naming, mandatory pre-storage masking, metadata, storage/retention classes, case/PR/closeout linkage. | auto + manual |
| `vitest-unit-component-engineer` | Vitest unit/component tests: intentional node-vs-DOM environment per file, owned-seam mocks, Testing Library queries, determinism, real run output. | **manual only** |
| `vite-build-qa-engineer` | Build-artifact QA: `VITE_` env classification, dist-level secret proof, build/preview parity (base, deep links, modes), bundle budgets, sourcemap policy. | **manual only** |
| `flaky-test-detective` | Classify → reproduce with counts → fix ONE cause → prove stability; no retries/sleeps/weakened assertions; product races routed as product bugs; quarantine with owner/ticket/expiry. | auto + manual |
| `test-data-architect` | Test-data design: read-only persona/baseline catalog, per-layer sources, determinism, worker-scoped isolation, synthetic-only PII posture, cleanup + seed evolution. | auto + manual |
| `regression-suite-curator` | Evidence-based promote/retain/demote/retire with written rationale, protected security regressions, enforced quarantine registry, tier-budget fit. | auto + manual |
| `integration-test-designer` | (pulled forward, #184) The layer between unit and E2E: real service/command/DB/auth/permission boundaries, named faked seams, persisted-state assertions, no browser. | auto + manual |
| `api-contract-test-designer` | (pulled forward, #185) Contract verification: provider/consumer roles, schema + error-envelope validation, additive-vs-breaking CI gate, version coverage; design stays with `api-event-architect`. | auto + manual |
| `accessibility-test-harness` | (pulled forward, #204) WCAG-pinned a11y harness: automated scans (baseline+ratchet) AND manual keyboard/focus/contrast/screen-reader checklists; honest about automation limits. | auto + manual |

Phase 6 — cloud, DevOps, reliability & release pack (`rollback-strategy-designer`
merged into `rollback-runbook-author` per reconciliation §3):

| Skill | What it does | Invocation |
|---|---|---|
| `cloud-architecture-decider` | Cloud-neutral platform decision: nine-axis requirements record, provider-neutral logical architecture, isolation/compliance hard filters before scoring, managed-vs-self-hosted with the operational bill, exit costs and reopen triggers. | auto + manual |
| `azure-saas-architect` | Maps a decided logical architecture to provider-idiomatic Azure: Entra ID/managed identities/OIDC, VNets + Private Link, per-store tenant isolation, compute by team maturity, Azure Policy/Defender posture, Bicep/Terraform, tag-keyed cost controls; SKU/limit/price claims become verification items. | auto + manual |
| `aws-saas-architect` | Maps a decided logical architecture to provider-idiomatic AWS: Organizations/SCPs, IAM roles + OIDC, VPC/PrivateLink, per-store tenant isolation, compute by team maturity, Security Hub/GuardDuty posture, Terraform/CDK, cost-allocation tags; quota/type/price claims become verification items. | auto + manual |
| `iac-reviewer` | Review-only IaC audit with blast radius first: destructive replaces, public exposure, IAM width deltas, secrets in code and state, tenant-isolation impact, drift, pinning, cost flags; never applies or runs plan against live backends. | auto + manual |
| `ci-pipeline-architect` | Pipeline stage graph with blocking semantics and a latency budget, CI secret governance (OIDC over stored keys, fork-PR posture), artifact provenance, promotion gates with named humans, branch-protection alignment; composes qa-automation-architect tiers. | **manual only** |
| `release-readiness-reviewer` | Evidence-based ship/no-ship gate: every dimension cites a verifiable artifact or is MISSING; CI evidence pinned to the release SHA; unknown = No-Go with the evidence that flips it. (Skill = procedure; same-named subagent composes it.) | auto + manual |
| `rollback-runbook-author` | Rollback strategy + stranger-executable runbook in one artifact: decision criteria with time-box, per-layer primitives in order, bad-window data repair, rehearsal log and staleness triggers; authors only, never executes. | auto + manual |
| `observability-operator` | Hands-on observability: structured redacted instrumentation, truthful health checks, alerts with severity/owner/runbook-link/justified threshold, query-verified claims, silences only with owner+expiry. | **manual only** |
| `slo-reliability-architect` | Journey-derived SLOs: symptom-based SLIs with measurement points, error budgets in user units, burn-rate paging with cause-alert demotion, budget policy with consequences, per-tenant reliability views. | auto + manual |
| `incident-response-runbook` | Incident machinery: one-minute severity ladder, IC/comms/ops roles, triage to decision points, containment invoking the rollback artifact by reference, tenant-aware comms, blameless postmortem where every finding lands as a test/alert/fix or owned risk. | auto + manual |

Phase 7 — AI security & LLM systems pack (14 = v4's 10 + 4 OWASP LLM Top 10 gap
additions, D6). Anchored to the OWASP Top 10 for LLM Applications (2025); these
skills **compose** the shipped tenant/security/cost/governance packs rather than
re-deriving them. **LLM03** is extend-existing (the shipped
`supply-chain-security-reviewer` was extended to models/datasets/adapters);
**LLM10** DoS/denial-of-wallet is baked into `ai-cost-guardrail-designer`;
`ai-evaluation-harness` absorbs the AI security test harness:

| Skill | What it does | Invocation |
|---|---|---|
| `ai-threat-modeler` | AI-specific threat model: AI assets + trust boundaries (all untrusted content), per-boundary threats anchored to the OWASP LLM Top 10, abuse cases, exploit-path-gated severity, each mitigation mapped to an owning skill + red-team case; composes `threat-modeler` for the classic surface. | auto + manual |
| `prompt-injection-defender` | Layered injection defense (LLM01): trust zones, the untrusted-content invariant, content/instruction separation, and the primary layer — deterministic action authorization OUTSIDE the model; direct + indirect payloads; red-team suite with SAFE-outcome assertions. | **manual only** |
| `rag-security-architect` | RAG/vector-store security (LLM08): authorization AT RETRIEVAL TIME (never post-filter), per-tenant index scoping, document-ACL propagation, embedding risks (inversion/membership/poisoning/stale-permission); composes `tenant-isolation-reviewer` + `multi-tenant-data-architect`. | auto + manual |
| `agent-tool-safety-guard` | Least-privilege tool access (LLM06): per-tool blast-radius matrix, calling-user authority (no service-account confused deputy), argument validation before execution, approval gates on irreversible actions, tool-chain abuse; composes `human-approval-boundary` + `agent-authorization-matrix`. | auto + manual |
| `llm-output-safety-reviewer` | Output-handling review (LLM05): model output as untrusted data to render/execute/URL/tool/store sinks (XSS/RCE/SSRF/injection/second-order), context-correct encoding, generated-code sandboxing; exploit-flow-gated findings. | auto + manual |
| `ai-evaluation-harness` | Versioned eval dataset (representative + adversarial/red-team + regression), per-dimension graders + thresholds (quality/schema/safety/grounding/injection/latency/cost), CI regression gate; absorbs the AI security test harness; honest real-run reporting. | **manual only** |
| `ai-cost-guardrail-designer` | Consumption guardrails (LLM10 DoS/denial-of-wallet): per-request token caps, tenant-scoped budgets/rate limits, agent loop/recursion bounds, fail-safe degraded mode + kill switch, burn-rate alerts before exhaustion; composes `saas-cost-architect` + `observability-operator`. | auto + manual |
| `ai-governance-risk-reviewer` | AI governance/risk posture: impact-based risk tiering, oversight-to-tier matching, accountable ownership, AI disclosure/consent, model/feature card, obligation→control mapping (EU AI Act tiers, NIST AI RMF) without asserting legal conclusions. | auto + manual |
| `ai-router-architect` | Centralized model-routing layer: one interface, server-side-only credentials, task/cost routing, choke-point cost enforcement, per-call telemetry, resilient fallback + circuit breaker + no-deploy kill switch, idempotent retries; composes `secrets-identity-hardener` + `observability-operator`. | **manual only** |
| `structured-output-validator` | Output-shape contract (LLM05 companion): schema (fields/types/enums/ranges), validate-before-use, semantic checks beyond shape (tenant-scoped ids), bounded failure handling; shape-is-not-safety handoffs to `llm-output-safety-reviewer` + `agent-tool-safety-guard`. | auto + manual |
| `sensitive-disclosure-guard` | (NEW, LLM02) Disclosure defense: data-minimization + pre-model redaction of secrets/PII/other-tenant data, output-path echo/bleed checks, log redaction at emission, provider retention/training posture; composes `tenant-isolation-reviewer` + `secrets-identity-hardener`. | auto + manual |
| `model-poisoning-reviewer` | (NEW, LLM04) Training/feedback/ingestion integrity: contributor-trust assessment, poisoning paths, feedback-loop Sybil defense, ingestion-as-truth integrity, provenance/holdout controls; acquire-vs-ingest boundary with `supply-chain-security-reviewer`. | auto + manual |
| `system-prompt-leakage-reviewer` | (NEW, LLM07) Two axes: no secrets in the prompt AND no security dependence on prompt secrecy — **system prompts are NOT security controls**; enforcement is deterministic and lives OUTSIDE the LLM; extraction-is-harmless framing. | auto + manual |
| `ai-misinformation-guard` | (NEW, LLM09) Grounding in retrieved sources (not memory), citation-to-claim verification, calibrated uncertainty/refusal, fact validation before action, package/API hallucination (slopsquatting) checks, overreliance-aware UX. | auto + manual |

## Authoring a new skill

1. Read [`docs/skill-generation-standard.md`](docs/skill-generation-standard.md).
2. Copy `.claude/skills/_template/` to `.claude/skills/<your-skill-name>/`.
3. Set frontmatter `name` to match the new directory exactly.
4. Fill in all required sections; keep `SKILL.md` under 500 lines (push detail to `references/`).
5. Add `evals/evals.json` (and `evals/trigger-evals.json` if the trigger overlaps another skill).
6. List the skill in [`docs/skills-catalog.md`](docs/skills-catalog.md) **and** this README.
7. Run the validator until it passes.

Side-effecting skills (writes, network, deploy, spend) MUST set `disable-model-invocation: true`
and document the irreversible step under **Stop Conditions**.

## Validation

Run from the repo root:

```bash
python scripts/validate-skills.py
```

Checks: `name` matches directory; `description` present and < 1024 chars; no broad
`allowed-tools`; `SKILL.md` < 500 lines; all required sections present; `evals/evals.json`
exists and parses (structural only — no runner yet); `evals/trigger-evals.json` parses when
present; catalog integrity (every skill listed in catalog + README, none claimed that don't
exist); bundled-name collision and duplicate-name checks.

Behavior: `_template` is ignored. When `_template` is the only skill directory, the validator
prints a "no skills found" status and exits `0`. Exit `0` = clean (warnings allowed); non-zero
= at least one error. Run it before every commit that touches `.claude/skills/`.

## CI (merge gate)

Every pull request targeting `main` runs
[`.github/workflows/validate-skills.yml`](.github/workflows/validate-skills.yml), which
provides two required status checks:

| Check | What it does |
| --- | --- |
| `validate-skills` | Runs `python scripts/validate-skills.py` on the PR (latest Python 3.x). Fails on any validator error — same checks as running it locally. |
| `gate-guard` | Diffs the PR against its base and **fails if the PR touches the merge gate itself** (anything under `.github/workflows/` or `scripts/validate-skills.py`). Such PRs print `This PR modifies the merge gate itself and requires manual review and merge.` and must be reviewed and merged manually by a human. |

Notes:

- Both job names are registered as required status checks — do not rename them (and keep
  them unique across all workflows) without updating branch protection.
- A `gate-guard` failure is not a defect; it is the intended signal that the change needs
  human eyes. Fixing the gate to "make CI green" defeats its purpose.
- The gate uses only `actions/checkout` and `actions/setup-python` — no third-party actions.
- Auto-merge is enabled per-phase via `gh pr merge --auto --squash` — never for changes
  touching the merge gate itself (see
  [`docs/reconciliation/auto-merge-policy.md`](docs/reconciliation/auto-merge-policy.md)).

## Target repository layout

```text
.claude/
  agents/                 # real read-only reviewer subagents
    <agent-name>.md
  skills/
    _template/            # reference template (ignored by validator)
    <skill-name>/
      SKILL.md
      references/
      assets/
      evals/
        evals.json
        trigger-evals.json   # when trigger overlaps another skill

docs/
  reconciliation/  research/  prompts/  roadmaps/  skills/  templates/
  skill-generation-standard.md
  skills-catalog.md

scripts/
  validate-skills.py
```

## Core rules

- Skills are reusable procedures, not essays. Agents are isolated read-only specialists.
- Build in waves. Do not create all 300 skills at once (roadmap = backlog, not a batch command).
- Start with standards, templates, eval convention, and validators (Phase 0).
- Every skill needs `SKILL.md` with clear frontmatter, concise workflow, output format,
  validation checklist, gotchas, stop conditions, and `evals/evals.json`.
- Avoid broad `allowed-tools`; use `disable-model-invocation: true` for side-effect workflows.
- Use read-only exploration first for audits, architecture, code, security, and QA review.
- Treat security, tenant isolation, QA evidence, and verification as first-class requirements.
- Keep product-specific skills out of this reusable foundation.

## Safety note

Claude Code Skills and subagents can influence future code, tests, reviews, and tool usage.
Review every generated skill and agent before trusting it. A reusable skill library is useful
only if it is specific, testable, constrained, maintained, and validated.
