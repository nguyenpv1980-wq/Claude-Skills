#!/usr/bin/env python3
"""Verify every commit in a pull request is signed off under the DCO (decision D60).

Run (CI):    python scripts/check_dco.py --range "origin/main..<head-sha>"
Run (tests): python scripts/check_dco.py --stdin < records

WHY THIS EXISTS
    CONTRIBUTING.md has asked contributors to sign off every commit
    (`git commit -s`) since decision D58, which chose the Developer Certificate
    of Origin over a CLA. Until D60 that ask was a checklist item: nothing
    checked it, so nothing enforced it, and a checklist nobody verifies is a
    wish. This turns the ask into a check.

WHAT IS CHECKED, AND ON WHAT
    Every commit in the pull request's range must carry a well-formed
    `Signed-off-by: Name <email>` trailer. Checking only the tip commit would
    be theatre: a branch's second commit is exactly as unsigned as its first.

WHAT IS DELIBERATELY *NOT* CHECKED (decision D60)
    The sign-off email is NOT required to equal the author email. The stricter
    rule would break the recovery this script itself prints: `git rebase
    --signoff` signs as the person RUNNING the rebase (the committer), not as
    each commit's original author, so a maintainer relaying an outside patch
    would be told to run a command that cannot make the check pass. The DCO
    certifies that someone with the right to submit the code said so, and the
    trailer records who; enforcing author-identity equality is an
    authentication claim this check is not in a position to make (see the bot
    note below).

THE TRUSTED-BOT EXEMPTION (narrow, and deliberately so)
    Commits authored by exactly `dependabot[bot]` and `github-actions[bot]`,
    matched on their GitHub noreply author addresses, pass without a trailer.
    Both are machine authors that cannot execute the DCO's certification (there
    is no person to certify), and neither can be made to add the trailer, so
    without this exemption every dependency bump would arrive permanently red —
    turning a security-patch pipeline into a nuisance to be routed around.
    `.github/dependabot.yml` already documents the compensating control on the
    riskiest bot bumps (a bump touching the merge gate trips gate-guard and
    therefore needs a human admin merge); that reasoning is cited here, not
    restated.

    Honest limit: a commit's author field is SELF-ASSERTED, so this exemption
    is not an authentication boundary and is not offered as one. Anyone able to
    write a commit could claim a bot's address and skip the trailer. That buys
    an attacker nothing — adding `-s` is free, so the sign-off was never the
    obstacle — and what actually gates merge here is human review plus branch
    protection, not this script. The exemption is kept to two exact identities
    on GitHub's noreply domain so it cannot widen by accident.

FAIL-CLOSED ON AN EMPTY RANGE
    Zero commits is an ERROR, not a vacuous pass. A pull request always has at
    least one commit, so an empty range means the range was computed wrong —
    the precise way a green check can come to be examining nothing at all. The
    self-tests hold the same line for the validator's directory-scanning checks
    (decision D55).

MERGE COMMITS ARE SKIPPED
    CI passes `--no-merges`. On a `pull_request` event GitHub checks out a
    synthetic merge commit it authored itself, which no contributor can sign;
    branch merges inside a long-lived feature branch are likewise not anyone's
    certification to make. The workflow additionally ranges to the PR's real
    head SHA rather than to that synthetic merge ref.

No third-party dependencies: this runs before, and independently of, the
PyYAML install that scripts/validate-skills.py needs.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent

# ASCII unit/record separators. A commit message is free-form text containing
# newlines and blank lines, so a line-oriented `git log` format cannot be
# parsed back unambiguously; these two control bytes do not occur in practice.
FIELD_SEP = "\x1f"
RECORD_SEP = "\x1e"
GIT_LOG_FORMAT = f"%H{FIELD_SEP}%ae{FIELD_SEP}%an{FIELD_SEP}%B{RECORD_SEP}"

# The exemption list, in full. Two entries, both machine authors on GitHub's
# noreply domain. The optional `NNN+` prefix is the bot's numeric account id,
# which GitHub includes in the author address it writes.
EXEMPT_BOTS = ("dependabot[bot]", "github-actions[bot]")
EXEMPT_BOT_EMAIL_RES = tuple(
    re.compile(
        rf"^(?:\d+\+)?{re.escape(bot)}@users\.noreply\.github\.com$", re.IGNORECASE
    )
    for bot in EXEMPT_BOTS
)

# `git commit -s` writes exactly "Signed-off-by: Name <email>". Both an
# identity and an address are required: a bare "Signed-off-by:" line certifies
# nobody. The key is matched case-insensitively because a hand-typed trailer
# that differs only in case is a typo, not a refusal to certify.
SIGNOFF_RE = re.compile(
    r"^[ \t]*Signed-off-by:[ \t]*(?P<name>\S[^<>]*?)[ \t]*"
    r"<(?P<email>[^<>@\s]+@[^<>\s]+)>[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)

RECOVERY = """RECOVERY - add the missing sign-off, then force-push:
  one commit       git commit --amend -s
  several commits  git rebase --signoff origin/main
  then             git push --force-with-lease"""


class Commit(NamedTuple):
    """One commit as DATA, so the rules below can be tested without a repo."""

    sha: str
    author_email: str
    author_name: str
    message: str

    @property
    def short(self) -> str:
        return self.sha[:12]

    @property
    def subject(self) -> str:
        for line in self.message.splitlines():
            if line.strip():
                return line.strip()
        return "(empty commit message)"


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


# --- the rules, as pure functions over data ---------------------------------


def is_exempt_bot(author_email: str) -> bool:
    """True only for the two exempt machine authors. Everything else is human."""
    email = (author_email or "").strip()
    return any(rx.match(email) for rx in EXEMPT_BOT_EMAIL_RES)


def has_signoff(message: str) -> bool:
    """True if the message carries at least one well-formed DCO trailer."""
    return SIGNOFF_RE.search(message or "") is not None


def check_commits(commits: list[Commit], rep: Report) -> None:
    """Apply the DCO contract to a list of commit records."""
    if not commits:
        rep.error(
            "no commits found in the range - refusing to pass a check that "
            "examined nothing (a pull request always has at least one commit, "
            "so an empty range means the range itself is wrong)"
        )
        return

    for commit in commits:
        who = f"{commit.author_name} <{commit.author_email}>"
        if is_exempt_bot(commit.author_email):
            rep.note(f"EXEMPT  {commit.short}  {who}  {commit.subject}")
        elif has_signoff(commit.message):
            rep.note(f"SIGNED  {commit.short}  {who}  {commit.subject}")
        else:
            rep.error(
                f"{commit.sha} is NOT signed off - {who} - "
                f'"{commit.subject}" carries no valid "Signed-off-by:" trailer'
            )


# --- getting the records ----------------------------------------------------


def parse_records(text: str) -> list[Commit]:
    """Parse the GIT_LOG_FORMAT stream back into Commit records."""
    commits: list[Commit] = []
    for chunk in text.split(RECORD_SEP):
        chunk = chunk.strip("\r\n")
        if not chunk.strip():
            continue
        parts = chunk.split(FIELD_SEP)
        if len(parts) != 4:
            raise ValueError(
                f"malformed commit record: expected 4 fields, got {len(parts)}"
            )
        sha, email, name, message = parts
        commits.append(Commit(sha.strip(), email.strip(), name.strip(), message))
    return commits


def git_log_records(rev_range: str) -> str:
    """Read the commit range out of the real repository."""
    proc = subprocess.run(
        ["git", "log", "--no-merges", f"--format={GIT_LOG_FORMAT}", rev_range],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"ERROR git log failed for range {rev_range!r}:\n{proc.stderr.strip()}"
        )
    return proc.stdout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify DCO sign-off on every commit in a range (decision D60)."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--range",
        dest="rev_range",
        help="git revision range to check, e.g. origin/main..<head-sha>",
    )
    source.add_argument(
        "--stdin",
        action="store_true",
        help="read git-log records from stdin instead of a repository (test mode)",
    )
    args = parser.parse_args(argv)

    if args.stdin:
        source_label = "stdin"
        raw = sys.stdin.read()
    else:
        source_label = args.rev_range
        raw = git_log_records(args.rev_range)

    print(f"Checking DCO sign-off over {source_label} ...\n")

    try:
        commits = parse_records(raw)
    except ValueError as exc:
        print(f"ERROR {exc}")
        return 1

    rep = Report()
    check_commits(commits, rep)

    for note in rep.notes:
        print(f"  {note}")
    if rep.notes:
        print()
    for err in rep.errors:
        print(f"ERROR {err}")

    if rep.errors:
        print(f"\nFAILED: {len(rep.errors)} commit(s) missing a DCO sign-off.\n")
        print(RECOVERY)
        return 1

    print(f"OK: {len(commits)} commit(s) checked, all signed off or exempt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
