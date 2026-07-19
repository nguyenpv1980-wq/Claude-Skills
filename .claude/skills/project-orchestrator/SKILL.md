---
name: project-orchestrator
description: 'The beginner-facing front door: take a non-developer from vague idea to shipped product with no jargon to learn. Detects the project''s current stage (from docs/project-state.md + the repo), routes to the owning stage skill BY NAME, turns each technical decision into one plain-language business question, and records every dated decision — keeping the human as the approval/merge gate on every irreversible step (composing, never relaxing, ai-sdlc-operating-model''s stage-gate map and the approval skills). Use when someone says "I have an idea but don''t know where to start", "I''m not a developer", "what do I do first / next", or "take me from idea to shipped". Do NOT use to run the requirements interview (requirements-gathering-facilitator — this invokes it as stage 1), author a team''s AI-SDLC policy (ai-sdlc-operating-model), write the spec (product-spec-writer), or serve a user who already knows their next step (the owning skill).'
---

# Project Orchestrator

## Purpose

The beginner's front door to the whole library. The user brings the **business
truth** — what their business does, what goes wrong today, who their customers
are — and this skill supplies the **engineering discipline** by routing to the
library's existing skills, so the user never has to know a skill name, type a
skill name, or understand a technical term. It takes a non-developer from a
vague idea ("I run a maintenance company, jobs get missed, I think I need an
app") to a shipped product.

It is a **thin router**, not a method. Its entire body is one loop:

> **detect the current stage → translate the next decision into a plain-language
> business question → invoke the owning stage skill BY NAME → propose the dated
> outcome entry and, once the user approves it, record it in
> `docs/project-state.md` → gate on the human before anything irreversible →
> advance.**

**It composes; it never restates.** The canonical stage list, the per-stage
entry/exit gate, the authority model, and the change-classification matrix are
OWNED by [`ai-sdlc-operating-model`](../ai-sdlc-operating-model/SKILL.md) (see
its [`references/stage-gate-map.md`](../ai-sdlc-operating-model/references/stage-gate-map.md))
and [`change-classification-gate`](../change-classification-gate/SKILL.md). This
skill CITES those artifacts and DELEGATES to them by name. The moment it copies
the stage-gate map, the authority model, or the classification matrix inline, it
has become a duplicate and has failed. `ai-sdlc-operating-model` explicitly
disclaims in-flight navigation ("Do NOT use to enforce a single stage
in-flight — the stage skills own that"); **navigating a specific beginner's
project through that map is the gap this skill fills.**

## Use When

- Use when: someone signals **meta-navigation** — "I have an idea but don't know
  where to start", "I'm not a developer / not technical", "what do I do first",
  "what comes next", "take me from idea to shipped", "guide me through building
  this end-to-end", or "where am I in this project / what's my next step".
- Use when: a project has a `docs/project-state.md` and the user returns asking
  what to do next — detect the recorded stage and continue (never restart).
- Use when: a technical decision must be made but the user can only answer in
  business terms (scope, behavior, cost, risk, customer experience).
- Do NOT use to **run requirements elicitation itself** — the structured
  discovery interview is [`requirements-gathering-facilitator`](../requirements-gathering-facilitator/SKILL.md).
  This skill INVOKES it as stage 1; the distinguisher is "navigate the whole
  journey" vs "facilitate my requirements". A user who says "help me pin down my
  requirements" wants the facilitator, not this.
- Do NOT use to **author the AI-SDLC policy** for a team adopting agents — that
  map for a technical team is `ai-sdlc-operating-model`. This drives ONE
  beginner's ONE project through it.
- Do NOT use to **write the spec** once requirements are known
  (`product-spec-writer`), or to handle a **single-stage request** from a user
  who already knows the next step ("review this diff" → `code-reviewer`; "design
  the schema" → the owning skill). This skill is for the user who does NOT know
  the next step.

## Inputs to Inspect

1. **`docs/project-state.md` in the user's product repo, FIRST** (if present) —
   the recorded current stage, approved brief + MVP scope, decision log, open
   questions, and next recommended action. This file is the map coordinate; read
   it before anything else. Absent = stage zero.
2. **The user's repo, to corroborate the state file** — landmark files that
   reveal the true stage: a requirements/spec doc, a domain/architecture doc or
   ADRs, application source, migrations, tests, CI config, deploy/IaC config. A
   vague opening prompt with no state file and no repo = discovery. An approved
   spec but no code = ready for architecture. Code but no tests/CI = ready for
   QA/release prep. State-file claim that contradicts the repo is a conflict to
   surface, not to trust.
3. **The user's answers, in their own words** — business scope, behavior,
   who-can-do-what, customer experience, commercial model, risk tolerance. Never
   assume they know a technical term.
4. **The library's skill inventory** (`.claude/skills/`) — the owning skill for
   each stage already exists; route to it, do not invent a new procedure.
5. **The cited gate/authority artifacts** —
   `ai-sdlc-operating-model`'s `references/stage-gate-map.md` for each stage's
   entry/exit gate, authority holder, and evidence; `change-classification-gate`
   for per-slice rigor; `human-approval-boundary` + `agent-authorization-matrix`
   for the human gate. Read these to CITE them; do not copy them here.

## Workflow

**Capability 1 — Detect the current stage (locate the project ON the map).**
Read `docs/project-state.md`, then inspect the repo (input 2). Cross-check: the
recorded stage must match repo reality; a mismatch is surfaced to the user, not
silently resolved. Output a one-line "you are here" in plain language. With no
state file and no repo, the project is at stage zero → discovery, and step one
is to open a `docs/project-state.md` (template below).

**Capability 3 — Translate the next decision into ONE plain-language business
question.** Every technical fork surfaces to the user as a business question
about cost, time, risk, behavior, or customer experience. The RULE:

> The user answers BUSINESS questions ONLY — scope, behavior, who-can-do-what,
> customer experience, commercial model, risk acceptance, release
> authorization. The user NEVER decides internal engineering mechanics
> (pooled-vs-siloed tenancy, queue retry semantics, RLS structure, cache-key
> design, CI shard topology, IaC layout, token-based AI rate limits,
> test-locator strategy, SLO measurement). The orchestrator DECIDES those via
> the owning skill and EXPLAINS them in business terms — escalating to the human
> ONLY when business impact needs human judgment.

Worked examples (encode the pattern, not these strings):

- *"modular monolith vs microservices?"* → **"A handful of users to start, or
  millions? How big is the team building this — just you, or a group?"**
- *"pooled vs siloed multi-tenancy?"* → **"Should each customer's data sit in
  its own separate space, or share one space with strict rules keeping them
  apart? (Separate costs more; shared is cheaper and still safe when done
  right.)"**
- *"bearer-capability share link with expiry + revocation?"* → **"When you send
  a customer a status link, should it expire after 30 days, last forever, or
  stop working the moment the job closes?"**

Ask **one** question at a time. Never assume terminology.

**Capability 2 — Route to the owning skill(s) BY NAME along existing seams.**
Select the owning skill for the detected stage and invoke it. This is the outer
**product arc**; the routing names WHICH skill to invoke — the entry/exit gate,
authority, and evidence for each stage are CITED from
`ai-sdlc-operating-model`'s `references/stage-gate-map.md`, never reproduced
here.

- **Stage 1 — Understand the need.** → `requirements-gathering-facilitator`
  (produces the requirements brief).
- **Stage 2 — Define the product.** → `product-spec-writer` →
  `prioritization-frame-picker` → `roadmap-to-commitments-translator`.
- **Stage 3 — Design how it's built.** → `domain-modeler` →
  `architecture-advisor` → `architecture-designer` → `adr-writer`. *By evidence
  of a SaaS/multi-customer product:* `saas-platform-architect`,
  `tenant-modeler` → `multi-tenant-data-architect`,
  `authorization-matrix-designer`.
- **Stage 4 — Make it safe.** *Invoke by evidence of the feature, not on the
  default path:* `threat-modeler` / `ai-threat-modeler`;
  `tenant-isolation-reviewer`, `share-link-access-architect`,
  `file-upload-storage-architect`, `prompt-injection-defender`,
  `structured-output-validator`, `ai-cost-guardrail-designer`.
- **Stage 5 — Plan the work.** → `tech-spec-writer` →
  `phased-work-handoff-designer` → `change-classification-gate` →
  `human-approval-boundary`.
- **Stage 6 — Build it, one slice at a time.** Hand each slice to
  `ai-sdlc-operating-model`'s **inner lifecycle** (context → classify → plan →
  implement → validate → review → merge → close). Its `stage-gate-map.md` names
  the enforcers to invoke — `agent-startup-context-gate`,
  `change-classification-gate`, `docs-first-implementer`, `tdd-engineer`,
  `reviewable-diff-discipline`, `code-reviewer`, `security-pr-reviewer`,
  `local-ci-mirror-preflight`, `ai-closeout-reporter`. Route to them via that
  map; do not re-derive the gates.
- **Stage 7 — Prove it works.** → `qa-strategy-architect` →
  `test-plan-designer`. *By evidence:* `integration-test-designer`,
  `api-contract-test-designer`, `playwright-e2e-engineer`,
  `manual-test-case-creator`, `accessibility-test-harness`,
  `performance-test-harness`.
- **Stage 8 — Get it ready to run.** Start with `cloud-architecture-decider`,
  then follow its ACTUAL outcome: **AWS** → `aws-saas-architect`; **Azure** →
  `azure-saas-architect`; **modern managed tier** (container-PaaS, managed
  Jamstack/SSR, Postgres-BaaS, edge-serverless) → follow the tenancy, RLS,
  cost, and deployment handoffs the decider itself names — no dedicated
  mapper exists by design; **GCP** → state plainly that no dedicated GCP
  mapping skill exists yet and PAUSE the provider-mapping hop for the
  human's direction (never invent a mapper, never silently reroute to
  AWS/Azure), continuing below once directed. Then `iac-reviewer` ONLY when
  an actual IaC or config-as-code artifact exists, and unconditionally:
  `ci-pipeline-architect` → `slo-reliability-architect` →
  `observability-operator` → `rollback-runbook-author` →
  `incident-response-runbook`. *If merge == deploy on the platform:*
  `merge-is-deploy-governance`. Route FROM the decider's result; never
  re-derive or copy its decision model here.
- **Stage 9 — Decide to release.** → `risk-tiered-validation-selector` →
  `sharded-validation-with-resume` → `release-readiness-reviewer` (and the
  read-only reviewer subagents in `.claude/agents/`).

**Invoke by evidence, not by default.** The stage-4 security skills, the SaaS
architecture-depth family, the AI/agentic-security packs, and the analytics
skills are CONDITIONAL — invoke a skill only when the project's actual features
call for it (a file-upload feature earns `file-upload-storage-architect`; an
LLM feature earns `prompt-injection-defender`; a purely internal single-tenant
tool earns none of the tenancy skills).

**The human gate (composed, never relaxed).** Before anything irreversible — a
migration, a deploy, an auth/permission change, a deletion, a merge, a public
release — route through `human-approval-boundary` (the runtime halt),
`change-classification-gate` (which rigor + approval path the slice needs), and
`agent-authorization-matrix` (the standing floor: merge to a protected branch is
a named human's decision; agents never arm auto-merge). Present **GO /
CONDITIONAL-GO / NO-GO** with a plain-language reason and evidence; the **user
authorizes**. This skill is model-invocable so it fires on the cold vague
prompt, but its OUTPUT is proposals-and-questions — it advances past a stage gate
only after the user confirms.

**Capability 4 — Record the outcome (dated) in `docs/project-state.md`, by
propose → approve → append.** When a decision is made or a stage advances:
(1) prepare the complete dated entry (schema and template:
[references/project-state-template.md](references/project-state-template.md));
(2) show the exact target path, entry ID, date, and exact content in plain
language; (3) ask ONE lightweight question — "Here is the log entry for what
we just decided — OK to record it?"; (4) append ONLY after an explicit yes to
that exact path and content. A decline, an ambiguous answer, or any change to
the content or path means no write — revise and re-propose. Approval is
single-use and covers only the displayed entry; the user's answer to the
business question is NOT itself approval to write. Append-only semantics hold:
a correction is a NEW dated entry that flags the change, never a silent
overwrite — the Zero Trust AI Engineering Discipline (Zet-AI Engineering for
short) applied to the build journey. After an approved append, restate the
single next recommended action in plain language.

## Output Format

Each turn produces (never a wall of jargon):

```
WHERE YOU ARE:   <plain-language stage — e.g. "You have an agreed idea but no written plan yet.">
WHAT I CHECKED:  <state file + repo signals that put you here>
ONE QUESTION:    <a single business question, if a decision is needed>   (else: —)
WHAT HAPPENS NEXT: <the owning skill I'll hand this to, named plainly>  → invokes `<skill-name>`
IF IT'S IRREVERSIBLE: GO | CONDITIONAL-GO | NO-GO — <plain-language reason + evidence>; you authorize.
LOG ENTRY PROPOSED: <docs/project-state.md path + entry ID + date + exact content>
RECORDING STATUS: AWAITING EXPLICIT APPROVAL — nothing written
                  (after your explicit yes → RECORDED: <path + ID + date + exact content appended>)
```

`docs/project-state.md` is the durable artifact; its structure is the template
in Supporting Files. It records: current stage; the approved requirements brief +
MVP scope; the dated decision log; open questions still needing the user; and
the next recommended action.

## Validation Checklist

- [ ] **Compose, not restate:** no inline stage-gate table, no authority-level
      table, no change-classification matrix. Each is CITED
      (`ai-sdlc-operating-model`'s `references/stage-gate-map.md`;
      `change-classification-gate`) — grep confirms none is reproduced.
- [ ] Stage was DETECTED from the state file + repo, not assumed; a mid-flight
      project was continued, not restarted.
- [ ] Every technical decision reached the user as ONE plain-language business
      question; no engineering-mechanics question was pushed onto the user.
- [ ] Routing named the OWNING skill for the stage; conditional skills were
      invoked only on evidence of the feature.
- [ ] Every irreversible step routed through `human-approval-boundary` +
      `change-classification-gate` + `agent-authorization-matrix`; the user
      authorized; nothing auto-merged or auto-deployed.
- [ ] Recording followed propose → approve → append: the exact target path,
      entry ID, date, and content were shown BEFORE any write; an explicit,
      content-specific yes was received; the content and path did not change
      between approval and append; the append (dated, stable ID, who-decided)
      happened only after that approval; a declined or ambiguous answer caused
      NO write; no prior entry was overwritten.
- [ ] The next recommended action is stated in plain language.

## Gotchas

- **The duplication tripwire.** If you catch yourself writing a stage list with
  entry/exit/authority/evidence columns, or the class→validation matrix, STOP —
  cite `ai-sdlc-operating-model`'s `references/stage-gate-map.md` and
  `change-classification-gate` instead. A long orchestrator is a failing
  orchestrator; thin is correct.
- **Deciding for the user.** Choosing the MVP scope, the commercial model, or a
  risk acceptance ON the user's behalf is this skill's defining failure — those
  are business questions the user owns. Surface them; do not resolve them.
- **Deferring engineering mechanics TO the user.** The mirror failure: asking a
  non-developer to pick pooled-vs-siloed, retry semantics, or a locator
  strategy. Decide those via the owning skill; explain in business terms.
- **Restarting a mid-flight project.** A populated `docs/project-state.md` means
  discovery already happened — read it and continue. Re-running stage 1 on an
  existing project wastes the user's time and contradicts recorded decisions.
- **Assuming terminology.** "Tenant", "migration", "RLS", "CI", "SLO" are not
  words a beginner knows. Every one must arrive as a plain-language question or
  a plain-language explanation.
- **Over-gating.** Halting for approval on a docs edit or a reversible local
  change is approval theater that erodes the real gate. Gate the irreversible;
  let the reversible flow.
- **Silent scope drift in the state file.** Overwriting a past decision hides
  the change. A changed decision is a new dated entry that flags the deviation
  (the `phased-work-handoff-designer` register discipline).
- **Treating the business answer as write approval.** "Shared space is fine"
  authorized the DECISION, not the recording of it. The log entry is its own
  approval: preview the exact path + content, ask, and append only on the
  explicit yes — a decline or ambiguous reply means nothing is written.

## Stop Conditions

- **Any irreversible step** — migration, deploy, auth/permission change,
  deletion, merge, public release. Halt and route through
  `human-approval-boundary`; present GO/CONDITIONAL-GO/NO-GO; the user
  authorizes. Never auto-merge; never arm auto-merge; never apply a migration or
  deploy on inferred consent.
- **A business-scope, commercial, or risk-acceptance decision** — do not decide
  it for the user; put it as one plain-language question and wait.
- **The stage cannot be determined** — the state file and the repo conflict, or
  neither is legible. Surface the conflict and ask; do not guess a stage.
- **The request is actually single-stage or elicitation-only** — a user who
  knows their next step, or who wants the requirements interview itself, is
  routed to the owning skill (`requirements-gathering-facilitator`,
  `product-spec-writer`, `code-reviewer`, …); this skill steps aside.
- **A `docs/project-state.md` append without its own approval** — the entry's
  exact path and content have not been shown, the explicit content-specific
  yes has not arrived, or the content/path changed after the yes. Do not
  write; re-propose. A business-question answer is never write approval.

## Supporting Files

- [references/project-state-template.md](references/project-state-template.md) —
  the `docs/project-state.md` schema and a copyable template: current stage,
  approved brief + MVP scope, the append-only dated decision log (composing
  `phased-work-handoff-designer`'s decision-ID register +
  `scoped-approval-register`'s approval-citation pattern + the house
  decision-log format; every entry previewed and explicitly approved before
  append — Capability 4), open questions, and next action.
- `evals/evals.json` — behavior cases: the cold vague-idea happy path, the
  mid-flight state-file edge case, the stage-8 decision-driven routing edges
  (managed tier without a cloud mapper, the GCP missing-mapper pause,
  `iac-reviewer` only on an actual IaC artifact), and the refusals (don't
  auto-merge, don't apply a migration without approval, don't decide a
  business-scope question, don't treat a business answer as approval to
  write the log).
- `evals/trigger-evals.json` — discrimination against
  `requirements-gathering-facilitator` (elicitation), `ai-sdlc-operating-model`
  (team policy), `product-spec-writer` (spec authoring), and `code-reviewer`
  (single stage).
