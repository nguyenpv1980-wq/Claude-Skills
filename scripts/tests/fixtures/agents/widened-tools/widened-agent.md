---
name: widened-agent
description: SYNTHETIC TEST FIXTURE, not a shipped agent. Grants Write on top of Read — the privilege escalation the read-only reviewer contract exists to forbid.
tools: Read, Write
model: opus
---

Fixture body for `scripts/tests/test_validator.py`. The reviewer agents in
`.claude/agents/` are read-only by contract; a Write, Edit, Bash or `*` grant
turns a reviewer into an actor, which is exactly what this fixture proves the
validator will reject.
