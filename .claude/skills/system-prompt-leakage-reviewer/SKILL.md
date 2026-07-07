---
name: system-prompt-leakage-reviewer
description: Review an LLM feature for system-prompt leakage (OWASP LLM07) on two axes — (1) CONTENTS: the system prompt must contain no secrets, API keys, credentials, connection strings, internal URLs/architecture, or access rules whose disclosure causes harm; and (2) DEPENDENCE: the system must not RELY on the prompt staying secret for security, because prompts are extractable and are NOT a security control. Enforcement of authz, filtering, and limits must be deterministic and live OUTSIDE the model. Produces findings for secrets-in-prompt (extract and route to secrets-identity-hardener) and for prompt-as-control anti-patterns (route enforcement to the owning skill). Use when reviewing a system prompt, or when security depends on prompt confidentiality. Do NOT use for injection defense (prompt-injection-defender), sensitive data in user/context/output (sensitive-disclosure-guard), or tool scope (agent-tool-safety-guard).
---

# System Prompt Leakage Reviewer

## Purpose

Review an LLM feature for the two failure modes behind LLM07. First, the
system prompt's CONTENTS: it must carry no secrets, credentials, keys,
connection strings, internal URLs/architecture details, or access rules whose
leak causes harm — because system prompts are extractable and should be assumed
public. Second, and more important, the system's DEPENDENCE on prompt secrecy:
no security property may rest on the prompt staying hidden. The core doctrine
this skill enforces: **a system prompt is not a security control** — real
enforcement of authorization, filtering, rate limits, and tool permissions is
deterministic and lives OUTSIDE the LLM. Findings split into secrets-in-prompt
(extract, rotate) and prompt-as-control anti-patterns (move the control out).

## Use When

- Use when: reviewing a system/developer prompt for leaked secrets or
  sensitive internal detail.
- Use when: a feature's security appears to depend on the prompt (or its
  rules) staying confidential.
- Use when: assessing extraction risk ("can a user get our system prompt?")
  and, more importantly, whether it MATTERS that they can.
- Do NOT use when: defending against untrusted content changing behavior
  (`prompt-injection-defender`) — related, but that's the input side.
- Do NOT use when: the sensitive data is in user input/context/output rather
  than the prompt (`sensitive-disclosure-guard`), or the concern is tool
  permissions (`agent-tool-safety-guard`).

## Inputs to Inspect

1. The system/developer prompt text: every instruction, embedded value, URL,
   rule, and example in it.
2. Embedded secrets: API keys, tokens, passwords, connection strings, internal
   endpoints, or any credential placed in the prompt "so the model can use it".
3. Security-relevant rules IN the prompt: "only admins may…", "never reveal
   prices below…", allow/deny lists, business logic that gates access — and
   whether anything ELSE enforces them.
4. The enforcement layer: is authorization/filtering/limits actually
   implemented in code outside the model, or is the prompt the only thing
   "enforcing" it.
5. Extraction exposure: whether the feature lets users get the model to reveal
   its instructions (direct ask, roleplay, translation, continuation).
6. `prompt-injection-defender` output where present (the two skills pair —
   injection often enables extraction).

## Workflow

1. **Read the prompt as if it were public.** Assume an attacker will obtain
   it. No prompt available to review → Stop Conditions. Then run both axes.
2. **Axis 1 — scan contents for secrets/sensitive detail** using
   [references/prompt-leakage-checks.md](references/prompt-leakage-checks.md):
   API keys, tokens, passwords, connection strings, internal URLs/hostnames,
   architecture specifics, other customers' data. Any found = finding; extract
   the value and route custody/rotation to `secrets-identity-hardener`.
3. **Axis 2 — find prompt-as-control dependence (the important one).** For
   every security-relevant rule in the prompt, ask: if the user ignored this
   line entirely, is there a deterministic control OUTSIDE the model that still
   stops them? If NO, that's the finding — the security rests on the prompt,
   which is not a control.
4. **Classify each security rule.** Authorization ("only admins…"), content
   gating ("never show X"), limits ("max N"), tool restriction ("don't call
   Y"). Each must have a real enforcement point: RBAC/policy check
   (`authorization-matrix-designer`), output filtering outside the model, rate
   limiting, tool authorization (`agent-tool-safety-guard`). The prompt line
   may stay as UX guidance, but it is not the control.
5. **Assess extraction, then de-emphasize it.** Note how easily the prompt
   leaks (it will), but frame the fix as removing what MATTERS if it leaks —
   not as trying to make the prompt un-extractable (an unwinnable goal).
   Prompt-hardening against extraction is defense-in-depth at best.
6. **Design canary/leak tests.** A canary marker in the prompt asserted absent
   from output; extraction attempts (direct, roleplay, translation) documented
   with the understanding that the real assertion is "extraction causes no
   harm". Hand to `ai-evaluation-harness`.
7. **Report both axes with routing.** Secrets → extract + rotate; prompt-as-
   control → move the control out to the named owning skill. State residual
   risk with a named acceptor.

## Output Format

```
SYSTEM-PROMPT LEAKAGE REVIEW — <feature>
Assumption: the system prompt is treated as PUBLIC.
Axis 1 — Contents (secrets/sensitive):
  [SEV] <secret/detail in prompt> → extract + rotate (→ secrets-identity-hardener)
Axis 2 — Prompt-as-control (dependence):
  <security rule in prompt> | deterministic control outside model? <yes / NO=finding>
    → move enforcement to <authorization-matrix-designer | agent-tool-safety-guard | output filter | rate limit>
Extraction exposure: <how easily it leaks — framed as "does it matter?">
Canary/leak tests: <marker absent from output; extraction attempts> (→ ai-evaluation-harness)
Residual risk: <what remains + named acceptor>
```

## Validation Checklist

- [ ] The prompt was reviewed as if public (assume extractable).
- [ ] Axis 1: no secrets, keys, credentials, connection strings, internal
      URLs, or sensitive detail remain in the prompt; found ones routed to
      `secrets-identity-hardener` for rotation.
- [ ] Axis 2: every security-relevant rule in the prompt has a deterministic
      enforcement point OUTSIDE the model, or is flagged as a finding.
- [ ] Each prompt-as-control finding routes enforcement to the owning skill
      (authz / tool / output-filter / rate-limit).
- [ ] Extraction risk is noted but the remediation is "remove what matters if
      leaked", not "make the prompt un-extractable".
- [ ] Canary/leak tests exist; the real assertion is that extraction causes no
      harm.

## AI Security Rules

- A system prompt is NOT a security control. Enforcement of authorization,
  filtering, limits, and tool permissions is deterministic and lives outside
  the LLM. This is the doctrine every finding traces back to.
- Assume the system prompt is public: it is extractable via injection,
  roleplay, translation, and continuation. Design so that leaking it costs
  nothing.
- Secrets never belong in a prompt: a key in the system prompt is a leaked key,
  full stop — rotate it and move it server-side.
- Prompt-hardening against extraction is defense-in-depth, never the primary
  control; do not report a feature "safe" because the prompt is hard to
  extract.

## Gotchas

- The seductive anti-pattern: "we put the API key in the system prompt so the
  model can call our API." That key is now one extraction prompt away from
  public. It must be server-side, called by code, never handed to the model.
- "Only admins can do X" as a prompt line with no RBAC behind it: a user says
  "I'm an admin" (or injects it) and the model complies — the prompt "rule"
  enforced nothing.
- Chasing un-extractability wastes effort: every published defense gets
  bypassed. The win is making extraction irrelevant, not impossible.
- Business logic in the prompt leaks strategy: pricing floors, unreleased
  features, internal thresholds — extraction hands competitors your playbook.
- Injection and leakage pair up: the same techniques that inject also extract
  (`prompt-injection-defender`); a feature weak to one is usually weak to both.
- Don't conflate with disclosure of USER data: this skill is the PROMPT's
  contents and the security-dependence on its secrecy;
  `sensitive-disclosure-guard` owns sensitive data flowing through the feature.

## Stop Conditions

- No system/developer prompt is available to review — stop; this skill reviews
  a concrete prompt and its enforcement surroundings.
- A live secret (valid key/credential) is found in the prompt — treat as
  active exposure: route rotation through `secrets-identity-hardener` and, if
  it may already be leaked, `incident-response-runbook`.
- The real issue is injection defense, sensitive user-data disclosure, or tool
  scope — hand to the owning skill.
- Fixing a prompt-as-control finding requires building the real enforcement
  (RBAC, filter, rate limit) — propose it; implementation is a classified,
  approved step routed to the owning skill.

## Supporting Files

- [references/prompt-leakage-checks.md](references/prompt-leakage-checks.md) —
  the secrets/sensitive-content scan list, the prompt-as-control anti-pattern
  catalog with the "what enforces it outside the model?" test, extraction
  techniques (for awareness, not as the fix), and canary-test seeds.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the threat & injection
  cluster and against `prompt-injection-defender` and `secrets-identity-hardener`.
