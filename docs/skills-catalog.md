# Project Aegis — Skills & Agents Catalog

Single source of truth for what skills and subagents exist, what is planned, and how the two
differ. The backlog below is derived from the **reconciled phase lists**
([`docs/reconciliation/step-0-reconciliation-v4.md`](reconciliation/step-0-reconciliation-v4.md) §3)
and the **category backlogs** under [`docs/skills/`](skills/). `scripts/validate-skills.py`
checks that every *implemented* skill is listed here and in `README.md`.

> **Status:** Phase 0 (foundation), Phase 1 (the 8-skill operating-discipline pack,
> decision D4), Phase 1.5 (the 4-skill AI-SDLC governance completion, roadmap
> #261/#268/#279/#280), Phase 2 (the 10-skill core architecture & engineering pack),
> Phase 3 (the 9-skill SaaS & tenant isolation pack), Phase 4 (the 9-skill
> security, RLS & supply-chain pack), Phase 5 (the 16-skill QA, E2E, manual QA
> & evidence pack — the 13 canonical skills plus 3 pulled forward from the QA
> backlog, roadmap #184/#185/#204), and Phase 6 (the 10-skill cloud, DevOps,
> reliability & release pack), Phase 7 (the 14-skill AI security &
> LLM systems pack — v4's 10 plus 4 OWASP LLM Top 10 gap additions, D6),
> Phase 7.5 (the 6-skill agentic AI security pack plus 3 extensions of
> existing skills — OWASP Agentic Top 10, D7), and the Compliance &
> Governance batch (the 9-skill ISO 27001 + ISO 42001 + SOC 2 pack with
> NIST AI RMF as companion — one shared control foundation, framework
> projections, and a crosswalk, D9) are implemented, plus the completed
> D13 library-meta scope (`skill-quality-reviewer`, D18; `library-diff-reviewer`,
> `eval-runner-designer`, `skill-usage-instrumenter`, and
> `skill-deprecation-planner`, D22), the
> D12.8 operational workflow patterns pack (10 evidence-extracted skills —
> the concrete rules of the Zero-Trust Engineering Discipline, D21), and the
> data/performance/QA-validation batch (D23: the 7-skill D12.1 data
> engineering pack, the 6-skill D12.3 performance engineering pack, and the
> 2 D10 Tier 1 performance/load validation skills — D12.3 designs FOR
> performance, D10 measures it), and the product/PM/growth batch (D24: the
> 5-skill D12.2 product-engineering craft pack, the 6-skill D12.5
> PM/product-engineering interface pack, and the 4-skill D12.6
> growth/analytics engineering pack — `product-spec-writer`≠`adr-writer`,
> `sunset-deprecation-communicator`≠`skill-deprecation-planner`, and the two
> three-way event/analytics seams pinned in trigger-evals), and the
> docs-engineering batch (D25, PART A of a two-PR set: the 8-skill D12.4
> technical writing / docs engineering pack — `adr-sequencer` extends
> `adr-writer`, `docs-retention-index`≠`skill-deprecation-planner` pinned
> both ways, `api-doc-generator-designer`≠`api-event-architect`), and the
> staff-IC / architecture / framework-refresh batch (D26, PART B of the
> same set: the 7-skill D12.7 staff+ IC craft pack, the 1-skill D12.9
> architecture-advisory pack, and the 3-skill D14 framework-refresh /
> source-currency pack — a detect→propose→human-review pipeline, none
> auto-updates; 148→159 skills), and the OWASP web-app gap-closure pair
> (D28: `security-logging-alerting-architect` closes A09:2025 Security
> Logging and Alerting Failures and `error-handling-security-reviewer`
> closes A10:2025 Mishandling of Exceptional Conditions — the D8 audit's
> two zero-coverage categories; all 10 OWASP web-app categories now have
> an owning skill; 159→161 skills).
> `_template` remains a reference template ignored by the validator.
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

## Implemented (Phases 0–5)

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

### Skills (Phase 1.5 — AI-SDLC governance completion)

Completes the category-08 governance layer Phase 1 started (roadmap
#261/#268/#279/#280). These four COMPOSE the Phase 1 skills — each stage or
control cites its enforcing skill by name, never restating its procedure. All
ship `evals/evals.json` **and** `evals/trigger-evals.json` (the four overlap
each other and the Phase 1 pack). Two edit behavior-steering artifacts and are
**manual-only** (`disable-model-invocation: true`): `agent-authorization-matrix`
(governance artifacts) and `agent-memory-governance` (memory files).

| Skill | Roadmap ref (cat 08) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `ai-sdlc-operating-model` | #261 | yes | End-to-end human+agent lifecycle contract: named stages with entry/exit gates, per-stage authority (human / agent / agent-with-approval), enforcing skill per stage, failure routing, learning loop; grounded in observed PR practice with a gap list. |
| `agent-authorization-matrix` | #268 | **no** (manual-only; edits governance artifacts) | Deny-by-default action × context matrix of standing agent authority — merge to protected branches requires a named human always, auto-merge arming forbidden to agents (armed state re-checked after every push), approval scope/expiry semantics; proposal-first. |
| `agent-memory-governance` | #279 | **no** (manual-only; edits memory files) | Memory WRITE/TRUST/HYGIENE rules: confirmed durable facts with provenance and absolute dates, never secrets; remembered repo/PR state verified against live git/gh before acting; per-entry disposition-approved cleanups. |
| `agent-governance-audit` | #280 | yes | Per-control PASS/FAIL/UNVERIFIABLE compliance audit of one AI-assisted change from primary evidence (PR timeline incl. who armed auto-merge, commits, CI runs); closeout claims cross-checked, never trusted; missing evidence is never a PASS. |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for all four: the
governance cluster discriminates internally (umbrella vs matrix vs memory vs
audit) and against the Phase 1 pack (`human-approval-boundary`,
`source-of-truth-reconciler`, `agent-startup-context-gate`,
`agent-instruction-consolidator`, `ai-closeout-reporter`,
`change-classification-gate`), Phase 2's `code-reviewer` and
`full-codebase-auditor`, and Phase 3's `authorization-matrix-designer`
(agent authority vs end-user RBAC).

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

### Skills (Phase 3 — SaaS & tenant isolation pack)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json` **and**
`evals/trigger-evals.json` (all nine sit in one of three overlap clusters). None has
side effects, so all are model-invocable. Per master-prompt §5: tenant isolation is
treated as cross-cutting (identity, data, API, storage, logs, analytics, support,
exports, imports, jobs, search, AI retrieval, billing, flags, audit), every skill
carries migration + rollback considerations, and the security-related skills require
negative tests.

| Skill | Source (category doc) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `saas-platform-architect` | cat 02 (platform; #79/#84) | yes | Per-component pooled/siloed/bridge decisions with named isolation mechanisms; control-plane/data-plane split; capability inventory; rollout with per-step rollback. |
| `tenant-modeler` | cat 02 #56 | yes | Tenant semantics: definition + hierarchy, membership-as-entity (roles on membership), invitations, ownership, lifecycle state machine with per-state access/data/billing/jobs posture. |
| `tenant-isolation-reviewer` | cat 03 (isolation review) | yes | Reviews REAL systems for cross-tenant leakage across all 15 surfaces; evidence-cited findings, isolation test matrix, negative tests, honest not-inspected list. |
| `multi-tenant-data-architect` | cat 02 #74/#77/#78 + cat 04 | yes | Per-store scoping decisions (incl. caches/search/vector stores), server-derived tenant-context propagation contract, ownership map, expand→contract migration with verification + rollback. |
| `authorization-matrix-designer` | cat 02 #59 | yes | Deny-by-default roles × permissions × resources matrix, object-level rules (anti-IDOR), enforcement-point map, brokered support access, negative-test plan, additive role migration. |
| `plan-entitlement-architect` | cat 02 #60/#64 | yes | Plan × entitlement matrix with one resolution point, uniform enforcement everywhere, metering hooks, plan-transition table (no silent data loss on downgrade), grandfathering + rollback. |
| `audit-log-architect` | cat 02 #70 | yes | Audit event taxonomy + versioned record schema, append-only integrity, explicit write-failure policy per category, retention/redaction, tenant-scoped access, negative tests. |
| `saas-cost-architect` | cat 02 #89 | yes | Bill-grounded cost drivers, attribution-or-admission per driver, distribution-based unit economics vs revenue, exposure math, guardrails with observe-first rollout + rollback. |
| `api-event-architect` | cat 04 (API/event contracts) | yes | Credential-derived tenant context, idempotency, per-tenant/plan rate limits, versioning + deprecation with dual-run, tenant-scoped signed webhooks, contract migration + rollback. |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for the three Phase 3 clusters:
tenant (`tenant-modeler`, `tenant-isolation-reviewer`, `multi-tenant-data-architect`),
platform/commercial (`saas-platform-architect`, `plan-entitlement-architect`,
`saas-cost-architect`), and access & events (`authorization-matrix-designer`,
`audit-log-architect`, `api-event-architect`) — plus cross-cluster discrimination for
the authorization-vs-entitlement axis ("can this ROLE do X" vs "does this PLAN include X").

### Skills (Phase 4 — security, RLS & supply-chain pack)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json` **and**
`evals/trigger-evals.json` (all nine sit in one of two overlap clusters). Per
master-prompt §6: ASVS-style verification, SSDF-style secure-SDLC, and SLSA-style
supply-chain thinking; scanner output is treated as input, not truth; high-severity
claims require an exploit path or abuse scenario; tenant isolation and object-level
authorization are mandatory on SaaS paths; every skill produces concrete artifacts and
negative tests; no finding is suppressed without written rationale. Two skills have
side effects and are **manual-only** (`disable-model-invocation: true`):
`appsec-implementer` and `secrets-identity-hardener` edit code/config.

Per reconciliation §3, the execution-plan `rls-policy-author` and
`rls-negative-test-designer` are **merged into `rls-policy-auditor`** (no separate
skills): it audits SELECT/INSERT/UPDATE/DELETE policies, hunts recursion / unsafe
SECURITY DEFINER / broad grants / missing tenant scope / service-role leakage /
frontend-derived scope, authors corrected policies on request, and always ships a
per-command negative-test plan.

| Skill | Source (category doc) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `threat-modeler` | cat 03 #91/#92 | yes | Design-time threat model: assets/actors/trust-boundaries, STRIDE per boundary, abuse cases, exploit-path-gated severity, mitigations mapped to negative tests; consumes tenant/authz outputs. |
| `appsec-implementer` | cat 03 (control implementation) | **no** (manual-only; edits code/config) | Builds one NAMED control test-first — negative test red→green, minimal server-side control, scoped diff, residual risk stated. |
| `multi-tenant-security-tester` | cat 03 #93/#95 + cat 06 | yes | Executable cross-tenant/authorization negative suite: two-tenant fixtures, forbidden-action-denied assertions, positive controls, IDOR/list/mass-assignment/exports/jobs, honest coverage. |
| `rls-policy-auditor` | cat 03 #94/#95/#96/#97/#98/#99/#100/#102 (merged author + negative-test designer) | yes | Per-command RLS audit/authoring: recursion, unsafe SECURITY DEFINER, broad grants, missing tenant scope, service-role leakage, frontend-derived scope; mandatory negative-test plan; delivers policies as a migration, never runs live DDL. |
| `secrets-identity-hardener` | cat 03 #103/#104/#123/#109 | **no** (manual-only; edits code/config) | Env classification (catches VITE_/NEXT_PUBLIC_ leaks), moves secrets server-side with a client-bundle-absence proof, rotates leaked creds, least-privilege service accounts, session/token flags. |
| `supply-chain-security-reviewer` | cat 03 #121/#122 | yes | SLSA-style: lockfile-based dependency set, reachability triage of scanner output, install/build-script and CI compromise paths, SHA pinning, compromise-path-gated severity. |
| `security-pr-reviewer` | cat 03 #114/#111/#112/#113 + cat 08 #277 | yes | Security lens on an ACTUAL diff: authz/object-level/tenant-scope, injection, secrets, SSRF, control-weakening detection; exploit-path-gated findings; no diff, no review. |
| `secure-migration-reviewer` | cat 03 #126 | yes | Whole-migration deploy safety: RLS/policy gaps, GRANT widening, unsafe defaults, destructive/irreversible ops, tenant-scoped backfills, lock risk, expand→contract deploy order, rollback; delegates policy text to `rls-policy-auditor`. |
| `static-analysis-reviewer` | cat 03 #121 adjacent + cat 06/08 | yes | Triages SAST/CodeQL/SARIF on first-party code: dedup, confirm-against-code disposition (TP/FP/dup/accepted), five-axis ranking (reachability/exploitability/asset/tenant/business), written suppression policy. |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for the two Phase 4 clusters:
the **threat & hardening** cluster (`threat-modeler`, `appsec-implementer`,
`secrets-identity-hardener`) and the **security-review** cluster
(`supply-chain-security-reviewer`, `security-pr-reviewer`, `secure-migration-reviewer`,
`static-analysis-reviewer`) — the latter with explicit discrimination against the
shipped `code-reviewer` (general review vs security-specialized). The **tenant-security**
cluster (`multi-tenant-security-tester`, `rls-policy-auditor`) additionally discriminates
against the shipped `tenant-isolation-reviewer` (inspection-based review vs executable
tests vs database-policy audit).

### Skills (Phase 5 — QA, E2E, manual QA & evidence pack)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json` **and**
`evals/trigger-evals.json` (all sixteen sit in one of four overlap clusters). Per
master-prompt §7: QA starts from risk; every layer choice picks the cheapest reliable
layer; E2E is reserved for critical journeys; manual cases are executable by another
tester; screenshot evidence carries naming/masking/metadata/storage rules; Playwright
uses resilient locators and web-first assertions with no arbitrary sleeps; Vite skills
prove `VITE_` secret non-exposure at the `dist/` level; Vitest skills choose the
environment intentionally; flake work classifies, reproduces, fixes one cause, and
proves stability. Four skills have side effects and are **manual-only**
(`disable-model-invocation: true`): `playwright-e2e-engineer` (writes specs, drives a
browser), `clickthrough-test-engineer` (drives a live app), `vitest-unit-component-engineer`
(writes test files, runs suites), and `vite-build-qa-engineer` (runs builds/preview).

**Pulled forward from the QA backlog** (in addition to the 13 canonical Phase 5 skills):
`integration-test-designer` (roadmap #184), `api-contract-test-designer` (roadmap #185),
and `accessibility-test-harness` (roadmap #204) — each with mandatory trigger-eval
discrimination against its nearest neighbors. Per reconciliation §3, `acceptance-criteria-tester`,
`e2e-test-architect`, and `qa-closeout-reporter` stay in the expansion backlog
(`qa-closeout-reporter` overlaps the shipped `ai-closeout-reporter` +
`screenshot-evidence-planner`, whose evidence bundle the closeout consumes).

| Skill | Source (category doc) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `qa-strategy-architect` | cat 06 #181/#182 | yes | Product-level QA strategy: ranked risk inventory → cheapest-reliable-layer decisions, explicit automation/manual split, evidence per change class, CI gates, ownership; delegates security negatives. |
| `test-plan-designer` | cat 06 #181/#192 | yes | Per-change test plan: risk-traced items with layer/data/environment, objective entry/exit criteria, named artifacts + CI placement, engineer-skill handoffs, explicit out-of-scope list. |
| `test-coverage-mapper` | cat 06 #191/#192 | yes | Surface-inventory-first coverage audit; maps by reading assertions (theater ≠ coverage); risk-ranked gap list with cheapest fill layer; honest covered/theater/uncovered/not-inspected statement. |
| `qa-automation-architect` | cat 06 #200/#211/#212 | yes | Automation blueprint: tools per layer with rationale, structure/fixtures/auth-state, parallel-safe isolation, artifacts, CI tiers with bounded logged retries, flake policy, small-step migration. |
| `playwright-e2e-engineer` | cat 06 #187/#189 | **no** (manual-only; writes specs, drives browser) | Critical-journey Playwright specs: role/label locators (testid = flagged semantics gap), web-first assertions, zero sleeps/networkidle, storageState per persona, failure traces, honest run reports incl. pass-on-retry. |
| `clickthrough-test-engineer` | cat 06 #222 | **no** (manual-only; drives a live app) | Pre-planned route-by-route interactive walkthrough (forms w/ invalid input, dialogs, permissions, states, console), severity-rated defects with masked evidence, honest executed/skipped coverage. |
| `manual-test-case-creator` | cat 06 #221 | yes | Stranger-executable manual cases: exact data/roles/environment, one observable expected result per step, screenshot checkpoints, pass/fail/blocked verdict rules, cleanup, requirement traces. |
| `screenshot-evidence-planner` | cat 06 #223 | yes | Evidence policy: risk-justified checkpoints, deterministic naming, mandatory pre-storage block-out masking, metadata (build/env/persona/viewport), storage/retention classes, case/PR/closeout linkage. |
| `vitest-unit-component-engineer` | cat 06 #183 + cat 05 #180 | **no** (manual-only; writes test files, runs suites) | Vitest unit/component tests: intentional node-vs-DOM environment per file, owned-seam mocks only, Testing Library user-facing queries, determinism, real run output, regression spot-check. |
| `vite-build-qa-engineer` | cat 05 #178 + cat 06 #217 | **no** (manual-only; runs builds/preview) | Build-artifact QA: `VITE_` env classification, dist-level secret value+pattern proof, build/preview parity (base, deep links, modes), bundle budgets + sourcemap policy; exposures → `secrets-identity-hardener`. |
| `flaky-test-detective` | cat 06 #209/#210 | yes | Classify → reproduce with counts → fix ONE cause → prove stability with repeated runs; no retries/sleeps/weakened assertions; product races routed as product bugs; quarantine with owner/ticket/expiry. |
| `test-data-architect` | cat 06 #196–#199 | yes | Persona/baseline catalog (read-only), per-layer data sources, determinism, worker-scoped parallel isolation, synthetic-only PII posture, structural cleanup + traceability, schema-coupled seed evolution. |
| `regression-suite-curator` | cat 06 #190/#210 | yes | Evidence-based promote/retain/demote/retire with written rationale (never silent deletion), protected security regressions (human-approval to retire), enforced quarantine registry, tier-budget fit. |
| `integration-test-designer` | cat 06 **#184 (pulled forward)** | yes | The layer BETWEEN unit and E2E: real service/command/DB/auth/permission boundaries, named faked seams with rationale, real-path auth minting, persisted-state assertions, no browser; security matrices deferred to `multi-tenant-security-tester`. |
| `api-contract-test-designer` | cat 06 **#185 (pulled forward)** | yes | Contract VERIFICATION (not design): provider/consumer roles, request/response schema + error-envelope validation, additive-vs-breaking CI gate, version coverage, fake-fidelity re-validation; contract design stays with `api-event-architect`. |
| `accessibility-test-harness` | cat 06 **#204 (pulled forward)** + cat 05 #173 | yes | WCAG-pinned a11y harness: automated scans (component/E2E/CI, baseline+ratchet) AND manual keyboard/focus/contrast/screen-reader checklists; explicit about what automation cannot judge. |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for the four Phase 5 clusters:
**strategy/plan/coverage** (`qa-strategy-architect`, `test-plan-designer`,
`test-coverage-mapper`, `qa-automation-architect`), **test-level**
(`vitest-unit-component-engineer`, `integration-test-designer`, `playwright-e2e-engineer`,
`api-contract-test-designer`), **UI/manual** (`clickthrough-test-engineer`,
`manual-test-case-creator`, `screenshot-evidence-planner`, `accessibility-test-harness`),
and **unit/build/flake/data** (`vite-build-qa-engineer`, `flaky-test-detective`,
`test-data-architect`, `regression-suite-curator`) — with cross-phase discrimination
against the shipped `code-reviewer`, `full-codebase-auditor`, `api-event-architect`,
`multi-tenant-security-tester`, `tdd-engineer`, `systematic-debugger`,
`secrets-identity-hardener`, and `ai-closeout-reporter`.

### Skills (Phase 6 — cloud, DevOps, reliability & release pack)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json` **and**
`evals/trigger-evals.json` (all ten sit in one of three overlap clusters). Per
master-prompt §8: cloud work starts cloud-neutral (requirements, constraints,
compliance, latency, regions, availability, cost, operability, risk BEFORE
service mapping); provider skills stay provider-idiomatic without inventing
product specifics (SKU/quota/price claims become verification items); release
skills demand evidence (CI checks on the release commit, artifacts, rollback
path), not vibes; runbooks meet the stranger-executability bar
(`manual-test-case-creator` discipline); SLOs derive from user journeys with
error budgets, and paging fires on symptoms, not causes. Two skills have side
effects and are **manual-only** (`disable-model-invocation: true`):
`ci-pipeline-architect` (edits pipeline definitions — behavior-steering,
secret-adjacent files that execute on push) and `observability-operator`
(edits live alert/dashboard config, executes operational queries).

Per reconciliation §3, the execution-plan `rollback-strategy-designer` is
**merged into `rollback-runbook-author`** (strategy + runbook are one
artifact); the remaining Phase 6 expansion backlog stays unbuilt (see below).

| Skill | Source (category doc) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `cloud-architecture-decider` | master §8 (cloud) | yes | Cloud-neutral decision: nine-axis requirements record (verified/assumed per entry), provider-neutral logical architecture, isolation/compliance hard filters BEFORE scoring, managed-vs-self-hosted per capability with the operational bill, exit costs + reopen triggers; ADR handoff. |
| `azure-saas-architect` | master §8 (cloud) | yes | Decided-Azure mapping: Entra ID + managed identities + OIDC federation, VNets/Private Link, per-store tenant-isolation mechanism (elastic pools, Cosmos partition keys, Blob prefixes), compute by team maturity, Azure Policy/Defender posture, Bicep/Terraform, tag-keyed cost controls; SKU/limit/price claims → verification items. |
| `aws-saas-architect` | master §8 (cloud) | yes | Decided-AWS mapping: Organizations/OU + SCPs, IAM roles + OIDC federation, VPC/PrivateLink, per-store tenant-isolation mechanism (Aurora silos, DynamoDB leading keys, S3 prefixes), compute by team maturity, Security Hub/GuardDuty posture, Terraform/CDK, activated cost-allocation tags; quota/type/price claims → verification items. |
| `iac-reviewer` | cat 07 #245 (+#257/#258 adjacent) | yes | Review-only IaC audit, blast radius FIRST (replace/delete of stateful resources), public exposure, IAM width deltas, secrets in code AND state, tenant-isolation impact, drift, pinning, cost flags; apply-safety verdict; never applies, never runs plan against live backends. |
| `ci-pipeline-architect` | cat 07 #238 (+#237/#239/#240) | **no** (manual-only; edits pipeline definitions) | Stage graph with blocking semantics + latency budget, CI secret governance (OIDC over stored keys, fork-PR posture, job→secret map), cache/artifact governance with provenance, environment promotion with named-human gates, branch-protection alignment; composes qa-automation-architect tiers, vite-build-qa-engineer, supply-chain pinning rules. |
| `release-readiness-reviewer` | cat 07 #241 (+#242) | yes | Evidence-based ship/no-ship gate: every dimension cites a verifiable artifact or is MISSING (CI on the release SHA, artifact provenance, test-signal fit, migration review, rollback path + rehearsal, flags, docs, observability, approvals); unknown = No-Go with the evidence that flips it; the same-named SUBAGENT composes this skill. |
| `rollback-runbook-author` | cat 07 #243 (+#242; absorbs rollback-strategy-designer) | yes | Rollback strategy + stranger-executable runbook in one artifact: roll-back-vs-fix-forward criteria with time-box, per-layer primitives in stated order, previous-good artifact by id, bad-window data repair, freeze step, rehearsal log + staleness triggers; authors only, never executes. |
| `observability-operator` | cat 07 #246/#247/#248/#252 | **no** (manual-only; edits live alert/dashboard config, runs operational queries) | Hands-on instrumentation (structured, correlated, redacted-at-emission), truthful health checks with timeouts, alerts with severity/owner/runbook-link/justified-threshold, query-verified claims, silences only with owner+expiry; implements slo-reliability-architect's design. |
| `slo-reliability-architect` | cat 07 #251 (+#247 design side) | yes | Journey-derived SLOs: symptom-based SLIs with measurement points + blind spots, targets with error budgets in user units, burn-rate paging with cause-alert demotions, failure-mode analysis, budget policy with consequences + decider, per-tenant/noisy-neighbor views. |
| `incident-response-runbook` | cat 07 #249 (+#250) | yes | One-minute severity ladder (ambiguity classifies up), IC/comms/ops roles with small-org collapse rule, triage to decision points, containment by REFERENCE to the rollback artifact, tenant-aware comms with legal gate on exposure, during-incident evidence capture, blameless postmortem where every finding lands (regression-suite-curator, observability-operator, runbook fix, architecture, or owned accepted risk). |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for the three Phase 6
clusters: **cloud-architecture** (`cloud-architecture-decider`,
`azure-saas-architect`, `aws-saas-architect`, `iac-reviewer`), **delivery**
(`ci-pipeline-architect`, `release-readiness-reviewer`, `rollback-runbook-author`),
and **reliability** (`observability-operator`, `slo-reliability-architect`,
`incident-response-runbook`) — with cross-phase discrimination against the shipped
`architecture-designer`, `saas-platform-architect`, `secure-migration-reviewer`,
`supply-chain-security-reviewer`, `security-pr-reviewer`, `qa-automation-architect`,
`vite-build-qa-engineer`, `code-reviewer`, `audit-log-architect`,
`systematic-debugger`, `regression-suite-curator`, `qa-strategy-architect`,
`saas-cost-architect`, and the `release-readiness-reviewer` **subagent**
(delegated review lens vs this skill's procedure — the `full-codebase-auditor`
namespace pattern).

### Skills (Phase 7 — AI security & LLM systems pack)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json` **and**
`evals/trigger-evals.json` (all fourteen sit in one of four overlap clusters).
Anchored to the **OWASP Top 10 for LLM Applications (2025)** per reconciliation
§3 (D6): v4's 10 skills plus 4 gap additions (`sensitive-disclosure-guard`
LLM02, `model-poisoning-reviewer` LLM04, `system-prompt-leakage-reviewer`
LLM07, `ai-misinformation-guard` LLM09). Per master-prompt §9: user input,
retrieved documents, webpages, tickets, emails, logs, tool outputs, and model
outputs are untrusted unless proven otherwise; untrusted content never modifies
system instructions, tool permissions, identity, access policy, or the
execution plan; RAG authz is enforced at retrieval time; tool access is
least-privilege with side effects approval-gated; AI outputs are
schema-validated before use; red-team/eval cases, telemetry/cost controls,
kill switch/fallback, and incident hooks are present where relevant. These skills
**compose** the shipped tenant/security/cost/governance/reliability packs rather
than re-deriving them. Three skills have side effects and are **manual-only**
(`disable-model-invocation: true`): `prompt-injection-defender` (edits
prompts/guardrail code), `ai-evaluation-harness` (runs evals that spend
tokens/money), and `ai-router-architect` (wires live providers/credentials).
The other eleven — including `structured-output-validator`, a design/spec skill
that produces a contract and hands wiring off — stay model-invocable.

Per reconciliation §3, **LLM03 (Supply Chain) is extend-existing**: the shipped
Phase 4 `supply-chain-security-reviewer` was extended (scoped diff) to cover the
AI/ML supply chain — third-party models, datasets, and fine-tuning adapters
(provenance, revision pinning, unsafe pickle/`torch.load` serialization vs
safetensors), with an explicit acquire-vs-ingest boundary handing curated-data
and pipeline integrity to `model-poisoning-reviewer`. **LLM10 (Unbounded
Consumption)** DoS/denial-of-wallet coverage is baked INTO
`ai-cost-guardrail-designer`, not a separate skill. `ai-evaluation-harness`
absorbs the AI security test harness (no separate `ai-security-test-harness`).

| Skill | OWASP LLM Top 10 | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `ai-threat-modeler` | cross-cutting | yes | AI-specific threat model: AI assets + trust boundaries (all untrusted content), per-boundary threats anchored to LLM Top 10, abuse cases, exploit-path-gated severity, each mitigation mapped to an owning skill + red-team case; composes threat-modeler for the classic surface. |
| `prompt-injection-defender` | LLM01 | **no** (manual-only; edits prompts/guardrail code) | Layered injection defense: trust zones, the untrusted-content invariant, content/instruction separation, and — the primary layer — deterministic action authorization OUTSIDE the model; direct + indirect payloads; red-team suite with SAFE-outcome assertions. |
| `rag-security-architect` | LLM08 | yes | RAG/vector-store security: authorization AT RETRIEVAL TIME (never post-filter), per-tenant index scoping, document-ACL propagation, embedding risks (inversion/membership/poisoning/stale-permission); composes tenant-isolation-reviewer + multi-tenant-data-architect. |
| `agent-tool-safety-guard` | LLM06 | yes | Least-privilege tool access: per-tool blast-radius matrix, calling-user authority (no service-account confused deputy), argument validation before execution, approval gates on irreversible actions, tool-chain composition abuse; composes human-approval-boundary + agent-authorization-matrix. |
| `llm-output-safety-reviewer` | LLM05 | yes | Output-handling review: model output as untrusted data to render/execute/URL/tool/store sinks (XSS/RCE/SSRF/injection/second-order), context-correct encoding, generated-code sandboxing; exploit-flow-gated findings. |
| `ai-evaluation-harness` | cross-cutting | **no** (manual-only; runs evals that spend tokens/money) | Versioned eval dataset (representative + adversarial/red-team + regression), per-dimension graders + thresholds (quality/schema/safety/grounding/injection/latency/cost), CI regression gate; absorbs the AI security test harness; honest real-run reporting (D3). |
| `ai-cost-guardrail-designer` | LLM10 (DoS/denial-of-wallet) | yes | Consumption guardrails: per-request token caps, tenant-scoped budgets/rate limits, agent loop/recursion bounds, fail-safe degraded mode + kill switch, burn-rate alerts before exhaustion; composes saas-cost-architect + observability-operator. |
| `ai-governance-risk-reviewer` | cross-cutting | yes | AI governance/risk posture: impact-based risk tiering, oversight-to-tier matching, accountable ownership, AI disclosure/consent, model/feature card, obligation→control mapping (EU AI Act tiers, NIST AI RMF) without asserting legal conclusions; composes ai-sdlc-operating-model + agent-governance-audit. |
| `ai-router-architect` | cross-cutting | **no** (manual-only; wires live providers/credentials) | Centralized model-routing layer: one interface, server-side-only credentials, task/cost routing, choke-point cost enforcement, per-call telemetry, resilient fallback + circuit breaker + no-deploy kill switch, idempotent retries; composes secrets-identity-hardener + observability-operator. |
| `structured-output-validator` | LLM05 companion | yes | Output-shape contract: schema (fields/types/enums/ranges), validate-before-use, semantic checks beyond shape (tenant-scoped ids), bounded failure handling; shape-is-not-safety handoffs to llm-output-safety-reviewer + agent-tool-safety-guard. |
| `sensitive-disclosure-guard` | LLM02 *(NEW)* | yes | Disclosure defense: data-minimization + pre-model redaction of secrets/PII/other-tenant data, output-path echo/bleed checks, log redaction at emission, provider retention/training posture; composes tenant-isolation-reviewer + secrets-identity-hardener. |
| `model-poisoning-reviewer` | LLM04 *(NEW)* | yes | Training/feedback/ingestion integrity: contributor-trust assessment, poisoning paths, feedback-loop Sybil defense, ingestion-as-truth integrity, provenance/holdout controls; acquire-vs-ingest boundary with supply-chain-security-reviewer. |
| `system-prompt-leakage-reviewer` | LLM07 *(NEW)* | yes | Two axes: no secrets in the prompt (extract + rotate via secrets-identity-hardener) AND no security dependence on prompt secrecy — **system prompts are NOT security controls**; enforcement is deterministic and lives OUTSIDE the LLM; extraction-is-harmless framing. |
| `ai-misinformation-guard` | LLM09 *(NEW)* | yes | Anti-misinformation: grounding in retrieved sources (not memory), citation-to-claim verification, calibrated uncertainty/refusal, fact validation before action, package/API hallucination (slopsquatting) checks, overreliance-aware UX; composes rag-security-architect + ai-governance-risk-reviewer. |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for the four Phase 7
clusters: **threat & injection** (`ai-threat-modeler`, `prompt-injection-defender`,
`system-prompt-leakage-reviewer`, `sensitive-disclosure-guard`), **data &
retrieval** (`rag-security-architect`, `model-poisoning-reviewer`), **output &
agency** (`agent-tool-safety-guard`, `llm-output-safety-reviewer`,
`structured-output-validator`, `ai-misinformation-guard`), and **AI platform
ops** (`ai-evaluation-harness`, `ai-cost-guardrail-designer`,
`ai-governance-risk-reviewer`, `ai-router-architect`) — with cross-phase
discrimination against the shipped `threat-modeler`, `security-pr-reviewer`,
`supply-chain-security-reviewer`, `multi-tenant-security-tester`,
`multi-tenant-data-architect`, `tenant-isolation-reviewer`, `secrets-identity-hardener`,
`saas-cost-architect`, `plan-entitlement-architect`, `observability-operator`,
`agent-authorization-matrix`, `human-approval-boundary`, `agent-governance-audit`,
`ai-sdlc-operating-model`, `regression-suite-curator`, `qa-automation-architect`,
`api-contract-test-designer`, and the `ai-security-red-team-reviewer` **subagent**
(which composes these skills — design/predict here vs hands-on adversarial probing there).

### Skills (Phase 7.5 — agentic AI security pack)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json` **and**
`evals/trigger-evals.json` (the agentic cluster overlaps internally and with
Phase 7). Anchored to the **OWASP Top 10 for Agentic Applications (2026)**,
ASI01–ASI10, per reconciliation §3 (D7): **6 new skills + 3 extensions of
existing skills**. The Agentic Top 10 **extends, not replaces, the LLM Top 10
(D6)** — agent systems inherit every Phase 7 LLM-side risk; this pack adds
the autonomy, tool, identity, memory, and multi-agent risks on top. Per D7,
**ASI08 and ASI10 merge into ONE `agent-containment-reviewer`** (fault
propagation and the containment-gap-once-drift-begins are two halves of the
same review — same inputs: agent topology, autonomy boundaries, kill/rollback
paths; it also covers the agentic slice of the backlog candidate
`ai-feature-kill-switch-designer`). Nothing else collapses: ASI01 vs ASI06 vs
ASI10 stay distinct (direct goal alteration vs stored-memory corruption vs
autonomous drift). One skill has side effects and is **manual-only**
(`disable-model-invocation: true`): `agent-goal-hijack-defender` (edits agent
loop/planner code and prompts). The other five are pure review/design skills
and stay model-invocable.

**Extensions (scoped additive diffs, not new skills):** ASI02 + the tool-side
slice of ASI05 extend Phase 7 `agent-tool-safety-guard` (tool misuse through
legitimate grants, side-effect limits, NL-driven execution paths,
code-execution tools as a maximal-blast-radius class); ASI05 extends Phase 7
`llm-output-safety-reviewer` (autonomous generate-and-run loops, per-run
ephemeral sandboxes, sandbox escape/persistence, NL-to-execution path maps);
ASI04 extends Phase 4 `supply-chain-security-reviewer` AGAIN (after D6/LLM03)
to the agentic supply chain (MCP servers and manifests, tool/skill
registries, plugin packages, A2A dependencies — install-vs-runtime seam with
`inter-agent-comms-reviewer`).

| Skill | OWASP Agentic Top 10 | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `agent-goal-hijack-defender` | ASI01 | **no** (manual-only; edits agent loop/planner code + prompts) | Goal/plan integrity across multi-step runs: pinned goal record outside the model context, principal-only mutation channel, per-step tracing with deviation signals, drift response, per-channel hijack red-team suite; builds on `prompt-injection-defender` (LLM01 owns the vector). |
| `agent-identity-privilege-reviewer` | ASI03 | yes | Agent identity architecture: distinct least-privilege identity per agent, task/time-scoped credentials, delegation chains that attenuate (never amplify), confused-deputy closure, dual attribution (principal + agent); complements `secrets-identity-hardener` (custody fixer). |
| `memory-context-poisoning-reviewer` | ASI06 | yes | Persistent memory/stored-context poisoning: write-path trust classes, validation-before-write, per-entry provenance, tenant/user/session scoping at write AND recall, TTL + purge with derived-state rollback, recalled memory as data never instructions; distinct from `model-poisoning-reviewer` (LLM04) and `rag-security-architect` (LLM08). |
| `inter-agent-comms-reviewer` | ASI07 | yes | A2A/MCP message security: per-edge mutual authn, end-to-end integrity, replay bounds, confidentiality, topology allowlists, spoofed-result handling; enforces authenticated ≠ trusted — peer messages never re-task, change permissions, or assert approvals. |
| `agent-containment-reviewer` | ASI08 + ASI10 (merged) | yes | One containment review: cascade half (blast-radius isolation, bounded upstream trust, circuit breakers, checkpoints/rollback, retry-storm/fan-out limits) + rogue half (drift baselines, agent inventory/lifecycle, kill switches that SEVER AUTHORITY — credentials revoked, not processes killed); composes `ai-cost-guardrail-designer` + `incident-response-runbook`. |
| `human-agent-trust-reviewer` | ASI09 | yes | Adversarial review of the approval layer: consent fatigue (rate/latency signals), self-reported summaries vs system-verified facts, bundling/salami-slicing, urgency manipulation, automation-bias controls; counterpart to `human-approval-boundary` (that skill places the gates; this attacks their resilience). |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for all six as one
**agentic cluster**: internal discrimination (goal hijack vs memory poisoning
vs drift/containment vs identity vs comms vs approval-trust) plus cross-phase
discrimination against the shipped `prompt-injection-defender` (LLM01 vs
ASI01), `model-poisoning-reviewer` (LLM04 vs ASI06), `rag-security-architect`
(LLM08 vs ASI06), `agent-tool-safety-guard`, `llm-output-safety-reviewer`,
`agent-authorization-matrix`, `human-approval-boundary`,
`secrets-identity-hardener`, `agent-memory-governance`,
`authorization-matrix-designer`, `api-event-architect`,
`ai-cost-guardrail-designer`, `incident-response-runbook`,
`observability-operator`, `agent-governance-audit`, `ai-misinformation-guard`,
`ai-governance-risk-reviewer`, and the `ai-security-red-team-reviewer`
**subagent**.

### Skills (Compliance & Governance batch — D9)

All under `.claude/skills/<name>/`; every one ships `evals/evals.json`
**and** `evals/trigger-evals.json` (all nine form one compliance cluster).
Anchored to reconciliation §3's "Compliance & Governance batch" subsection
and D9, **including every per-source verification flag**: SOC 2 is an AICPA
**attestation** (a CPA's examination), never a certification — 27001/42001
are the certifiable management-system standards; 27001 Annex A counts
(93 = 37/8/14/34) are secondary-sourced and 42001 Annex A counts conflict
across sources (deliberately unstated); the SOC 2 Type 1/Type 2 definitions
and Security-as-required-baseline are CPA-firm-sourced; the ~60–80%
cross-framework overlap is an industry estimate; the vendor-market
rationale is positioning, not a standards claim — every skill carries these
in a **Compliance Precision Rules** section as
verify-against-the-standard-before-citing items. Architecture per D9:
**ONE shared control foundation + framework projections + a crosswalk**,
NOT three parallel skill sets. The batch **MAPS controls that largely
already exist** (Phase 3/4 technical controls, the Phase 5 evidence pack,
Phase 1.5 + Phase 7 AI governance) and produces auditor-grade evidence on
top — net-new is mostly ISO management-system artifacts (SoA, internal
audit, management review) and evidence plumbing. Invocability was evaluated
explicitly: all nine are mapping/documentation/design skills producing
proposal artifacts — none edits live governance artifacts or evidence
stores (store mutation and controlled-document rewrites are excluded via
Stop Conditions), so **all nine are model-invocable**.

| Skill | Layer (D9) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `compliance-control-foundation` | Shared foundation | yes | One framework-agnostic catalog (7 domains + AI governance): each control ONCE with objective/owner/mechanism/evidence hook, mapped by name to shipped Phase 3/4 artifacts; framework-neutral text; honest implemented/partial/missing status incl. the D8 residues. |
| `compliance-evidence-collector` | Shared foundation | yes | Evidence OVER TIME (SOC 2 Type 2's core demand, reused for ISO surveillance): per-control type, cadence matched to operating frequency, population for sampling, collector, retention, integrity; window-coverage matrix with recover-or-except holes; reuses the Phase 5 evidence pack; never mutates a live evidence store. |
| `statement-of-applicability-author` | Shared foundation | yes | The ISO-mandatory SoA serving BOTH 27001 and 42001: per-control include/exclude with 6.1.3 risk-treatment traces, verifiable exclusions, status mapped to foundation mechanisms, controlled-document diffs; requires the licensed Annex A table — never reconstructs entries or counts from memory. |
| `iso-27001-isms-architect` | Framework projection | yes | ISMS clauses 4–10 (incl. the Amd 1:2024 climate-relevance check), four-theme Annex A selection via the foundation; headline net-new = risk register, internal audit program, management review; theme counts flagged secondary-verify-before-citing; readiness plan, never a certification claim. |
| `iso-42001-aims-architect` | Framework projection | yes | AIMS clauses 4–10 + the three assessments (AI risk 6.1.2/8.2, AI risk treatment 6.1.3/8.3, AI system impact 6.1.4/8.4 on individuals/societies); maps the Phase 1.5 pack + `ai-governance-risk-reviewer` as operational mechanisms; Annex A counts never stated (sources conflict); ISMS-delta design when 27001 exists. |
| `soc2-trust-criteria-mapper` | Framework projection | yes | ATTESTATION-not-certification scoping: system boundary, commitment-driven category selection (Security baseline + optional four), Type 1 vs Type 2 with window feasibility, subservice-organization carve-outs; Type definitions flagged CPA-firm-sourced — verify against the AICPA guide. |
| `multi-framework-crosswalk` | Cross-cutting | yes | One row per control → 27001 Annex A + SOC 2 TSC + 42001 Annex A (+ AI RMF function); edition-pinned, text-in-hand cells only, FULL/PARTIAL(residue) honesty, explicit joint sets; the 60–80% overlap cited only as flagged industry estimate. |
| `compliance-gap-auditor` | Cross-cutting | yes | ONE parameterized audit vs chosen framework(s): MET/PARTIAL/GAP/UNVERIFIABLE per requirement from cited evidence (missing evidence is never MET), blockers-first remediation order, shared-gap dividend; readiness assessment, never an audit opinion. |
| `ai-lifecycle-risk-manager` | Cross-cutting | yes | NIST AI RMF GOVERN/MAP/MEASURE/MANAGE operationalized per lifecycle stage with owners, triggers, and a register; voluntary + under-revision flags encoded; composes feature reviews, threat models, evals, incident machinery; companion to the AIMS — never presented as certifiable. |

Trigger-overlap coverage (`evals/trigger-evals.json`) ships for all nine as
one **compliance cluster**: internal discrimination (foundation vs evidence
program vs SoA vs the three projections vs crosswalk vs gap audit vs
lifecycle program) plus cross-phase discrimination against the shipped
`agent-governance-audit` (process compliance of ONE agent change vs
framework compliance of the org), `ai-governance-risk-reviewer` (one AI
feature's governance posture vs org-level certification readiness),
`ai-sdlc-operating-model`, `audit-log-architect`,
`screenshot-evidence-planner`, `manual-test-case-creator`,
`authorization-matrix-designer`, `threat-modeler`, `ai-threat-modeler`,
`ai-evaluation-harness`, `slo-reliability-architect`,
`incident-response-runbook`, and `full-codebase-auditor`.

### Skills (D13 — library meta / self-application)

The complete D13 scope (reconciliation §3 D13 subsection; decisions D18 +
D22): the library applies its own discipline to itself.
`skill-quality-reviewer` shipped first (D18); the remaining four shipped
together (D22), completing the scope. All five ship `evals/evals.json`
**and** `evals/trigger-evals.json`, and all are pure review/design skills —
verdicts, specs, and plans; none edits anything — so all are
**model-invocable**. The composition web: `skill-quality-reviewer` COMPOSES
`scripts/validate-skills.py` as its entry gate; `library-diff-reviewer`
composes `skill-quality-reviewer` as its single-skill inner loop (the seam
pinned at D18, now owned from both sides); `eval-runner-designer` designs
execution for the eval corpus whose case INTEGRITY `skill-quality-reviewer`
judges; `skill-usage-instrumenter` produces the evidence package
`skill-deprecation-planner` consumes; and `skill-deprecation-planner`'s
doc-lifecycle twin (`docs-retention-index`, D12.4) stays banked with the
SKILL-vs-DOC seam pinned in trigger-evals.

| Skill | Source (D13) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `skill-quality-reviewer` | reconciliation §3 D13 — highest-leverage candidate, pulled first per the D13 standing rule (D18) | yes | The judgment layer above the mechanical validator: validator-first gate, then the seven checks it cannot script — trigger quality (trigger-oriented vs merely descriptive), trigger collision against the FULL shipped corpus (colliders NAMED), duplication/extension (LLM03/ASI04 precedent), eval integrity (boundary cases vs hollow filler), section substance (Stop Conditions that actually refuse), scope discipline, invocation posture. Per-check PASS/CONCERN/FAIL with quoted evidence → ship / revise / reject / make-it-an-extension. |
| `library-diff-reviewer` | reconciliation §3 D13 (D22) — the PR-level counterpart whose seam was pinned at D18 | yes | Reviews a whole library-changing PR end-to-end: fresh validator evidence pinned to the PR head, registration consistency (placement, post-merge voice, banked-candidate graduation, count arithmetic at EVERY site), collision sweep against the shipped corpus AND in-batch siblings, diff coherence (nothing smuggled in), per-skill quality via `skill-quality-reviewer` as the inner loop. One approve/request-changes verdict; performs no platform action. |
| `eval-runner-designer` | reconciliation §3 D13 (D22) — closes the design gap D3 left open ("there is no eval runner yet") | yes | Designs how the eval corpus would actually EXECUTE: per-case-type semantics (fresh isolated session; refusal cases fire AND refuse), pairwise discrimination scoring, deterministic-vs-LLM-judge assertion routing with JUDGE-ERROR honesty, UNRUN-default reporting, cost/sampling tiers, flake policy (repeats + quorum + visible quarantine), advisory-first CI. Design/spec only — never claims a runner exists or that evals pass. |
| `skill-usage-instrumenter` | reconciliation §3 D13 (D22) — usage telemetry design: invoked vs unused, wrong-fire evidence | yes | Designs the library's usage-evidence layer: invocation signals (auto vs explicit, coarse enums only — never prompt content or user identifiers), wrong-fire/correction events, computed never-fired lists over a stated window, evidence tiers (host-recorded vs self-reported), thresholds that name an action AND consumer, and the rare-but-critical exemption so low usage alone never condemns a safety-net skill. Adds no hooks; edits nothing. |
| `skill-deprecation-planner` | reconciliation §3 D13 (D22) — safe skill sunset: mark, redirect, remove | yes | Plans a skill's staged retirement: qualifying trigger (superseded + coverage diff / absorbed / evidenced disuse / defect), reverse-link sweep with a disposition per inbound reference, mark → redirect-window → remove with rollback per stage (squash removal reverts as one ordinary commit), registration rows moved to a retired record — never silently deleted. Plan only; every stage is human-approved. |

### Skills (D12.8 — operational workflow patterns pack)

Evidence-extracted pack (reconciliation §3 D12.8, banked by D15, built by D21):
the 10 operational workflow patterns extracted from a read-only audit of two
production multi-agent repositories
([`docs/research/aegis-workflow-extraction-report.md`](research/aegis-workflow-extraction-report.md)),
all HIGH confidence with concrete artifacts, product content stripped at
extraction (live identifiers templated as placeholders per report §6.3).
These are the concrete, invocable rules of the **Zero-Trust Engineering
Discipline** (D16) — its TRACK / VERIFY / GOVERN / HAND OFF groups. All 10
ship `evals/evals.json` **and** `evals/trigger-evals.json`; every skill names
the neighbor it composes with and discriminates against it in trigger-evals.
9 of 10 are advisory/design skills producing guidance → model-invocable;
`standing-approval-and-auto-advance` is **manual-only** because it authors
standing autonomy — the same reasoning that makes `agent-authorization-matrix`
manual-only.

| Skill | Source (D12.8 / report P-id) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `scoped-approval-register` | P2 | yes | Durable, append-style record of every granted approval — Status / Reason / Scope allowed / Scope FORBIDDEN / Evidence — with supersede-never-rewrite lifecycle and the deny-by-default citation rule. Composes `human-approval-boundary` (WHERE approval is required vs how the grant is recorded). |
| `standing-approval-and-auto-advance` | P3 | **no — manual only** | The governed anti-approval-fatigue layer: named-scope standing approval for the mechanical loop, phase-advance into already-approved phases only, per-session restated approval, explicit opt-out, reviewer-block path. Merge-after-green only as explicit opt-in profile, never default; never covers protected-branch merge or arming auto-merge; rationale cites the ungoverned-auto-merge incident in `agent-authorization-matrix`'s evals. |
| `chat-backlog-reconciliation` | P13 | yes | Cadenced extraction of chat-only decisions/bugs/backlog into dated repo docs, then per-item audit against PR/source evidence (completed/partial/active/not-active/unknown); chat claims cap at unknown without repo proof; standing rule: tracked repo docs, not stale chat. |
| `context-co-update-ci-gate` | P8 | yes | CI gate failing PRs that touch important paths without a context-map/notes update (declared no-op escape hatch, never silent) + the update protocol (date+SHA stamps, evidence-only status moves, risk notes never deleted without proof). Write-back half of `agent-startup-context-gate`'s read loop. |
| `lane-authoring-guide` | P10 | yes | Pre-work, evidence-cited guide per parallel agent lane: lifecycle slice, contracts, per-unit recipe + checklist, and the explicit "must NOT do" boundary; mutually exclusive lanes, cited claims or `unverified` labels. Work's BEGINNING — distinct from the closeout at work's end. |
| `local-ci-mirror-preflight` | P4 | yes | Per-commit CI mirror: derive local equivalents of every PR-triggered check from the workflow files, baseline on clean mainline FIRST (separate git worktree), classify every failure PR-caused / pre-existing / CI-infra / cannot-determine; declared docs-only path; preflight record feeds the closeout. |
| `risk-tiered-validation-selector` | P5 | yes | Fail-closed classifier from changed files to validation depth (docs-only / fast / full): never-docs-only and forced-full lists, max-over-files aggregation, diffable rules, unmatched ⇒ full. Routes validation COST where `change-classification-gate` routes APPROVAL. |
| `sharded-validation-with-resume` | P6 | yes | Full tier as named functional shards: persisted status file (failed ≠ interrupted), resume reruns only unfinished shards (never resumes past real failures), empty-or-fail uncategorized catch-shard, parallel shards into ONE aggregate gate as the sole required check. |
| `merge-is-deploy-governance` | P7 | yes | Standing governance when merge==deploy: documented reality (incl. what does NOT auto-deploy), PR validation promoted to the authoritative gate, post-merge demoted to verification, branch-protection config recorded in-repo (human-only changes), stated exposure window, revert-PR rollback with strategy-correct mechanics (squash ⇒ ordinary `git revert <sha>`). |
| `gated-deployment-prompt-template` | P11 | yes | Reusable operator prompt for recurring risky ops: placeholders only (no live identifiers; env-var names for credentials), hard rules with required inputs, stop conditions with safe halt states, backup-then-verify gating, per-phase smoke expectations, required per-run report, ETA ranges anchored to a deployment-history index; uncited claims labeled "unverified". |

### Skills (D12.1 — data engineering pack)

The 7-skill data engineering pack (reconciliation §3 D12 table, built by D23,
2026-07-07): multi-tenant operational + analytical data as a first-class
discipline. All 7 ship `evals/evals.json` **and** `evals/trigger-evals.json`;
all are design/plan/verdict skills that edit nothing → **model-invocable**.
The pack's decision chain: `operational-vs-analytical-splitter` decides WHAT
leaves the operational store; `streaming-event-architect` designs the CDC/
event transport it prescribes (internal pipeline only — the external contract
stays with `api-event-architect`, the batch's highest-risk seam, pinned both
ways); `warehouse-lake-architect` designs the analytical destination;
`data-quality-monitor-designer` watches the data content;
`pii-lifecycle-designer` overlays personal-data lifecycle rules estate-wide;
`schema-evolution-planner` sequences live schema change; and
`data-migration-runbook-author` turns approved plans into operator-executable
runbooks (consuming `secure-migration-reviewer` verdicts and
`rollback-runbook-author` conventions, executing nothing).

| Skill | Source (D12.1 / D23) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `schema-evolution-planner` | reconciliation §3 D12.1 | yes | Staged expand → migrate → contract plans for live-store schema change: per-stage old×new compatibility guarantees, consumer enumeration incl. events + analytics extracts, verification gates per stage, deprecation register, rollback per stage. Plans only; runbook and safety review are named handoffs. |
| `streaming-event-architect` | reconciliation §3 D12.1 | yes | INTERNAL event/stream backbone: per-flow stream-vs-queue, keys with honest ordering scope ("per key, unordered across keys"), at-least-once + idempotent consumers ("exactly-once" interrogated), DLQ with owner + replay, retention vs compaction, event-schema compatibility, CDC. External webhooks/feeds stay with `api-event-architect`. |
| `data-quality-monitor-designer` | reconciliation §3 D12.1 | yes | Data-content checks across six dimensions (freshness, volume, uniqueness, validity, consistency, drift) placed at ingest/transform/serving, each with severity, owner, and block/quarantine/alert-and-pass action — never silent auto-fix; per-dataset quality SLAs; alert wiring handed to `observability-operator`. |
| `operational-vs-analytical-splitter` | reconciliation §3 D12.1 | yes | Decides which workloads leave the transactional store and how (replica / CDC→analytical / materialized views / cache) against owner-stated freshness tolerance, with evidence-attributed pain, the one-bad-query escape to `query-plan-reader`, a stop-doing list with enforcement, and staged cutover. |
| `warehouse-lake-architect` | reconciliation §3 D12.1 | yes | The analytical estate: warehouse/lake/lakehouse by workload + team maturity, raw→conformed→curated zones with contracts, dimensional-vs-wide modeling + SCD policy, tenant key mandatory in every zone with per-tenant access for customer-facing analytics, PII per lifecycle rules, partitioning/formats, catalog governance, cost posture. |
| `pii-lifecycle-designer` | reconciliation §3 D12.1 | yes | Personal-data lifecycle estate-wide: classification, per-store data map (incl. logs, caches, vector stores, backups, vendors), minimization, retention with enforcement mechanics, erasure that PROPAGATES with an honest backup stance, anonymization-vs-pseudonymization with re-identification checks, residency. |
| `data-migration-runbook-author` | reconciliation §3 D12.1 | yes | Operator-executable data-move runbooks: prerequisites (approved plan + safety review + VERIFIED backup), signal-tuned batching with idempotent resume, per-batch verification with expected outputs, numeric abort criteria naming safe halt states, rollback per stage, no-return points flagged for human approval. Authors documents; executes nothing. |

### Skills (D12.3 — performance engineering pack)

The 6-skill performance engineering pack (reconciliation §3 D12 table, built
by D23, 2026-07-07): performance as an engineering discipline — these skills
**design FOR performance**; the D10 pair below **measures** it (the seam is
pinned in trigger-evals on both sides). All 6 ship both eval files; all are
design/analysis skills that edit nothing → **model-invocable**.
`profiling-methodology-designer` attributes unexplained time and hands
findings to the narrow tools: `query-plan-reader` (one heavy query) vs
`n-plus-one-detector` (many fast queries — the sibling seam), and
`frontend-perf-engineer` (the browser's share). `latency-budget-architect`
allocates targets it CONSUMES from `slo-reliability-architect` (never sets
them); `caching-strategy-designer` never caches authorization results by
default and defers a new cache store's isolation to
`multi-tenant-data-architect`.

| Skill | Source (D12.3 / D23) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `profiling-methodology-designer` | reconciliation §3 D12.3 | yes | Where-does-time-go methodology: attribution level first (trace / on-CPU / off-CPU / allocation — low utilization means WAITING), measurement conditions (warm/cold, representative load + volume, overhead budget), narrowing loop with stop rule and ruled-out register, handoff map. Production attach = approval-gated; fixes nothing. |
| `query-plan-reader` | reconciliation §3 D12.3 | yes | ONE query's plan → ranked verdict: dominant cost node, estimate-vs-actual divergence first (statistics refresh is the cheapest fix), sargability rewrites, composite indexes priced in write amplification, tenant/row-security predicate cost read, re-verification at representative volume. |
| `n-plus-one-detector` | reconciliation §3 D12.3 | yes | Chatty data-access patterns (N+1, repeated identical, serial awaits, over-fetch) evidenced by per-request counts, fixed by pattern (eager/preload, batched loaders memoized per REQUEST scope — a tenant-leak boundary), guarded by query-count budgets in tests. Refuses the cache-the-storm reflex. |
| `caching-strategy-designer` | reconciliation §3 D12.3 | yes | What/where/how-it-stays-correct caching: written consistency envelope per item, invalidation before shipping (backstop TTL always), tenant-qualified keys as a correctness boundary, stampede + cold-start protection, failure semantics, hit-ratio targets with a removal trigger. Authorization results never cached by default. |
| `latency-budget-architect` | reconciliation §3 D12.3 | yes | End-to-end target → per-hop budgets with closing arithmetic: overhead rows (serialization, queue wait, connections, retries), honest tail math on fan-out, timeouts DERIVED from budgets with cascade checks, explicit headroom, budget-claim review rule. Consumes SLO targets; never sets them. |
| `frontend-perf-engineer` | reconciliation §3 D12.3 | yes | The browser's share: metrics pinned to a device/network class, deletion-first weight audit, splitting with a floor, asset/font strategy, SSR/hydration honesty (the double bill), evidence-based runtime fixes, bundle-size + metric budgets as CI gates with a claim rule. |

### Skills (D10 Tier 1 — performance/load validation)

The 2-skill QA Tier 1 headline pair (reconciliation §3 Phase 5 QA-expansion
Tier 1, built by D23, 2026-07-07 — built as TWO skills; the banked may-merge
option was declined: instrument and traffic plan are different deliverables).
These **MEASURE** performance — the pre-release validation counterpart to the
D12.3 design pack and to Phase 6 `slo-reliability-architect`'s production
targets. Both ship both eval files; both are design skills that edit nothing
→ **model-invocable** — and both carry Stop Conditions forbidding execution
against production or live third parties without explicit human approval.

| Skill | Source (D10 / D23) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `performance-test-harness` | reconciliation §3 Phase 5 Tier 1 (#205) | yes | The measurement instrument: per-surface measured set, environment contract stamped on every result (volume, tenant shape, pinned hardware, declared cache state), baselines + variance-derived noise bands (single-run diffs banned), thresholds CONSUMED from budget/SLO owners, CI tiers with advisory→blocking promotion, UNRUN as a first-class status. |
| `load-test-planner` | reconciliation §3 Phase 5 Tier 1 (#206) | yes | The traffic plan: workload model from production evidence (write share explicit, open-vs-closed arrival model chosen), whale + long-tail tenant mix with the NOISY-NEIGHBOR scenario judged per-tenant, volumes with skew, load/stress/soak/spike by question, ramps with abort criteria, pass/fail citing owner-set numbers. |

### Skills (D12.2 — product engineering craft pack)

The 5-skill product-engineering craft pack (reconciliation §3 D12.2 table,
built by D24, 2026-07-07): the API/UX craft INSIDE the contract that
`api-event-architect` owns — the craft details (pagination cursors, error
taxonomies, empty/loading/error states, notification/webhook UX, mobile
viewport), never the contract itself. The `api-event-architect` seam is
pinned in every skill's trigger-evals; `error-taxonomy-designer` (the error
MODEL) and `edge-state-ux-designer` (rendering the error STATE) are pinned
against each other both ways. All 5 ship `evals/evals.json` **and**
`evals/trigger-evals.json`; all are design skills that edit nothing →
**model-invocable**.

| Skill | Source (D12.2 / D24) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `pagination-cursor-designer` | reconciliation §3 D12.2 | yes | The pagination MECHANISM inside a contract: cursor (keyset) vs offset with drift/deep-page costs stated, opaque versioned cursor (sort key + tiebreaker), strict total ordering, page-size bounds, honest end signaling, the tenant/permission predicate bound server-side (a cross-tenant paging boundary), surface pattern chosen. Contract/routes/rate-limits stay with `api-event-architect`. |
| `error-taxonomy-designer` | reconciliation §3 D12.2 | yes | The error MODEL: a finite taxonomy with stable machine codes, one envelope (code/message/details/correlation-id/retryable), an honest client-vs-server-vs-retryable split, actionable messages, ONE exception→taxonomy boundary, and a disclosure rule keeping stack traces/internals/PII out. Rendering the error state is `edge-state-ux-designer`. |
| `edge-state-ux-designer` | reconciliation §3 D12.2 | yes | The per-view non-happy-path state matrix: the three distinct empties (first-run/filtered/error), honest loading (skeleton vs spinner, delay threshold, optimistic rollback), error placement by blast radius, partial failure, refetch/offline, forbidden-not-empty. Renders `error-taxonomy-designer`'s codes; a11y verification is `accessibility-test-harness`. |
| `notification-webhook-ux-designer` | reconciliation §3 D12.2 | yes | The human-facing UX of notifications (channels, per-category preferences, digest/dedup noise control, read-state, opt-out that works) and developer webhooks (delivery log, test-send, replay, secret rotation with an overlap window). The delivery CONTRACT (envelope/signing/retry/versioning/subscriptions) stays with `api-event-architect`. |
| `mobile-viewport-craft` | reconciliation §3 D12.2 | yes | Mobile/responsive viewport correctness: content-driven breakpoints, touch-target sizing, safe-area/notch, the 100vh→dvh/svh/lvh fix, input/keyboard behavior, hover-absence and gestures, wide-table reflow. Page WEIGHT/network cost stays with `frontend-perf-engineer`; a11y verification with `accessibility-test-harness`. |

### Skills (D12.5 — PM / product-engineering interface pack)

The 6-skill PM/product-engineering interface pack (reconciliation §3 D12.5
table, built by D24, 2026-07-07): the engineering/PM boundary. Two hard
seams are pinned both ways in trigger-evals — `product-spec-writer` ≠
`adr-writer` (a product spec is a user-facing feature spec, not an
architecture decision record) and `sunset-deprecation-communicator` ≠
`skill-deprecation-planner` (sunsetting a product FEATURE for external
users vs retiring a library SKILL). `feature-flag-rollout-strategist` is
pinned ≠ `plan-entitlement-architect`/`authorization-matrix-designer`
(rollout vs entitlement/permission). All 6 ship both eval files; all are
facilitation/design skills that edit nothing → **model-invocable**.

| Skill | Source (D12.5 / D24) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `requirements-gathering-facilitator` | reconciliation §3 D12.5 | yes | Elicits requirements BEFORE a spec: separates the problem from stakeholders' solutions, draws out users/jobs and the current workaround, surfaces the implicit (assumptions, non-goals, constraints), reconciles conflict to a decider; produces a confidence-marked brief that feeds `product-spec-writer`. Facilitates; does not decide. |
| `product-spec-writer` | reconciliation §3 D12.5 | yes | The PRODUCT spec: problem/job, goals and explicit non-goals, scenarios, functional requirements with TESTABLE acceptance criteria, edge/error behavior, rollout intent + success metrics, open questions. Pinned ≠ `adr-writer` (a product spec is not an architecture decision record); routes technical decisions there. |
| `roadmap-under-uncertainty-planner` | reconciliation §3 D12.5 | yes | Horizon-based roadmap (now/next/later) over a false-precision dated Gantt: confidence decaying with distance, learning-first sequencing (retire uncertainty), outcomes over feature lists, capacity slack, a re-plan cadence. Consumes a ranking from `prioritization-frame-picker`; owns sequencing over TIME. |
| `prioritization-frame-picker` | reconciliation §3 D12.5 | yes | Picks the RIGHT prioritization frame (RICE/WSJF/value-effort/Kano/MoSCoW) instead of defaulting, marks input reliability, refuses false rigor (buckets + a sensitivity check), and pulls must-dos out of the value formula. Ranks; sequencing over time is `roadmap-under-uncertainty-planner`'s. |
| `feature-flag-rollout-strategist` | reconciliation §3 D12.5 | yes | The ROLLOUT strategy: flag classified by purpose, progressive stages with advance/rollback criteria, sticky targeting, guardrails + a tested kill switch, a fail-safe default, flag-debt removal. Pinned ≠ `plan-entitlement-architect`/`authorization-matrix-designer` (entitlement/permission) and ≠ `ab-test-designer` (experiment). |
| `sunset-deprecation-communicator` | reconciliation §3 D12.5 | yes | Sunsetting a PRODUCT feature/API to users: rationale, impact, migration path, a firm timeline, an escalating multi-channel comms plan, grandfathering, and a tombstone (not a silent 404). Pinned ≠ `skill-deprecation-planner` (retiring a library SKILL) and ≠ `api-event-architect` (standing deprecation policy). |

### Skills (D12.6 — growth / analytics engineering pack)

The 4-skill growth/analytics engineering pack (reconciliation §3 D12.6
table, built by D24, 2026-07-07): user-facing product analytics, distinct
from system-facing telemetry. Two THREE-way seams are pinned in
trigger-evals — `event-schema-architect` ≠ `api-event-architect`
(external contract) ≠ `streaming-event-architect` (internal pipeline);
and `product-analytics-instrumenter` ≠ `observability-operator` (system
telemetry) ≠ `skill-usage-instrumenter` (library usage signal).
`ab-test-designer` covers BOTH experiment design and result reading. All 4
ship both eval files; all edit nothing → **model-invocable**.

| Skill | Source (D12.6 / D24) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `event-schema-architect` | reconciliation §3 D12.6 | yes | The ANALYTICS event schema/tracking plan: naming taxonomy, typed properties, global properties, identity stitching (anonymous→identified), a registry as source of truth, additive versioning, PII minimization. THREE-way seam pinned ≠ `api-event-architect` (external contract) ≠ `streaming-event-architect` (internal pipeline). |
| `funnel-definition-designer` | reconciliation §3 D12.6 | yes | Rigorous funnel/conversion/retention definition: steps from real events, a counting model with a pinned denominator, a stated window, order semantics, attribution, and WHERE-not-WHY discipline (causes need an experiment). Consumes `event-schema-architect`; ≠ `ab-test-designer` (causal test). |
| `ab-test-designer` | reconciliation §3 D12.6 | yes | Designs AND reads experiments: falsifiable hypothesis, one primary metric + guardrails, power/sample-size from a practical MDE, a fixed horizon (no peeking), sticky assignment; readout with CIs, multiple-comparison/SRM/Simpson's/novelty checks, ship/kill/iterate with residual uncertainty. Pinned ≠ `feature-flag-rollout-strategist` (safety rollout). |
| `product-analytics-instrumenter` | reconciliation §3 D12.6 | yes | The product-analytics INSTRUMENTATION: client-vs-server capture, identity at capture, consent-gating + PII minimization at the source, capture reliability, de-dup, tracking QA. THREE-way seam pinned ≠ `observability-operator` (system telemetry) ≠ `skill-usage-instrumenter` (library usage). |

### Skills (D12.4 — technical writing / docs engineering pack)

The 8-skill docs engineering pack (reconciliation §3 D12.4 table, built by
D25, 2026-07-07 — PART A of the D12.4+D12.7+D12.9+D14 two-PR batch):
durable documentation as its own discipline. Three seams are pinned in
trigger-evals: `adr-sequencer` EXTENDS `adr-writer` (longitudinal ADR
corpus management — composes it, does not duplicate single-record
authoring); `docs-retention-index` ↔ `skill-deprecation-planner` (DOC
lifecycle/retirement vs library-SKILL retirement — pinned both ways, the
seam `skill-deprecation-planner` already referenced as "banked, not
built"); `api-doc-generator-designer` ↔ `api-event-architect` (generated
reference vs the API contract). All 8 ship `evals/evals.json` **and**
`evals/trigger-evals.json`; all are authoring/design skills that produce
docs/plans and edit nothing → **model-invocable** (`docs-retention-index`
gates actual doc DELETION behind human approval).

| Skill | Source (D12.4 / D25) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `readme-craftsman` | reconciliation §3 D12.4 | yes | The README as entry point, not manual: first-screen what/why/who, a verified quickstart, common-case usage, and routes OUT to deeper docs; resists the kitchen sink and stays maintainable. |
| `adr-sequencer` | reconciliation §3 D12.4 | yes | Longitudinal ADR CORPUS management atop `adr-writer`: the index, status lifecycle, bidirectional superseding links, contradiction detection, new-ADR-vs-amend, append-only history (supersede, never overwrite). Composes `adr-writer` for single records. |
| `diataxis-doc-organizer` | reconciliation §3 D12.4 | yes | Organizes the whole docs SET by the four Diátaxis modes (tutorial/how-to/reference/explanation), diagnosing actual-vs-claimed mode, splitting two-job docs, cross-linking not embedding, and setting the anti-mode-bleed discipline. |
| `docs-as-code-architect` | reconciliation §3 D12.4 | yes | The docs TOOLCHAIN/pipeline: in-repo PR-reviewed docs, generator choice, per-PR previews, CI link/prose/build checks, executable-sample testing (the drift-killer), versioned publishing, URL stability. Not the content or its organization. |
| `api-doc-generator-designer` | reconciliation §3 D12.4 | yes | GENERATED API reference from the source of truth (OpenAPI/GraphQL/docstrings) so it can't drift: the generated-vs-authored split, upstream enrichment, validated examples, versioning. Documents the contract `api-event-architect` owns. |
| `contribution-guide-author` | reconciliation §3 D12.4 | yes | The zero-to-merged CONTRIBUTING guide: verified setup, the real workflow, automated standards, honest review expectations, governance + PRIVATE security disclosure, and first-contribution on-ramps. Product-agnostic. |
| `onboarding-doc-designer` | reconciliation §3 D12.4 | yes | New-hire onboarding: the day1/week1/month1 ramp, verified setup, a mental-model orientation (not the manual), how-we-work incl. unwritten norms, a glossary + who-to-ask, an early-win first task, and a self-heal currency plan. |
| `docs-retention-index` | reconciliation §3 D12.4 | yes | The numbered DOC-lifecycle index: retention category + reason-to-keep + superseded-by + cleanup rule per doc (mirrored in frontmatter), reverse-reference sweep, staged mark→redirect→remove with human-approved deletion. DOC counterpart to `skill-deprecation-planner` (pinned both ways). |

### Skills (D12.7 — staff+ IC craft pack)

The 7-skill staff+ IC craft pack (reconciliation §3 D12.7 table, built by
D26, 2026-07-07 — PART B of the D12.4+D12.7+D12.9+D14 two-PR batch):
technical leadership without management authority. Seams pinned in
trigger-evals: `tech-spec-writer` ≠ `adr-writer` (whole design vs one
decision) ≠ `product-spec-writer`; `phased-work-handoff-designer` ≠
`ai-closeout-reporter` (one turn) ≠ `ai-sdlc-operating-model` (lifecycle);
`staff-scope-selector` ≠ `promotion-packet-writer` (future scope vs past
impact, both ways). All 7 ship both eval files; all produce specs/plans/
verdicts and edit nothing → **model-invocable**.

| Skill | Source (D12.7 / D26) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `tech-spec-writer` | reconciliation §3 D12.7 | yes | The whole-design tech spec / RFC: problem/goals/non-goals, proposed design (data model, APIs, components), alternatives, cross-cutting concerns (security/perf/observability/migration/testing), risks, sign-off. Composes `adr-writer` + `architecture-designer`. ≠ one ADR, ≠ product spec. |
| `design-review-facilitator` | reconciliation §3 D12.7 | yes | Facilitates the design review: pre-read + right reviewers, importance-first discussion, actively elicited dissent, an EXPLICIT outcome, captured decisions — countering rubber-stamp/bikeshed/HiPPO/no-decision. Reviews a design; doesn't write it. |
| `cross-team-dependency-negotiator` | reconciliation §3 D12.7 | yes | Cross-team dependencies: two-way map, early surfacing, CONCRETE commitments (deliverable+date+owner both sides), de-risking (stub/flag/parallel), honest accounting for the other team's priorities, and a pre-agreed escalation trigger. The interface contract is `api-event-architect`'s. |
| `roadmap-to-commitments-translator` | reconciliation §3 D12.7 | yes | Extracts the firm-promise subset from a roadmap: commit-able vs aspirational, capacity-grounded (velocity minus maintenance, buffered), dependency-gated, honest date RANGES, and the not-committed gap named. The inverse of `roadmap-under-uncertainty-planner`. |
| `staff-scope-selector` | reconciliation §3 D12.7 | yes | Chooses a staff+ IC's highest-leverage FUTURE scope: level-relative leverage, under-owned problems, matched to strengths, screened against the traps (only-fun/firefighting/too-narrow/invisible-glue/over-reach), with a rationale + explicit NOT-doing list. ≠ `promotion-packet-writer`. |
| `promotion-packet-writer` | reconciliation §3 D12.7 | yes | Assembles the promotion case: impact-not-activity, mapped to every rubric dimension, a sustained pattern, honest gap analysis, corroboration, committee language — no inflation. ≠ `staff-scope-selector` (future scope), ≠ `ai-closeout-reporter` (one task). |
| `phased-work-handoff-designer` | reconciliation §3 D12.7 | yes | The cross-stage handoff protocol: a decision-ID register carried across stages, per-stage changed/NOT-touched lists, proven-invocation evidence (tell-tale output), deviation flags, and a cold-start continuation contract. ≠ `ai-closeout-reporter` (one turn), ≠ `ai-sdlc-operating-model` (lifecycle). |

### Skills (D12.9 — architecture advisory pack)

The 1-skill architecture advisory pack (reconciliation §3 D12.9, added by
D20, built by D26, 2026-07-07): the architecture STYLE/paradigm advisor
that filled the gap between `architecture-designer` (concrete architecture)
and `cloud-architecture-decider` (cloud posture). Ships both eval files;
edits nothing → **model-invocable**.

| Skill | Source (D12.9 / D26) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `architecture-advisor` | reconciliation §3 D12.9 | yes | Advises the architecture STYLE (monolith/modular-monolith/microservices/event-driven/serverless/SOA/hybrid): interviews the need FIRST, relevant candidates only, case-specific tradeoffs, a clear recommendation + sensitivity; resists trend-chasing both ways (willing to say "boring modular monolith"). ≠ `architecture-designer` (concrete), `cloud-architecture-decider`, `saas-platform-architect`, `domain-modeler`. |

### Skills (D14 — framework refresh / source-currency pack)

The 3-skill framework refresh / source-currency pack (reconciliation §3 D14,
built by D26, 2026-07-07): keeping the library current with EXTERNAL truth,
distinct from D12 (breadth) and D13 (self-quality). A pipeline —
`framework-edition-tracker` (detect edition drift + delta) →
`framework-mapping-refresher` (propose the edits, human review) — plus
`source-currency-auditor` (the broad staleness sweep). NONE auto-updates:
all detect/propose/flag and hand changes to human review. All 3 ship both
eval files; all edit nothing → **model-invocable**.

| Skill | Source (D14 / D26) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `framework-edition-tracker` | reconciliation §3 D14 | yes | Tracks cited standard EDITIONS (OWASP/ISO/SOC 2/NIST): an edition register, drift detection, and a DELTA report — verify-don't-assert edition facts; reports drift, updates nothing. Feeds `framework-mapping-refresher`. ≠ broad staleness (`source-currency-auditor`). |
| `framework-mapping-refresher` | reconciliation §3 D14 | yes | Turns a verified edition delta into SPECIFIC proposed edits across affected skills/references/coverage maps, judging meaning-not-labels, surfacing new coverage GAPS, flagged for HUMAN review — never auto-applied. Downstream of `framework-edition-tracker`, upstream of `library-diff-reviewer`. |
| `source-currency-auditor` | reconciliation §3 D14 | yes | Broad citation-currency sweep: inventory external-source citations, volatility-tuned staleness thresholds, flag stale/broken/superseded with reason and load-bearing priority — flags for re-verification, verifies/changes nothing. ≠ edition tracking (`framework-edition-tracker`). |

### Skills (D28 — OWASP web-app A09/A10 gap closure)

The 2-skill OWASP Web-App Top 10:2025 gap-closure pair (the D8 audit's two
zero-coverage categories, tracked as reconciliation §3 Phase 8 backlog
items; built by D28, 2026-07-08): with these, all 10 web-app categories
have at least one owning skill — A02/A04 remain "partial" by the D8 rubric.
Both ship both eval files; both edit nothing → **model-invocable**.

| Skill | Source (D8 backlog / D28) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `security-logging-alerting-architect` | reconciliation §3 Phase 8 backlog (D8) | yes | Designs the security-event DETECTION and ALERTING layer (closes OWASP A09:2025): the detection coverage map (which security events must be logged, with detectable fields), alert-vs-ticket rules with baseline-justified thresholds + bounded noise control, and response wiring (owner, severity, escalation, runbook link) with coverage tests and an honest blind-spot register. ≠ `audit-log-architect` (records, never detects/alerts), `observability-operator` (implements the alert config), `slo-reliability-architect` (reliability paging), `incident-response-runbook` (the playbook AFTER the alert). |
| `error-handling-security-reviewer` | reconciliation §3 Phase 8 backlog (D8) | yes | Reviews error/exception handling through the security lens (closes OWASP A10:2025): fail-closed defaults, error-path authorization, exception-driven logic bypass, leak-free error responses — file:line findings with concrete failure scenarios and a fail-closed matrix; recommends fixes, never applies them. ≠ `security-pr-reviewer` (broad diff gate), `appsec-implementer` (builds the fix), `static-analysis-reviewer` (judges scanner output), `error-taxonomy-designer` (the error MODEL vs the security of its handling). |

### Skills (D31 — SaaS architecture depth, D12.11 strong cluster)

The 10-skill D12.11 STRONG cluster (reconciliation §3 D12.11; built by D31,
2026-07-08), scheduled ahead of the D12.10 SAST/DAST pack. Net-new
architecture-depth surfaces for a multi-tenant SaaS from a read-only audit of
production SaaS patterns. All are design/review skills editing nothing →
**model-invocable**; the three that can touch live systems
(`command-gateway-architect`, `synthetic-monitoring-architect`,
`offline-first-sync-architect`) carry Stop Conditions forbidding execution
against production without human approval. `usage-metering-and-cost-attribution-pipeline-designer`
resolved **STANDALONE** (not an extension of `saas-cost-architect`). The 4
low-priority D12.11 candidates were the deferred Build B, since built by D32
(below). All ship both eval files.

| Skill | Source (D12.11 / D31) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `command-gateway-architect` | reconciliation §3 D12.11 | yes | The single server-mediated write path (command bus): command registry + fixed per-command pipeline (validate → authenticate actor from token → authorize → server-derive tenant scope from trusted rows → idempotency → execute → emit audit+events → safe error envelope) + the no-direct-client-writes invariant (datastore backstop). ≠ `api-event-architect` (external contract), `authorization-matrix-designer` (the policy it ENFORCES), `audit-log-architect` (record schema it emits into), `streaming-event-architect` (event transport). |
| `realtime-subscription-architect` | reconciliation §3 D12.11 | yes | Live client delivery (WS/SSE/DB-change/presence): server-derived channel keys, authorize-at-subscribe-time re-checked as authority changes (per-tenant AND per-user leak boundary), cross-node fan-out, stateful-connection scaling + drain, backpressure, reconnect/replay, presence. ≠ `streaming-event-architect` (internal backbone), `api-event-architect` (webhooks), `offline-first-sync-architect` (offline sync — in-batch seam), `notification-webhook-ux-designer` (UX). |
| `background-job-orchestration-architect` | reconciliation §3 D12.11 | yes | The async job/worker EXECUTION model: worker pools, cron with overlap/missed-run policy, job idempotency + resumability/checkpointing, retry/backoff + poison classifier, DLQ with owner, visibility timeouts, per-tenant fairness. ≠ `streaming-event-architect` (transport vs execution — hard pin), `performance-test-harness`/`load-test-planner` (measure it), `command-gateway-architect` (synchronous protected write). |
| `horizontal-scalability-reviewer` | reconciliation §3 D12.11 | yes | Can-it-scale-out review: statelessness/session externalization, connection-ceiling math, sticky-session / in-process-singleton / local-cache / run-N-times / local-filesystem smells, autoscaling + LB + graceful drain — ranked readiness verdict. ≠ `slo-reliability-architect` (sets targets), `latency-budget-architect` (latency allocation), `caching-strategy-designer` (cache design). |
| `search-architecture-designer` | reconciliation §3 D12.11 | yes | Keyword/faceted search: in-DB full-text (tsvector/pg_trgm) vs engine, indexing pipeline + honest freshness lag, ranking, the query-side AND index-side per-tenant isolation boundary (fail-closed, negative-tested), faceting/pagination seam. ≠ `rag-security-architect` (semantic/vector), `multi-tenant-data-architect` (base tenancy), `pagination-cursor-designer` (cursor mechanics). |
| `file-upload-storage-architect` | reconciliation §3 D12.11 | yes | File/object storage + upload: direct-vs-proxied, one-verb/one-key short-expiry signed URLs, tenant-prefixed server-derived keys, magic-byte content validation, malware scan before serve, off-request derivatives, retention/lifecycle, CDN, safe serving (no stored XSS). ≠ `pii-lifecycle-designer` (personal-data lifecycle of contents), `rls-policy-auditor` (audit existing storage policies). |
| `usage-metering-and-cost-attribution-pipeline-designer` | reconciliation §3 D12.11 — **resolved STANDALONE (D31)** | yes | The metering→pricing→rollup→reconciliation DATA PIPELINE: billing-safe metadata-only event table, time-bounded rate cards, idempotent cost entries (safe under replay), additive reconstructable rollups, budgets/alerts/forecast, invoice reconciliation, correction handling. ≠ `saas-cost-architect` (unit-economics cost MODEL — closest neighbor, hard pin), `ai-cost-guardrail-designer` (AI spend enforcement), `operational-vs-analytical-splitter` (rollup placement). |
| `synthetic-monitoring-architect` | reconciliation §3 D12.11 | yes | Black-box PRODUCTION monitoring: incident-value probe catalog (journey/dependency/heartbeat), a HARD prod-safety contract (no mutation, ring-fenced synthetic accounts, no fixture leak, cleanup), synthetic SLIs feeding SLOs, sustained-failure alerting. DESIGNS probes; does not run them against prod. ≠ `performance-test-harness`/`load-test-planner` (pre-release), `playwright-e2e-engineer` (CI E2E), `slo-reliability-architect` (targets), `observability-operator` (white-box). |
| `offline-first-sync-architect` | reconciliation §3 D12.11 | yes | The client OFFLINE data layer: durable ordered write queue with client-id idempotency, optimistic apply + rollback on reject, version-based conflict detection + eyes-open resolution (LWW/merge/CRDT/manual — refuses silent data loss), background sync (dedup), reconciliation integrity. ≠ `edge-state-ux-designer` (UX states), `caching-strategy-designer` (server cache), `realtime-subscription-architect` (live online push — in-batch seam). |
| `admin-console-architect` | reconciliation §3 D12.11 (HIGH/pull-forward) | yes | The internal ops/support/superadmin CONSOLE: least-privilege tiers, audited-by-construction cross-tenant access (reads too), bounded/marked/consented/time-boxed impersonation, break-glass elevation (approved, auto-expiring), gated + reversible control-plane actions. ≠ `authorization-matrix-designer` (the policy it ENFORCES), `observability-operator` (telemetry vs action surface), `agent-authorization-matrix` (AI-agent vs human), `incident-response-runbook` (the playbook it serves). |

### Skills (D32 — SaaS architecture depth, D12.11 low-priority set)

The 4-skill D12.11 LOW-PRIORITY set (reconciliation §3 D12.11; built by D32,
2026-07-08) — the deferred Build B, completing the D12.11 pack (all 14
candidates resolved: 10 strong D31 + 4 low-priority D32). These are
scale-stage or possibly-extension surfaces. Two carried a
standalone-vs-extension flag resolved at build time: `intra-tenant-scope-architect`
and `share-link-access-architect` both shipped **STANDALONE** (each ~60%
distinct from its candidate parent). All are design/review skills editing
nothing → **model-invocable**; the three that DESIGN a production-reshaping
change (`cell-based-architecture-designer` cell migration/rebalancing,
`data-partitioning-sharding-strategist` reshard, `intra-tenant-scope-architect`
add-a-scope-axis migration) carry Stop Conditions forbidding execution against
production without human approval. All ship both eval files.

| Skill | Source (D12.11 / D32) | Model-invocable? | Trigger summary |
| --- | --- | --- | --- |
| `cell-based-architecture-designer` | reconciliation §3 D12.11 (LOW) | yes | Cell (blast-radius) partitioning: a self-contained full-stack cell per tenant-subset, tenant→cell mapping + placement, a THIN cell-router, cell-by-cell deploy/canary, global-concern enumeration, migration/rebalancing (designed, not run). SCALE-STAGE — tests the premise first and recommends NOT adopting cells when a cheaper lever suffices. ≠ `saas-platform-architect` (per-component pooled/siloed isolation, not whole-stack cells), `architecture-advisor` (the style choice, whose menu omits cells), `agent-containment-reviewer` (agent blast radius, not infra cells). |
| `data-partitioning-sharding-strategist` | reconciliation §3 D12.11 (LOW) | yes | OLTP partitioning/sharding for WRITE/size scale: shard-key selection (tenant_id + its hot-tenant limit), range/hash/list partitioning, cross-shard cost, reshard/rebalance runbook (designed, not run) — gated behind DON'T-SHARD-PREMATURELY (single well-indexed primary + replicas first; shard only on evidenced ceiling). ≠ `multi-tenant-data-architect` (isolation scoping, not throughput), `warehouse-lake-architect` (analytical partitioning), `operational-vs-analytical-splitter` (what leaves the OLTP store). |
| `intra-tenant-scope-architect` | reconciliation §3 D12.11 (LOW/flag) — **resolved STANDALONE (D32)** | yes | A second mandatory scoping axis BELOW the tenant (site/region/org-unit): per-user scope-grant model, the composite tenant+scope row-filter predicate on every scoped table, scope-restricted vs tenant-wide roles, server-derived propagation through app+edge, live add-axis migration (designed, not run). ≠ `tenant-modeler` (tenant semantics/hierarchy — a child tenant is a separate boundary), `multi-tenant-data-architect` (the tenant_id storage axis this presupposes), `authorization-matrix-designer` (roles×permissions vs a row-filter dimension), `command-gateway-architect` (execute-time write scope vs the standing read-side axis). |
| `share-link-access-architect` | reconciliation §3 D12.11 (LOW/flag) — **resolved STANDALONE (D32)** | yes | Guest/public share-link (bearer-capability) access: opaque high-entropy expiring revocable tokens, per-link scope (one resource, one permission), ephemeral guest sessions (not memberships), optional password/OTP gate, enumeration/abuse defense (no existence oracle), audit — the link exposes exactly its resource, never a hole into the tenant. ≠ `authorization-matrix-designer` (member RBAC + impersonation, not anyone-with-the-link), `api-event-architect` (machine API credentials / webhook signing). |

---

## Backlog by phase (reconciled)

The v4 phase structure is canonical. Each phase's first-pass skills are listed; see the
reconciliation doc §3 for merge/move notes and the per-phase "expansion backlog."

### Phase 1 — AI operating-discipline pack (P0)
✅ **Implemented** — all 8 skills moved to [Implemented → Skills](#skills-phase-1--operating-discipline-pack) above.
Source: [`docs/skills/08-ai-era-sdlc-agent-ops.md`](skills/08-ai-era-sdlc-agent-ops.md).

### Phase 1.5 — AI-SDLC governance completion (P0/P1)
✅ **Implemented** — 4 skills (roadmap #261/#268/#279/#280) moved to
[Implemented → Skills (Phase 1.5)](#skills-phase-15--ai-sdlc-governance-completion)
above, completing the category-08 governance layer Phase 1 started.
Source: [`docs/skills/08-ai-era-sdlc-agent-ops.md`](skills/08-ai-era-sdlc-agent-ops.md).
The remaining cat-08 items (#266 AI Task Decomposition, #267 Prompt-to-Diff
Traceability, #273 AI Work Evidence Pack, #277 AI Code Review Protocol, #278 AI
Pair Engineering Protocol) remain backlog, built in Phase 8 batches.

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
✅ **Implemented** — all 9 first-pass skills moved to
[Implemented → Skills (Phase 3)](#skills-phase-3--saas--tenant-isolation-pack) above.
Source: [`docs/skills/02-saas-platform-architecture.md`](skills/02-saas-platform-architecture.md).
Reconciliation §3 merges: `rls-policy-author` / `rls-negative-test-designer` are
**deferred to Phase 4** (merged into `rls-policy-auditor`); the Phase 3 **expansion
backlog** (`tenant-provisioning-designer`, `membership-invitation-designer`,
`role-permission-architect`, `security-impact-note-author`) remains backlog, built in
Phase 8 batches.

### Phase 4 — Security, RLS & supply chain (P0/P1)
✅ **Implemented** — all 9 first-pass skills moved to
[Implemented → Skills (Phase 4)](#skills-phase-4--security-rls--supply-chain-pack) above.
Source: [`docs/skills/03-saas-security-rls.md`](skills/03-saas-security-rls.md).
Reconciliation §3 merge: the execution-plan `rls-policy-author` and
`rls-negative-test-designer` are merged into `rls-policy-auditor` (no separate skills).
The Phase 4 **expansion backlog** (the remaining cat-03 rows: authentication/session
review, CSRF/XSS/SQLi deep-dives, storage-policy review, webhook security, rate-limit
design, logging redaction, compliance-evidence mapping, privacy-by-design, security-drift
detection, security-impact-note authoring) remains backlog, built in Phase 8 batches.

### Phase 5 — QA, E2E, manual QA & evidence (P0/P1)
✅ **Implemented** — all 13 canonical first-pass skills PLUS 3 pulled forward from the
QA backlog (`integration-test-designer` #184, `api-contract-test-designer` #185,
`accessibility-test-harness` #204) moved to
[Implemented → Skills (Phase 5)](#skills-phase-5--qa-e2e-manual-qa--evidence-pack) above.
Source: [`docs/skills/06-qa-test-engineering.md`](skills/06-qa-test-engineering.md),
[`05-frontend-ux-engineering.md`](skills/05-frontend-ux-engineering.md).
Per reconciliation §3, the Phase 5 **expansion backlog** (`acceptance-criteria-tester`,
`e2e-test-architect`, `qa-closeout-reporter` — the latter overlaps the shipped
`ai-closeout-reporter` + `screenshot-evidence-planner` — plus the remaining cat-06 rows)
remains backlog, built in Phase 8 batches — **except the Tier 1 headline pair
`performance-test-harness` + `load-test-planner` (#205/#206), ✅ built by D23
(2026-07-07) as two skills and moved to
[Implemented → Skills (D10 Tier 1)](#skills-d10-tier-1--performanceload-validation)
above.**

### Phase 6 — Cloud, DevOps, reliability & release (P1)
✅ **Implemented** — all 10 first-pass skills moved to
[Implemented → Skills (Phase 6)](#skills-phase-6--cloud-devops-reliability--release-pack) above.
Source: [`docs/skills/07-devops-release-reliability.md`](skills/07-devops-release-reliability.md)
plus master-prompt §8 for the three cloud skills.
Reconciliation §3 merge: `rollback-strategy-designer` is merged into
`rollback-runbook-author` (no separate skill). The Phase 6 **expansion backlog**
(`cloud-security-baseline-reviewer`, `resilience-architecture-reviewer`,
`migration-deployment-runbook`, `environment-parity-reviewer`,
`database-backup-verifier`) remains backlog, built in Phase 8 batches.

> Note: `release-readiness-reviewer` and `full-codebase-auditor` exist as **subagents**
> (review lens) and also as **skills** (procedure) — `full-codebase-auditor` skill shipped
> in Phase 2; `release-readiness-reviewer` skill shipped here in Phase 6. Different
> namespaces (`.claude/agents/` vs `.claude/skills/`); the agent composes the skill.

### Phase 7 — AI security & LLM systems (P1)
✅ **Implemented** — all 14 skills (v4's 10 + 4 OWASP LLM Top 10 gap additions,
D6) moved to
[Implemented → Skills (Phase 7)](#skills-phase-7--ai-security--llm-systems-pack)
above. Source: [`docs/skills/09-ai-software-engineering.md`](skills/09-ai-software-engineering.md)
and the reconciliation doc §3 Phase 7 coverage map (D6).
Per D6: **LLM03** is extend-existing — the shipped Phase 4
`supply-chain-security-reviewer` was extended (scoped diff) to the AI/ML supply
chain (models, datasets, fine-tuning adapters); **LLM10** DoS/denial-of-wallet
is baked into `ai-cost-guardrail-designer`; and `ai-evaluation-harness` absorbs
the AI security test harness (no separate `ai-security-test-harness`). The
Phase 7 **expansion backlog** (`ai-provider-adapter-designer`,
`prompt-contract-designer`, `ai-human-in-the-loop-designer`,
`ai-autonomy-boundary-designer`, `ai-feature-kill-switch-designer` — whose
agentic slice is now covered by `agent-containment-reviewer`) remains
backlog, built in Phase 8 batches. Phase 7.5 (agentic AI security, D7) is
implemented below; the Compliance & Governance batch (D9) follows it.

### Phase 7.5 — Agentic AI security (P1)
✅ **Implemented** — all 6 new skills + 3 extensions (OWASP Agentic Top 10,
D7) moved to
[Implemented → Skills (Phase 7.5)](#skills-phase-75--agentic-ai-security-pack)
above. Source: the reconciliation doc §3 Phase 7.5 coverage map (D7),
anchored to the OWASP Top 10 for Agentic Applications (2026), ASI01–ASI10.
Per D7: **ASI08 + ASI10 merged** into `agent-containment-reviewer`;
**ASI02/ASI05** extend Phase 7 `agent-tool-safety-guard` and
`llm-output-safety-reviewer` (scoped diffs); **ASI04** extends Phase 4
`supply-chain-security-reviewer` again after the D6/LLM03 extension. The
Compliance & Governance batch (D9) is implemented below.

### Compliance & Governance batch (D9)
✅ **Implemented** — all 9 skills moved to
[Implemented → Skills (Compliance & Governance batch)](#skills-compliance--governance-batch--d9)
above. Source: the reconciliation doc §3 "Compliance & Governance batch"
subsection + D9 in §5, including every per-source verification flag.
Architecture per D9: one shared control foundation
(`compliance-control-foundation`, `compliance-evidence-collector`,
`statement-of-applicability-author`) + framework projections
(`iso-27001-isms-architect`, `iso-42001-aims-architect`,
`soc2-trust-criteria-mapper`) + cross-cutting (`multi-framework-crosswalk`,
`compliance-gap-auditor`, `ai-lifecycle-risk-manager`) — the 9 reconciled
candidates, already merged, NOT split into per-framework variants. The
batch maps controls that largely already exist (Phases 3/4, the Phase 5
evidence pack, Phase 1.5 + Phase 7 AI governance) and produces
auditor-grade evidence on top.

### D13 — Library meta / self-application (fully implemented)
All 5 skills ✅ **implemented** — `skill-quality-reviewer` (D18), then
`library-diff-reviewer`, `eval-runner-designer`, `skill-usage-instrumenter`,
and `skill-deprecation-planner` (D22, 2026-07-07, completing the scope) —
moved to
[Implemented → Skills (D13)](#skills-d13--library-meta--self-application)
above. Source: the reconciliation doc §3 D13 subsection + D13/D18/D22 in §5.

### D12.8 — Operational workflow patterns (evidence-extracted; implemented)
All 10 skills ✅ **implemented** (D21, 2026-07-07) — moved to
[Implemented → Skills (D12.8)](#skills-d128--operational-workflow-patterns-pack)
above: the concrete rules of the Zero-Trust Engineering Discipline (D16).
Source: the reconciliation doc §3 D12.8 subsection (banked by D15) and
[`docs/research/aegis-workflow-extraction-report.md`](research/aegis-workflow-extraction-report.md).
`docs-retention-index` (P1) remains banked under D12.4; the D15 enrichment
deltas for shipped skills remain recorded in reconciliation §3 — neither is
part of this pack.

### D12.1 + D12.3 — Data engineering & performance engineering (implemented)
All 13 skills ✅ **implemented** (D23, 2026-07-07) — moved to
[Implemented → Skills (D12.1)](#skills-d121--data-engineering-pack) and
[Implemented → Skills (D12.3)](#skills-d123--performance-engineering-pack)
above. Source: the reconciliation doc §3 D12 candidate-pack table (banked by
D12) + D23 in §5. The remaining D12 packs (D12.2 product craft, D12.4 docs
engineering incl. `docs-retention-index`, D12.5 PM interface, D12.6
growth/analytics, D12.7 staff+ craft) remain banked candidates.

### Phase 8 — Backlog expansion (P2)
Remaining roadmap skills, generated in validated batches of ≤20 (see reconciliation §4.1).
The two D8-audit backlog items (`security-logging-alerting-architect`,
`error-handling-security-reviewer`) are ✅ **built** (D28, 2026-07-08) and moved to
[Implemented → Skills (D28)](#skills-d28--owasp-web-app-a09a10-gap-closure) above.

---

## Capability map (300+ target backlog)

The strategic backlog the library was audited against lives in
[`docs/300-repeatable-software-saas-skills-roadmap.md`](300-repeatable-software-saas-skills-roadmap.md)
— the original 300. Per the D12 standing rule the library is NOT capped at 300 skills: this
is a 300+ target backlog, and skills ship on demand and framework coverage, not count:

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
