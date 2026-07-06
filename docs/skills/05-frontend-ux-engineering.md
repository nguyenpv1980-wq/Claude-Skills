# Frontend & UX Engineering

Frontend skills for routes, components, state, accessibility, security, and usability.

These are product-agnostic, repeatable Claude skills. They are meant to become executable `SKILL.md` workflows, not one-off prompts.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 161 | Frontend Architecture Map | P0 | Map routes, layouts, providers, state, data hooks, permissions, and shared UI boundaries. |
| 162 | Component Boundary Design | P0 | Separate page, container, feature, shared, and primitive components with clear ownership. |
| 163 | Design System Token Governance | P1 | Use semantic tokens for color, spacing, typography, state, and theme behavior. |
| 164 | Route Protection Design | P0 | Implement auth, role, onboarding, and admin gates consistently across routes. |
| 165 | Frontend Authorization Guard | P0 | Prevent unauthorized actions in UI while relying on backend enforcement as source of truth. |
| 166 | Form Architecture Design | P1 | Use validation, defaults, dirty state, submit state, error mapping, and accessibility consistently. |
| 167 | Server State Management | P1 | Design caching, invalidation, optimistic updates, stale time, retries, and loading boundaries. |
| 168 | Client State Boundary Review | P1 | Avoid overusing global state and place local, URL, cache, and persistent state intentionally. |
| 169 | URL State Architecture | P1 | Represent filters, tabs, search, sort, pagination, and dialogs in shareable URLs when useful. |
| 170 | Error Boundary Strategy | P1 | Wrap risky pages and components with graceful failure states and diagnostic context. |
| 171 | Empty State Design | P1 | Provide useful empty, loading, permission-denied, offline, failed, and no-result states. |
| 172 | Responsive Layout Review | P1 | Ensure layouts work across desktop, tablet, mobile, narrow screens, and embedded previews. |
| 173 | Accessibility Review | P0 | Check labels, focus, keyboard navigation, dialogs, contrast, announcements, and semantic HTML. |
| 174 | Frontend Performance Review | P1 | Inspect bundle size, lazy loading, render cost, memoization, waterfalls, and large lists. |
| 175 | Offline UX Design | P2 | Design queueing, sync status, conflict handling, and user messaging for offline-capable apps. |
| 176 | PWA Boundary Review | P2 | Validate service worker registration, cache strategy, updates, install prompt, and production-only behavior. |
| 177 | Notification UX Design | P2 | Design read/unread, dismiss, archive, preferences, grouping, priority, and digest behavior. |
| 178 | Frontend Security Review | P0 | Review XSS, sensitive data in browser, public env vars, storage use, and unsafe direct writes. |
| 179 | Visual Regression Readiness | P2 | Identify stable screens and states suitable for screenshots or visual diff testing. |
| 180 | Frontend QA Harness Design | P1 | Design component, route, URL-state, accessibility, and E2E coverage for frontend changes. |

## Skill implementation standard

When this category is converted into executable skills, each `SKILL.md` should include:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns / stop conditions
