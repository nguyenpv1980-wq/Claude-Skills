#!/usr/bin/env python3
"""Validate skills under .claude/skills/ against the repo skill-generation standard.

Checks performed per skill (see docs/skill-generation-standard.md):
  * SKILL.md exists and has a ----fenced frontmatter block that parses with a
    SPEC-STRICT YAML parser (decision D50 — check_frontmatter_strict_yaml,
    HARD: lenient in-house parsing let 67 descriptions ship that strict
    Agent-Skills consumers such as Codex CLI silently DROP; see the
    "Portability contract" in docs/skill-generation-standard.md).
  * the raw `description:` line must not open a YAML block scalar (`>`/`|`)
    (D50 follow-up per PR #59 review — check_description_not_block_scalar,
    HARD: spec-strict parsers ACCEPT block scalars, but the Portability
    contract forbids them because consumers differ on folding/chomping, so
    this is checked on the RAW line BEFORE the parse).
  * frontmatter `name` exactly equals the skill's directory name.
  * frontmatter `description` present, non-empty, and < 1024 characters
    measured on the strict-PARSED value — quoting characters and doubled
    apostrophes are serialization, not content, and do not count (external
    consumers measure the parsed value; D49 evidence).
  * manual-only skills (`disable-model-invocation: true`) carry the exact
    32-char sentinel "MANUAL-ONLY; never auto-invoke. " as the FIRST 32
    characters of the parsed description (decision D50 —
    check_manual_only_sentinel, HARD: strict consumers ignore the field and
    surface only the description front at selection time, per D49). The
    check is BIDIRECTIONAL (D50 follow-up per PR #59 review): a description
    that LEADS with the sentinel but lacks the field also fails — Claude
    Code itself would auto-invoke a skill whose text forbids it.
  * no BROAD `allowed-tools` grant (e.g. "*", "all", bare "Bash").
  * SKILL.md body is < 500 lines.
  * all nine required sections present (v4 standard): Purpose, Use When,
    Inputs to Inspect, Workflow, Output Format, Validation Checklist, Gotchas,
    Stop Conditions, Supporting Files.
  * evals convention (repo decision D3 — structural only, no runner):
    evals/evals.json exists and parses; evals/trigger-evals.json parses if present.

Repo-level checks:
  * README-catalog integrity: every skill is listed in docs/skills-catalog.md
    AND in README.md.
  * bundled-name collision: no skill name duplicates another skill, and no
    skill name shadows a reserved bundled skill name.
  * README map-matches-territory (decision D43): the README's marked SKILL-COUNT
    equals the real skill count on disk, and the roster's per-family counts (plus
    the one project-orchestrator front door) reconcile with disk and with the
    FAMILY-COUNT marker — both HARD errors. Curated surfaces (roster flagship
    names, the roles table) are checked at WARNING level only, since they are
    human-curated and deliberately not 1:1 with the skill set.

The `_template` directory is ALWAYS ignored (it is a template, not a shipped skill).
When `_template` is the only skill directory, the script prints "no skills found"
and exits 0.

Exit code 0 = clean (possibly with warnings), non-zero = at least one error.
Requires PyYAML for the strict frontmatter parse (decision D50):
`python -m pip install pyyaml`. Fails closed if it is missing. No other
third-party dependencies.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # reported fail-closed in main() — see decision D50
    yaml = None

# --- configuration ---------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
CATALOG = REPO_ROOT / "docs" / "skills-catalog.md"
README = REPO_ROOT / "README.md"

IGNORED_DIRS = {"_template"}
MAX_SKILL_LINES = 500
MAX_DESCRIPTION_CHARS = 1024

REQUIRED_SECTIONS = [
    "Purpose",
    "Use When",
    "Inputs to Inspect",
    "Workflow",
    "Output Format",
    "Validation Checklist",
    "Gotchas",
    "Stop Conditions",
    "Supporting Files",
]

# Names shipped/bundled elsewhere in the Claude ecosystem that a repo skill must
# not shadow, to avoid ambiguous invocation. Extend as needed.
RESERVED_BUNDLED_NAMES = {
    "watch",
    "docx",
    "pdf",
    "pptx",
    "xlsx",
    "schedule",
    "skill-creator",
    "verify",
    "code-review",
    "simplify",
    "loop",
    "run",
    "init",
    "review",
    "security-review",
}

# allowed-tools values that count as "broad" and are rejected.
BROAD_TOOL_TOKENS = {"*", "all", "any", "bash"}


# --- frontmatter parsing (decision D50: spec-strict) ------------------------

# Exactly 32 characters including the trailing space. Strict Agent-Skills
# consumers ignore `disable-model-invocation` and surface only the front of
# the description at selection time (D49 discovery), so the START of the
# parsed description value is the sentinel's only guaranteed-visible position.
MANUAL_ONLY_SENTINEL = "MANUAL-ONLY; never auto-invoke. "

# A raw frontmatter `description:` line whose value opens a YAML block scalar
# (`>` folded / `|` literal, with or without chomping/indentation indicators).
# A quoted scalar can never match: its first value character is a quote.
BLOCK_SCALAR_DESC_RE = re.compile(r"^description:\s*([>|])", re.MULTILINE)


def split_frontmatter(text: str):
    """Return (frontmatter_text, body_str) or (None, text) if no ----fenced block."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    return "\n".join(lines[1:end]), "\n".join(lines[end + 1 :])


def check_description_not_block_scalar(fm_text: str, name_ctx: str, rep: Report) -> None:
    """Decision D50 follow-up (HARD; Codex-review P2 on PR #59): the raw
    `description:` line must not open a YAML block scalar. The Portability
    contract says "One physical line. No block scalars (`>`, `|`)" because
    consumers differ on folding/chomping behavior — but a spec-strict parser
    happily ACCEPTS a block scalar and returns an ordinary string, so the
    parsed-value checks alone cannot catch one. This runs on the RAW
    frontmatter text, BEFORE the parse.
    """
    m = BLOCK_SCALAR_DESC_RE.search(fm_text)
    if m:
        rep.error(
            f"[{name_ctx}] `description:` opens a YAML block scalar "
            f"('{m.group(1)}') — forbidden by the Portability contract in "
            "docs/skill-generation-standard.md (consumers differ on "
            "folding/chomping); write the description as ONE single-quoted "
            "line ('' doubles an internal apostrophe)"
        )


def check_frontmatter_strict_yaml(fm_text: str, name_ctx: str, rep: Report):
    """Decision D50 (HARD): the frontmatter must parse with a spec-strict
    YAML parser. Claude Code's own reader is lenient, but other Agent-Skills
    consumers strict-parse and SILENTLY DROP non-compliant skills (before
    D50, Codex CLI dropped 67 of the 184). The classic failure is an unquoted
    `: ` inside a description; the fix is a single-quoted scalar with internal
    apostrophes doubled ('').

    Returns the parsed mapping, or None after reporting the error.
    """
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        msg = " ".join(str(exc).split())
        rep.error(
            f"[{name_ctx}] frontmatter does not parse as strict YAML: {msg} "
            "— single-quote the offending scalar ('' doubles an internal apostrophe)"
        )
        return None
    if not isinstance(data, dict):
        rep.error(
            f"[{name_ctx}] frontmatter must parse to a YAML mapping, "
            f"got {type(data).__name__}"
        )
        return None
    return data


def check_manual_only_sentinel(name_ctx: str, fm: dict, desc, rep: Report) -> None:
    """Decision D50 (HARD, BIDIRECTIONAL): the `disable-model-invocation`
    field and the sentinel front of the parsed description must agree.

    field -> sentinel: every manual-only skill carries the exact sentinel as
    the first 32 characters of its parsed description, so consumers that
    ignore `disable-model-invocation` (D49: Codex CLI) still surface the
    safety contract in the only position they are guaranteed to show.

    sentinel -> field (D50 follow-up per PR #59 review): a description that
    claims MANUAL-ONLY without the field set is worse than either alone —
    Claude Code enforces the FIELD, so it would auto-invoke a skill whose
    own text forbids it.
    """
    dmi = fm.get("disable-model-invocation")
    is_manual = dmi is True or str(dmi).strip().lower() == "true"
    has_sentinel = isinstance(desc, str) and desc.startswith(MANUAL_ONLY_SENTINEL)
    if is_manual and not has_sentinel:
        rep.error(
            f"[{name_ctx}] disable-model-invocation is true but the parsed "
            f"description does not START with the exact sentinel "
            f"{MANUAL_ONLY_SENTINEL!r} (32 chars incl. trailing space) — "
            "strict consumers ignore the field and see only the description front"
        )
    elif has_sentinel and not is_manual:
        rep.error(
            f"[{name_ctx}] description claims MANUAL-ONLY (starts with the "
            f"exact 32-char sentinel) but disable-model-invocation is not set "
            "— Claude Code would auto-invoke a skill whose text forbids it"
        )


def section_headers(body: str) -> set[str]:
    """Return the set of `##`-level section titles present in the body."""
    out = set()
    for line in body.splitlines():
        m = re.match(r"^##\s+(.*\S)\s*$", line)
        if m:
            out.add(m.group(1).strip())
    return out


# --- validation ------------------------------------------------------------


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def discover_skills() -> list[Path]:
    if not SKILLS_DIR.is_dir():
        return []
    out = []
    for child in sorted(SKILLS_DIR.iterdir()):
        if not child.is_dir():
            continue
        if child.name in IGNORED_DIRS:
            continue
        out.append(child)
    return out


def validate_skill(skill_dir: Path, rep: Report) -> str | None:
    """Validate one skill directory. Returns the skill name (for collision checks)."""
    name_ctx = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        rep.error(f"[{name_ctx}] missing SKILL.md")
        return None

    text = skill_md.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(text)
    if fm_text is None:
        rep.error(f"[{name_ctx}] SKILL.md has no parseable frontmatter block")
        return None

    # Decision D50 follow-up (PR #59 review): raw-line check BEFORE the parse
    # — a spec-strict parser ACCEPTS the block-scalar descriptions the
    # Portability contract forbids, so the parsed values cannot reveal them.
    check_description_not_block_scalar(fm_text, name_ctx, rep)

    # Decision D50: the frontmatter must strict-parse, and every field check
    # below runs on the strictly PARSED values — exactly what external
    # Agent-Skills consumers see.
    fm = check_frontmatter_strict_yaml(fm_text, name_ctx, rep)
    if fm is None:
        return skill_dir.name

    # name matches directory
    fm_name = fm.get("name")
    if not fm_name:
        rep.error(f"[{name_ctx}] frontmatter missing `name`")
    elif fm_name != skill_dir.name:
        rep.error(
            f"[{name_ctx}] frontmatter name '{fm_name}' != directory '{skill_dir.name}'"
        )

    # description — every check measures the strict-PARSED value: quoting
    # characters and doubled apostrophes are serialization, not content, and
    # external consumers (D49: Codex) measure the parsed value too.
    desc = fm.get("description")
    if desc is not None and not isinstance(desc, str):
        rep.error(f"[{name_ctx}] `description` must be a plain string scalar")
        desc = None
    if not desc or not desc.strip():
        rep.error(f"[{name_ctx}] frontmatter missing/empty `description`")
    elif len(desc) >= MAX_DESCRIPTION_CHARS:
        rep.error(
            f"[{name_ctx}] description is {len(desc)} chars (parsed value; "
            f"must be < {MAX_DESCRIPTION_CHARS})"
        )
    check_manual_only_sentinel(name_ctx, fm, desc, rep)

    # allowed-tools must not be broad
    tools = fm.get("allowed-tools")
    if tools is not None:
        tool_list = tools if isinstance(tools, list) else [tools]
        for t in tool_list:
            if str(t).strip().lower() in BROAD_TOOL_TOKENS:
                rep.error(
                    f"[{name_ctx}] broad allowed-tools grant '{t}' is forbidden; "
                    f"scope it narrowly or omit the field"
                )

    # side-effect skills should disable model invocation (advisory)
    dmi = str(fm.get("disable-model-invocation", "")).lower()
    if dmi not in ("true", "false", ""):
        rep.warn(f"[{name_ctx}] disable-model-invocation should be true/false")

    # line count
    n_lines = len(text.splitlines())
    if n_lines >= MAX_SKILL_LINES:
        rep.error(
            f"[{name_ctx}] SKILL.md is {n_lines} lines (must be < {MAX_SKILL_LINES})"
        )

    # required sections
    present = section_headers(body)
    missing = [s for s in REQUIRED_SECTIONS if s not in present]
    if missing:
        rep.error(f"[{name_ctx}] missing required section(s): {', '.join(missing)}")

    # evals convention (structural only — no runner yet, per decision D3)
    evals_json = skill_dir / "evals" / "evals.json"
    if not evals_json.is_file():
        rep.error(f"[{name_ctx}] missing evals/evals.json")
    else:
        try:
            json.loads(evals_json.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            rep.error(f"[{name_ctx}] evals/evals.json does not parse as JSON: {exc}")

    # trigger-evals.json is optional, but must parse when present
    trigger_json = skill_dir / "evals" / "trigger-evals.json"
    if trigger_json.is_file():
        try:
            json.loads(trigger_json.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            rep.error(
                f"[{name_ctx}] evals/trigger-evals.json does not parse as JSON: {exc}"
            )

    return skill_dir.name


def check_catalog_integrity(skill_names: list[str], rep: Report) -> None:
    catalog_text = CATALOG.read_text(encoding="utf-8") if CATALOG.is_file() else ""
    readme_text = README.read_text(encoding="utf-8") if README.is_file() else ""
    if not CATALOG.is_file():
        rep.error(f"catalog not found at {CATALOG.relative_to(REPO_ROOT)}")
    if not README.is_file():
        rep.error(f"README not found at {README.relative_to(REPO_ROOT)}")
    for name in skill_names:
        if name and name not in catalog_text:
            rep.error(f"[{name}] not listed in docs/skills-catalog.md")
        if name and name not in readme_text:
            rep.error(f"[{name}] not listed in README.md")


# --- README map-matches-territory checks (decision D43) --------------------
#
# check_catalog_integrity above is only a SUBSTRING test: it verifies each skill
# name appears SOMEWHERE in README. That let presentation-drift ship green
# repeatedly — stale skill counts, a family added without bumping its total, a
# renamed flagship left in the roster. Per the discipline's own rule, "anything
# caught by hand twice becomes a machine check," these checks reconcile the
# README's *authoritative* counts against reality. The authoritative numbers are
# wrapped in HTML-comment markers the validator owns, so there is no guessing
# which "179" in the prose is the current total (historical and aspirational
# numbers are deliberately left unmarked).

SKILL_COUNT_MARKER = re.compile(
    r"<!--\s*SKILL-COUNT\s*-->\s*(\d+)\s*<!--\s*/SKILL-COUNT\s*-->"
)
FAMILY_COUNT_MARKER = re.compile(
    r"<!--\s*FAMILY-COUNT\s*-->\s*(\d+)\s*<!--\s*/FAMILY-COUNT\s*-->"
)
# A roster family line, e.g. "1. **Operating discipline** *(Phase 1, 8)* — ...".
# The trailing (\d+) is that family's declared skill count. Non-greedy name and
# phase groups tolerate names with punctuation ("CONSTRAIN/CURATE", "Data + ...")
# and varied phase labels ("Phase 1.5", "D12.8", "D42").
FAMILY_LINE = re.compile(
    r"^\d+\.\s+\*\*.+?\*\*\s+\*\([^)]*?,\s*(\d+)\)\*",
    re.MULTILINE,
)
# A backticked kebab-case token (skill-name shape) inside the roster prose.
ROSTER_SKILL_TOKEN = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")

WHATS_IN_THE_LIBRARY = "## What's in the library"
ROLES_SECTION = "## The roles Aegis can play"


def _section_text(text: str, header: str) -> str | None:
    """Return the body of a `## header` section, up to the next `## ` header.

    Returns None if the header is absent — callers decide whether that is an
    error or a graceful degrade.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def check_readme_counts(real_count: int, rep: Report) -> None:
    """HARD: the README's marked SKILL-COUNT must equal the real skills on disk."""
    if not README.is_file():
        return  # check_catalog_integrity already reports the missing README
    text = README.read_text(encoding="utf-8")
    m = SKILL_COUNT_MARKER.search(text)
    if not m:
        rep.error(
            "README is missing the <!-- SKILL-COUNT -->N<!-- /SKILL-COUNT --> marker "
            "(the authoritative current-total the validator reconciles against disk)"
        )
        return
    marked = int(m.group(1))
    if marked != real_count:
        rep.error(
            f"README SKILL-COUNT marker says {marked} but {real_count} skill(s) exist "
            "on disk (update the marked count in the \"What's in the library\" intro)"
        )


def check_readme_family_roster(real_count: int, rep: Report) -> None:
    """HARD: the roster under "What's in the library" must reconcile with disk.

    (a) sum(family counts) + 1 (the project-orchestrator front door, which is
        explicitly NOT a family) == real skill count; and
    (b) the number of family lines == the FAMILY-COUNT marker.

    Degrades to a WARNING if the roster section is absent or unparseable, so a
    benign future format change degrades gracefully instead of hard-blocking
    every PR.
    """
    if not README.is_file():
        return
    text = README.read_text(encoding="utf-8")
    section = _section_text(text, WHATS_IN_THE_LIBRARY)
    if section is None:
        rep.warn(
            f"README roster section '{WHATS_IN_THE_LIBRARY}' not found; "
            "skipping family-count reconciliation"
        )
        return
    family_counts = [int(m.group(1)) for m in FAMILY_LINE.finditer(section)]
    if not family_counts:
        rep.warn(
            "README roster: no family lines parsed under "
            f"'{WHATS_IN_THE_LIBRARY}'; skipping family-count reconciliation"
        )
        return
    n_families = len(family_counts)
    total = sum(family_counts) + 1  # +1 = project-orchestrator front door (not a family)
    if total != real_count:
        rep.error(
            f"README roster family counts sum to {sum(family_counts)} + 1 orchestrator "
            f"= {total}, but {real_count} skill(s) exist on disk "
            "(a family's *(Phase/D, N)* count is out of sync with reality)"
        )
    fm = FAMILY_COUNT_MARKER.search(text)
    if not fm:
        rep.error(
            "README is missing the <!-- FAMILY-COUNT -->N<!-- /FAMILY-COUNT --> marker "
            "(the authoritative family total the roster is checked against)"
        )
    elif int(fm.group(1)) != n_families:
        rep.error(
            f"README FAMILY-COUNT marker says {int(fm.group(1))} but {n_families} "
            "family line(s) exist in the roster (add the family AND bump the marker)"
        )


def check_roster_flagships_exist(real_names: set[str], rep: Report) -> None:
    """WARN: every backticked kebab-case skill name in the roster must exist.

    Catches a renamed or removed flagship left stale in the roster — the reverse
    of check_catalog_integrity, which only ensures each real skill appears
    somewhere. WARNING, not error: the roster is curated prose and a future
    non-skill backticked token should not hard-block a PR.
    """
    if not README.is_file():
        return
    text = README.read_text(encoding="utf-8")
    section = _section_text(text, WHATS_IN_THE_LIBRARY)
    if section is None:
        return
    for token in sorted({m.group(1) for m in ROSTER_SKILL_TOKEN.finditer(section)}):
        if token not in real_names:
            rep.warn(
                f"README roster references `{token}`, which is not a skill on disk "
                "(a renamed/removed flagship left stale in the roster?)"
            )


def check_roles_table_present(rep: Report) -> None:
    """WARN: the curated '## The roles Aegis can play' section should exist.

    The roles table is a human-curated positioning layer, deliberately NOT 1:1
    with skills, so this checks presence only — completeness is a judgment call
    (see CONTRIBUTING "How to add a skill", step 3e).
    """
    if not README.is_file():
        return
    text = README.read_text(encoding="utf-8")
    if ROLES_SECTION not in text:
        rep.warn(
            f"README is missing the '{ROLES_SECTION}' section "
            "(the curated positioning layer)"
        )


def check_name_collisions(skill_names: list[str], rep: Report) -> None:
    seen: set[str] = set()
    for name in skill_names:
        if not name:
            continue
        if name in seen:
            rep.error(f"duplicate skill name '{name}'")
        seen.add(name)
        if name in RESERVED_BUNDLED_NAMES:
            rep.error(
                f"skill name '{name}' collides with a reserved bundled skill name"
            )


def main() -> int:
    if yaml is None:
        print(
            "ERROR PyYAML is required for the strict frontmatter parse "
            "(decision D50). Install it with: python -m pip install pyyaml"
        )
        return 1

    rep = Report()
    skills = discover_skills()

    if not skills:
        print("no skills found (only _template present or skills dir empty) - nothing to validate")
        return 0

    print(f"Validating {len(skills)} skill(s) under .claude/skills/ ...\n")

    names: list[str] = []
    for skill_dir in skills:
        name = validate_skill(skill_dir, rep)
        names.append(name or "")

    check_name_collisions(names, rep)
    check_catalog_integrity([n for n in names if n], rep)

    # README map-matches-territory (decision D43): reconcile the README's
    # authoritative counts and roster against the real skills on disk.
    real_count = len(skills)
    real_names = {s.name for s in skills}
    check_readme_counts(real_count, rep)          # HARD
    check_readme_family_roster(real_count, rep)   # HARD
    check_roster_flagships_exist(real_names, rep)  # WARN
    check_roles_table_present(rep)                 # WARN

    for w in rep.warnings:
        print(f"WARN  {w}")
    for e in rep.errors:
        print(f"ERROR {e}")

    print()
    if rep.errors:
        print(f"FAILED: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
        return 1
    print(f"OK: {len(skills)} skill(s) valid, {len(rep.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
