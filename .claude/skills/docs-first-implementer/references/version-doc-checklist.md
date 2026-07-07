# Version & Docs Lookup Checklist

Supporting detail for `docs-first-implementer`. Read on demand.

## Where the LOCKED version lives, per ecosystem

| Ecosystem | Range (do not trust) | Resolved version (trust) |
| --- | --- | --- |
| Node/npm | `package.json` dependencies | `package-lock.json` → `packages` entry; `npm ls <pkg>` |
| Node/pnpm | `package.json` | `pnpm-lock.yaml`; `pnpm why <pkg>` |
| Node/yarn | `package.json` | `yarn.lock`; `yarn why <pkg>` |
| Python/pip | `requirements.txt` (if ranged) | `pip show <pkg>`; `requirements.txt` when fully pinned |
| Python/poetry | `pyproject.toml` | `poetry.lock`; `poetry show <pkg>` |
| Python/uv | `pyproject.toml` | `uv.lock`; `uv pip show <pkg>` |
| Go | `go.mod` require | `go.mod` (pinned) + `go list -m <mod>` |
| .NET | `*.csproj` PackageReference | `packages.lock.json` if present; `dotnet list package` |
| Ruby | `Gemfile` | `Gemfile.lock`; `bundle info <gem>` |
| Rust | `Cargo.toml` | `Cargo.lock`; `cargo tree -p <crate>` |

Transitive-vs-direct check (Node): `npm ls <pkg>` shows every resolved copy;
if two majors appear, find which one the failing/target import actually
resolves to before reading any changelog.

## Doc-source preference order

1. **Versioned official docs** — use the site's version switcher; a URL
   without an explicit version serves "latest" and lies about older installs.
2. **The installed package itself** — `node_modules/<pkg>/README.md`,
   `docs/`, and the `.d.ts` type definitions (types are the most honest API
   spec available offline). Python: `site-packages/<pkg>/`, `help(obj)`.
3. **Changelog / migration guide bridging** — when docs exist only for a
   different version, read `CHANGELOG.md` or GitHub releases between the
   documented version and the installed one; note every touched API.
4. **Source code of the installed package** — last resort, but authoritative;
   read the exported function's actual signature.

Record which rung was used. Rung 3 and 4 usage belongs in "unverified
assumptions" if any gap remains.

## Changelog-bridging tactics

- Search the changelog for the exact symbol names you plan to call.
- Breaking changes cluster at majors, but deprecations and default-value
  changes hide in minors — scan minor entries for "deprecat", "default",
  "renamed", "removed".
- If the bridge spans a major, look for an official migration guide first;
  reconstructing a major migration from raw changelog entries is error-prone
  and should be flagged as risk.

## Repo-precedent scan

Before writing new usage, search for existing imports of the library:
an established wrapper (`lib/redis.ts`, `utils/http_client.py`) means new
code goes through the wrapper. Bypassing it is an architectural deviation to
surface, not a shortcut. Also check for project-level config (retry policy,
base URLs, serializers) the wrapper applies — duplicating it inline drifts.
