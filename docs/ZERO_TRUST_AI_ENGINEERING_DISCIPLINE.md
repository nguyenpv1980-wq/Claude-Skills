# Zero Trust AI Engineering Discipline

> **Never trust, always verify — every step of the lifecycle.**
> *Assume drift. Demand evidence. Track everything.*

*The tagline deliberately mirrors the Zero Trust security motto "never trust, always
verify," and the gloss's "assume drift" mirrors Zero Trust's companion principle "assume
breach." The homage is intentional: this doctrine extends a proven security principle from
network access to the whole engineering process.*

---

## Core definition

**Zero Trust AI Engineering Discipline (Zet-AI Engineering for short, pronounced
"zet-eye") is the practice of applying the security principle "never trust, always verify"
to the ENTIRE software development lifecycle** — every
decision, code change, test result, completion claim, and piece of documentation is verified
against concrete evidence rather than trusted from memory, assumption, or assertion,
continuously at every step.

Nothing is taken on faith because it was true earlier, because someone remembers it that way,
or because a summary asserts it. The map is re-checked against the territory before it is
used. Evidence is the currency; memory and assertion are not accepted as payment.

## Distinction from classic Zero Trust

Classic **Zero Trust** is a network-security model: never trust a user or device by its
network location; verify every access request explicitly; assume breach. It governs *access*.

This doctrine borrows the same instinct but applies it to the development **process**, not to
network access. Where classic Zero Trust asks *"is this actor allowed to access this?"*, this
doctrine asks *"is this claim actually true, and where is the proof?"* One guards the
perimeter of a system; the other guards the integrity of how the system gets built.

## The two failure modes it prevents

- **DRIFT — the map and the territory diverge.** Documentation says one thing while the code
  does another; decisions get re-litigated because no one is certain what was actually
  decided. The recorded state and the real state quietly fall out of sync.
- **ROT — silent decay.** Tests are quietly skipped, approvals are forgotten, finished work
  is redone. Nothing announces the loss; the discipline just erodes one unchecked step at a
  time.

**Shared root cause:** both come from trusting something without checking it. Drift is a
trusted *description* going stale; rot is a trusted *guarantee* going stale. The fix for both
is the same instinct — verify against evidence instead of trusting the last known state.

This is where **"assume drift" mirrors "assume breach."** Just as Zero Trust assumes an
attacker may already be inside the network and therefore verifies every access, this doctrine
assumes the docs and the memory may already have gone stale and therefore verifies every
claim. You do not wait for proof that the map is wrong before checking it; you assume it may
be wrong and check by default.

## Why it matters most for AI-assisted development

Human teams carry partial natural defenses against drift and rot: memory, gut-feel, the
reflex of *"wait — didn't we decide X?"* A human notices when a claim smells wrong.

AI assistants lack these defenses. An AI will confidently act on stale memory, claim
done-when-not-done, and let documentation drift — not out of laziness, but because it
genuinely cannot tell. It has no gut to check against. Absent an external evidence
requirement, an AI's most confident output and its least reliable output look identical.

So this discipline is the specific antidote to how AI assistants fail. It replaces the human
gut-feel that AI does not have with **enforced evidence** — a structural requirement that
every claim be checked against the real repository, the real test run, the real approval
record, before it is trusted.

## The concrete rules

The discipline has six pillars — four outward-facing (**TRACK**, **VERIFY**, **GOVERN**,
**HAND OFF**), governing the work, and two inward-facing (**CONSTRAIN**, **CURATE**),
governing the AI's own operating environment. What the industry calls harness engineering,
context engineering, and loop engineering falls out of the inward half — the harness is
CONSTRAIN's subject, the context window is CURATE's, and the agentic loop splits between
them (its bounds and stops are CONSTRAIN; its observe-and-validate step is CURATE): the
industry's disciplines expressed in this doctrine's voice, not competitors to it.

The doctrine is not abstract. The outward pillars' building blocks are the ten operational
workflow patterns banked as pack **D12.8** in
[`docs/reconciliation/step-0-reconciliation-v4.md`](reconciliation/step-0-reconciliation-v4.md),
extracted with HIGH-confidence evidence from a read-only audit documented in
[`docs/research/aegis-workflow-extraction-report.md`](research/aegis-workflow-extraction-report.md).
Each pattern is one rule of the discipline:

### TRACK — keep the record and the reality in sync

- **`scoped-approval-register` (P2)** — record every approval durably, with its status,
  reason, scope allowed, scope forbidden, and evidence, so an approval is never re-argued
  from memory.
- **`chat-backlog-reconciliation` (P13)** — extract chat-only decisions and backlog into
  dated repo docs on a cadence, then audit each item against PR/source evidence.
- **`context-co-update-ci-gate` (P8)** — fail any PR that touches important paths without
  updating the context map, so the map cannot silently drift from the territory.

### VERIFY — prove it green before trusting it

- **`local-ci-mirror-preflight` (P4)** — derive local equivalents of every PR-triggered CI
  check and verify on clean mainline first, classifying each failure by cause.
- **`risk-tiered-validation-selector` (P5)** — classify each change to a validation depth,
  failing closed to full validation when unsure, so cost lands where risk is.
- **`sharded-validation-with-resume` (P6)** — run validation in named shards with persisted
  status and resume-after-timeout, plus a catch-shard, under one aggregate required check.

*A verifier that cannot fail is theater with an exit code — every check must be proven able
to fail before it counts.*

### GOVERN — hold the merge/deploy gate with human authority

- **`standing-approval-and-auto-advance` (P3)** — the ONLY governed way to thin low-risk
  approval fatigue, within named scope and with an explicit opt-out; it never covers a
  protected-branch merge or arming auto-merge, which stay human-only.
- **`merge-is-deploy-governance` (P7)** — when the platform auto-deploys on merge, treat PR
  validation as the authoritative gate, record branch-protection config in-repo, and keep a
  revert-PR rollback path.
- **`gated-deployment-prompt-template` (P11)** — a reusable operator prompt for risky
  operations with stop conditions, backup-then-verify gating, and evidence-calibrated ETAs.

### HAND OFF — transfer knowledge with evidence, before work begins

- **`lane-authoring-guide` (P10)** — a pre-work, evidence-cited authoring guide per parallel
  lane, transferring planner-to-implementer knowledge *before* the work starts.

The doctrine's answer to documentation **rot** specifically is **`docs-retention-index`
(P1)**, banked under D12.4: a numbered index that governs every workflow doc's lifecycle —
retention category, reason-to-keep, superseded-by, and cleanup rule — so retiring a document
becomes an approvable operation rather than something that never happens.

The four pillars above govern **the work** from the outside — records, proof, gates,
knowledge transfer. The two below govern **the AI's own operating environment** from the
inside: the harness it runs in, the context it is fed, the loop it executes.

### CONSTRAIN — build the operating environment so the AI cannot exceed its authority

*The harness is the contract. An agent's authority should be a property of its environment,
not of its obedience.*

- **`agent-harness-architect` (planned — D42)** — every model call passes ONE server-side
  choke point that verifies identity from credentials (never from payload) and walks a
  deny-by-default ladder (permission, entitlement, budget, input policy) before the model
  runs; the tool/provider registry is closed so an unknown capability fails closed;
  instructions are server-side versioned artifacts no untrusted party can supply; and the
  audit write is fail-closed — an action that cannot be recorded does not happen.
- **`agentic-loop-designer` (planned — D42)** — every loop has clamped iterations, typed
  retryability, and honest terminal states: a policy rejection is never retried; a failed
  check is retried once on identical input to classify flake vs deterministic; an empty
  result is a legitimate stop, never forced into output.
- **`agent-authorization-matrix` (P-existing)** — the standing human-vs-agent authority
  matrix is the policy this environment enforces; the harness is how that matrix becomes
  physics instead of promise.

### CURATE — control what enters and leaves the context; an unverified input is an unverified output

*The context window is a supply chain. Feed the model a curated diet, not access.*

- **`model-context-designer` (planned — D42)** — what enters the window is assembled
  server-side under hard caps and closed input schemas; secrets, personal data, and raw
  payloads are minimized or ride a transient never-persisted channel; what the model saw is
  reconstructible afterward; and exclusions are designed and documented, not accidental.
- **`structured-output-validator` (P-existing, extended in D42)** — nothing downstream
  trusts model output until it passes parse → strict schema → policy scan; failures are
  logged as safety evidence and rejected, never silently repaired; where possible the
  contract is encoded in types so a non-compliant output is unrepresentable.
- **`ai-evaluation-harness` (P-existing)** — the curated input diet and the output contract
  are pinned by evals, so a prompt/model/retrieval change that degrades them fails a gate,
  not a user.

## Proof from this project's own history

This library was itself built under this discipline, and its documented incidents are
evidence **for** it, not against it. Every failure the project absorbed during its own
construction traces to a single moment where the discipline was skipped:

- an **ungoverned auto-merge** that fired without human sign-off;
- **sessions acting on stale memory**, colliding on shared state;
- a **build run in the wrong directory**, against an unverified repo.

None of these were failures of effort. Each was a step trusted instead of verified. And each
is now encoded as an **eval case in a shipped governance skill** — the ungoverned-auto-merge
incident lives in `agent-authorization-matrix`'s evals; the stale-memory collisions and the
empty-directory build are likewise captured as eval cases in the startup- and
context-governance skills that halt and ask rather than trust.

The library's own scars are the doctrine's field test. It does not preach a discipline it has
not paid for.
