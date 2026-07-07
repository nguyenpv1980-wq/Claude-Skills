# Contract Test Patterns

Detail file for `api-contract-test-designer`. Loaded on demand.

## Provider-side vs consumer-side obligations

| Role | We are… | Tests prove… |
| --- | --- | --- |
| Provider | the API/webhook producer | every response/payload validates against the published schema; invalid requests get the contracted error envelope; versions in support window all hold |
| Consumer | a client of someone's API | our client tolerates documented variation (absent optionals, unknown extra fields, every documented error shape); our fakes match the real provider |

Most systems are both — assign roles per surface, not per repo.

## Breaking-change rule table (default; defer to api-event-architect policy)

| Change | Class |
| --- | --- |
| new endpoint, new OPTIONAL field, new enum value (open enums), widened input | additive — pass |
| remove/rename field or endpoint, optional→required, type change, narrowed enum, semantics change of existing field, new required header/param | breaking — fail without new version + deprecation path |
| error-envelope shape change | breaking (most-missed case) |

The gate computes schema diff per PR and classifies with this table; breaking
requires the version bump + deprecation evidence, not a warning label.

## Error-envelope test catalog

Per surface: 400 malformed body, 401 unauthenticated, 403 forbidden,
404 not-found, 409/422 domain rejection, 429 rate-limited, 5xx shape.
Assert: envelope fields (code, message, correlation id per contract),
content-type, and that internals (stack traces, SQL, tenant ids of others)
never leak. Authorization CORRECTNESS (who gets the 403) is
`multi-tenant-security-tester`'s suite — here only the SHAPE of the refusal.

## Fake-fidelity recipes

- Recorded fixtures: re-record or re-validate against the provider sandbox on
  a schedule (weekly/CI cron); diff failures open a task, not a silent update.
- Hand-written fakes: generate from the provider schema where possible;
  otherwise validate fake outputs against the schema in the contract suite.
- Every integration-suite faked seam (`integration-test-designer` boundary
  map) lists which contract artifact keeps it honest.

## Tooling notes (adjust to repo)

Schema validation: OpenAPI validators, zod/JSON Schema asserts at the
serializer boundary, protobuf conformance. Diff gating: openapi-diff-style
tools or schema snapshot + classified diff in CI. Consumer-driven contract
frameworks (Pact-style) only when a real multi-team consumer/provider
relationship justifies the broker cost — name the consumer before adopting.
