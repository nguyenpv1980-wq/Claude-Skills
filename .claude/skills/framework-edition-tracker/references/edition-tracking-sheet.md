# Edition Tracking Sheet

Detail for `framework-edition-tracker`. Read on demand.

## Edition-register format

```
| Framework | Cited edition | Cited in (skills/refs) | Drift |
|-----------|---------------|------------------------|-------|
| OWASP Top 10 | <edition as cited> | phase-4 skills, ... | ? |
| ISO 27001 | <edition as cited> | iso-27001-isms-architect | ? |
| ISO 42001 | <edition as cited> | iso-42001-aims-architect | ? |
| SOC 2 | <criteria set as cited> | soc2-trust-criteria-mapper | ? |
| OWASP LLM Top 10 | <edition as cited> | phase-7 skills | ? |
| OWASP Agentic Top 10 | <edition as cited> | phase-7.5 skills | ? |
| NIST AI RMF | <version as cited> | compliance companion | ? |
```

Capture the cited edition VERBATIM from each skill's own text — that's
what the library claims, right or wrong.

## Verify-don't-assert discipline

Edition numbers and dates are the most stale-prone facts here. For each
framework's CURRENT published edition:
- VERIFY against the standards body's source.
- If not verifiable now → mark **UNVERIFIED — confirm against source**.
- NEVER assert "the latest edition is X" from memory.
- Do NOT trigger a refresh on an unverified delta.

## Drift status

| Status | Meaning |
|---|---|
| current | Cited edition == latest published |
| SUPERSEDED | A newer edition exists (cited X → new Y) |
| unverified | Latest edition not confirmed against source |

## Delta-report structure (superseded only)

```
Framework: <name>  Cited: <X>  New: <Y>
What changed (impact level, NOT specific skill edits):
  - Added: <new categories/controls>
  - Removed: <dropped>
  - Renamed/merged/split: <...>
  - Restructured: <...>
Impact: <# skills touched × how load-bearing>
→ framework-mapping-refresher (proposes edits; human review before landing)
```

Keep the delta at "what changed in the STANDARD". Mapping it to concrete
skill edits is the refresher's job.

## Priority

Rank refresh effort by: (# skills touched) × (load-bearing-ness of the
claim) × (framework revision cadence). A footnote revision in one skill is
not a category restructure across every compliance skill.
