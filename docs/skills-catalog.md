# Skills & Agents Catalog

Single source of truth for what skills and subagents exist, what is planned, and how the two
differ. The backlog below is derived from the **reconciled phase lists**
([`docs/reconciliation/step-0-reconciliation-v4.md`](reconciliation/step-0-reconciliation-v4.md) §3)
and the **category backlogs** under [`docs/skills/`](skills/). `scripts/validate-skills.py`
checks that every *implemented* skill is listed here and in `README.md`.

> **Status:** Phase 0 (foundation), Phase 1 (the 8-skill operating-discipline pack,
> decision D4), and Phase 2 (the 10-skill core architecture & engineering pack) are
> implemented. `_template` remains a reference template ignored by the validator.
> Everything under "Backlog" is planned, not built.

---

## Skills vs. Agents

| | **Skill** (`.claude/skills/`) | **Subagent** (`.claude/agents/`) |
| --- | --- | --- |
| What it is | A reusable *procedure* — an ordered workflow Claude loads and executes. | A read-only *reviewer persona* spawned to judge a delimited task in its own context. |
| Invocation | Triggers on its `description`, or explicitly by name. | Delegated to via the Agent tool. |
| Tools | Inherits session tools; narrows via `allowed-tools`. | Declares its own tools; **read-only by default** (decision D2). |
| Best for | Repeatable transformations/generation with a defined output + evals. | Focused review/audit passes that benefit from isolation and a specialized lens. |
| Rule of thumb | If it *does* something and produces an artifact → skill. | If it *judges* something and returns findings → agent. |

Agents **compose** skills; they must not duplicate skill bodies. Role → subagent mapping is
in the reconciliation doc §5.

---

## Priority definitions

| Tier | Meaning |
| --- | --- |
| **P0** | Foundation + operating discipline + core engineering/SaaS/security/QA that must exist before the library is trustworthy. Phases 0–5 skew P0. |
| **P1** | High-value packs that build on P0: cloud/DevOps/reliability and AI security (Phases 6–7), plus P1 items inside earlier phases. |
| **P2** | Remaining 300-roadmap breadth, generated in Phase 8 batches of ≤20 after P0/P1 prove the pattern. |

---

## Implemented (Phases 0–1)

### Foundation (Phase 0)

| Item | Type | Status |
| --- | --- | --- |
| `docs/skill-generation-standard.md` | standard | ✅ |
| `docs/templates/skill-template.md` | template | ✅ |
| `docs/templates/evals-template.json` | template | ✅ |
| `docs/reconciliation/step-0-reconciliation-v4.md` | reconciliation record | ✅ |
| `docs/skills-catalog.md` | this catalog | ✅ |
| `scripts/validate-skills.py` | validator | ✅ |
| `.claude/skills/_template/` | reference template skill (ignored by validator) | ✅ |

### Subagents (read-only reviewers)

| Subagent | v4 role | Status |
| --- | --- | --- |
| `principal-architecture-reviewer` | Principal Claude Architect | ✅ |
| `secure-saas-reviewer` | SaaS Security & Tenant Isolation | ✅ |
| `qa-automation-lead` | QA Automation & Release Evidence | ✅ |
| `full-codebase-auditor` | Full Codebase Audit | ✅ |
| `senior-troubleshooting-lead` | Senior Troubleshooting | ✅ |
| `ai-security-red-team-reviewer` | AI Security & LLM Systems | ✅ |
| `release-readiness-reviewer` | Release Captain | ✅ |

### Skills (Phase 1 — operating-discipline pack)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json` (structural
convention, decision D3 — present and well-formed, not "passing").

| Skill | Roadmap ref (cat 08) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `agent-startup-context-gate` | #262 | yes | Verify repo identity + load governing context before any work; halt when the location can't be verified. |
| `source-of-truth-reconciler` | #269 (+#270 assumption-surfacing) | yes | Resolve doc/code/instruction conflicts by evidence-cited precedence; surface all assumptions. |
| `change-classification-gate` | #264 (+#263 scope lock) | yes | Classify a change → validation floor + approval path; lock scope to the approved class. |
| `human-approval-boundary` | #265 (+#270 stop-when-unclear) | yes | Halt for explicit approval at high-risk boundaries with a structured approval request. |
| `reviewable-diff-discipline` | #271 (+#272 exact-file staging) | yes | Small intentional diffs; exact-path staging; staged set must equal declared intent. |
| `ai-closeout-reporter` | #274 | yes | Terminal closeout with a mandatory "intentionally not done / omitted" section. |
| `agent-failure-recovery` | #275 | **no** (manual-only; mutates git state) | Preserve-first recovery of broken git/tree state; destructive cleanup needs backup + approval. |
| `agent-instruction-consolidator` | #276 | **no** (manual-only; edits behavior-steering files) | Align agent instruction files to one canonical source with rule-preservation proof. |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for the two overlap clusters:
context/truth (`agent-startup-context-gate`, `source-of-truth-reconciler`) and
change governance (`change-classification-gate`, `human-approval-boundary`,
`reviewable-diff-discipline`).

### Skills (Phase 2 — core architecture & engineering pack)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json` **and**
`evals/trigger-evals.json` (all ten sit in one of three overlap clusters).

| Skill | Source (category doc) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `domain-modeler` | cat 01 #3 (Domain Model Discovery) | yes | Domain model from requirements/code — language, contexts, aggregates + invariants; ends at a hard "do not code yet" gate. |
| `architecture-designer` | cat 01 #42/#55 | yes | Inspects CURRENT architecture first; component/dependency/data-ownership maps, tradeoffs, ADR draft, incremental migration plan. |
| `adr-writer` | cat 01 #1 (ADR Authoring) | yes | ADR with honest alternatives, consequences, operational impact, mandatory rollback/reversal plan + review date. |
| `docs-first-implementer` | cat 08 discipline (ex-`grill-with-docs`) | yes | Pin the EXACT installed version (lockfile), read matching docs, summarize task syntax, implement, verify; uncertainty declared, never guessed. |
| `tdd-engineer` | cat 06 | yes | Strict red-green-refactor; confirms each test fails for the INTENDED reason before implementing the minimal change; exact commands reported. |
| `systematic-debugger` | cat 06/08 | yes | Reproduce → reduce → isolate → fix ONE thing → verify → prevent; prediction-tested hypotheses, no shotgun fixes. |
| `code-reviewer` | cat 08 #277 (AI Code Review Protocol) | yes | Reviews ACTUAL diffs only; severity-ranked findings with file:line evidence + remediation; no diff, no review. |
| `code-simplifier` | cat 01 #11 adjacent | **no** (manual-only; edits working code) | Behavior-preserving simplification, green-before-and-after per move; coverage gate; "not done" list is a deliverable. |
| `principal-code-analyst` | cat 01 | yes | Subsystem strategic read: findings laddered to architecture/security/cost claims; risk register; small-step remediation + validation plan. |
| `full-codebase-auditor` | cat 06/08 #280 | yes | Whole-repo audit, inventory BEFORE findings; results filed as confirmed / likely / hypotheses / missing information; provable coverage. |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for the three Phase 2 clusters:
design (`domain-modeler`, `architecture-designer`, `adr-writer`), implementation
(`docs-first-implementer`, `tdd-engineer`, `systematic-debugger`), and review/audit
(`code-reviewer`, `code-simplifier`, `principal-code-analyst`, `full-codebase-auditor`).

> Namespace note (intended, see Phase 6 note below): `full-codebase-auditor` exists as
> both a **subagent** (`.claude/agents/`, the review lens) and this **skill**
> (`.claude/skills/`, the procedure). The agent composes the skill.

---

## Backlog by phase (reconciled)

The v4 phase structure is canonical. Each phase's first-pass skills are listed; see the
reconciliation doc §3 for merge/move notes and the per-phase "expansion backlog."

### Phase 1 — AI operating-discipline pack (P0)
✅ **Implemented** — all 8 skills moved to [Implemented → Skills](#skills-phase-1--operating-discipline-pack) above.
Source: [`docs/skills/08-ai-era-sdlc-agent-ops.md`](skills/08-ai-era-sdlc-agent-ops.md).

### Phase 2 — Core architecture & engineering (P0)
✅ **Implemented** — all 10 first-pass skills moved to
[Implemented → Skills (Phase 2)](#skills-phase-2--core-architecture--engineering-pack) above.
Source: [`docs/skills/01-software-architecture-engineering.md`](skills/01-software-architecture-engineering.md),
[`04-backend-api-data-engineering.md`](skills/04-backend-api-data-engineering.md).
The Phase 2 **expansion backlog** (reconciliation §3: `api-contract-designer`,
`idempotency-first-designer`, `validation-boundary-designer`, `observability-by-design`,
`operational-runbook-author`, `system-context-mapper`, `bounded-context-identifier`,
`dependency-direction-guard`, `refactor-safety-planner`) remains backlog, built in
Phase 8 batches.

### Phase 3 — SaaS & tenant isolation (P0/P1)
`saas-platform-architect`, `tenant-modeler`, `tenant-isolation-reviewer`,
`multi-tenant-data-architect`, `authorization-matrix-designer`, `plan-entitlement-architect`,
`audit-log-architect`, `saas-cost-architect`, `api-event-architect`.
Source: [`docs/skills/02-saas-platform-architecture.md`](skills/02-saas-platform-architecture.md).

### Phase 4 — Security, RLS & supply chain (P0/P1)
`threat-modeler`, `appsec-implementer`, `multi-tenant-security-tester`, `rls-policy-auditor`,
`secrets-identity-hardener`, `supply-chain-security-reviewer`, `security-pr-reviewer`,
`secure-migration-reviewer`, `static-analysis-reviewer`.
Source: [`docs/skills/03-saas-security-rls.md`](skills/03-saas-security-rls.md).

### Phase 5 — QA, E2E, manual QA & evidence (P0/P1)
`qa-strategy-architect`, `test-plan-designer`, `test-coverage-mapper`, `qa-automation-architect`,
`playwright-e2e-engineer`, `clickthrough-test-engineer`, `manual-test-case-creator`,
`screenshot-evidence-planner`, `vitest-unit-component-engineer`, `vite-build-qa-engineer`,
`flaky-test-detective`, `test-data-architect`, `regression-suite-curator`.
Source: [`docs/skills/06-qa-test-engineering.md`](skills/06-qa-test-engineering.md),
[`05-frontend-ux-engineering.md`](skills/05-frontend-ux-engineering.md).

### Phase 6 — Cloud, DevOps, reliability & release (P1)
`cloud-architecture-decider`, `azure-saas-architect`, `aws-saas-architect`, `iac-reviewer`,
`ci-pipeline-architect`, `release-readiness-reviewer`, `rollback-runbook-author`,
`observability-operator`, `slo-reliability-architect`, `incident-response-runbook`.
Source: [`docs/skills/07-devops-release-reliability.md`](skills/07-devops-release-reliability.md).

> Note: `release-readiness-reviewer` and `full-codebase-auditor` exist as **subagents**
> (review lens) and also as **skills** (procedure) — `full-codebase-auditor` skill shipped
> in Phase 2; `release-readiness-reviewer` skill is planned here. Different namespaces
> (`.claude/agents/` vs `.claude/skills/`); the agent composes the skill.

### Phase 7 — AI security & LLM systems (P1)
`ai-threat-modeler`, `prompt-injection-defender`, `rag-security-architect`,
`agent-tool-safety-guard`, `llm-output-safety-reviewer`, `ai-evaluation-harness`,
`ai-cost-guardrail-designer`, `ai-governance-risk-reviewer`, `ai-router-architect`,
`structured-output-validator`.
Source: [`docs/skills/09-ai-software-engineering.md`](skills/09-ai-software-engineering.md).

### Phase 8 — Backlog expansion (P2)
Remaining roadmap skills, generated in validated batches of ≤20 (see reconciliation §4.1).

---

## Capability map (300-skill roadmap)

The full backlog lives in [`docs/300-repeatable-software-saas-skills-roadmap.md`](300-repeatable-software-saas-skills-roadmap.md):

| Category | Count | Document |
| --- | ---: | --- |
| Software Architecture & Engineering | 55 | [`01`](skills/01-software-architecture-engineering.md) |
| SaaS Platform Architecture | 35 | [`02`](skills/02-saas-platform-architecture.md) |
| SaaS Security, Multi-Tenancy & RLS | 40 | [`03`](skills/03-saas-security-rls.md) |
| Backend, API & Data Engineering | 30 | [`04`](skills/04-backend-api-data-engineering.md) |
| Frontend & UX Engineering | 20 | [`05`](skills/05-frontend-ux-engineering.md) |
| QA, Test Architecture & Validation | 55 | [`06`](skills/06-qa-test-engineering.md) |
| DevOps, Release & Reliability | 25 | [`07`](skills/07-devops-release-reliability.md) |
| AI-Era SDLC & Agent Operating Discipline | 20 | [`08`](skills/08-ai-era-sdlc-agent-ops.md) |
| AI Software Engineering & LLM Systems | 20 | [`09`](skills/09-ai-software-engineering.md) |
| **Total** | **300** | |

---

## Evals & validation note

Every implemented skill must ship `evals/evals.json` (and `evals/trigger-evals.json` when its
trigger overlaps another skill). **Evals are structurally validated only — there is no runner
yet (decision D3).** Run `python scripts/validate-skills.py` before every commit that touches
`.claude/skills/`.
