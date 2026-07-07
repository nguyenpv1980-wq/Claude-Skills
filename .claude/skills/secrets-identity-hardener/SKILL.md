---
name: secrets-identity-hardener
description: Harden how an application handles secrets and identity — move hardcoded credentials/tokens/keys into a secret manager or server-only env, classify each variable as public vs server-only (and catch client-bundle exposure like VITE_/NEXT_PUBLIC_ leaks), enforce least-privilege service accounts, add rotation and revocation, and tighten session/token handling (expiry, refresh, storage flags) — with tests proving a secret is unreachable from the client and a rotated credential is honored. Use when secrets are hardcoded/committed, env classification is unclear, a key needs rotation, or service accounts are over-privileged. Side-effecting and manual-only. Do NOT use to implement one app-layer control (appsec-implementer), audit RLS/service-role in the DB (rls-policy-auditor), or model threats (threat-modeler).
disable-model-invocation: true
---

# Secrets & Identity Hardener

## Purpose

Move an application from "secrets are wherever they landed" to a defensible
posture: every secret lives in a secret manager or server-only environment,
every environment variable is classified public vs server-only, client bundles
provably contain no server secret, service accounts hold least privilege, and
credentials rotate and can be revoked. The deliverable is a scoped set of code/
config changes plus evidence — a test or build check proving the secret is not
in the client bundle, and that a rotated credential is honored — not a promise.
This skill changes code and config, so it is manual-only and gates production
changes through human approval.

## Use When

- Use when: secrets are hardcoded in source, committed to the repo, or present
  in the client bundle.
- Use when: environment-variable classification is unclear — which vars are
  safe to ship to the browser, which are server-only, CI-only, or deploy-only.
- Use when: a credential must be rotated or revoked, or a service account is
  over-privileged.
- Use when: session/token handling needs tightening (expiry, refresh,
  storage flags, revocation).
- Do NOT use when: the task is one specific app-layer control (validation,
  encoding, an authz check) — that is `appsec-implementer`.
- Do NOT use when: the concern is database service-role/RLS leakage — that is
  `rls-policy-auditor`.
- Do NOT use when: you are enumerating threats or deciding what to protect —
  `threat-modeler`.
- Do NOT use when: only asked to REVIEW a diff for secret leaks — that is
  `security-pr-reviewer`; this skill remediates.

## Inputs to Inspect

1. Where secrets currently live: source files, committed `.env`, config,
   CI/CD variables, IaC, container images. Find them before moving them.
2. The client build config: bundler env-exposure rules (`VITE_`,
   `NEXT_PUBLIC_`, `REACT_APP_`, etc.) and what actually ends up in the
   shipped bundle. A prefix convention is not proof — inspect the build output.
3. The secret manager / platform available (cloud secret store, KMS, vault,
   deployment secrets) and how the app loads from it at runtime.
4. Service accounts and their grants: what each machine identity can do vs
   what it needs (least privilege).
5. Session/token handling: token type, storage (cookie vs localStorage),
   flags, expiry, refresh, revocation path.
6. Git history for committed secrets (a rotated secret is safe; a
   still-valid committed secret needs rotation, not just deletion).

## Workflow

1. **Inventory and classify.** List every secret and env var; classify each:
   public (safe for client), server-only, CI-only, deploy-only. Anything
   server-only currently reachable by the client is a finding to fix.
2. **Classify the change** (`change-classification-gate`); rotating live
   credentials, editing production config, or touching deploy secrets crosses
   `human-approval-boundary` — get approval before those steps.
3. **Write the proving check first** where feasible: a test or build assertion
   that the server-only secret does NOT appear in the client bundle / is not
   readable from the browser. Confirm it FAILS against the current exposed
   state (the leak is real) before fixing.
4. **Remediate storage:** move hardcoded/committed secrets into the secret
   manager or server-only env; load at runtime server-side; replace client
   references to server secrets with a server-side proxy/endpoint.
5. **Rotate what leaked.** A secret that was committed or client-exposed is
   compromised — rotate it (with approval), don't just relocate it. Deleting
   it from source without rotation leaves a live credential in git history.
6. **Least-privilege service accounts:** narrow grants to what's needed;
   record what was removed and why.
7. **Tighten sessions/tokens** if in scope: `HttpOnly`/`Secure`/`SameSite`
   cookies, sane expiry, working refresh, server-side revocation; add tests.
8. **Prove it.** Rerun the bundle/exposure check to green; verify a rotated
   credential is honored and the old one rejected (where testable). Record
   real commands and output.
9. **Stage exactly the intended files** (`reviewable-diff-discipline`) and
   report: what moved, what rotated, residual exposure (e.g. history needing
   BFG/rotation), and follow-ups. Never print the secret values themselves.

## Output Format

```
SECRETS & IDENTITY HARDENING — <app/scope>
Env classification: <var — public | server-only | CI-only | deploy-only>
Exposed secrets found: <name/location — how exposed> (values NOT printed)
Change class: <class> — approval: <path / obtained?>
Bundle-exposure check (red→green): <cmd> — before: FAIL, after: PASS
Remediation: <secret — moved to <store>, loaded <how>, client uses <proxy>>
Rotations: <credential — rotated? (approval) | rotation still required>
Service accounts: <identity — grants removed → least privilege>
Session/token changes: <flags/expiry/revocation added + tests>
Residual risk: <git history, secrets not yet rotated, out-of-scope stores>
Files changed: <exact paths>
Handoff: security-pr-reviewer to verify; ops to complete rotations if pending.
```

## Validation Checklist

- [ ] Every secret and env var classified; client-reachable server secrets
      identified.
- [ ] Client bundle inspected (not just prefix convention) and a check proves
      no server secret ships to the browser.
- [ ] Committed/exposed secrets are ROTATED, not merely deleted from source.
- [ ] Service accounts reduced to least privilege with removals recorded.
- [ ] Session/token hardening (if in scope) has flags, expiry, revocation,
      and tests.
- [ ] Proving checks run red before and green after; real output recorded.
- [ ] No secret values printed in output, logs, or tests.
- [ ] Staged set equals the intended footprint; production changes approved.

## Security Rules

- A secret that was ever committed or shipped to a client is compromised and
  must be rotated — relocation alone does not restore secrecy.
- Server-only secrets must be provably absent from the client bundle; a
  naming convention (`VITE_`/`NEXT_PUBLIC_`) is a rule, not evidence — verify
  the built artifact.
- Never print, log, echo, or commit secret VALUES; operate on names and
  locations. Tests assert on absence/behavior, not on the secret's content.
- Rotating live credentials, editing production config, or changing deploy
  secrets requires explicit human approval (`human-approval-boundary`).
- Least privilege is the default for machine identities; broad grants require
  written justification.

## Gotchas

- Deleting a hardcoded key from source but not rotating it leaves it live in
  git history — the fix is rotation, and history rewrite is a separate,
  approval-gated action.
- Bundler prefix rules are opt-in exposure: a var without the public prefix is
  hidden, but a server secret accidentally given the prefix ships to every
  browser — inspect the bundle.
- Moving a secret to an env var that the frontend build still inlines just
  relocates the leak; confirm the runtime read is server-side.
- Rotating a shared credential can break other consumers — enumerate who uses
  it before rotating, and coordinate; this is why rotation is approval-gated.
- localStorage-stored tokens are readable by any XSS; moving to HttpOnly
  cookies changes CSRF posture — harden both together, not one in isolation.

## Stop Conditions

- Rotating a live credential, editing production config, or rewriting git
  history to purge a secret → stop for explicit approval
  (`human-approval-boundary`); these are irreversible or broadly impactful.
- The only safe fix requires an ops action outside the repo (rotate a cloud
  key, revoke a token in a provider console) → stop and hand off with exact
  steps; do not fake completion.
- A secret is exposed in a way that is actively exploitable in production →
  report immediately; containment/rotation priority is the human's call.
- The task expands into database service-role/RLS scope → hand to
  `rls-policy-auditor`; into a single app control → `appsec-implementer`.

## Supporting Files

- [references/secret-classification-and-rotation.md](references/secret-classification-and-rotation.md)
  — the env-classification rubric, client-bundle exposure checks per bundler,
  rotation procedure, and least-privilege service-account patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `appsec-implementer`,
  `threat-modeler`, and `security-pr-reviewer`.
