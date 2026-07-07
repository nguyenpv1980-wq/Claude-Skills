---
name: threat-modeler
description: Build a threat model for a feature or system BEFORE it is implemented — assets, actors, trust boundaries, data flows, STRIDE-style threat enumeration per boundary, abuse cases written from attacker behavior, risks ranked with concrete exploit paths, mitigations mapped to each threat, and a validation test plan with negative tests per mitigation. Use when designing a security-sensitive feature (auth, uploads, payments, integrations, admin/support tooling), when asked to "threat model" something, before exposing a new external surface, or after an incident to enumerate sibling attack paths. Consumes tenant-modeler and authorization-matrix-designer outputs as inputs when present rather than re-deriving them. Do NOT use to review an implemented diff (security-pr-reviewer), audit existing tenant isolation (tenant-isolation-reviewer), or triage scanner output (static-analysis-reviewer).
---

# Threat Modeler

## Purpose

Produce a threat model a team can build and test against: what we are
building, what can go wrong, what we will do about it, and how we will prove
the defenses work. The deliverables are an asset/actor/trust-boundary map,
per-boundary threat enumeration, abuse cases written as attacker behavior,
risks ranked by concrete exploit path (not gut feeling), mitigations mapped
one-to-one to threats, and a validation test plan where every mitigation gets
a negative test. A threat without an exploit path is a hypothesis and is
labeled as one; a mitigation without a test is a wish.

## Use When

- Use when: designing a security-sensitive feature — authentication, file
  upload, payment flow, third-party integration, webhook receiver, admin or
  support tooling, data export.
- Use when: asked to "threat model" a system, feature, or design doc.
- Use when: a new externally reachable surface is about to ship and nobody
  has enumerated how it can be abused.
- Use when: after an incident, to enumerate sibling attack paths the incident
  class implies (the found hole is rarely the only one).
- Do NOT use when: reviewing an implemented diff for security — that is
  `security-pr-reviewer`; this skill works on designs and systems, not hunks.
- Do NOT use when: auditing an existing system for cross-tenant leakage —
  that is `tenant-isolation-reviewer`.
- Do NOT use when: triaging SAST/scanner findings — `static-analysis-reviewer`.
- Do NOT use when: the threats are AI/LLM-specific (prompt injection, RAG
  authorization, excessive agency) — that is the Phase 7 pack; note the gap
  rather than improvising coverage here.

## Inputs to Inspect

1. The design artifact under threat: design doc, ADR, issue, or the existing
   code and schema of the surface being extended. No artifact → Stop Conditions.
2. Prior security context: tenant model (`tenant-modeler` output), the
   authorization matrix (`authorization-matrix-designer` output), audit
   taxonomy — consume these as inputs; do not re-derive tenant semantics or
   role definitions inside the threat model.
3. Entry points and data flows: routes, webhooks, jobs, imports, file
   handling, third-party callbacks — where untrusted data enters and where
   trust levels change.
4. The assets at stake: which data or capability an attacker would want
   (credentials, tenant business data, money movement, admin capability).
5. Existing mitigations already in the codebase (middleware, validators,
   policies) so the model records real posture, not assumed posture.
6. Prior incidents and pen-test findings for this system, if any.

## Workflow

1. **Scope the model.** One feature/surface per pass. State what is in and
   out of scope; an unbounded threat model converges on generic advice.
2. **Map the system:** assets (what's worth stealing/breaking), actors
   (legitimate roles from the authorization matrix, plus attacker personas:
   anonymous, authenticated wrong-tenant, malicious insider, compromised
   dependency), entry points, and data flows.
3. **Draw trust boundaries** — every place data crosses a privilege or trust
   level (client→server, server→DB, tenant→tenant, app→third party,
   CI→production). Number them; threats attach to boundaries.
4. **Enumerate threats per boundary** using the STRIDE prompts in
   [references/threat-catalog.md](references/threat-catalog.md). For SaaS
   paths, tenant isolation and object-level authorization threats are
   mandatory rows at every data-access boundary, never optional.
5. **Write abuse cases** for the credible threats: attacker persona, concrete
   steps, and payoff ("wrong-tenant authenticated user calls export with a
   guessed id and receives tenant B's ledger"). An abuse case must be
   specific enough to become a test later.
6. **Rank risks.** High severity REQUIRES a stated exploit path — who,
   from where, doing what, getting what. No exploit path → cap at medium and
   label what would confirm it. Rank by exploitability × asset impact,
   including tenant blast radius (one tenant vs all tenants).
7. **Map mitigations** one-to-one to ranked threats: the control, where it
   lives (which boundary), and who builds it. Unmitigated threats are
   explicitly accepted (needs the human's written rationale — route via
   `human-approval-boundary`) or explicitly deferred with an owner.
8. **Write the validation test plan:** for every mitigation, at least one
   negative test executing the abuse case and observing denial/failure.
   Hand implementable tenant/authz tests to `multi-tenant-security-tester`;
   control implementation goes to `appsec-implementer`.
9. **Deliver the model** in the output format; keep it versionable next to
   the design doc so it can be re-run when the design changes.

## Output Format

```
THREAT MODEL — <feature/system> (scope: <in / out>)
Assets: <asset — why an attacker wants it>
Actors: <legitimate roles (from authz matrix) + attacker personas>
Trust boundaries: B1..Bn <boundary — trust change at it>
Data flows: <entry point → boundary → store/exit>
Threats (per boundary, STRIDE-tagged):
  T<n> [B<x>] <threat> — <abuse case: persona, steps, payoff>
Risk ranking:
  [HIGH]   T<n> — exploit path: <who, from where, doing what, getting what>
  [MEDIUM] T<n> — <path or "hypothesis — confirmed by: <what>">
  [LOW]    ...
Mitigations: T<n> → <control> at <boundary> — owner: <who>
Accepted/deferred threats: <threat — written rationale or owner + date>
Validation test plan: T<n> → <negative test: attempt + expected failure>
Handoffs: <appsec-implementer: controls | multi-tenant-security-tester: tests>
Not modeled: <explicitly out-of-scope areas + why>
```

## Validation Checklist

- [ ] Scope stated; every threat attaches to a numbered trust boundary.
- [ ] Attacker personas include anonymous, wrong-tenant authenticated, and
      privileged insider — not just "hacker".
- [ ] Every SaaS data-access boundary has tenant-isolation and object-level
      authorization threat rows.
- [ ] Every HIGH risk has a concrete exploit path; path-less highs were
      downgraded and labeled hypotheses.
- [ ] Every credible threat maps to a mitigation, a written acceptance, or a
      deferral with an owner — none silently dropped.
- [ ] Every mitigation has a negative test in the validation plan.
- [ ] Existing mitigations were verified in code, not assumed present.
- [ ] Nothing was implemented — this skill models; building is a handoff.

## Security Rules

- High-severity claims without an exploit path are forbidden — rank them
  medium as hypotheses and name what would confirm them.
- Threats are never deleted from the model without written rationale;
  "unlikely" is a ranking, not a removal.
- Tenant isolation and object-level authorization are mandatory analysis
  rows on every SaaS data path (master-prompt §6), even when the requester
  did not ask about tenancy.
- Absence of a mitigation in scope is recorded as accepted risk requiring
  human sign-off, never silently normalized.

## Gotchas

- Threat models that skip actor definition produce generic STRIDE noise —
  the wrong-tenant *authenticated* user is the persona most SaaS models miss,
  and the most common real attacker.
- Trust boundaries inside the backend (job runner with service credentials,
  support console, internal admin API) get skipped because "it's internal";
  privilege boundaries count even with no network hop.
- Modeling the happy-path dataflow only: file uploads, error paths, retries,
  and webhook redelivery all carry attacker-controlled data too.
- A mitigation that exists in middleware can be bypassed by a second route to
  the same data (GraphQL next to REST, RPC next to ORM) — enumerate routes to
  the asset, not routes you were told about.
- Re-deriving tenant semantics or role definitions here drifts from the
  canonical `tenant-modeler` / `authorization-matrix-designer` outputs —
  consume them and cite them instead.

## Stop Conditions

- No design artifact, code, or schema exists to model — stop; ask for the
  design input rather than modeling from imagination.
- The tenant model or authorization semantics are undefined and the feature
  is tenant-facing → stop; run `tenant-modeler` /
  `authorization-matrix-designer` first, then model against their output.
- Modeling reveals an apparently exploitable hole in the LIVE system (not
  the design) → report it immediately as a finding with its exploit path;
  containment is the human's call via `human-approval-boundary`.
- The requester asks to skip or delete threats to make the model look clean
  → refuse; record the threat and route acceptance through written rationale.

## Supporting Files

- [references/threat-catalog.md](references/threat-catalog.md) — STRIDE
  prompts per boundary type, SaaS-specific threat rows, and abuse-case
  patterns with payoff templates.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `appsec-implementer`
  and `secrets-identity-hardener` (threat & hardening cluster) and against
  `security-pr-reviewer` / `tenant-isolation-reviewer`.
