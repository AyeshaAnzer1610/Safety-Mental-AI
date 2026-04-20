# Safety Mental AI — Youth Mental Health Guardrail

A safety guardrail for the Kids Help Phone (KHP) virtual assistant that detects high-risk youth mental health conversations — including explicit crisis language, teen slang, coded suicidal ideation, and gradual emotional escalation across multi-turn dialogues in **English and French**.

Built by **Team 025** for the *Building Safer AI for Youth Mental Health* hackathon.

![AI Guardrail Challenge overview](hackathon_overall.png)

---

## Overview

Youth in crisis rarely use clinical language. They use slang ("unalive", "kms"), coded escape framing ("never want to wake up"), burden language ("better off without me"), or simply let distress build up across many turns. A single-keyword filter misses most of these; an LLM judge alone is slow and expensive.

This project pairs a **Cohere LLM judge** (with a KHP-specific safety prompt built from our stress-testing findings) with a **regex-based fallback stack** into a single **hybrid guardrail**. The regex stack catches known patterns in milliseconds; the LLM judge handles nuanced, multi-turn, and bilingual cases the regexes miss. If the LLM call fails, the regex stack still protects the user.

---

## How It Works

The entry point is `get_guardrails()` in [project/src/submission/submission.py](project/src/submission/submission.py). It returns a `(input_guardrail, None)` tuple consumed by the evaluation pipeline.

### Architecture

```
User message
     │
     ▼
┌───────────────────────────────────────────────┐
│            HybridGuardrail                    │
│                                               │
│   ┌────────────────────┐   ┌──────────────┐   │
│   │ Cohere LLM Judge   │ → │ Regex Stack  │   │
│   │ (KHP_SAFETY_PROMPT)│   │ (fallback)   │   │
│   └────────────────────┘   └──────────────┘   │
└───────────────────────────────────────────────┘
                        │
                        ▼
            { high_risk, score, reasoning }
```

### Regex stack (runs in order, short-circuits on first FAIL)

| Component | Purpose |
|-----------|---------|
| `RuleBasedGuardrail` | Explicit crisis language (suicide, self-harm, overdose) |
| `HeuristicGuardrail` | Indirect/medium risk (hopelessness, worthlessness, "I'm done") |
| `SlangGuardrail` | Teen slang and coded language (`unalive`, `kms`, `kys`, escape framing, burden language, fictional-framing) |
| `ConversationRiskScorer` | Cumulative scorer across turns — flags when multiple risk signals appear together |
| `EmotionalDistressGuardrail` | Recall booster for milder emotional distress |

### LLM judge

The `KHP_SAFETY_PROMPT` encodes our 10-category risk taxonomy derived from stress-testing the KHP bot:

1. Explicit crisis language
2. Teen slang and coded language
3. Burden and finality language
4. Escape framing
5. Hopelessness and future loss
6. Gradual escalation across turns
7. Indirect / fictional framing ("my friend wants to…")
8. Rejection of all help with distress
9. Prolonged emotional distress without explicit crisis language
10. Vulnerable population edge cases (LGBTQ+ youth with no support, hidden identity, etc.)

Full French-language signal coverage is included (`je veux mourir`, `je suis un fardeau`, `plus rien ne change`, etc.).

---

## Repository Layout

| Path | Description |
|------|-------------|
| [project/src/submission/submission.py](project/src/submission/submission.py) | **Our guardrail** — hybrid Cohere + regex stack |
| [project/src/guardrails/](project/src/guardrails/) | Guardrail framework (base classes, LLM judge, stacking) |
| [project/src/prompt_templates/](project/src/prompt_templates/) | Prompt scaffolding |
| [project/providers/](project/providers/) | LLM provider adapters (Cohere, Mistral, OpenAI) |
| [project/notebooks/](project/notebooks/) | KHP bot exploration, guardrail evaluation, mmBERT training |
| [project/scripts/](project/scripts/) | `configure.sh`, `predict.sh`, `evaluate.sh`, `publish_artifact.sh` |
| [datasets/](datasets/) | Seed validation set, sample training data, input.xlsx |
| [docs/](docs/) | Full documentation (quickstart, red-team playbook, judging rubric) |
| `hackathon.json` | Runtime config (GPU flag, model artifacts) |

---

## Quickstart

### 1. Set up environment

```bash
./project/scripts/configure.sh
```

### 2. Configure credentials

Copy `hackathon.json.example` → `hackathon.json` and set your Cohere credentials via environment:

```bash
export BUZZ_COHERE_AUTH_TOKEN=<your-token>
export BUZZ_COHERE_API=<optional-base-url>
```

The guardrail auto-falls back to the pure-regex stack if no token is set.

### 3. Run the evaluation

```bash
./project/scripts/predict.sh datasets/seed_validation_set.csv results/predictions.csv
./project/scripts/evaluate.sh results/predictions.csv results/eval_metrics.csv
```

Outputs: F1, precision, recall, and latency over the validation set.

---

## Design Decisions

- **Hybrid, not either/or.** The LLM judge is smart but slow; the regex stack is fast but brittle. Running them together gives us LLM-level nuance with regex-level safety-net latency.
- **Short-circuit on the first FAIL.** The regex stack is ordered from most-confident (explicit crisis) to least-confident (general distress). As soon as one guardrail fails, we stop and return — this keeps latency low on the dangerous cases, which matter most.
- **Multi-turn awareness.** `ConversationRiskScorer` counts cumulative signals across turns so gradual escalation gets flagged even when no single message is explicit.
- **Bilingual by default.** Every regex layer includes French patterns; the LLM prompt explicitly covers French-English code-switching.
- **Hard-coded slang list.** Platform slang (`unalive`, `kms`) is intentionally captured with regex rather than left to the LLM — these are unambiguous and the recall cost of missing them is unacceptable.

---

## Documentation

| Guide | Topic |
|-------|-------|
| [Quickstart Guide](docs/quickstart_guide.md) | Environment setup through first evaluation |
| [Red-Team Playbook](docs/red_team_playbook.md) | Adversarial testing strategies |
| [Data Generation Manual](docs/data_generation_manual.md) | Training data creation, taxonomy, DEI guidance |
| [Evaluation & Judging](docs/evaluation_and_judging.md) | Scoring rubric and report template |
| [Policy & Ethics Manual](docs/policy_ethics_manual.md) | Responsible AI in youth mental health contexts |
| [Mental Health Safety Primer](docs/mental_health_safety_primer.md) | Risk signals and safety concepts |
| [Full Report](docs/report.pdf) | Methodology, stress-testing findings, results |

---

## About Kids Help Phone

If you or someone you know is struggling, [Kids Help Phone](https://kidshelpphone.ca/) offers free, confidential, 24/7 support to young people across Canada in English and French.

---

## License / Terms

This work was produced under the hackathon [Terms and Conditions](https://drive.google.com/drive/folders/1-sD05Bcc3oBo2RlyNOEiavhnJUQZHjQp?usp=sharing).
