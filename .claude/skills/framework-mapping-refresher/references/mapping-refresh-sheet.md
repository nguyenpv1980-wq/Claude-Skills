# Mapping Refresh Sheet

Detail for `framework-mapping-refresher`. Read on demand.

## Precondition

Start from a VERIFIED delta (from `framework-edition-tracker`). Unverified
or suspected → route back. Refreshing on a bad delta multiplies the error.

## Site-sweep checklist (find every affected site)

- [ ] Skill `description` frontmatter citing the edition.
- [ ] SKILL.md body references to the edition/categories.
- [ ] `references/` files with mappings/coverage tables.
- [ ] Coverage maps / crosswalk tables.
- [ ] The literal edition string (year/version) everywhere.

Missing one site = half-migrated, internally contradictory library.

## Change-type → edit patterns

| Delta change | Proposed edit | Watch |
|---|---|---|
| Renamed category | Update label at each site | Scope may have shifted — flag |
| Added control/category | Map to covering skill OR surface GAP | Don't invent coverage |
| Removed control | Remove mapping; note in coverage map | Don't leave dangling refs |
| Merged controls | Combine mappings | Meaning change — flag |
| Split control | Divide mapping across new items | Meaning change — flag |
| Restructured | Re-map relationships | Human call likely |
| Edition string | Old year/version → new | Everywhere |

## Meaning-preservation rule

A rename/merge/split is rarely just a label. Propose edits that preserve
MEANING, and FLAG any item where the scope shift makes the correct new
mapping a judgment call. Never blind find-replace a scope change.

## Gap-surfacing rule

New-edition category with no covering skill = a GAP finding. Options for
the human:
- Add a new skill.
- Record it as explicitly not-covered.
NEVER invent a mapping to make coverage look complete — that's the
dishonesty this trio prevents.

## Output is a PROPOSAL

This skill proposes; it does not apply. Edits land only via a normal PR
approved by a human / `library-diff-reviewer`. Keep voice/structure of
each skill intact — targeted refresh, not re-author.
