---
name: appsec-implementer
description: Implement a specific, already-decided application-security control in code — input validation at a boundary, output encoding, parameterized queries, authorization checks on a resource, secure session/cookie flags, safe file handling, SSRF/redirect allowlists, or a security fix for a known finding — test-first, with the control proven by a failing-then-passing negative test and no scope creep. Use when a threat model, security review, or the user has NAMED the control to build and you are editing the codebase to add it. Side-effecting and manual-only. Do NOT use to decide WHICH controls are needed (threat-modeler), review a diff (security-pr-reviewer), harden secrets/identity broadly (secrets-identity-hardener), or author RLS policies (rls-policy-auditor).
disable-model-invocation: true
---

# AppSec Implementer

## Purpose

Turn a named security control into a small, tested, reviewable code change.
The control is proven by a negative test that fails before the change and
passes after — an assertion that the abuse case is now denied — not by
"looks secure now". The deliverable is a scoped diff plus the test evidence
(commands run and their real output), touching only the files the control
requires. This skill builds one decided control at a time; it does not decide
what to build and it does not opportunistically refactor.

## Use When

- Use when: a threat model, `security-pr-reviewer` finding, or the user has
  NAMED the control — "add server-side authorization to this endpoint",
  "parameterize this query", "validate and length-cap this input", "set
  HttpOnly/Secure/SameSite on the session cookie", "allowlist the redirect
  target".
- Use when: fixing a specific known vulnerability with a regression test that
  pins the fix.
- Do NOT use when: it is not yet decided which controls are needed — run
  `threat-modeler` first; implementing undecided controls is guessing.
- Do NOT use when: reviewing a diff for security — `security-pr-reviewer`.
- Do NOT use when: the work is broad secrets/identity hardening across the
  app — `secrets-identity-hardener`.
- Do NOT use when: the control is a database RLS policy — author/audit via
  `rls-policy-auditor`.
- Do NOT use when: the ask is a sweeping "make the app secure" — that is not
  one control; decompose it via `threat-modeler` first.

## Inputs to Inspect

1. The control specification: the exact threat/finding it closes, from
   `threat-modeler`, `security-pr-reviewer`, or the user's request. No named
   control → Stop Conditions.
2. The code at the boundary being hardened: the handler, query, template,
   session config, or file path involved — and its callers.
3. The project's existing security utilities: validators, sanitizers, the ORM
   / query builder, the auth/session middleware — reuse them; do not
   hand-roll crypto or a second validation layer.
4. The test suite and its runner: where security/negative tests live and how
   they run, so the new test fits the project's conventions.
5. Framework/library versions (via lockfile) for the security API being used
   — behavior differs across versions; consult `docs-first-implementer`
   discipline rather than assuming an API exists.

## Workflow

1. **Confirm the control is decided and singular.** Restate the one control
   and the abuse case it closes. If undecided or plural, stop and route to
   `threat-modeler`.
2. **Classify the change** (`change-classification-gate`) and confirm the
   approval path — security-control code changes need review; production
   config/secret changes cross `human-approval-boundary`.
3. **Write the negative test first.** Encode the abuse case as a test that
   attempts the forbidden action and asserts denial/failure. Run it; confirm
   it FAILS for the intended reason (the vulnerability is real), not a typo
   or setup error. This is the `tdd-engineer` red step for security.
4. **Implement the minimal control** using existing project utilities at the
   correct boundary (server-side, not just the client). No unrelated edits.
5. **Run the negative test; confirm it now passes.** Then run the full
   relevant suite to confirm no regression. Record exact commands + output.
6. **Add positive-path coverage** if the control could over-block (a
   validator that rejects legitimate input is a new bug).
7. **Stage exactly the intended files** (`reviewable-diff-discipline`);
   verify the staged set equals the control's footprint — no drive-by changes.
8. **Report** the control, the before/after test evidence, the files touched,
   residual risk, and any follow-up the control does NOT cover, so a reviewer
   (`security-pr-reviewer`) can verify it.

## Output Format

```
APPSEC CONTROL IMPLEMENTED — <control name>
Closes: <threat/finding id + abuse case>
Change class: <class> — approval: <path / obtained?>
Negative test (red→green):
  command: <cmd>
  before: FAIL — <intended failure reason>
  after:  PASS
Full suite: <command> — <result>
Files changed: <exact paths — control footprint only>
Boundary: <where the control sits — confirmed server-side>
Reused utilities: <existing validators/ORM/middleware used>
Does NOT cover: <residual risk / adjacent controls still open>
Handoff: security-pr-reviewer to verify the diff.
```

## Validation Checklist

- [ ] The control was named/decided before implementation — not invented here.
- [ ] A negative test was written first and confirmed failing for the right
      reason before the fix.
- [ ] The same test passes after the change; full relevant suite still green;
      real commands and output recorded.
- [ ] The control sits at a server-side/authoritative boundary, not only the
      client or UI.
- [ ] Existing project security utilities reused; no hand-rolled crypto or
      duplicate validation layer.
- [ ] Staged set equals the control footprint; no unrelated refactors.
- [ ] Residual/adjacent risk stated for the reviewer.

## Security Rules

- No security control ships without a negative test that fails before it and
  passes after — an untested control is unverified (master-prompt §6).
- Controls are enforced server-side / authoritatively; client-side checks are
  UX, never the security boundary.
- Never hand-roll cryptography, token generation, or password hashing — use
  the platform/library primitive; flag if none is available and stop.
- Do not weaken or delete an existing control to make a test pass; if a
  control conflicts with the change, surface it via `human-approval-boundary`.
- Fixing one instance of a class (one unparameterized query) requires noting
  the sibling instances for a follow-up pass — do not imply the class is closed.

## Gotchas

- Adding validation only on the client leaves the server endpoint exploitable;
  the API is the boundary, the form is not.
- A negative test that passes on the FIRST run (before the fix) is testing the
  wrong thing — the vulnerability wasn't reproduced; fix the test before the code.
- Over-strict validators become availability bugs: a regex that rejects valid
  emails/names/unicode is a new defect — add positive cases.
- Encoding at the wrong layer (escaping in the DB instead of at render, or
  double-encoding) neutralizes the control or corrupts data.
- Security "fixes" that touch many files invite rubber-stamping and hide the
  one line that matters — keep the diff to the control.

## Stop Conditions

- No specific control is named, or the ask is "make it secure" broadly →
  stop; decompose via `threat-modeler` first.
- The change touches production config, secrets, or a security policy whose
  blast radius is unclear → stop for `human-approval-boundary`.
- The negative test cannot be made to fail before the fix → stop; the
  vulnerability is not reproduced and the control may be unnecessary or
  misplaced — reconfirm the threat.
- Implementing the control requires a schema/RLS change → that is
  `rls-policy-auditor` / `secure-migration-reviewer` territory; hand off.
- The only correct fix is a dependency upgrade with breaking changes → stop
  and surface the tradeoff rather than silently pinning or forcing it.

## Supporting Files

- [references/control-implementation-patterns.md](references/control-implementation-patterns.md)
  — per-control implementation checklists (validation, encoding, authz,
  session, file handling, SSRF/redirect) and the negative-test shape for each.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `threat-modeler`,
  `secrets-identity-hardener`, and `security-pr-reviewer`.
