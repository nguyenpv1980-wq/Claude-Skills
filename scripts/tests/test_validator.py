#!/usr/bin/env python3
"""Self-tests for scripts/validate-skills.py (decision D55).

Run:  python scripts/tests/test_validator.py      # exit 0 = every assertion held

WHY THIS EXISTS
    validate-skills.py is the repo's single load-bearing merge gate, and until
    D55 it had no tests at all. Every hard check it grew — the D43 README count
    markers, the D50 strict-YAML / sentinel / block-scalar trio — was hand-proved
    once in a pull-request description and never proved again. This suite
    re-proves them on every CI run, so a later refactor cannot quietly disarm
    one.

NO PYTEST, DELIBERATELY
    The repo's entire dependency surface is one package (PyYAML), and the
    validator fails closed without it. Adding a test framework to test one
    script would invert that minimalism. Plain asserts suffice: the first
    failure prints and exits non-zero.

PROVING THE SUITE CAN FAIL
    A check nobody has watched fail is an assertion, not a gate. Every bad
    fixture here is paired with the specific error text it must produce. To
    confirm the suite is really wired to the validator, neuter one check and
    re-run: comment out the `rep.error(...)` call inside
    check_description_not_block_scalar() and the two block-scalar cases go red
    immediately. Any other check can be checked the same way.

IMPORT WRINKLE
    validate-skills.py is hyphenated, so `import validate_skills` cannot reach
    it; it is loaded by path through importlib below.
"""
from __future__ import annotations

import importlib.util
import sys
from contextlib import contextmanager
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
FIXTURES = TESTS_DIR / "fixtures"
VALIDATOR_PATH = TESTS_DIR.parent / "validate-skills.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("aegis_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load the validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = _load_validator()

# Every satisfied expectation appends its label here, so the run ends with a
# count rather than a bare "no news is good news".
PASSES: list[str] = []


def expect_error(rep, needle: str, label: str) -> None:
    """Assert the report contains an error mentioning `needle`, and show it."""
    hits = [e for e in rep.errors if needle in e]
    if not hits:
        raise AssertionError(
            f"{label}\n    expected an error containing {needle!r}\n"
            f"    got: {rep.errors or '[]'}"
        )
    PASSES.append(label)
    fired = hits[0] if len(hits[0]) <= 132 else hits[0][:129] + "..."
    print(f"  PASS  {label}")
    print(f"        fired: {fired}")


def expect_clean(rep, label: str) -> None:
    """Assert the report is error-free."""
    if rep.errors:
        raise AssertionError(f"{label}\n    expected no errors\n    got: {rep.errors}")
    PASSES.append(label)
    print(f"  PASS  {label} (no errors)")


@contextmanager
def readme_at(path: Path):
    """Point the validator's README constant at a fixture for one block."""
    original = validator.README
    validator.README = path
    try:
        yield
    finally:
        validator.README = original


# --- existing hard checks (the D50 trio) ------------------------------------


def test_strict_yaml_parse():
    """D50: frontmatter must parse under a spec-strict YAML parser."""
    good = "name: good-skill\ndescription: 'Does a thing: carefully, on one line.'\n"
    rep = validator.Report()
    parsed = validator.check_frontmatter_strict_yaml(good, "good-skill", rep)
    expect_clean(rep, "strict-YAML accepts a single-quoted description containing ': '")
    assert parsed["description"] == "Does a thing: carefully, on one line.", (
        "the parsed value must have its quoting stripped"
    )

    bad = "name: bad-skill\ndescription: Does a thing: carelessly, unquoted.\n"
    rep = validator.Report()
    parsed = validator.check_frontmatter_strict_yaml(bad, "bad-skill", rep)
    expect_error(
        rep,
        "does not parse as strict YAML",
        "strict-YAML rejects an unquoted ': ' (the 67-skill Codex drop, D49/D50)",
    )
    assert parsed is None, "a failed parse must return None, not a partial mapping"

    rep = validator.Report()
    validator.check_frontmatter_strict_yaml("- just\n- a list\n", "listy", rep)
    expect_error(rep, "must parse to a YAML mapping", "non-mapping frontmatter rejected")


def test_description_block_scalar():
    """D50 follow-up: a `description:` block scalar is forbidden pre-parse."""
    for marker in (">", "|"):
        fm = f"name: x\ndescription: {marker}\n  folded onto the next line\n"
        rep = validator.Report()
        validator.check_description_not_block_scalar(fm, "x", rep)
        expect_error(
            rep, "block scalar", f"block-scalar description '{marker}' rejected"
        )

    rep = validator.Report()
    validator.check_description_not_block_scalar(
        "name: x\ndescription: 'one quoted line'\n", "x", rep
    )
    expect_clean(rep, "a single-quoted description is not a block scalar")


def test_manual_only_sentinel_bidirectional():
    """D50: `disable-model-invocation` and the sentinel must agree both ways."""
    sentinel = validator.MANUAL_ONLY_SENTINEL
    assert len(sentinel) == 32, "the sentinel contract is exactly 32 chars"

    rep = validator.Report()
    validator.check_manual_only_sentinel(
        "x", {"disable-model-invocation": True}, "Does a thing.", rep
    )
    expect_error(
        rep,
        "does not START with the exact sentinel",
        "field -> sentinel: manual-only skill missing the sentinel is rejected",
    )

    rep = validator.Report()
    validator.check_manual_only_sentinel("x", {}, sentinel + "Does a thing.", rep)
    expect_error(
        rep,
        "would auto-invoke a skill whose text forbids it",
        "sentinel -> field: sentinel without the field is rejected",
    )

    rep = validator.Report()
    validator.check_manual_only_sentinel(
        "x", {"disable-model-invocation": True}, sentinel + "Does a thing.", rep
    )
    expect_clean(rep, "field + sentinel agreeing is accepted")

    rep = validator.Report()
    validator.check_manual_only_sentinel("x", {}, "Does a thing.", rep)
    expect_clean(rep, "an ordinary auto-invocable skill is accepted")


# --- existing hard checks (the D43 README markers) --------------------------


def test_readme_count_markers():
    """D43: the marked counts must reconcile with the real skills on disk."""
    with readme_at(FIXTURES / "readme" / "good.md"):
        rep = validator.Report()
        validator.check_readme_counts(5, rep)
        validator.check_readme_family_roster(5, rep)
        expect_clean(rep, "README fixture reconciles (SKILL-COUNT 5, 2+2 families +1)")

    with readme_at(FIXTURES / "readme" / "bad-skill-count.md"):
        rep = validator.Report()
        validator.check_readme_counts(5, rep)
        expect_error(
            rep, "SKILL-COUNT marker says", "stale SKILL-COUNT marker rejected"
        )

    with readme_at(FIXTURES / "readme" / "bad-family-sum.md"):
        rep = validator.Report()
        validator.check_readme_family_roster(5, rep)
        expect_error(
            rep, "family counts sum to", "roster family counts out of sync rejected"
        )

    with readme_at(FIXTURES / "readme" / "good.md"):
        rep = validator.Report()
        validator.check_readme_family_roster(99, rep)
        expect_error(
            rep,
            "family counts sum to",
            "roster that no longer matches the disk count is rejected",
        )


# --- existing hard checks (whole-skill paths) -------------------------------


def test_skill_end_to_end():
    """The per-skill path over real fixture directories on disk."""
    rep = validator.Report()
    name = validator.validate_skill(FIXTURES / "skills" / "good-skill", rep)
    expect_clean(rep, "the canonical good fixture skill validates end to end")
    assert name == "good-skill", "validate_skill must return the skill name"

    rep = validator.Report()
    validator.validate_skill(FIXTURES / "skills" / "missing-section", rep)
    expect_error(
        rep,
        "missing required section(s): Stop Conditions",
        "a skill missing a required section is rejected",
    )

    rep = validator.Report()
    validator.validate_skill(FIXTURES / "skills" / "long-description", rep)
    expect_error(
        rep,
        "chars (parsed value; must be < 1024)",
        "a description over the parsed-length ceiling is rejected",
    )

    rep = validator.Report()
    validator.validate_skill(FIXTURES / "skills" / "no-such-fixture", rep)
    expect_error(rep, "missing SKILL.md", "a skill directory without SKILL.md is rejected")


# --- checks added by decision D55 -------------------------------------------


def _body(sections) -> str:
    """Build a SKILL.md body carrying exactly these `##` sections, in order."""
    return "\n".join(f"## {s}\n\nprose\n" for s in sections)


def test_section_order():
    """D55: the required sections must appear in the canonical order."""
    canonical = list(validator.REQUIRED_SECTIONS)

    rep = validator.Report()
    validator.check_section_order(_body(canonical), "x", rep)
    expect_clean(rep, "canonical section order accepted")

    interleaved = canonical[:6] + ["Safety Rules"] + canonical[6:]
    rep = validator.Report()
    validator.check_section_order(_body(interleaved), "x", rep)
    expect_clean(rep, "an optional section (Safety Rules) may interleave freely")

    scrambled = [s for s in canonical if s != "Gotchas"]
    scrambled.insert(scrambled.index("Workflow"), "Gotchas")
    rep = validator.Report()
    validator.check_section_order(_body(scrambled), "x", rep)
    expect_error(rep, "out of order", "Gotchas written before Workflow is rejected")

    rep = validator.Report()
    validator.check_section_order(_body(canonical + ["Workflow"]), "x", rep)
    expect_error(
        rep,
        "duplicate required section header",
        "a required section written twice is rejected",
    )

    assert validator.ordered_headers("## B\n## A\n## B\n") == ["B", "A", "B"], (
        "ordered_headers must preserve both order and duplicates"
    )
    assert validator.section_headers("## B\n## A\n## B\n") == {"A", "B"}, (
        "section_headers must remain the set twin of ordered_headers"
    )

    # ...and the check must be WIRED into the per-skill path, not merely defined.
    rep = validator.Report()
    validator.validate_skill(FIXTURES / "skills" / "out-of-order-sections", rep)
    expect_error(
        rep, "out of order", "the scrambled fixture skill is rejected end to end"
    )
    assert not any("missing required section" in e for e in rep.errors), (
        "the scrambled fixture has all nine sections; only ORDER may fire"
    )


def test_agents_schema():
    """D55: .claude/agents/*.md must strict-parse and stay read-only."""
    agents = FIXTURES / "agents"

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "good")
    expect_clean(rep, "an agent granting only Read, Grep, Glob is accepted")

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "widened-tools")
    expect_error(
        rep,
        "beyond the read-only set",
        "`tools: Read, Write` is rejected as a privilege escalation",
    )

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "name-mismatch")
    expect_error(
        rep, "!= filename stem", "an agent whose name disagrees with its file is rejected"
    )

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "bad-model")
    expect_error(rep, "is not one of", "an unrecognised model is rejected")

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "no-such-directory")
    expect_clean(rep, "a missing agents directory degrades quietly")

    # That graceful degrade is also how this check could silently become a
    # no-op, so pin the real surface: the directory must exist, be non-empty,
    # and conform.
    shipped = list(validator.AGENTS_DIR.glob("*.md"))
    assert shipped, f"expected agent files under {validator.AGENTS_DIR}"
    rep = validator.Report()
    validator.check_agents_schema(rep)
    expect_clean(rep, f"all {len(shipped)} shipped reviewer agents conform")


def test_docs_paths_links():
    """D55: guided-path and README picker links must resolve."""
    tree = FIXTURES / "paths-tree"
    good_paths, good_readme = tree / "docs" / "paths", tree / "README-good.md"

    rep = validator.Report()
    validator.check_docs_paths_links(rep, good_paths, good_readme)
    expect_clean(rep, "resolving path links and a resolving picker are accepted")

    rep = validator.Report()
    validator.check_docs_paths_links(rep, tree / "docs" / "paths-dangling", good_readme)
    expect_error(
        rep, "which does not exist on disk", "a dangling SKILL.md link is rejected"
    )

    rep = validator.Report()
    validator.check_docs_paths_links(rep, tree / "docs" / "paths-mismatch", good_readme)
    expect_error(
        rep,
        "does not match its target skill",
        "a resolving link whose label names a DIFFERENT skill is rejected",
    )

    rep = validator.Report()
    validator.check_docs_paths_links(rep, good_paths, tree / "README-dangling.md")
    expect_error(
        rep,
        "which does not exist on disk",
        "a README picker pointing at a missing path doc is rejected",
    )

    # Pin the real surface, so a mis-pathed PATHS_DIR cannot make this a no-op.
    shipped = list(validator.PATHS_DIR.glob("*.md"))
    assert shipped, f"expected guided-path docs under {validator.PATHS_DIR}"
    linked = sum(
        len(validator.PATH_SKILL_LINK.findall(d.read_text(encoding="utf-8")))
        for d in shipped
    )
    assert linked, "expected the shipped guided paths to contain SKILL.md links"
    rep = validator.Report()
    validator.check_docs_paths_links(rep)
    expect_clean(
        rep, f"all {linked} links across {len(shipped)} shipped guided paths resolve"
    )


def test_workflows_sha_pinned():
    """D55: every action must be pinned to a full 40-hex commit SHA."""
    workflows = FIXTURES / "workflows"

    rep = validator.Report()
    validator.check_workflows_sha_pinned(rep, workflows / "pinned")
    expect_clean(
        rep,
        "a 40-hex pin with a trailing `# vX.Y.Z`, plus a local action, is accepted",
    )

    rep = validator.Report()
    validator.check_workflows_sha_pinned(rep, workflows / "floating")
    expect_error(
        rep, "actions/checkout@v7", "a floating tag `@v7` is rejected"
    )
    expect_error(
        rep, "actions/setup-python@ece7cb0", "an abbreviated SHA is rejected too"
    )

    # Pin the real surface: the workflows directory must exist and actually
    # contain action references, or this check could pass by scanning nothing.
    shipped = [
        p
        for p in validator.WORKFLOWS_DIR.iterdir()
        if p.suffix in (".yml", ".yaml")
    ]
    assert shipped, f"expected workflows under {validator.WORKFLOWS_DIR}"
    refs = sum(
        1
        for p in shipped
        for line in p.read_text(encoding="utf-8").splitlines()
        if validator.USES_ACTION_REF.match(line.split("#", 1)[0])
    )
    assert refs, "expected the shipped workflows to reference actions"
    rep = validator.Report()
    validator.check_workflows_sha_pinned(rep)
    expect_clean(rep, f"all {refs} shipped action references are SHA-pinned")


TESTS = [
    test_strict_yaml_parse,
    test_description_block_scalar,
    test_manual_only_sentinel_bidirectional,
    test_readme_count_markers,
    test_skill_end_to_end,
    test_section_order,
    test_agents_schema,
    test_docs_paths_links,
    test_workflows_sha_pinned,
]


def main() -> int:
    if validator.yaml is None:
        print(
            "ERROR PyYAML is required to exercise the strict frontmatter parse; "
            "install it with: python -m pip install -r requirements.txt"
        )
        return 1

    print(f"Self-testing {VALIDATOR_PATH.name} ...\n")
    for test in TESTS:
        summary = (test.__doc__ or "").strip().splitlines()[0]
        print(f"{test.__name__} - {summary}")
        try:
            test()
        except AssertionError as exc:
            print(f"  FAIL  {exc}")
            print(f"\nFAILED after {len(PASSES)} passing assertion(s).")
            return 1
        print()

    print(f"OK: {len(PASSES)} validator self-test assertion(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
