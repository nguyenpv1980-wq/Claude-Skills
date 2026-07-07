---
name: ai-threat-modeler
description: Build the AI-specific threat model for an LLM feature, RAG pipeline, or agent BEFORE it ships — inventory AI assets (prompts, models, vector stores, tools, credentials) and trust boundaries where user input, retrieved documents, tool outputs, and model outputs are all untrusted by default; enumerate threats per boundary against the OWASP LLM Top 10 (injection, disclosure, poisoning, prompt leakage, excessive agency, unbounded consumption); write abuse cases from attacker behavior; rank risks by concrete exploit path; and map every mitigation to an owning skill plus a red-team/eval case. Composes threat-modeler for the classic STRIDE surface. Use when a feature contains a model call, retrieval step, or agent loop and needs a threat model or AI risk analysis. Do NOT use for non-AI features (threat-modeler), to design one specific defense (prompt-injection-defender, rag-security-architect), review a diff (security-pr-reviewer), or build/run red-team evals (ai-evaluation-harness).
---

# AI Threat Modeler

## Purpose

Produce a design-time threat model for an AI system — an LLM feature, RAG
pipeline, or agent — that treats the AI-specific attack surface as
first-class instead of bolting "prompt injection" onto a web threat model.
The output inventories AI assets and trust boundaries, enumerates threats per
boundary anchored to the OWASP LLM Top 10 (2025), writes abuse cases from
attacker behavior, ranks risks by concrete exploit path (not vibes), and maps
each accepted mitigation to the skill that owns building it and the red-team
or eval case that will prove it holds. The classic web/data surface is NOT
re-derived here — it composes `threat-modeler` output for the non-AI half.

## Use When

- Use when: designing or reviewing an LLM feature, RAG pipeline, agent, or
  AI integration that needs a threat model before (or after) it ships.
- Use when: asked "what could go wrong with this AI feature?", for an AI
  risk analysis, or to anchor AI security work to OWASP LLM Top 10 coverage.
- Use when: an AI feature is entering a security review and no AI threat
  model exists yet — this skill produces the map the reviews hang off.
- Do NOT use when: the feature has no model call, retrieval step, or agent
  loop — that is `threat-modeler`.
- Do NOT use when: designing one named defense in depth — injection defense
  is `prompt-injection-defender`, retrieval authorization is
  `rag-security-architect`, tool permissions are `agent-tool-safety-guard`.
- Do NOT use when: reviewing an actual code diff (`security-pr-reviewer`) or
  building/running red-team suites (`ai-evaluation-harness`).

## Inputs to Inspect

1. The feature design: what the model is asked to do, which model(s), what
   context is assembled, what the output drives (display, tools, writes).
2. Every content source feeding the model: user input, retrieved documents,
   webpages, tickets, emails, logs, tool outputs, prior model outputs — each
   is a trust boundary, untrusted by default.
3. The tool surface if agentic: tool list, per-tool side effects, granted
   credentials, approval gates already present.
4. Retrieval architecture if RAG: vector stores, ingestion sources, tenant
   scoping (compose `tenant-isolation-reviewer` findings, don't re-audit).
5. Existing threat models — `threat-modeler` output for the surrounding
   system; this skill extends it, never duplicates it.
6. Prompts and system instructions (what secrets/rules they carry), provider
   choice and data-handling posture, cost/quota controls already in place.

## Workflow

1. **Scope the AI system.** Name the model calls, context assembly, retrieval
   steps, tool invocations, and output sinks. Draw the data flow from every
   untrusted source to the model and from the model to every consumer. No
   design available → Stop Conditions.
2. **Inventory AI assets.** System prompts, model access/credentials, vector
   stores and their contents, fine-tuned weights/adapters, golden datasets,
   tool credentials, per-tenant data reachable through retrieval or tools,
   the AI budget itself (spend is an asset).
3. **Mark trust boundaries.** Every point where user input, retrieved
   documents, webpages, tickets, emails, logs, tool outputs, or model outputs
   enter a component is a boundary. Rule: untrusted content NEVER modifies
   system instructions, tool permissions, identity, access policy, or the
   execution plan — any place it could is a finding.
4. **Enumerate threats per boundary** using
   [references/llm-top10-threat-catalog.md](references/llm-top10-threat-catalog.md):
   map each applicable OWASP LLM Top 10 (2025) category to this system's
   concrete shape — injected instructions in retrieved docs (LLM01), tenant
   data in context (LLM02), poisoned corpus/adapter (LLM03/04), output-sink
   execution (LLM05), over-broad tools (LLM06), secrets in system prompt
   (LLM07), cross-tenant vectors (LLM08), fabricated answers driving actions
   (LLM09), token-drain loops (LLM10). Mark categories not applicable — with
   the reason — rather than skipping silently.
5. **Write abuse cases from attacker behavior.** "Attacker submits a support
   ticket containing instructions that make the summarizer call the refund
   tool" — concrete actor, path, and payoff. At least one abuse case per
   in-scope category.
6. **Rank by exploit path.** High severity REQUIRES a concrete path from
   attacker capability to impact (data theft, unauthorized action, money).
   Theoretical-only concerns are recorded as low/watch items, not inflated.
7. **Map mitigations to owners.** Each accepted risk gets: the mitigation,
   the owning skill that designs/builds it (`prompt-injection-defender`,
   `rag-security-architect`, `agent-tool-safety-guard`,
   `structured-output-validator`, `sensitive-disclosure-guard`,
   `system-prompt-leakage-reviewer`, `ai-cost-guardrail-designer`,
   `model-poisoning-reviewer`, `ai-misinformation-guard`, or a non-AI skill),
   and the red-team/eval case `ai-evaluation-harness` will encode. Deferred
   risks get a named acceptor via `human-approval-boundary`.
8. **Reconcile with the classic model.** Cross-check `threat-modeler` output
   for the surrounding system; list AI threats that ALSO have a classic
   variant (SSRF via model-emitted URL is both) once, with one owner.

## Output Format

```
AI THREAT MODEL — <feature/system>
System map: <model calls, context sources, retrieval, tools, output sinks>
Assets: <AI assets incl. prompts, stores, credentials, budget>
Trust boundaries: <each untrusted source → component entry point>
Threats (per boundary, OWASP LLM Top 10 anchored):
  [LLM0X] <threat in this system's concrete shape>
    Abuse case: <actor → path → payoff>
    Exploit path: <capability → impact> | Severity: <H/M/L + why>
    Mitigation: <control> → Owner: <skill> → Proof: <red-team/eval case>
Not applicable: <LLM0X — reason>
Classic-surface handoff: <items owned by threat-modeler / other skills>
Accepted/deferred risks: <risk — named acceptor — review date>
```

## Validation Checklist

- [ ] Every content source feeding the model is marked as a trust boundary
      (user input, retrieved docs, webpages, tickets, emails, logs, tool
      outputs, model outputs).
- [ ] All ten OWASP LLM Top 10 categories dispositioned: threat enumerated
      or explicitly not-applicable with a reason.
- [ ] Every threat has an abuse case written from attacker behavior.
- [ ] High severity is backed by a concrete exploit path to impact.
- [ ] Every mitigation names an owning skill AND a red-team/eval case.
- [ ] Classic (non-AI) threats are handed to `threat-modeler` output, not
      re-derived; overlaps listed once with one owner.
- [ ] Deferred risks carry a named human acceptor and review date.

## AI Security Rules

- User input, retrieved documents, webpages, tickets, emails, logs, tool
  outputs, and model outputs are untrusted unless explicitly proven
  otherwise; any flow where they can modify system instructions, tool
  permissions, identity, access policy, or the execution plan is a finding.
- A model output is attacker-influenced whenever any untrusted content was
  in context — treat downstream sinks accordingly.
- Severity is exploit-path-gated: no concrete path, no HIGH.
- Coverage claims are per-category and honest: "not applicable" needs a
  reason, "covered" needs an owner and a proof case.

## Gotchas

- The most common blind spot is INDIRECT injection: content nobody typed at
  the model (a calendar invite, a README, a scraped page) that the feature
  dutifully retrieves into context. Enumerate sources, not just the chat box.
- "The system prompt tells it not to" is not a mitigation — instructions are
  not enforcement. Route such findings to `system-prompt-leakage-reviewer`
  and deterministic controls.
- Cost is an asset: an attacker who can make you spend $50k in tokens never
  needs to steal data (LLM10). Model denial-of-wallet paths explicitly.
- Agent loops compound: one injected instruction can chain through tools;
  model the CHAIN (tool A's output feeds tool B's arguments), not just
  single calls.
- A threat model of the happy-path demo misses the feature's real surface —
  model the retries, fallbacks, caches, and background jobs too.
- Don't inflate: an LLM feature with no tools, no retrieval, and no tenant
  data has a genuinely small surface; say so instead of manufacturing risk.

## Stop Conditions

- No design, architecture, or code exists to model — stop; this skill models
  a described system, it does not invent one.
- The feature turns out to have no model call, retrieval, or agent loop —
  hand to `threat-modeler` and stop.
- Modeling reveals an apparently ACTIVE exploitation (injection already
  landing, budget already draining) — report immediately and route to
  `incident-response-runbook`; containment is a human decision.
- The risk acceptance decision itself (ship despite X) belongs to a named
  human via `human-approval-boundary` — never accepted silently here.

## Supporting Files

- [references/llm-top10-threat-catalog.md](references/llm-top10-threat-catalog.md)
  — per-category threat shapes, abuse-case seeds, and the applicability
  rubric for OWASP LLM Top 10 (2025).
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the threat & injection
  cluster and against `threat-modeler`, `security-pr-reviewer`, and the
  `ai-security-red-team-reviewer` subagent.
