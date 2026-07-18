---
name: agent-harness-architect
description: 'Design the governed operating environment an AI agent runs inside — the harness: ONE server-side mediation point every model/tool call crosses; identity from credentials (never from model-supplied payload), propagated; a deny-by-default pre-flight ladder (authenticate → authorize → entitlement → budget → input policy) BEFORE the model runs, each rung fail-closed; a CLOSED tool/provider registry (unknown capability fails, never improvised); instructions as server-side versioned artifacts no untrusted party can override; a fail-closed audit write — what cannot be recorded does not execute. The AI-specific harness atop command-gateway-architect''s mediated path, enforcing agent-authorization-matrix''s policy. Use when wiring an agent into a runtime or when model calls run ungoverned. DESIGNS the harness; its attack review belongs to agent-tool-safety-guard, agent-containment-reviewer, prompt-injection-defender. Do NOT use for loop bounds/stops (agentic-loop-designer) or context content (model-context-designer).'
---

# Agent Harness Architect

## Purpose

An agent's authority is a property of its environment, not of its obedience.
This skill designs that environment — the harness: the governed runtime every
model call and tool call of an AI agent passes through. The deliverable is a
harness design with six load-bearing parts: (1) ONE server-side mediation
point no model or tool call can go around; (2) caller identity verified from
credentials — never from anything the model or client supplies in a payload —
and propagated to every downstream check; (3) a deny-by-default pre-flight
ladder (authenticate → authorize → entitlement → budget → input policy)
walked BEFORE the model runs, each rung fail-closed; (4) a CLOSED
tool/provider registry, where an unknown capability fails instead of being
improvised; (5) system instructions held as server-side versioned artifacts
no untrusted party can supply or override; and (6) a fail-closed audit write —
an action that cannot be recorded does not execute. This skill DESIGNS the
harness; the security review of the harness — injection paths, tool misuse,
containment — belongs to `prompt-injection-defender`,
`agent-tool-safety-guard`, and `agent-containment-reviewer`. It PRODUCES the
artifact those skills review.

## Use When

- Use when: building or overhauling the runtime environment an AI agent or
  LLM feature runs inside — where calls are gated, identity is established,
  tools are registered, instructions live, and actions are recorded.
- Use when: model/tool calls run ungoverned — call sites reach providers or
  tools directly, each doing its own checks (or none), and the agent's limits
  exist only as prompt text asking it to behave.
- Use when: an agent is being wired into a product and its authority needs to
  become environmental (checks it cannot skip) rather than behavioral
  (instructions it is trusted to obey).
- Auto-invocable: a pure design skill — it produces a spec and changes no
  live system, wires no credentials, and grants no authority.
- Do NOT use when: the job is the ATTACK REVIEW of a harness — injection
  paths are `prompt-injection-defender`, tool misuse / excessive agency is
  `agent-tool-safety-guard`, cascade/rogue containment is
  `agent-containment-reviewer`. This skill DESIGNS the harness; the security
  review of the harness belongs to those skills.
- Do NOT use when: the subject is the general server-mediated WRITE path for
  a product's protected mutations — that is `command-gateway-architect`; this
  skill builds the AI-specific harness ON TOP of that pattern and cites it,
  never restates it.
- Do NOT use when: the question is the agentic loop's iteration bounds, retry
  typing, or stopping semantics — that is `agentic-loop-designer`; the loop
  runs INSIDE this harness, and every call an iteration makes still passes
  this harness's ladder.
- Do NOT use when: deciding what CONTENT fills the model's context window —
  that is `model-context-designer` (the harness gates the call; the context
  designer curates what rides in it).
- Do NOT use when: authoring the standing human-vs-agent authority POLICY —
  that is `agent-authorization-matrix`; this environment ENFORCES that
  matrix, it does not define it.
- Do NOT use when: designing model/provider routing internals (selection,
  fallback, key custody) — that is `ai-router-architect`; the harness governs
  what the router may reach.

## Inputs to Inspect

1. Every model-call and tool-call site: which paths reach a provider or a
   tool today, and which of them pass through any shared mediation vs calling
   directly.
2. The identity story per call: where the acting identity comes from —
   verified credentials/session vs anything supplied in a model output,
   request body, or prompt — and whether it is propagated or re-asserted
   downstream.
3. The standing authority policy: `agent-authorization-matrix` output if
   present — the matrix this environment must enforce; without it the ladder
   has no authorize rung to call.
4. Existing mediation infrastructure: a `command-gateway-architect`-style
   command bus or gateway the harness can extend rather than duplicate.
5. The tool/provider surface: every tool, function, and model the agent can
   reach today, and how one gets added (governed registry change vs ad-hoc).
6. Instruction custody: where system instructions live — versioned server
   artifact vs string in client code vs assembled from parts an untrusted
   party can influence.
7. Audit posture: what is recorded per call today, and what happens when
   that write fails (does the action proceed unrecorded?).
8. Budget/entitlement sources: the caps and plan gates the ladder's budget
   and entitlement rungs will consume (`ai-cost-guardrail-designer`,
   `plan-entitlement-architect` outputs if present).

## Workflow

1. **Fix the single mediation point.** Name the one server-side component
   every model and tool call passes through, and enumerate every current
   around-path (direct SDK calls, client-side keys, ad-hoc tool shims). The
   design must close each one — a harness with a bypass is documentation,
   not a control.
2. **Design identity: credentials only, propagated always.** The acting
   user/agent identity is established from verified credentials or session at
   the mediation point and propagated to every downstream check. Nothing —
   not a model output, not a tool argument, not a prompt segment — may assert
   identity. Flag every place identity is currently read from a payload.
3. **Design the pre-flight ladder, deny-by-default, fail-closed.** Fixed
   order, all rungs BEFORE the model runs: **authenticate** (who is calling)
   → **authorize** (may this identity perform this action — calls the
   `agent-authorization-matrix` policy, never re-authors it) → **entitlement**
   (does the plan/tenant include this capability) → **budget** (is there
   spend/quota left — caps consumed from `ai-cost-guardrail-designer`) →
   **input policy** (does the input pass the closed schema and content
   rules). Each rung fail-closed: a rung that errors DENIES the call. A rung
   evaluated after the model has already run is not pre-flight — the spend
   and the exposure already happened.
4. **Close the registry.** The tool/provider registry is a closed, versioned
   list: a capability not in it FAILS — it is never improvised, auto-wrapped,
   or "gracefully" substituted. Adding a capability is a governed registry
   change with an owner, not a runtime event. The registry also scopes what
   `ai-router-architect`'s routing may reach.
5. **Put instructions in server custody.** System instructions are
   server-side versioned artifacts: source-controlled, deployed like code,
   selected by the server per call. No untrusted party — user, retrieved
   document, tool output, client code — can supply or override them. Record
   which instruction version served each call.
6. **Make the audit write fail-closed.** Every mediated call records actor,
   action, target, instruction version, ladder outcome, and result — and the
   write is part of the action's critical path: an action that cannot be
   recorded does not execute. Record-or-refuse, never act-then-hope. The
   audit record schema itself is `audit-log-architect`'s.
7. **Prove every deny path can fire.** For each ladder rung, the closed
   registry, and the audit write, design the test that proves it can reject:
   an unauthenticated call denied, an unauthorized action denied, an
   over-budget call denied, an unknown tool failed, an audit-down action
   refused. A verifier that cannot fail is theater with an exit code — a
   rung that has never rejected anything in a test is unproven.
8. **Deliver the design** in the Output Format, with every seam named as a
   handoff — the policy, the write-path pattern, routing, loop semantics,
   context content, and the attack review — composed, never restated.

## Output Format

```
AGENT HARNESS DESIGN — <system/agent>
Invariant: no model/tool call around the mediation point; authority is a
  property of the environment (enforces agent-authorization-matrix), not of
  the agent's obedience.
Mediation point: <the one server-side component; every around-path + its closure>
Identity: <credential/session source → verification → propagation;
  model-supplied identity rejected everywhere>
Pre-flight ladder (fixed order, BEFORE the model runs, each rung fail-closed):
  authenticate → authorize(<policy source>) → entitlement(<plan source>) →
  budget(<cap source>) → input-policy(<schema/content rules>)
Registry: <closed tool/provider list; unknown capability = fail; change process>
Instruction custody: <server-side versioned artifacts; version pinned per call;
  who may change them>
Audit: <record fields; fail-closed rule: cannot-record ⇒ does-not-execute>
Deny-path proofs: <per rung/registry/audit: the test that proves it can reject>
Handoffs: authority policy → agent-authorization-matrix; mediated write-path
  pattern → command-gateway-architect; routing → ai-router-architect;
  loop semantics → agentic-loop-designer; context content →
  model-context-designer; audit schema → audit-log-architect;
  attack review → prompt-injection-defender + agent-tool-safety-guard +
  agent-containment-reviewer
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every model and tool call passes the ONE mediation point; every
      around-path is enumerated and closed, not just discouraged.
- [ ] Identity comes from verified credentials only and is propagated; no
      check anywhere accepts model-supplied or payload-supplied identity.
- [ ] The ladder is deny-by-default, fixed-order, entirely pre-flight, and
      every rung fail-closed (an erroring rung denies).
- [ ] The authorize rung CALLS the standing authority policy
      (`agent-authorization-matrix`); it does not re-author it.
- [ ] The registry is closed: an unknown capability fails; additions are
      governed changes, not runtime improvisation.
- [ ] Instructions are server-side versioned artifacts; no untrusted party
      can supply or override them; the serving version is recorded per call.
- [ ] The audit write is fail-closed: an action that cannot be recorded does
      not execute.
- [ ] Every deny path has a designed proof it can fire — no rung, registry
      check, or audit gate is trusted untested.
- [ ] The design grants the agent NO new authority and creates no
      self-authorization or auto-execution path for privileged actions.
- [ ] The yields are stated: attack review → the named security skills;
      composed seams cited, not restated.

## Gotchas

- Prompt text is not a control: "you may not call this tool" in the system
  prompt constrains nothing — only the environment check does. The harness
  exists precisely because obedience is not an enforcement mechanism.
- A ladder evaluated after the model responds is a post-mortem, not a gate:
  the tokens are spent and the exposure has happened. Pre-flight means
  before the model runs, every rung.
- A registry that "falls back" to wrapping an unknown tool at runtime is an
  open registry with extra steps — the failure mode it exists to prevent.
- A fail-open budget rung is a denial-of-wallet vector: the cost check
  erroring into "allow" converts an outage into unbounded spend.
- Audit-after-execute loses the record exactly when it matters: a crash
  between action and write yields an unrecorded action. Record-or-refuse.
- "The model already knows who the user is" is how payload-supplied identity
  sneaks in — the model knowing it is exactly why it cannot be trusted; the
  mediation point re-establishes identity from credentials every time.
- Building the harness and reviewing it for attacks in the same pass reviews
  your own homework — yield the attack review to the security cluster.
- A deny path that has never fired in a test may be wired to nothing —
  theater with an exit code. Prove each rung can reject before trusting it.

## Stop Conditions

- The standing authority policy does not exist or is ambiguous → obtain it
  (from `agent-authorization-matrix` or a human) before designing the
  authorize rung; a harness enforcing an undefined policy is false assurance.
- The requested design would BYPASS the human-authority matrix or
  auto-execute privileged actions without human approval — self-authorized
  escalation, agent-armed merges/deploys, unattended spend or destructive
  operations → refuse and stop. This skill designs constraint; it does not
  grant the agent new authority, and a harness is not a device for laundering
  autonomy past its policy.
- Wiring the designed harness into a live system (live credentials, provider
  config, datastore permissions, deployment) → that is an implementation
  step under the repo's approval path (`human-approval-boundary`); this
  skill designs, it does not deploy.
- The request is actually an attack audit of an existing harness → hand to
  `prompt-injection-defender` / `agent-tool-safety-guard` /
  `agent-containment-reviewer` and stop.

## Supporting Files

- `evals/evals.json` — behavior cases: the ungoverned-call-sites design, the
  prompt-text-permissions conversion, the unknown-capability edge, the
  self-authorization refusal, and the attack-audit should-not-trigger.
- `evals/trigger-evals.json` — discrimination against
  `command-gateway-architect` (general write path vs AI harness),
  `ai-router-architect` (routing internals), `agent-authorization-matrix`
  (policy vs environment), `agentic-loop-designer` (in-batch: loop semantics
  vs call gating), `model-context-designer` (in-batch: context content vs
  call gating), and the design-vs-review seam against
  `agent-tool-safety-guard` / `prompt-injection-defender` /
  `agent-containment-reviewer`.
- No `references/` — the harness contract above is the complete procedure;
  detail lives in the produced design artifact.
