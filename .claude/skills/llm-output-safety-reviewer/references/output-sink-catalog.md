# LLM output sink catalog

Detail for `llm-output-safety-reviewer`. OWASP LLM05 (Improper Output
Handling), 2025. Model output is untrusted; each sink below re-asks "what if
this is adversarial?".

## Render sinks (→ XSS / markup injection)

- **HTML/JSX/templates:** must be context-correctly escaped. Auto-escaping on
  by default is good; `dangerouslySetInnerHTML`, `v-html`, `innerHTML`,
  `Element.insertAdjacentHTML`, template `| safe` filters bypass it — each is
  a finding when fed model output unless sanitized.
- **Markdown:** many renderers allow raw HTML by default. Disable raw HTML or
  run an allowlist sanitizer (DOMPurify-style) AFTER rendering. Watch
  `javascript:` / `data:` URLs in links and images, and `onerror`/`onload`
  attributes.
- **Attributes / URLs in markup:** escaping for element text ≠ safe in an
  attribute or `href`. Validate URL schemes (allow http/https/mailto).
- **Defense in depth:** Content-Security-Policy limits blast radius but is not
  a substitute for encoding.

## Execution sinks (→ injection / RCE)

- **SQL/NoSQL:** parameterize; never string-concatenate model output into a
  query. ORM raw-query escapes bypass this.
- **Shell / OS command:** avoid entirely; if unavoidable, use argument arrays
  (no shell), allowlist the command and args. Model output in a shell string
  is command injection.
- **eval / dynamic code:** model output into `eval`, `Function`, `exec`,
  template engines with code, or deserialization is RCE-class.
- **Generated-code execution (agent writes code that runs):** requires a real
  sandbox — isolated process/container/VM, no ambient credentials, network
  denied unless required and then allowlisted, CPU/memory/time limits, no
  access to the host filesystem beyond a scratch dir. "We instruct it to write
  safe code" is not a control. This is the ASI05 seam too (agentic).

## URL / path / request sinks

- **SSRF:** server-side fetch of a model-produced URL must use an allowlist and
  block private/link-local ranges and cloud metadata endpoints
  (169.254.169.254 and equivalents). "Follow the link the model found" is the
  classic hole.
- **Path traversal:** model-chosen filenames/paths resolved without
  canonicalization + base-dir check allow `../` escapes. Resolve and verify
  containment.
- **Request construction:** headers/bodies built from output can smuggle
  (CRLF, extra params).

## Tool-argument sinks

- Validate shape/type/values before the side effect (compose
  `structured-output-validator`); enforce the permission/identity boundary
  (compose `agent-tool-safety-guard`). Shape-valid output can still be a
  malicious value (another tenant's id).

## Store-and-reuse (second-order)

- Output persisted then later rendered/executed is untrusted again on READ.
  Encoding at write time helps only the writer's context; a different reader
  (admin console, export, another service) may render it raw.
- Classic path: model output stored as "internal data", later displayed in a
  trusted-internal UI that skips escaping.
- Rule: sanitize/encode at the sink that USES the data, in that sink's
  context — not (only) once at write time.

## Severity gating

Exploit-gated: a concrete flow from adversarial model output to XSS/RCE/SSRF/
injection/data-exposure is HIGH; a theoretical "could be unsafe" without a
reachable sink is lower. Name the flow in every finding.
