---
name: good-agent
description: SYNTHETIC TEST FIXTURE, not a shipped agent. The conforming shape — frontmatter strict-parses, name matches the filename stem, tools stay inside the read-only set, model is recognised.
tools: Read, Grep, Glob
model: opus
---

Fixture body for `scripts/tests/test_validator.py`. Never invoked as an agent;
it lives outside `.claude/agents/`, so the validator only sees it when the test
suite passes this directory explicitly.
