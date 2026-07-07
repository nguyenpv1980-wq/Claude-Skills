---
name: llm-output-safety-reviewer
description: Review how an application consumes LLM output for improper output handling (OWASP LLM05) — treat every model output as untrusted data and trace it to each sink: HTML/markdown rendering (XSS), SQL/NoSQL/shell/eval execution (injection, RCE), file paths and URLs (traversal, SSRF), tool/function arguments, and stored-then-re-consumed content (second-order). Verify context-correct encoding/escaping, sandboxing for any executed generated code, and that output is validated/typed before it drives an action. Use when model output is rendered, executed, stored, or used to build a command, query, path, or request. Do NOT use for schema-shape validation of structured output (structured-output-validator), the injection that produced the output (prompt-injection-defender), factual correctness (ai-misinformation-guard), or tool-permission scope (agent-tool-safety-guard).
---

# LLM Output Safety Reviewer

## Purpose

Review whether an application handles model output safely (LLM05): the model
output is untrusted data, and every place it flows — a rendered page, a
database query, a shell command, a file path, a URL, a tool argument, or a
store it will later be read from — is a potential injection or execution sink.
The review traces output to each sink and verifies context-correct
encoding/escaping, sandboxing for executed generated code, and
validate-before-act discipline, producing severity-ranked findings each with
the flow from model output to impact.

## Use When

- Use when: model output is rendered as HTML/markdown, executed as SQL/shell/
  code, written to files, used to build URLs or requests, passed as tool
  arguments, or stored and later re-consumed.
- Use when: reviewing an AI feature's output path for XSS, injection, RCE,
  SSRF, path traversal, or second-order (stored-output) issues.
- Use when: an agent generates code that the system then runs.
- Do NOT use when: the concern is the SHAPE/type of structured output —
  `structured-output-validator` (this skill is the injection/exec sink review;
  they compose).
- Do NOT use when: the concern is the injection that manipulated the model
  (`prompt-injection-defender`), factual accuracy
  (`ai-misinformation-guard`), or how broad the tools are
  (`agent-tool-safety-guard`).

## Inputs to Inspect

1. The output sinks: every place the model's output is used — templates/JSX,
   query builders, command execution, file I/O, HTTP clients, tool-call
   dispatch, storage writes.
2. The rendering path: is output treated as text or as markup; is auto-escaping
   on; is `dangerouslySetInnerHTML`/`v-html`/`innerHTML` or a markdown renderer
   with raw-HTML enabled in play.
3. Execution paths: any `eval`, dynamic SQL, shell-out, code interpreter, or
   generated-code runner; the sandbox (or absence) around it.
4. URL/path construction from output: SSRF (model-chosen URL fetched
   server-side), path traversal (model-chosen filename).
5. Storage-and-reuse: output persisted then later rendered/executed as if
   trusted (second-order injection).
6. Existing encoding/validation: escaping helpers, allowlists, content
   security policy, and where they are and aren't applied.

## Workflow

1. **Enumerate output sinks.** List every consumer of model output and
   classify each: render, execute, store, or drive-an-action. No output-
   handling code to inspect → Stop Conditions.
2. **Treat output as untrusted.** For each sink, ask the same question you'd
   ask of raw user input: what happens if the output is adversarial? Model
   output is attacker-influenced whenever untrusted content was in context.
3. **Review rendering sinks** using
   [references/output-sink-catalog.md](references/output-sink-catalog.md):
   HTML/markdown must be context-correctly encoded or sanitized; raw-HTML
   rendering of model output is a finding unless sanitized with an allowlist;
   check CSP as defense in depth.
4. **Review execution sinks.** Model output that becomes SQL, shell, eval, or
   generated code that runs: require parameterization/allowlisting, and for
   generated-code execution require a real sandbox (isolated, no secrets, no
   network unless required, resource-limited). Unsandboxed execution of
   generated code is RCE-class.
5. **Review URL/path/request sinks.** Server-side fetch of a model-chosen URL
   is SSRF — require an allowlist and block internal ranges/metadata
   endpoints. Model-chosen file paths need traversal-safe resolution.
6. **Review tool-argument sinks.** Output used as tool arguments must be
   validated before the side effect (compose `structured-output-validator`
   for shape, `agent-tool-safety-guard` for the permission boundary).
7. **Review store-and-reuse.** Output persisted and later rendered/executed is
   re-untrusted on read: encoding at write time is not enough if a different
   reader trusts it. Flag second-order paths.
8. **Rank findings by flow.** Each finding names the flow (model output →
   sink → impact) and severity gated on a concrete exploit; give the
   context-correct fix (escape here, parameterize there, sandbox, allowlist).

## Output Format

```
LLM OUTPUT-HANDLING REVIEW — <feature>
Output sinks: <render | execute | store | action — each location>
Findings (severity-ranked):
  [SEV] <sink type> at <file:line>
    Flow: <model output → sink → impact (XSS/RCE/SSRF/injection/2nd-order)>
    Fix: <context-correct encoding | parameterize | sandbox | allowlist>
Sandbox posture (if code exec): <isolation, secrets, network, limits>
Second-order paths: <stored output re-consumed as trusted>
Defense-in-depth: <CSP, output length caps, content types>
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] Every model-output sink enumerated and classified (render/execute/
      store/action).
- [ ] Rendering sinks use context-correct encoding; raw-HTML rendering is
      sanitized with an allowlist or flagged.
- [ ] Execution sinks are parameterized/allowlisted; generated-code execution
      runs in a real sandbox or is flagged as RCE-class.
- [ ] URL sinks checked for SSRF (allowlist, internal-range block); path sinks
      checked for traversal.
- [ ] Tool-argument sinks validate before the side effect (composed with
      structured-output-validator / agent-tool-safety-guard).
- [ ] Stored-then-reused output is treated as untrusted on read (second-order).
- [ ] Findings name the output→sink→impact flow; severity is exploit-gated.

## Security Rules

- Model output is untrusted data, handled with the same discipline as raw user
  input — no sink gets to assume it's clean.
- Encoding is context-specific: HTML-escaping does not make output safe for a
  SQL string, a shell command, a URL, or a filename. Match the sink.
- Generated code that executes requires a sandbox; "we prompt it to write safe
  code" is not a control.
- Escaping at write time does not sanitize a later trusting read — second-order
  sinks re-validate.

## Gotchas

- Markdown renderers often pass through raw HTML by default — a model emitting
  `<img onerror=…>` inside markdown becomes XSS unless raw HTML is disabled or
  sanitized.
- Streaming output tempts teams to render incrementally before any
  sanitization runs — the sanitize step must not be skipped for the stream.
- "It's just displayed, not executed" ignores that display IS execution for a
  browser — HTML/JS renders.
- SSRF via model output is easy to miss: the model helpfully returns a URL and
  the server fetches it to "follow the link" — straight into the metadata
  endpoint.
- The exploit often lands one hop away: output stored today, rendered in an
  admin console tomorrow by code that assumes internal data is safe.
- Don't conflate with shape validation: JSON that parses cleanly can still
  carry an XSS payload in a string field — shape-valid ≠ safe-to-render.

## Stop Conditions

- No output-handling code (templates, query builders, exec paths) is
  available — stop; this skill reviews concrete sinks, not a description.
- The review finds generated code executing unsandboxed with access to
  secrets or the network — flag as blocking and route remediation through
  `human-approval-boundary`.
- The real issue is the model being manipulated (injection), output shape, or
  factual correctness — hand to the owning skill.
- A live exploit is evident (active XSS/RCE via output) — route to
  `incident-response-runbook`.

## Supporting Files

- [references/output-sink-catalog.md](references/output-sink-catalog.md) —
  per-sink review checklist (render/execute/URL/path/tool-arg/store),
  context-correct encoding rules, the generated-code sandbox rubric, and
  second-order injection patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the output & agency
  cluster and against `security-pr-reviewer` and `structured-output-validator`.
