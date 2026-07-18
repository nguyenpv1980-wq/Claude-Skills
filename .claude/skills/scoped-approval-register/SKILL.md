---
name: scoped-approval-register
description: 'Record every granted human approval as a durable, append-style register entry — Status, Reason, Scope allowed, Scope FORBIDDEN, Evidence — so authorization survives the approving conversation and is cited from the repo, never re-argued from memory. Covers placement, entry lifecycle (supersede, never rewrite), and the deny-by-default citation rule: an action is authorized only if an ACTIVE entry''s allowed scope covers it as worded. Use when an approval was just granted and must be recorded, when agents re-ask already-decided permissions, or when "am I allowed to do X?" has no citable answer. Composes human-approval-boundary: it decides WHERE approval is required and halts; this records the grant it obtains. Do NOT use to decide whether approval is needed (human-approval-boundary), design standing-approval policy (standing-approval-and-auto-advance — its adopted policy lands here as an entry), codify authority floors (agent-authorization-matrix), or record design decisions (adr-writer).'
---

# Scoped Approval Register

## Purpose

Make granted approvals durable, scoped, and citable. Approvals granted in
conversation evaporate when the conversation does — the next session either
re-asks (fatigue) or assumes (hazard). This skill records each grant as an
append-style register entry with five mandatory fields — Status, Reason,
Scope allowed, Scope FORBIDDEN, Evidence — so that months later an agent can
cite exactly what is and is not authorized, and negative scope is as explicit
as positive scope. The register is the TRACK half of the approval discipline:
`human-approval-boundary` obtains the decision; this skill makes it outlive
the chat. Evidence for the pattern: a production multi-agent repo (Repo A)
maintained ~60 such "narrow exception" blocks in its context map, each with
exactly these fields.

## Use When

- Use when: a human just granted an approval (in chat, PR comment, or issue)
  and it must be recorded before the wording is lost.
- Use when: an agent re-asks permission for something already decided, and no
  one can point to where the decision lives.
- Use when: "am I allowed to do X?" has no citable answer — set up or extend
  the register.
- Use when: auditing whether a past action was covered by a recorded grant
  (read the register; cite the entry).
- Do NOT use when: deciding whether the NEXT step needs approval or halting
  for it — that is `human-approval-boundary`; this skill records what that
  boundary obtains.
- Do NOT use when: designing a STANDING approval for the mechanical delivery
  loop with opt-out and phase-advance semantics — that is
  `standing-approval-and-auto-advance`; once designed and human-granted, its
  standing scope is recorded HERE as an entry.
- Do NOT use when: defining which actions agents may ever take autonomously —
  that is `agent-authorization-matrix` (the standing policy); the register
  records individual grants made under or beyond it.
- Do NOT use when: recording an architecture/technology decision with
  alternatives and consequences — that is `adr-writer`. Approvals authorize
  actions; ADRs record design choices.

## Inputs to Inspect

1. The grant itself — the human's exact wording, verbatim (chat message, PR
   comment, issue reply). The wording IS the scope; paraphrase widens or
   narrows it silently.
2. The existing register, if any (`docs/approvals/`, a context-map exceptions
   section, or wherever the repo keeps it) — to append, supersede, or detect
   conflicts with prior entries.
3. What was actually requested when the approval was sought — the
   `human-approval-boundary` request block if one exists (action, blast
   radius, options), so the recorded scope matches what was asked.
4. Expiry signals: did the grantor say "this once", "for this phase",
   "until X"? Durable vs one-time must come from the wording, not assumption.
5. Repo conventions for where governance records live (see
   [references/register-format.md](references/register-format.md) placement
   options).

## Workflow

1. **Capture the grant verbatim at the moment it is given.** Quote the exact
   approving words and their source location. If the wording is ambiguous
   about scope, ask the grantor to tighten it NOW — recording an ambiguous
   scope creates a phantom authorization.
2. **Locate or create the register.** Prefer one dedicated, append-style file
   (e.g. `docs/approvals/APPROVAL_REGISTER.md`); a context-map exceptions
   section is an equally valid house pattern. One register per repo — split
   registers fragment citation.
3. **Write the entry** with all mandatory fields (full template and field
   semantics: [references/register-format.md](references/register-format.md)):
   Status, Date + Grantor, Reason, **Scope allowed** (as worded), **Scope
   FORBIDDEN** (explicit negatives — what this approval does NOT cover),
   Evidence (link/pointer to the grant), Expiry/review-by.
4. **Derive the FORBIDDEN scope explicitly.** Ask: what adjacent action would
   a future agent plausibly stretch this grant to cover? Name it as
   forbidden. An empty forbidden list is a draft, not an entry.
5. **Check for interactions:** does this entry supersede, conflict with, or
   partially overlap an existing one? Supersede by adding a new entry and
   flipping the old entry's Status to `SUPERSEDED by <id>` — never rewrite or
   delete history.
6. **State the citation rule with the register** (once, at the top): an
   action is authorized by the register only if an ACTIVE entry's Scope
   allowed covers it; absence from any FORBIDDEN list is not permission —
   deny-by-default holds.
7. **Deliver:** the new/updated entry, any superseded-entry status flips, and
   a one-line pointer for the closeout so the grant is discoverable.

## Output Format

```
APPROVAL REGISTER ENTRY
Id:              <register-id — sequential or date-based>
Status:          ACTIVE | SUPERSEDED by <id> | EXPIRED <date> | REVOKED <date, by whom>
Date / Grantor:  <YYYY-MM-DD> / <named human or role>
Reason:          <why this authorization exists>
Scope allowed:   <exact actions, files, branches, environments — as worded by the grantor>
Scope FORBIDDEN: <explicit negatives this grant does NOT cover — never empty>
Evidence:        <link: PR comment / issue / chat record / commit>
Expiry:          <date, condition, "one-time", or "until superseded">
```

## Validation Checklist

- [ ] The grant is quoted or linked verbatim — the entry's scope matches the
      grantor's wording, not a paraphrase.
- [ ] Scope FORBIDDEN is present and names real adjacent actions — not empty,
      not boilerplate.
- [ ] Evidence field points at a retrievable artifact, not "approved in chat"
      with no pointer.
- [ ] Expiry/one-time vs durable comes from the wording, not assumption.
- [ ] Superseded/conflicting entries had Status flipped — no entry was
      rewritten or deleted.
- [ ] The citation rule (deny-by-default; ACTIVE + covered = authorized) is
      stated with the register.
- [ ] No secrets, tokens, or live identifiers in the entry — reference
      environments and tenants by placeholder or name, never credential.

## Gotchas

- **Paraphrase drift:** "yes, go ahead" recorded as "approved schema changes"
  is a fabricated widening. Record the words and what they answered.
- **The missing negative:** most approval disputes are about the action NEXT
  to the approved one. The FORBIDDEN field exists to close that door while
  the grantor is still present.
- **Approval of a different step:** a grant for step A cited to authorize
  step B is the classic misuse; the citation rule (covered-by-wording) is
  what blocks it. See also `human-approval-boundary`'s rule that enthusiasm
  is not approval.
- **Register rot:** entries whose Expiry passed but Status still says ACTIVE
  make the register lie. Sweep expired entries when touching the register.
- **Two registers:** once approvals live in two places, every citation is
  contestable. Merge before appending.
- **Recording ≠ granting:** an entry with no evidence link records nothing.
  The register cannot create authority, only preserve it.

## Stop Conditions

- Asked to record an approval that was never actually granted (no quotable
  wording, no evidence) — refuse: the register preserves real grants; it
  does not manufacture them. This includes backdating entries "so the audit
  passes."
- The grant's wording is too ambiguous to scope and the grantor is
  unavailable — record nothing yet; a scoped question back to the grantor is
  the output.
- The new entry would contradict an ACTIVE entry and it is unclear which the
  grantor intends to stand — surface both, ask; do not pick.
- Asked to widen an existing entry's scope "since it's basically the same" —
  refuse; widening requires a new grant from the grantor.

## Supporting Files

- [references/register-format.md](references/register-format.md) — full entry
  template, field semantics, lifecycle states, placement options, a worked
  example, and anti-patterns.
- `evals/evals.json` — behavior cases incl. refusing to fabricate or backdate
  an entry.
- `evals/trigger-evals.json` — discrimination against `human-approval-boundary`,
  `standing-approval-and-auto-advance`, `agent-authorization-matrix`, and
  `adr-writer`.
