# Coverage Mapping Method

Detail file for `test-coverage-mapper`. Loaded on demand.

## Surface inventory recipe

Enumerate before judging. Typical sources:

| Surface kind | Where to find it |
| --- | --- |
| Routes/pages | router config, pages/app directory |
| API endpoints | route handlers, OpenAPI spec, controller files |
| Commands/services | command handlers, service classes, use-case modules |
| Schema | migrations, table definitions (RLS-bearing tables flagged) |
| Background jobs | queue/cron definitions |
| Integrations | webhook handlers, provider clients |

Record each with an id so the map is diffable across audits.

## Verifying vs theater rubric

A test VERIFIES a surface when it asserts observable behavior a user or
consumer depends on. Theater signals:

- No assertion, or assertions that cannot fail (`expect(result).toBeDefined()`
  on a constructor result).
- Render-only component tests (mounts, asserts nothing about behavior).
- Snapshot-everything tests nobody reviews on update.
- Asserting against the mock itself (mock called with X, where X is the only
  thing the test set up — circular).
- Integration tests where every boundary is mocked: reclassify to unit at
  best; the boundary is NOT covered.

When in doubt, ask: "what real bug would make this test fail?" No answer →
theater.

## Gap-ranking worksheet

For each uncovered/theater surface:

1. Impact if broken: data loss / money / security / journey blocked / cosmetic.
2. Likelihood: change frequency (git churn), complexity, incident history.
3. Detection without a test: would anything else catch it before users?

Rank = impact-first, likelihood as tiebreaker, low-detectability promotes.
Security-relevant gaps (tenant/authz) are always reported, with specification
delegated to `multi-tenant-security-tester`.

## Coverage statement discipline

Report four buckets with counts: covered / theater / uncovered /
not-inspected. "Not-inspected" is honest scope-cutting; omitting it converts
a partial audit into a false whole-scope claim.
