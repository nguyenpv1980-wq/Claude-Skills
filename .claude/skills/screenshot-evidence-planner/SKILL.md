---
name: screenshot-evidence-planner
description: Design the screenshot/visual-evidence policy for testing and releases — WHICH checkpoints require captures (risk-worthy states, not everything), a deterministic NAMING convention, mandatory MASKING of sensitive data (PII, tokens, tenant identifiers) before storage, required METADATA (build, environment, persona, viewport, timestamp, case id), STORAGE location/retention/access rules, and how evidence links to test cases, PRs, and closeout reports. Also sets capture-quality rules (deterministic viewport, stable data). Use when asked what screenshots a release or test pass needs, to standardize evidence naming/masking/storage, when screenshot evidence is inconsistent or leaks customer data, or to make manual/clickthrough/E2E artifacts audit-ready. Planning/policy only — it does not capture screenshots. Do NOT use to run the capturing session (clickthrough-test-engineer), write the cases referencing checkpoints (manual-test-case-creator), or write the closeout itself (ai-closeout-reporter).
---

# Screenshot Evidence Planner

## Purpose

Produce the evidence policy that makes screenshots trustworthy artifacts
instead of a folder of `Screenshot (47).png`: which states get captured and
why, how files are named so a stranger can locate and interpret them, what
gets masked before storage, what metadata makes a capture attributable to a
build, and where evidence lives with what retention. The output governs
every capturing skill and feeds closeout reporting — this skill itself
captures nothing.

## Use When

- Use when: asked which screenshots a release, test pass, or audit needs.
- Use when: evidence exists but is unusable — inconsistent names, no build
  attribution, sensitive data visible, scattered storage.
- Use when: a compliance/customer requirement demands audit-ready visual
  evidence with retention rules.
- Use when: manual cases, clickthrough sessions, or Playwright failure
  artifacts need one shared evidence convention.
- Do NOT use when: someone must capture screenshots NOW in a session —
  `clickthrough-test-engineer` (it follows this policy).
- Do NOT use when: writing the manual cases that reference checkpoints —
  `manual-test-case-creator`.
- Do NOT use when: producing the closeout report that bundles evidence —
  the shipped `ai-closeout-reporter`; this skill defines what it bundles.
- Do NOT use when: the ask is visual-regression pixel-diff tooling — that is
  automation architecture (`qa-automation-architect`) with this policy as
  input.

## Inputs to Inspect

1. What evidence consumers need: release gates, PR review, compliance/audit
   obligations, customer commitments — evidence without a consumer is cost.
2. The capture producers in play: manual passes, clickthrough sessions,
   Playwright failure artifacts — and what they can technically emit.
3. Sensitivity reality: what data appears on screens (PII, tokens, tenant
   names, financials) and any redaction obligations; tenant-isolation rules
   apply to evidence too (a screenshot of tenant A's data in tenant B's bug
   ticket is a leak).
4. Storage options actually available (repo, artifact store, ticket system)
   and their access control.
5. Existing conventions worth keeping (partial policies, naming habits).

## Workflow

1. **Define checkpoints from risk, not habit.** For each surface/pass in
   scope: which states are evidence-worthy — the state that proves the
   requirement, the state before/after destructive actions, permission-view
   differences per persona, error states. "Screenshot everything" buries the
   one capture that matters; each checkpoint gets an id and a "what must be
   visible" line. Catalog in
   [references/evidence-rules.md](references/evidence-rules.md).
2. **Fix the naming convention:** deterministic, sortable, collision-free —
   pattern `<checkpoint-id>--<route/case>--<persona>--<build>--<timestamp>`
   (adjust tokens to the repo), documented with examples and counter-examples.
3. **Write the masking rules as mandatory:** what is ALWAYS masked (emails,
   names, tokens, payment data, cross-tenant identifiers), how (block-out,
   not blur — blur is reversible for text), when (before storage, never
   "later"), and the review step for evidence leaving the org boundary.
4. **Specify metadata per capture:** build/commit, environment, persona/role,
   viewport, timestamp, capturing case/session id — carried in a sidecar
   record or report table, not burned illegibly into filenames.
5. **Set storage, retention, and access:** where evidence lives per class
   (PR artifact vs release record vs compliance archive), retention windows,
   and who can read what (evidence containing tenant data inherits
   tenant-access restrictions).
6. **Define linkage:** how checkpoints attach to manual case ids, clickthrough
   reports, PRs, and the closeout evidence bundle (`ai-closeout-reporter`
   consumes this) — an unlinked screenshot is unfindable a month later.
7. **Set capture-quality rules** so evidence is judgeable: deterministic
   viewport(s), stable/seeded data, full relevant state in frame, UI chrome
   included where context matters.

## Output Format

```
EVIDENCE POLICY — <scope>
Consumers & obligations: <who needs evidence, for what, incl. compliance>
Checkpoint catalog:
  <CP-id> — <surface/state> — what must be visible — why (risk/requirement)
Naming convention: <pattern + 2 valid examples + 1 counter-example>
Masking rules: <always-masked list; method (block-out); enforcement point;
               cross-tenant rule>
Metadata: <required fields + where recorded (sidecar/report table)>
Storage & retention: <class → location → retention → access rule>
Linkage: <checkpoint ↔ case/session/PR/closeout wiring>
Capture-quality rules: <viewport(s), data stability, framing>
Adoption: <which producers follow this (manual/clickthrough/playwright) +
          migration note for existing evidence>
```

## Validation Checklist

- [ ] Every checkpoint has a consumer/risk justification — no
      screenshot-everything.
- [ ] Naming is deterministic, sortable, and demonstrated with examples.
- [ ] Masking list is explicit, block-out based, enforced BEFORE storage.
- [ ] Cross-tenant evidence rule stated (evidence inherits tenant access).
- [ ] Metadata fields make every capture attributable to build + persona +
      environment.
- [ ] Storage, retention, and access defined per evidence class.
- [ ] Linkage to cases/sessions/PRs/closeout defined.
- [ ] No screenshots captured by this skill.

## Safety Rules

- Sensitive-data masking is not optional and not deferrable: evidence is
  stored masked or not stored.
- Blur and crop are not masking for text — block-out only.
- Evidence containing one tenant's data never appears in another tenant's
  ticket, report, or communication.
- Production screenshots follow the strictest masking class by default.

## Gotchas

- Filenames as the only metadata channel fail at the first rename — the
  sidecar/report table is the source of truth; the filename is a locator.
- Retention "forever" turns evidence into a liability archive of PII —
  retention windows are part of the policy, not an afterthought.
- Playwright's auto-artifacts (traces, failure screenshots) contain unmasked
  real data by design — classify their storage separately (short retention,
  restricted access) instead of pretending they're policy-compliant evidence.
- Checkpoints defined against unstable demo data produce unjudgeable
  captures — stable/seeded data is a capture-quality rule, not a nicety.
- A policy nobody can follow in-flow (20 manual fields per capture) will be
  ignored — metadata that can be auto-derived (build, timestamp) must be.

## Stop Conditions

- No consumer for the evidence can be named → stop and ask what the evidence
  is FOR; a policy without consumers is ceremony.
- Compliance/retention obligations are referenced but not documented → get
  the actual obligation text before encoding retention rules.
- The policy would require storing unmaskable sensitive data → surface the
  conflict via `human-approval-boundary` rather than quietly weakening
  masking.
- Asked to also capture the evidence now → hand to
  `clickthrough-test-engineer` / the executing pass.

## Supporting Files

- [references/evidence-rules.md](references/evidence-rules.md) — checkpoint
  selection catalog, naming token table, masking classes, metadata schema,
  and storage-class matrix.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the UI/manual cluster
  and against the shipped `ai-closeout-reporter`.
