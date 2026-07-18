---
name: model-context-designer
description: 'Design what enters and leaves a model''s context window — a curated diet, not open access: context assembled SERVER-SIDE under hard token/size caps; every input passes a CLOSED schema; secrets/PII/raw payloads minimized or carried on a transient never-persisted channel with the persisted-vs-transient split explicit; what the model saw RECONSTRUCTIBLE afterward; exclusions designed and documented, never accidental. The context window is a supply chain — an unverified input is an unverified output. Distinct from agent-startup-context-gate (session-START loading; this is runtime per-call assembly), ai-cost-guardrail-designer (prices the spend; this decides the CONTENT), and rag-security-architect (who may retrieve; this curates what retrieval feeds the window). Use when designing prompt/context assembly, deciding what an agent may see, or when context is stuffed ad hoc. DESIGNS the curated context; the poisoning attack review belongs to memory-context-poisoning-reviewer.'
---

# Model Context Designer

## Purpose

The context window is a supply chain: an unverified input is an unverified
output. This skill designs that supply chain — what enters and leaves a
model's context window on every call. The deliverable is a context design
with six load-bearing parts: (1) context assembled SERVER-SIDE from vetted
parts, never handed to the model as open access to a data source; (2) hard
token/size caps per segment and in total, with deterministic priority and
truncation rules; (3) CLOSED input schemas — every segment that enters the
window passes a defined shape; (4) secrets, personal data, and raw payloads
minimized, and what must ride anyway carried on a transient never-persisted
channel, with the persisted-vs-transient split explicit per segment; (5)
reconstructibility — what the model saw on any past call can be established
afterward; and (6) designed exclusions — what is deliberately NOT in the
window, documented with reasons, so absence is a decision rather than an
accident. This skill DESIGNS the curated context; the security review of
context and memory for poisoning belongs to
`memory-context-poisoning-reviewer` — it PRODUCES the artifact that skill
reviews.

## Use When

- Use when: designing or overhauling how a prompt/context is assembled for a
  model call — which segments, from where, in what order, under what caps.
- Use when: deciding what data an AI feature or agent may see — the model
  currently gets a whole record, table, or document dump because scoping was
  never designed.
- Use when: secrets, personal data, or raw payloads are landing in prompts
  and prompt logs, and the persisted-vs-transient question has no answer.
- Use when: nobody can say afterward what the model saw for a given call, or
  what was left out of the window and why.
- Auto-invocable: a pure design skill — it produces a context specification
  and changes no live system or data flow.
- Do NOT use when: the job is the ATTACK REVIEW of context or memory — can
  untrusted content poison what gets stored and trusted later — that is
  `memory-context-poisoning-reviewer`. This skill DESIGNS the curated
  context; the security review of it belongs to that skill.
- Do NOT use when: the subject is session-START context — verifying the repo,
  loading governing docs before work begins — that is
  `agent-startup-context-gate`; this skill owns RUNTIME per-call context
  assembly, a different moment with a different failure mode.
- Do NOT use when: the question is the token/spend BUDGET itself — caps as
  cost policy are `ai-cost-guardrail-designer`; the cap is a cost decision,
  the curation is a content decision, and this skill designs content within
  the caps that skill prices.
- Do NOT use when: the question is retrieval AUTHORIZATION — who may retrieve
  which documents is `rag-security-architect`; this skill curates what the
  (already-authorized) retrieval feeds the window.
- Do NOT use when: the subject is redaction mechanics and output-path echo
  checks for sensitive data — that is `sensitive-disclosure-guard`; this
  skill decides the context diet those controls apply to.
- Do NOT use when: the question is gating the CALL — identity, authority,
  budget rungs — that is `agent-harness-architect`; the harness gates the
  call, this skill curates what rides in it.

## Inputs to Inspect

1. Every context source feeding the call today: system instructions, user
   input, conversation history, retrieved documents, tool outputs, memory,
   ambient state — with each source's trust class and current size behavior.
2. How assembly happens now: server-side composition from vetted parts vs
   client-assembled strings vs the model holding a live connection to a data
   source (open access — the anti-pattern).
3. What downstream persists: prompt logs, traces, conversation stores — and
   whether secrets/PII currently land in any of them.
4. The spend caps in force (`ai-cost-guardrail-designer` output if present):
   the budget the content design must fit inside.
5. The retrieval layer's authorization posture (`rag-security-architect`
   output if present): what the retriever is allowed to return — the
   ceiling on what curation can admit.
6. Reconstruction demands: audit, compliance, or debugging requirements to
   show what the model saw for a past call, and any retention limits pulling
   the other way.
7. The consumers of model output: what downstream trusts the answer, which
   determines how much an unverified input costs.

## Workflow

1. **Inventory the segments.** Name every candidate segment for the window
   (instructions, user input, history, retrieved content, tool output,
   memory) with its source, trust class, and size behavior. A segment nobody
   can name is a segment nobody is curating.
2. **Assemble server-side.** The final context is composed server-side from
   vetted parts. The model never gets open access to a store "so it has
   everything" — a curated diet, not access. Client-supplied fragments are
   inputs to validation, never pre-assembled context.
3. **Set hard caps with deterministic degradation.** A token/size cap per
   segment and in total. When content exceeds a cap, what is dropped or
   summarized follows a designed priority order — not "whatever fit last".
   The caps' PRICE comes from `ai-cost-guardrail-designer`; this step decides
   what the capped space carries.
4. **Close the input schemas.** Every segment entering the window passes a
   closed schema: shape, size, and allowed content class. Free-form blobs
   are the exception and are named as such. An input that fails its schema
   does not enter the window — the supply chain rejects unverified goods at
   the dock, not after they ship.
5. **Minimize and split persisted-vs-transient.** Secrets, personal data,
   and raw payloads: first minimize (does the model need the value, or a
   reference/derivative?); what must ride anyway goes on a transient
   never-persisted channel. Mark every segment PERSISTED or TRANSIENT
   explicitly — an unmarked segment defaults to the strictest treatment.
6. **Design reconstructibility honestly.** What the model saw must be
   establishable afterward: persisted segments by content or
   reference+version; transient segments by class, shape, and hash — never
   by storing the sensitive content that was excluded from persistence.
   State the honest trade: reconstruction of transient segments proves WHAT
   KIND of thing rode along, not its verbatim value. Where a verbatim
   requirement and a never-persist requirement collide → Stop Conditions.
7. **Design the exclusions.** List what is deliberately NOT in the window —
   other tenants' data, unscoped history, whole-record dumps, standing
   secrets — each with its reason. Absence must be a documented decision; an
   accidental exclusion is a bug wearing a compliance costume, and an
   accidental inclusion is a leak.
8. **Prove the caps and exclusions can fail.** Design the tests: over-cap
   input is truncated by the designed priority (not silently admitted); a
   schema-failing segment is rejected; an excluded class is demonstrably
   absent from an assembled context; a transient segment is demonstrably
   absent from every persisted store. A verifier that cannot fail is theater
   with an exit code.
9. **Deliver the design** in the Output Format, seams cited: poisoning
   review, session-start gate, cost policy, retrieval authz, disclosure
   mechanics — composed, never restated.

## Output Format

```
MODEL CONTEXT DESIGN — <feature/agent>
Principle: the context window is a supply chain — an unverified input is an
  unverified output; a curated diet, not open access.
Segments: <name — source — trust class — schema — cap — priority —
  PERSISTED|TRANSIENT>
Assembly: <server-side composer; order; what happens on over-cap (designed
  degradation); no open-access paths>
Input schemas: <per segment: shape/size/content class; rejection behavior>
Minimization: <secret/PII/raw-payload decisions: value vs reference vs
  derivative; the transient channel and its guarantees>
Reconstructibility: <per segment: content | reference+version | class+hash;
  the honest limit on transient segments>
Exclusions (designed): <what is NOT in the window — each with reason>
Failure proofs: <over-cap, schema-reject, exclusion-absence,
  transient-not-persisted — the test for each>
Handoffs: poisoning attack review → memory-context-poisoning-reviewer;
  session-start context → agent-startup-context-gate; spend caps →
  ai-cost-guardrail-designer; retrieval authz → rag-security-architect;
  redaction/echo mechanics → sensitive-disclosure-guard; call gating →
  agent-harness-architect
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every segment is named with source, trust class, schema, cap,
      priority, and an explicit PERSISTED or TRANSIENT mark.
- [ ] Assembly is server-side from vetted parts; no path gives the model
      open access to a data source in place of curated content.
- [ ] Hard caps exist per segment and in total, with deterministic,
      designed degradation — never "whatever fit".
- [ ] Every input passes a closed schema before entering the window;
      schema failures are rejected, not admitted.
- [ ] Secrets/PII/raw payloads are minimized first; what rides is on the
      transient never-persisted channel; the split is explicit.
- [ ] What the model saw is reconstructible afterward, with the transient
      limitation stated honestly (class/shape/hash, never stored content).
- [ ] Exclusions are designed and documented with reasons — nothing is
      absent (or present) by accident.
- [ ] Every cap, schema, exclusion, and transient guarantee has a designed
      proof it can fail.
- [ ] The yields are stated: poisoning review →
      memory-context-poisoning-reviewer; neighboring lanes cited, not
      restated.

## Gotchas

- "Give the model everything so it has context" is the anti-pattern this
  skill exists to replace: open access is not context engineering, it is
  the absence of it — and every unverified byte admitted is an unverified
  byte in the answer.
- Prompt logs are where transient data goes to become permanent: the
  never-persisted channel must be checked against EVERY store — traces,
  analytics, conversation history, error reports — not just the obvious log.
- A cap without a designed priority order silently drops the most important
  segment on the worst day; "truncate from the end" is a decision, make it
  deliberately.
- Reconstructibility promised as "we log the full prompt" contradicts the
  transient channel the moment a secret rides along — the honest design
  records class+hash for transient segments and says so.
- History is a segment too: unbounded conversation history is the cap
  violation everyone forgets, and yesterday's unvetted content re-enters
  today's window through it.
- An exclusion nobody wrote down gets "fixed" by the next engineer who
  notices the model lacks the data — designed exclusions carry their reason
  precisely so helpfulness doesn't reverse them.
- Schema-valid is not trust: a closed schema bounds shape and class, it does
  not make retrieved content's INSTRUCTIONS safe — injected instructions in
  admitted content are `prompt-injection-defender`'s lane; say so, don't
  solve it here.

## Stop Conditions

- A verbatim-reconstruction requirement and a never-persist requirement
  collide on the same segment (compliance wants the exact content, policy
  forbids storing it) → surface the conflict with the honest options
  (reference+version, class+hash, scoped retention with its own controls)
  and stop for a human decision; do not promise both absolutes.
- The context sources themselves are unknown — nobody can name what feeds
  the window today → inventory first; a curation design over an unknown
  supply chain is fiction.
- The request is to widen the diet to open access (a live connection to a
  store in place of curated segments) → refuse the open-access design,
  present the curated alternative, and escalate if the requirement survives.
- Wiring the design into a live pipeline (changing what production prompts
  contain) → implementation under the repo's approval path; this skill
  designs, it does not deploy.
- The real concern is poisoning of stored memory/context, retrieval
  authorization, or redaction mechanics → hand to
  `memory-context-poisoning-reviewer` / `rag-security-architect` /
  `sensitive-disclosure-guard` and stop.

## Supporting Files

- `evals/evals.json` — behavior cases: the ad-hoc context-stuffing design,
  the secrets-in-prompt-logs split, the reconstruction-vs-never-persist
  edge, the open-access refusal, and the poisoning-review
  should-not-trigger.
- `evals/trigger-evals.json` — discrimination against
  `agent-startup-context-gate` (session-start vs per-call runtime),
  `ai-cost-guardrail-designer` (cap price vs content),
  `rag-security-architect` (retrieval authz vs curation),
  `sensitive-disclosure-guard` (redaction mechanics),
  `agent-harness-architect` (in-batch: call gating vs context content), and
  the design-vs-review seam against `memory-context-poisoning-reviewer`.
- No `references/` — the context contract above is the complete procedure;
  detail lives in the produced design artifact.
