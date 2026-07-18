---
name: diataxis-doc-organizer
description: 'Organize a documentation SET using the Diátaxis framework — sort content into the four modes (tutorials for learning, how-to guides for tasks, reference for information, explanation for understanding), diagnose what each existing doc actually IS versus what it claims to be (the common rot: a "tutorial" that is really reference, a how-to bloated with explanation), place each piece in the right quadrant, structure the doc tree accordingly, and set the maintenance discipline that keeps the modes from bleeding. Owns the SHAPE and organization of the whole docs corpus. Use when documentation is disorganized, when readers can''t find what they need, when docs mix teaching with reference, or when adopting Diátaxis. Do NOT use to write the README entry point (readme-craftsman), design the docs toolchain/pipeline (docs-as-code-architect), sequence the ADR corpus (adr-sequencer), or design new-hire onboarding docs (onboarding-doc-designer).'
---

# Diátaxis Doc Organizer

## Purpose

Documentation fails not because it's missing but because it's mixed: the
"getting started tutorial" stops to dump a table of every config option,
the how-to guide detours into a philosophy of the architecture, and the
reference tries to also teach — so a learner drowns in detail and a
working developer can't find the one fact they need. Diátaxis names the
cure: four distinct modes, each serving a different reader need, kept
apart. This skill organizes a documentation SET by those modes — it
diagnoses what each existing doc actually IS versus what it pretends to
be, places every piece in the right quadrant, splits the docs that are
doing two jobs, structures the tree, and sets the discipline that keeps
modes from bleeding again. It owns the shape of the whole corpus.

## Use When

- Use when: documentation is disorganized and readers can't find what
  they need, or the same page tries to teach, instruct, and reference at
  once.
- Use when: adopting Diátaxis (or any tutorials/how-to/reference/
  explanation split) for an existing or new docs set.
- Use when: a "tutorial" is really reference, a how-to is bloated with
  explanation, or reference material is scattered through guides.
- Use when: planning the documentation tree/structure for a project.
- Do NOT use when: the task is the single README entry point — that is
  `readme-craftsman` (the README links INTO the organized set).
- Do NOT use when: the task is the docs toolchain/pipeline (generator,
  build, CI, deploy) — that is `docs-as-code-architect`; this skill
  organizes content, not the build system.
- Do NOT use when: the task is the ADR decision corpus specifically —
  that is `adr-sequencer`.
- Do NOT use when: the task is onboarding docs for a new team member —
  that is `onboarding-doc-designer` (an audience-defined set that may span
  modes).

## Inputs to Inspect

1. The existing docs: every page, its title, its claimed purpose, and its
   real content — the raw material to classify.
2. The readers and their needs: who reads the docs and in what situation
   (learning the tool for the first time vs doing a specific task vs
   looking up a fact vs wanting to understand why).
3. The mismatches: pages whose content doesn't match their heading (the
   "tutorial" full of reference tables), and pages doing two jobs at once.
4. Navigation and findability: how docs are currently structured and where
   readers get lost.
5. Generated/reference sources: API reference or other material that
   should be generated and slotted as reference (coordinate with
   `api-doc-generator-designer`).

## Workflow

1. **Classify every doc by the two axes.** Diátaxis splits on
   acquisition-vs-application (learning vs doing) and practical-vs-
   theoretical (steps vs knowledge). That yields four modes:
   - **Tutorial** — learning-oriented: a hand-held lesson with guaranteed
     success; the reader learns by doing, the author takes responsibility.
   - **How-to guide** — task-oriented: a recipe to achieve a specific goal
     for someone already competent; no teaching, no tangents.
   - **Reference** — information-oriented: accurate, complete, dry
     description of the machinery; structured for lookup, not reading.
   - **Explanation** — understanding-oriented: the why, the background,
     the tradeoffs and context; discursive, not step-by-step.
2. **Diagnose actual vs claimed.** For each doc, name what it really is.
   The most common rot is a page labeled one mode doing another's job —
   flag every mismatch.
3. **Split the two-job docs.** A tutorial carrying a reference table → the
   table becomes (or links to) reference. A how-to with a why-essay → the
   essay moves to explanation. Each resulting piece serves one need.
4. **Place and structure.** Put each piece in its quadrant and build the
   tree so all four modes are discoverable — a reader knows whether they
   want to learn, do, look up, or understand, and finds that section.
5. **Cross-link, don't embed.** A how-to LINKS to the reference it needs
   rather than inlining it; a tutorial links to explanation for the
   curious. Links keep modes pure while staying connected.
6. **Set the maintenance discipline.** New docs get classified on
   creation; the four-quadrant rule prevents re-mixing. Note where
   reference should be generated (→ `api-doc-generator-designer`) so it
   stays accurate.
7. **Deliver** the organization map — per-doc disposition (keep/split/
   move/create), the target tree, and the discipline — in the Output
   Format.

The four-modes reference (purpose, voice, what belongs, anti-patterns),
the classification decision tree, and the split patterns:
[references/diataxis-sheet.md](references/diataxis-sheet.md).

## Output Format

```
DOCS ORGANIZATION MAP — <project> (Diátaxis)
Per-doc disposition:
  <doc>: actual mode=<tutorial|how-to|reference|explanation>; claimed=<...>; action=<keep|split|move|rewrite>
Splits:        <two-job docs → the pieces they become, per mode>
Target tree:   Tutorials / How-to guides / Reference / Explanation — with contents
Cross-links:   <how-to → reference; tutorial → explanation> (link, don't embed)
Gaps:          <missing modes for key reader needs>
Generated ref: <reference that should be generated → api-doc-generator-designer>
Maintenance:   classify-on-create rule; keep modes separate
Boundaries:    README → readme-craftsman; pipeline → docs-as-code-architect;
               ADRs → adr-sequencer; onboarding set → onboarding-doc-designer
```

## Validation Checklist

- [ ] Every doc is classified by its ACTUAL mode, and mismatches with its
      claimed mode are flagged.
- [ ] Two-job docs are split so each piece serves one reader need.
- [ ] All four modes are discoverable in the tree; a reader can tell where
      to go by their need.
- [ ] How-to guides link to reference rather than embedding it; tutorials
      link to explanation.
- [ ] Reference that should be generated is marked for
      `api-doc-generator-designer` so it stays accurate.
- [ ] Gaps (a key reader need with no doc in the right mode) are named.
- [ ] A classify-on-create maintenance rule is stated to prevent
      re-mixing.
- [ ] README, pipeline, ADR, and onboarding concerns are handed to their
      owning skills.

## Gotchas

- The signature failure is the tutorial that teaches for two paragraphs
  then becomes a reference dump — it fails the learner (too much) and the
  looker-upper (too buried). Split it; don't let one page serve two needs.
- Tutorial and how-to look similar and are opposite: a tutorial teaches a
  beginner by the hand with guaranteed success; a how-to hands a
  competent person a recipe. Confusing them frustrates both audiences.
- Reference is for lookup, not reading; writing it in a chatty, teaching
  voice makes it slow to scan and hides the facts. Keep it dry and
  structured.
- Explanation is where the "why" belongs — banishing it entirely leaves
  users doing things by rote, but smuggling it into how-tos derails the
  task. Give it its own home.
- Embedding reference inside guides guarantees drift: the same fact lives
  in five places and updates in none. Link to one source (ideally
  generated).
- "We'll just have one big docs page" is how mode-mixing starts. The
  four-quadrant structure is the maintenance mechanism, not bureaucracy.

## Stop Conditions

- The task is the README entry point specifically → route to
  `readme-craftsman` (it links into the organized set).
- The task is the docs toolchain/pipeline → route to
  `docs-as-code-architect`; this skill organizes content, not the build.
- The task is the ADR corpus or the new-hire onboarding set → route to
  `adr-sequencer` or `onboarding-doc-designer`.
- Classifying a doc requires deciding what the product/feature actually
  DOES (the content is wrong, not just mis-placed) → that's a
  content/authoring question for the relevant owner, not an organization
  call; flag it rather than filing wrong content in a tidy quadrant.

## Supporting Files

- [references/diataxis-sheet.md](references/diataxis-sheet.md) — the
  four-modes reference (purpose, voice, what belongs, anti-patterns), the
  classification decision tree, and the split patterns for two-job docs.
- `evals/evals.json` — behavior cases including the tutorial-that-is-
  reference diagnosis, the split, and the corpus-structuring pass.
- `evals/trigger-evals.json` — discrimination against `readme-craftsman`,
  `docs-as-code-architect`, and `onboarding-doc-designer`.
