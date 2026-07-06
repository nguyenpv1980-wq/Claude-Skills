# DevOps, Release & Reliability Engineering

Operational skills for CI/CD, release, rollback, monitoring, incident response, and environments.

These are product-agnostic, repeatable Claude skills. They are meant to become executable `SKILL.md` workflows, not one-off prompts.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 236 | Branching Strategy Design | P1 | Define branch naming, protection, review, merge strategy, and release flow. |
| 237 | Pull Request Gate Design | P0 | Require checks, reviews, validation evidence, security approval, and clean diffs before merge. |
| 238 | CI Pipeline Architecture | P0 | Design lint, typecheck, build, unit, integration, security, E2E, and final gate stages. |
| 239 | CI Secret Governance | P0 | Control where secrets are available, how skipped-secret jobs behave, and how failures are reported. |
| 240 | Artifact Governance | P1 | Collect logs, reports, screenshots, coverage, build assets, and release artifacts safely. |
| 241 | Release Readiness Review | P0 | Assess scope, tests, migrations, monitoring, rollback, docs, and stakeholder approval before release. |
| 242 | Deployment Strategy Design | P1 | Choose rolling, blue/green, canary, feature-flagged, or manual deployment based on risk. |
| 243 | Rollback Strategy Design | P0 | Define code rollback, config rollback, migration rollback, data repair, and verification steps. |
| 244 | Environment Parity Review | P1 | Compare local, CI, staging, preview, and production environment behavior and config. |
| 245 | Infrastructure Drift Review | P1 | Detect differences between documented infra, IaC, platform settings, secrets, and actual runtime. |
| 246 | Runtime Configuration Validation | P1 | Validate required env vars, provider keys, URLs, modes, and feature flags at startup. |
| 247 | Health Check Design | P1 | Design liveness, readiness, dependency, queue, database, and integration health checks. |
| 248 | Monitoring and Alerting Design | P1 | Define actionable alerts with severity, owner, runbook, threshold, and noise control. |
| 249 | Incident Response Runbook | P1 | Document triage, containment, communication, rollback, evidence capture, and postmortem steps. |
| 250 | Postmortem Facilitation | P1 | Produce blameless incident analysis with timeline, root causes, fixes, owners, and prevention. |
| 251 | SLO and Error Budget Design | P2 | Define reliability targets, measurements, burn alerts, and release tradeoffs. |
| 252 | Log Taxonomy Design | P1 | Standardize log levels, event names, correlation IDs, redaction, and diagnostic fields. |
| 253 | Database Backup Verification | P0 | Verify backups exist, are nonzero, restorable, current, and outside unsafe commit paths. |
| 254 | Migration Deployment Runbook | P0 | Define target confirmation, backup, apply, verify, smoke, rollback, and documentation steps. |
| 255 | Scheduled Job Operations | P1 | Operate cron and background jobs with visibility, retries, alerts, locks, and manual rerun paths. |
| 256 | Dependency Upgrade Workflow | P1 | Upgrade packages with compatibility review, changelog scan, tests, rollback, and security context. |
| 257 | Build Reproducibility Review | P1 | Ensure builds are deterministic, lockfiles are respected, and generated outputs are controlled. |
| 258 | Containerization Review | P2 | Review Dockerfiles, layers, secrets, runtime user, health checks, and build context. |
| 259 | Developer Onboarding Runbook | P1 | Document local setup, tools, environment, scripts, validation, and troubleshooting. |
| 260 | Operational Handoff Report | P1 | Summarize what changed, how it runs, how to monitor, how to roll back, and known risks. |

## Skill implementation standard

When this category is converted into executable skills, each `SKILL.md` should include:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns / stop conditions
