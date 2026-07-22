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
   (**exit 0**) before any PR. One-time local setup: `python -m pip install pyyaml` — the
   strict frontmatter parse (D50) requires it, and the validator fails closed without it
   (CI installs it automatically). Skills that do not register in the
   catalog and README fail validation.
   *Why:* the validator is the one automated check that the library's structure is intact; a
   red validator means the change is not shippable, full stop.

## How to add a skill

1. Copy the `_template` skill directory to `.claude/skills/<your-skill-name>/` and rename it
   so `name` matches the new directory.
2. Rewrite every section against
   [`docs/skill-generation-standard.md`](docs/skill-generation-standard.md) — required
   sections, description length, discriminating triggers, overlap avoidance, and evals.
   Description contract: strict-YAML-valid (single-quote it if it contains `: `), parsed
   value < 1024 chars, capability front-loaded; manual-only skills carry the
   `MANUAL-ONLY; never auto-invoke. ` sentinel first *(validator-enforced — see the
   Portability contract in the standard)*.
3. **Register the skill on every surface it must appear on.** "Register in the README" is not
   one table — it is all of the surfaces below. The validator mechanically enforces the
   deterministic parts (3a, 3b, 3d, and the family-count reconciliation); the judgment parts —
   3c's flagship choice, 3e's role decision, 3f's pillar link — are yours. The rule lists them
   all so "register the README" can't quietly mean "add to one table and forget the rest":
   - **3a. [`docs/skills-catalog.md`](docs/skills-catalog.md)** — add the skill to the
     appropriate section. *(validator-enforced: the name must appear.)*
   - **3b. [README](README.md) → the "Skills (shipped)" table** — add the skill's row.
     *(validator-enforced: the name must appear.)*
   - **3c. [README](README.md) → the roster family under "What's in the library"** (the numbered
     family list) — if the skill is a flagship example of its family, add it to that family's
     `*e.g.*` list, and **increment that family's count** in the `*(Phase/D, N)*` marker. If it
     starts a **new** family, add the family line **and** increment the marked
     `FAMILY-COUNT`. *(The flagship choice is judgment; the family-count total is
     validator-enforced — see 3d.)*
   - **3d. [README](README.md) → the count claims** — the current-total ("N skills") and the
     family count ("N discipline families") must match reality. The authoritative numbers are
     wrapped in `<!-- SKILL-COUNT -->…<!-- /SKILL-COUNT -->` and
     `<!-- FAMILY-COUNT -->…<!-- /FAMILY-COUNT -->` markers in the "What's in the library" intro;
     update the number inside the markers. *(validator-enforced: the marked skill-count must
     equal the real skills on disk, and the family counts must reconcile — see rule 8.)*
   - **3e. [README](README.md) → the "The roles Aegis can play" table** — add or update a row
     **only if** the skill represents a **new user-facing capability/role** not already covered.
     This is a judgment call: most skills extend an existing role and need **no** new row; a
     genuinely new capability does. Worked example — the D42 CONSTRAIN/CURATE design pack
     warranted a new row ("an AI agent operating-environment architect") because it added a design
     capability the roles table did not yet name. *(Judgment — the validator only checks that the
     section exists.)*
   - **3f. [`docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`](docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md)**
     — **only if** the skill enforces or is named under a doctrine pillar: update that pillar's
     skill references, and never leave a "(planned)" marker once the skill ships (the D41→D42
     honesty loop). *(Judgment — not validator-enforced.)*

   **The same list runs in reverse:** when renaming or retiring a skill, also grep
   `docs/paths/` and the README picker for the old name — `skill-deprecation-planner`'s
   reverse-link sweep includes `docs/paths/` as a named member.
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

README presentation-drift — a stale skill count, a renamed skill left un-updated in a table, a
family added without bumping its total — was caught **by hand** more than once during this
project's own construction. Per the discipline's own rule, *anything caught by hand twice
becomes a machine check* (Part C of the D43 decision): the validator now reconciles the README's
authoritative counts against reality — **`check_readme_counts`** (the marked `SKILL-COUNT` must
equal the skills discovered on disk) and **`check_readme_family_roster`** (the roster's per-family
counts, plus the one `project-orchestrator` front door, must sum to the real total, and the number
of family lines must equal the `FAMILY-COUNT` marker). These are hard errors; a roster that can't
be parsed at all degrades to a warning rather than blocking every PR. The map is now held to the
territory mechanically, not by memory. See the **D43** entry in
[`docs/reconciliation/step-0-reconciliation-v4.md`](docs/reconciliation/step-0-reconciliation-v4.md)
§5 for the decision.

## External contributions

Contributions are welcome from anyone. Every pull request is reviewed by the
maintainer before merge; pull requests touching a security-relevant surface
receive an additional explicit security review. Outside contributions are never
self-merged.

Those **security-relevant surfaces** are: `scripts/`, `.github/`, `AGENTS.md`,
[`docs/skill-generation-standard.md`](docs/skill-generation-standard.md) §5, and
any skill's frontmatter invocation posture (`disable-model-invocation` or the
MANUAL-ONLY sentinel), its **Security Rules**, or its **Stop Conditions**.

Before opening a PR:

- The validator and self-tests must be green — `python scripts/validate-skills.py`
  and `python scripts/tests/test_validator.py`.
- Sign off every commit under the [Developer Certificate of
  Origin](https://developercertificate.org): `git commit -s` adds the
  `Signed-off-by:` line. There is **no CLA** — Apache-2.0 §5 already governs the
  license of inbound contributions. CI enforces DCO; fix a missing sign-off with
  `git commit --amend -s` or `git rebase --signoff`.

Pull requests from forks run CI with read-only tokens by default.
