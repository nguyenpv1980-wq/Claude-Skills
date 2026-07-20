# Something's broken — describe the symptom, not the cause

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** something in your app is wrong and you don't know why.

**How to run it:** in your agent tool (Claude Code, Codex CLI, or any Agent Skills tool),
describe the symptom in plain words — "users can see someone else's data", "tests fail only
in CI" — and the matching specialist selects itself. (Auto-selection quality varies by tool —
see the README's [tools section](../../README.md#using-aegis-with-codex-cli-and-other-agent-skills-tools).)
You never need to route anything yourself; the table below is the human-readable
map of who owns what, so you can see where your problem lands.

## The symptom map

| The symptom, in plain words | Who owns it |
|---|---|
| "Users can see data that isn't theirs." | [`tenant-isolation-reviewer`](../../.claude/skills/tenant-isolation-reviewer/SKILL.md) — finds every surface where one customer's data can reach another. |
| "I removed someone / revoked their access / they logged out — and the old access still works." Or: "they changed plans and still see the old tier." | [`authority-invalidation-architect`](../../.claude/skills/authority-invalidation-architect/SKILL.md) — finds every place the old access survives and proves the change actually took effect. |
| "One query or page is slow." / "It gets slower as data grows." / "I don't know where the time goes." | [`query-plan-reader`](../../.claude/skills/query-plan-reader/SKILL.md) for the slow query · [`n-plus-one-detector`](../../.claude/skills/n-plus-one-detector/SKILL.md) for slows-with-more-data · [`frontend-perf-engineer`](../../.claude/skills/frontend-perf-engineer/SKILL.md) for a slow page · [`profiling-methodology-designer`](../../.claude/skills/profiling-methodology-designer/SKILL.md) when nobody knows where the time goes. |
| "Tests fail randomly / only in CI." | [`flaky-test-detective`](../../.claude/skills/flaky-test-detective/SKILL.md) — separates flaky from genuinely broken, with the evidence. |
| "Production is down right now." | [`incident-response-runbook`](../../.claude/skills/incident-response-runbook/SKILL.md) — drives the live incident. Then [`rollback-runbook-author`](../../.claude/skills/rollback-runbook-author/SKILL.md) *before* the next release, so next time there's a tested way back. |
| "It fails and none of the above fits." | [`systematic-debugger`](../../.claude/skills/systematic-debugger/SKILL.md) — the general case: drives from symptom to root cause instead of guessing. |

## After the diagnosis

Whichever specialist takes it, the close is the same discipline: a root cause backed by
evidence, a fix you can review, and proof the fix actually took — not a "should be fine
now". If the diagnosis reveals the problem is bigger than a bug (a design gap, a security
hole), the specialist names the skill that owns that follow-up; let it hand off rather
than stretching the debugging session into a redesign.
