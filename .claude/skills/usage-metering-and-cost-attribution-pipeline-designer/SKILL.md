---
name: usage-metering-and-cost-attribution-pipeline-designer
description: Design the metering → pricing → rollup → reconciliation DATA PIPELINE for a multi-tenant SaaS — a billing-safe usage-event table (metadata only, no message/file CONTENT), time-bounded rate cards, cost entries carrying idempotency keys so replays and retries never double-bill, additive rollups (an analytical projection), budgets + breach alerts, spend forecast, and reconciliation of metered totals against provider invoices. Produces the event schema, rate-card model, idempotent cost-entry contract, rollup jobs, and reconciliation loop. Use when BUILDING the metering/billing pipeline, when usage numbers do not match the invoice, or when retries double-count. Do NOT use for the unit-economics COST MODEL — what a tenant costs, whether pricing is profitable (saas-cost-architect — closest neighbor, pinned hard), AI spend guardrails/kill-switch (ai-cost-guardrail-designer), or the operational-vs-analytical split (operational-vs-analytical-splitter).
---

# Usage Metering & Cost Attribution Pipeline Designer

## Purpose

Billing-grade numbers are an engineering problem before they are a finance
one: a usage event dropped or counted twice, a rate card changed without a
time boundary, a rollup that is not additive, or a metered total that never
gets checked against the provider's invoice — each quietly produces a number
someone gets billed on. This skill designs the DATA PIPELINE that turns raw
usage into trustworthy per-tenant cost: a billing-safe event table, versioned
rate cards, idempotent cost entries that survive replays, additive rollups,
budgets with breach alerts, a spend forecast, and a reconciliation loop
against the source-of-truth invoice. The deliverable is the event schema,
the rate-card model, the cost-entry + idempotency contract, the rollup jobs,
and the reconciliation loop.

**Standalone, not an extension of `saas-cost-architect` (resolved at build,
D31).** `saas-cost-architect` builds the economic MODEL — driver inventory
from real bills, attribution POLICY, unit economics vs revenue, and whether a
tenant is profitable; it answers "what does this cost and does pricing cover
it." This skill builds the running PIPELINE that produces the numbers that
model (and the invoice) depend on — event schema, idempotency keys, additive
rollups, invoice reconciliation. They compose: the model decides what to
attribute; the pipeline computes and reconciles it at billing grade. The
overlap is the word "attribution"; the surfaces (a reasoning artifact vs an
ETL/schema design) barely touch.

## Use When

- Use when: BUILDING the metering/billing data pipeline — the usage-event
  table, rating against rate cards, cost entries, rollups, and reconciliation.
- Use when: metered usage numbers do not match the provider's invoice, or
  finance cannot reconcile what was billed to what was measured.
- Use when: retries, replays, or re-processing double-count usage or cost,
  and the pipeline needs idempotency.
- Use when: rate/price changes corrupt historical bills because rate cards
  have no time boundary (a price change silently re-rates last month).
- Use when: designing per-tenant budgets, breach alerts, and spend forecasts
  off metered data.
- Do NOT use when: the question is the COST MODEL / unit economics — what a
  tenant or plan actually costs, whether pricing is profitable, which tenants
  are underwater — that is `saas-cost-architect` (the closest neighbor). This
  skill is the pipeline that FEEDS that model, not the model.
- Do NOT use when: the subject is AI-spend guardrails specifically — per-
  request token caps, cost-aware rate limits, a spend kill switch — that is
  `ai-cost-guardrail-designer`; this pipeline may METER AI usage, but the
  budget-enforcement/kill-switch design lives there.
- Do NOT use when: the question is WHETHER analytics/rollup workloads should
  leave the operational store — that is `operational-vs-analytical-splitter`;
  the rollup this skill designs is an analytical projection whose placement
  that decision governs.

## Inputs to Inspect

1. The metered activity: what generates cost or is billed (API calls, storage,
   seats, AI tokens, compute-minutes, third-party pass-through) — the events
   the pipeline must capture, and their volume.
2. The pricing model (from `plan-entitlement-architect` / the price book):
   plans, unit prices, allowances/overage, and how often prices change — the
   rate cards the pipeline rates against.
3. Existing metering, if any: how usage is recorded today, whether events are
   deduplicated, and any incident history of double-billing or unreconciled
   drift.
4. The provider/source-of-truth totals: the cloud/AI/third-party invoices the
   metered totals must reconcile against, and their granularity and lag.
5. The tenant model: how usage events carry tenant (and user/feature) context
   for attribution, and whether any activity is currently un-attributed.
6. Privacy constraints: what must NOT enter a usage event (message/file
   content, PII, prompt text) — the billing-safe boundary.

## Workflow

1. **Design the billing-safe usage-event table.** One append-only event per
   metered unit: `tenant_id`, optional `user_id`/`feature`, `metric`,
   `quantity`, `occurred_at`, `source`, and a unique `event_id`. The
   discipline: METADATA ONLY — never message bodies, file contents, prompt/
   response text, or PII. The event records THAT usage happened and how much,
   not what was in it. State the retention and that events are immutable.
2. **Model rate cards with time boundaries.** A rate card maps
   metric → price, and every card carries an effective `[valid_from,
   valid_to)` window. Rating an event uses the card in effect at the event's
   `occurred_at`, NOT the current card — so a price change never re-rates
   history. Version cards; never mutate a past one.
3. **Design cost entries with idempotency keys.** Rating produces cost
   entries (exact where measured, estimated where inferred, allocated where
   proportional — label which). Each entry carries an idempotency key derived
   from the event id + rate-card version, so re-running the rater, replaying
   events, or retrying a batch produces the SAME entry, never a duplicate.
   Re-processing is a normal operation; the pipeline must be safe under it.
4. **Design additive rollups.** Daily (and per-tenant/per-metric) rollups
   that SUM cost entries into aggregates. Additivity is the property that
   makes them safe to recompute and to combine across time — avoid rollups
   that can't be re-derived from the entries. State that a rollup is a
   projection of the entries, always reconstructable, never the source of
   truth. (Its analytical-store placement follows
   `operational-vs-analytical-splitter`.)
5. **Design budgets, breach alerts, and forecast.** Per-tenant/plan budget
   thresholds evaluated against rollups; alerts fired BEFORE the budget is
   gone (with owners); a spend forecast from the trend. Note that ENFORCING a
   budget (throttle/kill) — especially for AI spend — is
   `ai-cost-guardrail-designer`'s job; this pipeline provides the metered
   signal it acts on.
6. **Design the reconciliation loop — the trust anchor.** Periodically
   compare metered totals against the provider/source-of-truth invoice per
   metric and tenant, compute drift, and define the tolerance beyond which
   the pipeline is considered broken and investigated. Metering nobody
   reconciles is a number nobody should bill on. Define what a discrepancy
   triggers (recompute, rate-card audit, missing-event hunt).
7. **Design late/out-of-order and correction handling.** Late-arriving events
   (a usage report delayed past its day) and corrections (a refund/void) as
   explicit additive adjustments with their own entries — never an in-place
   edit of a past rollup. State the close/lock policy (when a period is
   finalized) and how post-close corrections are booked to the next period.
8. **Deliver** the event schema, rate-card model, cost-entry + idempotency
   contract, rollup jobs, and reconciliation loop in the Output Format, with
   the cost-MODEL, AI-guardrail, and split handoffs named.

## Output Format

```
USAGE METERING & COST PIPELINE — <system/domain>
Usage-event table: <fields; METADATA ONLY (no content/PII); immutable; retention>
Rate cards:     <metric → price; [valid_from, valid_to); rate at occurred_at,
  not current; versioned, past cards immutable>
Cost entries:   <exact/estimated/allocated labeled; idempotency key =
  event_id + rate-card version; re-processing produces same entry>
Rollups:        <daily/tenant/metric SUM of entries; additive; reconstructable
  projection, not source of truth; analytical placement → operational-vs-analytical-splitter>
Budgets/alerts/forecast: <thresholds vs rollups; alert-before-gone + owners;
  forecast>; ENFORCEMENT (throttle/kill, esp. AI) → ai-cost-guardrail-designer
Reconciliation: <metered totals vs provider invoice per metric/tenant; drift +
  tolerance; discrepancy → recompute/audit/missing-event hunt>
Late/corrections: <late events + refunds/voids as additive adjustments;
  period close/lock; post-close → next period>
Boundaries:     cost MODEL / unit economics → saas-cost-architect;
  AI spend guardrails → ai-cost-guardrail-designer
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Usage events carry metadata only — no message/file content, prompt
      text, or PII; events are immutable and retained.
- [ ] Rate cards are time-bounded and events are rated at their `occurred_at`
      card version; a price change never re-rates history.
- [ ] Every cost entry carries an idempotency key; re-running the rater or
      replaying events produces the same entry, never a duplicate.
- [ ] Rollups are additive projections of cost entries — reconstructable, and
      never the source of truth.
- [ ] A reconciliation loop compares metered totals to the provider invoice
      with a stated tolerance and a defined action on drift.
- [ ] Late/out-of-order events and corrections are additive adjustments, not
      in-place edits of finalized rollups; a period close/lock policy exists.
- [ ] Budget ENFORCEMENT (throttle/kill) is deferred to
      `ai-cost-guardrail-designer`; the pipeline provides the signal.
- [ ] The unit-economics/profitability question is deferred to
      `saas-cost-architect`; this skill builds the pipeline, not the model.

## Gotchas

- Putting content in a usage event ("store the prompt so we can debug
  billing") turns the metering table into a PII/secret store with billing-
  grade retention — meter metadata, never payload.
- A rate card without a time boundary re-rates the past the moment you change
  a price: last month's invoices silently shift. Rate at `occurred_at`.
- No idempotency key means every retry/replay double-bills; and metering
  pipelines retry constantly. Idempotency is not optional here, it is the
  correctness property.
- Non-additive rollups (storing a computed average or a running balance you
  can't re-derive) can't be recomputed after a correction — keep rollups as
  sums of immutable entries.
- Editing a finalized rollup to "fix" a number destroys the audit trail;
  corrections are new, additive, signed adjustment entries.
- Metering that is never reconciled against the real invoice drifts silently
  until a customer disputes a bill; reconciliation is the trust anchor, not a
  nice-to-have.
- Late events after period close, booked into the closed period, change a
  finalized invoice; define the close/lock and book late items to the next
  period.
- Estimated and exact cost entries mixed without a label make the number
  un-auditable; label the basis of every entry.

## Stop Conditions

- The request is really "what does a tenant/plan cost and is our pricing
  profitable" → route to `saas-cost-architect`; this skill builds the
  pipeline that produces the inputs to that model, not the model.
- The request is AI-spend enforcement (token caps, cost-aware rate limits, a
  kill switch) → route to `ai-cost-guardrail-designer`; this pipeline supplies
  the metered signal but does not design the enforcement.
- The source-of-truth invoice to reconcile against is unavailable → the
  pipeline can be designed, but say plainly that its numbers are unverified
  until reconciliation has a source; do not present unreconciled metering as
  billing-grade.
- Asked to run the pipeline / a re-rating job against production billing data
  → this skill DESIGNS; executing a re-rate or correction against live
  billing follows the repo's approval path (billing changes are high-blast-
  radius).

## Supporting Files

- `evals/evals.json` — behavior cases: the build-the-pipeline design, the
  replay-idempotency edge, the reconciliation-drift case, the content-in-event
  refusal, and the cost-model non-trigger.
- `evals/trigger-evals.json` — discrimination against `saas-cost-architect`
  (THE hard-pinned seam — pipeline vs cost model), `ai-cost-guardrail-designer`
  (metering signal vs spend enforcement), and `operational-vs-analytical-splitter`
  (rollup as analytical projection).
- No `references/` — the event/rate-card/idempotency/reconciliation procedure
  above is complete; detail lives in the produced artifacts.
