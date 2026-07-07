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
(reconciled decision D4). **Phase 2** ships the 10-skill **core architecture &
engineering pack** — see [Skills (shipped)](#skills-shipped) below.

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
| 2 | Core architecture & engineering (10) | P0 | ✅ this branch |
| 3 | SaaS & tenant isolation (9) | P0/P1 | backlog |
| 4 | Security, RLS & supply chain (9) | P0/P1 | backlog |
| 5 | QA, E2E, manual QA & evidence (13) | P0/P1 | backlog |
| 6 | Cloud, DevOps, reliability & release (10) | P1 | backlog |
| 7 | AI security & LLM systems (10) | P1 | backlog |
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
