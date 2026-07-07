# RLS Audit Checklist — per command, failure modes, negative tests

Progressive-disclosure detail for `rls-policy-auditor`. Postgres-oriented but
the reasoning transfers to any policy-based row security. Audit each table's
four commands separately; RLS enabled is not RLS enforced.

## Per-command audit questions

### SELECT (`USING`)
- Does the predicate require the caller's tenant scope on EVERY row?
- Is the scope from server context (`current_setting('request.jwt.claims')`,
  `auth.uid()`, session var set by the app) — not a client-passed column value?
- Any permissive policy that ORs in broader access (e.g. `USING (true)` for a
  role that end users can reach)?

### INSERT (`WITH CHECK`)
- Is there a `WITH CHECK` at all? Missing = any row can be inserted, including
  with another tenant's id → write-side hole.
- Does `WITH CHECK` force `tenant_id = <server-derived caller tenant>`?
- Can the client supply `tenant_id`/`owner_id` and have it honored?

### UPDATE (`USING` AND `WITH CHECK`)
- `USING` restricts WHICH rows can be updated (caller's tenant only)?
- `WITH CHECK` restricts the RESULTING row (can't move a row to another
  tenant)? Missing `WITH CHECK` = tenant hopping.

### DELETE (`USING`)
- Can the caller delete only their tenant's rows? Any role with unrestricted
  delete?

## Seven failure modes (detect → fix)

1. **Missing tenant scope** — policy predicate omits tenant. *Fix:* add
   `tenant_id = <server ctx>` to USING/WITH CHECK.
2. **Deny-by-default gap** — RLS enabled but a permissive policy reopens
   access, or a role has BYPASSRLS. *Fix:* restrictive policies; remove
   BYPASSRLS from request-path roles.
3. **Policy recursion** — policy calls a function that SELECTs the same table
   under RLS. *Fix:* mark helper `SECURITY DEFINER` with a pinned
   `search_path` and query a non-recursive source, or restructure.
4. **Unsafe SECURITY DEFINER** — DEFINER helper without `SET search_path`,
   broader than needed, or returning rows that bypass caller scope. *Fix:*
   pin `search_path`, least privilege, return only caller-scoped rows; prefer
   `SECURITY INVOKER` unless DEFINER is justified.
5. **Over-broad GRANT** — `GRANT ALL`/`GRANT … TO anon`/public. *Fix:* grant
   least privilege per role; anon gets only what's intentionally public.
6. **Service-role leakage** — `service_role`/superuser/BYPASSRLS reachable
   from user-influenced request handling, or its key exposed to the client.
   *Fix:* confine service role to trusted server jobs; never in client path.
7. **Frontend-derived scope** — tenant/user id taken from a client-controlled
   value. *Fix:* derive scope from verified session/JWT claims server-side.

## Negative-test session sequences (mandatory deliverable)

Express each as a session that sets the caller context, then attempts a
forbidden action, with the expected result. Include a positive control.

```sql
-- SELECT isolation
SET request.jwt.claims = '{"tenant_id":"A", "role":"member"}';
SELECT count(*) FROM invoices WHERE tenant_id = 'B';   -- EXPECT 0
SELECT count(*) FROM invoices WHERE tenant_id = 'A';   -- positive control: > 0

-- INSERT write-side
SET request.jwt.claims = '{"tenant_id":"A"}';
INSERT INTO invoices (tenant_id, amount) VALUES ('B', 100);  -- EXPECT rejected

-- UPDATE tenant hop
UPDATE invoices SET tenant_id = 'B' WHERE id = '<A-row>';     -- EXPECT rejected/0

-- DELETE cross-tenant
DELETE FROM invoices WHERE tenant_id = 'B';                   -- EXPECT 0 affected

-- anon / service-role
RESET request.jwt.claims;  -- anon
SELECT count(*) FROM invoices;                               -- EXPECT 0 (or only public)
```

Adapt the context-setting mechanism to the project (Supabase JWT claims,
`SET LOCAL app.tenant_id`, connection role, etc.). Every table × command that
matters gets a row; the not-audited list captures the rest.

## Handoffs

- Authored/corrected policies → deliver as a migration for
  `secure-migration-reviewer` + human approval; never apply live from here.
- App/API/cross-surface isolation tests → `multi-tenant-security-tester`.
