# Fixture link target

SYNTHETIC TEST FIXTURE for `scripts/tests/test_validator.py`, not a shipped
skill — note the deliberately nested location, which is never discovered by
`scripts/validate-skills.py` (that reads only the repo-root `.claude/skills/`).

This file has no frontmatter on purpose: the link-resolution check asserts only
that a linked target EXISTS on disk, so nothing here is ever parsed.
