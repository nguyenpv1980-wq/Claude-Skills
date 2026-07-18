---
name: chat-backlog-reconciliation
description: 'On a cadence, extract decisions, bugs, and backlog items that exist only in ephemeral AI-chat history into dated repo docs, then AUDIT every item against PR/source evidence — classified completed / partial / active / not-active / unknown with citations; a chat "done" caps at unknown until repo evidence upgrades it. Enforces the standing rule: do not rely on stale chat history — tracked repo docs are the working record. Produces the dated extraction doc, the per-item audit table, and survivors routed to the real backlog/decision log. Use on a reconciliation cadence, when decisions live only in chats, when chat memory and repo state disagree about what was done, or before resuming work from old conversations. Do NOT use to govern a persistent agent-memory store (agent-memory-governance), resolve a live conflict between repo sources (source-of-truth-reconciler), close out one just-finished task (ai-closeout-reporter), or record a single fresh approval (scoped-approval-register).'
---

# Chat Backlog Reconciliation

## Purpose

Move truth out of chat and prove it against the repo. AI-assisted work
generates decisions, bug reports, and backlog items inside conversations that
expire — and future sessions then act on half-remembered versions of them.
This skill runs the two-step discipline observed in both source repos of the
extraction evidence: (1) EXTRACT chat-only items into a dated repo document,
(2) AUDIT each item against PR/commit/source evidence, classifying it
completed / partial / active / not-active / unknown — because a chat that
says "done" proves nothing. The deliverable enforces the standing rule: the
tracked repo doc, not chat history, is the working record from now on.

## Use When

- Use when: on a recurring reconciliation cadence (weekly/per-phase) over
  recent AI conversations.
- Use when: decisions or backlog items are known to exist only in chat —
  nothing in the repo records them.
- Use when: chat memory and repo state disagree about what was decided or
  done, or someone asks "did we ever actually fix/decide X?" about a
  chat-era commitment.
- Use when: resuming work from an old conversation whose claims have not
  been re-verified against the repo.
- Do NOT use when: governing a persistent agent MEMORY store (write/trust/
  hygiene rules for memory files) — that is `agent-memory-governance`; this
  skill's subject is conversation history, and its output is repo docs, not
  memory entries.
- Do NOT use when: two REPO sources (doc vs code vs test) conflict and
  precedence must be decided — that is `source-of-truth-reconciler`. Here
  chat is never a contender for truth; it is a lead list to verify.
- Do NOT use when: reporting one just-finished task — that is
  `ai-closeout-reporter` (terminal report for a single piece of work; this
  skill sweeps MANY conversations on a cadence).
- Do NOT use when: a single fresh approval needs recording — that is
  `scoped-approval-register` (though the sweep may FIND unrecorded grants
  and route them there).

## Inputs to Inspect

1. The chat sources in scope: exported conversations, session transcripts,
   chat-derived notes — with their dates. Undated chat claims are still
   extractable but say so.
2. Any existing extraction docs from prior sweeps (don't re-extract what a
   dated doc already holds; start from the last sweep's boundary).
3. The repo's real backlog and planning record — where surviving items must
   land (issue tracker, backlog doc, decision log).
4. Evidence surfaces for the audit: merged/closed PRs, commit history, the
   files a claim says were changed, test files, CI runs.
5. The repo's decision-record conventions (dated decision log, ADRs) so
   extracted DECISIONS are filed in the house format, not a new one.

## Workflow

1. **Bound the sweep.** Which conversations, what date range, since which
   prior sweep. State the boundary in the output doc — an unbounded sweep
   cannot claim completeness.
2. **Extract candidates.** From the chat sources, list every decision, bug,
   commitment, and backlog item that is not already in a tracked repo doc.
   Record each with: quoted/paraphrased content, source conversation + date,
   and what the chat CLAIMED about its status.
3. **Audit each item against evidence — never against chat.** For every
   item, look for PR/commit/file/test evidence and classify (definitions and
   evidence rules:
   [references/reconciliation-audit-format.md](references/reconciliation-audit-format.md)):
   - `completed` — evidence proves it fully done (cite PR/SHA/file:line);
   - `partial` — some evidence, gaps named;
   - `active` — work in progress (open PR/branch cited);
   - `not-active` — no evidence anyone started; still wanted or explicitly
     dropped (which one, say);
   - `unknown` — cannot determine from available evidence; what would
     resolve it.
   A chat message saying "done" is a claim, not evidence: without repo
   proof the ceiling is `unknown`.
4. **Write the dated reconciliation doc** (one per sweep, dated filename)
   with the extraction table + audit verdicts + citations.
5. **Route the survivors.** `not-active`-but-wanted and `partial` gaps go to
   the real backlog; unrecorded decisions go to the decision log/ADR flow;
   unrecorded approvals route to `scoped-approval-register`. Each routed
   item gets its destination noted in the doc.
6. **Enforce the standing rule.** The doc (and the repo's agent
   instructions, if they carry such rules) states: do not rely on stale chat
   history — use the tracked repo docs; future sessions cite the
   reconciliation doc, not the conversations it drained.
7. **Set the next sweep boundary** — a reconciliation without a cadence
   decays into a one-off.

## Output Format

```
CHAT BACKLOG RECONCILIATION — <YYYY-MM-DD>
Sweep boundary:  <conversations/date-range covered; prior sweep doc>
Items:
  | # | Item (quoted/paraphrased) | Chat source + date | Chat claimed | Audit verdict | Evidence | Routed to |
  |---|---|---|---|---|---|---|
  | 1 | <decision/bug/backlog item> | <conv, date> | "done" | completed \| partial \| active \| not-active \| unknown | <PR #/SHA/file:line or "none found"> | <backlog/decision-log/register/n-a> |
Unresolved (unknown) items: <what evidence would resolve each>
Standing rule: tracked repo docs are the working record; this doc supersedes
the chats it drained. Next sweep: <boundary/cadence>.
```

## Validation Checklist

- [ ] Sweep boundary stated; prior sweep referenced (no silent gaps or
      double-extraction).
- [ ] Every item carries a source conversation + date and a verdict from the
      five-class taxonomy.
- [ ] No item is classified `completed` on chat say-so — every `completed`
      cites PR/commit/file evidence.
- [ ] `unknown` used honestly where evidence is absent — not upgraded, not
      guessed.
- [ ] Survivors routed: backlog items to the real backlog, decisions to the
      decision log, approvals to the register — destinations named.
- [ ] The doc is dated and the standing rule + next sweep boundary are
      stated.
- [ ] No live identifiers or secrets copied out of chats into the doc —
      template as placeholders.

## Gotchas

- **Chat optimism:** conversations systematically over-claim completion
  ("fixed!" … then the fix was never pushed). That is WHY the audit step
  exists; extraction without audit just launders stale claims into a doc.
- **Duplicate extraction:** the same decision discussed in three chats
  becomes three "items". Deduplicate by content before auditing.
- **Verdict drift:** `not-active` hides two different truths — still-wanted
  vs deliberately dropped. Record which, or the item resurrects/dies
  wrongly.
- **The doc becomes the new stale chat** if never swept again: the standing
  rule holds only while the cadence does.
- **Secrets in chats:** conversations legitimately contain tokens and live
  identifiers that repo docs must not. Extraction is not copy-paste;
  template them out.
- **Chat-vs-repo conflicts discovered mid-sweep** (repo doc says X, chat
  decided Y later): that pair is two repo-relevant sources in conflict —
  hand THAT item to `source-of-truth-reconciler` rather than silently
  picking.

## Stop Conditions

- Asked to mark items `completed` from chat claims without evidence ("just
  trust the summary, we discussed it") → refuse; the audit against evidence
  is the skill. Offer `unknown` with what would resolve it.
- The chat sources are unavailable/unexportable → stop and say what is
  needed; do not reconstruct "what we probably decided" from memory.
- An extracted item contradicts a tracked repo decision → do not overwrite
  either; surface the conflict (route to `source-of-truth-reconciler`).
- The sweep uncovers a live hazard (leaked credential in chat, an
  unrecorded approval that authorized something already run in production)
  → surface it immediately; do not sit on it until the doc is done.

## Supporting Files

- [references/reconciliation-audit-format.md](references/reconciliation-audit-format.md)
  — verdict definitions with evidence rules, the extraction/audit table
  template, dedup guidance, and a worked example.
- `evals/evals.json` — behavior cases incl. refusing evidence-free
  `completed` verdicts.
- `evals/trigger-evals.json` — discrimination against
  `agent-memory-governance`, `source-of-truth-reconciler`,
  `ai-closeout-reporter`, and `scoped-approval-register`.
