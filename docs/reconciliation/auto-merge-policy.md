# Auto-Merge Policy

**Recorded:** 2026-07-06
**Repo:** `nguyenpv1980-wq/Claude-Skills` (renamed → `nguyenpv1980-wq/Project-Aegis`; the old URL redirects)
**Context:** companion decision to the CI merge gate
([`.github/workflows/validate-skills.yml`](../../.github/workflows/validate-skills.yml));
extends the decisions in [`step-0-reconciliation-v4.md`](step-0-reconciliation-v4.md).

> **Correction (D34, 2026-07-10).** This document originally specified an **opt-in, per-phase
> auto-merge** mechanism (`gh pr merge --auto --squash`). Per the repo owner, that mechanism
> was **never adopted**: Aegis's entire development used **manual merge** by a human after the
> required checks passed, and auto-merge was never armed as policy. The policy below is
> corrected forward to describe the actual process; the original auto-merge-arming wording is
> summarized inline for provenance, not silently removed. See reconciliation §5, decision D34.
> The one time auto-merge fired — PR #7 — was the unauthorized incident recorded in §6, which
> is precisely why merge stays human-gated.

## Policy

1. **Merge is manual — a human is the gate.** Every PR is reviewed and merged by a human
   after all required status checks (`validate-skills` and `gate-guard`) pass. **Auto-merge is
   never armed** for this project's development. (The superseded original policy made
   auto-merge an opt-in, per-phase step via `gh pr merge --auto --squash`; that arming step was
   never adopted — see the correction above.)

2. **Merge-gate changes are never auto-merged.** Any change touching the merge gate itself —
   anything under `.github/workflows/` or the file `scripts/validate-skills.py` — always
   requires **manual human review and merge**, regardless of phase or opt-in status. The
   `gate-guard` job enforces this mechanically by failing such PRs with:

   > This PR modifies the merge gate itself and requires manual review and merge.

   A `gate-guard` failure is the intended signal, not a defect. Do not weaken the gate,
   rename its jobs, or bypass the failing check to "make CI green"; a human merges these
   PRs deliberately after reviewing the gate change.

## Rationale

The gate exists so skill-generation work lands safely: a human merges each validated PR, and
any PR that edits the validator or the workflows must be reviewed and merged manually
regardless. Keeping merge human-gated — never auto-armed — is the direct lesson of the
ungoverned-auto-merge incident (PR #7) this project absorbed and now encodes as an
`agent-authorization-matrix` eval. An auto-merge-arming step could otherwise loosen the checks
and then merge on its own (now weaker) green run; requiring a human at the merge keeps every
landing deliberate.
