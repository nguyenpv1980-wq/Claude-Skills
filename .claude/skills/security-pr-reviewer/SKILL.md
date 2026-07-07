---
name: security-pr-reviewer
description: Security-focused review of an ACTUAL diff (PR, branch delta, or staged/working changes) — hunts authn/authz gaps, missing object-level and tenant-scope checks, injection, unsafe deserialization, secrets in code/config/logs, SSRF, mass assignment, and unsafe security-relevant changes introduced by the change. Reports severity-ranked findings, each with file:line evidence, an exploit path or abuse scenario for high-severity claims, and remediation; requires tenant-isolation and object-level authorization checks on SaaS data paths. Use when asked to security-review a PR/branch/commit or to gate a change on security before merge. Do NOT use for general code review (code-reviewer), design-time threat modeling (threat-modeler), dependency/CI supply-chain review (supply-chain-security-reviewer), migration safety (secure-migration-reviewer), or triaging scanner output (static-analysis-reviewer).
---

# Security PR Reviewer

## Purpose

Give a change a security verdict backed by evidence: severity-ranked findings
anchored to file:line in the real diff, each high-severity finding carrying an
exploit path or abuse scenario, and an approve / request-changes decision with
the blocking findings named. This is the security lens on a specific diff —
narrower and deeper on security than `code-reviewer`, but working on the same
artifact (an obtained diff), never on an imagined change. On SaaS data paths,
tenant isolation and object-level authorization are mandatory review dimensions,
checked whether or not the PR description mentions them.

## Use When

- Use when: asked to security-review a PR, branch-against-base, commit, or the
  current staged/working diff.
- Use when: gating a change on security before merge, or a change touches
  auth, data access, uploads, external calls, or config.
- Do NOT use when: the request is a general correctness/quality review — that
  is `code-reviewer` (this skill is the security-specialized pass).
- Do NOT use when: there is no diff yet and the ask is design-time threat
  enumeration — `threat-modeler`.
- Do NOT use when: the risk is dependency/CI supply chain —
  `supply-chain-security-reviewer`.
- Do NOT use when: the change is a database migration whose safety is the
  question — `secure-migration-reviewer`.
- Do NOT use when: the input is SAST/CodeQL/SARIF output to triage —
  `static-analysis-reviewer`.
- Never security-review from a description of a change: no diff, no review.

## Inputs to Inspect

1. The actual diff and its base: `gh pr diff <n>` / `git diff <base>...<branch>`
   / `git diff` + `git diff --staged`. Record which was reviewed. No diff →
   Stop Conditions.
2. The stated intent (PR description, linked issue) — but the review judges
   what the code does, not what the description claims.
3. Surrounding unchanged code of each hunk: the authz middleware the new route
   relies on, the query the new input flows into, the caller that sets scope —
   security bugs live in the contract between changed and unchanged code.
4. The security context: tenant model and authorization matrix for the data
   paths touched; existing validators/sanitizers the change should use.
5. New tests (or their absence) for the security-relevant behavior — a
   security fix without a negative test is unverified.

## Workflow

1. **Obtain the real diff** and base; note size and which files carry
   security weight (auth, data access, config, uploads, external calls).
2. **Map the change to boundaries.** For each hunk, identify the trust
   boundary it touches (client→server, tenant→tenant, server→DB, app→3rd
   party) and review against that boundary's threats.
3. **Authn/authz pass:** new/changed endpoints authenticated? Authorization
   checked at the RESOURCE (object-level), not just the route or UI? On SaaS
   data access, is tenant scope server-derived and applied to every query the
   diff adds? (mandatory rows — see Security Rules).
4. **Injection & input pass:** untrusted input reaching SQL/NoSQL/shell/
   template/deserialization; parameterization and contextual encoding present;
   mass assignment of restricted fields (role, tenant_id, owner_id, price).
5. **Secrets & config pass:** secrets added to code/config/logs; server
   secrets exposed to the client bundle; unsafe logging of tokens/PII; SSRF or
   open-redirect via new user-supplied URLs.
6. **Security-relevant change pass:** does the diff weaken an existing control
   (loosened policy, removed check, broadened CORS/permissions)? Flag any
   control removal explicitly.
7. **Rank and evidence findings.** Each finding: severity, file:line, and for
   HIGH+ a concrete exploit path or abuse scenario (persona → steps → payoff).
   No exploit path → cap at medium and label "needs verification".
8. **Judge test adequacy:** are the security behaviors pinned by tests that
   would fail if the control were reverted? Name the gaps.
9. **Deliver the verdict** (approve / approve-with-nits / request-changes)
   with blockers listed and what was NOT reviewed (generated files, areas out
   of the diff) so coverage is honest.

## Output Format

```
SECURITY PR REVIEW — <PR/branch/diff id> (base: <ref>, N files)
Reviewed diff via: <command>
Verdict: approve | approve-with-nits | request-changes
Boundaries touched: <client→server | tenant→tenant | server→DB | app→3rd party>
Findings (severity-ranked):
  [CRITICAL|HIGH] <file:line> — <vuln>; exploit: <persona → steps → payoff>; fix: <remediation>
  [MEDIUM|LOW]    <file:line> — <issue>; fix: <remediation>
SaaS checks: tenant scope <server-derived? applied to new queries?> | object-level authz <present?>
Control changes: <any existing control weakened/removed — explicit>
Tests: <security behaviors pinned? gaps — would a revert be caught?>
Not reviewed: <exclusions + why>
```

## Validation Checklist

- [ ] Reviewed an actual obtained diff; command recorded; no review from prose.
- [ ] Every hunk mapped to the trust boundary it touches.
- [ ] Object-level authorization and tenant-scope checks assessed on every
      SaaS data path the diff adds — even if the PR didn't mention them.
- [ ] Injection, mass-assignment, secrets, and SSRF/redirect passes done.
- [ ] Any weakening/removal of an existing control is flagged explicitly.
- [ ] Every HIGH+ finding has an exploit path/abuse scenario; path-less claims
      capped at medium and labeled.
- [ ] Test adequacy judged by "would a revert of the control be caught?".
- [ ] Verdict names blockers; not-reviewed list present.

## Security Rules

- No diff, no review — never infer a change's security from its description.
- HIGH/CRITICAL findings require an exploit path or abuse scenario
  (master-prompt §6); without one, rank medium and mark needs-verification.
- Tenant isolation and object-level authorization are mandatory review
  dimensions on SaaS data paths, not optional, regardless of the PR's stated
  scope.
- A change that weakens or removes a security control is a finding on its own,
  even if the new state still "works".
- Findings are never suppressed to unblock a merge; accepted risk needs the
  human's written rationale via `human-approval-boundary`.
- This skill reviews; it does not fix. Fixes are a separate change
  (`appsec-implementer`).

## Gotchas

- The vulnerability is often in the unchanged code the diff now reaches — a
  new caller feeding an old unparameterized query; review the contract, not
  the hunk alone.
- Authorization at the route or in the UI is not object-level authorization —
  the new endpoint may check "is a member" but not "owns THIS record".
- A diff that adds a second route to existing data (GraphQL beside REST) can
  bypass the isolation the first route enforced — check for parallel paths.
- Secrets slip in via config/test fixtures/log statements, not just source —
  scan the whole diff, including non-`src` files.
- A green CI run means existing tests pass, not that the new security behavior
  is tested — read the test diff, not the badge.
- Large or generated-heavy diffs induce rubber-stamping; say where scrutiny
  thinned rather than implying uniform coverage.

## Stop Conditions

- No diff can be obtained → stop; do not review from a verbal description.
- The diff changes security policy, RLS, or auth flows in ways whose
  implications are unclear → flag for human security review via
  `human-approval-boundary`; do not approve on inference.
- The security-relevant change is a DB migration or RLS policy → hand the
  policy/migration portion to `rls-policy-auditor` / `secure-migration-reviewer`.
- The finding is a dependency/CI supply-chain issue rather than app code →
  hand to `supply-chain-security-reviewer`.
- Asked to both review and silently fix in one pass → review first; fixes are
  a separate, explicitly-approved change.

## Supporting Files

- [references/security-review-passes.md](references/security-review-passes.md)
  — the per-pass checklists (authz, injection, secrets, control-change) with
  boundary-specific prompts and the exploit-path template for high-severity
  findings.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `secure-migration-reviewer`,
  `static-analysis-reviewer`, `supply-chain-security-reviewer`, and the shipped
  `code-reviewer` (security-review cluster).
