---
name: skill-deprecation-planner
description: Plan the safe retirement of a library skill — the lifecycle end. Establishes the trigger (superseded with a coverage diff, absorbed as an extension, evidence-backed disuse, defect), runs the reverse-link sweep (every neighbor description, trigger-eval, catalog/README row, or agent definition naming the skill gets a disposition), then stages the exit — mark (successor named), redirect for a grace window, remove (registration rows moved to a retired record, never silently deleted) — each stage with rollback (a squash-merged removal reverts as one ordinary commit). Plan only; executes nothing — removal is a human-approved operation. Use when asked to deprecate, retire, remove, or sunset a skill, prune the library on evidence, or after a reject/make-it-an-extension verdict. Do NOT use for doc lifecycle/retirement (docs-retention-index — now shipped), product-feature sunset messaging, usage-evidence gathering (skill-usage-instrumenter), or reviewing the removal PR (library-diff-reviewer).
---

# Skill Deprecation Planner

## Purpose

Let the library shrink as deliberately as it grows. Skills are added under a
standard, registered in a catalog, and named by their neighbors' yield
clauses and trigger-evals — which means an unplanned deletion breaks more
than a directory: it leaves dangling "that is X" redirects pointing at
nothing, trigger-evals expecting a skill that no longer exists, and count
arithmetic that silently lies. This skill produces the staged retirement
plan — trigger established, every inbound reference dispositioned, the
mark → redirect → remove path with a rollback per stage — so retiring a
skill is as governed as shipping one. It plans; it never deletes.

## Use When

- Use when: asked to deprecate, retire, remove, sunset, or "clean up" a
  skill — for any stated reason.
- Use when: a skill has been superseded by a newer one and the library
  should route requests to the successor.
- Use when: a `skill-quality-reviewer` verdict was reject or
  make-it-an-extension, and the absorbed/rejected skill needs a governed
  exit.
- Use when: usage evidence (a `skill-usage-instrumenter` evidence package)
  shows sustained zero fires for a non-exempt skill and the owner wants a
  retirement plan.
- Do NOT use when: the retiring artifact is a DOC — retention categories,
  superseded-by chains, and cleanup rules for workflow documents belong to
  `docs-retention-index` (now shipped; it owns doc lifecycle end-to-end —
  this skill must not absorb it).
- Do NOT use when: the sunset is a product FEATURE and the work is customer
  communication and migration messaging — that is a product/PM concern
  (`sunset-deprecation-communicator`, now shipped), not library mechanics.
- Do NOT use when: the question is whether anything still USES the skill —
  that evidence design is `skill-usage-instrumenter`; this skill consumes
  its package.
- Do NOT use when: reviewing the PR that executes a retirement — that is
  `library-diff-reviewer` (it checks the executed diff against this plan).
- Do NOT use when: the "retirement" is really a rename or a scope change —
  that is an ordinary skill modification with its own review, not a
  lifecycle exit.

## Inputs to Inspect

1. The target skill's full directory: frontmatter (its description is what
   currently attracts requests), all sections, `references/*`, and its
   evals — what the library loses if this leaves.
2. The reverse-link surface: every place the skill's name appears outside
   its own directory — other skills' `SKILL.md` yield clauses, every
   `trigger-evals.json` (`expected_skill`, `should_not_trigger`,
   `overlaps_with`), the catalog, the README, agent definitions, CI/config
   references. (Purpose: a full-text search for the skill name across the
   repo; every hit becomes a row in the disposition table.)
3. The deprecation trigger's evidence: the successor skill (for
   supersession), the quality-review verdict (for absorption/rejection),
   the usage evidence package (for disuse), or the defect record.
4. The library's registration conventions: how the catalog and decision log
   record status changes, and where a retired record belongs.
5. The decision log itself — retirement lands as a NEW dated entry; older
   entries stating old counts stay untouched (they were true when written).

## Workflow

1. **Establish the trigger — or stop.** Exactly one of:
   - *Superseded:* name the successor AND write the coverage diff — what
     the successor covers, and what dies with the retiree. Residue is
     declared intentionally-dropped (with owner sign-off) or blocks the
     retirement; it never disappears silently.
   - *Absorbed:* a make-it-an-extension verdict; name the base skill and
     the extension diff that carries the surviving content.
   - *Disuse:* a usage evidence package (tier and window stated) for a
     non-exempt skill — anecdote and "seems old" do not qualify.
   - *Defect:* the skill is wrong/harmful as written; note whether a fix
     was considered and why retirement wins.
   No qualifying trigger → no plan; say so.
2. **Run the reverse-link sweep.** Enumerate every inbound reference and
   assign each a disposition: *repoint* (to the successor), *rewrite* (the
   neighbor's yield clause or trigger-eval case no longer needs the seam),
   or *annotate historical* (decision-log and provenance text stays as
   written). An inbound reference with no disposition blocks the plan.
3. **Stage 1 — mark.** The skill stays present and functional; its
   description gains a deprecation notice naming the successor and yielding
   its triggers ("DEPRECATED — superseded by <successor>; new requests go
   there"); catalog/README rows annotated; a dated decision-log entry
   records the decision and the planned window.
4. **Stage 2 — redirect window.** A stated grace period in which the
   deprecated skill redirects rather than serves. Monitor for stragglers:
   anything still firing or referencing it (instrumented signal if
   available, else the tier-2 path). New references to a deprecated skill
   are review findings from this point.
5. **Stage 3 — remove.** Directory deleted; registration rows MOVE to a
   retired record (catalog retired section + decision-log entry) rather
   than vanishing; count arithmetic decremented at every site a count
   appears; trigger-evals of neighbors updated per the disposition table;
   the removal PR reviewed by `library-diff-reviewer` against this plan.
6. **Design the rollback per stage.** Stage 1/2: revert the marking
   commit(s). Stage 3: on a squash-merge platform the removal PR merged as
   ONE ordinary commit — rollback is `git revert <squash-sha>`, restoring
   the directory and its registration rows in one step. State where the
   point of no return actually is (external consumers who copied the skill
   are outside this plan's reach — say so).
7. **Deliver the plan** in the Output Format: trigger + evidence,
   disposition table, per-stage checklists with dates/windows, rollback per
   stage, and the explicit statement that execution — every stage of it —
   is a human-approved operation this skill does not perform.

Stage checklists, the disposition-table format, the reverse-link sweep
procedure, and retired-record conventions:
[references/deprecation-stage-playbook.md](references/deprecation-stage-playbook.md).

## Output Format

```
SKILL DEPRECATION PLAN — <skill-name>
Trigger:      superseded (successor: <name>) | absorbed (base: <name>) | disuse (evidence: tier/window) | defect
Coverage diff: <what the successor covers | what is intentionally dropped (owner-acknowledged) | "n/a">
Reverse links: <N inbound references → disposition table: repoint | rewrite | annotate-historical>
Stage 1 MARK:      <description notice + successor; registration annotations; decision-log entry> — rollback: <revert marking commit>
Stage 2 REDIRECT:  <grace window + dates; straggler monitoring source> — rollback: <un-mark; window closes>
Stage 3 REMOVE:    <directory deletion; rows moved to retired record; count sites decremented; neighbor evals updated; removal PR → library-diff-reviewer> — rollback: <git revert of the single (squash) removal commit>
Point of no return: <external copies/consumers outside plan reach — stated honestly>
Execution:    NOT performed by this plan — each stage is a human-approved operation
Not planned:  <what this plan deliberately leaves out, and why>
```

## Validation Checklist

- [ ] Exactly one qualifying trigger is established with its evidence; no
      plan rests on "seems unused" or "feels old".
- [ ] For supersession: the coverage diff exists and every residue item is
      either carried, or intentionally dropped with owner acknowledgment —
      none silent.
- [ ] The reverse-link sweep enumerated ALL inbound references (skills,
      trigger-evals, catalog, README, agents, config) and every row has a
      disposition.
- [ ] All three stages have checklists, dates/windows, and a rollback; the
      squash-revert mechanic is stated for the removal stage.
- [ ] Registration rows move to a retired record — nothing is deleted from
      the catalog/decision log without a destination.
- [ ] Historical decision-log entries are untouched; retirement is a NEW
      dated entry.
- [ ] The plan states it executes nothing and names the human approval each
      stage requires.

## Gotchas

- Dangling yield clauses: neighbors saying "that is X" for a removed X
  send requests into a void — the single most common breakage. The
  disposition table exists because of it.
- Trigger-evals rot: a removed skill lingering in `expected_skill` or
  `should_not_trigger` lists makes the eval corpus assert the impossible.
  Neighbor evals are part of the removal diff, not a follow-up.
- Partial supersession sold as full: the successor covers 80% and the
  other 20% dies silently. The coverage diff is the defense — residue is
  carried, or dropped OUT LOUD, never elided.
- Deprecation-by-neglect: a skill marked deprecated with no removal date
  becomes permanent clutter with a warning label. Stage 2 has an end date
  or stage 1 shouldn't start.
- Count-site misses: removal decrements the skill count in fewer places
  than it appears (catalog status, README narrative, tables). Reuse the
  same site list additions use — arithmetic drift reads as sloppiness and
  breeds distrust of the record.
- Editing history to match the present: "fixing" old decision-log entries
  that state the old count rewrites the record. Entries are append-only;
  the new entry explains the new total.
- Retiring the seam instead of the skill: when a retiring skill is one
  side of a pinned discrimination seam, the surviving side's trigger-evals
  and description must be rewritten to absorb or re-route the seam — not
  left referencing a ghost.
- Rare-but-critical skills condemned by usage: low fire counts on
  incident/recovery/refusal skills are success, not disuse. The evidence
  package's exemption check is a blocking input, not advice.

## Stop Conditions

- Asked to delete the skill NOW, plan later ("just remove the directory,
  we'll tidy references after") → refuse; unstaged deletion is exactly the
  dangling-reference incident this skill exists to prevent. The plan comes
  first; execution is human-approved.
- No qualifying trigger — the reason offered is taste, age, or an
  unevidenced hunch → stop and route: usage questions to
  `skill-usage-instrumenter`, quality questions to
  `skill-quality-reviewer`, or get an explicit owner decision recorded as
  the trigger.
- Asked to edit historical decision-log entries to reflect the removal →
  refuse; the log is append-only. New entry, old entries untouched.
- The supersession coverage diff leaves residue nobody will own → halt the
  plan at stage 0 and surface the residue; a retirement that silently
  drops covered ground is a scope decision for a human, not a planner
  default.
- An inbound reference cannot be dispositioned (a neighbor's whole
  workflow depends on the retiring skill) → stop; that is not a
  deprecation problem but a design problem — hand it to
  `skill-quality-reviewer` / the library owners before any staging.
- Asked to also plan a DOC's retirement in the same pass → decline that
  slice; doc lifecycle is `docs-retention-index` scope (now shipped) —
  hand it off.

## Supporting Files

- [references/deprecation-stage-playbook.md](references/deprecation-stage-playbook.md)
  — per-stage checklists, the disposition-table format, the reverse-link
  sweep procedure, retired-record conventions, and rollback mechanics
  including the squash-revert note.
- `evals/evals.json` — behavior cases including the rare-but-critical
  pushback edge and the delete-now refusal.
- `evals/trigger-evals.json` — discrimination against `docs-retention-index`
  (the doc-lifecycle seam), `skill-usage-instrumenter`,
  `library-diff-reviewer`, and `skill-quality-reviewer`.
