---
name: long-description
description: 'SYNTHETIC TEST FIXTURE, not a shipped skill: this description is deliberately padded past the 1024-character ceiling that validate-skills.py enforces on the strict-PARSED description value, so scripts/tests/test_validator.py can prove the parsed-length check still fires rather than merely asserting that it exists. The ceiling matters because external Agent-Skills consumers measure the parsed value and not the raw line: quoting characters and doubled apostrophes are serialization rather than content, so a description that looks short enough before parsing can still overflow a consumer budget after it. What follows is padding that says something true rather than lorem ipsum, because a fixture a reader skips is a fixture nobody notices has rotted: a check proven able to fail once is worth more than a check asserted to work forever, every gate in this repository earns its place by being seen to reject something, and the cheapest moment to learn that a check no longer fires is a test run rather than a merge that quietly ships a dropped skill to every downstream consumer.'
---

# Long description (test fixture)

The frontmatter description above exceeds the parsed-length ceiling on purpose.

## Purpose

Prove the parsed-description length check can fail.

## Use When

The self-test suite asserts on an over-length description error.

## Inputs to Inspect

- This file.

## Workflow

1. `validate_skill()` is called on this directory.
2. The report must state the parsed character count and the ceiling.

## Output Format

One error naming the measured length.

## Validation Checklist

- [ ] The error reports a parsed length of 1024 or more.

## Gotchas

Trimming this description to look tidier would disarm the fixture. It is long
by design.

## Stop Conditions

Stop if the ceiling itself changes — the fixture, not just the constant, needs
updating.

## Supporting Files

- `evals/evals.json` — structural placeholder.
