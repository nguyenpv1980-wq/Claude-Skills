---
name: docs-first-implementer
description: Implement against frameworks, libraries, or external services by first identifying the EXACT versions installed in this repo and reading the matching documentation — official docs, local node_modules/vendored docs, changelogs — before writing any code. Summarizes only the syntax relevant to the task, implements, then verifies with the project's tests/build/lint. States uncertainty explicitly when docs for the pinned version are unavailable instead of guessing from training data. Use when implementing a feature that touches a framework or library API, when an API may have changed across versions, when integrating an external SDK or service, or after being burned by an API that "should exist" but doesn't in the installed version.
---

# Docs-First Implementer

## Purpose

Eliminate the "implemented against a remembered API" failure mode: code
written for a version the project does not have, deprecated options,
hallucinated methods. The discipline is version → docs → summarize → implement
→ verify: pin the exact installed version, read documentation that matches
it, extract only the task-relevant syntax, implement, and prove it with the
project's own verification commands. Where matching docs cannot be found,
uncertainty is stated as a first-class output, not papered over.

## Use When

- Use when: implementing a feature that leans on a framework or library API —
  routing, ORM queries, auth middleware, UI library components, SDK calls.
- Use when: the library is fast-moving or the API surface differs across
  majors (build tools, meta-frameworks, cloud SDKs, AI SDKs).
- Use when: a previous attempt failed with "X is not a function" or
  deprecation warnings — symptoms of version drift.
- Do NOT use when: the change is pure project-internal logic touching no
  external API — normal implementation discipline suffices.
- Do NOT use when: the task is diagnosis of an unknown-cause failure — that
  is `systematic-debugger` (which may hand off here once the fix touches a
  library API).
- Do NOT use when: the human asked for test-first development explicitly —
  run `tdd-engineer` as the outer loop; this skill governs the docs step
  inside it.

## Inputs to Inspect

1. Version manifests: `package.json` + lockfile, `requirements.txt`/
   `pyproject.toml`/`poetry.lock`, `go.mod`, `*.csproj`, `Gemfile.lock` —
   the LOCKED version, not the semver range.
2. The documentation matching that version: versioned official docs, the
   installed package's own `README`/`docs/` in `node_modules` or site-packages,
   changelog/migration guides between the docs' version and the installed one.
3. Existing usage of the same library in this repo — the project may already
   have a sanctioned pattern (wrapper, config, error handling) to follow.
4. The project's verification commands: test runner, build, lint, typecheck
   (from package scripts, CI config, or CLAUDE.md).

## Workflow

1. **Pin the exact version.** Read the lockfile, not the manifest range.
   Record: library, locked version, and where it is imported today.
2. **Find version-matching docs.** Preference order: versioned official docs
   for that exact major/minor → the installed package's bundled README/types/
   docs → changelog diff from the nearest documented version. Record which
   source was actually used.
3. **Summarize task-relevant syntax only** — the 3–10 API facts this task
   needs (signatures, options, defaults, error behavior), each attributed to
   its source. No general tutorial prose.
4. **Check repo precedent.** If the repo already wraps or configures this
   library, follow that pattern; deviating from it is a decision to surface,
   not a default.
5. **Declare uncertainty before coding.** Anything the docs did not answer
   goes in an "unverified" list — implemented defensively and called out.
6. **Implement** the minimal change consistent with the summarized syntax and
   repo conventions.
7. **Verify** with the project's own commands (tests, build, lint,
   typecheck). Report the exact commands and real results. A missing
   verification path is reported, not silently skipped.

## Output Format

```
DOCS-FIRST IMPLEMENTATION — <task>
Version pin: <library>@<locked version> (source: <lockfile>)
Docs consulted: <source + version — e.g. official vX.Y docs, node_modules README,
                 CHANGELOG X.Y→X.Z>
Relevant syntax: <the 3–10 facts used, each with source>
Repo precedent followed: <pattern/file, or "none exists">
Unverified assumptions: <each with mitigation> | None
Change: <files touched, summary>
Verification: <exact commands + actual results>
```

## Validation Checklist

- [ ] Version taken from the LOCKFILE (or equivalent resolved source).
- [ ] Every API call in the change traces to the syntax summary; every
      summary line traces to a named doc source.
- [ ] Docs source version matches the installed version, or the gap is
      bridged via changelog and said so.
- [ ] Repo's existing wrapper/pattern for this library followed or the
      deviation justified.
- [ ] Verification commands actually run, with real output reported —
      failures included.
- [ ] Unverified assumptions listed explicitly ("None" written deliberately).

## Gotchas

- The manifest says `^4.0.0` but the lockfile resolved 4.9.2 — features and
  deprecations live in that gap. Always the lockfile.
- Docs sites default to "latest"; a URL without a version selector is a trap.
  Prefer the version switcher or the installed package's own files.
- Two majors of the same library can coexist (transitive vs direct); confirm
  which one the import resolves to before trusting either changelog.
- Training-data memory of an API feels identical to knowledge of it. The tell:
  you didn't read it today. If it's not in the syntax summary, don't type it.
- AI-era libraries (SDKs, frameworks <2 years old) change signatures between
  minors; changelog reading is not optional there.
- Local docs in `node_modules` describe the installed version by definition —
  they beat a newer, shinier docs site.

## Stop Conditions

- No documentation for the installed version can be located and the changelog
  gap is unbridgeable → stop and present options (upgrade, spike, proceed
  with declared risk) rather than implementing from memory.
- The docs reveal the requested approach is deprecated or unsafe in this
  version → surface before implementing, don't silently substitute.
- The correct implementation requires a version bump → that is a dependency
  change with its own blast radius; get approval via
  `change-classification-gate`/`human-approval-boundary` rather than bundling it.
- Verification commands fail for pre-existing reasons unrelated to the change
  → report the baseline failure; do not "fix" unrelated tests to get green.

## Supporting Files

- [references/version-doc-checklist.md](references/version-doc-checklist.md) —
  per-ecosystem lockfile locations, doc-source preference tables, and
  changelog-bridging tactics.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `tdd-engineer` and
  `systematic-debugger` (implementation cluster).
