# Triage Rubric — dispositions, five-axis ranking, false-positive patterns

Progressive-disclosure detail for `static-analysis-reviewer`. A scanner hit is
a lead; the triage is the verdict.

## Dispositions

| Disposition | Meaning | Requires |
|---|---|---|
| True positive | Real defect confirmed in the code | Ranking + fix direction |
| False positive | Refuted by the code (safe path, unreachable, rule misfire) | The **code fact** that refutes it |
| Duplicate | Same root cause as another finding | Link to the kept finding |
| Accepted risk | Real but consciously accepted | Written rationale + owner + date + human sign-off |

"False positive" as a bare label is not acceptable — record the specific code
fact (e.g. "input passes through `escapeHtml()` at line 44 before the sink").

## Five-axis ranking (for true positives)

Rank each true positive; the highest axis usually sets severity, but combine:

1. **Reachability** — can an attacker's input reach this code?
   - reachable from an unauthenticated endpoint > authenticated > internal-only
     > dead/test/example code.
2. **Exploitability** — how hard to exploit?
   - trivial (single request) > needs conditions > needs local access /
     unlikely preconditions.
3. **Asset sensitivity** — what does it protect?
   - auth/credentials/money/PII/tenant data > business data > cosmetic.
4. **Tenant impact** — SaaS blast radius.
   - cross-tenant (all tenants) > single-tenant > per-user. Cross-tenant
     raises severity a level.
5. **Business impact** — regulatory, reputational, contractual exposure.

### HIGH/CRITICAL gate
A high-ranked finding states an exploit path: **who** reaches it, **how**,
**what they get**, and the **tenant blast radius**. A reachability question
alone (no demonstrated exploit) → cap at MEDIUM, mark "needs-verification".

## Common false-positive patterns by rule class

| Rule class | Frequent FP cause | Confirm by |
|---|---|---|
| SQL injection | ORM/param binding already used | Check the actual call is parameterized |
| XSS | Framework auto-escaping / sanitizer in path | Confirm output context + escaping |
| Path traversal | Input validated/normalized before use | Trace the normalization |
| Hardcoded secret | Test fixture / example / placeholder | Confirm it's not a real, live secret |
| Weak crypto | Non-security use (checksum, cache key) | Confirm the value isn't a security control |
| Deserialization | Trusted/internal source only | Confirm the source is not attacker-controlled |

Confirming a safe path means verifying the safe path is ACTUALLY taken — not
that a safe function exists somewhere in the file.

## Deduplication

Group by (rule id, sink) and by root cause. One vulnerability reported along N
data-flow paths is ONE finding with N paths of evidence — not N findings.

## Suppression-rationale format

```
SUPPRESS <rule id> @ <file:line>
Disposition: false-positive | accepted-risk
Reason (code fact / risk decision): <specific, auditable>
Owner: <who>   Date: <YYYY-MM-DD>   Sign-off: <human-approval-boundary ref, if accepted risk>
```

Blanket rules ("ignore all lows", "mute this rule everywhere") are not
rationales and rot the baseline.

## Scope honesty

Triaging scanner output is not a full security review — the scanner misses
whole classes (logic flaws, authz gaps it has no rule for). Say so; route
deeper needs to `security-pr-reviewer` (diff) or `threat-modeler` (design).
Fixes go to `appsec-implementer`.
