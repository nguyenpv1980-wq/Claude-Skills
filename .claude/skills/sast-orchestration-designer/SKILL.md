---
name: sast-orchestration-designer
description: 'Design HOW a SAST suite is RUN over a repository — category-level analyzer selection (not a named vendor), ruleset/config management, baseline + diff-scanning (gate NEW-since-baseline on PRs vs full scans), incremental-vs-full strategy, a GOVERNED false-positive suppression list (never silent inline muting), and CI integration. Designs the RUNNING of SAST and feeds the whole-repo aggregator (security-scan-orchestrator, in-batch); the INTERPRETATION of findings (true/false-positive, ranking, the suppression VERDICT) is static-analysis-reviewer''s (yield). Fail-closed: a scan that errors, times out, or skips a language is a REPORTED GAP, never a silent pass. Use when standing up or tuning SAST, designing baseline/diff scanning, or governing FP suppression. Do NOT use to triage findings (static-analysis-reviewer), aggregate a whole-repo scan (security-scan-orchestrator), or scan dependencies (supply-chain-security-reviewer).'
---

# SAST Orchestration Designer

## Purpose

Static analysis is only as useful as the way it is run: a suite with no
baseline drowns a team in pre-existing noise, one that only scans changed files
never catches a latent bug in untouched code, and one whose suppressions are
silent inline comments accumulates invisible debt. This skill designs HOW a
SAST suite RUNS over a repository. The deliverable has seven load-bearing
parts: (1) category-level analyzer **selection** per language/framework,
tool-agnostic; (2) **ruleset/config** management, versioned in-repo; (3) a
**baseline + diff-scanning** design — gate NEW findings on a PR, run a full
scan on a cadence, and refresh the baseline under governance; (4) a **governed
suppression** workflow where every suppression is a reviewed, rationale-bearing,
owned entry in a version-controlled list, never a silent mute; (5) an
**incremental-vs-full** strategy fit to the CI latency budget; (6) **CI
integration** with merge-blocking semantics and a fail-closed error rule; and
(7) the **handoff** of results to triage. This skill designs the RUN that
PRODUCES findings; the INTERPRETATION of those findings — true-positive /
false-positive, ranking, and the suppression VERDICT — belongs to
`static-analysis-reviewer`. It produces one input to the whole-repo aggregate,
`security-scan-orchestrator` coordinates.

## Use When

- Use when: standing up SAST on a repo for the first time, or tuning an existing
  run that is too noisy, too slow, or missing a language.
- Use when: designing baseline capture + diff-scanning — a PR gate on
  NEW-since-baseline findings plus a full scan on a cadence.
- Use when: the false-positive suppression list has degraded into silent inline
  muting and needs to become a governed, reviewed, rationale-bearing artifact.
- Use when: deciding incremental (PR / changed-files) vs full-repo scan cadence
  and where each sits in CI within a latency budget.
- Auto-invocable: it designs the run and produces a plan/config design; it runs
  nothing against production, changes no code, and fixes nothing — so it carries
  no side-effect gate.
- Do NOT use when: interpreting the findings a SAST run produces — deciding
  true vs false positive, ranking, or writing the suppression verdict — that is
  `static-analysis-reviewer` (the orchestrate-vs-triage seam — yield). This
  skill designs the RUN; that skill JUDGES the output.
- Do NOT use when: aggregating a whole-repo multi-tool scan (SAST + dependency +
  secret + IaC) into one report — that is `security-scan-orchestrator`
  (in-batch); this SAST-run design is one input it coordinates.
- Do NOT use when: the subject is dependency/CVE/provenance scanning — that is
  the SCA category owned by `supply-chain-security-reviewer`, not SAST.
- Do NOT use when: designing the whole delivery pipeline — that is
  `ci-pipeline-architect`; this skill produces the SAST stage's contract that
  plugs into it.
- Do NOT use when: reviewing the security of the scan-error-handling CODE for
  fail-closed correctness — that is `error-handling-security-reviewer`; this
  skill designs the fail-closed run behavior it can then review.

## Inputs to Inspect

1. Languages/frameworks in the repo → which SAST analyzer category applies to
   each; a language with no configured analyzer is a coverage gap, not silence.
2. Current SAST config/ruleset if any: enabled rule classes, severity
   thresholds, custom rules, and how they are stored (versioned vs ad-hoc).
3. Existing baseline and suppression list: how suppressions are recorded today
   (silent inline mute vs governed entry), and how stale they are.
4. Repo size and change rate → informs incremental vs full cadence and whether a
   full scan fits the CI latency budget.
5. Where SAST runs today (local, PR CI, nightly) and what, if anything, it
   gates or merge-blocks.
6. The triage consumer: who receives findings — `static-analysis-reviewer`, a
   security gate, or `security-scan-orchestrator` for whole-repo aggregation.

## Workflow

1. **Select the SAST approach by category** for each language/framework,
   tool-agnostic — name what must be covered, not a vendor. A language with no
   analyzer is a stated coverage gap.
2. **Manage the ruleset/config.** Enabled rule classes, severity thresholds, and
   any custom rules live versioned in-repo and are reviewed like code — not
   tuned ad-hoc on the CI box.
3. **Design baseline + diff-scanning.** Capture a baseline of known findings; a
   PR scan gates on NEW findings vs the baseline; a full scan runs on a cadence.
   Define how the baseline is refreshed and burned down under governance — never
   auto-erased to make a gate green.
4. **Design the governed suppression workflow.** A suppression is an entry in a
   version-controlled list — rule id, location, written rationale, owner, date,
   and expiry/review — reviewed like code, never a silent inline mute. This
   skill designs the LIST and its governance; the DECISION that a specific
   finding is a false positive worth suppressing is `static-analysis-reviewer`'s
   triage VERDICT — this skill does not populate verdicts.
5. **Choose incremental vs full strategy and cadence**, fit to the CI latency
   budget: incremental for fast PR feedback, full on a cadence for completeness.
   Neither alone is sufficient — pair them.
6. **Integrate into CI.** Place the stage, define merge-blocking on NEW findings,
   and set the fail-closed rule: a scan that errors, times out, or skips a
   language FAILS the gate, it does not pass green. Cite `ci-pipeline-architect`
   for the pipeline itself.
7. **Define the handoff.** Normalized SAST output goes to
   `static-analysis-reviewer` for triage and/or to `security-scan-orchestrator`
   for whole-repo aggregation. This skill does not triage.
8. **Prove the fail-closed path.** Design the check that a scan
   error/timeout/skipped-language surfaces as a gate failure or gap — a scan
   that cannot run is not a clean scan, and a verifier that cannot fail is
   theater with an exit code.

## Output Format

```
SAST RUN DESIGN — <repo>
Coverage: <language/framework → SAST analyzer category; unsupported = stated GAP>
Ruleset/config: <enabled rule classes, severity thresholds, custom rules; versioned in-repo>
Baseline + diff: <baseline capture; PR gate = NEW-since-baseline; full-scan cadence; refresh/burn-down policy>
Suppression (GOVERNED list, NOT silent mute):
  <entry = rule id + location + written rationale + owner + date + expiry/review>
  — the FP/accepted VERDICT is static-analysis-reviewer's, not this skill's
Scan strategy: <incremental (PR/changed-files) + full (cadence); CI latency-budget fit>
CI integration: <stage placement; merge-blocking on NEW findings>  (pipeline → ci-pipeline-architect)
Fail-closed: <scan error/timeout/skipped-language ⇒ gate FAILS / GAP surfaced; the proof it fires>
Handoff: findings TRIAGE → static-analysis-reviewer;
  whole-repo aggregation → security-scan-orchestrator;
  secure error-path review → error-handling-security-reviewer
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Analyzer coverage stated per language; unsupported languages are gaps, not
      silence.
- [ ] Ruleset/config is versioned in-repo and reviewed like code.
- [ ] Baseline + diff-scanning designed with a governed refresh/burn-down (not
      auto-erased).
- [ ] Suppression is a governed, reviewed, rationale-bearing list — and the
      FP/accepted VERDICT is yielded to `static-analysis-reviewer`, not decided
      here.
- [ ] Incremental and full scanning are paired; cadence fits the CI latency
      budget.
- [ ] CI integration has merge-blocking semantics and a fail-closed error rule.
- [ ] The fail-closed path (scan error/skip ⇒ gate fails/gap) has a designed
      proof it fires.
- [ ] Findings are handed to triage/aggregation — not interpreted here.
- [ ] No fix applied and no finding acted on — this designs the run only.

## Gotchas

- A baseline that "accepts everything currently here" with no burn-down means
  real issues live in the baseline forever — the baseline needs a reduction
  policy, not just a snapshot.
- Silent inline suppression comments sprinkled through the code ARE the
  anti-pattern: a suppression with no rationale, no owner, and no review is
  invisible debt. Govern the list.
- Suppressing is not triaging: this skill designs WHERE suppressions live and
  HOW they are governed; WHICH findings deserve suppression is
  `static-analysis-reviewer`'s verdict — do not cross into deciding TP/FP.
- Diff-scanning that only ever scans changed files never catches a latent issue
  in untouched code — pair PR-incremental with a periodic full scan.
- A run that skips an unsupported language and reports "0 findings" is a false
  green — the coverage gap must surface (fail-closed), not vanish.
- Tuning rules down to cut noise can silence an entire vulnerability class —
  noise reduction is triage's job (rank/suppress with rationale), not blanket
  rule-disabling at the run layer.

## Stop Conditions

- Asked to TRIAGE the findings — decide TP/FP, rank them, or write suppression
  verdicts → hand to `static-analysis-reviewer`; this designs the run, not the
  judgment.
- Asked to silently mute findings or disable a rule class to make a gate green
  with no rationale → refuse; suppression is a governed, rationale-bearing,
  reviewed list.
- Asked to treat or report a scan that errored, timed out, or skipped a
  language as clean → refuse; a scan that cannot run is not a clean scan
  (fail-closed).
- Asked to auto-fix the findings → refuse; this designs the RUN — fixes are the
  human's / `appsec-implementer`'s.
- The ask is actually whole-repo multi-tool aggregation → hand to
  `security-scan-orchestrator` (in-batch).

## Supporting Files

- `evals/evals.json` — behavior cases: the noisy-first-time SAST setup, the
  governed-suppression-not-silent-mute edge, the interpret-these-findings
  should-not-trigger (→ `static-analysis-reviewer`), and the silent-mute-to-go-
  green and treat-errored-scan-as-clean refusals.
- `evals/trigger-evals.json` — discrimination against `static-analysis-reviewer`
  (triage vs run design), `security-scan-orchestrator` (in-batch: whole-repo
  aggregation vs single-category run design, pinned both ways),
  `supply-chain-security-reviewer` (SCA vs SAST), and `ci-pipeline-architect`
  (pipeline vs the SAST stage contract).
- No `references/` — the run-design contract above is the complete procedure;
  detail lives in the produced design.
