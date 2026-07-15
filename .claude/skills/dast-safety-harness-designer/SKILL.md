---
name: dast-safety-harness-designer
description: Design a SAFE dynamic-testing (DAST) harness against a RUNNING application — the safety harness is the deliverable, not an attack method. Mandates EXPLICIT WRITTEN AUTHORIZATION before any run (scope, target, window, blast radius recorded — composes human-approval-boundary); staging/non-production targets only unless prod is explicitly authorized; rate/impact limits so it never DoS-es the target; no destructive probes without separate sign-off; data-handling; and the run/result contract. Fail-closed: no written authorization → no run. It DESIGNS the harness; it is NOT a penetration-testing playbook and does not enumerate exploits (out of scope). Use when planning authorized dynamic testing of a running app or building the safety harness around it. Do NOT use to enumerate exploits (out of scope), define WHAT to test (threat-modeler), test tenant isolation (multi-tenant-security-tester), or scan static code (security-scan-orchestrator).
---

# DAST Safety Harness Designer

## Purpose

Dynamic testing sends real traffic at live software, so the dangerous part is
never "what do we test" — it is "did we have permission, and can the test hurt
the target or anything downstream of it." This skill designs the SAFETY HARNESS
around authorized dynamic (running-app) security testing. The deliverable has
six load-bearing parts: (1) an **explicit written authorization** recorded
before any run — scope, target, time window, intensity, and sign-off owner —
composed through `human-approval-boundary` and classified via
`change-classification-gate`; (2) a **target allowlist** of only approved
non-production/staging (or explicitly-authorized) environments; (3) **rate and
impact limits** with an abort condition so the test cannot DoS the target;
(4) a **no-destructive-probes** default, where any state-mutating test needs
separate sign-off and a rollback plan; (5) **data-handling** rules for whatever
the scan surfaces, which can itself contain secrets or PII; and (6) the
**run/result contract**. Fail-closed: no written authorization means no run.
The harness — authorization, safety, and scope — is what this skill designs.
It is NOT a penetration-testing playbook and does not enumerate exploits: WHAT
is worth testing is `threat-modeler`'s, and the attack methodology is out of
scope.

## Use When

- Use when: planning authorized dynamic (running-app) security testing and you
  need the safety/authorization harness around it.
- Use when: a DAST run is being set up and needs its scope, target allowlist,
  rate limits, and written-authorization gate defined and recorded.
- Use when: an existing dynamic-testing effort has no authorization record, no
  rate limits, or is pointed at production — bring it under a safe harness.
- Auto-invocable: it designs the harness — a plan plus a safety contract — and
  runs no scan and attacks nothing. The RUN the harness governs is gated on
  written human authorization, which this design mandates.
- Do NOT use when: the ask is to enumerate exploits or write a
  penetration-testing methodology/playbook — that is out of scope; this designs
  the SAFE HARNESS, not the attack.
- Do NOT use when: defining WHAT is worth testing — assets, boundaries, threats
  — that is `threat-modeler`; this designs the safe RUN of what it identifies.
- Do NOT use when: the target is tenant-isolation testing specifically — that is
  `multi-tenant-security-tester`.
- Do NOT use when: classifying/approving the change a DAST run represents — the
  sign-off is `human-approval-boundary` and the classification is
  `change-classification-gate`; a DAST run is a classified, approved action, and
  this harness composes both rather than restating them.
- Do NOT use when: the testing is STATIC — code/repo scanning with no running
  app — that is `security-scan-orchestrator` (whole-repo) or
  `sast-orchestration-designer` (the SAST run).

## Inputs to Inspect

1. The written authorization: does it exist, and does it state scope, target
   host(s), time window, permitted intensity, and a sign-off owner? No
   authorization → Stop Conditions (the harness may be designed; the run cannot).
2. The target environment: is it non-production/staging, or explicitly-
   authorized production? Ownership — does the requester own it or hold written
   permission to test it?
3. The blast-radius surface: state-mutating endpoints, shared databases or
   dependencies, downstream systems the target calls, and the data it holds.
4. Rate/impact tolerances: what load the target sustains before it degrades, and
   any existing rate limits or protections in front of it.
5. Data sensitivity: what real or sensitive data (PII, secrets) the scan could
   surface, and the handling/redaction/disposal rules that must apply.
6. The threat model or list of what is worth testing (`threat-modeler` output if
   present) — the harness runs the safe test of what that identifies; it does
   not re-derive the threats.

## Workflow

1. **Require and record written authorization first.** Scope, target, window,
   intensity, and sign-off — composed through `human-approval-boundary` and
   classified via `change-classification-gate`. No authorization means the
   harness may be designed but the run does not happen (fail-closed).
2. **Fix the target allowlist.** Only the explicitly-authorized hosts and
   environments are in bounds; production is excluded unless the authorization
   names it with explicit sign-off. Anything off the allowlist is out of scope.
3. **Set rate and impact limits.** Bound request rate, concurrency, and the time
   window so the test cannot DoS the target, and define the abort/kill condition
   that stops the run if the target degrades.
4. **Rule out destructive probes by default.** Non-mutating probes only; any
   destructive or state-changing test requires separate explicit sign-off and a
   rollback plan. Irreversibility is the bar, not intent.
5. **Define data-handling.** How findings, captured requests/responses, and any
   surfaced sensitive data are stored, redacted, and disposed — scan output can
   itself contain secrets and PII and is handled like production data.
6. **Define the run/result contract.** What runs, against what, when, and under
   whose authorization; the result report format; and who receives it. Findings
   go to triage/human, never auto-fixed.
7. **Design the fail-closed proofs.** Show that without valid written
   authorization the run does not start, that an off-allowlist target is
   refused, and that breaching the rate/abort limit stops the run — a safety
   control that has never blocked anything is unproven (a verifier that cannot
   fail is theater with an exit code).
8. **Yield the attack methodology.** The harness makes testing safe and
   authorized; WHICH exploits to attempt is not this skill's output — WHAT to
   test is `threat-modeler`'s, and the exploit playbook is out of scope.

## Output Format

```
DAST SAFETY HARNESS — <app / target>
Authorization (REQUIRED before any run): scope | target(s) | window | intensity | sign-off owner
  — recorded via human-approval-boundary; classified via change-classification-gate.
  NO written authorization ⇒ NO run (fail-closed).
Target allowlist: <approved hosts/envs; production EXCLUDED unless explicitly authorized>
Rate/impact limits: <request rate, concurrency, window; abort condition if the target degrades>
Destructive/state-mutating probes: <DEFAULT OFF; any such probe = separate sign-off + rollback>
Data handling: <storage, redaction, disposal of findings + any surfaced secrets/PII>
Run/result contract: <what runs, when, under whose authorization; result format; recipient>
Fail-closed proofs: <no-auth ⇒ no start; off-allowlist target refused; rate/abort breach stops run>
Yields: WHAT to test (assets/threats) → threat-modeler;
  tenant-isolation testing → multi-tenant-security-tester;
  the sign-off → human-approval-boundary; classification → change-classification-gate;
  exploit methodology → OUT OF SCOPE (this designs the safe harness, not the attack)
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Explicit WRITTEN authorization (scope/target/window/intensity/sign-off) is
      required and recorded before any run.
- [ ] Target allowlist is explicit; production is excluded unless the
      authorization names it with sign-off.
- [ ] Rate and impact limits are set with an abort condition — the scan cannot
      DoS the target.
- [ ] Destructive/state-mutating probes are off by default; any such probe has
      separate sign-off and a rollback plan.
- [ ] Data-handling is defined for findings and any surfaced secrets/PII
      (storage, redaction, disposal).
- [ ] The run/result contract is defined; findings route to triage/human, never
      auto-fixed.
- [ ] Fail-closed proofs are designed: no-auth ⇒ no run, off-allowlist target
      refused, rate/abort breach stops the run.
- [ ] The attack methodology is NOT enumerated — WHAT to test is yielded to
      `threat-modeler`; the exploit playbook is out of scope.
- [ ] `human-approval-boundary` and `change-classification-gate` are composed,
      not restated.

## Safety Rules

- Dynamic testing without explicit WRITTEN authorization is forbidden — no
  exception for urgency, "it's only staging," or "we own it but never wrote it
  down." No authorization record → no run.
- Only test systems the requester owns or holds written permission to test; an
  unauthorized DAST run against infrastructure you do not control is an attack,
  not a test.
- Production is excluded by default; testing it requires the authorization to
  name it with explicit human sign-off, plus tighter rate limits and no
  destructive probes.
- Rate and impact limits are mandatory: an unbounded dynamic scan is a
  denial-of-service against your own target.
- This skill designs SAFE, AUTHORIZED testing; it does not produce an attack
  methodology or exploit catalog — that is out of scope.

## Gotchas

- "We own it, so we don't need it in writing" is how a test takes down a shared
  staging environment nobody realized was load-bearing — the written record is
  the control, and it names the blast radius.
- DAST sends real traffic at live software: an unbounded scan is a self-inflicted
  DoS. Rate limits and an abort condition are not optional niceties.
- A staging target that shares a database or a downstream dependency with
  production has a blast radius bigger than its hostname — enumerate what the
  target calls before deciding it is safe.
- The scan OUTPUT can contain secrets or PII the app returned — captured
  requests/responses need production-grade handling, not a plaintext log.
- A destructive probe run "just to see if it works" against a shared environment
  is irreversible — destructive tests are off by default and separately signed
  off with a rollback plan.
- Designing the safe harness is not writing the exploit playbook — if the ask
  drifts into "and here is how to attack X," that is the pen-test methodology
  this skill deliberately does not produce.

## Stop Conditions

- No written authorization (scope/target/window/sign-off) exists for the run →
  the harness may be DESIGNED, but the RUN does not proceed; refuse to endorse
  or design an unauthorized run (fail-closed; composes `human-approval-boundary`).
- Asked to point DAST at production without explicit authorization and sign-off
  → refuse; production is excluded unless the authorization names it.
- Asked to enumerate exploits or produce a penetration-testing attack playbook →
  refuse; this designs the SAFE HARNESS, not the attack methodology.
- Asked to run destructive/state-mutating probes without separate sign-off and a
  rollback plan → refuse.
- The target is infrastructure the requester cannot show authorization for →
  refuse; unauthorized dynamic testing is an attack, not a test.
- A run surfaces live production secrets/PII → apply the data-handling rules and
  route to human containment (`human-approval-boundary`); do not exfiltrate.

## Supporting Files

- `evals/evals.json` — behavior cases: the bring-it-under-a-safe-harness setup,
  the shared-staging-blast-radius edge, the no-written-authorization refusal
  (fail-closed), the point-it-at-prod refusal, and the write-me-an-exploit-
  playbook should-not-do refusal.
- `evals/trigger-evals.json` — discrimination against `threat-modeler` (what to
  test vs the safe run), `multi-tenant-security-tester` (tenant-isolation
  testing), `human-approval-boundary` / `change-classification-gate` (the
  compose seams — sign-off and classification), and `security-scan-orchestrator`
  (dynamic vs static).
- No `references/` — the harness contract above is the complete procedure;
  detail lives in the produced harness design.
