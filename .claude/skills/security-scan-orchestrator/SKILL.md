---
name: security-scan-orchestrator
description: Orchestrate a whole-repo security scan and aggregate it into ONE prioritized report — coordinate the static suite (SAST + dependency/SCA + secret + IaC/config scanning), normalize every scanner's output into one finding schema, and route it. It RUNS and AGGREGATES; it does NOT triage findings (finding TRIAGE is static-analysis-reviewer's — yield) and NEVER fixes, opens PRs, or changes settings — every action is handed to a human. Tool-agnostic (scanner CATEGORIES, not one vendor's CLI). Fail-closed: a scanner that errors or cannot run is a REPORTED GAP, never a silent clean pass. Use when asked to security-scan a whole repo, run the scan suite, or aggregate multi-tool findings. Do NOT use to triage findings (static-analysis-reviewer), judge dependency risk (supply-chain-security-reviewer), design the SAST run (sast-orchestration-designer), or test a running app (dast-safety-harness-designer).
---

# Security Scan Orchestrator

## Purpose

A scan suite that runs but never gets aggregated is a pile of siloed reports
nobody reconciles; a suite that reports "clean" when one scanner silently
failed is a lie with an exit code. This skill orchestrates a WHOLE-REPO static
security scan and turns it into ONE report. The deliverable has four
load-bearing parts: (1) a defined scan **scope** — what is in, what is excluded,
and why each exclusion is a decision and not a silent gap; (2) a **coordinated
run** of the applicable scanner categories (SAST, dependency/SCA, secret,
IaC/config), tool-agnostic, each with its exit status, version, and ruleset
captured; (3) **normalized, deduplicated findings** in one schema with severity
aggregated onto one scale and cross-tool duplicates collapsed; and (4) an
explicit **coverage + gap** account where any scanner that errored, timed out,
or could not run is surfaced as a GAP. This skill RUNS and AGGREGATES. It does
NOT triage the findings — the true-positive / false-positive / ranking JUDGMENT
belongs to `static-analysis-reviewer`, and dependency/provenance judgment to
`supply-chain-security-reviewer` — and it fixes nothing, opens no PR, changes no
setting: every action is handed to a human. It PRODUCES the report those skills
and that human act on.

## Use When

- Use when: asked to run a whole-repo security scan, stand up the scanning
  suite, or aggregate multiple scanners' output into one prioritized report.
- Use when: several scanners run but their outputs are siloed — separate
  reports, no cross-tool dedup, no unified severity, no single coverage view.
- Use when: a security-scan gate needs one normalized report (with an honest
  gap list) to gate on, rather than N disconnected tool outputs.
- Auto-invocable: it orchestrates read-only scanners over a repo and produces a
  report; it changes no code, fixes nothing, and grants no authority — so it
  carries no side-effect gate. Any remediation is a separate human-owned step.
- Do NOT use when: the job is to TRIAGE/interpret findings — decide which are
  real, rank them, write suppression verdicts — that is
  `static-analysis-reviewer`. This skill produces the findings; that skill
  judges them (the orchestrate-vs-triage seam — yield).
- Do NOT use when: the question is what a dependency/CVE/provenance finding
  MEANS or whether it is reachable — that JUDGMENT is
  `supply-chain-security-reviewer`; this skill orchestrates the dependency-scan
  RUN and folds its output into the aggregate.
- Do NOT use when: the subject is HOW the SAST run itself is designed — tool
  selection, ruleset/config, baseline + diff-scanning, governed suppression —
  that is `sast-orchestration-designer` (in-batch); this skill aggregates what
  that produces alongside the other categories.
- Do NOT use when: the testing is DYNAMIC against a running app — that is
  `dast-safety-harness-designer`, which carries a written-authorization gate;
  do not fold live-app testing into a static repo scan.
- Do NOT use when: wiring the scan into the delivery pipeline — that is
  `ci-pipeline-architect`; this skill produces the scan/report contract the
  pipeline runs, it does not own the pipeline.

## Inputs to Inspect

1. Repo scope: languages, directories, and what is deliberately out of scope
   (vendored, generated, fixtures) — each exclusion recorded with a reason.
2. Which scanner CATEGORIES apply to THIS repo: SAST (per language), dependency
   /SCA, secret scanning, IaC/config — and which are not applicable and why.
3. Existing scan config, baselines, and suppression lists already in the repo,
   so prior decisions are respected and stale suppressions are visible.
4. Where findings go today: siloed per-tool reports, an unaggregated dump, or a
   gate — and whether coverage (what did NOT run) is tracked at all.
5. The consuming step: is a human or `static-analysis-reviewer` triaging, is CI
   gating, and at what severity threshold — the report is shaped for that.
6. Provenance needs: the exact commit/ref scanned, and the tool + version +
   ruleset that produced each finding, so the report is reproducible.

## Workflow

1. **Define the scan scope.** State what is in scope and what is excluded, with
   a reason per exclusion. An undocumented exclusion is an invisible blind spot;
   a documented one is an auditable decision.
2. **Select scanner categories, tool-agnostic.** For the repo, name the
   applicable categories — SAST, dependency/SCA, secret, IaC/config — by what
   each must cover, not by a vendor's product. A category with no available tool
   for a language is a stated coverage gap, not silence.
3. **Orchestrate the run.** Run each scanner against the pinned ref; capture its
   exit status, version, and ruleset. A scanner that errors, times out, or does
   not support a language is recorded as a GAP — never dropped, never treated as
   "0 findings = clean" (fail-closed).
4. **Normalize** every scanner's native output into one finding schema:
   stable id, category, rule, location, native severity, provenance, and a
   fingerprint for dedup.
5. **Deduplicate across tools.** Collapse findings that are the same issue
   reported by multiple scanners (or multiple rules) into one, keeping every
   tool's provenance as evidence. (This is aggregation-time cross-TOOL dedup —
   not the within-tool triage `static-analysis-reviewer` does.)
6. **Aggregate severity onto one scale.** Map each tool's native severity to a
   single normalized scale and record the mapping — one tool's HIGH is not
   another's; concatenating raw severities is not aggregation.
7. **Assemble the ONE report** per Output Format: coverage (what ran, what did
   not, and why), normalized deduped findings, the GAP list, provenance, and the
   routing of triage and any action to their owners. Do NOT triage or fix here.
8. **Prove the fail-closed path.** Design the check that a failed/absent scanner
   shows up as a GAP and cannot pass as clean — a scan that cannot run is not a
   clean scan, and a verifier that cannot fail is theater with an exit code.

## Output Format

```
WHOLE-REPO SECURITY SCAN REPORT — <repo @ ref>
Scope: <in-scope>            Excluded: <path — reason>
Suite (category → tool-agnostic): SAST | dependency/SCA | secret | IaC/config
Coverage: <category → ran | FAILED | not-applicable; version; ruleset; ref>
Findings (normalized, deduped — NOT triaged):
  [CRIT|HIGH|MED|LOW] <category>/<rule> @ <file:line>
    provenance: <tool+version+ruleset>   fingerprint: <hash>
Duplicates collapsed (cross-tool): <n>
GAPS (fail-closed — a scanner that could not run is NOT a clean pass):
  <category/tool — error | timeout | unsupported — what is UNKNOWN as a result>
Severity aggregation: <native → normalized scale mapping>
Routing (this skill acts on nothing):
  finding TRIAGE → static-analysis-reviewer
  dependency/provenance JUDGMENT → supply-chain-security-reviewer
  fixes / actions → human
Handoffs: SAST run design → sast-orchestration-designer;
  CI wiring → ci-pipeline-architect;
  dynamic/running-app testing → dast-safety-harness-designer (needs written authorization)
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Scope defined; every exclusion carries a reason (no silent blind spots).
- [ ] Scanner categories named tool-agnostically; inapplicable categories and
      unscannable languages stated as gaps.
- [ ] Every scanner's exit status, version, and ruleset captured against a
      pinned ref.
- [ ] Every failed/absent scanner surfaced as a GAP — none dropped or read as
      "0 findings = clean."
- [ ] Findings normalized into one schema; cross-tool duplicates collapsed with
      all provenance kept.
- [ ] Severity aggregated onto one scale with the mapping recorded.
- [ ] No triage/interpretation done here — the TP/FP/ranking verdict is yielded
      to `static-analysis-reviewer`.
- [ ] No fix applied, no PR opened, no setting changed — every action routed to
      a human.
- [ ] The fail-closed gap path has a designed proof it fires.

## Gotchas

- Zero findings because a scanner RAN and found nothing is the opposite fact
  from zero findings because it FAILED to run — conflating them is the classic
  false green. The gap list exists to keep them apart.
- Two tools flagging the same sink is one issue, not two; skipping cross-tool
  dedup inflates the backlog and hides the real count.
- Native severities are not comparable across tools — one scanner's HIGH is
  another's MEDIUM. Normalize onto one scale and record the mapping.
- Aggregation is not triage: producing counts and a severity-sorted list is not
  deciding what is real. The moment you start marking false positives you have
  crossed into `static-analysis-reviewer`'s lane — stop and yield.
- "The scan passed" from a suite whose SAST step silently skipped an
  unsupported language is a coverage lie — the unscanned surface is a gap.
- Secret-scanner hits are sensitive: the report references the location, never
  echoes the secret value into the aggregate or logs.

## Stop Conditions

- Asked to FIX a finding, auto-remediate, open a PR, or change a setting →
  refuse; this orchestrates and reports, and every action is the human's
  (orchestrate-and-report, human-approves-action).
- Asked to TRIAGE / interpret which findings are real, or to rank/suppress them
  on the merits → hand to `static-analysis-reviewer`; this skill produces the
  findings, it does not judge them.
- Asked to report a suite as clean when a scanner errored, timed out, or could
  not run → refuse; a scan that cannot run is not a clean scan (fail-closed) —
  surface the gap.
- The suite would include DYNAMIC / running-app testing → that is
  `dast-safety-harness-designer` with a written-authorization gate; do not fold
  it into a static repo scan.
- A secret-scanner surfaces a live credential → report its location and route to
  human containment (`human-approval-boundary`); do not echo or exfiltrate the
  value.

## Supporting Files

- `evals/evals.json` — behavior cases: the siloed-outputs aggregation, the
  failed-scanner-is-a-gap fail-closed edge, the interpret-these-findings
  should-not-trigger (→ `static-analysis-reviewer`), and the auto-fix and
  report-errored-scan-as-clean refusals.
- `evals/trigger-evals.json` — discrimination against `static-analysis-reviewer`
  (triage vs orchestration), `supply-chain-security-reviewer` (dep/provenance
  judgment vs the dep-scan run), `sast-orchestration-designer` (in-batch: SAST
  run design vs whole-repo aggregation), `dast-safety-harness-designer`
  (dynamic vs static), and `ci-pipeline-architect` (pipeline vs scan contract).
- No `references/` — the report contract above is the complete procedure;
  detail lives in the produced report.
