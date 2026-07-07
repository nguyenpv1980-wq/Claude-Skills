---
name: supply-chain-security-reviewer
description: Review software supply-chain risk with SLSA-style provenance thinking — dependencies (known CVEs triaged by reachability, not just presence), lockfile integrity and pinning, transitive/typosquat/confusion risk, install and build scripts, CI/CD workflows (untrusted PR triggers, secret exposure, over-broad token scopes, unpinned third-party Actions), artifact provenance, and postinstall/hook execution. Extends to the AI/ML supply chain (LLM03): third-party models, datasets, and fine-tuning adapters. Produces severity-ranked findings each with a compromise path, an exploitability verdict, and concrete remediation (pin, upgrade, remove, isolate). Use when reviewing dependencies, lockfiles, CI workflows, a build pipeline, a dependency bump, or an acquired model/dataset/adapter for supply-chain risk. Do NOT use to triage SAST/CodeQL findings in first-party code (static-analysis-reviewer), review app logic in a diff (security-pr-reviewer), or model feature threats (threat-modeler).
---

# Supply-Chain Security Reviewer

## Purpose

Assess whether an attacker can compromise the software through what it
depends on and how it is built — not just whether a scanner printed CVEs. The
review applies SLSA-style provenance thinking to dependencies, lockfiles,
install/build scripts, CI/CD workflows, and artifacts, and reports
severity-ranked findings where each carries a compromise path (how an attacker
gets from the weakness to code execution or secret theft), an exploitability
verdict (reachable/exploitable vs latent), and a concrete remediation. A CVE
in a package that is never called on a reachable path is triaged as such, not
treated as an automatic critical; a `postinstall` script pulling a remote blob
is a finding whether or not a scanner flagged it.

## Use When

- Use when: reviewing dependencies / lockfiles / a dependency bump for
  supply-chain risk.
- Use when: reviewing CI/CD workflows, GitHub Actions, or a build pipeline for
  compromise paths (untrusted triggers, secret exposure, token scope, unpinned
  actions).
- Use when: install/build scripts, postinstall hooks, or vendored artifacts
  need a trust review.
- Use when: a scanner (Dependabot, `npm audit`, Snyk, Trivy) produced output
  that needs triage into what actually matters.
- Use when: acquiring an AI/ML artifact — a third-party base model, a
  downloaded dataset, or a fine-tuning adapter — and its provenance, format
  safety, and pinning need a supply-chain review (OWASP LLM03).
- Do NOT use when: reviewing the integrity of training data YOU collect or
  pipelines YOU run (feedback loops, RAG ingestion) — that is
  `model-poisoning-reviewer` (acquire-vs-ingest is the split).
- Do NOT use when: triaging SAST/CodeQL findings in FIRST-PARTY code — that is
  `static-analysis-reviewer` (dependency-vs-own-code is the split).
- Do NOT use when: reviewing application logic in a diff —
  `security-pr-reviewer`.
- Do NOT use when: modeling feature-level threats — `threat-modeler`.

## Inputs to Inspect

1. Manifests and lockfiles: `package.json`/`package-lock.json`/`pnpm-lock`/
   `yarn.lock`, `requirements.txt`/`poetry.lock`, `go.mod`/`go.sum`, etc. —
   the lockfile is the source of truth for what actually installs.
2. Scanner output if provided (Dependabot/`npm audit`/Snyk/Trivy/OSV) — input
   to triage, never the final verdict.
3. CI/CD workflows: `.github/workflows/*`, pipeline configs — triggers,
   permissions/token scopes, third-party actions and their pinning, where
   secrets are exposed, and whether untrusted PRs reach privileged jobs.
4. Install/build scripts: `postinstall`/`preinstall`/`prepare` hooks, build
   scripts, Makefiles, Dockerfiles — anything that executes during install or
   build, especially remote fetches.
5. Dependency metadata for risk signals: maintenance status, sudden
   maintainer changes, typosquat/confusion candidates, direct vs transitive.
6. Artifact/provenance signals: are builds reproducible, signed, attested;
   are vendored binaries checked in without provenance.
7. AI/ML artifacts if any (LLM03): third-party base models, downloaded
   datasets, and fine-tuning adapters — their source/registry, revision
   pinning (a mutable tag/`latest` is not pinned), serialization format
   (pickle/`torch.load` execute code on load; prefer safetensors), and
   license/provenance. Acquisition only — integrity of data you curate or
   pipelines you run is `model-poisoning-reviewer`.

## Workflow

1. **Establish what actually ships/builds.** Read the lockfile (not just the
   manifest) for the real dependency set; identify direct vs transitive. No
   manifest/lockfile or pipeline to review → Stop Conditions.
2. **Triage scanner output** (if any) by reachability: for each flagged CVE,
   is the vulnerable code path called by this project? Sort into
   true-positive-reachable, true-positive-latent, false-positive, duplicate.
   Presence ≠ exploitability.
3. **Review install/build execution:** enumerate scripts that run on install
   or build; flag remote downloads, curl-to-shell, obfuscated steps,
   credential access. These execute with developer/CI privileges.
4. **Review CI/CD for compromise paths** using
   [references/supply-chain-checklist.md](references/supply-chain-checklist.md):
   untrusted trigger reaching secrets (e.g. `pull_request_target` +
   checkout of PR code + secret use), over-broad `GITHUB_TOKEN`/permissions,
   unpinned third-party actions (tag vs commit SHA), cache poisoning, and
   artifact upload/download trust.
5. **Assess dependency-specific risk:** typosquatting, dependency confusion
   (internal name resolvable from a public registry), abandoned/maintainer-
   changed packages, and unnecessary heavy/native deps that widen the surface.
6. **Check integrity and provenance:** lockfile committed and pinned; hashes/
   integrity present; vendored artifacts have a documented source; releases
   signed/attested where the ecosystem supports it (SLSA levels as a frame).
   For **AI/ML artifacts (LLM03)** — third-party models, datasets, adapters —
   see [references/supply-chain-checklist.md](references/supply-chain-checklist.md):
   pin to an immutable revision/digest (not a mutable tag or `latest`), prefer
   safetensors over pickle/`torch.load` formats that execute code on load,
   confirm the source registry and license, and treat a downloaded artifact as
   untrusted until its provenance checks out. Integrity of data you curate or
   pipelines you run stays with `model-poisoning-reviewer`.
7. **Rank findings** with a compromise path and exploitability verdict.
   High severity REQUIRES a path from the weakness to code execution/secret
   theft; a reachable exploit or a plausible install-time execution qualifies,
   a latent unreachable CVE does not.
8. **Remediate concretely:** pin (to SHA/version+hash), upgrade (state the
   safe version), remove, or isolate (least-privilege token, split trusted/
   untrusted jobs). Note accepted risk only with written rationale.

## Output Format

```
SUPPLY-CHAIN REVIEW — <repo/scope>
Dependency set: <direct N / transitive M — from lockfile>
Scanner triage: reachable-TP <n> | latent-TP <n> | false-positive <n> | dup <n>
Findings (severity-ranked):
  [CRITICAL|HIGH|MEDIUM|LOW] <area: dep / script / CI / artifact>
    Compromise path: <weakness → attacker action → code exec / secret theft>
    Exploitability: <reachable/exploitable | install-time | latent>
    Remediation: <pin SHA / upgrade to <v> / remove / isolate / split job>
Install/build execution: <scripts that run + risk>
CI/CD posture: <triggers, token scope, action pinning, secret exposure>
Provenance: <lockfile pinned? integrity hashes? signing/attestation? SLSA frame>
Accepted risk: <finding — written rationale>
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] Lockfile (not just manifest) used to determine the real dependency set.
- [ ] Scanner findings triaged by reachability into TP-reachable / TP-latent /
      FP / duplicate — none accepted at face value.
- [ ] Install/build scripts and postinstall hooks reviewed for remote fetch
      and privileged execution.
- [ ] CI/CD reviewed for untrusted-trigger-to-secret paths, token scope, and
      third-party action pinning (SHA vs tag).
- [ ] Typosquat/confusion/abandonment risk considered for notable deps.
- [ ] Every HIGH+ finding has a compromise path AND an exploitability verdict.
- [ ] Remediations are concrete (pin/upgrade/remove/isolate), not "update deps".
- [ ] AI/ML artifacts (if any) reviewed for revision pinning, safe
      serialization (safetensors vs pickle/`torch.load`), source, and license;
      curated-data/pipeline integrity routed to `model-poisoning-reviewer`.
- [ ] Accepted risk carries written rationale; not-reviewed list present.

## Security Rules

- Scanner output is input, not truth (master-prompt §6): a CVE is triaged by
  reachability and exploitability before it gets a severity.
- High-severity claims require a compromise path to code execution or secret
  theft; "a CVE exists" without a reachable/exploitable path is not high.
- Unpinned third-party CI actions (mutable tags) are a finding — pin to a
  full commit SHA.
- `pull_request_target`/privileged workflows that check out and run untrusted
  PR code while secrets are available are treated as critical unless proven
  isolated.
- Findings are not suppressed without written rationale via
  `human-approval-boundary`; upgrades that only relocate risk are labeled, not
  claimed as fixes.

## Gotchas

- `npm audit`/Dependabot severity is CVSS-based and context-blind — a
  "critical" in a dev-only or unreachable transitive dep may be noise, while a
  "moderate" on a reachable parser may be the real risk. Triage by reachability.
- The dangerous code often runs at INSTALL time (postinstall) or BUILD time,
  before any test — a scanner scoped to runtime deps misses it.
- Pinning to a version tag is not pinning: tags are mutable; only a commit SHA
  (for actions) or version+integrity-hash (for packages) is fixed.
- Dependency confusion: an internal package name that also resolves on a
  public registry lets an attacker publish a higher version and win — check
  scoping/registry config, not just the lockfile.
- A green Dependabot dashboard says nothing about install scripts, CI token
  scope, or unpinned actions — those are not "vulnerabilities" it scans for.
- Bumping a dependency to clear a CVE can pull a new maintainer's compromised
  release — review the upgrade target, don't just accept "latest".
- AI model formats execute code: loading a pickle-based checkpoint (`torch.load`,
  `pickle.load`, some `.bin`/`.pt`/`.ckpt`) runs arbitrary code on load — a
  "downloaded model" is a "run this file". Prefer safetensors; treat pickle
  artifacts from untrusted sources as install-time RCE.
- A model/dataset pinned to a mutable hub tag or `latest` is not pinned — the
  remote can change under you; pin to an immutable revision/commit/digest.

## Stop Conditions

- No manifest, lockfile, or pipeline is available to review → stop; this
  skill does not assess supply chain from a description.
- A finding indicates an ACTIVE compromise (malicious package already
  installed, secret already exfiltrated via CI) → report immediately with the
  path; containment/rotation is the human's call (`human-approval-boundary`).
- Remediation requires applying a dependency upgrade or editing CI on a live
  repo with breaking potential → propose the change; applying it is a
  separate, classified, approved step (not done from this review skill).
- The finding is in first-party code flagged by SAST, not a dependency/CI
  issue → hand to `static-analysis-reviewer`.

## Supporting Files

- [references/supply-chain-checklist.md](references/supply-chain-checklist.md)
  — the CI/CD compromise-path catalog, reachability-triage rubric, pinning
  and provenance checks, and dependency-confusion/typosquat detection notes.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `static-analysis-reviewer`,
  `security-pr-reviewer`, and `secure-migration-reviewer` (security-review
  cluster).
