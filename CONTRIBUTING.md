# Contributing

Contributing to this project follows **[Zero Trust AI Engineering Discipline](docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md)**
(Zet-AI Engineering for short) —
*"Never trust, always verify — every step of the lifecycle. Assume drift. Demand evidence.
Track everything."* This project teaches that discipline as a skill library; it also
practices it on itself. Whether you are a human contributor or an AI assistant, the rules
below are how work gets done here: nothing is trusted from memory, assertion, or a closeout
summary — every claim is verified against the real repository, the real validator run, and
the real approval record before it is trusted or merged.

## Operating rules

Each rule is enforceable, and each carries the reason it exists — drawn from this project's
own proven practice, including failures it absorbed during its own construction.

1. **One session per repo at a time.** Cross-repo parallel work is fine; two sessions in
   *this* repo at once is not.
   *Why:* concurrent sessions share one checkout and collide — branch squatting and
   stale-memory re-merges — a proven failure mode here.

2. **Evidence before merge.** Every change is independently verified — validator green, and
   claims checked against the actual repo state (git, PRs, files) — before it merges.
   *Why:* a closeout is a claim, not proof; trusting it instead of checking is exactly how
   rot sets in.

3. **No auto-merge.** Human approval is the merge gate; auto-merge is never armed.
   *Why:* an ungoverned auto-merge is one of this project's documented incidents. The **one**
   governed exception is the `standing-approval-and-auto-advance` (P3) pattern, which defines
   the only safe autonomous-merge path — within a **named scope**, with an explicit
   **opt-out**, and never extending to a protected-branch merge or arming auto-merge, which
   stay human-only.

4. **Track every decision.** Material decisions are recorded in
   [`docs/reconciliation/step-0-reconciliation-v4.md`](docs/reconciliation/step-0-reconciliation-v4.md)
   §5 as dated `D`-entries. Decisions are immutable once recorded: correct forward with a new
   entry, never rewrite history.
   *Why:* if the decision record can be silently edited, no one can trust what was decided —
   and decisions get re-litigated (drift).

5. **Verify state before acting.** Reconcile memory and assumptions against live git/PR
   reality before making any change; never act on remembered state alone.
   *Why:* sessions acting on stale memory is a documented incident here — a path that exists
   is not proof it is the right repo, and a remembered SHA is not the current one.

6. **Full closeouts with honest gaps.** Every task ends with what was done **and** an
   explicit *"intentionally not done"* section (write "None" when empty). An unqualified
   "complete" is allowed **only** once every gap is closed with evidence.
   *Why:* a silent scope reduction reported as "done" is the most expensive kind of drift —
   it is discovered only when the missing work is needed.

7. **Small, reviewable diffs; exact-file staging; branch identity verified before every
   commit, push, and PR.** Stage the specific files you changed — never `git add -A` on a
   shared checkout — and run `git branch --show-current` before each commit/push/PR.
   *Why:* small diffs get real review; exact staging and a branch check prevent committing a
   neighbor session's work or pushing to the wrong branch.

8. **The validator is the structural gate.** `python scripts/validate-skills.py` must pass
   (**exit 0**) before any PR. Skills that do not register in the
   catalog and README fail validation.
   *Why:* the validator is the one automated check that the library's structure is intact; a
   red validator means the change is not shippable, full stop.

## How to add a skill

1. Copy the `_template` skill directory to `.claude/skills/<your-skill-name>/` and rename it
   so `name` matches the new directory.
2. Rewrite every section against
   [`docs/skill-generation-standard.md`](docs/skill-generation-standard.md) — required
   sections, description length, discriminating triggers, overlap avoidance, and evals.
3. Register the skill in the catalog ([`docs/skills-catalog.md`](docs/skills-catalog.md)) and
   the [README](README.md).
4. Run `python scripts/validate-skills.py` and confirm it reports the new count with exit 0
   before opening a PR (rule 8).

## How to bank a decision

Record material decisions as dated `D`-entries in §5 of
[`docs/reconciliation/step-0-reconciliation-v4.md`](docs/reconciliation/step-0-reconciliation-v4.md).
Number the entry after the last one, date it, and state what was decided and why. Never edit
a prior entry to change history — supersede it with a new, forward-correcting entry (rule 4).

## On self-auditing

Rules 2 and 8 are enforced by human review plus the validator — and now by the library's own
judgment layer. The shipped skill **`skill-quality-reviewer`** (built D18; see the
reconciliation doc, §3) automates that self-audit — checking a skill-adding change against the
generation standard and the validator gate so every addition gets the review the standard
demands.
