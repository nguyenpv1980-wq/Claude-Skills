# Auto-Merge Policy

**Recorded:** 2026-07-06
**Repo:** `nguyenpv1980-wq/Claude-Skills`
**Context:** companion decision to the CI merge gate
([`.github/workflows/validate-skills.yml`](../../.github/workflows/validate-skills.yml));
extends the decisions in [`step-0-reconciliation-v4.md`](step-0-reconciliation-v4.md).

## Policy

1. **Auto-merge is opt-in, per phase.** Auto-merge is permitted only for phases explicitly
   opted in via:

   ```bash
   gh pr merge --auto --squash
   ```

   A phase PR without this explicit opt-in follows the normal manual review-and-merge flow.
   Auto-merge completes only after all required status checks (`validate-skills`,
   `gate-guard`) pass.

2. **Merge-gate changes are never auto-merged.** Any change touching the merge gate itself —
   anything under `.github/workflows/` or the file `scripts/validate-skills.py` — always
   requires **manual human review and merge**, regardless of phase or opt-in status. The
   `gate-guard` job enforces this mechanically by failing such PRs with:

   > This PR modifies the merge gate itself and requires manual review and merge.

   A `gate-guard` failure is the intended signal, not a defect. Do not weaken the gate,
   rename its jobs, or bypass the failing check to "make CI green"; a human merges these
   PRs deliberately after reviewing the gate change.

## Rationale

The gate exists so skill-generation phases can land safely at volume. A PR that edits the
validator or the workflows could otherwise loosen the checks and then auto-merge on its own
(now weaker) green run. Splitting the policy this way keeps routine, validated phase work
fast while making every change to the gate itself deliberate and human-approved.
