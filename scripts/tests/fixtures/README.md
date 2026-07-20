# Validator test fixtures

Everything under this directory is **synthetic input for
`scripts/tests/test_validator.py`** (decision D55). None of it is a shipped
skill, agent, workflow, or doc:

- it lives outside `.claude/skills/`, `.claude/agents/`, `.github/workflows/`
  and `docs/paths/`, so `scripts/validate-skills.py` never discovers it during
  a normal run;
- every fixture is reached only by an explicit path argument from the test
  suite.

Fixtures come in good/bad pairs. The bad ones exist to prove a check can
actually fail — a check that has never been seen to fail is an assertion, not a
gate.

| Path | Exercises |
|------|-----------|
| `skills/good-skill/` | the whole per-skill path, expected 0 errors |
| `skills/missing-section/` | required-section presence |
| `skills/out-of-order-sections/` | section ORDER, end to end through `validate_skill` |
| `skills/long-description/` | parsed-description length ceiling |
| `agents/*/` | `.claude/agents/` schema (one directory per failure mode) |
| `workflows/*/` | action SHA-pinning |
| `readme/` | the D43 SKILL-COUNT / family-roster reconciliation |
| `paths-tree/` | guided-path + README link resolution, in a miniature repo layout |
