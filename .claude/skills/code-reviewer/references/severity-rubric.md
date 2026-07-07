# Review Severity Rubric & Pass Checklists

Supporting detail for `code-reviewer`. Read on demand.

## Severity definitions

| Severity | Definition | Boundary examples |
| --- | --- | --- |
| **BLOCKER** | Merging causes incorrect behavior, data loss/corruption, a security hole, or an unrecoverable operational state on a plausible path. | Missing authz on a new endpoint; migration drops a column still read by deployed code; unhandled rejection crashes the worker loop. |
| **MAJOR** | A real defect or serious risk, but on an edge path, recoverable, or currently unreachable — will bite later if not now. | Race on concurrent update of the same row; retry without idempotency on a payment call; N+1 that's fine at 10 rows and fatal at 10k. |
| **MINOR** | Worth fixing, does not threaten correctness or safety. | Missing test for an error branch; misleading function name; duplicated constant. |
| **NIT** | Style/preference; the author may reasonably decline. | Ordering of imports; comment phrasing; `map` vs loop taste. |

Escalation rules: a MINOR in security-adjacent code escalates one level.
A pattern repeated across the diff is one finding at the pattern's severity,
listing occurrences — not N duplicate findings.

## Severity is impact, not certainty

Certainty is expressed separately: a suspected BLOCKER you couldn't verify is
written as `[BLOCKER?] needs verification: <what would confirm it>` — never
silently downgraded to MINOR because you weren't sure.

## Pass checklists (expanded)

**Correctness:** inverted/short-circuited conditions; off-by-one at loop and
pagination boundaries; null/undefined/empty/zero/NaN handling; error paths
that swallow or double-handle; float money math; timezone-naive datetimes;
mutation of shared references; async ordering assumptions; missing `await`.

**Security:** input validation at every new boundary; authz (not just authn)
on new routes/queries — object-level, not just role-level; parameterized
queries; template/HTML escaping; secrets or tokens in diffs, configs, logs,
or test fixtures; unsafe deserialization/dynamic eval; tenant scope on every
new data access; SSRF on new outbound fetches with user-influenced URLs.

**Reliability:** timeout on every new network call; retry with backoff and a
cap, idempotent or guarded; partial-failure behavior of multi-step
operations; resource cleanup on error paths (connections, files, locks);
queue/stream consumers that can't poison-loop.

**Performance:** queries inside loops; missing index for the new query shape
(check the migration!); payloads that grow with data volume; hot-path
allocations; caches without eviction or with cross-tenant keys.

**Tests:** the revert test — would the suite fail if the diff's behavior
change were undone? New error paths exercised, not just happy paths;
assertions on behavior rather than snapshots-of-everything; fixtures that
don't encode the bug being fixed.

**Migrations:** forward-only safety while old code still runs (add-then-use,
never rename-in-place); rollback statement or explicit "irreversible because";
long-running table locks on large tables; deploy-order dependency stated.

## Anti-noise rules

- Max one style/convention comment per pattern; link the convention.
- Do not restate what the diff does — findings only.
- "Consider…" without a reason is deleted; every suggestion carries its why.
- Praise is allowed and specific ("the retry guard on L84 closes the old
  double-charge window") — it teaches as much as criticism.
