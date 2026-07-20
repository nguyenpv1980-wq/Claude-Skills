# Add AI features safely

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** you want to add an AI feature — a chatbot, an assistant, an agent,
anything that calls a model — without opening a security hole. The threats here are
different from classic app security (a model can be talked into things a database cannot),
so the order matters: map the threats first, design the guardrails second, prove they hold
last.

**How to run it:** open your project in your agent tool (Claude Code, Codex CLI, or any Agent
Skills tool) and take the steps top to bottom. For most steps, plain words are enough — the
named skill selects itself. (Auto-selection quality varies by tool — see the README's [tools
section](../../README.md#using-aegis-with-codex-cli-and-other-agent-skills-tools).) Two steps are marked
**manual-only — name it explicitly**: you start them by typing the skill's name.

Steps marked *"if…"* are conditional — skip them honestly when they don't match your
feature's shape.

## The order

1. **Map the threats first —
   [`ai-threat-modeler`](../../.claude/skills/ai-threat-modeler/SKILL.md).**
   Yields the feature's threat map, with each mitigation naming the skill that owns it.
   Handoff: this map decides which of the steps below your feature actually needs — it is
   the reason this path starts here.

2. **Design the operating environment** — pick by your feature's shape:

   - **[`agent-harness-architect`](../../.claude/skills/agent-harness-architect/SKILL.md)** —
     yields the governed environment every model and tool call passes through, instead of
     model calls scattered wherever they were convenient.
   - **[`model-context-designer`](../../.claude/skills/model-context-designer/SKILL.md)** —
     yields the contract for what the model is allowed to see.
   - **[`agentic-loop-designer`](../../.claude/skills/agentic-loop-designer/SKILL.md)** —
     *only if the feature loops or acts on its own* — yields the loop's bounds and its
     honest ways to stop.

   Handoff: these designs are what the later steps defend and test.

3. **Contract the outputs and the spend:**

   - **[`structured-output-validator`](../../.claude/skills/structured-output-validator/SKILL.md)** —
     yields the validation contract for model output your code parses and acts on.
   - **[`llm-output-safety-reviewer`](../../.claude/skills/llm-output-safety-reviewer/SKILL.md)** —
     yields the handling rules for model output that gets rendered, executed, or passed
     downstream.
   - **[`ai-cost-guardrail-designer`](../../.claude/skills/ai-cost-guardrail-designer/SKILL.md)** —
     yields the token caps, budgets, and the fail-closed kill switch, so a runaway feature
     costs you a limit, not a bill.

4. **Defend the data going in:**

   - **[`sensitive-disclosure-guard`](../../.claude/skills/sensitive-disclosure-guard/SKILL.md)** —
     yields the controls on PII and secrets flowing toward the model.
   - *If the feature retrieves your documents or data to answer (RAG):*
     **[`rag-security-architect`](../../.claude/skills/rag-security-architect/SKILL.md)** —
     yields authorization enforced at retrieval time, so the model can only be shown what
     the asking user is allowed to see.

5. **Defend against injection —
   [`prompt-injection-defender`](../../.claude/skills/prompt-injection-defender/SKILL.md)**
   *(manual-only — name it explicitly; its own trigger says it runs after the threat model
   flags injection risk, which step 1 has now done).* Yields the layered defenses for the
   injection paths step 1 mapped. Handoff: its red-team cases feed step 6.

6. **Make it hold over time —
   [`ai-evaluation-harness`](../../.claude/skills/ai-evaluation-harness/SKILL.md)**
   *(manual-only — name it explicitly).* Yields the red-team cases from steps 1 and 5
   encoded as a standing regression net, so every future change re-proves the defenses
   instead of quietly eroding them.

7. ***Optional close* — [`ai-governance-risk-reviewer`](../../.claude/skills/ai-governance-risk-reviewer/SKILL.md).**
   Yields the feature's risk tier, its user-facing disclosure posture, and the human
   oversight it requires — worth running when the feature touches real users' decisions,
   money, or data.

## What this is — and isn't

This is a guided order, not a guarantee. Each skill's own output is the evidence — the
threat map, the contracts, the passing evaluation runs. An AI feature is safe on the day
the evidence says so, and stays safe only while step 6's net keeps catching what changes.
