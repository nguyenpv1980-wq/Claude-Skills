---
name: static-analysis-reviewer
description: Triage SAST / CodeQL / SARIF / linter-security output on first-party code into what actually matters — sort each finding into true-positive, false-positive, duplicate, or accepted-risk, and rank the true positives by reachability, exploitability, asset sensitivity, tenant impact, and business impact. Confirms each true positive against the real code (a scanner hit is a lead, not a verdict), requires an exploit path for high-severity, and outputs a triaged, deduplicated, prioritized remediation list with a suppression policy (no finding suppressed without written rationale). Use when handed scanner/SAST/SARIF/CodeQL output to make sense of. Do NOT use for dependency/CI supply-chain risk (supply-chain-security-reviewer), reviewing a raw diff (security-pr-reviewer), or migration safety (secure-migration-reviewer).
---

# Static Analysis Reviewer

## Purpose

Turn a wall of scanner findings into a short, trustworthy, prioritized list.
Static analysis over-reports: it flags patterns, not proven vulnerabilities.
This skill confirms each finding against the actual code, sorts them into
true-positive / false-positive / duplicate / accepted-risk, and ranks the true
positives by reachability, exploitability, asset sensitivity, tenant impact,
and business impact — so effort goes to the findings that can actually hurt.
The deliverable is a triaged, deduplicated, ranked remediation list with an
explicit suppression policy: nothing is dismissed without a written reason a
reviewer can audit. A scanner hit is a lead, not a verdict.

## Use When

- Use when: handed SAST / CodeQL / Semgrep / SARIF / security-linter output on
  first-party code and asked to make sense of it, prioritize it, or reduce
  the noise.
- Use when: a security gate is failing on scanner findings and you need to
  separate real issues from noise (with rationale, not blanket suppression).
- Use when: converting scanner output into a prioritized remediation backlog.
- Do NOT use when: the findings are about dependencies, CVEs, or CI/build —
  that is `supply-chain-security-reviewer` (first-party-code-vs-supply-chain
  is the split).
- Do NOT use when: there is no scanner output and the ask is to review a diff
  by hand — `security-pr-reviewer`.
- Do NOT use when: the subject is a migration's safety —
  `secure-migration-reviewer`.
- Do NOT use when: the ask is design-time threat enumeration —
  `threat-modeler`.

## Inputs to Inspect

1. The scanner output: SARIF file, CodeQL/Semgrep results, or the tool's
   report — rule ids, locations, severities, and data-flow paths if present.
   No output to triage → Stop Conditions.
2. The actual source at each flagged location and along its data-flow path —
   the triage confirms or refutes the finding against real code, never on the
   rule name alone.
3. Reachability context: is the flagged code on a reachable path (an exposed
   endpoint, a called function) or dead/test/example code?
4. Sensitivity context: what asset the code touches (auth, tenant data, money,
   PII) and whether a SaaS tenant boundary is involved.
5. Prior triage decisions / existing suppressions (baseline) — so previously
   accepted risk isn't re-litigated blindly and stale suppressions get caught.

## Workflow

1. **Load and normalize** the findings (SARIF/report). Group by rule and by
   sink so duplicates and the same-root-cause clusters are visible. No output
   → stop.
2. **Deduplicate:** collapse findings that are the same issue reported via
   multiple paths or multiple rules into one, keeping the paths as evidence.
3. **Confirm each finding against the code.** For each (or each cluster):
   trace the flagged data flow in the real source. Decide:
   - **True positive** — the pattern is a real defect on inspection.
   - **False positive** — refuted by the code (input already sanitized,
     framework auto-escapes, path unreachable, rule misfired). Record WHY.
   - **Duplicate** — same root cause as another.
   - **Accepted risk** — real but consciously accepted (needs written
     rationale; see suppression policy).
4. **Rank the true positives** by the five axes in
   [references/triage-rubric.md](references/triage-rubric.md): reachability
   (can an attacker reach it), exploitability (how hard), asset sensitivity
   (what it protects), tenant impact (one tenant vs all — cross-tenant blast
   raises severity), business impact.
5. **Require an exploit path for high severity.** A true positive ranked
   HIGH/CRITICAL states who reaches it, how, and what they get. No path →
   cap at medium and note what would confirm it (a reachability question is
   not automatically high).
6. **Apply the suppression policy:** false positives and accepted risk are
   suppressed only WITH a written rationale (rule id, why refuted/accepted,
   who, date). Blanket "ignore all lows" is not a rationale.
7. **Produce the remediation list:** ranked true positives, each with the
   confirmed location, the exploit path (for highs), and a fix direction —
   handing fixes to `appsec-implementer` and any diff-level nuance to
   `security-pr-reviewer`.
8. **Report the triage math:** counts in vs out (TP/FP/dup/accepted), so the
   noise reduction is auditable and the scanner can be tuned.

## Output Format

```
STATIC ANALYSIS TRIAGE — <tool + scope>
Input: <N raw findings> → <M after dedup>
Disposition: true-positive <n> | false-positive <n> | duplicate <n> | accepted <n>
True positives (ranked):
  [CRITICAL|HIGH|MEDIUM|LOW] <rule id> @ <file:line>
    Confirmed: <what the code actually does on the flagged path>
    Exploit path (HIGH+): <who reaches it, how, what they get; tenant blast>
    Rank basis: reachability/exploitability/asset/tenant/business
    Fix: <direction>  → appsec-implementer
False positives: <rule id @ loc — why refuted (code fact)>
Accepted risk: <rule id @ loc — written rationale, owner, date>
Suppression policy applied: <yes — per-finding rationale recorded>
Not triaged: <findings/areas not reached + why>
```

## Validation Checklist

- [ ] Findings deduplicated and grouped by root cause before triage.
- [ ] Every finding confirmed against actual source, not judged by rule name.
- [ ] Each finding has a disposition (TP / FP / duplicate / accepted) with a
      code-grounded reason.
- [ ] True positives ranked on all five axes, with tenant blast radius
      considered for SaaS code.
- [ ] Every HIGH+ has an exploit path; reachability-only findings not
      auto-promoted to high.
- [ ] Every suppression (FP/accepted) has a written rationale; no blanket
      dismissals.
- [ ] Triage math (in→out counts) reported for auditability.
- [ ] Fixes handed off, not applied here.

## Security Rules

- Scanner output is input, not truth (master-prompt §6): every finding is
  confirmed or refuted against the real code before it gets a disposition.
- No finding is suppressed without a written, auditable rationale — "false
  positive" alone is not a rationale; the code fact that refutes it is.
- High severity requires an exploit path; a reachable pattern with no
  demonstrable exploit is ranked medium and marked needs-verification.
- Cross-tenant impact raises severity — a true positive that leaks across
  tenants outranks the same class scoped to a single tenant.
- Accepted risk requires the human's sign-off via `human-approval-boundary`;
  this skill records the acceptance, it does not grant it.

## Gotchas

- A HIGH rule severity is the RULE's default, not this finding's severity —
  re-rank by reachability and impact, don't inherit the tool's number.
- The same vulnerability surfaces as many findings (one per path/sink);
  triaging each independently inflates the backlog — dedup first.
- Framework context flips verdicts: an ORM auto-parameterizes, a template
  engine auto-escapes — a "SQL injection"/"XSS" flag can be a false positive,
  but only after you confirm the safe path is actually taken.
- Test files, fixtures, examples, and generated code produce findings that are
  usually not reachable in production — classify by reachability, but don't
  assume "it's a test" without checking it isn't shipped.
- Suppressing to make the gate green hides real issues and rots the baseline;
  a suppression without a code-grounded reason is a future incident.
- A finding the scanner MISSED is still possible — triaging scanner output is
  not a full security review; say so, and route deeper needs to
  `security-pr-reviewer` / `threat-modeler`.

## Stop Conditions

- No scanner/SARIF/report output is provided → stop; this skill triages
  existing output, it does not run scans or review code cold (route to
  `security-pr-reviewer`).
- A confirmed true positive is critical and exploitable in production → report
  it immediately with its path; containment is the human's call
  (`human-approval-boundary`) before finishing the full triage.
- Asked to suppress findings without rationale to pass a gate → refuse; record
  each disposition with a reason or escalate accepted risk for written
  sign-off.
- The findings are dependency/CVE/CI issues, not first-party code → hand to
  `supply-chain-security-reviewer`.

## Supporting Files

- [references/triage-rubric.md](references/triage-rubric.md) — the five-axis
  ranking rubric with scoring guidance, disposition definitions, common
  false-positive patterns by rule class, and the suppression-rationale format.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `supply-chain-security-reviewer`,
  `security-pr-reviewer`, `secure-migration-reviewer`, and the shipped
  `code-reviewer` (security-review cluster).
