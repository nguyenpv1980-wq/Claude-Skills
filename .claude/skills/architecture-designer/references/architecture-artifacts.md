# Architecture Artifact Quality Bars

Supporting detail for `architecture-designer`. Read on demand.

## Boundary contract catalog

Every edge in the component map gets one of these labels:

| Contract | Coupling | Failure mode to note |
| --- | --- | --- |
| Sync call (HTTP/RPC/in-process interface) | Temporal + availability | Callee down → caller degraded; timeout/retry semantics required |
| Async event | Schema only | Consumer lag, duplicate delivery, ordering |
| Shared table/store | Total (schema, timing, locks) | Any writer migration breaks every reader; declare it, plan to retire it |
| File/batch handoff | Schema + schedule | Partial files, reprocessing, idempotency |
| Anticorruption adapter | Contained | Translation drift; adapter becomes the de-facto spec |

"They import each other's internals" is not a contract; it is the absence of
one — list it under coupling risks.

## Component map quality bar

- Each component has ONE responsibility sentence. If the sentence needs "and,"
  split or justify.
- Allowed dependency directions are stated (e.g., `billing → identity`, never
  reverse). A map without directions cannot detect violations later.
- Every external system appears at the edge with its adapter named.

## Data ownership map quality bar

- Exactly one owner per store/table. Joint ownership is a finding, not a
  category.
- Readers outside the owner go through the owner's contract (API, view,
  event-built replica) — direct foreign reads are recorded as debt with a
  retirement increment in the migration plan.
- Ownership follows write authority: whoever enforces the invariants owns the
  data, regardless of who queries it most.

## Tradeoff table template

| Criterion | Option A: <name> | Option B: <name> |
| --- | --- | --- |
| Complexity added | | |
| Delivery speed (first increment shipped) | | |
| Operability (on-call surface, failure modes) | | |
| Cost (infra + cognitive) | | |
| Reversibility | | |
| What breaks first under 10x load | | |

Fill every cell with a concrete claim, not "medium." The recommendation must
name its reversal condition: "choose A; revisit if <measurable condition>."

## Migration increment patterns

- **Strangler seam** — route new traffic through the target boundary while old
  paths keep working; retire old path as a separate increment.
- **Ownership transfer** — first move writes behind the owner's contract, then
  move readers, then move the data. Never move data first.
- **Contract extraction** — introduce the interface in-place (same deployable),
  verify with tests, only then consider physical separation.
- **Event backfill** — stand up the event flow alongside the sync path; compare
  outputs; cut over when parity holds for a defined window.

Each increment in the plan states: what ships, how it is verified, and the
stop point (what condition pauses the migration without stranding it).
