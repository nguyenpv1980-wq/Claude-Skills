# Product-Agnostic Claude Skills and Agents Roadmap

Prepared: 2026-07-06
Purpose: define a reusable, product-agnostic roadmap for Claude Code Skills and project subagents.

## Executive position

This roadmap turns Claude into a disciplined engineering partner. It is not a prompt dump and not a project-specific memory file.

The first objective is not maximum skill count. The first objective is reusable operating discipline:

- Architecture before implementation.
- Current docs before code.
- Tests before risky changes.
- Security and tenant isolation by design.
- QA evidence before closeout.
- Read-only specialist agents before autonomous write agents.
- Eval-backed skills before expansion.

## Target maturity levels

| Level | Name | Outcome |
|---:|---|---|
| 0 | Repo seed | Research, findings, roadmap, and prompts exist. |
| 1 | Skill factory | Standards, templates, eval schema, and validators exist. |
| 2 | Foundation skills | Core engineering skills and core read-only agents exist. |
| 3 | Platform skills | SaaS, cloud, security, AI security, QA, audit, and troubleshooting waves exist. |
| 4 | Eval-backed library | Skills have realistic evals and trigger checks. |
| 5 | Product-agnostic operating system | 300-skill roadmap is implemented in validated batches. |

## Recommended phases

| Phase | Priority | Main outcome | Why it matters |
|---:|---|---|---|
| 0 | P0 | Skill and agent factory | Prevents low-quality bulk generation. |
| 1 | P0 | Core engineering discipline | Improves almost every future Claude engineering task. |
| 2 | P1 | SaaS and cloud architecture | Establishes tenancy, reliability, operations, and cost boundaries. |
| 3 | P1 | Security and AI security | Makes security and AI tool safety verifiable. |
| 4 | P1 | QA, E2E, manual QA, Playwright, Vite, Vitest | Produces release evidence and avoids brittle testing. |
| 5 | P1 | Audit and troubleshooting | Forces whole-repo inventory, evidence, and root-cause discipline. |
| 6 | P2 | 300-skill expansion | Scales the library after quality gates exist. |

## Phase 1 foundation skills

| Skill | Priority | Purpose |
|---|---|---|
| `domain-modeler` | P0 | Model business capabilities, ubiquitous language, bounded contexts, aggregates, and events before coding. |
| `architecture-designer` | P0 | Review or design module boundaries, dependency direction, data ownership, coupling, tradeoffs, and ADRs. |
| `grill-with-docs` | P0 | Force current docs, local version/config inspection, implementation notes, and verification. |
| `tdd-engineer` | P0 | Enforce red-green-refactor, regression tests, minimal implementation, and exact command reporting. |
| `systematic-debugger` | P0 | Reproduce, reduce, isolate, fix one thing, verify, and explain prevention. |
| `code-reviewer` | P0 | Review actual diffs for correctness, security, performance, reliability, maintainability, tests, and migrations. |
| `code-simplifier` | P1 | Reduce complexity while preserving behavior and public APIs unless explicitly approved. |
| `adr-writer` | P1 | Capture architecture decisions with context, alternatives, consequences, rollback, and review date. |

## Phase 1 core agents

| Agent | Priority | Tools posture | Purpose |
|---|---|---|---|
| `codebase-explorer` | P0 | Read-only | Inventory files, modules, entry points, dependencies, tests, docs, and risks. |
| `principal-architect-reviewer` | P0 | Read-only | Review architecture, coupling, module boundaries, data ownership, and migration risk. |
| `security-reviewer` | P0 | Read-only | Review trust boundaries, auth, authz, secrets, tenant isolation, and sensitive data exposure. |
| `qa-strategy-reviewer` | P1 | Read-only | Review test strategy, coverage gaps, evidence, flake risk, and release readiness. |
| `senior-debugger` | P1 | Read-only first | Analyze complex failures using reproduction, evidence, hypotheses, and verification. |

## Phase 2 SaaS and cloud skills

| Skill | Priority | Purpose |
|---|---|---|
| `saas-platform-architect` | P0 | Build platform blueprint covering tenants, identity, control/data plane, data isolation, billing, observability, SLOs, cost, and migration. |
| `tenant-modeler` | P0 | Define tenant hierarchy, membership, user mapping, context resolution, support access, jobs, logs, and lifecycle. |
| `multi-tenant-data-architect` | P0 | Compare shared DB, schema-per-tenant, DB-per-tenant, hybrid, RLS, backup, restore, deletion, performance, and leak tests. |
| `saas-entitlement-billing-architect` | P1 | Define plans, limits, metering, billing events, abuse controls, and cost alignment. |
| `slo-reliability-architect` | P1 | Define critical journeys, SLIs/SLOs, failure modes, RTO/RPO, degraded mode, and runbooks. |
| `observability-operator` | P1 | Define logs, metrics, traces, audit events, dashboards, alert rules, and incident workflow. |
| `saas-cost-architect` | P1 | Model cost per tenant, user, API call, AI request, file, job, and feature. |
| `api-event-architect` | P1 | Design APIs, events, idempotency, versioning, retry, and dead-letter behavior. |
| `cloud-architecture-decider` | P1 | Start cloud-neutral, then map to Azure or AWS based on requirements. |
| `azure-saas-architect` | P2 | Map logical SaaS architecture to Azure services with security, network, data, IaC, cost, and reliability tradeoffs. |
| `aws-saas-architect` | P2 | Map logical SaaS architecture to AWS services with IAM, data, network, observability, cost, and reliability tradeoffs. |
| `cloud-security-baseline-reviewer` | P1 | Review identity, network, secrets, data, logging, policy, posture, and incident gaps. |
| `iac-reviewer` | P1 | Review Terraform, Bicep, CDK, CloudFormation, and deployment drift/security/cost/reliability risk. |
| `resilience-architecture-reviewer` | P1 | Review availability, failover, DR, dependency failure, backups, chaos tests, and rollback. |

## Phase 3 security and AI security skills

| Skill | Priority | Purpose |
|---|---|---|
| `threat-modeler` | P0 | Produce assets, data flows, trust boundaries, threats, abuse cases, mitigations, residual risk, and owner. |
| `appsec-implementer` | P0 | Turn AppSec requirements into implementation plan, tests, controls, and verification. |
| `secure-sdlc-reviewer` | P1 | Review security requirements, implementation checks, vuln response, and evidence. |
| `multi-tenant-security-tester` | P0 | Build negative tests for tenant isolation across API, UI, DB, storage, logs, search, exports, and AI retrieval. |
| `secrets-identity-hardener` | P0 | Review secrets, keys, managed identities, tokens, CI/CD exposure, rotation, and least privilege. |
| `supply-chain-security-reviewer` | P1 | Review dependencies, SBOM, provenance, build integrity, artifacts, and vulnerability response. |
| `security-pr-reviewer` | P1 | Review PR diffs for exploit paths, severity, impacted assets, fix plan, and regression tests. |
| `ai-threat-modeler` | P0 | Map AI systems, prompts, RAG, tools, memory, data flows, trust boundaries, and AI-specific threats. |
| `prompt-injection-defender` | P0 | Design untrusted content handling, instruction hierarchy, tool gating, and prompt-injection evals. |
| `rag-security-architect` | P0 | Enforce retrieval-time authorization, document ACLs, redaction, citations, audit, and leak tests. |
| `agent-tool-safety-guard` | P0 | Define tool scopes, approval gates, idempotency, rate limits, budgets, and audit logs. |
| `ai-security-test-harness` | P1 | Create red-team and regression evals for AI safety, jailbreaks, data leakage, and tool abuse. |
| `ai-governance-risk-reviewer` | P1 | Review AI inventory, risk classification, lifecycle, owners, monitoring, and incident response. |
| `llm-output-safety-reviewer` | P1 | Review unsafe downstream output handling, validation, encoding, human review, and consumer controls. |

## Phase 4 QA and frontend validation skills

| Skill | Priority | Purpose |
|---|---|---|
| `qa-strategy-architect` | P0 | Design risk-based QA strategy, test levels, automation/manual split, environments, data, gates, and reporting. |
| `acceptance-criteria-tester` | P0 | Convert vague requirements into testable criteria with positive, negative, edge, permission, tenant, and failure cases. |
| `test-plan-designer` | P0 | Produce scope, cases, preconditions, data, environments, exploratory charters, and exit criteria. |
| `test-coverage-mapper` | P1 | Map requirements, journeys, APIs, modules, risks, and defects to tests and gaps. |
| `qa-automation-architect` | P1 | Design fixtures, data lifecycle, page object policy, API helpers, mocks, CI, reports, and flake policy. |
| `e2e-test-architect` | P0 | Select critical journeys for E2E and define tags, data, roles, tenants, CI placement, and artifacts. |
| `playwright-e2e-engineer` | P0 | Build resilient Playwright tests with role/label/test-id locators, web-first assertions, no hard waits, and traces. |
| `clickthrough-test-engineer` | P0 | Create route/navigation smoke tests with expected states, controls, console/network checks, and screenshots. |
| `manual-test-case-creator` | P0 | Create executable manual cases with steps, expected results, screenshots, pass/fail, cleanup, and defect instructions. |
| `screenshot-evidence-planner` | P1 | Define screenshot checkpoints, naming, metadata, masking, storage, and signoff expectations. |
| `vitest-unit-component-engineer` | P1 | Build Vite-native unit/component/browser/type/snapshot tests with intentional environment and useful coverage. |
| `vite-build-qa-engineer` | P1 | Audit Vite build, preview, env exposure, base path, chunk handling, cache behavior, plugins, and performance. |
| `flaky-test-detective` | P1 | Reproduce, classify, reduce, fix one flake source, and prove stability. |
| `regression-suite-curator` | P1 | Keep regression suites lean by value, risk, runtime, flake rate, and ownership. |
| `test-data-architect` | P1 | Design isolated, reproducible, tenant-scoped fixtures and cleanup. |
| `accessibility-test-engineer` | P1 | Add semantic roles, labels, keyboard, focus, alt text, and error announcement checks. |
| `performance-test-engineer` | P2 | Define workload, SLIs, thresholds, artifacts, and non-misleading performance tests. |
| `visual-regression-engineer` | P2 | Choose stable targets, masks, baseline policy, artifact storage, and review process. |

## Phase 5 audit and troubleshooting skills

| Skill | Priority | Purpose |
|---|---|---|
| `full-codebase-auditor` | P0 | Inventory the whole repo before findings; audit architecture, security, tests, dependencies, CI/CD, deployment, docs, and operations. |
| `code-audit-orchestrator` | P0 | Run structured audit scope, inventory, risks, findings, severity, evidence, remediation, and verification. |
| `static-analysis-reviewer` | P1 | Triage CodeQL/SAST/SARIF by exploitability, reachability, asset sensitivity, tenant impact, and business impact. |
| `dependency-license-audit-reviewer` | P1 | Inspect manifests/lockfiles for vulnerabilities, abandoned packages, duplicates, license risk, and safe upgrades. |
| `code-quality-auditor` | P1 | Review complexity, duplication, dead code, coupling, circular dependencies, unclear boundaries, and refactor safety. |
| `principal-code-analyst` | P0 | Connect code to domain boundaries, architecture, security, reliability, cost, performance, testability, and operations. |
| `senior-troubleshooter` | P0 | Debug with symptom, journey, env, changes, reproduction, evidence, hypotheses, one fix, verification, root cause, and prevention. |

## Long-term product-agnostic 300-skill target

Use this distribution only after phases 0-5 validate cleanly.

| Category | Target count | Notes |
|---|---:|---|
| Software architecture and engineering | 55 | Includes DDD, ADRs, boundaries, contracts, migrations, refactor safety, observability. |
| SaaS architecture | 35 | Includes tenants, control/data plane, billing, onboarding, support, exports, integrations, cost. |
| SaaS security and tenant isolation | 40 | Includes RLS, object authorization, storage, sensitive data, cross-tenant leak tests, audit. |
| Backend, API, and data engineering | 30 | Includes APIs, jobs, queues, idempotency, consistency, caching, database patterns. |
| Frontend, UX, and product engineering | 20 | Includes Vite, routing, accessibility, state, forms, UX states, performance. |
| QA, test automation, validation, and evidence | 55 | Includes test strategy, Playwright, Vitest, manual QA, evidence, flake, coverage, regression. |
| DevOps, reliability, and operations | 25 | Includes CI/CD, deploys, rollback, runbooks, SLOs, monitoring, incident response. |
| AI-era SDLC and agent governance | 20 | Includes agent startup, approvals, phase locks, traceability, closeout, work evidence. |
| AI software engineering and AI security | 20 | Includes AI router, prompt contracts, RAG, evals, redaction, autonomy, safety, cost. |
| Total | 300 | Generate as validated batches of 8-12, not a single dump. |

## Project-specific skills policy

Project-specific skills for WayPoint, Brigara OS, Carrot & Daikon Ordering, Memora, Evanna-AI, MentorME, or SaaS Founder Coaching should be created only after the reusable foundation exists.

When a skill depends on a private or product-specific repo, keep this public repo generic. Put private implementation references in the private project repo instead.