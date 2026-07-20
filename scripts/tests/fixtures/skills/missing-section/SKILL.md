---
name: missing-section
description: 'SYNTHETIC TEST FIXTURE, not a shipped skill: identical to good-skill except that the Stop Conditions section is deliberately absent, proving the required-section presence check still fires.'
---

# Missing section (test fixture)

Deliberately omits `## Stop Conditions`.

## Purpose

Prove the required-section presence check can fail.

## Use When

The self-test suite asserts on a missing-section error.

## Inputs to Inspect

- This file.

## Workflow

1. `validate_skill()` is called on this directory.
2. The report must name `Stop Conditions` as missing.

## Output Format

One error naming the absent section.

## Validation Checklist

- [ ] The error names `Stop Conditions`.

## Gotchas

Adding the missing section back would silently disarm this fixture.

## Supporting Files

- `evals/evals.json` — structural placeholder.
