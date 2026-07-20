# Check your app before you trust it

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** you built something — maybe with AI writing most of the code — and you
want to know if it's safe before real users and real data depend on it. You don't need to
know what any of the skill names below mean; each one is a specialist that explains itself
when it runs.

**How to run it:** open your project in your agent tool (Claude Code, Codex CLI, or any Agent
Skills tool) and take the steps top to bottom. For most steps, asking for what the step
describes in plain words is enough — the named skill selects itself. (Auto-selection quality
varies by tool — see the README's [tools section](../../README.md#using-aegis-with-codex-cli-and-other-agent-skills-tools).)
Two steps act on secrets, so they are deliberately never invoked
automatically: they are marked **manual-only — name it explicitly**, and you start them by
typing the skill's name.

Steps marked *"If…"* are conditional — skip them honestly when the condition doesn't apply
to your app.

## The order

1. **Map what was actually built —
   [`full-codebase-auditor`](../../.claude/skills/full-codebase-auditor/SKILL.md).**
   Yields an honest inventory of the codebase's real state, risks, and technical debt — the
   map every later step works from. Handoff: keep its risk list open; each step below picks
   up its findings.

2. **Stop the urgent leaks —
   [`secrets-identity-hardener`](../../.claude/skills/secrets-identity-hardener/SKILL.md)**
   *(manual-only — name it explicitly: it acts on secrets, so it never auto-fires).*
   Yields leaked and hardcoded credentials found, moved out of the code, and rotated — the
   bleeding-now class closed before anything slower. Handoff: any identity findings feed the
   isolation work in step 3.

   *If your app is built with Vite:* also name
   [`vite-build-qa-engineer`](../../.claude/skills/vite-build-qa-engineer/SKILL.md)
   *(manual-only — name it explicitly)*. Yields proof the shipped browser bundle itself is
   secret-free — what step 2 fixed in the source, this confirms in the artifact users
   actually download.

3. ***If your app has multiple users or customers*** *(most SaaS apps do)* — prove they
   can't see each other:

   - **Find every leak surface —
     [`tenant-isolation-reviewer`](../../.claude/skills/tenant-isolation-reviewer/SKILL.md).**
     Yields every place one customer's data could reach another. Handoff: its findings
     drive the two skills below.
   - **Audit and fix the database rules —
     [`rls-policy-auditor`](../../.claude/skills/rls-policy-auditor/SKILL.md).**
     Yields the row-security audit with the fix delivered as a reviewable migration.
   - **Make the fix un-regressable —
     [`multi-tenant-security-tester`](../../.claude/skills/multi-tenant-security-tester/SKILL.md).**
     Yields the isolation findings turned into an executable negative test suite, so a
     future change can't silently reopen the leak.

4. **Scan the whole repository —
   [`security-scan-orchestrator`](../../.claude/skills/security-scan-orchestrator/SKILL.md).**
   Yields one aggregated security-scan report across the codebase. Handoff: hand the report
   to [`static-analysis-reviewer`](../../.claude/skills/static-analysis-reviewer/SKILL.md),
   which yields the findings triaged into real-versus-noise, and to
   [`supply-chain-security-reviewer`](../../.claude/skills/supply-chain-security-reviewer/SKILL.md),
   which yields a judgment on the dependency tree your app inherited.

5. **Check what happens when it fails —
   [`error-handling-security-reviewer`](../../.claude/skills/error-handling-security-reviewer/SKILL.md).**
   Yields the fail-open paths — the catch-the-error-and-continue class AI-generated code
   loves — each one closed or explicitly accepted. Handoff: open items go on the step-7
   evidence list.

6. ***If your app has AI features*** *(a chatbot, an assistant, anything that calls a
   model)*: branch to **[Add AI features safely](add-ai-safely.md)** and run that path,
   then come back here for the close.

7. **The go/no-go —
   [`release-readiness-reviewer`](../../.claude/skills/release-readiness-reviewer/SKILL.md).**
   Yields an evidence-based GO / CONDITIONAL-GO / NO-GO on shipping, built from what the
   steps above actually found — not from anyone's assurance that it's probably fine. This
   is the close of the path.

## What this is — and isn't

This is a guided order, not a guarantee. Each skill's own output is the evidence: what it
found, what it fixed, what it left open. If a step reports findings you don't understand,
ask Claude Code to explain them in plain words before moving on — an unexplained finding is
not a cleared one.
