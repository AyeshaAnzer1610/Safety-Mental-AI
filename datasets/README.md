# Datasets

## Seed dataset

The seed validation dataset (`seed_validation_set.csv`) contains 100 examples of annotated conversations. The participants are encouraged to use these seed conversations for data augmentation and integrate data from the broader categories described in the Taxonomy (refer to the Data Generation Manual for details).

## Evaluation context

- Model tuning: Participants are encouraged to fine-tune their own models to surpass the provided baselines.
- Dataset storage: Any dataset created for fine-tuning must be stored within the `datasets/` folder, as this location is used by organizers for evaluation review.
- Risk definition: Topic does not equal risk. Any taxonomy topic can be classified as `high_risk` if strong safety signals are present.
- Misuse signals: Functional misuse signals (e.g., refusal to escalate or replacing human support) can increase the risk level regardless of the topic.

More details on taxonomy and data generation are in the `docs/`

## Implementation note for developers

**Topic does not equal risk.** Any taxonomy category becomes **High Risk** if one or more of the following appears:

- Burden language
- Finality language
- Escape framing
- Active self-harm
- Suicide-ideation euphemisms
- Immediate safety concern
- High misuse signal

## Required Submission Contents

Submissions must include:

- Source datasets or links/instructions to fetch them.
- Any generated/augmented datasets used for fine-tuning (store these files directly in `datasets/`).
- Concise notes on preprocessing, labeling, and quality checks.
- Notes detailing diversity coverage, multilingual coverage, and representation of minority groups.

## Evaluation criteria

- **Primary metrics:** precision, recall, and F1 (especially high-risk detection performance).
- **Latency:** response time and practical runtime efficiency under official scripts.
- **Robustness:** performance on ambiguous, noisy, and adversarial inputs covering different diversity metrics.
- **Calibration trade-offs:** reducing harmful misses while controlling false alerts.
- **Documentation quality:** clear data methodology, labeling rationale, and notes on limitations/biases.

## Recommended dataset metadata

For each dataset, please document the following:

- source and license/usage terms
- language coverage (`fr`, `en`, `mix`)
- label schema (`low_risk` / `high_risk`)
- known limitations or bias risks
- Actions taken to ensure Diversity, Equity, and Inclusion (DEI) metrics

Note: Keep large model weights out of this folder; store them in S3 and reference them from `hackathon.json` artifacts.



