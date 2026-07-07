# Pipeline Stages Reference

Detail file for `ci-pipeline-architect`. Loaded on demand.

## Canonical stage catalog

| Stage | Default trigger | Default blocking | Defect class caught | Notes |
| --- | --- | --- | --- | --- |
| Lint/format | PR | merge-blocking | style drift, obvious errors | seconds; run first |
| Typecheck | PR | merge-blocking | type contract breaks | parallel with lint |
| Build (once) | PR | merge-blocking | compilation/bundling breaks | artifact reused downstream |
| Unit/component | PR | merge-blocking | logic regressions | tier per `qa-automation-architect` |
| Integration | PR | merge-blocking | wiring/boundary breaks | containerized deps |
| Secret scan | PR | merge-blocking | committed credentials | block early, before human review |
| SAST | PR or merge | merge-blocking once triaged | injection/authz classes | triage per `static-analysis-reviewer`; untriaged = advisory first |
| Dependency scan | PR + scheduled | advisory → blocking by policy | vulnerable/hijacked deps | discipline per `supply-chain-security-reviewer` |
| Build-output QA | PR or merge | per policy | secret-in-bundle, parity | `vite-build-qa-engineer` for Vite estates |
| E2E (smoke tier) | merge | merge-blocking on main | critical-journey breaks | full E2E nightly per tier policy |
| Artifact package + provenance | merge | blocking for deploy | untraceable deploys | commit + run id stamped |
| Deploy to staging | merge/manual | — | — | env-scoped secrets |
| Promote to production | manual | approval-gated | — | named human approvers |

## Secret-governance patterns

- **OIDC federation**: CI job → short-lived cloud role assumption; no
  stored cloud keys. Role scoped per environment and per repo/branch claim.
- **Job→secret map**: every secret lists the jobs that may see it; deploy
  secrets never available to test jobs; nothing secret-bearing on
  fork-PR-triggered runs.
- **Untrusted-code isolation**: steps executing PR code or package install
  scripts run in jobs WITHOUT secrets; artifacts pass between jobs, secrets
  do not.
- **Missing-secret behavior**: skip the dependent step with a visible
  "SKIPPED: missing <name>" report line — never a green pass that ran
  nothing.
- **Cache trust**: separate cache namespaces for privileged vs
  PR-triggered runs; lockfile-keyed.

## Deployment strategy → rollback primitive

| Strategy | Rollback primitive | Use when |
| --- | --- | --- |
| Rolling | redeploy previous artifact | default; stateless services |
| Blue/green | traffic flip back to old color | instant backout needed; cost of double capacity accepted |
| Canary | abort ramp, route 100% to stable | high-risk changes with good SLI signal (`slo-reliability-architect`) |
| Flag-gated | kill switch flips flag off | decouple deploy from release; UI/behavioral changes |

Every environment's chosen strategy and primitive feeds
`rollback-runbook-author` — a strategy without a rehearsed primitive is a
diagram, not a rollback path.

## Branch-protection alignment checklist

- [ ] Required-check names exactly match current merge-blocking job names.
- [ ] No orphaned required checks (renamed/deleted jobs still "required").
- [ ] Bypass actors limited to the governed list (`agent-authorization-matrix`).
- [ ] Force-push and deletion blocked on protected branches.
- [ ] Auto-merge posture per repo governance (arming is a human act).
