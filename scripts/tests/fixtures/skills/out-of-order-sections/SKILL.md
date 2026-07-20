---
name: out-of-order-sections
description: 'SYNTHETIC TEST FIXTURE, not a shipped skill: all nine required sections are PRESENT but Gotchas is written before Workflow, so only the section-ORDER check may fire against it.'
---

# Out of order sections (test fixture)

Every required section is present, so the presence check passes. Their relative
order is wrong, so the order check must fail. That isolation is the point: an
error here can only mean the order check fired.

## Purpose

Prove the section-order check can fail end to end, through `validate_skill`.

## Use When

The self-test suite asserts that a scrambled skill is rejected.

## Inputs to Inspect

- This file.

## Gotchas

This section is deliberately placed before Workflow. Moving it back into
canonical position would disarm the fixture.

## Workflow

1. `validate_skill()` is called on this directory.
2. The report must name the out-of-order sections.

## Output Format

One error showing the found order against the canonical order.

## Validation Checklist

- [ ] The error mentions the sections being out of order.
- [ ] No missing-section error accompanies it.

## Stop Conditions

Stop if the canonical order in the standard changes — the fixture encodes it.

## Supporting Files

- `evals/evals.json` — structural placeholder.
