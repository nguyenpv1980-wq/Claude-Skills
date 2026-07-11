# Project Aegis

**Project Aegis — Shield of the agent fleet**

*Discipline before code. Evidence before merge.*

Project Aegis is an operating system for engineering software with AI — a reusable
Claude engineering shield: a library of skills, subagents, validation gates, and
safety patterns, governed by Zero Trust AI Engineering Discipline, that turns Claude
into a disciplined senior/principal engineering partner for architecture, SaaS,
security, QA, audit, troubleshooting, and AI safety.

## About

Project Aegis is a reusable Claude engineering operating system built to protect, guide,
and sharpen AI-assisted software development. It combines reusable Claude Code skills,
read-only specialist subagents, validation gates, eval conventions, and disciplined
engineering workflows so Claude operates like a senior/principal engineering partner.
The name carries three layers: the divine shield of Zeus and Athena; the Navy's Aegis,
shield of the fleet — fitting for a veteran-founded project whose operating model is a
fleet of agents; and a shield proven in use — several skills' eval cases are drawn from
real incidents this project absorbed during its own construction (an unauthorized
auto-merge, stale-memory session collisions, an empty-directory build). The goal is not
prompt bloat; it is a protected execution framework where Claude models before coding,
reads docs before implementation, tests before changes, keeps diffs small, respects
human approval boundaries, and produces evidence before closeout.

The repo is built in **phases**, each a validated batch that builds on the ones before it.
**Phase 0** established the foundation — the authoring standard, templates, eval convention,
validator, catalog, the seven read-only reviewer subagents, and the Step 0 reconciliation of
the two earlier planning tracks. On that base, **Phase 1** shipped the 8-skill AI engineering
**operating-discipline pack** (decision D4); **Phase 1.5** added the 4-skill **AI-SDLC
governance completion** (roadmap #261/#268/#279/#280), finishing the category-08 governance
layer Phase 1 began; **Phase 2** shipped the 10-skill **core architecture & engineering
pack**; **Phase 3** the 9-skill **SaaS & tenant isolation pack**; **Phase 4** the 9-skill
**security, RLS & supply-chain pack**; and **Phase 5** the 16-skill **QA, E2E, manual QA &
evidence pack** (13 canonical skills plus 3 pulled forward from the QA backlog: roadmap
#184/#185/#204).

**Phase 6** shipped the 10-skill **cloud, DevOps, reliability & release pack**; **Phase 7**
the 14-skill **AI security & LLM systems pack** (v4's 10 plus 4 OWASP LLM Top 10 gap
additions, D6); and **Phase 7.5** the **agentic AI security pack** (OWASP Agentic Top 10 for
2026, D7: 6 new skills plus 3 extensions of existing ones, with ASI08 and ASI10 merged into a
single containment reviewer).

The **Compliance & Governance batch** (D9) shipped the 9-skill **compliance pack** — ISO
27001:2022 + ISO 42001:2023 + SOC 2 with NIST AI RMF as companion: one shared control
foundation, framework projections, and a crosswalk that map controls which largely already
exist and produce auditor-grade evidence on top. The **library-meta pack (D13)** then turned
the library on itself — `skill-quality-reviewer` (D18) as the judgment layer atop the
mechanical validator, and D22's four remaining skills (`library-diff-reviewer`,
`eval-runner-designer`, `skill-usage-instrumenter`, `skill-deprecation-planner`) — so the
library now reviews its own additions and PRs, designs how its evals run, measures which
skills actually fire, and can retire a skill as deliberately as it ships one.

A run of **D12 craft packs** followed. The **operational workflow patterns pack** (D12.8, D21)
shipped the 10 evidence-extracted skills that are the concrete, invocable rules of the
**Zero Trust AI Engineering Discipline** (D16). The **data/performance/QA-validation batch**
(D23) shipped three at once — the 7-skill **D12.1 data engineering pack**, the 6-skill
**D12.3 performance engineering pack**, and the 2-skill **D10 Tier 1 performance/load
validation pair** (D12.3 designs *for* performance; D10 *measures* it). The
**product/PM/growth batch** (D24) shipped the 5-skill **D12.2 product-engineering craft
pack**, the 6-skill **D12.5 PM/product-engineering interface pack**, and the 4-skill **D12.6
growth/analytics engineering pack**. The **docs-engineering batch** (D25) shipped the 8-skill
**D12.4 technical writing / docs engineering pack**, and the **staff-IC / architecture /
framework-refresh batch** (D26) shipped the 7-skill **D12.7 staff+ IC craft pack**, the
1-skill **D12.9 architecture-advisory pack**, and the 3-skill **D14 framework-refresh /
source-currency pack**.

The **OWASP web-app gap-closure pair** (D28) closed the last two zero-coverage categories from
the D8 OWASP Top 10:2025 audit — `security-logging-alerting-architect` (A09) and
`error-handling-security-reviewer` (A10) — so all 10 web-app categories now have an owning
skill. The **SaaS architecture-depth pack** (D12.11) then completed in two builds: the
10-skill **strong cluster** (D31) and the 4-skill **low-priority set** (D32), resolving all 14
candidates and bringing the library to **175 skills**. **D33** then ran a library-wide
`skill-quality-reviewer` sweep that landed corrections only, and D34–D36 were
documentation-only — no change to the count. Most recently, **D38** added
`project-orchestrator`, the beginner-facing top-level lifecycle router that is the library's
front door (175→176), bringing it to **176 skills**.

Full per-pack detail lives in [Skills (shipped)](#skills-shipped) below; for a quick map of
what *kinds* of help the library offers, see [What's in the library](#whats-in-the-library).

## What this is

Aegis is not just a collection of skills; it is an **operating system for engineering
software with AI**. It combines (a) a library of ready-to-use skills an AI coding
assistant follows, (b) read-only specialist reviewers that give independent second
opinions, (c) validation gates and eval conventions that check the work mechanically,
and (d) — governing all of it — **Zero Trust AI Engineering Discipline**, the doctrine
that decides how everything above is allowed to operate.

The discipline's essence in one line: **"Never trust, always verify — every step of the
lifecycle. Assume drift. Demand evidence. Track everything."** It is documented at
[docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md](docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md)
and deliberately extends the Zero Trust security principle from network access to the
whole development lifecycle. The problem it solves: AI assistants confidently act on
stale memory, claim done-when-not-done, and let docs drift away from the code — this
system replaces that risk with enforced evidence at every step.

The library holds itself to the bar it enforces: `skill-quality-reviewer` (D18) reviews the
library's own additions, and its sweep corrections were applied in D33.

## The roles Aegis can play

Under the hood, Aegis is a library of 176 skills organized into 19 discipline families. In
practical terms, Aegis can make Claude act as:

| Aegis can act as… | What that means for you | Example skills |
|---|---|---|
| **an AI engineering governance lead** | Sets the rules for how humans and AI build software together — and audits that they were actually followed. | `ai-sdlc-operating-model`, `agent-governance-audit` |
| **a principal software architect** | Designs how the whole system fits together and where each new piece belongs. | `architecture-designer`, `architecture-advisor` |
| **a domain-driven design facilitator** | Turns how your business actually works into a clear model the software is built around. | `domain-modeler` |
| **a staff or principal software engineer** | Writes the code the disciplined way — tests first, small reviewable changes, honest review. | `tdd-engineer`, `code-reviewer` |
| **a SaaS platform and multi-tenancy architect** | Designs how many customers share one system without ever seeing each other's data. | `saas-platform-architect`, `tenant-isolation-reviewer` |
| **an application security and RLS specialist** | Hardens the app and locks down exactly who can read which rows in the database. | `rls-policy-auditor`, `security-pr-reviewer` |
| **a QA automation and Playwright engineer** | Builds automated tests that click through your app like a real user and catch breakage before customers do. | `playwright-e2e-engineer`, `qa-automation-architect` |
| **a cloud, DevOps and reliability architect** | Decides where and how it runs in production — and keeps it up. | `cloud-architecture-decider`, `slo-reliability-architect` |
| **an AI security and agentic-red-team architect** | Attacks your own AI features before an outsider does — prompt injection, data leaks, runaway agents. | `ai-threat-modeler`, `prompt-injection-defender` |
| **an ISO 27001, ISO 42001 and SOC 2 readiness advisor** | Gets you audit-ready for the security and AI-governance certifications enterprise customers ask for. | `iso-27001-isms-architect`, `soc2-trust-criteria-mapper` |
| **a product discovery and specification facilitator** | Interviews you to turn a vague idea into clear written requirements and a spec. | `requirements-gathering-facilitator`, `product-spec-writer` |
| **a product analytics and experimentation architect** | Decides what to measure and runs honest A/B tests, so decisions rest on evidence, not guesses. | `product-analytics-instrumenter`, `ab-test-designer` |
| **a technical writer and documentation engineer** | Writes the docs — READMEs, guides, API references — and keeps them from drifting out of date. | `readme-craftsman`, `docs-as-code-architect` |
| **a staff+ technical leadership advisor** | Brings the senior-engineer judgment call: what's worth building, how to scope it, when to say no. | `staff-scope-selector`, `tech-spec-writer` |
| **a full-codebase auditor** | Reads an entire codebase and reports its real health, risks, and technical debt. | `full-codebase-auditor`, `principal-code-analyst` |
| **a senior production troubleshooter** | When something breaks, drives from symptom to root cause instead of guessing. | `systematic-debugger`, `incident-response-runbook` |

You never have to pick from this list yourself — Aegis selects and coordinates the right role
for each step. Not a developer? See [From idea to shipped: the no-experience
path](#from-idea-to-shipped-the-no-experience-path) for the guided path that puts the right
one to work for you.

## The discipline behind it: Zero Trust AI Engineering Discipline

Security taught the industry its hardest lesson decades ago: never trust by default —
verify everything. We call it Zero Trust, and nobody serious argues with it anymore. Then
AI-assisted development arrived and quietly reintroduced blind trust everywhere: trust in
the AI's "done", trust in its summaries of what it changed, trust in the docs it says it
updated. **Zero Trust AI Engineering Discipline** applies "never trust, always verify" to
the entire development lifecycle — every completion claim, test result, and line of
documentation is checked against reality before it is believed.

Why adopt it? Because unverified AI work fails in two quiet ways: **drift** — docs and
plans slowly stop describing what the code actually does — and **rot** — tests and
safeguards silently decay until the day you need them. The discipline is how you get AI's
speed *without* inheriting its silent decay. Every skill in this library is built to
operate under it. In practice it comes down to six rules:

- **"Done" isn't done until it's verified** — a completion claim is checked against the
  real repo and the real test run, never taken on faith.
- **Demand evidence, not assertion** — a summary saying it works is not proof it works.
- **Assume drift** — docs and memory are probably slightly stale until reconciled against
  reality; check by default instead of waiting for proof they're wrong.
- **Small, reviewable changes — nothing smuggled in** — diffs stay small enough for a
  human to genuinely review, and contain exactly what they claim to.
- **A human is the gate** — the AI proposes; a person approves the merge. Always.
- **Track every decision** — dated, written down, never rewritten.

> **"Never trust, always verify — every step of the lifecycle."**
> *Assume drift. Demand evidence. Track everything.*

The full doctrine:
[docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md](docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md).

## From idea to shipped: the no-experience path

You do not need to be a developer to use this. You do not need to know a single skill name, or
what "RLS" or "CI" or "architecture" means. If you have a real problem and the patience to
answer questions about your own business, Aegis supplies the engineering discipline to take you
from that idea to a working, shipped product.

**The deal, stated plainly.** You bring the business truth — the problem, how your business
actually works, who's involved, what "done" looks like, and the decisions only you can make.
Aegis brings the engineering — the questions you didn't know to ask, the technical translation,
the architecture, the security, the tests, the reviews, and the evidence that it all works. You
are never asked to know a technical term. You are asked to know your business, and to decide.

**The one prompt to start.** Paste this into Claude Code (see [Getting started](#getting-started)
for how to get it running first). This one message is the whole on-ramp:

> "I have an idea for an application, but I'm not a developer and I don't know what questions I
> should be asking. Guide me from the idea through requirements, design, development, testing,
> security review and deployment. Ask me one plain-language question at a time. Don't expect me
> to know technical terminology — select and coordinate the right expertise yourself, explain
> decisions in business language, bring me in when a human decision or approval is needed, and
> never move to coding until the earlier stage is confirmed."

You don't have to name a skill: `project-orchestrator` picks this up automatically, works out
where your project is, and drives the rest.

**What it actually feels like.** A short, real exchange — not the whole interview, just enough to
show the shape of it:

> **You:** "I run a small maintenance company. We use text messages and spreadsheets to assign
> work. Jobs get missed, technicians lose instructions, and customers keep calling for updates. I
> think I need an app, but I don't know how to build one."
>
> **Aegis:** "Before we decide what to build, I'll help you understand the problem — who
> experiences it, what happens today, and what success would change. One question at a time, no
> technical terms needed. Walk me through what happens today when a customer calls with a request,
> from the phone call to the job being finished."
>
> *…several plain-language questions later, a technical decision arrives as a business question:*
>
> **Aegis:** "When you send a customer a link to check their job's status, should that link
> expire after 30 days, stay available indefinitely, or stop working once the job is closed?"

Notice the last one. Under the hood that is a decision about scoped, revocable access links — but
you are never asked to design that. You are asked the business question: how long should a
customer be able to see their job? You answer in the language of your business; Aegis handles the
engineering it implies.

**The nine stages, in plain language.** Every project walks the same path. At each stage Aegis
does the engineering work and brings you the decisions that are genuinely yours:

1. **Understand the problem** — Aegis interviews you; you describe how the business really works
   and what success would change.
2. **Define the product** — what's in the first version, and what's deliberately left out for
   later. You approve the scope.
3. **Design the system** — the structure, the data, who can see what. You approve the tradeoffs in
   business terms: cost, time, risk.
4. **Design the security** — keeping each customer's data separate, how customer links work,
   uploads, AI safety. You choose the business behavior (for example, how long a customer link
   stays alive).
5. **Plan the build** — the work is broken into small, demonstrable releases. You approve the
   order things get built.
6. **Build each slice** — docs first, tests first, small reviewable changes, security review,
   evidence at every step. You approve anything irreversible before it happens.
7. **Test and accept** — automated tests, plus a short list of real-world scenarios for a human to
   walk through. Aegis writes the step-by-step instructions; you (or a business tester on your
   team) follow them.
8. **Prepare to deploy** — hosting, cost, uptime, backups, and a way to undo a bad release. You
   answer the business questions: how much downtime can you tolerate, what monthly cost is
   acceptable?
9. **Decide to release** — independent reviewers check the architecture, security, testing and
   readiness, and you get a plain-language **GO / CONDITIONAL GO / NO-GO** with the evidence behind
   it. **You** authorize the release. Aegis never merges or deploys on its own.

**What you decide vs. what Aegis decides.** The line is bright, and it is the point of the whole
system: you own the business decisions, Aegis owns the engineering ones — and always tells you
their cost, time, and risk so you can judge:

| You decide (the business) | Aegis decides (the engineering) — and explains in business terms |
|---|---|
| What goes in the first release | The data architecture and how records relate |
| Whether a completed job can be reopened | Retry and failure behavior when something goes wrong |
| Who can see what | How access control is implemented and enforced |
| How customers are notified | Caching, performance, and reliability targets |
| Your pricing tiers | The CI pipeline and how each change is validated |
| Whether to accept a known risk | Infrastructure layout and AI rate limits |
| The final authorization to deploy | The test strategy and what it covers |

You are never asked to choose the right-hand column. But you are always told what it costs you in
money, time, or risk — so the business decisions on the left are made with real information.

**One honest line.** This doesn't remove the need for judgment, it doesn't guarantee your product
will succeed in the market, and it doesn't take you out of the loop — you remain the person who
says yes. What it does is make sure that when you say yes, you're saying it to work that was done
with discipline and backed by evidence.

## How to use this

### Getting started

Step 1 gets you the repo; then pick the option that matches how you work. Options 1–5 all
run Claude Code; Option 6 is the honest fallback for when you can't run Claude Code at all.

**Step 1 — get the repo** (every option starts here):

You'll need a terminal for this step (a window where you type commands). On Windows: press
the Windows key, type "terminal", press Enter. On Mac: press Cmd+Space, type "terminal",
press Enter. If typing `git` in it says the command isn't found, install Git first from
[https://git-scm.com/downloads](https://git-scm.com/downloads).

```bash
git clone https://github.com/nguyenpv1980-wq/Project-Aegis.git
cd Project-Aegis
```

`git clone` copies the library to your machine; `cd` puts you in the folder every option
below starts from. Later, run `git pull` from the same folder to update to the latest skills.

**One engine, many surfaces.** Claude Code is one engine available on several surfaces —
the terminal, VS Code (and forks like Cursor and Windsurf), JetBrains IDEs, a Desktop app,
and the web. The skills in `.claude/skills/` load the same way on every local surface, so
pick whichever matches how you work. The current full list is at
[https://code.claude.com/docs/en/platforms](https://code.claude.com/docs/en/platforms).

**Option 1 — Claude Code CLI (terminal, any OS, works alongside any editor).**

1. Install Claude Code — follow the install steps on the official docs at
   [https://code.claude.com/docs](https://code.claude.com/docs). It requires a Claude
   subscription (Pro/Max/Team/Enterprise) or Console API access. (Install commands change
   over time; the official page is always current, so we link instead of copying them here.)
2. From the cloned repo folder, run:

   ```bash
   claude
   ```

3. That's the whole setup. Claude Code auto-discovers everything under `.claude/` — the 176
   skills and 7 subagents load automatically. There is no registration step.
4. **How you invoke a skill** — skills are trigger-invoked, not slash-commanded. You invoke
   one by *describing a task that matches its trigger*, or by *naming it*. Two literal
   prompts to type at the Claude Code prompt:
   - "I want to build a new feature but the requirements are vague — use the
     requirements-gathering-facilitator skill to run discovery with me."
   - "Review this diff for tenant-isolation problems." (no skill named — the matching skill
     is selected from the task itself)
5. Leaving and coming back: `claude --continue` resumes your most recent session in this repo.

**Option 2 — VS Code — and Cursor, Windsurf, VSCodium (any VS Code fork).**

1. Install the official **Claude Code** extension by Anthropic: open the Extensions view
   (`Ctrl+Shift+X` / `Cmd+Shift+X`), search "Claude Code", and install the one from verified
   publisher Anthropic.
2. **File → Open Folder** → the cloned `Project-Aegis` folder. Claude Code works on the
   workspace root, so the skills under `.claude/` are picked up from there.
3. Open the panel via the Spark icon in the editor toolbar (or Command Palette →
   "Claude Code"). First launch signs you in via your browser.
4. Type the same trigger-style prompts as in Option 1 — the extension and the CLI are the
   same Claude Code. Prefer a terminal? Open the integrated terminal
   (`` Ctrl+` `` / `` Cmd+` ``) and run `claude` there instead.
5. **Using a fork like Cursor or Windsurf?** The steps above are identical — forks install
   the same Anthropic extension the same way. One distinction, stated plainly: the skills
   are used by **Claude Code**, not by the fork's own AI. Cursor's native chat/Composer
   does *not* auto-load `.claude/skills/` — pasting a `SKILL.md` into it works only as a
   manual procedure, same as Option 6.

**Option 3 — JetBrains IDEs (IntelliJ, PyCharm, WebStorm, Rider…).**

1. Install the Claude Code CLI **first** — the JetBrains plugin does not bundle it; it
   connects to the CLI you install. Follow the install steps at
   [https://code.claude.com/docs](https://code.claude.com/docs) (same as Option 1, step 1).
2. In the IDE: **Settings → Plugins → Marketplace**, search "Claude Code" (by Anthropic),
   click **Install**, then restart the IDE.
3. **Open** the cloned `Project-Aegis` folder as the project. The plugin connects to the
   CLI, shows Claude's changes in the IDE's own diff viewer, and shares your current
   selection — prompt the same way as in Option 1.

Any other editor (Neovim, Emacs, Sublime, classic Visual Studio…): no plugin needed — open
a terminal in the repo folder and type `claude`.

**Option 4 — Claude Code Desktop app (no terminal at all).** The same engine in a graphical
app — visual diff review, parallel sessions, and not a command line in sight. Install it
from [https://claude.ai](https://claude.ai) (current platforms listed at
[https://code.claude.com/docs](https://code.claude.com/docs)), open the cloned
`Project-Aegis` folder, and type the same prompts as in Option 1. For people who never want
to see a terminal.

**Option 5 — Claude Code on the Web (zero install).**
[claude.ai/code](https://claude.ai/code) runs Claude Code on Anthropic's servers against a
Git repository — point it at your fork of this repo (or any repo you've copied skills
into) and prompt the same way, with nothing installed; it works from a browser and the iOS
app. One honest caveat: it works on the cloud copy of the repository, not on the files on
your machine.

**Option 6 — Claude.ai / the Claude apps (no Claude Code at all).** Without Claude Code you don't get
automatic `.claude/` discovery — but the skills are just Markdown procedures, so you can
still use them. Open the `SKILL.md` you want (from GitHub or a local clone) and paste its
content into your project's custom instructions / project knowledge, or reference the pattern
directly in the conversation. This gives you the procedure and its discipline; it does
**not** give you the automatic trigger selection, the read-only subagents, or the CI
validator — those are Claude Code features.

**Using the skills in your own project.** Copy the `.claude/skills/<name>/` folders you want
into your own repo's `.claude/skills/` — Claude Code discovers them there exactly the same
way. If your repo has no `.claude/skills/` folder yet, create it first (it's just a folder).
Literal copy commands, run from inside the cloned `Project-Aegis` folder — swap
`tdd-engineer` for the skill you want and the path for your own repo:

On Windows (PowerShell):

```powershell
Copy-Item -Recurse .claude\skills\tdd-engineer C:\path\to\your-repo\.claude\skills\tdd-engineer
```

`Copy-Item -Recurse` copies the skill's folder and everything inside it into your repo.

On macOS/Linux:

```bash
cp -r .claude/skills/tdd-engineer /path/to/your-repo/.claude/skills/
```

`cp -r` is the same copy on Mac and Linux (`-r` means "include everything inside the folder").

[`docs/skill-generation-standard.md`](docs/skill-generation-standard.md) defines the
format if you want to write your own.

**Your first session — from a vague idea.** If you're not a developer and you have an idea but
no idea what to do first, name the front door: `project-orchestrator`. It works out where your
project is, asks you one plain-language business question at a time, routes each step to the
right skill for you (no skill name needed), keeps a human as the approval gate on anything
irreversible, and records the decisions in a `docs/project-state.md` so you can stop and resume
anytime. Literal first prompt to paste:

> "I run a maintenance company and jobs keep getting missed — I think I need an app but I'm not
> a developer and don't know where to start. Use the project-orchestrator skill to guide me."

`project-orchestrator` opens your project by handing the discovery step to
`requirements-gathering-facilitator`. If you already KNOW you need the requirements interview,
you can name that skill directly instead:

> "I'm starting a new feature. Use the requirements-gathering-facilitator skill: interview
> me with structured questions until we have a requirements brief, then hand off to
> product-spec-writer."

From there the natural chain is `requirements-gathering-facilitator` → `product-spec-writer`
→ the architecture and tech-spec skills (`architecture-designer`, `tech-spec-writer`) → build,
with the discipline skills below enforcing the loop — and `project-orchestrator` walking you
across the whole chain if you'd rather not track it yourself.

**Run the core loop.** Every change, large or small, follows the same rhythm:

1. **Classify the change** — what kind of change is this, and what validation and
   approval path does that class require?
2. **Verify against evidence** — run the checks; never assume state from memory.
3. **Keep the diff small and reviewable** — one intent, exact files, nothing smuggled in.
4. **A human approves the merge** — the assistant proposes; a person decides.
5. **Record the decision** — a dated entry in the planning record, so history never
   drifts.

This loop is not overhead layered on top of the discipline; it **is** the discipline in
practice.

**Follow the non-negotiable operating rules** (full text with rationales in
[CONTRIBUTING.md](CONTRIBUTING.md)): evidence before merge; one session per repo at a
time; no auto-merge — the human is the gate; and every decision tracked as a dated
entry in the reconciliation doc.

**What a change looks like.** One realistic pass through the loop:

> A developer asks for a new feature. The assistant classifies the change and locks the
> scope, then composes the relevant shipped skills — say, domain modeling, test-first
> implementation, and a security review matching the change class. It produces a small
> diff with passing tests as evidence and opens a pull request, which the validator
> gates in CI. A human reviews and merges. The decision lands as a dated entry in the
> planning record.

## Map of the system

- **Skills** ([`.claude/skills/`](.claude/skills/)) — the 176 shipped procedures: 19
  discipline families, fronted by `project-orchestrator`, the beginner-facing router that
  walks a non-developer through them from idea to shipped. See **[What's in the
  library](#whats-in-the-library)** below for the roster (each family, its purpose, and
  example skills), and [Skills (shipped)](#skills-shipped) for the full per-skill tables.
- **Subagents** — seven read-only specialist reviewers, one per lens; see
  [Subagents (read-only reviewers)](#subagents-read-only-reviewers).
- **The planning record**
  ([`docs/reconciliation/step-0-reconciliation-v4.md`](docs/reconciliation/step-0-reconciliation-v4.md))
  — the dated decisions (D1–D38) in §5 are the project's immutable decision log; the
  D12/D14 candidate scopes recorded there are banked-but-not-built future
  work (the D12.8 pack graduated from banked to built with D21; the D13
  library-meta scope completed with D22).
- **The doctrine**
  ([docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md](docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md))
  and **the operating rules** ([CONTRIBUTING.md](CONTRIBUTING.md)) — why the system
  works this way, and the eight enforceable rules every session follows.
- **Validation + CI** — the local structural gate ([Validation](#validation)) and the
  merge gate ([CI (merge gate)](#ci-merge-gate)).

## What's in the library

**Skill roles at a glance.** The 176 skills sit in **19 discipline families** (each a shipped
build batch), fronted by one beginner-facing orchestrator. This is the scannable map of what
*kinds* of help exist; the full per-skill tables are in [Skills (shipped)](#skills-shipped) below.

**Start here — `project-orchestrator` (the front door).** If you're a non-developer with an
idea and no idea what to do first, this is the one skill to name. It isn't a 20th family — it's
the navigator *above* the other 19: it works out which stage your project is in, routes you to
the right skill below (you never need its name), turns every technical choice into a
plain-language business question, records each dated decision in a `docs/project-state.md`, and
keeps a human as the approval gate on anything irreversible. See
*[Your first session](#getting-started)* for the opening prompt.

1. **Operating discipline** *(Phase 1, 8)* — the always-on rules that keep AI-assisted work
   honest: classify before acting, verify against evidence, keep diffs small, halt for
   approval, close out honestly. *e.g.* `change-classification-gate`, `human-approval-boundary`,
   `reviewable-diff-discipline`, `ai-closeout-reporter`.
2. **AI-SDLC governance** *(Phase 1.5, 4)* — the human+agent lifecycle contract: named stages
   and gates, standing agent authority, memory governance, after-the-fact process audit.
   *e.g.* `ai-sdlc-operating-model`, `agent-authorization-matrix`, `agent-memory-governance`,
   `agent-governance-audit`.
3. **Core architecture & engineering** *(Phase 2, 10)* — modeling and building systems well:
   domain models, architecture design, ADRs, docs-first + test-first implementation, debugging,
   code review. *e.g.* `domain-modeler`, `architecture-designer`, `adr-writer`, `tdd-engineer`,
   `systematic-debugger`.
4. **SaaS & tenant isolation** *(Phase 3, 9)* — multi-tenant foundations: platform structure,
   tenant semantics, per-store scoping, roles/permissions, plans, audit trail, cost, external
   API contracts. *e.g.* `saas-platform-architect`, `tenant-isolation-reviewer`,
   `authorization-matrix-designer`, `audit-log-architect`, `api-event-architect`.
5. **Security, RLS & supply chain** *(Phase 4, 9)* — hands-on appsec: threat modeling, RLS
   policy audit, secrets hardening, supply-chain review, security PR review, migration safety,
   SAST triage. *e.g.* `threat-modeler`, `rls-policy-auditor`, `secrets-identity-hardener`,
   `supply-chain-security-reviewer`, `security-pr-reviewer`.
6. **QA, E2E & evidence** *(Phase 5, 16)* — test strategy through execution and proof: QA
   strategy, test plans, coverage mapping, Playwright/unit/build QA, flake control, test data,
   evidence policy. *e.g.* `qa-strategy-architect`, `test-coverage-mapper`,
   `playwright-e2e-engineer`, `flaky-test-detective`, `screenshot-evidence-planner`.
7. **Cloud, DevOps, reliability & release** *(Phase 6, 10)* — running it in production: cloud
   choice, Azure/AWS mapping, IaC review, CI pipelines, release readiness, rollback,
   observability, SLOs, incidents. *e.g.* `cloud-architecture-decider`, `iac-reviewer`,
   `release-readiness-reviewer`, `rollback-runbook-author`, `slo-reliability-architect`.
8. **AI security & LLM systems** *(Phase 7, 14)* — securing LLM features against the OWASP LLM
   Top 10: injection, RAG/tool safety, output handling, evals, cost guardrails, disclosure,
   routing. *e.g.* `ai-threat-modeler`, `prompt-injection-defender`, `rag-security-architect`,
   `ai-evaluation-harness`, `ai-cost-guardrail-designer`.
9. **Agentic AI security** *(Phase 7.5, 6)* — the OWASP Agentic Top 10 risks layered on top of
   the LLM ones: goal hijack, agent identity/privilege, memory poisoning, inter-agent comms,
   containment, human-trust. *e.g.* `agent-goal-hijack-defender`,
   `agent-identity-privilege-reviewer`, `memory-context-poisoning-reviewer`,
   `agent-containment-reviewer`.
10. **Compliance & governance** *(D9, 9)* — auditor-grade readiness for ISO 27001 / ISO 42001 /
    SOC 2 (+ NIST AI RMF): one control foundation, framework projections, a crosswalk, evidence,
    gap audit. *e.g.* `compliance-control-foundation`, `multi-framework-crosswalk`,
    `compliance-gap-auditor`, `soc2-trust-criteria-mapper`.
11. **Library meta / self-application** *(D13, 5)* — the library applied to itself: quality
    review, whole-PR review, eval-execution design, usage instrumentation, deprecation planning.
    *e.g.* `skill-quality-reviewer`, `library-diff-reviewer`, `eval-runner-designer`,
    `skill-deprecation-planner`.
12. **Operational workflow patterns** *(D12.8, 10)* — the concrete, invocable rules of the
    **Zero Trust AI Engineering Discipline**: approval registers, CI-mirror preflight,
    risk-tiered + sharded validation, merge-is-deploy governance. *e.g.*
    `scoped-approval-register`, `local-ci-mirror-preflight`, `risk-tiered-validation-selector`,
    `merge-is-deploy-governance`.
13. **Data + performance engineering & load validation** *(D23, 15)* — the data plane and its
    speed: schema evolution, streaming, data quality, warehouse/lake, PII; profiling, query
    plans, N+1, caching, latency; plus perf/load test harnesses. *e.g.*
    `schema-evolution-planner`, `pii-lifecycle-designer`, `query-plan-reader`,
    `n-plus-one-detector`, `load-test-planner`.
14. **Product, PM & growth** *(D24, 15)* — turning product intent into shippable, measured work:
    requirements elicitation feeding specs, then prioritization, flag-gated rollout, and
    analytics instrumentation — see *Your first session* in
    [Getting started](#getting-started) for the entry-point walkthrough.
    *e.g.* `requirements-gathering-facilitator`, `product-spec-writer`,
    `prioritization-frame-picker`, `feature-flag-rollout-strategist`, `event-schema-architect`,
    `ab-test-designer`.
15. **Docs engineering** *(D25, 8)* — durable documentation as a discipline: README craft,
    ADR-corpus sequencing, Diátaxis organization, the docs-as-code pipeline, generated API
    reference, onboarding. *e.g.* `readme-craftsman`, `diataxis-doc-organizer`,
    `docs-as-code-architect`, `api-doc-generator-designer`, `onboarding-doc-designer`.
16. **Staff+ IC, architecture advisory & framework refresh** *(D26, 11)* — technical leadership
    and currency: tech specs, design review, dependency negotiation, promotion/scope, the
    architecture-style advisor, framework-edition tracking. *e.g.* `tech-spec-writer`,
    `design-review-facilitator`, `staff-scope-selector`, `architecture-advisor`,
    `framework-edition-tracker`.
17. **OWASP web-app gap closure** *(D28, 2)* — the two web-app categories that previously had no
    owner: security logging/alerting design (A09) and error-path security review (A10). *e.g.*
    `security-logging-alerting-architect`, `error-handling-security-reviewer`.
18. **SaaS architecture depth — strong cluster** *(D31, 10)* — deep multi-tenant surfaces: the
    command gateway, realtime, background jobs, horizontal scaling, search, file storage, usage
    metering, synthetic monitoring, offline-first, admin console. *e.g.*
    `command-gateway-architect`, `realtime-subscription-architect`,
    `background-job-orchestration-architect`, `admin-console-architect`.
19. **SaaS architecture depth — low-priority set** *(D32, 4)* — the scale-stage partitioning
    surfaces: cell-based architecture, OLTP sharding, a below-tenant scope axis, and guest
    share-link access. *e.g.* `cell-based-architecture-designer`,
    `data-partitioning-sharding-strategist`, `intra-tenant-scope-architect`,
    `share-link-access-architect`.

## Start here (canonical reading order)

1. [`docs/reconciliation/step-0-reconciliation-v4.md`](docs/reconciliation/step-0-reconciliation-v4.md) — what was reconciled and why (read first).
2. [`docs/research/claude-skills-architecture-audit-findings-v4.md`](docs/research/claude-skills-architecture-audit-findings-v4.md) — canonical architecture audit.
3. [`docs/prompts/claude-skills-master-generation-prompts-v4.md`](docs/prompts/claude-skills-master-generation-prompts-v4.md) — canonical master + phase prompts.
4. [`docs/300-repeatable-software-saas-skills-roadmap.md`](docs/300-repeatable-software-saas-skills-roadmap.md) — the strategic backlog / capability map (the original 300; per the D12 standing rule a 300+ target backlog — ship on demand and framework coverage, not count).
5. [`docs/skills/`](docs/skills/) — category-level backlogs.
6. [`docs/skills-catalog.md`](docs/skills-catalog.md) — implemented vs. backlog, priorities, skills-vs-agents.
7. [`docs/skill-generation-standard.md`](docs/skill-generation-standard.md) — the authoring standard the validator enforces.

**Historical / reference inputs** (superseded by the v4 pair + reconciliation; retained for provenance):

- [`docs/prompts/senior-principal-claude-skills-execution-plan.md`](docs/prompts/senior-principal-claude-skills-execution-plan.md) — earlier combined execution plan (now historical).
- `docs/research/claude-skills-principal-architecture-findings.md`
- `docs/prompts/master-claude-skills-and-agents-development-prompt.md`
- `docs/prompts/phased-claude-skills-prompts.md`
- `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md`
- `docs/150-claude-skills-roadmap.md` (superseded by the original 300-skill roadmap — per the D12 standing rule a 300+ target backlog, not a cap)

## Reconciled phase plan (single source of truth)

The v4 phase structure is canonical. See [the reconciliation doc](docs/reconciliation/step-0-reconciliation-v4.md) §3
for the per-phase skill lists and how the older execution-plan names merge in.

| Phase | Pack | Priority | Status |
|---:|---|---|---|
| 0 | Foundation: standard, templates, eval convention, validator, catalog, README, 7 subagents, `_template` | P0 | ✅ merged |
| 1 | AI engineering **operating-discipline** pack (8 skills) | P0 | ✅ merged |
| 1.5 | AI-SDLC **governance completion** (4 skills: roadmap #261/#268/#279/#280) | P0/P1 | ✅ merged |
| 2 | Core architecture & engineering (10) | P0 | ✅ merged |
| 3 | SaaS & tenant isolation (9) | P0/P1 | ✅ merged |
| 4 | Security, RLS & supply chain (9) | P0/P1 | ✅ merged |
| 5 | QA, E2E, manual QA & evidence (16 = 13 canonical + 3 pulled forward from the QA backlog: roadmap #184/#185/#204) | P0/P1 | ✅ merged |
| 6 | Cloud, DevOps, reliability & release (10) | P1 | ✅ merged |
| 7 | AI security & LLM systems (14 = v4's 10 + 4 OWASP LLM Top 10 additions, D6) | P1 | ✅ merged |
| 7.5 | Agentic AI security (OWASP Agentic Top 10, D7: 6 new + 3 extensions) | P1 | ✅ merged |
| D9 | Compliance & Governance batch (9 = 3 shared foundation + 3 framework projections + 3 cross-cutting; ISO 27001 + ISO 42001 + SOC 2, NIST AI RMF companion) | P1 | ✅ merged |
| D13 | Library meta / self-application (5 = `skill-quality-reviewer`, D18, + the 4 completing the scope: `library-diff-reviewer`, `eval-runner-designer`, `skill-usage-instrumenter`, `skill-deprecation-planner`, D22) | P1 | ✅ shipped (D18 + D22) |
| D12.8 | Operational workflow patterns (10 evidence-extracted skills — the concrete rules of the Zero Trust AI Engineering Discipline, D16/D21; sourced from the workflow extraction report) | P1 | ✅ shipped (D21) |
| D23 | Data + performance + QA-validation batch (15 = D12.1 data engineering 7 + D12.3 performance engineering 6 + D10 Tier 1 perf/load validation 2; D12.3 designs FOR performance, D10 measures it — seam pinned both sides) | P1 | ✅ shipped (D23) |
| D24 | Product / PM / growth batch (15 = D12.2 product-engineering craft 5 + D12.5 PM/product-engineering interface 6 + D12.6 growth/analytics engineering 4; two hard seams — `product-spec-writer`≠`adr-writer`, `sunset-deprecation-communicator`≠`skill-deprecation-planner` — and the two three-way event/analytics seams pinned in trigger-evals) | P1/P2 | ✅ shipped (D24) |
| D25 | Docs engineering batch (8 = D12.4 technical writing / docs engineering; `adr-sequencer` extends `adr-writer`, `docs-retention-index`≠`skill-deprecation-planner` pinned both ways, `api-doc-generator-designer`≠`api-event-architect`) — PART A of the D12.4+D12.7+D12.9+D14 two-PR batch, 140→148 | P1 | ✅ shipped (D25) |
| D26 | Staff-IC / architecture / framework-refresh batch (11 = D12.7 staff+ IC craft 7 + D12.9 architecture-advisor 1 + D14 framework refresh 3) — PART B of the D12.4+D12.7+D12.9+D14 two-PR batch, 148→159. Seams: `tech-spec-writer`≠`adr-writer`, `phased-work-handoff-designer`≠`ai-closeout-reporter`≠`ai-sdlc-operating-model`, `architecture-advisor`≠`architecture-designer`, D14 detect→propose→human-review | P2 | ✅ shipped (D26) |
| D28 | OWASP web-app gap-closure pair (2 = `security-logging-alerting-architect` closes A09:2025 + `error-handling-security-reviewer` closes A10:2025 — the D8 audit's two zero-coverage categories; all 10 OWASP web-app categories now owned), 159→161. Seams: A09 skill ≠ `audit-log-architect`/`observability-operator`/`slo-reliability-architect`/`incident-response-runbook`; A10 skill ≠ `security-pr-reviewer`/`appsec-implementer`/`static-analysis-reviewer`/`error-taxonomy-designer` | P1 | ✅ shipped (D28) |
| D31 | SaaS architecture depth — D12.11 STRONG cluster (10 = `command-gateway-architect`, `realtime-subscription-architect`, `background-job-orchestration-architect`, `horizontal-scalability-reviewer`, `search-architecture-designer`, `file-upload-storage-architect`, `usage-metering-and-cost-attribution-pipeline-designer`, `synthetic-monitoring-architect`, `offline-first-sync-architect`, `admin-console-architect`), 161→171. Hard-pinned seams: usage-metering ≠ `saas-cost-architect` (pipeline vs cost model), background-job ≠ `streaming-event-architect` (execution vs transport), realtime ↔ offline-first (online push vs offline sync, in-batch); `command-gateway-architect` enforces `authorization-matrix-designer`'s policy. usage-metering resolved STANDALONE. The 4 low-priority D12.11 candidates remain unbuilt (Build B). | P1 | ✅ shipped (D31) |
| D32 | SaaS architecture depth — D12.11 LOW-PRIORITY set (4 = `cell-based-architecture-designer`, `data-partitioning-sharding-strategist`, `intra-tenant-scope-architect`, `share-link-access-architect`), 171→175. Completes the D12.11 pack (all 14 candidates resolved: 10 strong D31 + 4 low-priority D32). Both flags resolved STANDALONE: `intra-tenant-scope-architect` ≠ `multi-tenant-data-architect` (subordinate per-user scope axis vs the tenant_id axis), `share-link-access-architect` ≠ `authorization-matrix-designer` (bearer-capability guest access vs member RBAC). Seams also pinned: cell-based ≠ `saas-platform-architect`/`architecture-advisor`/`agent-containment-reviewer`; sharding ≠ `multi-tenant-data-architect`/`warehouse-lake-architect`/`operational-vs-analytical-splitter`. | P2 | ✅ shipped (D32) |
| D38 | Beginner-facing lifecycle orchestrator / library front door (1 = `project-orchestrator`), 175→176. The top-level navigator that takes a non-developer from a vague idea to a shipped product: runtime stage detection + next-skill routing along existing seams + plain-language business-question translation + a persistent dated `docs/project-state.md`. Composes `ai-sdlc-operating-model`'s stage-gate map (**cited, never copied** — the anti-duplication condition) and keeps the human as the approval/merge gate via `human-approval-boundary` + `change-classification-gate` + `agent-authorization-matrix`. Defers elicitation to `requirements-gathering-facilitator`, team-policy authoring to `ai-sdlc-operating-model`. | P1 | ✅ shipped (D38) |
| 8 | Backlog expansion in ≤20-skill validated batches | P2 | backlog |

## Subagents (read-only reviewers)

Real project subagents live under `.claude/agents/<name>.md` (reconciled decision D2),
read-only by default. Each maps to a v4 orchestrator role (see reconciliation §5):

| Subagent | Lens |
|---|---|
| `principal-architecture-reviewer` | Architecture boundaries, coupling, data ownership, scalability. |
| `secure-saas-reviewer` | Tenant isolation, RLS, authz, secrets, cross-tenant leakage. |
| `qa-automation-lead` | Test strategy, coverage gaps, flake risk, release evidence. |
| `full-codebase-auditor` | Whole-repo inventory, evidence-based risk, debt map. |
| `senior-troubleshooting-lead` | Reproduction, hypothesis ranking, root cause. |
| `ai-security-red-team-reviewer` | Prompt injection, tool/RAG abuse, data exfil. |
| `release-readiness-reviewer` | CI/build/test evidence, migrations, rollback, go/no-go. |

## Skills (shipped)

**Start here — the beginner's front door** (D38; full detail:
[`docs/skills-catalog.md`](docs/skills-catalog.md)):

| Skill | What it does | Invocation |
|---|---|---|
| `project-orchestrator` | The top-level, beginner-facing navigator: takes a non-developer from a vague idea to a shipped product. Detects the current lifecycle stage (reads `docs/project-state.md` + inspects the repo), routes to the owning stage skill by name, turns every technical decision into one plain-language business question, and records each dated decision in `docs/project-state.md`. Keeps a human as the approval/merge gate on every irreversible step — composes `ai-sdlc-operating-model`'s stage-gate map (cited, never copied), `change-classification-gate`, `human-approval-boundary`, `agent-authorization-matrix`. Defers the requirements interview to `requirements-gathering-facilitator` and team-policy authoring to `ai-sdlc-operating-model`. | auto + manual |

Phase 1 — AI engineering operating-discipline pack, under `.claude/skills/<name>/`
(full detail: [`docs/skills-catalog.md`](docs/skills-catalog.md)):

| Skill | What it does | Invocation |
|---|---|---|
| `agent-startup-context-gate` | Verifies repo identity and loads governing context before any work; halts when the location can't be verified (a path that exists is not proof it's the right repo). | auto + manual |
| `source-of-truth-reconciler` | Resolves conflicts between instructions, docs, code, tests, and memory by evidence-cited precedence; surfaces every assumption. | auto + manual |
| `change-classification-gate` | Classifies a change before work → validation floor + approval path; locks scope to the approved class. | auto + manual |
| `human-approval-boundary` | Halts for explicit approval before schema, RLS/security, prod-data, secrets, deploy, billing, or destructive work; stops when security impact is unclear. | auto + manual |
| `reviewable-diff-discipline` | Keeps diffs small and intentional; stages exact files only; staged set must equal declared intent. | auto + manual |
| `ai-closeout-reporter` | Terminal closeout report with a mandatory "intentionally not done / omitted" section — scope reductions are never silent. | auto + manual |
| `agent-failure-recovery` | Preserve-first recovery from broken git/tree state; destructive cleanup only with backup + explicit approval. | **manual only** |
| `agent-instruction-consolidator` | Aligns CLAUDE.md / AGENTS.md / Cursor / Copilot instruction files to one canonical source with rule-preservation proof. | **manual only** |

Phase 1.5 — AI-SDLC governance completion (roadmap #261/#268/#279/#280; completes the
category-08 layer Phase 1 started — composes the Phase 1 skills, never restates them):

| Skill | What it does | Invocation |
|---|---|---|
| `ai-sdlc-operating-model` | End-to-end human+agent lifecycle contract: named stages with entry/exit gates, per-stage authority (human / agent / agent-with-approval), enforcing skill per stage, failure routing, learning loop; grounded in observed PR practice with a gap list. | auto + manual |
| `agent-authorization-matrix` | Deny-by-default action × context matrix of standing agent authority — merge to protected branches requires a named human always; auto-merge arming is forbidden to agents (armed state re-checked after every push); approval scope/expiry semantics; proposal-first. | **manual only** |
| `agent-memory-governance` | Persistent-memory WRITE/TRUST/HYGIENE rules: confirmed durable facts with provenance and absolute dates, never secrets; remembered repo/PR state verified against live git/gh before acting; disposition-approved cleanups. | **manual only** |
| `agent-governance-audit` | Audits one AI-assisted change's process compliance from primary evidence (PR timeline incl. who armed auto-merge, commits, CI runs): per-control PASS/FAIL/UNVERIFIABLE verdicts; closeout claims cross-checked; missing evidence is never a PASS. | auto + manual |

Phase 2 — core architecture & engineering pack:

| Skill | What it does | Invocation |
|---|---|---|
| `domain-modeler` | Domain model from requirements/code — language, bounded contexts, aggregates with invariants; hard "do not code yet" gate at the end. | auto + manual |
| `architecture-designer` | Inspects the CURRENT architecture first, then component/dependency/data-ownership maps, tradeoffs, ADR draft, and an incremental migration plan. | auto + manual |
| `adr-writer` | Architecture Decision Records with honest alternatives, consequences, operational impact, mandatory rollback/reversal plan and review date. | auto + manual |
| `docs-first-implementer` | Pins the exact installed library version (lockfile), reads version-matching docs before coding, verifies with real commands; declares uncertainty instead of guessing. | auto + manual |
| `tdd-engineer` | Strict red-green-refactor: confirms each test fails for the intended reason before the minimal implementation; reports exact commands and results. | auto + manual |
| `systematic-debugger` | Reproduce → reduce → isolate → fix one thing → verify → prevent; prediction-tested hypotheses, single-variable fixes, regression test kept. | auto + manual |
| `code-reviewer` | Reviews actual diffs only — severity-ranked findings with file:line evidence and remediation; no diff, no review. | auto + manual |
| `code-simplifier` | Behavior-preserving simplification with the suite green before and after every move; coverage gate; restraint ("not done" list) is a deliverable. | **manual only** |
| `principal-code-analyst` | Subsystem-level strategic analysis laddering code findings to architecture, security, cost; risk register + small-step remediation with validation signals. | auto + manual |
| `full-codebase-auditor` | Whole-repo audit with inventory-first coverage; findings filed as confirmed / likely / hypotheses / missing information. (Skill = procedure; same-named subagent composes it.) | auto + manual |

Phase 3 — SaaS & tenant isolation pack:

| Skill | What it does | Invocation |
|---|---|---|
| `saas-platform-architect` | Platform structure: per-component pooled/siloed/bridge decisions with named isolation mechanisms, control-plane/data-plane split, capability inventory, rollout plan with per-step rollback. | auto + manual |
| `tenant-modeler` | Tenant semantics: definition, hierarchy, membership-as-entity (roles on membership), invitations, ownership, and a lifecycle state machine with per-state access/data/billing/jobs posture. | auto + manual |
| `tenant-isolation-reviewer` | Reviews real systems for cross-tenant leakage across all 15 surfaces (identity → audit, incl. AI retrieval); evidence-cited findings, isolation test matrix, negative tests, honest not-inspected list. | auto + manual |
| `multi-tenant-data-architect` | Per-store tenant scoping decisions (incl. caches, search, vector stores), server-derived tenant-context propagation, ownership map, expand→contract migration with verification and rollback. | auto + manual |
| `authorization-matrix-designer` | Deny-by-default roles × permissions × resources matrix, object-level rules, enforcement-point map, brokered support access, negative tests, additive role migration. | auto + manual |
| `plan-entitlement-architect` | Plan × entitlement matrix with one resolution point enforced uniformly on every surface; metering hooks; plan transitions with no silent data loss; grandfathering + rollback. | auto + manual |
| `audit-log-architect` | Audit event taxonomy, versioned record schema, append-only integrity with explicit write-failure policy, retention/redaction, tenant-scoped access, negative tests. | auto + manual |
| `saas-cost-architect` | Bill-grounded cost drivers, per-tenant attribution (or admitted overhead), distribution-based unit economics vs revenue, exposure math, guardrails with observe-first rollout. | auto + manual |
| `api-event-architect` | External API/event contracts: credential-derived tenant context, idempotency, per-tenant/plan rate limits, versioning with dual-run deprecation, tenant-scoped signed webhooks. | auto + manual |

Phase 4 — security, RLS & supply-chain pack:

| Skill | What it does | Invocation |
|---|---|---|
| `threat-modeler` | Design-time threat model: assets/actors/trust-boundaries, STRIDE per boundary, abuse cases, exploit-path-gated severity, mitigations mapped to negative tests; consumes tenant/authz outputs instead of re-deriving them. | auto + manual |
| `appsec-implementer` | Implements one NAMED security control test-first — negative test red→green, minimal server-side control, scoped diff, residual risk stated. | **manual only** |
| `multi-tenant-security-tester` | Executable cross-tenant/authorization negative suite: two-tenant fixtures, forbidden-action-denied assertions, positive controls, IDOR/list/mass-assignment/exports/jobs, honest coverage. | auto + manual |
| `rls-policy-auditor` | Per-command RLS audit/authoring (merges rls-policy-author + rls-negative-test-designer): recursion, unsafe SECURITY DEFINER, broad grants, missing tenant scope, service-role leakage, frontend-derived scope; mandatory negative-test plan; policies delivered as a migration, never run live. | auto + manual |
| `secrets-identity-hardener` | Env classification (catches VITE_/NEXT_PUBLIC_ leaks), moves secrets server-side with a client-bundle-absence proof, rotates leaked credentials, least-privilege service accounts, session/token flags. | **manual only** |
| `supply-chain-security-reviewer` | SLSA-style: lockfile-based dependency set, reachability triage of scanner output, install/build-script and CI compromise paths, SHA pinning, compromise-path-gated severity. | auto + manual |
| `security-pr-reviewer` | Security lens on an actual diff: authz/object-level/tenant-scope, injection, secrets, SSRF, control-weakening detection; exploit-path-gated findings; no diff, no review. | auto + manual |
| `secure-migration-reviewer` | Whole-migration deploy safety: RLS/policy gaps, GRANT widening, unsafe defaults, destructive/irreversible ops, tenant-scoped backfills, lock risk, expand→contract deploy order, rollback; delegates policy text to `rls-policy-auditor`. | auto + manual |
| `static-analysis-reviewer` | Triages SAST/CodeQL/SARIF on first-party code: dedup, confirm-against-code disposition (TP/FP/dup/accepted), five-axis ranking (reachability/exploitability/asset/tenant/business), written suppression policy. | auto + manual |

Phase 5 — QA, E2E, manual QA & evidence pack (13 canonical + 3 pulled forward from the
QA backlog, roadmap #184/#185/#204):

| Skill | What it does | Invocation |
|---|---|---|
| `qa-strategy-architect` | Product-level QA strategy: ranked risk inventory → cheapest-reliable-layer decisions, explicit automation/manual split, evidence per change class, CI gates, ownership. | auto + manual |
| `test-plan-designer` | Per-change test plan: risk-traced items with layer/data/environment, objective entry/exit criteria, named artifacts and CI placement, explicit out-of-scope list. | auto + manual |
| `test-coverage-mapper` | Coverage audit: surface inventory first, maps tests by reading assertions (theater ≠ coverage), risk-ranked gaps with cheapest fill layer, honest not-inspected list. | auto + manual |
| `qa-automation-architect` | Automation blueprint: tools per layer with rationale, structure/fixtures/auth-state, parallel-safe isolation, CI tiers with bounded logged retries, flake policy, migration steps. | auto + manual |
| `playwright-e2e-engineer` | Critical-journey Playwright specs: role/label locators, web-first assertions, zero sleeps/networkidle, storageState per persona, failure traces, honest run reports. | **manual only** |
| `clickthrough-test-engineer` | Pre-planned interactive walkthrough of a running app (forms with invalid input, dialogs, permissions, states, console), severity-rated defects with masked evidence, honest coverage. | **manual only** |
| `manual-test-case-creator` | Stranger-executable manual cases: exact data/roles/environment, one observable expected result per step, screenshot checkpoints, verdict rules, cleanup. | auto + manual |
| `screenshot-evidence-planner` | Evidence policy: risk-justified checkpoints, deterministic naming, mandatory pre-storage masking, metadata, storage/retention classes, case/PR/closeout linkage. | auto + manual |
| `vitest-unit-component-engineer` | Vitest unit/component tests: intentional node-vs-DOM environment per file, owned-seam mocks, Testing Library queries, determinism, real run output. | **manual only** |
| `vite-build-qa-engineer` | Build-artifact QA: `VITE_` env classification, dist-level secret proof, build/preview parity (base, deep links, modes), bundle budgets, sourcemap policy. | **manual only** |
| `flaky-test-detective` | Classify → reproduce with counts → fix ONE cause → prove stability; no retries/sleeps/weakened assertions; product races routed as product bugs; quarantine with owner/ticket/expiry. | auto + manual |
| `test-data-architect` | Test-data design: read-only persona/baseline catalog, per-layer sources, determinism, worker-scoped isolation, synthetic-only PII posture, cleanup + seed evolution. | auto + manual |
| `regression-suite-curator` | Evidence-based promote/retain/demote/retire with written rationale, protected security regressions, enforced quarantine registry, tier-budget fit. | auto + manual |
| `integration-test-designer` | (pulled forward, #184) The layer between unit and E2E: real service/command/DB/auth/permission boundaries, named faked seams, persisted-state assertions, no browser. | auto + manual |
| `api-contract-test-designer` | (pulled forward, #185) Contract verification: provider/consumer roles, schema + error-envelope validation, additive-vs-breaking CI gate, version coverage; design stays with `api-event-architect`. | auto + manual |
| `accessibility-test-harness` | (pulled forward, #204) WCAG-pinned a11y harness: automated scans (baseline+ratchet) AND manual keyboard/focus/contrast/screen-reader checklists; honest about automation limits. | auto + manual |

Phase 6 — cloud, DevOps, reliability & release pack (`rollback-strategy-designer`
merged into `rollback-runbook-author` per reconciliation §3):

| Skill | What it does | Invocation |
|---|---|---|
| `cloud-architecture-decider` | Cloud-neutral platform decision: nine-axis requirements record, provider-neutral logical architecture, isolation/compliance hard filters before scoring, managed-vs-self-hosted with the operational bill, exit costs and reopen triggers. | auto + manual |
| `azure-saas-architect` | Maps a decided logical architecture to provider-idiomatic Azure: Entra ID/managed identities/OIDC, VNets + Private Link, per-store tenant isolation, compute by team maturity, Azure Policy/Defender posture, Bicep/Terraform, tag-keyed cost controls; SKU/limit/price claims become verification items. | auto + manual |
| `aws-saas-architect` | Maps a decided logical architecture to provider-idiomatic AWS: Organizations/SCPs, IAM roles + OIDC, VPC/PrivateLink, per-store tenant isolation, compute by team maturity, Security Hub/GuardDuty posture, Terraform/CDK, cost-allocation tags; quota/type/price claims become verification items. | auto + manual |
| `iac-reviewer` | Review-only IaC audit with blast radius first: destructive replaces, public exposure, IAM width deltas, secrets in code and state, tenant-isolation impact, drift, pinning, cost flags; never applies or runs plan against live backends. | auto + manual |
| `ci-pipeline-architect` | Pipeline stage graph with blocking semantics and a latency budget, CI secret governance (OIDC over stored keys, fork-PR posture), artifact provenance, promotion gates with named humans, branch-protection alignment; composes qa-automation-architect tiers. | **manual only** |
| `release-readiness-reviewer` | Evidence-based ship/no-ship gate: every dimension cites a verifiable artifact or is MISSING; CI evidence pinned to the release SHA; unknown = No-Go with the evidence that flips it. (Skill = procedure; same-named subagent composes it.) | auto + manual |
| `rollback-runbook-author` | Rollback strategy + stranger-executable runbook in one artifact: decision criteria with time-box, per-layer primitives in order, bad-window data repair, rehearsal log and staleness triggers; authors only, never executes. | auto + manual |
| `observability-operator` | Hands-on observability: structured redacted instrumentation, truthful health checks, alerts with severity/owner/runbook-link/justified threshold, query-verified claims, silences only with owner+expiry. | **manual only** |
| `slo-reliability-architect` | Journey-derived SLOs: symptom-based SLIs with measurement points, error budgets in user units, burn-rate paging with cause-alert demotion, budget policy with consequences, per-tenant reliability views. | auto + manual |
| `incident-response-runbook` | Incident machinery: one-minute severity ladder, IC/comms/ops roles, triage to decision points, containment invoking the rollback artifact by reference, tenant-aware comms, blameless postmortem where every finding lands as a test/alert/fix or owned risk. | auto + manual |

Phase 7 — AI security & LLM systems pack (14 = v4's 10 + 4 OWASP LLM Top 10 gap
additions, D6). Anchored to the OWASP Top 10 for LLM Applications (2025); these
skills **compose** the shipped tenant/security/cost/governance packs rather than
re-deriving them. **LLM03** is extend-existing (the shipped
`supply-chain-security-reviewer` was extended to models/datasets/adapters);
**LLM10** DoS/denial-of-wallet is baked into `ai-cost-guardrail-designer`;
`ai-evaluation-harness` absorbs the AI security test harness:

| Skill | What it does | Invocation |
|---|---|---|
| `ai-threat-modeler` | AI-specific threat model: AI assets + trust boundaries (all untrusted content), per-boundary threats anchored to the OWASP LLM Top 10, abuse cases, exploit-path-gated severity, each mitigation mapped to an owning skill + red-team case; composes `threat-modeler` for the classic surface. | auto + manual |
| `prompt-injection-defender` | Layered injection defense (LLM01): trust zones, the untrusted-content invariant, content/instruction separation, and the primary layer — deterministic action authorization OUTSIDE the model; direct + indirect payloads; red-team suite with SAFE-outcome assertions. | **manual only** |
| `rag-security-architect` | RAG/vector-store security (LLM08): authorization AT RETRIEVAL TIME (never post-filter), per-tenant index scoping, document-ACL propagation, embedding risks (inversion/membership/poisoning/stale-permission); composes `tenant-isolation-reviewer` + `multi-tenant-data-architect`. | auto + manual |
| `agent-tool-safety-guard` | Least-privilege tool access (LLM06): per-tool blast-radius matrix, calling-user authority (no service-account confused deputy), argument validation before execution, approval gates on irreversible actions, tool-chain abuse; composes `human-approval-boundary` + `agent-authorization-matrix`. | auto + manual |
| `llm-output-safety-reviewer` | Output-handling review (LLM05): model output as untrusted data to render/execute/URL/tool/store sinks (XSS/RCE/SSRF/injection/second-order), context-correct encoding, generated-code sandboxing; exploit-flow-gated findings. | auto + manual |
| `ai-evaluation-harness` | Versioned eval dataset (representative + adversarial/red-team + regression), per-dimension graders + thresholds (quality/schema/safety/grounding/injection/latency/cost), CI regression gate; absorbs the AI security test harness; honest real-run reporting. | **manual only** |
| `ai-cost-guardrail-designer` | Consumption guardrails (LLM10 DoS/denial-of-wallet): per-request token caps, tenant-scoped budgets/rate limits, agent loop/recursion bounds, fail-safe degraded mode + kill switch, burn-rate alerts before exhaustion; composes `saas-cost-architect` + `observability-operator`. | auto + manual |
| `ai-governance-risk-reviewer` | AI governance/risk posture: impact-based risk tiering, oversight-to-tier matching, accountable ownership, AI disclosure/consent, model/feature card, obligation→control mapping (EU AI Act tiers, NIST AI RMF) without asserting legal conclusions. | auto + manual |
| `ai-router-architect` | Centralized model-routing layer: one interface, server-side-only credentials, task/cost routing, choke-point cost enforcement, per-call telemetry, resilient fallback + circuit breaker + no-deploy kill switch, idempotent retries; composes `secrets-identity-hardener` + `observability-operator`. | **manual only** |
| `structured-output-validator` | Output-shape contract (LLM05 companion): schema (fields/types/enums/ranges), validate-before-use, semantic checks beyond shape (tenant-scoped ids), bounded failure handling; shape-is-not-safety handoffs to `llm-output-safety-reviewer` + `agent-tool-safety-guard`. | auto + manual |
| `sensitive-disclosure-guard` | (NEW, LLM02) Disclosure defense: data-minimization + pre-model redaction of secrets/PII/other-tenant data, output-path echo/bleed checks, log redaction at emission, provider retention/training posture; composes `tenant-isolation-reviewer` + `secrets-identity-hardener`. | auto + manual |
| `model-poisoning-reviewer` | (NEW, LLM04) Training/feedback/ingestion integrity: contributor-trust assessment, poisoning paths, feedback-loop Sybil defense, ingestion-as-truth integrity, provenance/holdout controls; acquire-vs-ingest boundary with `supply-chain-security-reviewer`. | auto + manual |
| `system-prompt-leakage-reviewer` | (NEW, LLM07) Two axes: no secrets in the prompt AND no security dependence on prompt secrecy — **system prompts are NOT security controls**; enforcement is deterministic and lives OUTSIDE the LLM; extraction-is-harmless framing. | auto + manual |
| `ai-misinformation-guard` | (NEW, LLM09) Grounding in retrieved sources (not memory), citation-to-claim verification, calibrated uncertainty/refusal, fact validation before action, package/API hallucination (slopsquatting) checks, overreliance-aware UX. | auto + manual |

Phase 7.5 — agentic AI security pack (6 new + 3 extensions). Anchored to the
OWASP Top 10 for Agentic Applications (2026), ASI01–ASI10, per reconciliation
§3 (D7). The Agentic Top 10 **extends** the LLM Top 10: agent systems inherit
every Phase 7 risk; this pack adds autonomy, tool, identity, memory, and
multi-agent risks on top. **ASI08+ASI10 merged** into one
`agent-containment-reviewer` (D7). **Extensions (scoped diffs, not new
skills):** `agent-tool-safety-guard` extended for ASI02 + the tool-side slice
of ASI05 (tool misuse, side-effect limits, code-execution tool class);
`llm-output-safety-reviewer` extended for ASI05 (autonomous generate-and-run
loops, ephemeral sandboxes, NL-to-execution paths);
`supply-chain-security-reviewer` extended again (after D6/LLM03) for ASI04
(MCP servers/manifests, tool/skill registries, plugins, A2A dependencies):

| Skill | What it does | Invocation |
|---|---|---|
| `agent-goal-hijack-defender` | (ASI01) Goal/plan integrity for multi-step agents: pinned goal record outside the model context, principal-only mutation channel, per-step tracing, deviation detection, drift response, per-channel hijack red-team suite; builds on `prompt-injection-defender` (LLM01 owns the vector). | **manual only** |
| `agent-identity-privilege-reviewer` | (ASI03) Agent identity architecture: distinct least-privilege identity per agent, task/time-scoped credentials, delegation chains that attenuate (never amplify), confused-deputy closure, dual attribution (principal + agent); complements `secrets-identity-hardener`. | auto + manual |
| `memory-context-poisoning-reviewer` | (ASI06) Persistent memory poisoning review: write-path trust, validation-before-write, provenance, tenant/user/session scoping at write AND recall, TTL + purge with rollback, recalled memory as data never instructions; distinct from `model-poisoning-reviewer` (LLM04) and `rag-security-architect` (LLM08). | auto + manual |
| `inter-agent-comms-reviewer` | (ASI07) A2A/MCP message security: per-edge mutual authn, end-to-end integrity, replay bounds, confidentiality, topology allowlists, spoofed results; authenticated ≠ trusted — peer messages never re-task or assert authority. | auto + manual |
| `agent-containment-reviewer` | (ASI08+ASI10 merged) Cascade half: blast-radius isolation, bounded upstream trust, circuit breakers, checkpoints/rollback, retry-storm limits. Rogue half: drift baselines, agent inventory/lifecycle, kill switches that SEVER AUTHORITY (credentials revoked, not processes killed); composes `ai-cost-guardrail-designer` + `incident-response-runbook`. | auto + manual |
| `human-agent-trust-reviewer` | (ASI09) Adversarial review of the approval layer: consent fatigue (rate/latency signals), self-reported summaries vs system-verified facts, bundling, urgency manipulation, automation-bias controls; counterpart to `human-approval-boundary`. | auto + manual |

Compliance & Governance batch (D9) — ISO 27001:2022 + ISO 42001:2023 + SOC 2,
with NIST AI RMF 1.0 as voluntary companion. Architecture: **one shared
control foundation + framework projections + a crosswalk** — not three
parallel skill sets. The batch **maps controls that largely already exist**
(Phases 3/4 technical controls, the Phase 5 evidence pack, Phase 1.5 +
Phase 7 AI governance) and produces auditor-grade evidence on top. Every
skill encodes the D9 precision flags (SOC 2 = AICPA **attestation**, never
certification; Annex A counts secondary-sourced/conflicting — verify before
citing; ~60–80% overlap = industry estimate) in a Compliance Precision
Rules section:

| Skill | What it does | Invocation |
|---|---|---|
| `compliance-control-foundation` | One framework-agnostic control catalog (access control, crypto, change mgmt, logging/monitoring, incident response, vendor mgmt, risk assessment + AI governance): each control written once with objective, owner, mechanism mapped by name to shipped skills, evidence hook, honest status. | auto + manual |
| `compliance-evidence-collector` | Operating-effectiveness evidence OVER TIME (SOC 2 Type 2's core demand, reused for ISO surveillance): per-control cadence matched to operating frequency, populations for sampling, retention/integrity, window-coverage matrix with holes; never mutates a live evidence store. | auto + manual |
| `statement-of-applicability-author` | The ISO-mandatory SoA serving both 27001 and 42001: per-control include/exclude justified by 6.1.3 risk-treatment traces, controlled-document diffs, licensed-Annex-A-only rows — never reconstructed from memory. | auto + manual |
| `iso-27001-isms-architect` | ISMS clauses 4–10 (incl. Amd 1:2024 climate-relevance check), four-theme Annex A selection via the foundation; headline net-new = risk register, internal audit program, management review cadence; readiness plan, never a certification claim. | auto + manual |
| `iso-42001-aims-architect` | AIMS clauses 4–10 + AI risk assessment (6.1.2/8.2), AI risk treatment (6.1.3/8.3), AI system impact assessment (6.1.4/8.4 — individuals/societies); maps the Phase 1.5 governance pack as operational mechanisms; Annex A counts never stated (sources conflict). | auto + manual |
| `soc2-trust-criteria-mapper` | SOC 2 scoping as ATTESTATION (never certification): system boundary, commitment-driven TSC category selection (Security baseline + optional four), Type 1 vs Type 2 with window feasibility, subservice carve-outs; Type definitions flagged CPA-firm-sourced. | auto + manual |
| `multi-framework-crosswalk` | One control → 27001 Annex A + SOC 2 TSC + 42001 Annex A (+ AI RMF function): edition-pinned, text-in-hand cells only, FULL/PARTIAL(residue) honesty, explicit joint sets — the do-the-work-once engine. | auto + manual |
| `compliance-gap-auditor` | ONE parameterized gap audit vs chosen framework(s): MET/PARTIAL/GAP/UNVERIFIABLE per requirement from cited evidence (missing evidence is never MET), blockers-first remediation order; readiness assessment, never an audit opinion. | auto + manual |
| `ai-lifecycle-risk-manager` | NIST AI RMF GOVERN/MAP/MEASURE/MANAGE operationalized across the AI lifecycle with owners, triggers, and a risk register; voluntary and under revision — never a certification target; companion to `iso-42001-aims-architect`. | auto + manual |

D13 — library meta / self-application (D18 + D22): the library applies its
own discipline to itself, end to end. All five are pure review/design
skills (verdicts, specs, plans — none edits anything) → model-invocable.
`skill-quality-reviewer` **composes** `scripts/validate-skills.py` as its
entry gate; `library-diff-reviewer` composes `skill-quality-reviewer` as
its single-skill inner loop (the seam pinned at D18, now owned from both
sides); `skill-usage-instrumenter` produces the evidence package
`skill-deprecation-planner` consumes; `docs-retention-index` (the
DOC-lifecycle twin, D12.4) stays banked with the SKILL-vs-DOC seam pinned
in trigger-evals:

| Skill | What it does | Invocation |
|---|---|---|
| `skill-quality-reviewer` | The judgment layer above the mechanical validator: validator-first gate, then the seven checks it cannot script — trigger quality (trigger-oriented vs merely descriptive), trigger collision against the full shipped corpus (colliding skills NAMED), duplication/extension (the LLM03/ASI04 precedent), eval integrity (boundary cases vs hollow filler), section substance (Stop Conditions that actually refuse), scope discipline, invocation posture. Per-check PASS/CONCERN/FAIL with quoted evidence → ship / revise / reject / make-it-an-extension. | auto + manual |
| `library-diff-reviewer` | Reviews a whole library-changing PR end-to-end: fresh validator evidence pinned to the PR head, registration consistency (placement, post-merge voice, banked-candidate graduation, count arithmetic at every site), collision sweep against the shipped corpus AND in-batch siblings, diff coherence, per-skill quality via `skill-quality-reviewer` as the inner loop → one approve/request-changes verdict; performs no platform action (no merge, no auto-merge arming). | auto + manual |
| `eval-runner-designer` | Designs how the eval corpus would actually EXECUTE — per-case-type semantics (fresh isolated session; refusal cases fire AND refuse), pairwise discrimination scoring, deterministic-vs-LLM-judge assertion routing with JUDGE-ERROR honesty, UNRUN-default reporting, cost/sampling tiers, flake policy, advisory-first CI. Design/spec only: never claims a runner exists or that evals pass. | auto + manual |
| `skill-usage-instrumenter` | Designs the usage-evidence layer: invocation signals (auto vs explicit, coarse enums — never prompt content or user identifiers), wrong-fire/correction events, never-fired lists over a stated window, evidence tiers, thresholds naming an action AND consumer, and the rare-but-critical exemption so low usage alone never condemns a safety-net skill. Adds no hooks; edits nothing. | auto + manual |
| `skill-deprecation-planner` | Plans a skill's staged retirement: qualifying trigger (superseded + coverage diff / absorbed / evidenced disuse / defect), reverse-link sweep with a disposition per inbound reference, mark → redirect-window → remove with rollback per stage (squash removal reverts as one ordinary commit), registration rows moved to a retired record. Plan only; every stage is human-approved. | auto + manual |

D12.8 — operational workflow patterns (D21): the 10 evidence-extracted
patterns from the read-only audit of two production multi-agent repositories
([extraction report](docs/research/aegis-workflow-extraction-report.md)) —
the concrete, invocable rules of the
[Zero Trust AI Engineering Discipline](docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md)
(D16), product-agnostic with identifiers templated as placeholders:

| Skill | What it does | Invocation |
|---|---|---|
| `scoped-approval-register` | Durable append-style record of every granted approval — Status / Reason / Scope allowed / Scope FORBIDDEN / Evidence — with supersede-never-rewrite lifecycle and deny-by-default citation; composes `human-approval-boundary` (which decides WHERE approval is required). | auto + manual |
| `standing-approval-and-auto-advance` | Governed anti-approval-fatigue: named-scope standing approval for the mechanical loop, phase-advance only into already-approved phases, per-session restatement, explicit opt-out, reviewer-block path; merge-after-green strictly opt-in (never default); never covers protected-branch merge or arming auto-merge — rationale anchored to the ungoverned-auto-merge incident. | **manual only** |
| `chat-backlog-reconciliation` | Cadenced extraction of chat-only decisions/bugs/backlog into dated repo docs, each item audited against PR/source evidence (completed/partial/active/not-active/unknown); chat "done" caps at unknown without repo proof. | auto + manual |
| `context-co-update-ci-gate` | CI gate failing PRs that touch important paths without a context-map update (declared, reviewable no-op hatch — never silent) + the honest-update protocol (date+SHA stamps, evidence-only status moves, risk notes never deleted without proof); write-back half of `agent-startup-context-gate`. | auto + manual |
| `lane-authoring-guide` | Pre-work, evidence-cited guide per parallel agent lane — lifecycle slice, contracts, per-unit recipe/checklist, explicit "must NOT do" boundary; mutually exclusive lanes; authored at work's BEGINNING (the closeout owns the end). | auto + manual |
| `local-ci-mirror-preflight` | Per-commit CI mirror: derive local equivalents of every PR-triggered check from workflow files, baseline on clean mainline first (separate git worktree), classify failures PR-caused / pre-existing / CI-infra / cannot-determine; declared docs-only path. | auto + manual |
| `risk-tiered-validation-selector` | Fail-closed classifier: changed files → validation depth (docs-only / fast / full) with never-docs-only + forced-full lists, max-over-files aggregation, diffable rules; routes validation COST where `change-classification-gate` routes APPROVAL. | auto + manual |
| `sharded-validation-with-resume` | Full tier as named functional shards: persisted status (failed ≠ interrupted), resume only past timeout/infra interruptions (never past real failures), empty-or-fail uncategorized catch-shard, ONE aggregate gate as the sole required check. | auto + manual |
| `merge-is-deploy-governance` | Standing governance for merge==deploy platforms: documented reality, PR validation as the authoritative gate, post-merge demoted to verification, branch protection recorded in-repo (human-only changes), stated exposure window, revert-PR rollback with strategy-correct mechanics. | auto + manual |
| `gated-deployment-prompt-template` | Reusable operator prompt for recurring risky ops: placeholders only, hard rules with required inputs, stop conditions with safe halt states, backup-then-verify gating, per-phase smoke expectations, required per-run report, history-index-anchored ETAs; uncited claims labeled "unverified". | auto + manual |

D12.1 — data engineering pack (D23): multi-tenant operational + analytical
data as a first-class discipline; the internal-pipeline-vs-external-contract
seam against `api-event-architect` is pinned both ways:

| Skill | What it does | Invocation |
|---|---|---|
| `schema-evolution-planner` | Staged expand→migrate→contract plans for live-store schema change: per-stage old×new compatibility guarantees, consumer enumeration incl. events and analytics extracts, verification gates, deprecation register, rollback per stage; runbook and safety review handed off. | auto + manual |
| `streaming-event-architect` | INTERNAL event/stream backbone: per-flow stream-vs-queue, keys with honest ordering scope, at-least-once + idempotent consumers ("exactly-once" interrogated), DLQ with owner and replay, retention vs compaction, event-schema compatibility, CDC; external webhooks/feeds stay with `api-event-architect`. | auto + manual |
| `data-quality-monitor-designer` | Data-content checks across six dimensions placed at ingest/transform/serving, each with severity, owner, and block/quarantine/alert-and-pass — never silent auto-fix; per-dataset quality SLAs; wiring handed to `observability-operator`. | auto + manual |
| `operational-vs-analytical-splitter` | Decides which workloads leave the transactional store and how (replica / CDC / materialized views / cache) against owner-stated freshness tolerance, with the one-bad-query escape, a stop-doing list with enforcement, and staged cutover. | auto + manual |
| `warehouse-lake-architect` | Analytical estate design: warehouse/lake/lakehouse by workload and team maturity, zones with contracts, modeling + SCD policy per mart, tenant key mandatory in every zone, PII per lifecycle rules, catalog governance, cost posture. | auto + manual |
| `pii-lifecycle-designer` | Personal-data lifecycle estate-wide: classification, per-store data map incl. logs/caches/vector stores/backups/vendors, minimization, retention with mechanics, propagating erasure with an honest backup stance, re-identification checks, residency. | auto + manual |
| `data-migration-runbook-author` | Operator-executable data-move runbooks: plan + safety review + VERIFIED backup as prerequisites, signal-tuned batching with idempotent resume, per-batch verification with expected outputs, numeric abort criteria naming safe halt states, human-approved no-return points. Authors documents; executes nothing. | auto + manual |

D12.3 — performance engineering pack (D23): these skills design FOR
performance; the D10 pair below MEASURES it (seam pinned both sides):

| Skill | What it does | Invocation |
|---|---|---|
| `profiling-methodology-designer` | Where-does-time-go methodology: attribution level first (low utilization = waiting → off-CPU), measurement conditions with an overhead budget, narrowing loop with stop rule and ruled-out register, handoff map to the narrow tools. Production attach approval-gated; fixes nothing. | auto + manual |
| `query-plan-reader` | ONE query's plan → ranked verdict: dominant cost node, estimate-vs-actual divergence first, sargability rewrites, composite indexes priced in write amplification, tenant/row-security predicate cost read, re-verification at representative volume. | auto + manual |
| `n-plus-one-detector` | Chatty data-access patterns (N+1, repeated identical, serial awaits, over-fetch) evidenced by per-request counts, fixed by pattern with request-scoped loaders (a tenant-leak boundary), guarded by query-count budgets in tests; refuses the cache-the-storm reflex. | auto + manual |
| `caching-strategy-designer` | What/where/how-it-stays-correct caching: written consistency envelope per item, invalidation before shipping with backstop TTLs, tenant-qualified keys, stampede and cold-start protection, failure semantics, hit-ratio targets with a removal trigger; authorization results never cached by default. | auto + manual |
| `latency-budget-architect` | End-to-end target → per-hop budgets with closing arithmetic: overhead rows, honest fan-out tail math, timeouts DERIVED from budgets with cascade checks, explicit headroom, the budget-claim review rule; consumes SLO targets, never sets them. | auto + manual |
| `frontend-perf-engineer` | The browser's share: metrics pinned to a device/network class, deletion-first weight audit, splitting with a floor, asset/font strategy, SSR/hydration honesty, evidence-based runtime fixes, bundle-size and metric budgets as CI gates. | auto + manual |

D10 Tier 1 — performance/load validation (D23): the QA roadmap's headline
pair; both MEASURE (pre-release validation counterpart to
`slo-reliability-architect`'s production targets), and neither runs against
production without explicit human approval:

| Skill | What it does | Invocation |
|---|---|---|
| `performance-test-harness` | The measurement instrument: per-surface measured set, environment contract stamped on every result, baselines + variance-derived noise bands (single-run diffs banned), thresholds CONSUMED from budget/SLO owners, CI tiers with advisory→blocking promotion, UNRUN as a first-class status. | auto + manual |
| `load-test-planner` | The traffic plan: workload model from production evidence (write share explicit, arrival model chosen), whale + long-tail tenant mix with the noisy-neighbor scenario judged per-tenant, volumes with skew, load/stress/soak/spike by question, ramps with abort criteria, owner-cited pass/fail. | auto + manual |

D12.2 — product engineering craft (D24): the API/UX craft INSIDE the
contract that `api-event-architect` owns (the craft details, not the
contract itself):

| Skill | What it does | Invocation |
|---|---|---|
| `pagination-cursor-designer` | The pagination MECHANISM inside a contract: cursor (keyset) vs offset with drift/deep-page costs stated, opaque versioned cursor (sort key + tiebreaker), strict total ordering, page-size bounds, honest end signaling, the tenant/permission predicate bound server-side (a cross-tenant paging boundary), surface pattern chosen. | auto + manual |
| `error-taxonomy-designer` | The error MODEL: a finite taxonomy with stable machine codes, one envelope (code/message/details/correlation-id/retryable), an honest client-vs-server-vs-retryable split, actionable messages, ONE exception→taxonomy boundary, and a disclosure rule keeping stack traces/internals/PII out. | auto + manual |
| `edge-state-ux-designer` | The per-view non-happy-path state matrix: the three distinct empties (first-run/filtered/error), honest loading (skeleton vs spinner, delay threshold, optimistic rollback), error placement by blast radius, partial failure, refetch/offline, forbidden-not-empty. Renders `error-taxonomy-designer`'s codes. | auto + manual |
| `notification-webhook-ux-designer` | The human-facing UX of notifications (channels, per-category preferences, digest/dedup noise control, read-state, opt-out that works) and developer webhooks (delivery log, test-send, replay, secret rotation with an overlap window); the delivery CONTRACT stays with `api-event-architect`. | auto + manual |
| `mobile-viewport-craft` | Mobile/responsive viewport correctness: content-driven breakpoints, touch-target sizing, safe-area/notch, the 100vh→dvh/svh/lvh fix, input/keyboard behavior, hover-absence and gestures, wide-table reflow; page WEIGHT stays with `frontend-perf-engineer`. | auto + manual |

D12.5 — PM / product-engineering interface (D24): the engineering/PM
boundary. Two hard seams pinned both ways in trigger-evals —
`product-spec-writer` ≠ `adr-writer` (product spec vs architecture
decision) and `sunset-deprecation-communicator` ≠
`skill-deprecation-planner` (product-feature sunset vs library-skill
retirement):

| Skill | What it does | Invocation |
|---|---|---|
| `requirements-gathering-facilitator` | Elicits requirements BEFORE a spec: separates the problem from stakeholders' solutions, draws out users/jobs and the current workaround, surfaces the implicit (assumptions, non-goals, constraints), reconciles conflict to a decider; produces a confidence-marked brief that feeds `product-spec-writer`. Facilitates; does not decide. | auto + manual |
| `product-spec-writer` | The PRODUCT spec: problem/job, goals and explicit non-goals, scenarios, functional requirements with TESTABLE acceptance criteria, edge/error behavior, rollout intent + success metrics, open questions. Pinned ≠ `adr-writer` (a product spec is not an architecture decision record). | auto + manual |
| `roadmap-under-uncertainty-planner` | Horizon-based roadmap (now/next/later) over a false-precision dated Gantt: confidence decaying with distance, learning-first sequencing (retire uncertainty), outcomes over feature lists, capacity slack, a re-plan cadence. Consumes a ranking from `prioritization-frame-picker`. | auto + manual |
| `prioritization-frame-picker` | Picks the RIGHT prioritization frame (RICE/WSJF/value-effort/Kano/MoSCoW) instead of defaulting, marks input reliability, refuses false rigor (buckets + a sensitivity check), and pulls must-dos out of the value formula. Ranks; sequencing over time is `roadmap-under-uncertainty-planner`'s. | auto + manual |
| `feature-flag-rollout-strategist` | The ROLLOUT strategy: flag classified by purpose, progressive stages with advance/rollback criteria, sticky targeting, guardrails + a tested kill switch, a fail-safe default, flag-debt removal. Pinned ≠ `plan-entitlement-architect`/`authorization-matrix-designer` (entitlement/permission) and ≠ `ab-test-designer` (experiment). | auto + manual |
| `sunset-deprecation-communicator` | Sunsetting a PRODUCT feature/API to users: rationale, impact, migration path, a firm timeline, an escalating multi-channel comms plan, grandfathering, and a tombstone (not a silent 404). Pinned ≠ `skill-deprecation-planner` (retiring a library SKILL) and ≠ `api-event-architect` (standing policy). | auto + manual |

D12.6 — growth / analytics engineering (D24): user-facing product
analytics, distinct from system telemetry. The two three-way seams pinned
in trigger-evals — `event-schema-architect` ≠ `api-event-architect` ≠
`streaming-event-architect`, and `product-analytics-instrumenter` ≠
`observability-operator` ≠ `skill-usage-instrumenter`:

| Skill | What it does | Invocation |
|---|---|---|
| `event-schema-architect` | The ANALYTICS event schema/tracking plan: naming taxonomy, typed properties, global properties, identity stitching, a registry as source of truth, additive versioning, PII minimization. THREE-way seam pinned ≠ `api-event-architect` (external contract) ≠ `streaming-event-architect` (internal pipeline). | auto + manual |
| `funnel-definition-designer` | Rigorous funnel/conversion/retention definition: steps from real events, a counting model with a pinned denominator, a stated window, order semantics, attribution, and WHERE-not-WHY discipline (causes need an experiment). Consumes `event-schema-architect`; ≠ `ab-test-designer`. | auto + manual |
| `ab-test-designer` | Designs AND reads experiments: falsifiable hypothesis, one primary metric + guardrails, power/sample-size from a practical MDE, a fixed horizon (no peeking), sticky assignment; readout with CIs, multiple-comparison/SRM/Simpson's/novelty checks, ship/kill/iterate with residual uncertainty. Pinned ≠ `feature-flag-rollout-strategist`. | auto + manual |
| `product-analytics-instrumenter` | The product-analytics INSTRUMENTATION: client-vs-server capture, identity at capture, consent-gating + PII minimization at the source, capture reliability, de-dup, tracking QA. THREE-way seam pinned ≠ `observability-operator` (system telemetry) ≠ `skill-usage-instrumenter` (library usage). | auto + manual |

D12.4 — technical writing / docs engineering (D25): durable documentation
as its own discipline. `adr-sequencer` EXTENDS `adr-writer` (longitudinal
ADR management, composed not duplicated); `docs-retention-index` is the
DOC-lifecycle counterpart to `skill-deprecation-planner` (pinned both
ways); `api-doc-generator-designer` documents the contract
`api-event-architect` owns:

| Skill | What it does | Invocation |
|---|---|---|
| `readme-craftsman` | The README as entry point, not manual: first-screen what/why/who, a verified quickstart, common-case usage, and routes OUT to deeper docs; resists the kitchen sink and stays maintainable. | auto + manual |
| `adr-sequencer` | Longitudinal ADR CORPUS management atop `adr-writer`: the index, status lifecycle, bidirectional superseding links, contradiction detection, new-ADR-vs-amend, and append-only history (supersede, never overwrite). Composes `adr-writer` for single records. | auto + manual |
| `diataxis-doc-organizer` | Organizes the whole docs SET by the four Diátaxis modes (tutorial/how-to/reference/explanation), diagnosing actual-vs-claimed mode, splitting two-job docs, and setting the discipline that keeps modes from bleeding. | auto + manual |
| `docs-as-code-architect` | The docs TOOLCHAIN/pipeline: in-repo PR-reviewed docs, generator choice, per-PR previews, CI link/prose/build checks, executable-sample testing (the drift-killer), versioned publishing, and URL stability. | auto + manual |
| `api-doc-generator-designer` | GENERATED API reference from the source of truth (OpenAPI/GraphQL/docstrings) so it can't drift: the generated-vs-authored split, upstream enrichment, validated examples, versioning. Documents the contract `api-event-architect` owns. | auto + manual |
| `contribution-guide-author` | The zero-to-merged CONTRIBUTING guide: verified setup, the real workflow, automated standards, honest review expectations, governance + private security disclosure, and first-contribution on-ramps. Product-agnostic. | auto + manual |
| `onboarding-doc-designer` | New-hire onboarding: the day1/week1/month1 ramp, verified setup, a mental-model orientation (not the manual), how-we-work incl. unwritten norms, a glossary + who-to-ask, an early-win first task, and a self-heal currency plan. | auto + manual |
| `docs-retention-index` | The numbered DOC-lifecycle index: retention category + reason-to-keep + superseded-by + cleanup rule per doc (mirrored in frontmatter), reverse-reference sweep, staged mark→redirect→remove with human-approved deletion. DOC counterpart to `skill-deprecation-planner` (pinned both ways). | auto + manual |

D12.7 — staff+ IC craft (D26): technical leadership without management
authority. `tech-spec-writer` ≠ `adr-writer` (whole design vs one
decision) ≠ `product-spec-writer`; `phased-work-handoff-designer` ≠
`ai-closeout-reporter` (one turn) ≠ `ai-sdlc-operating-model` (lifecycle);
`staff-scope-selector` ≠ `promotion-packet-writer` (future scope vs past
impact, both ways):

| Skill | What it does | Invocation |
|---|---|---|
| `tech-spec-writer` | The whole-design tech spec / RFC: problem/goals/non-goals, proposed design (data model, APIs, components), alternatives, cross-cutting concerns (security/perf/observability/migration/testing), risks, sign-off. Composes `adr-writer` (decisions) + `architecture-designer` (structure). ≠ one ADR, ≠ product spec. | auto + manual |
| `design-review-facilitator` | Facilitates the design review: pre-read + right reviewers, importance-first discussion, actively elicited dissent, an EXPLICIT outcome (approved/changes/rework/blocked), captured decisions — countering rubber-stamp/bikeshed/HiPPO/no-decision. Reviews a design; doesn't write it. | auto + manual |
| `cross-team-dependency-negotiator` | Cross-team dependencies: two-way map, early surfacing, CONCRETE commitments (deliverable+date+owner both sides), de-risking (stub/flag/parallel), honest accounting for the other team's priorities, and a pre-agreed escalation trigger. The org side; the contract is `api-event-architect`'s. | auto + manual |
| `roadmap-to-commitments-translator` | Extracts the firm-promise subset from a roadmap: commit-able vs aspirational, capacity-grounded (velocity minus maintenance, buffered), dependency-gated, honest date RANGES, and the not-committed gap named. The inverse of `roadmap-under-uncertainty-planner`. | auto + manual |
| `staff-scope-selector` | Chooses a staff+ IC's highest-leverage FUTURE scope: level-relative leverage, under-owned problems, matched to strengths, screened against the traps (only-fun/firefighting/too-narrow/invisible-glue/over-reach), with a rationale + explicit NOT-doing list. ≠ `promotion-packet-writer` (past impact). | auto + manual |
| `promotion-packet-writer` | Assembles the promotion case: impact-not-activity, mapped to every rubric dimension, a sustained pattern, honest gap analysis, corroboration, committee language — no inflation. ≠ `staff-scope-selector` (future scope), ≠ `ai-closeout-reporter` (one task). | auto + manual |
| `phased-work-handoff-designer` | The cross-stage handoff protocol: a decision-ID register carried across stages, per-stage changed/NOT-touched lists, proven-invocation evidence (tell-tale output), deviation flags, and a cold-start continuation contract. ≠ `ai-closeout-reporter` (one turn), ≠ `ai-sdlc-operating-model` (lifecycle). | auto + manual |

D12.9 — architecture advisory (D26): the STYLE/paradigm advisor that filled
the gap between `architecture-designer` (concrete architecture) and
`cloud-architecture-decider` (cloud posture):

| Skill | What it does | Invocation |
|---|---|---|
| `architecture-advisor` | Advises the architecture STYLE (monolith/modular-monolith/microservices/event-driven/serverless/SOA/hybrid): interviews the need FIRST, relevant candidates only, case-specific tradeoffs, a clear recommendation + sensitivity; resists trend-chasing both ways (willing to say "boring modular monolith"). ≠ `architecture-designer` (concrete), `cloud-architecture-decider`, `saas-platform-architect`, `domain-modeler`. | auto + manual |

D14 — framework refresh / source-currency discipline (D26): keeping the
library current with EXTERNAL truth. A pipeline — `framework-edition-tracker`
(detect edition drift + delta) → `framework-mapping-refresher` (propose
edits, human review) — plus `source-currency-auditor` (broad staleness
sweep); none auto-updates:

| Skill | What it does | Invocation |
|---|---|---|
| `framework-edition-tracker` | Tracks cited standard EDITIONS (OWASP/ISO/SOC 2/NIST): an edition register, drift detection, and a DELTA report — verify-don't-assert edition facts; reports drift, updates nothing. Feeds `framework-mapping-refresher`. ≠ broad staleness (`source-currency-auditor`). | auto + manual |
| `framework-mapping-refresher` | Turns a verified edition delta into SPECIFIC proposed edits across affected skills/references/coverage maps, judging meaning-not-labels, surfacing new coverage GAPS, flagged for HUMAN review — never auto-applied. Downstream of `framework-edition-tracker`, upstream of `library-diff-reviewer`. | auto + manual |
| `source-currency-auditor` | Broad citation-currency sweep: inventory external-source citations, volatility-tuned staleness thresholds, flag stale/broken/superseded with reason and load-bearing priority — flags for re-verification, verifies/changes nothing. ≠ edition tracking (`framework-edition-tracker`). | auto + manual |

D28 — OWASP web-app A09/A10 gap closure: the D8 audit's two zero-coverage
OWASP Top 10:2025 categories, built from the Phase 8 backlog — all 10
web-app categories now have an owning skill (A02/A04 remain "partial" by
the D8 rubric). Both edit nothing:

| Skill | What it does | Invocation |
|---|---|---|
| `security-logging-alerting-architect` | The security-event DETECTION/ALERTING design (closes A09:2025): detection coverage map (which events must be logged, with detectable fields), alert-vs-ticket rules with baseline-justified thresholds + bounded noise control, response wiring (owner, severity, escalation, runbook link), coverage tests, honest blind spots. ≠ `audit-log-architect` (records, never detects/alerts), `observability-operator` (implements alert config), `slo-reliability-architect` (reliability paging), `incident-response-runbook` (the playbook AFTER). | auto + manual |
| `error-handling-security-reviewer` | The error/exception-path security REVIEW (closes A10:2025): fail-closed defaults, error-path authorization, exception-driven bypass, leak-free error responses — file:line findings, a fail-closed matrix, missing-negative-test list; recommends fixes, never applies them. ≠ `security-pr-reviewer` (broad diff gate), `appsec-implementer` (builds the fix), `static-analysis-reviewer` (scanner triage), `error-taxonomy-designer` (the error MODEL). | auto + manual |

D31 — SaaS architecture depth (D12.11 STRONG cluster): 10 net-new
architecture-depth surfaces for a multi-tenant SaaS, surfaced by a
read-only audit of production SaaS patterns; scheduled ahead of the D12.10
SAST/DAST pack. All design/review skills that edit nothing → model-invocable;
the three that can touch live systems (command-gateway backstop,
synthetic-monitoring probes, offline-first reconciliation) carry Stop
Conditions forbidding execution against production without human approval.
The 4 low-priority D12.11 candidates were the deferred Build B, since built in
D32 (below):

| Skill | What it does | Invocation |
|---|---|---|
| `command-gateway-architect` | The single server-mediated write path (command bus): a per-command pipeline (validate → authenticate actor from token → authorize → server-derive tenant scope → idempotency → execute → emit audit+events → safe error envelope) + the no-direct-client-writes invariant. ≠ `api-event-architect` (external contract), `authorization-matrix-designer` (the policy it ENFORCES), `audit-log-architect` (records it emits). | auto + manual |
| `realtime-subscription-architect` | Live client delivery (WS/SSE/DB-change/presence): channel model, authorize-at-subscribe-time (per-tenant AND per-user leak boundary), fan-out, stateful-connection scaling, backpressure, reconnect/replay. ≠ `streaming-event-architect` (internal backbone), `api-event-architect` (webhooks), `offline-first-sync-architect` (offline sync, in-batch), `notification-webhook-ux-designer` (UX). | auto + manual |
| `background-job-orchestration-architect` | The async job/worker EXECUTION model: worker pools, cron, job idempotency + resumability, retry/backoff, DLQ, visibility timeouts, per-tenant fairness. ≠ `streaming-event-architect` (transport vs execution — hard pin), `performance-test-harness`/`load-test-planner` (measure it), `command-gateway-architect` (sync protected write). | auto + manual |
| `horizontal-scalability-reviewer` | Can-it-scale-out review: statelessness, connection-ceiling math, sticky-session / in-process-singleton / local-cache / run-N-times smells, autoscaling + graceful drain — ranked readiness verdict. ≠ `slo-reliability-architect` (targets), `latency-budget-architect` (latency), `caching-strategy-designer` (cache design). | auto + manual |
| `search-architecture-designer` | Keyword/faceted search: in-DB full-text vs engine, indexing + freshness, ranking, the query-side AND index-side per-tenant isolation boundary (fail-closed), pagination seam. ≠ `rag-security-architect` (vector/semantic), `multi-tenant-data-architect` (base tenancy), `pagination-cursor-designer` (cursor mechanics). | auto + manual |
| `file-upload-storage-architect` | File/object storage + upload: direct-vs-proxied, narrowly-scoped signed URLs, tenant-prefixed keys, magic-byte content validation, malware scan, off-request derivatives, retention, CDN. ≠ `pii-lifecycle-designer` (personal-data lifecycle of contents), `rls-policy-auditor` (audit existing storage policies). | auto + manual |
| `usage-metering-and-cost-attribution-pipeline-designer` | The metering→rollup→reconciliation DATA PIPELINE: billing-safe metadata-only event table, time-bounded rate cards, idempotent cost entries, additive rollups, budgets/alerts, invoice reconciliation. **STANDALONE (D31).** ≠ `saas-cost-architect` (unit-economics cost MODEL — closest neighbor, hard pin), `ai-cost-guardrail-designer` (AI spend enforcement), `operational-vs-analytical-splitter` (rollup placement). | auto + manual |
| `synthetic-monitoring-architect` | Black-box PRODUCTION monitoring: scheduled prod-safe probes/journeys + dependency/heartbeat, a hard no-mutate/no-fixture-leak safety contract, synthetic SLIs + alerting. DESIGNS probes, does not run them against prod. ≠ `performance-test-harness`/`load-test-planner` (pre-release), `playwright-e2e-engineer` (CI E2E), `slo-reliability-architect` (targets), `observability-operator` (white-box). | auto + manual |
| `offline-first-sync-architect` | The client OFFLINE data layer: durable idempotent write queue, optimistic apply + rollback, version-based conflict detection + eyes-open resolution (refuses silent data loss), background sync, reconciliation integrity. ≠ `edge-state-ux-designer` (UX states), `caching-strategy-designer` (server cache), `realtime-subscription-architect` (live online push, in-batch). | auto + manual |
| `admin-console-architect` | The internal ops/support/superadmin CONSOLE: least-privilege tiers, audited-by-construction cross-tenant access (reads too), bounded/marked/time-boxed impersonation, break-glass elevation, gated control-plane actions. ≠ `authorization-matrix-designer` (the policy it ENFORCES), `observability-operator` (telemetry vs action), `agent-authorization-matrix` (AI-agent vs human), `incident-response-runbook` (the playbook it serves). | auto + manual |

D32 — SaaS architecture depth (D12.11 LOW-PRIORITY set): the 4 deferred
Build-B candidates, completing the D12.11 pack (all 14 candidates now
resolved: 10 strong built D31, 4 low-priority built D32). Two carried a
standalone-vs-extension flag resolved at build time — `intra-tenant-scope-architect`
(~60% distinct from `multi-tenant-data-architect`) and `share-link-access-architect`
(~60% distinct from `authorization-matrix-designer`) — both shipped STANDALONE.
All design/review skills that edit nothing → model-invocable; the three that
DESIGN a production-reshaping change (cell migration/rebalancing, a reshard, an
add-a-scope-axis migration) carry Stop Conditions forbidding execution against
production without human approval — they design, they do not run.

| Skill | What it does | Invocation |
|---|---|---|
| `cell-based-architecture-designer` | Cell (blast-radius) partitioning: a self-contained full-stack cell per tenant-subset, tenant→cell mapping + placement, a THIN cell-router, cell-by-cell deploy/canary, global-concern enumeration, migration/rebalancing. SCALE-STAGE — tests the premise first and recommends NOT adopting cells when a cheaper lever suffices. ≠ `saas-platform-architect` (per-component pooled/siloed isolation), `architecture-advisor` (the style choice, whose menu omits cells), `agent-containment-reviewer` (agent blast radius). | auto + manual |
| `data-partitioning-sharding-strategist` | OLTP partitioning/sharding for WRITE/size scale: shard-key selection (tenant_id + its hot-tenant limit), range/hash/list partitioning, cross-shard cost, reshard/rebalance runbook — gated behind DON'T-SHARD-PREMATURELY (single well-indexed primary + replicas first; shard only on evidenced ceiling). ≠ `multi-tenant-data-architect` (isolation scoping), `warehouse-lake-architect` (analytical partitioning), `operational-vs-analytical-splitter` (what leaves the OLTP store). | auto + manual |
| `intra-tenant-scope-architect` | A second mandatory scoping axis BELOW the tenant (site/region/org-unit): per-user scope-grant model, the composite tenant+scope row-filter predicate on every scoped table, scope-restricted vs tenant-wide roles, server-derived propagation, live add-axis migration. **STANDALONE (D32).** ≠ `tenant-modeler` (tenant semantics/hierarchy), `multi-tenant-data-architect` (tenant_id-axis storage), `authorization-matrix-designer` (roles×permissions vs a row-filter), `command-gateway-architect` (execute-time write scope). | auto + manual |
| `share-link-access-architect` | Guest/public share-link (bearer-capability) access: opaque expiring revocable tokens, per-link scope, ephemeral guest sessions, optional password/OTP gate, enumeration/abuse defense, audit — the link exposes exactly its resource, never a hole into the tenant. **STANDALONE (D32).** ≠ `authorization-matrix-designer` (member RBAC + impersonation), `api-event-architect` (machine API credentials / webhook signing). | auto + manual |

## Authoring a new skill

1. Read [`docs/skill-generation-standard.md`](docs/skill-generation-standard.md).
2. Copy `.claude/skills/_template/` to `.claude/skills/<your-skill-name>/`.
3. Set frontmatter `name` to match the new directory exactly.
4. Fill in all required sections; keep `SKILL.md` under 500 lines (push detail to `references/`).
5. Add `evals/evals.json` (and `evals/trigger-evals.json` if the trigger overlaps another skill).
6. List the skill in [`docs/skills-catalog.md`](docs/skills-catalog.md) **and** this README.
7. Run the validator until it passes.

Side-effecting skills (writes, network, deploy, spend) MUST set `disable-model-invocation: true`
and document the irreversible step under **Stop Conditions**.

## Validation

Run from the repo root:

```bash
python scripts/validate-skills.py
```

Checks: `name` matches directory; `description` present and < 1024 chars; no broad
`allowed-tools`; `SKILL.md` < 500 lines; all required sections present; `evals/evals.json`
exists and parses (structural only — no runner yet); `evals/trigger-evals.json` parses when
present; catalog integrity (every on-disk skill is listed in the catalog and README);
bundled-name collision and duplicate-name checks.

Behavior: `_template` is ignored. When `_template` is the only skill directory, the validator
prints a "no skills found" status and exits `0`. Exit `0` = clean (warnings allowed); non-zero
= at least one error. Run it before every commit that touches `.claude/skills/`.

## CI (merge gate)

Every pull request targeting `main` runs
[`.github/workflows/validate-skills.yml`](.github/workflows/validate-skills.yml), which
provides two required status checks:

| Check | What it does |
| --- | --- |
| `validate-skills` | Runs `python scripts/validate-skills.py` on the PR (latest Python 3.x). Fails on any validator error — same checks as running it locally. |
| `gate-guard` | Diffs the PR against its base and **fails if the PR touches the merge gate itself** (anything under `.github/workflows/` or `scripts/validate-skills.py`). Such PRs print `This PR modifies the merge gate itself and requires manual review and merge.` and must be reviewed and merged manually by a human. |

Notes:

- Both job names are registered as required status checks — do not rename them (and keep
  them unique across all workflows) without updating branch protection.
- A `gate-guard` failure is not a defect; it is the intended signal that the change needs
  human eyes. Fixing the gate to "make CI green" defeats its purpose.
- The gate uses only `actions/checkout` and `actions/setup-python` — no third-party actions.
- Merge is manual: a human merges each PR after the required checks pass — auto-merge is
  never armed for this project's development, and changes touching the merge gate itself always
  require manual review regardless (see
  [`docs/reconciliation/auto-merge-policy.md`](docs/reconciliation/auto-merge-policy.md)).

## Target repository layout

```text
.claude/
  agents/                 # real read-only reviewer subagents
    <agent-name>.md
  skills/
    _template/            # reference template (ignored by validator)
    <skill-name>/
      SKILL.md
      references/
      assets/
      evals/
        evals.json
        trigger-evals.json   # when trigger overlaps another skill

docs/
  reconciliation/  research/  prompts/  roadmaps/  skills/  templates/
  skill-generation-standard.md
  skills-catalog.md

scripts/
  validate-skills.py
```

## Core rules

- Skills are reusable procedures, not essays. Agents are isolated read-only specialists.
- Build in waves. Do not create the backlog at once (the original 300-skill roadmap, per the D12 standing rule a 300+ target backlog — ship on demand and framework coverage, not count; roadmap = backlog, not a batch command).
- Start with standards, templates, eval convention, and validators (Phase 0).
- Every skill needs `SKILL.md` with clear frontmatter, concise workflow, output format,
  validation checklist, gotchas, stop conditions, and `evals/evals.json`.
- Avoid broad `allowed-tools`; use `disable-model-invocation: true` for side-effect workflows.
- Use read-only exploration first for audits, architecture, code, security, and QA review.
- Treat security, tenant isolation, QA evidence, and verification as first-class requirements.
- Keep product-specific skills out of this reusable foundation.

## Safety note

Claude Code Skills and subagents can influence future code, tests, reviews, and tool usage.
Review every generated skill and agent before trusting it. A reusable skill library is useful
only if it is specific, testable, constrained, maintained, and validated.
