# Skill Generation Standard

This is the authoritative standard for authoring Claude Code **skills** in this
repository. Every skill under `.claude/skills/` MUST conform. `scripts/validate-skills.py`
enforces the machine-checkable subset of these rules; the rest are review conventions.

The `.claude/skills/_template/` directory is the reference implementation of this
standard and is exempt from validation (it is a template, not a shipped skill).

---

## 1. Directory layout

```
.claude/skills/
  <skill-name>/
    SKILL.md            # required — entry point, loaded on invocation
    evals/
      evals.json        # required — representative cases (structural validation)
      trigger-evals.json # required only when the trigger overlaps another skill
    references/         # optional — progressive-disclosure detail files
    scripts/            # optional — helper scripts the skill may call
    assets/             # optional — templates, fixtures, static files
```

- One skill per directory. The directory name is the skill's canonical name.
- Everything the skill needs lives inside its own directory. No cross-skill imports.

---

## 2. Frontmatter rules

`SKILL.md` MUST begin with a YAML frontmatter block delimited by `---`.

| Field | Required | Rule |
| --- | --- | --- |
| `name` | yes | Must exactly equal the containing directory name. This is the repo convention that keeps invocation, filesystem, and catalog in sync. Lowercase kebab-case. |
| `description` | yes | Specific and **trigger-oriented** — say *when* to use the skill and *what it does*, in terms a model can match against a user request. Under **1024 characters**, measured on the parsed value (see the Portability contract below). Avoid vague verbs ("helps with", "handles"). |
| `disable-model-invocation` | conditional | Set to `true` for any skill that performs **side effects** (writes files outside scratch, calls networks, mutates external state, spends money, deploys). Such skills must be invoked explicitly by a human, never auto-triggered by the model — and their description must lead with the exact `MANUAL-ONLY; never auto-invoke. ` sentinel (see the Portability contract below). **Narrow approved-write exception (mirrors §5):** an auto-invocable skill may create or append to a non-executable documentation or project-state file in the current working tree, only as a second-phase action after showing the exact target path and exact content or diff and receiving explicit, content-specific, single-use approval in the current session; the approved path and content must not change before the write. The exception does NOT cover overwrite, delete, or rename; source code; executable or configuration files; agent-instruction or behavior-steering files; security, identity, authorization, policy, or CI/workflow files; secrets; network calls; external or live-state mutation; spending; deployment; or other irreversible action — those remain manual-only and require `disable-model-invocation: true`. |
| `allowed-tools` | optional | If present, must be a **narrow** list. Broad grants (`*`, `all`, `Bash` alone with no scoping) are forbidden — they defeat least-privilege. Omit the field to inherit the session default rather than widening it. |

### Description guidance

- **Good:** `"Convert a messy .xlsx export into a normalized sheet with typed columns and a summary tab. Use when the user hands you a spreadsheet to clean, reformat, or chart."`
- **Bad:** `"Helps with spreadsheets."` (not trigger-oriented, not specific)

### Portability contract

Aegis skills are consumed by more tools than Claude Code — the open Agent Skills
format is read by Codex CLI, Cursor, Gemini CLI and others, and those consumers
parse frontmatter with SPEC-STRICT YAML parsers and select skills from the
description alone (decisions D49/D50). Claude Code being lenient is not license
to author leniently: a skill only Claude Code can parse is not portable, and
before D50 exactly that shipped 67 times. The contract:

- **Strict-YAML-valid, always.** If the description contains `: ` (colon-space)
  or anything else a plain YAML scalar cannot carry, single-quote the whole
  scalar and double internal apostrophes (`'it''s'` parses to `it's`). Strict
  consumers silently DROP a skill whose frontmatter fails to parse — the skill
  simply does not exist there.
- **One physical line.** No block scalars (`>`, `|`) — consumers differ on
  folding behavior.
- **Parsed value under 1024 characters.** The validator measures the PARSED
  value: quoting characters and doubled apostrophes are serialization, not
  content, and do not count toward the limit.
- **Front-load the capability.** Some consumers' native selection sees only
  roughly the first ~90 characters of the description (D49 measurement: Codex
  ≈92). The first clause must say what the skill DOES; qualifiers and "Do NOT
  use" boundaries come later. *(Authoring guidance — judged in review, not
  mechanically checked.)*
- **Manual-only skills lead with the sentinel.** Every skill with
  `disable-model-invocation: true` carries the exact 32-character sentinel
  `MANUAL-ONLY; never auto-invoke. ` (trailing space included) as the FIRST 32
  characters of the parsed description. Consumers that ignore the field still
  surface the description front, so that position is the only
  guaranteed-visible safety signal.

The checks in `scripts/validate-skills.py` (strict-parse, parsed-value length,
sentinel position — each proven able to fail before shipping) are the
enforcement; this section is the why.

---

## 3. Progressive disclosure

`SKILL.md` is the **only** file guaranteed to load when the skill triggers. Keep it
lean and push detail outward:

- Keep `SKILL.md` **under 500 lines** (hard limit; validator enforces).
- Put long procedures, lookup tables, and edge-case catalogs in `references/*.md`
  and link to them by relative path. The model reads them **on demand**.
- Put runnable logic in `scripts/` and call it, rather than inlining large code blocks.
- The top of `SKILL.md` should let a reader decide *in seconds* whether this skill
  applies. Detail comes later or in references.

---

## 4. Required sections

Every `SKILL.md` body MUST contain these `##` sections, in this order (this is the v4
standard — the validator enforces all nine):

1. **Purpose** — one paragraph: what this skill produces and the value it delivers.
2. **Use When** — concrete trigger conditions. Mirror the frontmatter `description`
   but with more nuance and counter-examples ("Do NOT use when…").
3. **Inputs to Inspect** — the repo files, docs, code, tests, and prior artifacts the
   skill must read before acting (context before action).
4. **Workflow** — the ordered steps the model follows. This is the operational core.
5. **Output Format** — the exact shape of the deliverable (file, report, structure).
6. **Validation Checklist** — a checklist the model runs before declaring done.
7. **Gotchas** — known failure modes, sharp edges, platform quirks.
8. **Stop Conditions** — when to halt and ask the human instead of proceeding
   (ambiguity, missing input, destructive or irreversible actions).
9. **Supporting Files** — the `references/`, `assets/`, `scripts/`, and `evals/` files the
   skill relies on (progressive disclosure), or "None" if the skill is self-contained.

Security, SaaS, AI-security, and tool-use skills may add optional sections such as
**Safety Rules**, **Security Rules**, **Tenant Isolation Rules**, **AI Security Rules**,
or **Tool Permission Rules**. Sections may contain subsections; the nine top-level
headers must all be present.

---

## 5. Least privilege & side effects

- Default to **read-only**. A skill that only reads and reports needs no `allowed-tools`
  widening at all.
- Any write/network/deploy/spend behavior requires `disable-model-invocation: true`
  AND an explicit **Stop Conditions** entry describing the irreversible step — with
  ONE narrow exception, next.
- **Approved-write exception (the only one; mirrors the frontmatter table).** An
  auto-invocable skill may create or append to a **non-executable documentation
  or project-state file in the current working tree** only as a second-phase
  action: it first shows the exact target path and the exact content or diff,
  and receives **explicit, content-specific, single-use approval in the current
  session**. The approved path and content must not change before the write.
- The exception does **NOT** cover: overwrite, delete, or rename; source code;
  executable or configuration files; agent-instruction or behavior-steering
  files; security, identity, authorization, policy, or CI/workflow files;
  secrets; network calls; external or live-state mutation; spending; deployment;
  or other irreversible action. Those remain manual-only and require
  `disable-model-invocation: true`.
- Never embed secrets, tokens, or absolute machine-specific paths in a skill.

---

## 6. Evaluations

Every shipped skill MUST ship `evals/evals.json` (see the canonical template's
[`.claude/skills/_template/evals/evals.json`](../.claude/skills/_template/evals/evals.json)) describing
representative trigger prompts and expected behaviors, with at least a happy path, an
edge case, a should-not-do case, and objective assertions. Skills whose trigger
description overlaps another skill MUST also ship `evals/trigger-evals.json`.

**Evals are a repo convention, validated structurally only (decision D3):** the validator
checks that `evals/evals.json` exists and parses as JSON (and that `trigger-evals.json`
parses when present). **There is no eval runner yet** — do not claim evals "pass," only
that they are present and well-formed.

---

## 7. Skills vs. agents (pointer)

Skills are reusable procedures. Subagents (`.claude/agents/`) are read-only reviewer
personas. See [`docs/skills-catalog.md`](skills-catalog.md) §"Skills vs. Agents" for
when to build which.

---

## 8. Checklist for a new skill

- [ ] Directory name == frontmatter `name`, lowercase kebab-case.
- [ ] `description` is specific, trigger-oriented, < 1024 chars.
- [ ] `SKILL.md` < 500 lines; detail pushed to `references/`.
- [ ] All nine required sections present and in order.
- [ ] `evals/evals.json` present and well-formed; `trigger-evals.json` if trigger overlaps.
- [ ] No broad `allowed-tools`; `disable-model-invocation: true` if it has side effects.
- [ ] Listed in [`docs/skills-catalog.md`](skills-catalog.md) and `README.md`.
- [ ] `scripts/validate-skills.py` passes.
