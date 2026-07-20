---
name: good-skill
description: 'SYNTHETIC TEST FIXTURE, not a shipped skill: the canonical-shape SKILL.md that validate-skills.py must accept with zero errors. Use when running scripts/tests/test_validator.py; any error reported against this file is a real validator regression.'
---

# Good skill (test fixture)

Structurally perfect on purpose. The description above is one single-quoted
line containing a `: ` — legal under a spec-strict YAML parser precisely
because it is quoted, which is the convention the Portability contract
mandates.

## Purpose

Be the known-good baseline for every per-skill check in the validator.

## Use When

The self-test suite needs a fixture that must produce zero errors.

## Inputs to Inspect

- This file.
- The sibling `evals/evals.json`.

## Workflow

1. `validate_skill()` is called on this directory.
2. The returned report is asserted to be empty.

## Output Format

An empty error list.

## Validation Checklist

- [ ] Frontmatter strict-parses.
- [ ] All nine required sections are present, in canonical order.

## Gotchas

Editing this fixture to be "more realistic" risks introducing a genuine
violation and turning a green baseline red for the wrong reason.

## Stop Conditions

Stop if this fixture ever needs a violation to pass — that means the validator
changed, and the change needs review, not a fixture edit.

## Supporting Files

- `evals/evals.json` — structural placeholder; the validator only checks it parses.
