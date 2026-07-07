---
name: sensitive-disclosure-guard
description: Prevent an LLM feature from disclosing sensitive information (OWASP LLM02) — audit and design the data-minimization and redaction pipeline so secrets, credentials, PII, and other-tenant data are stripped BEFORE they enter model context, prompts, or logs; assemble context with least-data (only the fields the task needs, not whole records); check the output path for leaks (the model echoing sensitive input, cross-conversation/cache bleed); and confirm provider data-handling posture (retention, training-on-inputs). Composes tenant-isolation-reviewer for the tenant surface and secrets-identity-hardener for credential custody. Use when an AI feature touches PII/secrets/tenant data, or to design a pre-model redaction pipeline. Do NOT use for retrieval authorization (rag-security-architect), output execution sinks (llm-output-safety-reviewer), system-prompt secrets (system-prompt-leakage-reviewer), or governance sign-off (ai-governance-risk-reviewer).
---

# Sensitive Disclosure Guard

## Purpose

Keep sensitive data from leaking through an LLM feature (LLM02): the deliverable
is a data-minimization and redaction design plus a leak audit across the three
places disclosure happens — what goes INTO the model (context/prompt), what the
model gives BACK (output echoing or inferring sensitive data), and what gets
recorded (logs, traces, provider retention). It enforces least-data context
assembly (only the fields the task needs), a redaction pipeline before model
calls, an output-path leak check, and a provider-posture confirmation. Tenant
scoping is composed from `tenant-isolation-reviewer` and credential custody from
`secrets-identity-hardener` — this skill focuses on the model-disclosure surface.

## Use When

- Use when: an AI feature's context, prompt, output, or logs can contain PII,
  secrets, credentials, financial/health data, or other-tenant data.
- Use when: designing a redaction / data-minimization pipeline in front of
  model calls.
- Use when: reviewing whether a feature leaks sensitive data in responses,
  logs, caches, or to the provider.
- Do NOT use when: the concern is WHO can retrieve WHICH documents
  (`rag-security-architect`) or an execution/render sink
  (`llm-output-safety-reviewer`).
- Do NOT use when: the secret lives in the system prompt
  (`system-prompt-leakage-reviewer`) or the ask is governance/consent sign-off
  (`ai-governance-risk-reviewer`).

## Inputs to Inspect

1. Context assembly: what data is put into the prompt/context and where it
   comes from — whole records vs the specific fields the task needs.
2. Sensitive-data inventory: what PII/secrets/credentials/regulated data could
   reach the model, and its classification.
3. The output path: whether responses can echo sensitive input, infer/aggregate
   it, or bleed across users/conversations via shared caches or memory.
4. Logging/telemetry: what prompts, contexts, and outputs are logged, and
   whether sensitive content is redacted before storage.
5. Provider posture: retention window, training-on-inputs terms, region/
   residency, sub-processors — from `ai-governance-risk-reviewer` where
   available.
6. Tenant context: `tenant-isolation-reviewer` findings for cross-tenant data
   in shared context/cache; `secrets-identity-hardener` for any credential
   exposure.

## Workflow

1. **Classify what could leak.** Inventory sensitive data that can reach the
   model's context, output, or logs, and classify it (PII, secret, regulated,
   other-tenant). No AI feature/data flow to inspect → Stop Conditions.
2. **Minimize context (least-data).** Challenge every field placed in context:
   does the task need it? Replace whole-record dumps with the specific fields
   required; tokenize/pseudonymize identifiers where the task doesn't need the
   real value. The cheapest leak prevention is not sending the data.
3. **Design the redaction pipeline** using
   [references/disclosure-controls.md](references/disclosure-controls.md):
   strip/mask secrets, credentials, and PII BEFORE the model call — pattern-
   and classification-based, applied to user input, retrieved content, and
   tool outputs alike. Define what is redacted vs tokenized-and-restored.
4. **Audit the output path.** Check whether the model can echo sensitive input
   back, infer it, or leak another user's data via shared conversation state,
   caches, or memory. Cross-conversation/cross-tenant bleed is a top finding
   (compose `tenant-isolation-reviewer`).
5. **Redact logs and telemetry.** Prompts, contexts, and outputs logged for
   debugging/observability must have sensitive content stripped at emission —
   an unredacted prompt log is a disclosure even if the response was safe
   (compose `observability-operator` for the emission point).
6. **Confirm provider posture.** Verify retention and training-on-inputs terms
   are acceptable for the data's classification; if the provider trains on
   inputs, sensitive data must not be sent (or must be redacted first).
   Governance permission is `ai-governance-risk-reviewer`; this skill checks
   the mechanism.
7. **Design leak tests.** Canary values planted in context that must never
   appear in output/logs; cross-user requests that must not surface another
   user's data; a prompt asking the model to reveal its input. Hand to
   `ai-evaluation-harness`.

## Output Format

```
SENSITIVE DISCLOSURE REVIEW — <feature>
Sensitive-data inventory: <PII | secrets | regulated | other-tenant — classification>
Context minimization: <whole-record dumps → least-data fields | tokenized ids>
Redaction pipeline: <what/where stripped before model call — input/retrieval/tool>
Output-path leaks: <echo | inference | cross-conversation/cache/tenant bleed>
Log/telemetry redaction: <sensitive content stripped at emission?> (→ observability-operator)
Provider posture: <retention | trains-on-inputs? | residency> (→ ai-governance-risk-reviewer)
Findings (severity-ranked): [SEV] <leak> — <path> — <fix>
Leak tests: <canary / cross-user / echo cases> (→ ai-evaluation-harness)
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] Sensitive data reaching context/output/logs is inventoried and
      classified.
- [ ] Context is minimized to the fields the task needs; whole-record dumps
      are flagged and reduced.
- [ ] A redaction pipeline strips secrets/credentials/PII BEFORE the model call
      across user input, retrieved content, and tool outputs.
- [ ] The output path is checked for echo, inference, and cross-user/cache/
      tenant bleed.
- [ ] Logs/telemetry redact sensitive content at emission (unredacted prompt
      logs are a finding).
- [ ] Provider retention/training posture is confirmed acceptable for the data
      classification.
- [ ] Leak tests use canaries and cross-user cases with expected no-leak
      outcomes.

## Security Rules

- The cheapest disclosure control is data minimization: don't send what the
  task doesn't need — least-data context beats redaction after the fact.
- Redaction happens BEFORE the model call and BEFORE logging — not after a
  leak is noticed.
- Cross-tenant/cross-user disclosure via shared context, caches, or memory is
  a critical finding (compose `tenant-isolation-reviewer`).
- Sending sensitive data to a provider that trains on inputs is a disclosure
  regardless of transport security — check the terms.

## Gotchas

- Whole-record context is the silent leak: "just pass the user object" sends
  fields the task never needed straight to the provider and the logs.
- The model echoes its input: ask "what do you know about me?" and an over-
  broad context happily reads back another record it was given.
- Shared caches/memory bleed across users: a response cache keyed too loosely,
  or conversation memory not scoped per user, serves one user's data to
  another.
- Prompt logs are the forgotten disclosure: teams redact responses but log the
  full prompt (with the PII) for "debugging" — that's the leak.
- Inference, not just echo: a model can aggregate/deduce sensitive facts from
  non-obvious context (re-identification) — minimize, don't just mask exact
  strings.
- Redaction is lossy and imperfect: pattern-based masking misses novel formats;
  minimization (not sending it) is more reliable than scrubbing.

## Stop Conditions

- No AI feature or data flow is available to review — stop; this skill audits
  a concrete disclosure surface.
- Sensitive data is already being sent to a provider that trains on it — flag
  as blocking and route the decision to `ai-governance-risk-reviewer` /
  `human-approval-boundary`.
- The real issue is retrieval authorization, an execution sink, or a
  system-prompt secret — hand to the owning skill.
- A review finds an active leak in production (other-tenant data in responses/
  logs) — route to `incident-response-runbook`.

## Supporting Files

- [references/disclosure-controls.md](references/disclosure-controls.md) — the
  data-minimization rubric, redaction-pipeline patterns (what to strip vs
  tokenize, where), output-path and log leak checks, provider-posture
  questions, and canary-based leak-test seeds.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the threat & injection
  cluster and against `rag-security-architect`, `secrets-identity-hardener`,
  and `tenant-isolation-reviewer`.
