# Memory Governance — rule sets, entry format, live checks

## WRITE rules (what may enter memory)

1. Confirmed durable facts only. Test: "can a single routine command make this
   false tomorrow?" If yes (PR state, branch tips, CI status, who is on-call),
   it is a snapshot — record the decision/lesson instead, or nothing.
2. Provenance mandatory: when written, based on what evidence.
3. Absolute dates only. Convert "yesterday"/"last Tuesday" at write time.
4. One fact per entry; entries link related entries rather than bundling.
5. Never: secrets, credentials, tokens, connection strings, PII. No
   exceptions clause — "just the staging password" is still a credential in a
   plaintext file that outlives the session.
6. Not what the repo records: code structure, git history, merged content.
   Store the pointer (`see docs/reconciliation/step-0-...md §3`), not a copy
   that will drift.
7. Update only when a confirmed fact CHANGES. Corrections replace the stale
   text and note the change (`was X until 2026-07-06, now Y per <evidence>`);
   never append a contradiction beneath the old claim.

## TRUST rules (before acting on memory)

Memory is a lead, not truth. Before any action premised on remembered state:

| Remembered claim | Verify with |
|---|---|
| PR open / merged / identity ("#11 is the docs PR") | `gh pr view <n> --json state,title,mergedAt,headRefName` |
| Branch exists / current branch | `git branch -a`, `git branch --show-current` |
| What merged to main / repo baseline | `git log --oneline -20 origin/main`, validator output |
| File / flag / command still exists | direct check before recommending it |
| Auto-merge / protection posture | `gh pr view <n> --json autoMergeRequest`, repo settings |

On divergence: live state wins, act on it, queue the memory correction. If the
divergence changes what the CURRENT task should do, route that conflict to
`source-of-truth-reconciler` (memory sits at the bottom of its precedence
order); only the memory fix returns here.

## HYGIENE classifications and dispositions

| Classification | Meaning | Default disposition |
|---|---|---|
| verified-current | live check confirms it | keep |
| stale | true when written; reality moved | correct (replace, with change provenance) |
| wrong-when-written | never true | correct or delete, with reason |
| duplicate | same fact elsewhere | merge-into the canonical entry |
| forbidden-content | secret/credential/PII | delete + **URGENT rotation recommendation** |
| unverifiable | no provenance, no way to check | delete or mark suspect — never silently trust |

All dispositions are proposed, human-approved, then applied exactly; the index
is updated and re-verified against the files afterwards.

## Case study — the stale-memory incident

Two sessions ran in parallel against one repo. Session A read memory: "PR #10
is open and needs merging" — true when written, but a colleague had already
merged it; A attempted a re-merge. Session B read memory describing PR #11's
purpose — the numbering had shifted as PRs opened and closed, and B pushed
work against the wrong PR. Neither entry was a lie; both were snapshots of
in-flight state trusted after they expired.

The rules this incident wrote: in-flight state does not enter memory (WRITE 1);
remembered PR state is verified with `gh` before any action (TRUST); and
parallel sessions assume memory is stale between write and read — the cost of
one `gh pr view` is always smaller than the cost of acting on a dead snapshot.
