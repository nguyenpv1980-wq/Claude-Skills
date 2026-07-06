# Backend, API & Data Engineering

Backend skills for commands, APIs, database design, integrations, jobs, and data integrity.

These are product-agnostic, repeatable Claude skills. They are meant to become executable `SKILL.md` workflows, not one-off prompts.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 131 | Command Handler Design | P0 | Design protected mutations with validation, auth, authorization, idempotency, audit, and safe errors. |
| 132 | Query Handler Design | P0 | Design read paths that enforce scope, filtering, pagination, redaction, and performance constraints. |
| 133 | REST API Design | P1 | Design predictable resources, methods, status codes, errors, pagination, filtering, and versioning. |
| 134 | RPC API Design | P1 | Design command-style endpoints with explicit inputs, outputs, authorization, and transaction semantics. |
| 135 | GraphQL Boundary Review | P2 | Review schema design, N+1 risks, authorization, field-level access, query depth, and cost limits. |
| 136 | Schema Design Review | P0 | Review tables, keys, constraints, indexes, nullability, defaults, and ownership semantics. |
| 137 | Migration Script Authoring | P0 | Create safe forward migrations with prechecks, constraints, indexes, grants, policies, and verification. |
| 138 | Data Backfill Design | P1 | Plan idempotent backfills with batching, checkpoints, safety gates, and rollback strategy. |
| 139 | Index Strategy Review | P1 | Design indexes based on query patterns, tenant filters, cardinality, write cost, and migration risk. |
| 140 | Pagination Strategy Design | P1 | Choose offset, cursor, keyset, or time-window pagination based on consistency and scale needs. |
| 141 | Validation Schema Design | P0 | Create shared or boundary-specific schemas for input validation and type-safe parsing. |
| 142 | Error Handling Middleware | P1 | Centralize safe error mapping, logging, correlation, and user-facing response shapes. |
| 143 | Rate Limit Middleware | P1 | Protect APIs with scoped limits and clear retry semantics. |
| 144 | Idempotency Key Middleware | P0 | Support safe retries with request keys, payload hashes, actor scope, and terminal response replay. |
| 145 | Webhook Intake Pipeline | P1 | Validate, persist, deduplicate, process, retry, and audit incoming external events. |
| 146 | Outbound Integration Adapter | P1 | Wrap third-party calls with timeouts, retries, circuit breakers, logging, and contract tests. |
| 147 | Background Job Design | P1 | Define queueing, schedules, locks, retries, dead letters, visibility, and operational ownership. |
| 148 | Cron Job Safety Review | P1 | Ensure scheduled jobs are idempotent, scoped, observable, and safe across timezones and retries. |
| 149 | File Upload Backend Design | P1 | Validate type, size, ownership, storage path, scanning, metadata, and lifecycle. |
| 150 | Data Import Backend Design | P1 | Implement inspect, map, preview, confirm, write, audit, and rollback-safe import flows. |
| 151 | Data Export Backend Design | P2 | Implement authorized export jobs with redaction, expiration, status tracking, and audit. |
| 152 | Search Backend Design | P1 | Design tenant-scoped indexing, filtering, ranking, highlighting, and permissions enforcement. |
| 153 | Realtime Subscription Design | P1 | Scope channels, filters, payloads, authorization, and connection lifecycle safely. |
| 154 | Cache Key Design | P1 | Create tenant-safe cache keys and invalidation paths for server and client caches. |
| 155 | Concurrency Race Review | P0 | Identify race conditions in creates, updates, approvals, imports, retries, and background jobs. |
| 156 | Transaction Scope Design | P1 | Keep transactions small, correct, and aligned with business invariants. |
| 157 | Data Integrity Constraint Review | P0 | Use constraints, uniqueness, checks, foreign keys, and not-null rules to protect invariants. |
| 158 | Edge Function Design | P1 | Design serverless functions with auth, environment validation, timeouts, cold start awareness, and logging. |
| 159 | API Compatibility Test Design | P1 | Protect API contracts from breaking existing clients and automation. |
| 160 | Backend Observability Hooks | P1 | Emit logs, metrics, traces, audit events, and correlation IDs from backend boundaries. |

## Skill implementation standard

When this category is converted into executable skills, each `SKILL.md` should include:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns / stop conditions
