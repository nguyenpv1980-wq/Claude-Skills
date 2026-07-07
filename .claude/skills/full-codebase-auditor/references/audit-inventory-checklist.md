# Audit Inventory & Coverage Procedure

Supporting detail for `full-codebase-auditor`. Read on demand.

## Inventory census (run before ANY finding)

1. **Tree:** list top-level directories; classify each: source | tests |
   config | generated | vendored | docs | infra | assets | unknown.
   "Unknown" is a legal classification that must be resolved or listed.
2. **File census:** counts and total size by extension (`git ls-files` piped
   through a counter). Flag: files >1 MB, binaries, anything tracked that
   looks generated (lockfile-adjacent, `dist/`, `.min.`).
3. **Sub-project sweep (monorepo trap):** find every dependency manifest at
   any depth (`package.json`, `pyproject.toml`, `go.mod`, `*.csproj`,
   `Gemfile`, `Cargo.toml`) — each one is a project to inventory.
4. **Entry points:** service mains, CLI entries (`bin`, scripts sections),
   scheduled jobs (cron/workflow triggers), serverless handlers, Dockerfile
   CMD/ENTRYPOINT.
5. **Pipelines:** every file under CI directories (`.github/workflows/`,
   `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines`); note triggers and
   what each gates.
6. **History stats:** commit recency per top-level area, churn top-20 files,
   contributor concentration (areas with a single author), first/last commit
   dates.

## Coverage planning table

| Depth | Meaning | When |
| --- | --- | --- |
| Fully | Every file read | Small critical areas: auth, payments, migrations, CI |
| Sampled | Stated rule, e.g. "3 largest + 3 highest-churn + 2 random" | Broad source areas |
| Not examined | Listed with reason | Vendored, generated, assets — or budget, honestly stated |

The coverage statement in the report mirrors this table exactly. An audit is
allowed to be shallow; it is not allowed to be secretly shallow.

## Per-dimension quick evidence checklist

- **Architecture:** import cycles across top-level areas; two+ areas writing
  one table/store; "utils"/"common" areas everything depends on.
- **Security:** history secret scan (high-entropy strings, key headers, .env
  in history); authz enforced at handlers vs "TODO"; raw SQL / string-built
  queries; CORS/debug flags in prod config; dependency CVEs via lockfile scan.
- **Quality:** churn × size hotspots; duplicated blocks across areas;
  swallowed exceptions (`except: pass`, empty catch); commented-out code
  volume.
- **Tests:** which suites CI actually invokes (compare CI config against test
  dirs — orphaned suites are a CONFIRMED finding); assertion density;
  skipped/quarantined tests count and age.
- **Dependencies:** lockfile age vs manifest; majors behind latest; archived/
  unmaintained upstream repos; license census against expected policy.
- **CI/CD & deploy:** required checks vs decorative ones; deploy mechanism
  discoverable; rollback path exists; env/secret injection method.
- **Docs & ops:** README setup steps replayable (statically judged); runbook
  existence for queues/crons/backups implied by code; ADR trail.

## Tier-assignment rules

| Tier | Standard | Example |
| --- | --- | --- |
| CONFIRMED | You verified it directly this audit | "CI never runs the `integration/` suite — no workflow references it" |
| LIKELY | Strong indirect evidence; one check away | "Payment retries are probably unsafe — no idempotency key anywhere in `payments/`; confirm by reading the gateway contract" |
| HYPOTHESIS | Consistent with observations; untested | "The nightly job's runtime growth suggests a missing index; would need query plans" |
| MISSING INFO | Could not check | "No access to production config; secret-handling posture unknown" |

Demotion is mandatory when evidence is secondhand (docs claim, comment says,
name implies). Every LIKELY and HYPOTHESIS entry names the check that would
promote it — those checks seed the roadmap's "investigations" lane.
