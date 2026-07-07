---
name: agent-governance-audit
description: Audit whether an AI-assisted change actually followed governance discipline — classification and scope lock, human approval at each crossed boundary, merge/deploy authority (WHO merged, who armed auto-merge), real validation evidence, security review where the class required it, closeout completeness (incl. intentionally-not-done), and governed memory/doc updates. Per-control verdicts PASS/FAIL/UNVERIFIABLE cite primary evidence (PR timeline, commits, CI runs, approval records); closeout self-claims are cross-checked, never trusted; missing evidence is never a PASS. Use when asked whether a change or PR followed process, for post-incident review, to spot-check agent work before widening autonomy, or to verify a closeout's claims. Read-only, produces the governance report and changes nothing. Do NOT use to write the closeout for your own finished work (ai-closeout-reporter), audit whole-repo code health (full-codebase-auditor), or review diff correctness (code-reviewer / security-pr-reviewer).
---

# Agent Governance Audit

## Purpose

Answer, with evidence, whether one AI-assisted change followed the discipline
it was supposed to — not whether the code is good (that is review), and not
what the author says happened (that is the closeout), but what the primary
record proves happened. The report gives each governance control a PASS, FAIL,
or UNVERIFIABLE verdict with cited evidence, and an overall verdict a human can
act on: keep trusting the process, fix the process, or shrink the autonomy.
This is the feedback loop that makes the operating model and the authorization
matrix more than paperwork.

## Use When

- Use when: asked whether a specific change, PR, or phase of work followed the
  governance process — planning, approvals, validation, security, closeout.
- Use when: reviewing compliance after an incident — what discipline was
  bypassed, and whether the gap is policy or behavior.
- Use when: spot-checking agent-produced changes on a cadence, or before
  granting an agent wider authority in `agent-authorization-matrix`.
- Use when: verifying a closeout report's claims against the primary record.
- Do NOT use when: closing out your OWN just-finished work — that is
  `ai-closeout-reporter` (first-person disclosure; this skill is the
  third-party check of such reports).
- Do NOT use when: auditing whole-repo code health, dead code, or debt — that
  is `full-codebase-auditor`. This skill audits one change's PROCESS, not a
  codebase's state.
- Do NOT use when: judging a diff's correctness or security — that is
  `code-reviewer` / `security-pr-reviewer`; their EXISTENCE in the trail is
  what this skill checks.
- Do NOT use when: defining the process being audited against — that is
  `ai-sdlc-operating-model` (this skill consumes it and feeds revisions back).

## Inputs to Inspect

1. The governing policy in force WHEN the change happened: operating model,
   `agent-authorization-matrix`, change-class validation floors, repo standard.
   If none existed, the audit baseline is the repo's shipped discipline-skill
   contracts — and the report says so.
2. The PR's primary record: `gh pr view <n> --json author,reviews,mergedBy,
   autoMergeRequest,statusCheckRollup,timelineItems` — who opened, reviewed,
   approved, armed auto-merge, and merged, in what order.
3. Commit and branch history: scope drift, force-pushes, history rewrites,
   files touched vs the approved class.
4. CI runs and their actual outputs — not their summary badges.
5. The closeout report and any approval records in conversation or docs —
   claims to be cross-checked against 2–4, never accepted on their own.
6. Memory and doc updates made as part of the change, if governed.

## Workflow

1. **Fix the baseline.** Identify the policy set in force at the time of the
   change; audit against that — never against rules adopted afterwards.
2. **Assemble the evidence trail from primary sources** (PR JSON, git history,
   CI logs). The closeout is a claim sheet to verify, not an evidence source.
3. **Score each applicable control** (full catalog with per-control evidence
   sources and pass criteria:
   [references/audit-control-checklist.md](references/audit-control-checklist.md)):
   - Classification: change class declared; touched files stayed inside it.
   - Approval: every crossed boundary has a recorded human approval whose
     scope covers the action taken.
   - Merge/deploy authority: WHO merged; whether auto-merge was armed, by
     whom, and whether a recorded human decision covers it — an agent-armed
     auto-merge that fired is an authority FAIL even if a human appears as
     `mergedBy`.
   - Validation: the class's required checks actually ran with real outputs.
   - Security review: present where the class required it.
   - Closeout: all sections present, including intentionally-not-done;
     claims consistent with the primary record.
   - Memory/docs: updates follow `agent-memory-governance` write rules.
4. **Verdict per control:** PASS (evidence cited) | FAIL (violation cited) |
   UNVERIFIABLE (evidence missing or inaccessible — stated as such, never
   silently upgraded to PASS).
5. **Overall verdict:** PASS only when every applicable control passes; any
   FAIL → FAIL; otherwise CONDITIONAL with the unverifiable list.
6. **Findings → remediation:** for each FAIL, name whether it is a policy gap
   (no rule existed) or a discipline gap (rule existed, was bypassed), and the
   control or skill that closes it.
7. **Deliver the report**, including an honest not-inspected list.

## Output Format

```
GOVERNANCE AUDIT REPORT
Change:      <PR / commit range / task>     Baseline: <policy in force + date>
Controls:
  <control> — PASS | FAIL | UNVERIFIABLE — <primary evidence: PR event, commit, CI run>
Overall:     PASS | FAIL | CONDITIONAL (<unverifiable list>)
Findings:    <each FAIL → policy gap | discipline gap → closing control>
Not inspected: <what this audit did not look at, and why>
```

## Validation Checklist

- [ ] Every verdict cites primary evidence (PR event, commit SHA, CI run id) —
      no verdict rests on the closeout's own claims.
- [ ] UNVERIFIABLE used wherever evidence is missing; nothing missing was
      scored PASS.
- [ ] Merge authority verified from the PR timeline, including who ARMED
      auto-merge, not just who appears as the merger.
- [ ] Audited against the policy in force at the time, not hindsight rules.
- [ ] Every FAIL classified as policy gap vs discipline gap, with a closing
      control.
- [ ] Not-inspected list present and honest.

## Gotchas

- The closeout is the most convenient and least reliable source — auditing it
  instead of the primary record turns the audit into proofreading.
- Merge-authority blind spot: `mergedBy` can show a bot or even a human while
  the real authority act was ARMING auto-merge sessions earlier. The timeline
  event for enabling auto-merge is the evidence that matters.
- CI green is not "validation complete" — the change class defines the floor;
  green on the wrong checks still FAILs the validation control.
- An approval that exists but covers a different scope ("yes to staging") is
  a FAIL for the production action, not a PASS with a footnote.
- A review approval seconds after PR-open is evidence of rubber-stamping —
  report the timing honestly without over-claiming intent.
- Hindsight bias: auditing yesterday's change against today's rules produces
  unfair FAILs and teaches people to distrust audits.

## Stop Conditions

- Asked to soften, omit, or flip an evidence-backed FAIL (e.g. "it already
  merged, mark it pass") → refuse; the report states what the evidence states.
- Primary evidence is inaccessible (private CI, deleted branch) → mark those
  controls UNVERIFIABLE, state what access would resolve them, and continue;
  do not reconstruct evidence by inference.
- The audit surfaces an ACTIVE hazard — auto-merge armed on an open PR with no
  recorded decision, a live credential in the trail → surface it immediately;
  do not sit on it until the report is done.
- No governing policy existed and the requester wants a PASS/FAIL anyway →
  deliver the audit against the shipped discipline-skill contracts, labeled as
  such — or stop if they insist on an unlabeled verdict.

## Supporting Files

- [references/audit-control-checklist.md](references/audit-control-checklist.md) —
  the control catalog: per-control evidence sources, pass criteria, and the
  gh/git commands that retrieve the primary record.
- `evals/evals.json` — behavior cases, including missing-evidence →
  UNVERIFIABLE and refusing to soften a FAIL.
- `evals/trigger-evals.json` — discrimination against `ai-closeout-reporter`,
  `full-codebase-auditor`, `code-reviewer`, and the Phase 1.5 siblings.
