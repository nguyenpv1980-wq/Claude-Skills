---
name: api-contract-test-designer
description: Design contract tests that VERIFY implementations against API, command, provider, webhook, and edge-function contracts WITHOUT UI tests — request/response schema validation (shape, types, required fields, error envelope), provider-side and consumer-side roles, versioning checks, and backward-compatibility gates (additive vs breaking diff rules) wired into CI. Contract = does the shape/version hold; not the business flow behind it. Produces the verification design and hands implementation off. Use when asked to contract-test an API/webhook/RPC surface, prevent breaking API consumers or partners, verify a provider's responses match what consumers were promised, or gate schema drift in CI. Do NOT use to DESIGN the contract itself — versioning policy, envelopes, rate limits are api-event-architect, which this skill verifies; not for end-to-end flow through internal boundaries (integration-test-designer) or browser tests (playwright-e2e-engineer).
---

# API Contract Test Designer

## Purpose

Design the verification layer that catches contract drift before consumers
do: schema/shape validation of requests and responses, error-envelope
conformance, version coverage, and backward-compatibility gates that fail CI
on breaking diffs. The contract itself (resources, versioning policy,
webhook envelopes) is designed by the shipped `api-event-architect` — this
skill builds the tests that prove implementations honor it, from both the
provider side (we produce what we promised) and the consumer side (we
tolerate what providers actually send).

## Use When

- Use when: asked to contract-test an API, command surface, webhook feed,
  RPC, or edge function — with no UI in the loop.
- Use when: consumers/partners keep breaking on releases and drift must be
  gated in CI.
- Use when: verifying backward compatibility of a proposed API change
  (additive vs breaking) before it ships.
- Use when: our system CONSUMES a third-party provider and fakes/recordings
  must be proven faithful to the real provider shape.
- Do NOT use when: the ask is to design or overhaul the contract — routes,
  versioning/deprecation policy, idempotency, webhook envelope — that is
  `api-event-architect`; this skill takes its output as the source of truth.
- Do NOT use when: the ask is business flow through real internal boundaries
  (service→DB→permissions) — `integration-test-designer`; contract checks
  shape/compatibility, not end-to-end behavior.
- Do NOT use when: authorization/tenant-isolation properties of the API are
  in question — the shipped `multi-tenant-security-tester`.
- Do NOT use when: a browser journey is involved — `playwright-e2e-engineer`.

## Inputs to Inspect

1. The contract source of truth: OpenAPI/JSON Schema/zod/protobuf definitions,
   `api-event-architect` output, published docs, or — if none exists — the
   de-facto shapes consumers rely on (and flag the missing contract).
2. The surfaces: endpoints, commands, webhooks, edge functions; their
   versions in the wild and the deprecation state of each.
3. Consumers: internal apps, partners, SDKs — what subset of the contract
   each actually uses (drives compatibility severity).
4. Provider dependencies we consume: which third-party shapes our fakes/
   recordings assume (ties to `integration-test-designer`'s faked seams).
5. CI reality: where schema artifacts live, how diffs could be computed per
   PR.

## Workflow

1. **Pin the contract source of truth per surface.** Machine-readable schema
   preferred. No schema anywhere → the first deliverable is extracting the
   de-facto contract into one (flagged as an assumption to confirm), not
   testing against vibes.
2. **Assign roles per surface:** provider-side tests (our responses/webhook
   payloads validate against the published schema — status codes, required
   fields, types, nullability, error envelope) and consumer-side tests (our
   client tolerates documented variation: optional fields absent, unknown
   fields present, documented error shapes). Role patterns in
   [references/contract-test-patterns.md](references/contract-test-patterns.md).
3. **Design schema-validation tests:** for each surface × version — valid
   request accepted; invalid request rejected with the CONTRACTED error
   envelope; response validates against schema (success AND error paths);
   webhook payloads validate before send.
4. **Design the compatibility gate:** schema diff per PR classified by rule —
   additive (new optional field, new endpoint) passes; breaking (removed/
   renamed field, type change, new required field, narrowed enum) fails
   unless a new version + deprecation path per the contract's policy exists.
5. **Cover version coverage explicitly:** every version still in its support
   window has provider-side tests; sunset versions' tests retire WITH the
   version, via `regression-suite-curator`.
6. **Keep fakes faithful:** consumer-side recordings/fixtures used by
   integration suites are re-validated against the provider schema on a
   schedule, so seams don't drift silently.
7. **Define CI placement & artifacts:** contract suite on PR (blocking),
   schema-diff report as PR artifact, provider re-validation cadence; hand
   implementation off with tool choices per the automation blueprint.

## Output Format

```
CONTRACT TEST DESIGN — <surface(s)>
Contract source of truth: <schema artifact per surface + gaps flagged>
Roles: <surface → provider-side / consumer-side obligations>
Schema validation specs:
  <id> — <surface × version> — <request|response|webhook|error-envelope>
       — validates <schema ref> — negatives <invalid input → contracted error>
Compatibility gate: <diff rules additive-pass/breaking-fail + version policy hook>
Version coverage: <versions in support window → specs; retiring versions noted>
Fake-fidelity plan: <which fixtures/recordings re-validate against providers, cadence>
CI placement: <PR blocking suite, diff artifact, scheduled re-validation>
Handoffs: <implementation → engineer; contract redesign gaps → api-event-architect;
          flow behavior → integration-test-designer>
Exit criteria: <all surfaces schema-pinned, gate active, versions covered>
```

## Validation Checklist

- [ ] Every surface has a pinned machine-readable contract or a flagged
      extraction task — no testing against undocumented vibes.
- [ ] Provider-side AND consumer-side roles assigned explicitly per surface.
- [ ] Error envelopes tested, not just success shapes.
- [ ] Breaking-vs-additive rules enumerated and wired as a CI gate.
- [ ] Every in-support version covered; retirement path via curator noted.
- [ ] Fake/recording fidelity re-validation scheduled.
- [ ] No business-flow assertions smuggled in (that's integration's layer).
- [ ] No UI tests anywhere in the design.

## Gotchas

- Testing only happy-path response shapes misses the most common drift:
  error envelopes change and consumers' error handling breaks silently.
- A schema that nobody generates from or validates against goes stale the
  week after it's written — the gate must run in CI or the contract is
  decorative.
- "Additive" changes can still break consumers that use strict/closed
  deserialization — consumer-side tolerance tests catch what diff rules
  can't see.
- Contract tests that call through the full stack with seeded data are
  integration tests wearing a badge — keep them at the schema boundary
  (handler/serializer level or recorded transport) so they stay fast and
  unambiguous.
- Webhooks drift more than APIs (no consumer request to fail loudly) —
  validate payloads at send time in the suite, and signature/envelope fields
  per the `api-event-architect` policy.

## Stop Conditions

- No contract artifact exists AND consumers can't be identified → extracting
  a de-facto contract would be guesswork about what matters; ask for the
  consumer list or the authoritative doc first.
- The observed implementation and the published contract disagree → that is
  a `source-of-truth-reconciler` decision (fix impl vs re-version contract),
  not a silent test-to-implementation.
- A required change is actually contract DESIGN (new versioning policy,
  envelope) → route to `api-event-architect` before writing verification
  for a contract that's about to change.
- Asked to also implement/run the suite → hand off; this skill designs.

## Supporting Files

- [references/contract-test-patterns.md](references/contract-test-patterns.md) —
  provider/consumer role patterns, breaking-change rule table,
  error-envelope test catalog, fake-fidelity recipes.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against the shipped
  `api-event-architect` (designs contracts) and `integration-test-designer`
  (flow vs shape), within the test-level cluster.
