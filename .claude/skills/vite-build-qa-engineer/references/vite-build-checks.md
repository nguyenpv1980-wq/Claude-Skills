# Vite Build Check Recipes

Detail file for `vite-build-qa-engineer`. Loaded on demand.

## Bundle-grep recipe

Search classes, in order:

1. **Known secret VALUES:** for each server-side secret available in the
   build environment (from CI secret names / server env inventory), search
   `dist/` for the literal value. This catches `define` leaks and accidental
   imports the prefix audit misses.
2. **Patterns:** `sk_live_`, `sk_test_`, `-----BEGIN`, `AIza[0-9A-Za-z_-]{35}`,
   `eyJ[A-Za-z0-9_-]+\.eyJ` (JWTs), `postgres(ql)?://`, `AKIA[0-9A-Z]{16}`,
   generic `[A-Za-z0-9_]*(SECRET|PRIVATE|PASSWORD)[A-Za-z0-9_]*\s*[:=]`.
3. **Each inventoried VITE_ value:** confirm what actually shipped and where.

File classes: `dist/**/*.{js,mjs,css,html,json,map}` — sourcemaps included;
a secret only in the map is still shipped.

Claim discipline: report "none found by value+pattern search over <file
classes>" — never "no secrets in bundle" as an absolute.

## Parity walk checklist (vite preview)

- Direct-URL load of every top-level route and one deep nested route
  (SPA fallback / 404 behavior).
- Hard refresh mid-flow; browser back after navigation.
- Asset loading under configured `base` (images, fonts, lazy chunks —
  check the network panel for 404s on dynamic imports).
- Mode-dependent behavior: one check per env-driven feature flag/API base.
- Console: zero new errors relative to dev on the same routes.

Record: `vite build --mode <real>` + `vite preview` versions and flags.

## Budget & sourcemap snippets (CI-ready shape)

- Size budget: compare `dist/assets/*.js` gzip sizes against a checked-in
  budget file; fail on regression > threshold, print the diff table.
- Unexpected inclusion: fail if entry chunk contains modules matching a
  denylist (server-only SDKs, node builtins polyfilled by accident,
  devtools).
- Sourcemap policy: assert presence/absence of `*.map` and of
  `//# sourceMappingURL` in shipped JS matches the repo policy per mode.

Placement of these checks in PR/merge tiers: per the
`qa-automation-architect` blueprint.

## Public-vs-secret designation notes

Classify by provider designation, not vibes: publishable/browser keys
(analytics write keys, maps browser keys, payment publishable keys) are
public-by-design; server/secret keys never ship. When a provider key's class
is unknown, treat as secret-shaped and flag for confirmation.
