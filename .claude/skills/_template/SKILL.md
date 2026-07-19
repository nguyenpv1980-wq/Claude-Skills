---
name: _template
description: 'TEMPLATE ONLY — not a real skill and never invoked. Copy this directory to .claude/skills/<your-skill-name>/, rename it, set `name` to match the new directory, and rewrite every section against docs/skill-generation-standard.md. Write the real description to the Portability contract: front-load what the skill DOES in the first ~90 characters, keep it ONE strict-YAML-valid line (single-quote it like this one and double internal apostrophes, ''like this''), parsed value under 1024 characters.'
# disable-model-invocation: true   # uncomment if the real skill has side effects — the
#   description must then START with the exact 32-char sentinel (trailing space included):
#   MANUAL-ONLY; never auto-invoke.
#   (validator-enforced; see the Portability contract in the standard)
#   ONE narrow exception (standard §5): an auto-invocable skill MAY create or append
#   to a non-executable documentation or project-state file in the working tree, but
#   only as a second-phase action — show the exact target path and exact content or
#   diff, receive explicit, content-specific, single-use approval in the current
#   session, and write exactly what was approved. Overwrite/delete/rename, source
#   code, executable/config files, agent-instruction files, security/identity/
#   policy/CI files, secrets, network calls, external mutation, spending, and
#   deployment are NOT covered — those stay manual-only.
# allowed-tools: Read, Grep, Glob  # optional & narrow only; omit to inherit defaults
---

# _template (reference skill)

> **This is a template, not a shipped skill.** It lives at `.claude/skills/_template/`
> and is deliberately ignored by `scripts/validate-skills.py`. Do not invoke it.
> To create a skill: copy this directory, rename it, and fill in every section below.
> Full rules: [docs/skill-generation-standard.md](../../../docs/skill-generation-standard.md).

## Purpose

State, in one paragraph, what the real skill produces and the value it delivers.
Example: "Produces a normalized spreadsheet and summary tab from a messy export."

## Use When

- Use when: the user's request matches the concrete trigger the skill is built for.
- Use when: an adjacent-but-in-scope variation of that request appears.
- Do NOT use when: the request looks similar but belongs to another skill or a
  plain response — name that case explicitly so the model doesn't over-trigger.

## Inputs to Inspect

- The repo files, docs, code, tests, and prior artifacts the real skill must read
  before acting. List them concretely so context precedes action.

## Workflow

1. Gather and validate the inputs the skill needs (see **Inputs to Inspect**).
2. Perform the core transformation, reading `references/` detail files on demand.
3. Produce the deliverable exactly as specified in **Output Format**.
4. Run the **Validation Checklist** before declaring done.

## Output Format

Describe the exact deliverable: file path(s) and naming, report structure, or data
schema. Be specific enough that two runs produce consistent shapes.

## Validation Checklist

- [ ] Output matches the shape declared above.
- [ ] No **Stop Conditions** were silently bypassed.
- [ ] Any side-effecting step was gated behind explicit human confirmation. The
      only write an auto-invocable skill may make (standard §5): create/append a
      non-executable documentation or project-state file, AFTER showing the exact
      path + content and receiving explicit, content-specific, single-use
      approval — path and content unchanged between approval and write.

## Gotchas

- Keep `SKILL.md` under 500 lines; push detail into `references/`.
- Keep the frontmatter `description` trigger-oriented and under 1024 chars.
- Directory name and frontmatter `name` must stay identical.

## Stop Conditions

- Stop and ask if required input is missing or the request is ambiguous.
- Stop and confirm before any irreversible or destructive action (delete, deploy,
  overwrite, spend).
- Before a documentation/project-state append under the standard-§5 approved-write
  exception: show the exact target path and exact content, wait for the explicit
  content-specific yes, and write only what was approved. A declined, ambiguous,
  or changed approval means NO write. Every other side effect stays manual-only
  (`disable-model-invocation: true`).

## Supporting Files

- `evals/evals.json` — required for every real skill; the copy in this template
  directory ([evals/evals.json](evals/evals.json)) is the canonical starting point.
- `evals/trigger-evals.json` — add when the skill's trigger overlaps another skill.
- `references/`, `assets/`, `scripts/` — add only when they reduce errors (progressive
  disclosure). Use "None" here if the skill is self-contained.
