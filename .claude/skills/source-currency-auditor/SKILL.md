---
name: source-currency-auditor
description: Audit the library's skills that cite external sources against a known-good source list, and flag every citation older than a stated threshold (N months) — or superseded/broken — for re-verification. The broad currency sweep: inventory external-source citations across all skills (standards editions, external docs/URLs, research, tool versions, prices/limits, dated facts), check each against a known-good list, flag stale/broken/superseded citations with the reason, and prioritize by how load-bearing and volatile the claim is. A periodic staleness gate, not an edition-specific tracker. Reports for re-verification; verifies nothing itself and changes nothing. Use when auditing citation freshness across the library, setting a currency threshold, or periodically sweeping for stale external references. Do NOT use to track specific framework EDITIONS and their deltas (framework-edition-tracker), propose mapping edits (framework-mapping-refresher), or review a skill's overall quality (skill-quality-reviewer).
---

# Source Currency Auditor

## Purpose

A skill can be perfectly written and quietly wrong because the external
world moved under it — a cited price changed, a linked doc 404s, a
research finding was superseded, a tool version is three majors behind.
None of it shows in the code; the library just slowly decays against
reality. This skill runs the broad currency sweep: it inventories every
external-source citation across the library, checks each against a
known-good source list and a staleness threshold, and flags what's stale,
broken, or superseded — for re-verification, prioritized by how
load-bearing and how volatile the claim is. It is a periodic gate on
external-truth decay, complementary to `framework-edition-tracker`'s
narrow focus on standard editions. It flags; it does not verify or fix —
because confirming currency requires checking the live source, not
trusting memory.

## Use When

- Use when: auditing whether the external sources the library cites are
  still current, across all skills.
- Use when: setting or applying a citation-staleness threshold (flag
  citations older than N months for re-verification).
- Use when: periodically sweeping for stale, broken, or superseded
  external references as a maintenance gate.
- Use when: a skill's claim depends on a volatile external fact (price,
  model id, tool version, limit) that may have drifted.
- Do NOT use when: the task is tracking specific FRAMEWORK editions and
  producing deltas — that is `framework-edition-tracker` (narrow, edition-
  specific); this is the broad age/staleness sweep.
- Do NOT use when: the task is proposing the specific mapping edits from a
  delta — that is `framework-mapping-refresher`.
- Do NOT use when: the task is reviewing a skill's overall QUALITY
  (triggers, sections, evals) — that is `skill-quality-reviewer`; this
  audits only citation currency.

## Inputs to Inspect

1. The external-source citations across skills: standards editions,
   external doc/URLs, research reports, tool/library versions, prices and
   limits, and any dated factual claim — and where each is cited.
2. The known-good source list: the current/authoritative source for each
   cited fact, where one exists, to compare against.
3. The staleness threshold(s): the age (N months) beyond which a citation
   needs re-verification — stricter for volatile facts than stable ones.
4. Volatility of each fact: how fast it goes stale (prices/model-ids/tool
   versions fast; foundational research slow) — sets the effective
   threshold.
5. Load-bearing-ness: whether the citation underpins a core claim or a
   footnote — sets priority.

## Workflow

1. **Inventory external-source citations.** Sweep the library for every
   claim resting on an external source: standard editions, URLs, research,
   versions, prices/limits, dated facts. Capture what's cited, where, and
   its stated date/version if any. An un-inventoried citation can't be
   audited.
2. **Set thresholds by volatility.** One flat "N months" is too blunt:
   prices and model ids stale in weeks, tool versions in months, and
   foundational research in years. Set an effective threshold per fact
   class, stricter where the world moves faster.
3. **Check each citation against the known-good list.** Classify: current,
   STALE (older than its threshold — needs re-verification), SUPERSEDED (a
   newer source exists), or BROKEN (dead link/removed source). Record the
   reason per flag.
4. **Prioritize by load-bearing × volatility.** A stale citation
   underpinning a core recommendation outranks a stale aside; a volatile
   fact outranks a stable one. Order the flags so re-verification effort
   goes where wrongness costs most.
5. **Flag for re-verification — verify nothing yourself.** Currency can
   only be confirmed against the live source, not asserted from memory.
   Produce the list of citations needing re-check, each with reason and
   priority; the actual re-verification (and any fix) is a separate,
   human/owner step. Route framework-edition specifics to
   `framework-edition-tracker` for the deep dive.
6. **Recommend a cadence.** This is a periodic gate — state how often to
   run it (and tighter for the volatile-fact skills), so currency stays a
   habit, not a one-off.
7. **Deliver** the currency audit in the Output Format: inventory, flags
   with reason and priority, and the cadence — changing nothing.

The citation-class thresholds, the flag taxonomy (stale/superseded/
broken), and the load-bearing × volatility priority matrix:
[references/currency-audit-sheet.md](references/currency-audit-sheet.md).

## Output Format

```
SOURCE CURRENCY AUDIT
Inventory:     <cited fact | source | where cited | stated date/version | class>
Thresholds:    per fact-class (volatile: weeks/months; stable: years)
Flags:
  <citation>: STALE (age>threshold) | SUPERSEDED (newer source) | BROKEN (dead) — reason
Priority:      load-bearing × volatility — highest first
Re-verify:     list for HUMAN/owner re-check (this skill verifies nothing);
               framework-edition specifics → framework-edition-tracker
Cadence:       recommended re-run interval (tighter for volatile-fact skills)
Changes:       NONE (audit only)
Boundaries:    editions/deltas → framework-edition-tracker; propose edits →
               framework-mapping-refresher; skill quality → skill-quality-reviewer
```

## Validation Checklist

- [ ] External-source citations are inventoried across the library (what,
      where, stated date/version).
- [ ] Thresholds are set by fact-class volatility, not one flat age.
- [ ] Each citation is classified current / stale / superseded / broken
      with a reason.
- [ ] Flags are prioritized by load-bearing × volatility.
- [ ] The output flags for re-verification; this skill verifies nothing
      and changes nothing.
- [ ] Framework-edition specifics are routed to `framework-edition-tracker`.
- [ ] A re-run cadence is recommended.
- [ ] Edition-delta, mapping-edit, and quality-review concerns are handed
      to their owning skills.

## Gotchas

- Confirming a source is current requires checking the LIVE source;
  asserting "still current" from memory is how the auditor becomes the
  stale claim. This skill flags for re-verification — it does not certify
  currency itself.
- A flat staleness threshold mis-serves both ends: it nags about
  foundational research that's fine for years and misses a price that went
  stale last week. Thresholds must track volatility.
- Broken links are the easiest currency failure to catch and the most
  embarrassing to leave — a dead source is a claim with no backing. Flag
  them first.
- Superseded is worse than merely old: a citation to a withdrawn or
  replaced source actively misinforms, where a still-valid old source just
  ages. Distinguish the two.
- Not all stale citations matter equally — prioritize by what the claim
  holds up. A stale footnote is noise; a stale core recommendation is a
  real defect.
- This is the BROAD sweep. When a flag is specifically a framework edition
  change, hand the deep dive to `framework-edition-tracker`; don't
  reproduce its delta work here.
- Auditing currency is not reviewing quality. If you're assessing
  triggers, sections, or eval integrity, that's `skill-quality-reviewer`.

## Stop Conditions

- The task is tracking specific framework editions / producing deltas →
  route to `framework-edition-tracker`.
- The task is proposing the specific mapping edits, or reviewing a skill's
  overall quality → route to `framework-mapping-refresher` or
  `skill-quality-reviewer`.
- A citation's currency cannot be confirmed without checking the live
  source → flag it for human re-verification with its reason; do NOT
  certify it current (or stale) from memory.
- A flagged citation is load-bearing and its staleness would materially
  mislead users → raise its priority and recommend prompt re-verification
  rather than leaving it in a long backlog.

## Supporting Files

- [references/currency-audit-sheet.md](references/currency-audit-sheet.md)
  — the citation-class thresholds, the flag taxonomy (stale/superseded/
  broken), and the load-bearing × volatility priority matrix.
- `evals/evals.json` — behavior cases including volatility-tuned
  thresholds, the flag-don't-verify discipline, and the broken-link catch.
- `evals/trigger-evals.json` — discrimination against `framework-edition-tracker`
  (editions vs broad staleness), `framework-mapping-refresher` (audit vs
  propose), and `skill-quality-reviewer` (currency vs quality).
