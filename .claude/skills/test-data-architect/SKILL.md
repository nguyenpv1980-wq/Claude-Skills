---
name: test-data-architect
description: Design the test-data strategy across all test layers — deterministic seed/fixture/factory design (personas, tenants, roles, stable ids), per-layer data sources (inline builders for unit, seeded DB for integration, API-created fixtures for E2E), parallel-run isolation (worker-scoped namespacing, no shared mutable records), PII-safe synthetic data (never production copies without an approved anonymization path), cleanup/TTL and traceability rules, and seed evolution coupled to schema changes. Use when asked to design fixtures/seeds/factories, fix tests fighting over shared data, decide how E2E/integration suites get their data, replace production-data copies in tests, or make test data deterministic and parallel-safe. Produces the design; suite wiring goes to the engineer skills. Do NOT use to design the tenant data model itself (multi-tenant-data-architect), build cross-tenant SECURITY test suites (multi-tenant-security-tester), or design automation structure (qa-automation-architect).
---

# Test Data Architect

## Purpose

Design the data foundation every test layer stands on: deterministic,
parallel-safe, PII-free, and owned. The output is a data design — persona and
tenant catalog, factory/seed architecture per layer, isolation and cleanup
rules, and an evolution policy tied to schema changes — that engineer skills
wire into their suites. Bad test data is the quiet cause of half of "flaky"
suites and most cross-contaminated runs; this skill removes that class of
failure by design.

## Use When

- Use when: asked to design fixtures, factories, seeds, or test personas.
- Use when: tests fight over shared records, break in parallel, or depend on
  run order for data reasons.
- Use when: deciding how integration/E2E suites obtain data (seed scripts,
  API-created, snapshot).
- Use when: production data (or lightly-scrubbed copies) is being used in
  tests and must be replaced with synthetic data.
- Use when: seeds have rotted — schema moved, fixtures didn't, tests assert
  against fossil data.
- Do NOT use when: designing the PRODUCT's tenant-scoped data layer —
  `multi-tenant-data-architect`; this skill designs TEST data shaped like
  that design.
- Do NOT use when: specifying cross-tenant/authorization negative TESTS —
  `multi-tenant-security-tester` (its two-tenant A/B fixture recipe is
  authoritative for those suites; this skill keeps general fixtures
  compatible with it, not competing).
- Do NOT use when: structuring the automation framework/CI —
  `qa-automation-architect` (it decides where fixtures LIVE; this skill
  decides what they ARE).

## Inputs to Inspect

1. The domain shape: entities, tenancy model, roles/personas that matter
   (tenant model + authorization matrix outputs where present).
2. Current test data reality: existing seeds/factories/fixtures, hardcoded
   ids, shared accounts, `.only`-style data workarounds, order dependence.
3. Layer needs: which suites exist/are planned (unit, integration, E2E,
   manual) and how each currently gets data.
4. Parallelism: worker counts per suite, CI vs local differences.
5. Data sensitivity: any production data in tests today, PII classes
   involved, retention/redaction obligations.

## Workflow

1. **Catalog personas and baseline entities.** Named personas (e.g., owner/
   admin/member per tenant, anonymous) with stable identifiers and
   documented properties; a minimal baseline world (tenants, one resource
   per interesting state) that suites can assume. Keep the catalog small —
   every baseline row is maintenance forever. Patterns in
   [references/test-data-patterns.md](references/test-data-patterns.md).
2. **Assign data sources per layer:** unit → in-memory builders (no DB);
   integration → factories writing through real migrations/constraints
   (per `integration-test-designer` boundaries); E2E → API-created
   per-run fixtures (per `playwright-e2e-engineer` determinism rules);
   manual → seeded accounts documented for `manual-test-case-creator`
   preconditions. One factory definition feeding all layers where feasible
   (single source of shape truth).
3. **Design determinism:** fixed seeds for generated values, no reliance on
   wall-clock "now" (injected clocks), stable sort-order assumptions made
   explicit, id strategies that don't collide across runs.
4. **Design parallel isolation:** worker-scoped namespacing (prefix/tenant
   per worker), no test mutates catalog baseline rows (baseline is
   read-only; mutation targets are per-test creations), resource pools for
   scarce externals.
5. **Enforce PII safety:** synthetic-only generation rules (realistic but
   fake names/emails/domains reserved for testing), NO production copies —
   if a production-shaped dataset is truly required, the anonymization path
   goes through `human-approval-boundary` with a named technique, never
   ad-hoc scrubbing.
6. **Define cleanup + traceability:** structural cleanup per layer
   (transaction rollback / teardown-by-namespace / TTL sweeps for orphaned
   E2E data), and traceability — every created record carries its run/test
   marker so orphans are attributable.
7. **Set the evolution policy:** seeds/factories change in the SAME change
   as schema migrations (the migration PR fails CI if factories lag);
   ownership named; fossil-fixture audits scheduled. Hand wiring to the
   engineer skills.

## Output Format

```
TEST DATA DESIGN — <scope>
Persona & baseline catalog: <personas + baseline world, all read-only>
Per-layer sources: <unit/integration/E2E/manual → source + creation path>
Factory architecture: <single shape-truth definitions, overrides, id strategy>
Determinism rules: <seeds, clock injection, explicit orderings>
Parallel isolation: <worker namespacing, read-only baseline, mutation scope>
PII safety: <synthetic generation rules; production-data stance;
            anonymization path if any (approved via human-approval-boundary)>
Cleanup & traceability: <per-layer mechanism + run/test markers + TTL>
Evolution policy: <schema-change coupling, ownership, fossil audits>
Compatibility: <two-tenant A/B security fixtures (multi-tenant-security-tester)
               satisfiable from this design>
Handoffs: <wiring → engineer skills; storage layout → qa-automation-architect>
```

## Validation Checklist

- [ ] Personas/baseline cataloged, minimal, and read-only in tests.
- [ ] Every layer has a named data source; no layer "borrows" another's.
- [ ] Determinism rules cover generated values, time, and ordering.
- [ ] Parallel isolation is structural (namespacing), not conventional
      ("please don't touch user1").
- [ ] Zero production data; synthetic rules stated; any anonymization path
      explicitly approved.
- [ ] Cleanup is structural with traceable run markers; TTL for orphans.
- [ ] Seed evolution coupled to schema changes with a named owner.
- [ ] Security-fixture compatibility (A/B tenants) confirmed, not re-owned.

## Gotchas

- The "one big seed file" grows until every test implicitly depends on row
  47 — keep baseline minimal and make tests create what they mutate.
- Hardcoded ids collide the day suites parallelize; worker-scoped prefixes
  are cheaper installed early than retrofitted.
- "Scrubbed" production copies leak through free-text fields, JSON blobs,
  and encoded columns — synthetic generation is the only clean default.
- Factories that bypass validations/constraints (raw inserts) produce
  states the app can't create — impossible-state fixtures make tests pass
  against fiction; write through real code paths or real migrations.
- Faker-style randomness without a fixed seed makes failures
  irreproducible — determinism beats variety in fixtures.
- Fixture realism drift: seeds built for the v1 schema silently stop
  representing real usage — the evolution policy is what prevents fossil
  suites.

## Stop Conditions

- The tenancy/role model is undefined and personas would be invented →
  route to `tenant-modeler`/`authorization-matrix-designer` first; test
  personas mirror the real model.
- Production data use is requested (or discovered) → stop that path;
  synthetic replacement is the default, and any anonymization exception
  goes through `human-approval-boundary` with a named technique.
- Layers/suites don't exist yet and per-layer sources would be speculative
  → design for the layers the strategy names, mark the rest deferred.
- Asked to also implement seeds/factories in code → hand to the engineer
  skills with this design.

## Supporting Files

- [references/test-data-patterns.md](references/test-data-patterns.md) —
  persona catalog template, factory patterns (shape truth, overrides,
  build-vs-create), namespacing schemes, synthetic-data generation rules,
  TTL/traceability recipes.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the unit/build/flake/data
  cluster and against `multi-tenant-data-architect` /
  `multi-tenant-security-tester`.
