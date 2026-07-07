---
name: model-poisoning-reviewer
description: Review the integrity of the data and pipelines that shape a model's behavior against data and model poisoning (OWASP LLM04) — training and fine-tuning datasets (provenance, curation, who can contribute), RLHF/feedback loops (can attackers mass-signal bad behavior into the next update), the RAG/embedding INGESTION path (untrusted content indexed as ground truth, poisoned documents crafted to rank for targeted queries), and backdoor/trigger-phrase risk. Produces severity-ranked findings each with a poisoning path (attacker input → corrupted behavior) plus provenance/curation/validation controls. Composes supply-chain-security-reviewer for acquired models/datasets/adapters. Use when you train, fine-tune, collect feedback, or ingest external content into a knowledge base. Do NOT use for retrieval AUTHORIZATION (rag-security-architect), acquiring third-party model artifacts (supply-chain-security-reviewer), or injection at inference (prompt-injection-defender).
---

# Model Poisoning Reviewer

## Purpose

Review whether an attacker can corrupt a model's behavior by poisoning the
data or feedback that shapes it (LLM04). The scope is the pipelines you run
that influence what the model learns or treats as ground truth: training and
fine-tuning datasets, RLHF/feedback loops, and the RAG/embedding INGESTION
path (which turns external content into retrievable "truth"). The output is
severity-ranked findings, each with a concrete poisoning path (attacker input
→ corrupted behavior) and the provenance, curation, and validation controls
that close it. Acquisition of third-party models/datasets/adapters is
`supply-chain-security-reviewer`'s (extended per D6); this skill owns the data
you ingest and the pipelines you run.

## Use When

- Use when: you train or fine-tune a model, collect user feedback that shapes
  behavior (RLHF, thumbs up/down, correction data), or ingest external content
  into a knowledge base / embedding index.
- Use when: assessing whether attacker-controlled input can end up in training
  data or be indexed as authoritative and steer future outputs.
- Use when: reviewing dataset provenance, curation, and validation for a model
  pipeline.
- Do NOT use when: the concern is WHO can retrieve documents at query time
  (`rag-security-architect` — LLM08) — this skill is the INGESTION integrity
  half.
- Do NOT use when: acquiring a third-party base model, dataset, or adapter
  (`supply-chain-security-reviewer`) or defending inference-time injection
  (`prompt-injection-defender`).

## Inputs to Inspect

1. The training/fine-tuning pipeline: data sources, who/what can contribute,
   curation and labeling process, validation before a dataset is used.
2. Feedback loops: how user feedback (ratings, corrections, conversations) is
   collected and whether/how it flows into the next model update.
3. The ingestion path: what external content is indexed into the knowledge
   base/embedding store, from where, and whether it's treated as ground truth.
4. Data provenance: can you trace each training/ingested item to a trusted
   source; is there an audit trail.
5. Validation/anomaly detection: outlier/poison detection on incoming data,
   label-integrity checks, canary/holdout evaluation for behavior shifts.
6. Acquired artifacts (hand-off boundary): base models, public datasets,
   adapters — noted and routed to `supply-chain-security-reviewer`.

## Workflow

1. **Map the behavior-shaping pipelines.** Identify every path by which data
   influences the model: training, fine-tuning, feedback→update, and ingestion
   →retrieval-as-truth. No such pipeline (pure prompting over a fixed model) →
   most of this is not applicable; say so and Stop.
2. **Assess contributor trust.** For each pipeline, who can put data in? Public
   users, scraped web content, and open feedback are attacker-reachable and
   the primary poisoning surface. Trusted-curated-only is low risk. Use
   [references/poisoning-controls.md](references/poisoning-controls.md).
3. **Trace poisoning paths.** For each attacker-reachable input, write the
   path: attacker submits X → it enters dataset/feedback/index → next
   update/retrieval → corrupted behavior (misinformation, backdoor trigger,
   biased output, recommended-scam). Concrete path required for HIGH severity.
4. **Review training/fine-tuning integrity.** Provenance of every source,
   curation/review before use, label integrity (label-flip attacks), and a
   holdout/canary evaluation that would CATCH a behavior shift before it ships.
5. **Review feedback loops.** Can an attacker mass-signal (Sybil thumbs-up on
   bad answers, coordinated corrections) to steer the next update? Require
   rate/identity controls on feedback, human review before feedback becomes
   training data, and anomaly detection on feedback distributions.
6. **Review ingestion integrity.** External content indexed as ground truth is
   a poisoning vector: an attacker plants a document engineered to rank for a
   target query (steering answers) or to carry an injection payload (hand the
   payload half to `prompt-injection-defender`). Require source trust,
   validation, and the ability to purge/rollback poisoned content.
7. **Check backdoor/trigger risk.** For fine-tuned or feedback-updated models,
   consider trigger-phrase backdoors (benign until a phrase appears); recommend
   provenance + evaluation on adversarial triggers.
8. **Rank findings and define controls.** Each finding: poisoning path,
   severity (exploit-path gated), and controls (provenance tracking, curation
   gates, feedback identity/rate limits, anomaly detection, holdout eval,
   purge/rollback). Behavior-shift monitoring routes to `observability-operator`;
   confirmed poisoning to `incident-response-runbook`.

## Output Format

```
MODEL POISONING REVIEW — <system>
Behavior-shaping pipelines: <training | fine-tune | feedback→update | ingestion→truth>
Contributor trust: <pipeline → who can contribute → attacker-reachable?>
Findings (severity-ranked):
  [SEV] <pipeline> — Poisoning path: <attacker input → corrupted behavior>
    Controls: <provenance | curation gate | feedback id/rate | anomaly detect | holdout eval | purge/rollback>
Backdoor/trigger risk: <assessment for tuned/updated models>
Acquired-artifact handoff: <models/datasets/adapters → supply-chain-security-reviewer>
Behavior-shift monitoring: <canary/holdout + drift signals> (→ observability-operator)
Not applicable: <pipeline absent — reason> | Not reviewed: <+ why>
```

## Validation Checklist

- [ ] Every behavior-shaping pipeline (train/fine-tune/feedback/ingestion) is
      identified or explicitly ruled not-applicable.
- [ ] Contributor trust is assessed per pipeline; attacker-reachable inputs are
      the flagged surface.
- [ ] Each finding has a concrete poisoning path (attacker input → corrupted
      behavior); HIGH severity is exploit-path gated.
- [ ] Training/fine-tuning has provenance, curation, and a holdout/canary eval
      that would catch a behavior shift before shipping.
- [ ] Feedback loops have identity/rate controls and human review before
      feedback becomes training data.
- [ ] Ingestion treats external content's trust explicitly and can purge/
      rollback poisoned content.
- [ ] Acquired third-party artifacts are routed to
      `supply-chain-security-reviewer`, not assessed here.

## Security Rules

- Attacker-reachable data is untrusted training material: public contributions,
  scraped content, and open feedback can steer the model and must be curated,
  rate/identity-limited, and validated before they shape behavior.
- Provenance is the backbone control: data you can't trace to a trusted source
  can't be trusted to train on.
- A behavior shift must be catchable before it ships: a holdout/canary/
  adversarial-trigger evaluation gates updates.
- Ingested external content is not ground truth by default — indexing it as
  authoritative is a poisoning vector.

## Gotchas

- The feedback loop is the sneaky vector: "we retrain on thumbs-up answers"
  lets a coordinated group vote a scam or bias into the model. Rate/identity-
  limit and human-review feedback before it trains.
- Data poisoning is slow and quiet: a small fraction of poisoned samples can
  install a targeted backdoor without hurting aggregate metrics — average
  accuracy won't reveal it; adversarial-trigger evaluation might.
- Ingestion-as-truth: RAG indexing of open web/user content means an attacker
  who gets a document indexed can steer answers for a target query — this is
  poisoning (integrity), separate from retrieval authz (rag-security-architect).
- Label-flip attacks: poisoning the LABELS (not just inputs) in
  crowd/user-sourced training data is easy to miss without label-integrity
  review.
- Don't confuse with supply chain: a poisoned dataset you CURATED is this
  skill; a poisoned dataset/adapter you DOWNLOADED is
  supply-chain-security-reviewer. State the boundary.
- Purge without rollback is incomplete: if you can delete a poisoned document
  but not roll back the model/index update it caused, the corruption persists.

## Stop Conditions

- No training, fine-tuning, feedback, or ingestion pipeline exists (pure
  prompting over a fixed third-party model) — most of LLM04 is not applicable;
  state that and route any acquired-artifact concern to
  `supply-chain-security-reviewer`.
- A poisoning path is already exploited (corrupted behavior in production, a
  known-planted document steering answers) — route to
  `incident-response-runbook`; containment/rollback is a human decision.
- The concern is retrieval authorization, third-party artifact acquisition, or
  inference-time injection — hand to the owning skill.
- Remediation requires retraining, purging data, or rolling back a model —
  propose it; execution is a classified, approved step
  (`human-approval-boundary`).

## Supporting Files

- [references/poisoning-controls.md](references/poisoning-controls.md) — the
  contributor-trust rubric, per-pipeline poisoning paths (training/feedback/
  ingestion), provenance/curation/anomaly/holdout controls, backdoor-trigger
  notes, and the boundary with `supply-chain-security-reviewer`.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the data & retrieval
  cluster and against `rag-security-architect` and `supply-chain-security-reviewer`.
