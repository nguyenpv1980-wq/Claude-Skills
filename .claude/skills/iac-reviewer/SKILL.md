---
name: iac-reviewer
description: 'Review infrastructure-as-code changes (Terraform, Bicep, CloudFormation, CDK, Pulumi) for deploy safety and security posture — destructive operations hiding in innocent diffs (replace/delete of stateful resources), state/backend safety, public exposure, over-broad IAM/RBAC widening, missing encryption, secrets in code or captured in state, tenant-isolation impact, drift from documented architecture, module pinning, and tagging/cost impact. Review-only: severity-ranked findings with file:line evidence and proposed corrections — never runs apply, never executes plan against live backends; provided plan output is input. Use when asked to review an IaC PR or diff, check whether an infra change is safe to apply, audit IaC for misconfiguration, or investigate drift. Do NOT use for database migrations (secure-migration-reviewer), cloud design (azure-saas-architect / aws-saas-architect), pipeline design (ci-pipeline-architect), or applying changes.'
---

# IaC Reviewer

## Purpose

Produce a deploy-safety and security review of an infrastructure-as-code
change: severity-ranked findings with file:line evidence, the blast radius
of the diff (what gets destroyed, replaced, or exposed), and proposed
corrections — without ever applying anything. The discipline is
blast-radius-before-style: the first questions are "what does this destroy
or replace" and "what does this expose", asked against the actual resource
graph, not the diff's cosmetic size. A one-line attribute change that
forces a stateful resource replacement is a data-loss event wearing a
trivial diff.

## Use When

- Use when: asked to review a Terraform/Bicep/CloudFormation/CDK/Pulumi PR
  or diff before it is applied.
- Use when: asked whether an infrastructure change is safe, what it will
  destroy/replace, or what it exposes.
- Use when: auditing existing IaC for security misconfiguration — public
  exposure, IAM width, encryption, secrets, tagging.
- Use when: investigating suspected drift between IaC, documented
  architecture, and actual runtime state.
- Do NOT use when: the change is a database schema migration —
  `secure-migration-reviewer` (DDL/DML deploy safety is its territory;
  this skill owns the infrastructure the database runs on).
- Do NOT use when: designing the architecture the IaC should express —
  `azure-saas-architect` / `aws-saas-architect` / `cloud-architecture-decider`.
- Do NOT use when: designing or editing CI/CD pipelines —
  `ci-pipeline-architect` (even though pipelines often run IaC).
- Do NOT use when: the request is to APPLY the change — applying is a
  human-gated operation outside this skill.

## Inputs to Inspect

1. The actual IaC diff (PR or working tree) — no diff, no review.
2. Plan/what-if output if the human provides it (treated as INPUT — this
   skill does not execute plan against live backends itself; plan execution
   touches state and cloud APIs and stays with the human/pipeline).
3. The surrounding module/resource definitions the diff touches — a diff
   line's meaning lives in its resource block and its references.
4. State/backend configuration: where state lives, locking, encryption,
   who can read it (state files contain secrets and resource details).
5. The documented architecture and tenancy model (`azure-saas-architect` /
   `aws-saas-architect` output, ADRs) — the reference point for drift and
   isolation impact.
6. Provider/module version pins (lockfiles, version constraints) and the
   registry sources modules come from.
7. The tagging standard and environment layout the repo claims to follow.

## Workflow

1. **Establish blast radius first**: walk the diff for operations that
   destroy or replace stateful resources — renames without state moves,
   immutable-attribute changes forcing replacement, count/for_each keying
   changes reindexing resources, deletions. For each: the resource, the
   data it holds, and whether the change is survivable. Plan output, when
   provided, is cross-checked against this reading — a plan the human did
   not provide is requested, not simulated.
2. **Hunt public exposure**: security groups/firewall rules widening to
   0.0.0.0/0 or broad CIDRs, storage buckets/containers going public,
   public IPs on data stores, disabled private-endpoint enforcement,
   ingress objects exposing internal services. Every exposure finding
   names the resource and the reachable surface.
3. **Review identity and access width**: IAM/RBAC policies widening
   (wildcards in actions/resources/principals), role-assumption trust
   changes, service accounts gaining scopes, cross-account/cross-tenant
   grants. Width findings cite the before/after delta, not just the after.
4. **Check encryption and secrets**: encryption disabled or defaulted off
   on new stores, secrets/credentials literal in IaC source or template
   parameters, values that will be captured in state (many provider
   resources store secrets in state — flag where the design should use a
   secret store reference instead), key-management changes.
5. **Assess tenant-isolation impact**: shared-infrastructure changes that
   collapse isolation the architecture promises — per-tenant resources
   becoming shared, network boundaries between tenant tiers removed,
   tenant-scoped IAM conditions loosened. Route mechanism-level questions
   to `tenant-isolation-reviewer` when the finding is systemic.
6. **Check drift and hygiene**: does the diff match the documented
   architecture (undocumented new dependencies = drift or doc rot —
   `source-of-truth-reconciler` when contested); module/provider pinning
   (unpinned = supply-chain surface — compose
   `supply-chain-security-reviewer` for registry-source risk), module
   duplication, dead resources, tagging compliance of new resources and
   the cost visibility lost when absent.
7. **Estimate cost impact of the diff**: new always-on resources, sizing
   changes, cross-region/egress-generating paths, log/telemetry volume
   changes — order-of-magnitude flags feeding `saas-cost-architect`, not
   invented prices.
8. **File findings and corrections**: severity-ranked (blocker / high /
   medium / low) with file:line, the failure scenario, and a proposed
   corrected snippet per finding where correction is unambiguous. State
   what was NOT reviewed (files, modules, or runtime state out of reach).

## Output Format

```
IAC REVIEW — <PR/diff identifier>
Blast radius: <destroy/replace/reindex operations — resource, data at risk,
  survivable? — or "none detected">
Findings (severity-ranked, file:line each):
  <BLOCKER/HIGH/MED/LOW — resource — what fails/exposes — evidence —
   proposed correction>
Tenant-isolation impact: <collapsed/preserved boundaries, or n/a + why>
Drift notes: <IaC vs documented architecture mismatches>
Cost flags: <order-of-magnitude impacts, attribution/tagging gaps>
Apply-safety verdict: <safe to apply / safe with corrections / do not apply
  — one-line reason>
Not reviewed: <what this review could not see (state, runtime, modules)>
```

## Validation Checklist

- [ ] Blast radius was established before style/hygiene findings; every
      destroy/replace of a stateful resource is called out.
- [ ] Every finding carries file:line evidence and a concrete failure or
      exposure scenario — no vibes-based severity.
- [ ] IAM/RBAC findings show the before/after width delta.
- [ ] Secrets checked in source AND as state-capture risk.
- [ ] Tenant-isolation impact explicitly assessed (or explicitly n/a).
- [ ] Nothing was applied, no plan was executed against a live backend,
      and no cloud state was mutated by this review.
- [ ] The not-reviewed list is honest — unseen modules/state are named,
      not silently assumed fine.
- [ ] DB schema migrations found in the diff were routed to
      `secure-migration-reviewer`, not reviewed here.

## Gotchas

- Resource renames without a state move (`moved` blocks / state mv) read
  as delete+create — the most common accidental-destroy pattern in review.
- for_each/count key changes reindex collections: the diff looks like an
  addition but the plan destroys and recreates siblings.
- "Temporary" 0.0.0.0/0 rules and public-access flags ship far more often
  than they are removed; treat every widening as permanent unless the diff
  contains its own expiry mechanism.
- Default values do heavy lifting: a module upgrade that changes a default
  (encryption, public access, deletion protection) alters resources with
  zero diff lines in the caller — check module version bumps for default
  changes.
- Plan output is environment-specific: a clean plan against staging says
  nothing about production state; name which environment the evidence
  covers.
- CDK/Pulumi reviews need the synthesized output when logic is dynamic —
  reviewing only the program code misses what loops and conditions
  actually emit.

## Stop Conditions

- No actual diff or IaC source is available → no review; ask for the
  change, do not review from a verbal description.
- The change's safety hinges on live state or plan output that is not
  provided → request it from the human; do not execute plan/what-if
  against live backends or guess state contents.
- The diff intends destruction of stateful production resources (even
  legitimately) → findings + `human-approval-boundary`; destruction is
  never waved through as review-approved.
- Asked to apply, fix-and-apply, or "just make it safe and ship it" →
  stop at proposed corrections; applying is outside this skill.

## Supporting Files

- `references/iac-review-checklist.md` — per-category checklists
  (blast radius, exposure, IAM width, secrets/state, hygiene) and
  tool-specific sharp edges (Terraform/Bicep/CloudFormation/CDK).
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the cloud cluster
  (`cloud-architecture-decider`, `azure-saas-architect`,
  `aws-saas-architect`) and against shipped `secure-migration-reviewer` /
  `supply-chain-security-reviewer` / `security-pr-reviewer`.
