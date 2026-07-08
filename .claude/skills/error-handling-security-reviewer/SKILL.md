---
name: error-handling-security-reviewer
description: Review error/exception handling through a security lens — fail-closed defaults (a failed check, timeout, or down dependency DENIES, never allows), error-path AUTHORIZATION (authz still enforced on every error/retry/fallback branch), exception-driven logic BYPASS (does an exception skip a check, validation, rollback, or audit write?), and leak-free error responses (no stack traces/secrets/internal detail to callers — generic outside, rich inside). Closes OWASP Top 10:2025 A10 (Mishandling of Exceptional Conditions). Use when reviewing catch blocks, fallbacks, global error handlers, or asking "what happens when this fails?". Do NOT use for broad diff security review (security-pr-reviewer — this is the error-path lens), building a named control (appsec-implementer), triaging scanner output (static-analysis-reviewer), or designing the error MODEL (error-taxonomy-designer).
---

# Error-Handling Security Reviewer

## Purpose

Give the error and exception paths of a codebase a security verdict: findings
with file:line evidence, severity, and a concrete failure scenario for each
place where exceptional conditions are mishandled — a check that fails open,
an error branch that skips authorization, an exception that bypasses
validation/rollback/audit, or an error response that leaks internals. This
closes OWASP Top 10:2025 A10 — Mishandling of Exceptional Conditions: the
failure class where the HAPPY path is secure and the security hole lives in
what happens when something throws, times out, or goes down. Attackers
deliberately CAUSE errors to reach these paths, so the review treats every
error branch as attacker-reachable. Review-only and model-invocable: it edits
nothing — fixes are recommended and handed to `appsec-implementer` or the
human.

## Use When

- Use when: asked to review error handling, exception handling, catch blocks,
  fallbacks, retries, or global error handlers for security.
- Use when: asking "what happens when this fails?" about a security-relevant
  path — auth service down, database timeout, validation throw, quota hit.
- Use when: a change adds try/catch, a circuit breaker, a fallback path, a
  default value on failure, or a global exception handler — the error-path
  lens on that specific surface.
- Use when: an incident showed a failure being converted into an allow, a
  skipped check, or an information leak, and the codebase needs the same
  pattern hunted everywhere.
- Do NOT use when: the ask is a broad security review of a whole diff/PR —
  `security-pr-reviewer` owns that gate; invoke THIS lens when the diff's
  risk is specifically in error/exception paths, or compose it within that
  review.
- Do NOT use when: implementing the fix for a finding — `appsec-implementer`
  builds the named control test-first; this skill reviews and reports.
- Do NOT use when: the input is SAST/scanner output to triage —
  `static-analysis-reviewer` judges scanner findings; this skill reads the
  actual code.
- Do NOT use when: designing the error MODEL itself — codes, envelope,
  taxonomy, retryability semantics — that is `error-taxonomy-designer`; this
  skill reviews whether the HANDLING of errors is secure, whatever the model.

## Inputs to Inspect

1. The error-handling surfaces themselves: global/framework exception
   handlers and middleware, try/catch blocks on security-relevant paths,
   fallback and retry logic, circuit breakers, default-value-on-failure
   expressions, and empty or log-only catch blocks.
2. The security checks those paths surround: authn/authz middleware order
   relative to error handlers, validation layers, rate limits, audit writes —
   what a thrown exception would skip.
3. The error responses actually produced: response bodies, headers, and
   status codes per failure class — in every environment configuration, since
   debug/verbose modes often differ.
4. The error taxonomy/envelope design (`error-taxonomy-designer` output) if
   one exists: the contract errors are supposed to follow — deviations on
   security-relevant fields are findings.
5. Dependency-failure behavior: what each security-relevant dependency
   (auth service, policy engine, database, cache) failing does to the
   decision the caller makes.
6. Tests over error paths: whether negative tests exist proving denial on
   failure — untested fail-closed claims are unverified.

## Workflow

1. **Inventory the error paths on security-relevant surfaces.** Locate global
   exception handlers, catch blocks, fallbacks, retries, and
   default-on-failure expressions that sit on or around authn, authz,
   validation, tenant scoping, rate limiting, payment, and audit logic. Use
   the pattern catalog in
   [references/error-path-review-sheet.md](references/error-path-review-sheet.md).
2. **Test each path against fail-closed defaults.** For every failure a
   security decision can encounter (exception, timeout, null/empty result,
   dependency down): does the code DENY, or does it default to allow, cached
   allow, or skip? A permission check whose catch returns `true`, an authz
   lookup whose timeout falls through to the handler, an allowlist that is
   bypassed when the list fails to load — each is a finding with the concrete
   trigger stated.
3. **Check error-path authorization.** Follow each error/retry/fallback
   branch end-to-end: is authentication and authorization still enforced on
   the alternate path? Fallback endpoints, degraded modes, and retry queues
   that re-execute work without re-checking the caller are the classic hole.
4. **Hunt exception-driven bypass.** For each thrown/caught/swallowed
   exception around a security control: does the exception cause a check,
   validation step, rollback, rate-limit count, or audit write to be
   SKIPPED while execution continues? Pay attention to catch-and-continue,
   exceptions swallowed to "keep the request alive", finally blocks that
   mask them, and partial-failure states committed as success.
5. **Review error responses for leaks.** Per failure class, what does the
   caller actually receive? Stack traces, exception class names/messages,
   SQL fragments, file paths, dependency hostnames, secrets/tokens, and
   existence-oracle differences (404 vs 403 revealing resource existence,
   timing/verbosity differences revealing valid usernames) — checked against
   every environment config, not just production's intended one.
6. **Verify the evidence discipline.** Each finding: file:line, severity,
   the concrete failure scenario (what an attacker causes → what wrongly
   happens), and the recommended fix direction. High-severity findings need
   the abuse path stated, not implied.
7. **Check the negative tests.** For every fail-closed claim the code makes,
   does a test prove denial on failure? Missing ones are listed as test
   requirements (for `appsec-implementer` to build with the fix, or
   `test-plan-designer` to schedule).
8. **Report and hand off.** Findings ranked by severity; fixes recommended,
   never applied — implementation goes to `appsec-implementer` (or the
   human), taxonomy-level defects to `error-taxonomy-designer`.

## Output Format

An error-handling security review containing:

1. **Verdict** — pass / findings-block-ship / findings-nonblocking, with the
   blocking findings named.
2. **Findings table** — per finding: file:line, lens (fail-open /
   error-path-authz / exception-bypass / response-leak), severity, concrete
   failure scenario (trigger → wrong outcome), recommended fix direction.
3. **Fail-closed matrix** — security decision × failure mode (exception,
   timeout, empty result, dependency down) × observed behavior
   (deny/allow/skip), with untestable cells marked unverified.
4. **Leak inventory** — failure class → what the caller receives → what it
   reveals, per environment configuration reviewed.
5. **Missing-negative-test list** — fail-closed claims with no test proving
   denial on failure.
6. **Handoff list** — fixes to `appsec-implementer`/the human, error-model
   defects to `error-taxonomy-designer`, detection gaps (errors worth
   alerting on) to `security-logging-alerting-architect`.

## Validation Checklist

- [ ] Every security-relevant error path found was tested against all four
      lenses: fail-closed, error-path authz, exception bypass, response
      leaks — none skipped silently.
- [ ] Every finding has file:line, severity, and a concrete failure scenario;
      high-severity findings state the abuse path.
- [ ] The fail-closed matrix covers exception, timeout, empty/null result,
      and dependency-down per security decision — cells that could not be
      determined are marked unverified, not assumed safe.
- [ ] Error responses were checked in every environment configuration
      reviewed, and existence-oracle asymmetries (403/404, timing,
      verbosity) were explicitly considered.
- [ ] No code was edited; every fix is a recommendation in the handoff list.
- [ ] Fail-closed claims without negative tests are listed as test
      requirements, and the review does not claim they hold.
- [ ] OWASP category claims are scoped to the concrete risks reviewed; exact
      category text is flagged for confirmation against the OWASP source,
      not asserted from memory.

## Gotchas

- **The happy path lies.** Reviews that walk the success flow conclude the
  auth is solid; A10 holes are only visible when you ask "and when this
  throws?" at every security decision. Attackers cause the error on purpose
  — oversized payloads, connection resets, induced timeouts are inputs.
- **Catch-and-continue is the quiet killer.** An empty or log-only catch
  around a security check converts every exception in that check into an
  allow. Severity is set by what the check guarded, not by how small the
  catch block looks.
- **Graceful degradation vs security bypass.** "Stay up when the auth
  service is down" is an availability feature that is also a
  fail-open decision. Degrading UX is fine; degrading a security control
  needs an explicit, human-approved risk acceptance — the review names it,
  never blesses it by default.
- **Retries re-execute, authorization doesn't re-check.** Queued retries and
  replayed jobs often run under a system identity after the original
  caller's context expired — the retry path is a separate authz surface.
- **The global handler masks partial failure.** A catch-all that maps
  everything to a friendly 200/generic 500 can hide that a transaction half
  committed, an audit write was skipped, or a rate-limit counter never
  incremented — response-code truthfulness is part of the review.
- **Leaks hide in asymmetry, not just stack traces.** Identical-looking
  errors that differ in timing, status code, or message detail form oracles
  (valid username, resource existence, tenant membership) even when no
  internals are printed.
- **Debug config in the wrong environment.** The leak-free production
  response and the verbose staging response are one misconfigured flag
  apart; review the configuration matrix, not one environment's output.
- **OWASP text drift.** This skill's A10 mapping uses the category name as
  recorded in the repo's D8 coverage audit of OWASP Top 10:2025; when
  quoting category text or scope, confirm against the OWASP source first
  (verify-don't-assert) — `framework-edition-tracker` owns edition drift.

## Stop Conditions

- No code to review — the ask is design-time ("how should errors work?") or
  there is no repo/diff access: route to `error-taxonomy-designer` (model)
  or `threat-modeler` (design) instead of reviewing from imagination.
- Asked to FIX the findings — implementation is `appsec-implementer` (or
  the human); applying fixes from inside the review destroys the
  review/implement separation.
- Asked to approve a fail-open behavior as a business tradeoff — that
  acceptance is a human decision to record (risk register / ADR), not a
  reviewer verdict; state the risk and stop.
- The error behavior cannot be determined statically (dynamic config,
  reflection, external policy) and no safe way exists to verify — mark the
  cell unverified and say what a safe verification would need, rather than
  guessing "probably denies".
- The review surfaces an apparently live, exploitable fail-open in
  production — stop expanding scope and surface it to the human immediately
  as a security disclosure, per `sensitive-disclosure-guard` discipline.

## Supporting Files

- [references/error-path-review-sheet.md](references/error-path-review-sheet.md)
  — the four review lenses with concrete code patterns to hunt, the
  fail-closed matrix template, and the leak-oracle checklist.
- [evals/evals.json](evals/evals.json) — behavior cases: full error-path
  review, catch-all-handler edge case, refusal to apply fixes, refusal to
  bless fail-open, and the scanner-triage boundary.
- [evals/trigger-evals.json](evals/trigger-evals.json) — discrimination
  against `security-pr-reviewer`, `appsec-implementer`,
  `static-analysis-reviewer`, and `error-taxonomy-designer`.
