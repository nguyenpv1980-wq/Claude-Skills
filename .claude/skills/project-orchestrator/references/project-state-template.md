# `docs/project-state.md` — schema and template

This is the durable memory of a project's journey from idea to shipped. The
orchestrator **reads it first every session** (to locate the project on the
lifecycle map) and **appends to it** as the project advances — each entry
previewed (exact path + content) and explicitly approved by the user before
it is written (the orchestrator's Capability 4 propose → approve → append
contract). It lives in the **user's product repo** at `docs/project-state.md`
— never in the skills library.

## Composition (what this schema reuses, by name)

- **Decision log** composes `phased-work-handoff-designer`'s decision-ID
  register: every binding decision gets a stable ID and is carried forward;
  each entry declares whether it **still binds**; a changed decision is a **new
  entry that flags the deviation**, never a silent overwrite.
- **Approvals** composes `scoped-approval-register`'s citation pattern: Status /
  Scope allowed / **Scope FORBIDDEN** / Evidence, append-style, supersede-never-
  rewrite, deny-by-default (an action is authorized only if an ACTIVE entry's
  allowed scope covers it as worded).
- **Plain-language summaries** are the house decision-log format: a human
  reading months later understands each entry without re-deriving it.

## Non-negotiable rules

1. **Append-only.** Never edit or delete a past entry. A correction is a NEW
   dated entry that references and supersedes the old one — the Zero Trust AI
   Engineering Discipline applied to the build journey.
2. **Dated.** Every entry carries an ISO date (`YYYY-MM-DD`; add time where two
   entries land the same day and order matters).
3. **Plain language.** Summaries are readable by a non-developer. Technical
   terms, when unavoidable, are explained in the same line.
4. **Attributed.** Every decision says who decided: `user` (a business decision
   the user authorized) or `orchestrator-via-<skill>` (an engineering decision
   the orchestrator made through the owning skill and explained).
5. **No secrets, no live identifiers.** Reference environments, tenants, and
   people by role or placeholder, never by credential or real name.

---

## Template (copy into `docs/project-state.md`)

```markdown
# Project State — <plain project name>

Last updated: <YYYY-MM-DD>
Current stage: <plain-language stage — e.g. "Design: how it will be built">
Next recommended action: <one plain-language sentence>

## The idea (approved brief)

- What the business does: <one line>
- What goes wrong today: <the problem, in the user's words>
- Who the customers/users are: <one line>
- What "done enough to ship" means (MVP): <the agreed first-release scope>

## MVP scope (approved)

- In scope for v1: <bullet list — what the first release WILL do>
- Explicitly OUT of scope for v1: <bullet list — what it deliberately will NOT do>
- Approved by: <user> on <YYYY-MM-DD>   (see Approval A-001)

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| PS-001 | <date> | <what was decided and why, in plain language> | user \| orchestrator-via-<skill> | yes | <link / skill output / the gate this unblocks> |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| A-001 | ACTIVE \| SUPERSEDED by <id> \| EXPIRED <date> | <date> / user | <exactly what was authorized, as worded> | <adjacent action this does NOT authorize> | <where the grant is recorded> |

## Open questions (still need the user)

- <one plain-language question at a time; the decision it unblocks>

## Deviations (a decision changed course)

- <PS-00x superseded by PS-00y on <date>: what changed and why — the old entry
  stays above, unedited>
```

---

## Worked example (generic maintenance-company illustration)

```markdown
# Project State — Maintenance job-tracking app

Last updated: 2026-03-04
Current stage: Design: how it will be built
Next recommended action: Answer one question about customer data separation, then
I hand the data design to the multi-tenant data skill.

## The idea (approved brief)

- What the business does: dispatches maintenance crews to customer sites.
- What goes wrong today: jobs get missed because they're tracked on paper.
- Who the customers/users are: office dispatchers (internal) and site contacts
  (external, who want a status link).
- What "done enough to ship" means (MVP): create a job, assign a crew, mark it
  done, and send the site contact a status link.

## MVP scope (approved)

- In scope for v1: job create/assign/complete; crew list; customer status link.
- Explicitly OUT of scope for v1: invoicing, scheduling optimization, a mobile app.
- Approved by: user on 2026-02-20 (see Approval A-001)

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| PS-001 | 2026-02-20 | Ship a small first version: create/assign/complete a job + a customer status link. Everything else waits. | user | yes | brief above; unblocks product spec |
| PS-002 | 2026-02-27 | Build it as one connected system for now (not many separate services) — cheaper and simpler for a small team and a few hundred users. | orchestrator-via-architecture-advisor | yes | advisor output; unblocks data design |
| PS-003 | 2026-03-04 | Status links stop working when the job closes (chosen over "expire in 30 days" / "last forever"). | user | yes | unblocks share-link design |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| A-001 | ACTIVE | 2026-02-20 / user | Build the v1 scope listed above. | Adding invoicing or a mobile app without a new decision. | brief sign-off, this file |

## Open questions (still need the user)

- Should every customer's data sit in its own separate space, or share one space
  with strict rules keeping them apart? (Separate costs more; shared is cheaper
  and still safe when done right.) — unblocks the data design.
```

Note how the user only ever answered **business** questions (what to ship, when a
link should die, how separate customer data should feel), while the
"one connected system vs many services" call was made by the orchestrator through
`architecture-advisor` and recorded as `orchestrator-via-…` — explained in plain
language, never handed to the user as a technical choice.
