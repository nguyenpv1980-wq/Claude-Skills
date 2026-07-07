# Supply-Chain Checklist — CI/CD paths, triage, pinning, provenance

Progressive-disclosure detail for `supply-chain-security-reviewer`. SLSA-style
framing: care about provenance (where artifacts came from) and integrity (that
they weren't tampered), not just CVE counts.

## Reachability triage rubric (for scanner output)

For each flagged CVE / advisory:

1. Is the vulnerable package a **direct** or **transitive** dep? (from lockfile)
2. Is the vulnerable **code path called** by this project, or only present?
3. Is it a **runtime**, **build/dev-only**, or **test-only** dependency?
4. Is there a **fixed version**, and does upgrading break anything?

Sort into:
- **TP-reachable** — called on a real path → severity per impact.
- **TP-latent** — present but unreachable → low/informational, note for hygiene.
- **False-positive** — not applicable (wrong OS, unused feature) → dismiss with reason.
- **Duplicate** — same root advisory via multiple paths → collapse.

Presence ≠ exploitability. A "critical" in an unreachable dev dep can rank
below a "moderate" in a reachable parser.

## CI/CD compromise-path catalog

| Path | Signal | Remediation |
|---|---|---|
| Untrusted trigger + secrets | `pull_request_target` (or self-hosted runner) that checks out PR code AND has secrets available | Split: untrusted build without secrets; privileged step on trusted code only |
| Over-broad token | `permissions: write-all` or default broad `GITHUB_TOKEN` | Least-privilege `permissions:` per job |
| Unpinned third-party action | `uses: someorg/action@v3` (mutable tag) | Pin to full commit SHA; review the SHA'd code |
| Secret in logs/artifacts | secrets echoed, or uploaded in build artifacts | Mask; never upload secrets; scope artifact reads |
| Cache poisoning | shared cache key writable by untrusted jobs | Scope cache keys; don't restore untrusted caches into trusted jobs |
| Script injection | `${{ github.event.* }}` interpolated into `run:` shell | Pass via env, quote; never inline untrusted event data |

## Install/build execution review

- Enumerate `postinstall`/`preinstall`/`prepare` (npm), `build.rs` (cargo),
  `setup.py`/build hooks (python), Dockerfile `RUN`, Makefile targets.
- Flag: remote downloads (`curl | sh`, fetching a blob), obfuscated/encoded
  commands, credential/env access, network calls during install.
- These run with developer or CI privileges BEFORE tests — treat as code exec.

## Dependency-specific risk

- **Typosquatting:** name close to a popular package (`reqests`, `lodahs`).
- **Dependency confusion:** an internal package name also resolvable on a
  public registry → attacker publishes higher version. Check registry/scope
  config, not just the lockfile.
- **Maintainer/abandonment:** sudden new maintainer, long-dead package
  suddenly updated, or unmaintained package on a critical path.
- **Surface bloat:** heavy/native deps for trivial needs widen the attack
  surface.

## Pinning & provenance checks

- Lockfile committed and used in CI (`npm ci`, `--frozen-lockfile`)?
- Integrity hashes present (subresource/`integrity`, `go.sum`, hash-pinned
  requirements)?
- Third-party actions pinned to commit SHA?
- Vendored binaries: documented source + checksum, or unexplained?
- Releases signed/attested (Sigstore/provenance) where the ecosystem supports
  it? Frame maturity with SLSA levels (source→build→provenance→hardened).

## HIGH-severity gate

A HIGH/CRITICAL finding must state a compromise path: weakness → attacker
action → **code execution or secret theft**. Reachable runtime exploit,
install-time script execution, or an untrusted-CI-to-secret path qualifies. A
latent unreachable CVE does not — rank it low and say why.

## Handoffs

- First-party SAST/CodeQL findings → `static-analysis-reviewer`.
- Applying an upgrade/CI change → separate classified, approved change.
