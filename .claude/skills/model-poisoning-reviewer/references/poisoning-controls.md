# Data & model poisoning controls

Detail for `model-poisoning-reviewer`. OWASP LLM04 (Data and Model Poisoning),
2025. Scope: pipelines YOU run that shape behavior. Acquired artifacts →
`supply-chain-security-reviewer`.

## Contributor-trust rubric

Poisoning risk tracks who can put data into a behavior-shaping pipeline:

| Contributor | Risk |
|---|---|
| Trusted, curated internal only | low |
| Authenticated customers/tenants | medium (abuse + volume) |
| Public users / open feedback | high (attacker-reachable) |
| Scraped web / open datasets | high (uncontrolled provenance) |

The high rows are the primary poisoning surface; controls scale with risk.

## Per-pipeline poisoning paths

### Training / fine-tuning
- Poisoned samples: attacker gets crafted examples into the dataset →
  targeted misbehavior / backdoor.
- Label flipping: corrupting labels in crowd/user-sourced data.
- Controls: source provenance + audit trail; curation/review before use;
  label-integrity checks; outlier/poison detection; a holdout/canary + 
  adversarial-trigger evaluation that would catch a behavior shift BEFORE
  shipping (aggregate accuracy won't).

### Feedback loops (RLHF / thumbs / corrections)
- Sybil/coordinated signaling: a group mass-upvotes bad answers or submits
  coordinated "corrections" to steer the next update (e.g. promote a scam URL).
- Controls: identity + rate limits on feedback; anomaly detection on feedback
  distributions; HUMAN REVIEW before feedback becomes training data; never
  auto-train on raw open feedback.

### Ingestion → retrieval-as-truth
- Poisoned document: attacker plants content engineered to rank for a target
  query, steering answers (integrity) — separate from retrieval authz.
- Injection payload in a document: hand the "content acts as instructions"
  half to `prompt-injection-defender`; the "content is treated as ground
  truth" half is here.
- Controls: source trust classification; validation before indexing; the
  ability to PURGE poisoned content AND roll back the index/update it caused;
  provenance metadata per document.

## Backdoor / trigger-phrase risk

- A fine-tuned or feedback-updated model can carry a backdoor: benign until a
  trigger phrase appears, then misbehaves. Small poison fractions suffice and
  don't move average metrics.
- Controls: provenance of all tuning data; evaluation on suspected adversarial
  triggers; prefer trusted-curated tuning data.

## Provenance & curation (backbone)

- Every training/ingested item traces to a trusted source with an audit trail.
- Data you can't trace can't be trusted to train on — quarantine or exclude.
- Curation gate: human/automated review before a dataset version is used;
  version datasets like code.

## Detection & monitoring

- Outlier/poison detection on incoming data; label-integrity checks.
- Holdout/canary evaluation gates each update; adversarial-trigger tests.
- Behavior-drift monitoring in production → `observability-operator`; a sudden
  quality/behavior shift after an update is a poisoning signal.
- Confirmed poisoning → `incident-response-runbook`; remediation (retrain,
  purge, rollback) is a classified, approved step.

## Boundary with supply-chain-security-reviewer

- **This skill (LLM04):** data you INGEST and pipelines you RUN — training
  data curation, feedback loops, RAG ingestion integrity.
- **supply-chain-security-reviewer (LLM03, extended per D6):** artifacts you
  ACQUIRE — third-party base models, downloaded datasets, fine-tuning adapters,
  their provenance and unsafe serialization.

State the boundary in the review; route acquired-artifact concerns across it.
