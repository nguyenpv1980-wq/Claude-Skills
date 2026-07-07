---
name: agent-memory-governance
description: Govern persistent agent memory as a curated, verified artifact — write rules (only confirmed durable facts with provenance and absolute dates; never secrets, credentials, tokens, or PII; never facts the repo itself records), trust rules (memory is a lead, not truth — reconcile remembered repo/PR/branch state against live git and gh output before acting on it), and hygiene (dedupe, correct stale entries, delete wrong ones, index consistency). Invoke explicitly to establish memory rules, audit or clean a memory store, decide whether a fact belongs in memory, or after a stale-memory incident — e.g. parallel sessions acting on remembered PR state that no longer matched the live repo. Produces rules plus per-entry audit dispositions; memory files edited only after approval — manual-only because memory steers future sessions. Do NOT use to resolve a live conflict between docs, code, or instructions (source-of-truth-reconciler) or to load context at task start (agent-startup-context-gate).
disable-model-invocation: true
---

# Agent Memory Governance

## Purpose

Keep persistent agent memory trustworthy enough to be useful and humble enough
to be safe. This skill sets the three rule sets memory lives by — WRITE (what
may enter), TRUST (how remembered state is verified before it drives action),
and HYGIENE (how entries are corrected, merged, and retired) — and executes
disposition-approved cleanups of an existing store. It exists because memory
that was true at write time silently rots: the motivating incident had two
parallel sessions act on remembered PR state, one attempting to re-merge an
already-merged PR, the other pushing work against the wrong PR entirely.

## Use When

- Use when (explicitly invoked by a human): establishing or revising the
  memory rules for a repo, project, or agent fleet.
- Use when: auditing or cleaning an existing memory store — stale entries,
  duplicates, contradictions, or suspected secrets in memory.
- Use when: deciding whether a specific fact belongs in memory at all, or how
  to record it (provenance, absolute dates, one fact per entry).
- Use when: after a stale-memory incident — a session acted on remembered
  repo/PR/branch/merge state that no longer matched reality — to codify the
  verify-before-act protocol.
- Do NOT use when: two sources conflict RIGHT NOW and the current task needs a
  verdict — that is `source-of-truth-reconciler` (memory is one source in that
  contest, and always loses to live repo state; this skill then fixes the
  losing memory entry as follow-up).
- Do NOT use when: starting a task and loading context — that is
  `agent-startup-context-gate` (whose verification habit this skill's TRUST
  rules feed).
- Do NOT use when: aligning agent instruction FILES (CLAUDE.md, AGENTS.md) —
  that is `agent-instruction-consolidator`; memory and instructions are
  different steering surfaces.
- Never auto-invoked: memory edits steer every future session —
  human-initiated only (`disable-model-invocation: true`).

## Inputs to Inspect

1. The memory store itself — every entry file plus the index; note the store's
   own format conventions (frontmatter, naming, index style) and follow them.
2. Live repo state for every repo-state claim memory makes: `git log`,
   `git branch -a`, `gh pr list --state all`, `gh pr view <n>` — the current
   truth each remembered claim is checked against.
3. Entry provenance: when each entry was written and on what evidence — an
   entry with no date or source cannot be aged or verified.
4. Incident history: which past sessions were misled by memory, and by which
   entries.
5. Any existing memory-policy rules — this run revises them, never forks a
   second policy.

## Workflow

1. **Establish or confirm the WRITE rules:**
   - Only confirmed durable facts — never in-flight state ("PR #10 is open"
     is a snapshot, not a fact; it expires the moment someone merges).
   - Provenance per entry: written-when, based-on-what evidence.
   - Absolute dates only — "last Tuesday" rots; "2026-07-06" does not.
   - One fact per entry; corrections REPLACE the stale text (with provenance
     of the change), never append a contradiction below it.
   - NEVER secrets, credentials, tokens, connection strings, or PII.
   - Not what the repo already records (code structure, git history, merged
     PRs' content) — store the pointer, not a drifting copy.
2. **Establish or confirm the TRUST rules:**
   - Memory is a lead, not truth. Before acting on any remembered repo, PR,
     branch, merge, or deploy state: verify against live `git`/`gh` output.
   - An entry naming a file, flag, or command → confirm it still exists
     before recommending or running it.
   - On divergence: live state wins, act on it, and queue the memory
     correction — never "fix" reality to match memory.
3. **Audit the store (when cleaning):** classify every entry —
   verified-current | stale (reality moved on) | wrong-when-written |
   duplicate | forbidden-content (secret/PII) | unverifiable — each with the
   live-check evidence that justified the classification.
4. **Propose per-entry dispositions:** keep | correct (with new text) |
   merge-into | delete (with reason). Forbidden-content entries are flagged
   URGENT with a rotation recommendation (a secret written to memory is a
   leaked secret — deleting the entry does not un-leak it).
5. **STOP for approval.** Present rules + disposition table. No memory file
   edits before explicit approval.
6. **Apply after approval** — exactly the approved dispositions; update the
   index to match; re-verify index ↔ files consistency.

## Output Format

```
MEMORY GOVERNANCE REPORT
Rules:        WRITE / TRUST / HYGIENE — established | confirmed | revised
Store audit:  <entry → classification → evidence (live git/gh check) → disposition>
Urgent:       <forbidden-content findings + rotation recommendation>
Corrections:  <stale entry → replacement text, with provenance>
Status:       AWAITING APPROVAL | APPLIED (index re-verified)
```

## Validation Checklist

- [ ] Every repo-state claim in memory was checked against live `git`/`gh`
      output — classifications cite the check, not recollection.
- [ ] No secret, credential, or PII retained anywhere in the store; URGENT
      findings carry a rotation recommendation, not just deletion.
- [ ] Corrections replace stale text (with change provenance); no entry ends
      up asserting two contradictory things.
- [ ] Every entry left in the store has provenance and absolute dates.
- [ ] Index matches the files after apply.
- [ ] No memory file was edited before explicit approval.

## Gotchas

- The incident class this skill exists for: memory said "PR #10 open, needs
  merge" and "PR #11 is the docs PR" — both true at write time, both wrong by
  read time. One session tried to re-merge a merged PR; another pushed to the
  wrong PR. Parallel sessions make memory stale between write and read;
  verify-before-act is the only posture that survives that.
- In-flight state masquerades as fact. Anything a single `gh` command can
  change (PR state, branch tips, CI status) is a snapshot — record the
  decision or lesson, not the moving state.
- A stale entry and a fresh one look identical without provenance dates —
  which is why undated entries are a hygiene finding by themselves.
- Deleting a wrong entry loses the trail; correcting without change
  provenance hides that reality moved. Correct-with-provenance beats both.
- Storing what the repo records invites drift: the copy in memory ages while
  the repo moves. Store pointers ("see docs/reconciliation/...") not copies.
- "It's just the staging password" is still a credential in a plaintext file
  that outlives the session. The rule has no exceptions clause.

## Stop Conditions

- Disposition table complete → full stop until explicit human approval;
  editing memory files before approval is this skill's defining failure.
- An entry contains a live credential → flag URGENT with rotation
  recommendation; never quote the value into reports or new entries.
- A memory-vs-reality divergence changes what the CURRENT task should do →
  that conflict routes to `source-of-truth-reconciler` now; only the memory
  correction returns here.
- Asked to store a secret or in-flight state "just this once" → refuse and
  cite the rule; offer the compliant alternative (pointer, or absolute-dated
  durable fact).

## Supporting Files

- [references/memory-rules.md](references/memory-rules.md) — the full WRITE /
  TRUST / HYGIENE rule sets, entry format with provenance, the live-check
  command set, and the stale-memory incident case study.
- `evals/evals.json` — behavior cases, including verify-then-act on remembered
  PR state (positive) and acting on stale memory unverified (should-not).
- `evals/trigger-evals.json` — discrimination against
  `source-of-truth-reconciler`, `agent-startup-context-gate`,
  `agent-instruction-consolidator`, and the Phase 1.5 siblings.
