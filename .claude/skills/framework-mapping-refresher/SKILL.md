---
name: framework-mapping-refresher
description: Given an edition delta (from framework-edition-tracker), propose the SPECIFIC updates to every affected skill description, reference file, and coverage map — locate each site that cites or maps the old edition, propose the concrete change per site (renamed category, added/removed control, restructured mapping, updated edition string), surface any new coverage GAP the edition introduces, and flag the whole set for HUMAN REVIEW before anything lands. Proposes; never auto-applies. Downstream of framework-edition-tracker (which detects the delta) and upstream of the human / library-diff-reviewer who approves the resulting PR. Use when a known, verified edition delta must become concrete proposed mapping updates. Do NOT use to DETECT the delta or track editions (framework-edition-tracker), audit citation age broadly (source-currency-auditor), author a mapping from scratch (the compliance/OWASP mapping skills), or review the resulting PR (library-diff-reviewer).
---

# Framework Mapping Refresher

## Purpose

When `framework-edition-tracker` reports that a cited standard has a new
edition, someone has to turn "the OWASP categories were renamed and
restructured" into the exact set of edits across every skill and reference
that cited the old edition — carefully, because a renamed category often
changed scope, a merged control changed the mapping, and a new category
may have opened a coverage gap. This skill does that: it locates every
affected site, proposes the concrete change per site, surfaces any new gap
the edition introduces, and packages the whole set for human review. It
proposes; it never applies. It sits between the tracker that DETECTS the
delta and the human / `library-diff-reviewer` who APPROVES the resulting
PR — the two gates that keep the library's standard citations trustworthy.

## Use When

- Use when: a known, verified edition delta (from
  `framework-edition-tracker`) must become concrete proposed edits across
  the affected skills/references/coverage maps.
- Use when: refreshing skill descriptions, reference files, or coverage
  maps to a new edition of a cited standard.
- Use when: an edition change may have opened a coverage gap that needs
  surfacing before the mapping is updated.
- Do NOT use when: the task is DETECTING drift or tracking which editions
  are cited — that is `framework-edition-tracker` (upstream); this
  consumes its delta.
- Do NOT use when: the task is a broad citation-age/staleness audit — that
  is `source-currency-auditor`.
- Do NOT use when: the task is authoring a framework mapping from scratch —
  that is the compliance/OWASP mapping skills (`multi-framework-crosswalk`,
  the ISO/SOC 2 skills); this refreshes existing mappings.
- Do NOT use when: the task is reviewing the resulting PR — that is
  `library-diff-reviewer`; this proposes the edits it will review.

## Inputs to Inspect

1. The edition delta: what changed between the cited and new editions
   (added/removed/renamed/merged/split/restructured), verified — from
   `framework-edition-tracker`.
2. Every affected site: the skill descriptions, reference files, and
   coverage maps that cite or map the old edition (a reverse-reference
   sweep for that framework).
3. The current mapping content at each site: exactly how the old edition
   is cited/mapped, so the proposed change is precise.
4. The scope of each changed item: whether a rename is cosmetic or a scope
   change, and whether a merge/split alters what maps to what — meaning,
   not just labels.
5. The coverage picture: which controls/categories the library claims to
   cover, so a newly-added category's gap is visible.

## Workflow

1. **Require a verified delta.** Start from a real, verified delta. If the
   edition change is only suspected or unverified, route back to
   `framework-edition-tracker`; proposing edits on an unconfirmed delta
   spreads an error across many files.
2. **Locate every affected site.** Sweep for each place the old edition is
   cited or mapped — skill descriptions, references, coverage maps, and
   the edition string itself. A refresh that misses a site leaves the
   library half-migrated and internally contradictory.
3. **Propose the concrete change per site.** For each changed item in the
   delta, the specific edit at each site: the renamed category, the
   added/removed control, the re-mapped relationship, the updated edition
   string. Preserve each skill's voice and structure — this is a targeted
   refresh, not a rewrite.
4. **Judge meaning, don't string-swap.** A renamed category may have
   changed scope; a merged control changes the mapping, not just the
   label; a split control needs the mapping divided. Propose edits that
   preserve MEANING, flagging any item where the scope change needs a human
   call.
5. **Surface new coverage gaps.** If the new edition adds a category the
   library doesn't cover, that's a GAP — surface it as a finding, not a
   silently-invented mapping. Do not fabricate coverage to make the map
   look complete.
6. **Package for human review — never apply.** Assemble the proposed edits
   per site plus the gap findings, and flag the set for human review. The
   change lands only via a normal PR approved by a human /
   `library-diff-reviewer`. This gate is non-negotiable for standard
   citations.
7. **Deliver** the proposal in the Output Format: per-site proposed edits,
   scope-change flags, new-gap findings, and the review flag.

The site-sweep checklist, the change-type → edit patterns, and the
meaning-preservation / gap-surfacing rules:
[references/mapping-refresh-sheet.md](references/mapping-refresh-sheet.md).

## Output Format

```
FRAMEWORK MAPPING REFRESH (PROPOSAL — not applied) — <framework: X → Y>
Delta source:  framework-edition-tracker (verified)
Affected sites: <every skill/reference/coverage-map citing the old edition>
Proposed edits (per site):
  <site>: <old text/mapping> → <proposed new> ; scope-change? <flag if meaning shifted>
New coverage gaps: <new-edition categories with no covering skill — findings, not invented mappings>
Edition strings:   <old → new, everywhere>
Review:        flagged for HUMAN review / library-diff-reviewer — NOT applied here
Boundaries:    detect delta → framework-edition-tracker; broad staleness →
               source-currency-auditor; author mapping → the mapping skills; review PR →
               library-diff-reviewer
```

## Validation Checklist

- [ ] The refresh starts from a verified delta; unverified deltas route
      back to `framework-edition-tracker`.
- [ ] Every affected site (descriptions, references, coverage maps,
      edition strings) is located — no half-migration.
- [ ] Each changed item has a concrete proposed edit per site, preserving
      the skill's voice.
- [ ] Scope changes (renamed/merged/split with altered meaning) are
      flagged for a human call, not blind string-swapped.
- [ ] New coverage gaps from the edition are surfaced as findings, not
      papered over with invented mappings.
- [ ] The proposal is flagged for human review and is NOT applied by this
      skill.
- [ ] Detection, broad staleness, authorship, and PR review are handed to
      their owning skills.

## Gotchas

- A renamed category is rarely just a label change — the scope often
  shifted, and a blind find-replace produces a mapping that's syntactically
  updated and semantically wrong. Judge the meaning; flag the scope shift.
- Missing one citing site leaves the library half-migrated: some skills say
  the new edition, some the old, and the internal contradiction is worse
  than being uniformly out of date. Sweep exhaustively.
- A new category the library doesn't cover is a GAP, not something to
  paper over. Inventing a mapping to make coverage look complete is the
  exact dishonesty these skills exist to prevent — surface it.
- Refreshing on an unverified delta multiplies a single wrong edition
  claim across many files. The verified delta from the tracker is the
  precondition.
- This skill PROPOSES; applying edits directly skips the human-review gate
  that keeps compliance/standard citations trustworthy. The output is a
  proposal, always.
- A "refresh" that rewrites the whole skill has overstepped — it's a
  targeted edition update, preserving voice and structure, not a re-author.

## Stop Conditions

- The delta is unverified or the task is really detecting drift → route to
  `framework-edition-tracker`.
- The task is a broad citation-age audit → route to
  `source-currency-auditor`.
- The task is authoring a mapping from scratch, or reviewing the resulting
  PR → route to the mapping skills or `library-diff-reviewer`.
- A changed item's scope shift is ambiguous enough that the correct new
  mapping is a judgment call → surface it for a human decision rather than
  proposing a mapping that might misrepresent coverage.

## Supporting Files

- [references/mapping-refresh-sheet.md](references/mapping-refresh-sheet.md)
  — the site-sweep checklist, the change-type → edit patterns, and the
  meaning-preservation / gap-surfacing rules.
- `evals/evals.json` — behavior cases including the exhaustive site sweep,
  the meaning-not-label discipline, and the new-gap surfacing.
- `evals/trigger-evals.json` — discrimination against `framework-edition-tracker`
  (detect vs propose), `source-currency-auditor` (broad staleness), and
  `library-diff-reviewer` (propose vs review).
