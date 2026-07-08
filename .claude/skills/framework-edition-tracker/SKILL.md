---
name: framework-edition-tracker
description: Track the editions of external standards the library's framework-mapping skills cite — OWASP Top 10 / LLM / Agentic, ISO 27001/42001, SOC 2, NIST AI RMF and similar — by maintaining an edition register (framework → cited edition → where cited), detecting when a NEW edition ships, and producing a DELTA report of what changed. Pins currency without touching any mapping: it reports drift, it does not update. The delta it produces feeds framework-mapping-refresher, which proposes the specific edits for human review. Use when checking whether cited standard editions are current, setting up edition tracking, or when a new edition of a cited framework drops. Do NOT use to PROPOSE the specific mapping updates from a delta (framework-mapping-refresher), audit citation AGE/staleness broadly (source-currency-auditor), or own the framework mapping content itself (the compliance/OWASP mapping skills, e.g. multi-framework-crosswalk).
---

# Framework Edition Tracker

## Purpose

Every framework mapping the library ships — the OWASP Top 10 maps, the
ISO and SOC 2 compliance projections, the NIST AI RMF companion — is a
point-in-time snapshot of an external standard that revises on its own
cadence. When a new edition drops and nobody notices, the library quietly
cites a superseded standard and its currency claim becomes false without a
single line of code changing. This skill closes that gap: it maintains an
edition register (which framework, which edition, cited where), watches
for new editions, and when one ships produces a DELTA report of what
changed — so drift with external truth is DETECTED instead of silent. It
deliberately does nothing else: it pins and reports currency; it does not
propose or apply mapping changes. The delta feeds
`framework-mapping-refresher`.

## Use When

- Use when: checking whether the standard editions the library cites are
  still current.
- Use when: setting up edition tracking for the framework-mapping skills.
- Use when: a new edition of a cited framework (OWASP, ISO, SOC 2, NIST)
  ships and you need the delta against what the library cites.
- Use when: an audit or currency review asks "are we citing the latest
  editions?".
- Do NOT use when: the task is proposing the SPECIFIC updates to skills/
  references from a known delta — that is `framework-mapping-refresher`
  (the next step); this only detects and reports.
- Do NOT use when: the task is auditing citation AGE/staleness across
  external sources broadly (not edition-specific) — that is
  `source-currency-auditor`.
- Do NOT use when: the task is authoring/owning the framework mapping
  content itself — that is the compliance/OWASP mapping skills (e.g.
  `multi-framework-crosswalk`, `iso-27001-isms-architect`); this tracks
  their currency, it doesn't write them.

## Inputs to Inspect

1. The framework citations across the library: which external standards
   are cited (OWASP Top 10:2025, ISO 27001:2022, ISO 42001:2023, SOC 2,
   OWASP LLM/Agentic Top 10, NIST AI RMF, …) and in which skills/
   references.
2. The edition each skill cites: the specific version/year, captured
   verbatim from the skill's own text.
3. The current published edition of each framework: what the standards
   body has actually released (a verification item, not a memory claim).
4. The existing edition register if any: prior tracking to update rather
   than re-derive.
5. Known volatility: which frameworks revise often (OWASP ~every few
   years) vs rarely, to set watch priority.

## Workflow

1. **Build the edition register.** For each cited framework: the
   framework, the edition the library currently cites, and every site
   (skill/reference) that cites it. This register is the source of truth
   for what currency the library claims.
2. **Establish the current published edition — by verification.** For each
   framework, determine the latest edition the standards body has actually
   released. Treat this as something to VERIFY against the source, never
   assert from memory — edition numbers and dates are exactly the facts
   that go stale. Where verification isn't possible now, mark it
   "unverified — confirm against source" rather than guessing.
3. **Detect drift.** Compare cited edition vs current published edition per
   framework. Flag each as current, superseded (new edition exists), or
   unverified.
4. **Produce the delta report — for superseded frameworks.** Summarize what
   changed between the cited edition and the new one (added/removed/renamed
   items, restructured categories) at a level that lets a human judge
   impact — without proposing the specific skill edits (that's the next
   skill).
5. **Rank by impact and volatility.** Which superseded editions touch the
   most skills or the most load-bearing claims, and which frameworks are
   due to revise soon — so the refresh effort goes where it matters.
6. **Hand off, do not update.** The delta report goes to
   `framework-mapping-refresher` to propose the concrete edits, which land
   only after human review. This skill's output is a detection artifact,
   not a change.
7. **Deliver** the register + drift status + delta report in the Output
   Format, with unverified items clearly marked.

The edition-register format, the delta-report structure, and the
verify-don't-assert discipline for edition facts:
[references/edition-tracking-sheet.md](references/edition-tracking-sheet.md).

## Output Format

```
FRAMEWORK EDITION TRACKING
Register:
  <framework | cited edition | cited in (skills/refs)>
Current published (VERIFIED against source | UNVERIFIED — confirm):
  <framework | latest edition | source>
Drift status:  <framework: current | SUPERSEDED (cited X → new Y) | unverified>
Delta report (superseded only): <what changed cited→new, impact-level, no specific edits>
Priority:      <by #skills touched × load-bearing × revision cadence>
Handoff:       delta → framework-mapping-refresher (proposes edits; human review before landing)
Boundaries:    broad staleness → source-currency-auditor; mapping content → the mapping skills
```

## Validation Checklist

- [ ] An edition register lists each cited framework, its cited edition,
      and every citing site.
- [ ] Current published editions are marked VERIFIED against source or
      explicitly UNVERIFIED — never asserted from memory.
- [ ] Drift status (current / superseded / unverified) is set per
      framework.
- [ ] A delta report summarizes what changed for superseded frameworks,
      at an impact level — without proposing specific skill edits.
- [ ] Priority reflects skills-touched × load-bearing × revision cadence.
- [ ] The delta is handed to `framework-mapping-refresher`; no mapping is
      updated here.
- [ ] Mapping authorship and broad source-staleness are handed to their
      owning skills.

## Gotchas

- Edition numbers and release dates are the single most stale-prone facts
  in the whole library — asserting "the latest OWASP Top 10 is 20XX" from
  memory is how the tracker itself goes wrong. Verify against the source;
  mark unverified when you can't.
- Silent edition drift is the failure this skill exists to catch: nothing
  in the code changes, but the library now cites a superseded standard and
  its currency claim is quietly false. Detection is the whole value.
- This skill DETECTS; it does not fix. Producing the delta and then
  editing the mappings blurs into `framework-mapping-refresher` and skips
  the human-review gate that keeps standard citations trustworthy.
- A delta report that dives into specific skill edits has overstepped —
  keep it at "what changed in the standard", and let the refresher map
  that to concrete changes for review.
- Tracking only the frameworks you remember misses the ones cited deep in
  references. Sweep all citing sites, not just the obvious skills.
- Not all editions matter equally: a minor revision touching one skill's
  footnote is not a major restructure touching every compliance skill.
  Rank by impact so effort follows risk.

## Stop Conditions

- The task is proposing the specific skill/reference edits from a delta →
  route to `framework-mapping-refresher`.
- The task is a broad citation-age/staleness audit across sources → route
  to `source-currency-auditor`.
- The task is writing/owning the framework mapping content → route to the
  relevant mapping skill (`multi-framework-crosswalk`, the ISO/SOC 2
  skills).
- The current published edition of a framework cannot be verified against
  the source right now → mark it UNVERIFIED and flag for confirmation; do
  not assert an edition number from memory and do not trigger a refresh on
  an unverified delta.

## Supporting Files

- [references/edition-tracking-sheet.md](references/edition-tracking-sheet.md)
  — the edition-register format, the delta-report structure, and the
  verify-don't-assert discipline for edition facts.
- `evals/evals.json` — behavior cases including drift detection, the
  verify-don't-assert refusal, and the detect-not-fix boundary.
- `evals/trigger-evals.json` — discrimination against `framework-mapping-refresher`
  (detect vs propose), `source-currency-auditor` (editions vs staleness),
  and `multi-framework-crosswalk` (currency vs mapping content).
