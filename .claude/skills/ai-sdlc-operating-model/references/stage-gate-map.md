# Stage-Gate Map — default composition table

The default lifecycle the operating model starts from. Every row composes an
existing skill by name; the model document cites this table and adapts rows to
the repo — it never copies skill procedures into itself.

| Stage | Entry condition | Exit gate | Authority | Enforcing skill | Evidence left behind |
|---|---|---|---|---|---|
| Context | task received | repo identity + governing docs verified; assumptions listed | agent | `agent-startup-context-gate` | context report (facts vs assumptions) |
| Reconcile | sources conflict (any stage may route here) | one resolved truth, assumptions surfaced | agent | `source-of-truth-reconciler` | reconciliation report with citations |
| Classify | context verified | change class + validation floor + approval path declared; scope locked | agent | `change-classification-gate` | declared class + file-set scope |
| Plan / approve | class known | boundaries identified; approvals obtained for boundary-crossing steps | human decides; agent requests | `human-approval-boundary` + `agent-authorization-matrix` | approval records with scope wording |
| Implement | scope + approvals in place | diff matches declared intent; only intended files staged | agent | `reviewable-diff-discipline` (with `docs-first-implementer`, `tdd-engineer` as the work demands) | scoped diff; commit trail |
| Validate | diff complete | change-class validation floor met with real outputs | agent | class floor from `change-classification-gate`; Phase 5 QA skills as applicable | command outputs, CI runs |
| Review | validation green | human/agent review recorded; security lens where class requires | human (agent may pre-review) | `code-reviewer` / `security-pr-reviewer` | review record on the PR |
| Merge | review + checks green | merged BY THE AUTHORITY HOLDER — per matrix, a named human for protected branches; agents open PRs and stop; agents never arm auto-merge | human | `agent-authorization-matrix` | merge event traceable to a human decision |
| Close | merged (or work stopped) | closeout delivered incl. intentionally-not-done | agent | `ai-closeout-reporter` | closeout report |
| Learn | closeout delivered | memory updated per write rules; periodic compliance spot-check scheduled | agent proposes; human approves memory/policy edits | `agent-memory-governance`, `agent-governance-audit` | governed memory entries; audit reports |

Failure at any stage routes to `agent-failure-recovery` (broken tree/branch
state) or back to Reconcile (conflicting truths). Instruction-file drift found
along the way routes to `agent-instruction-consolidator` (manual).

## Authority levels

- **agent** — autonomous within the stage's contract; evidence still required.
- **agent-with-approval** — agent executes only inside a recorded approval's
  scope (one-time or durable; never wider than its wording).
- **human** — the decision itself is human; the agent may prepare everything
  up to the decision point and must stop there.

## Adoption sequencing notes

1. Adopt the merge-authority row first — it is where the worst incidents live
   (unreviewed merges via auto-merge armed in an earlier session).
2. Then the classify + approve rows (scope lock, boundary approvals), which
   prevent most drift at the source.
3. Then evidence rows (validate, close), which make the audit stage possible.
4. Schedule `agent-governance-audit` spot-checks only after the rows they
   would audit are adopted — auditing unadopted policy produces noise.
5. Revisit the model on its review date with audit findings in hand; the map
   is versioned policy, not scripture.
