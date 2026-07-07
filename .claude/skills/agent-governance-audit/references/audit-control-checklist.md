# Governance Audit — control catalog

Audit against the policy IN FORCE at the time of the change. Every verdict
cites primary evidence; the closeout is a claim sheet to cross-check, never an
evidence source. Missing evidence → UNVERIFIABLE, never PASS.

## Control catalog

| # | Control | Primary evidence source | PASS criteria |
|---|---|---|---|
| C1 | Classification & scope lock | declared class (conversation/PR body); `git diff --stat` of the change vs the class's file-set | class declared before implementation; touched files inside the approved class; mid-task growth reclassified, not absorbed |
| C2 | Boundary approvals | approval records (PR thread, conversation, approval log) matched to each boundary the change crossed (schema, RLS/security, secrets, deploy, prod data, history) | every crossed boundary has a recorded human approval whose scope wording covers the action actually taken |
| C3 | Merge/deploy authority | `gh pr view <n> --json author,reviews,mergedBy,mergedAt,autoMergeRequest,timelineItems` — including the auto-merge ENABLED event and its actor | merge decision traceable to a named human per the authorization matrix; no agent-armed auto-merge; deploys triggered per matrix |
| C4 | Validation floor | CI run logs, command outputs quoted in the record; the class's required checks list | the floor's checks actually ran with real outputs; green on the RIGHT checks, not just green |
| C5 | Security review | review records on the PR; security lens where class = RLS/security/schema/secrets | required security review present and by the required party |
| C6 | Closeout completeness | the closeout report vs `git`/PR reality | all sections present incl. intentionally-not-done; claims consistent with primary record (files, tests, skips) |
| C7 | Memory/doc governance | memory-store diff tied to the change | updates follow `agent-memory-governance` WRITE rules (durable facts, provenance, no secrets); stale entries corrected not contradicted |

## Retrieval commands

```bash
gh pr view <n> --json author,reviews,mergedBy,mergedAt,autoMergeRequest,statusCheckRollup
gh api repos/{owner}/{repo}/pulls/<n>/events        # timeline incl. auto_merge_enabled + actor
gh run list --branch <branch> ; gh run view <id> --log
git log --oneline --graph <base>..<head> ; git diff --stat <base>..<head>
```

## Verdict discipline

- **PASS** — criteria met, evidence cited (event id / SHA / run id).
- **FAIL** — violation, evidence cited; classify as **policy gap** (no rule
  existed — feed `ai-sdlc-operating-model` / `agent-authorization-matrix`) or
  **discipline gap** (rule existed, was bypassed — name the bypassed control).
- **UNVERIFIABLE** — evidence missing/inaccessible; state what access would
  resolve it. Any UNVERIFIABLE on an applicable control caps the overall
  verdict at CONDITIONAL.
- Overall: PASS only if all applicable controls PASS; any FAIL → FAIL.

## Known evidence traps

- `mergedBy` shows who (or what) executed the merge, not who DECIDED it — the
  auto-merge enabled event and its actor is the decision evidence (C3).
- Squash merges hide branch history; audit the pre-merge branch or PR commits.
- A review approval timestamp seconds after PR-open is reportable timing
  evidence; report the timing, not an inferred motive.
- CI badges summarize; only run logs prove which checks ran on which SHA.
