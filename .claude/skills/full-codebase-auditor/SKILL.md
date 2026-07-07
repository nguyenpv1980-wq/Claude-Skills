---
name: full-codebase-auditor
description: Audit an ENTIRE repository with inventory-first discipline — enumerate every directory, language, entry point, dependency manifest, CI/CD pipeline, and doc before forming any finding, so nothing is judged by its most interesting-looking files. Covers architecture, security, code quality, tests, dependencies, CI/CD, deployment, documentation, and operational readiness, and separates every result into confirmed findings, likely findings, hypotheses, and missing information. Use for whole-repo health checks, technical due diligence on an inherited or acquired codebase, "what state is this project actually in", or a pre-investment/pre-handover audit. Do NOT use for one diff (code-reviewer), one subsystem's strategic read (principal-code-analyst), or one live failure (systematic-debugger). Note: the full-codebase-auditor SUBAGENT composes this skill; the skill is the procedure.
---

# Full Codebase Auditor

## Purpose

Deliver a whole-repository audit whose coverage is provable: the inventory
comes first and every part of the repo is either examined or explicitly
listed as not-examined, so the audit's blind spots are in the report instead
of hidden. Epistemic honesty is the second pillar — every result is filed as
confirmed (verified evidence), likely (strong indirect evidence), hypothesis
(consistent with observations, unverified), or missing information (couldn't
check), and no category ever borrows the confidence of a stronger one.

## Use When

- Use when: asked what state a whole repository is in — inherited code,
  contractor handover, acquisition due diligence, long-unmaintained project.
- Use when: a periodic health audit is due across architecture, security,
  tests, dependencies, and operations at once.
- Use when: the `full-codebase-auditor` subagent needs its procedure — the
  agent composes this skill and returns its findings.
- Do NOT use when: one change needs review (`code-reviewer`), one subsystem
  needs a strategic read (`principal-code-analyst`), or one failure needs
  diagnosis (`systematic-debugger`).
- Do NOT use when: the real question is "audit our skills/docs repo's catalog
  integrity" — run the repo's own validator first; audit judgment is for what
  validators can't check.

## Inputs to Inspect

1. The complete tree: every top-level directory, file-type census, repo size,
   generated-vs-source areas (`git ls-files`, directory listing — not a
   stroll through interesting folders).
2. Every dependency manifest and lockfile, every CI/CD workflow, every
   Dockerfile/IaC file, every config and env template.
3. Entry points: services, CLIs, jobs, scheduled tasks — what actually runs.
4. Git history at repo scale: churn hotspots, contributor concentration,
   commit recency by area, large binaries.
5. Tests and their CI wiring: what runs on merge vs what merely exists.
6. Docs: README accuracy, setup instructions vs reality, ADRs, runbooks.

## Workflow

1. **Inventory before judgment.** Enumerate the tree, classify every
   top-level area (source, tests, config, generated, vendored, docs, infra,
   unknown), census languages and sizes, list entry points, manifests, CI
   pipelines. Publish this inventory as report section one — findings may
   only reference inventoried areas.
2. **Plan coverage against a budget.** Every area gets a depth: read-fully,
   sample (state the sampling rule, e.g. "3 largest + 3 highest-churn
   files"), or not-examined (with reason). No area is silently skipped.
3. **Audit per dimension, collecting evidence:**
   - *Architecture:* real component boundaries, dependency direction
     violations, shared-data coupling, doc-vs-code drift.
   - *Security:* secrets in history/config, authn/authz patterns at
     boundaries, input validation, dependency CVE exposure, dangerous
     defaults. (Repo-level review, not a pentest — say so.)
   - *Quality:* hotspot complexity × churn, duplication concentrations,
     dead/vendored drift, error-handling consistency.
   - *Tests:* what is pinned vs theater, coverage of money paths, CI
     enforcement gaps (tests that exist but never run).
   - *Dependencies:* staleness spread, unpinned ranges, abandoned packages,
     license flags.
   - *CI/CD & deployment:* what gates a merge, what deploys, rollback
     ability, environment/config handling.
   - *Docs & operations:* can a new engineer set it up; do runbooks exist
     for the failure modes the code implies.
4. **File every result into the four-tier scheme** — confirmed / likely /
   hypothesis / missing information — with evidence (file:line, command
   output, history stats) attached at the tier that evidence supports.
5. **Rank confirmed+likely findings** by severity and blast radius into a
   remediation roadmap: quick wins, structural fixes, investigations (which
   convert hypotheses into findings).
6. **Write the coverage statement:** examined fully / sampled (rule) /
   not examined (reason) — the audit's own audit trail.

## Output Format

```
CODEBASE AUDIT — <repo> @ <commit>
Executive summary: <≤6 sentences, state + top risks + recommended next steps>
1. Inventory: <tree areas + classification, languages, sizes, entry points,
   manifests, CI pipelines>
2. Coverage: <area → fully | sampled (rule) | not examined (reason)>
3. Findings by dimension (architecture, security, quality, tests,
   dependencies, CI/CD, deployment, docs, operations):
   [CONFIRMED] <finding> — evidence <anchor> — severity/blast radius
   [LIKELY]    <finding> — indirect evidence — what would confirm
   [HYPOTHESIS]<observation-consistent guess> — what would test it
4. Missing information: <what could not be checked and why it matters>
5. Remediation roadmap: <quick wins / structural / investigations, ranked>
```

## Validation Checklist

- [ ] Inventory section exists and precedes all findings; findings reference
      only inventoried areas.
- [ ] Every repo area appears in the coverage statement — none silently
      skipped.
- [ ] Sampling rules stated wherever sampling was used.
- [ ] Every finding carries its tier, and evidence matches the tier claimed
      (no hypothesis dressed as confirmed).
- [ ] Security results labeled as repo-level review, not penetration testing.
- [ ] Missing-information section present ("None" only if truly everything
      was checkable).
- [ ] Roadmap ranks by severity × blast radius, and names which
      investigations would upgrade hypotheses.
- [ ] Read-only throughout — the audit changes nothing.

## Gotchas

- The interesting-files trap is the defining failure: auditing what caught
  the eye and extrapolating. The inventory-first rule exists to kill it.
- The scariest areas are the ones that resist reading — generated blobs,
  vendored trees, 4k-line files. Budget-limited depth there is fine;
  UNLISTED depth-limiting is not.
- A test suite can be green and enforce nothing — check CI wiring and
  assertion quality, not the badge.
- Secrets live in git HISTORY after deletion from HEAD; scan history, and
  treat any found credential as live until rotation is confirmed.
- Monorepos hide whole projects in subdirectories with their own manifests
  and CI — the inventory census must catch them or the audit lies.
- Recency bias: last quarter's code reflects the current team; five-year-old
  load-bearing code reflects the actual risk.

## Stop Conditions

- The repo is too large to audit meaningfully in budget → stop after the
  inventory, propose a staged plan (inventory now, dimensions per pass), and
  let the human pick rather than delivering thin uniform coverage silently.
- A live, exploitable vulnerability or leaked credential is found →
  surface immediately via `human-approval-boundary`; report-writing never
  queues behind an active exposure.
- Audit would require executing untrusted code (builds, installs, hooks) →
  static-only unless the human approves a sandboxed run.
- The repo's identity/remote doesn't match what the audit was commissioned
  for → `agent-startup-context-gate` failure; stop before auditing the wrong
  codebase.

## Supporting Files

- [references/audit-inventory-checklist.md](references/audit-inventory-checklist.md) —
  the full inventory census procedure, coverage-planning table, per-dimension
  evidence checklists, and tier-assignment rules.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `code-reviewer`,
  `code-simplifier`, and `principal-code-analyst` (review/audit cluster).
