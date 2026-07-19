---
name: skill-quality-reviewer
description: 'Review ONE library skill''s quality — the judgment layer above scripts/validate-skills.py. Runs the mechanical validator first (structure/lengths/registration/name collisions are its job — never re-checked), judges what it cannot: description trigger-oriented ("use when <situation>") vs merely descriptive; trigger collision with shipped skills, colliders NAMED (the main failure mode across the full shipped skill corpus); duplication better shipped as an EXTENSION (the LLM03/ASI04 pattern); evals that test real boundaries vs hollow filler; section substance (Stop Conditions that actually refuse); scope (one job); invocation posture (manual-only iff side effects). Per-check PASS/CONCERN/FAIL with evidence; verdict ship/revise/reject/make-it-an-extension. Use when a skill is drafted, revised, or quality-audited. Do NOT use for a change''s process compliance (agent-governance-audit), product code (code-reviewer, full-codebase-auditor), or a whole skill-adding PR (library-diff-reviewer).'
---

# Skill Quality Reviewer

## Purpose

Give one skill — newly drafted or already shipped — the review the mechanical
validator cannot perform. `scripts/validate-skills.py` proves a skill is
structurally VALID; this skill judges whether it is GOOD: whether an AI
matching a user request against the full shipped corpus of descriptions
would pick it at the right moment and yield at the wrong one, whether it
earns a place in the library instead of duplicating one, and whether its
evals would actually catch it misbehaving. The deliverable is a per-check
verdict with cited evidence and one overall recommendation a maintainer can
act on: ship, revise, reject, or make-it-an-extension of a named existing
skill.

## Use When

- Use when: a new skill has been drafted and needs quality review before it
  enters the library.
- Use when: asked to audit an existing shipped skill's quality — trigger
  precision, overlap with newer skills, eval honesty, scope creep.
- Use when: a skill-adding change is in flight and the question is "is this
  skill good enough and distinct enough to ship?"
- Do NOT use when: the question is whether an agent CHANGE followed process —
  classification, approvals, merge authority, closeout — that is
  `agent-governance-audit` (different target: a change's process trail, not a
  skill definition's quality).
- Do NOT use when: reviewing product code — a diff is `code-reviewer`,
  whole-repo health is `full-codebase-auditor`. This skill's only target is a
  skill definition under `.claude/skills/`.
- Do NOT use when: auditing a skill-adding PR end-to-end (CI validator run,
  catalog integrity, branch/merge discipline) — that is `library-diff-reviewer`
  (D13, built D22). This skill is that review's inner loop: it judges ONE
  skill's quality; the PR-level mechanics belong to that skill.
- Do NOT use to re-run what the validator enforces: a validator FAIL goes
  back to the author against the standard — quality review never starts from
  a structurally invalid skill.

## Inputs to Inspect

1. The target skill's full directory: `SKILL.md` (frontmatter and every
   section), `references/*`, `evals/evals.json`, and `evals/trigger-evals.json`
   when present.
2. [`docs/skill-generation-standard.md`](../../../docs/skill-generation-standard.md)
   — the standard this review judges against (all eight sections).
3. Fresh output of `python scripts/validate-skills.py` — the mechanical gate
   this review builds on and never re-implements.
4. Every shipped skill's frontmatter `description` (`.claude/skills/*/SKILL.md`)
   — the corpus for the overlap sweep; the nearest neighbors read in full,
   not just their descriptions.
5. [`docs/skills-catalog.md`](../../../docs/skills-catalog.md) — which overlap
   cluster the skill claims and which discrimination its neighbors already
   ship in their trigger-evals.
6. `RESERVED_BUNDLED_NAMES` in `scripts/validate-skills.py` — the validator
   blocks exact collisions; judgment must also catch confusably-close names.

## Workflow

1. **Gate on the mechanical validator.** Run
   `python scripts/validate-skills.py` (or confirm a fresh pass on the exact
   revision under review). If it fails, stop and return the output — structure
   precedes judgment. Everything the validator enforces (frontmatter parse,
   name==directory, description present and < 1024 chars, no broad
   allowed-tools, < 500 lines, all nine sections present, evals JSON parse,
   catalog + README registration, duplicate and reserved-name collisions) is
   settled by that run and is NOT re-checked or re-scored below: a mechanical
   PASS is this review's entry ticket, never part of its verdict.
2. **Check 1 — trigger quality.** Is the description trigger-ORIENTED — does
   it state the situations that should invoke it ("use when …") and the
   near-misses that should not ("do NOT use …") — rather than merely
   descriptive ("this skill does X")? Trigger-oriented descriptions are what
   make auto-invocation work; a feature list with no situation is a FAIL even
   at 900 well-formed characters.
3. **Check 2 — trigger overlap/collision (highest-value check).** Sweep every
   shipped description and ask, per plausible user request: would an AI know
   which skill wins? NAME each colliding skill and quote the request that
   confuses them. Overlap without shipped discrimination (trigger-evals
   naming that exact neighbor) is a CONCERN at best, a FAIL when the loser
   would fire on the winner's core case.
4. **Check 3 — duplication / extension.** Does the skill substantially restate
   a shipped skill's job? When the genuinely new content would fit as a
   scoped additive diff to an existing skill, recommend make-it-an-extension
   and name the base — the library's precedent: LLM03 and ASI04 both landed
   as extensions of `supply-chain-security-reviewer`, not as clone skills.
5. **Check 4 — eval integrity.** Do `evals/evals.json` cases test the
   BOUNDARY: a real happy path, a genuine edge (not a happy path with an
   adjective), a should-not-trigger case a neighbor would actually contest,
   and a should-not-do/refusal case with teeth? Does `trigger-evals.json`
   discriminate against the RIGHT neighbors — the ones check 2 found, not a
   convenient strawman?
6. **Check 5 — section substance.** Are the nine sections filled or merely
   present to satisfy the validator? Especially: Stop Conditions are real
   halt/refusal conditions (who is refused, what triggers the halt), Use When
   is specific with counter-examples, Gotchas are earned failure modes rather
   than platitudes.
7. **Check 6 — scope discipline.** One job done well, or a catch-all that
   should split? Count the distinct jobs a stranger would say it performs.
8. **Check 7 — invocation posture.** `disable-model-invocation: true` iff the
   skill has side effects (edits files/config outside scratch, runs
   state-changing commands, calls networks, deploys, spends money); pure
   review/design/report skills stay auto-invocable. Manual-only skills must
   name the irreversible step in Stop Conditions.
9. **Deliver the verdict.** Per check PASS / CONCERN / FAIL, each citing
   evidence (quoted description phrases, the named colliding skill, the
   hollow eval case id), then ONE overall recommendation: ship | revise |
   reject | make-it-an-extension (with the named base skill), plus the
   specific revisions required before ship.

Per-check criteria, the trigger-oriented-description rubric, the overlap
sweep procedure, hollow-eval patterns, and the posture decision table:
[references/quality-review-checklist.md](references/quality-review-checklist.md).

## Output Format

```
SKILL QUALITY REVIEW — <skill-name>
Validator:   PASS (<run output line>) | FAIL → review stopped, output returned
Standard:    docs/skill-generation-standard.md; corpus swept: <N> shipped skills
Checks:
  1 Trigger quality        PASS | CONCERN | FAIL — <quoted description evidence>
  2 Overlap/collision      PASS | CONCERN | FAIL — <colliding skill(s) + the request that confuses them | "none found">
  3 Duplication/extension  PASS | CONCERN | FAIL — <overlapped skill + what an extension diff would contain>
  4 Eval integrity         PASS | CONCERN | FAIL — <hollow/missing case types, by case id>
  5 Section substance      PASS | CONCERN | FAIL — <present-but-empty sections, quoted>
  6 Scope discipline       PASS | CONCERN | FAIL — <the distinct jobs found, if more than one>
  7 Invocation posture     PASS | CONCERN | FAIL — <side effects found vs posture declared>
Recommendation: ship | revise | reject | make-it-an-extension of <base skill>
Colliding skills: <named list | none>
Required before ship: <specific revisions, each mapped to a check>
Not inspected: <what this review did not read, and why>
```

## Validation Checklist

- [ ] Mechanical validator ran fresh (or a fresh pass was confirmed) BEFORE
      any judgment; no validator check was re-implemented or re-scored here.
- [ ] Every non-PASS verdict cites concrete evidence — quoted text, a named
      skill, an eval case id; no vibes-only CONCERN.
- [ ] The overlap sweep covered ALL shipped descriptions, not only the
      skill's own cluster or phase.
- [ ] Colliding skills are NAMED wherever check 2 or 3 is non-PASS.
- [ ] The recommendation is exactly one of the four verdicts;
      make-it-an-extension names its base skill.
- [ ] Nowhere does the report treat the mechanical PASS as evidence of
      quality.
- [ ] Not-inspected list present and honest.

## Gotchas

- The rubber-stamp trap: "the validator passed" answers structure, not
  quality. The failure populations barely overlap — a perfectly structured
  skill can still be unpickable, colliding, hollow, or a duplicate.
- Descriptions written to impress rather than to trigger: capability lists
  with no situation. The working test: from this description alone, would a
  model know when this skill WINS a request and when it must YIELD?
- Overlap hides across phases: the confusable neighbor is often in a
  different pack (agent authority vs end-user RBAC; LLM04 vs ASI06
  poisoning; evidence-policy vs manual-QA evidence). Same-cluster-only
  sweeps miss exactly these.
- Hollow evals look full: assertions that restate the Workflow verbatim, a
  should-not-trigger prompt nothing would ever route here anyway, an "edge"
  that is the happy path with a twist adjective, refusal cases the skill
  text never actually promises to refuse.
- Present-but-empty sections satisfy the validator: "Stop Conditions: ask
  the user when unsure" is a filled header with no refusal in it.
- A CONCERN pile-up is itself a verdict: several small concerns across
  trigger + evals + substance normally roll up to revise, not
  ship-with-nits.
- Invocation posture drifts on revision: a review skill that gains a "then
  apply the fix" step becomes side-effecting and must flip to manual-only —
  re-check posture on every re-review, not just at birth.
- Near-miss names pass the collision check: the validator blocks only EXACT
  reserved/duplicate names; `code-review-helper` next to the bundled
  `code-review` is a judgment finding, not a validator error.

## Stop Conditions

- Asked to approve or ship a skill BECAUSE the mechanical validator passed →
  refuse the shortcut: mechanical pass is necessary, never sufficient. Run
  the judgment checks or return no verdict.
- Asked to soften or flip an evidence-backed FAIL, or to unname a colliding
  skill → refuse; the report states what the evidence states.
- The target skill's directory or SKILL.md is missing or unreadable → stop;
  there is no quality review of a skill from its description or from memory.
- The mechanical validator FAILS on the target revision → stop the quality
  review and return the validator output; structure precedes judgment.
- Asked to EDIT the skill to fix the findings → out of scope: this skill
  reviews and changes nothing. Hand the required-before-ship list to the
  author (or a build session) and re-review the revision.
- The standard and the validator disagree on a rule (one demands what the
  other ignores) → surface the discrepancy to a human; do not silently pick
  a side.

## Supporting Files

- [references/quality-review-checklist.md](references/quality-review-checklist.md)
  — per-check PASS/CONCERN/FAIL criteria, the trigger-oriented-description
  rubric with examples, the full-corpus overlap sweep procedure, the
  hollow-eval pattern catalog, and the invocation-posture decision table.
- `evals/evals.json` — behavior cases, including the
  descriptive-description-plus-collision → revise case and the
  no-rubber-stamp-on-mechanical-pass refusal.
- `evals/trigger-evals.json` — discrimination against
  `agent-governance-audit`, `full-codebase-auditor`, `code-reviewer`, and
  the `library-diff-reviewer` seam (built D22; owned from both sides).
