# Claude Skills

This repository is the documentation home for product-agnostic Claude skills, operating patterns, and implementation guidance for software architecture, SaaS architecture, engineering, security, AI engineering, and QA.

## Current documents

- [`docs/prompts/senior-principal-claude-skills-execution-plan.md`](docs/prompts/senior-principal-claude-skills-execution-plan.md) — earlier senior principal execution plan combining prior chat requirements, uploaded v3 files, repo roadmap, and Claude skill guidance.
- [`docs/research/claude-skills-architecture-audit-findings-v4.md`](docs/research/claude-skills-architecture-audit-findings-v4.md) — senior principal Claude/AI architecture audit, recommendations, priority phases, and skill/agent design rules.
- [`docs/prompts/claude-skills-master-generation-prompts-v4.md`](docs/prompts/claude-skills-master-generation-prompts-v4.md) — phase-by-phase prompts for Claude Code to create reusable skills and agent/orchestrator prompts.
- [`docs/300-repeatable-software-saas-skills-roadmap.md`](docs/300-repeatable-software-saas-skills-roadmap.md) — product-agnostic 300-skill roadmap for repeatable software and SaaS architecture, engineering, security, AI engineering, and QA skills.
- [`docs/skills/`](docs/skills/) — category-level skill backlogs that break the 300 skills into focused engineering domains.
- [`docs/150-claude-skills-roadmap.md`](docs/150-claude-skills-roadmap.md) — superseded by the 300-skill roadmap and kept only as a redirect for older references.

## Priority order

1. Software architecture and engineering best practices
2. SaaS platform architecture and engineering
3. SaaS security engineering, especially tenant isolation and RLS
4. QA, validation, E2E, and test harness engineering
5. Backend, API, data, frontend, and UX engineering
6. DevOps, release, reliability, observability, and operational handoff
7. AI-era software development lifecycle and agent operating discipline
8. AI software engineering and LLM system design

## Skill implementation standard

Each future `.claude/skills/<skill-name>/SKILL.md` should be small, executable, repeatable, product-agnostic, and safe to reuse across multiple software and SaaS repositories.

## Recommended Claude Code starting point

Ask Claude Code to read:

```text
docs/research/claude-skills-architecture-audit-findings-v4.md
docs/prompts/claude-skills-master-generation-prompts-v4.md
```

Then run the Master Role Prompt and Phase 0 only. Do not generate all 300 skills in one pass.
