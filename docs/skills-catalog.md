# Skills & Agents Catalog

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
> reliability & release pack), and Phase 7 (the 14-skill AI security &
> LLM systems pack — v4's 10 plus 4 OWASP LLM Top 10 gap additions, D6)
> are implemented. `_template` remains a
> reference template ignored by the validator. Everything under "Backlog" is
> planned, not built.

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
remains backlog, built in Phase 8 batches.

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
`ai-autonomy-boundary-designer`, `ai-feature-kill-switch-designer`) remains
backlog, built in Phase 8 batches. Phase 7.5 (agentic AI security, D7) and the
Compliance & Governance batch (D9) follow it.

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
