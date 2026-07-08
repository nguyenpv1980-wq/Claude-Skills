# Architecture Style Sheet

Detail for `architecture-advisor`. Read on demand.

## Need-interview checklist (BEFORE advising)

- [ ] Domain / problem shape.
- [ ] Load & traffic shape (steady? spiky? scale?).
- [ ] Team size + number of teams.
- [ ] **Operational maturity** (can they run distributed systems?).
- [ ] Deployment/hosting constraints.
- [ ] Scaling & change expectations over a realistic horizon.
- [ ] Consistency / latency needs.
- [ ] Existing estate (if migration) + what actually hurts today.

No recommendation before this. Interviewing IS the task if unknown.

## Per-style fit factors

| Style | Fits when | Cost / risk |
|---|---|---|
| Monolith | Small team, early, simple | Scaling/team contention later |
| Modular monolith | Most teams; want boundaries w/o distribution | Discipline to keep modules clean |
| Microservices | Many teams, high ops maturity, independent scaling need | Large permanent operational premium |
| Event-driven | Async workflows, decoupling, fan-out | Eventual consistency; debugging complexity |
| Serverless | Spiky/low baseline load, small ops team | Cold starts, vendor lock, limits |
| SOA | Enterprise integration of coarse services | Heavier governance |
| Hybrid | Carve out only what needs it | Boundary clarity matters |

## Trend-trap warnings

- **Microservices premium:** distributed tracing, network failure
  handling, deploy orchestration, cross-service data consistency — a large
  PERMANENT tax. Only worth it when the team can pay it and genuinely needs
  independent scaling/deployment.
- **Distributed monolith:** services split physically but coupled
  logically — every change touches several, nothing deploys independently.
  Worse than the monolith it replaced. The most common bad outcome.
- **Contrarian trend-avoidance:** reflexively refusing microservices is as
  unprincipled as reflexively adopting them. Fit, not stance.
- **Modular monolith is underrated:** most boundary benefits, none of the
  distribution tax, splittable later on evidence. Recommend the boring
  option when it fits — and it fits often.

## Recommendation must include

1. Only the relevant candidates (2–4).
2. Case-specific pros/cons (tied to the interview).
3. A clear recommendation WITH reasoning.
4. **Sensitivity:** what would change it (team growth, traffic ×N,
   isolation need for one component).

## Handoffs

- Concrete component/dependency map + migration → `architecture-designer`.
- Cloud provider/posture → `cloud-architecture-decider`.
- Tenancy structure/isolation → `saas-platform-architect`.
- Domain concepts/boundaries → `domain-modeler` (can inform style).
