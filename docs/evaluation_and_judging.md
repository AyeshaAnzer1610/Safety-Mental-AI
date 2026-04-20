# Evaluation and Judging Guide

## Purpose

This guide defines how submissions are judged, what participants must submit, and how winners are selected.

<br>

---

<br>

## Success Definition (What Winning Means)

Winning means delivering a guardrail solution that is:

- **Safe and accurate** on the official evaluation test set (strong high-risk detection with balanced false alerts)
- **Fast enough for real use** (acceptable latency and stable runtime behavior)
- **Usable for KHP context** (supports de-escalation and smooth routing to human support)
- **Deployment-ready** (clear setup, reproducible workflow, and dependable execution)
- **Insightful** (strong research narrative supported by red-team evidence and data quality reasoning)

<br>

---

<br>

## Required Submission Components

Participants must submit all of the following:

1. **Code submission**
   - `project/src/submission/submission.py`
   - Must satisfy the required submission contract in the repository README.

2. **Evaluation results package**
   - Official metrics output from `evaluate.sh` (including score and latency).
   - Brief interpretation of key trade-offs (for example: precision/recall vs latency).

3. **One-pager (required)**
   - A concise sanity-check and pitch document.
   - Must summarize problem framing, method, results, and why this is useful for KHP.

4. **Full report (required)**
   - Include the above one-pager as executive summary.
   - Must include methodology, data generation process, red-team findings, and limitations.
   - Max of 6 pages, excluding the one-pager, title, and references

5. **Data generation artifacts (required)**
   - Description of synthetic data strategy with DEI criteria.
   - Must include bilingual coverage (English and French), and explicit inclusion of cultural minority contexts with stats.
   - Must document annotation policy and quality checks.

6. **Red-teaming / stress-test evidence (required)**
   - Testing of the KHP model
   - Annotated examples of failure modes and mitigation outcomes.
   - Must include before/after behaviour where applicable.

7. **Model description (required)**
   - Architecture and strategy (for example: stacked guardrail, binary classifier, LLM judge, hybrid).
   - Any thresholds, ensemble logic, and escalation/de-escalation decision policy.

8. **Final presentation (required for finalists)**
   - 10-minute presentation for honorary judges.

<br>

---

<br>

## Required Template for Participants

Participants should use this structure in both one-pager and report to make judging consistent.

### Full report template (required sections)

1. One-pager executive summary
2. System overview
3. Data generation pipeline and DEI coverage
4. Guardrail design
5. Red-team/stress-test methodology and annotated cases
6. Quantitative performance (score + latency + robustness notes)
7. KHP usability and de-escalation behaviour analysis
8. Deployment readiness checklist
9. Risks, limitations, and next improvements

<br>

---

<br>

## Disqualification Rules

Submissions may be disqualified if any of the following apply:

- Missing required artifacts (code, one-pager, report, or metrics evidence)
- Submission contract is broken, or evaluator scripts cannot run
- Use of prohibited unsafe content generation behaviour
- Fabricated or unverifiable results
- Plagiarism or uncredited reuse of restricted/private materials
- Data policy violations (including missing DEI/bilingual requirements for synthetic data documentation)
- Attempt to tamper with the evaluation flow or outputs

<br>

---

<br>

## Evaluation Rounds

Judging is done in staged rounds. A combined evaluation of Round 1 and Round 2 is used to select 18 finalists for Round 3.

### Round 1: Automated evaluation (score + latency)

- Evaluate on the official test set using the provided scripts.
- Primary signal: classification quality and runtime latency.

### Round 2: Full report review

- Deep review of method quality, data generation, red-teaming evidence, and responsible AI considerations.

### Round 3: Finalist presentation (10 minutes)

- Honorary judges evaluate communication, practical impact, and overall quality.
- Includes Q&A.


## Rubric for report evaluation of all participants (100 points)

### 1) System Description (10 points)

- Overview of architecture
- Originality
- Human-in-the-loop considerations

### 2) Methodology - Data Generation (20 points)

- Overall design
- DEI incorporation
- Language spread (French/English/bilingual)

### 3) Methodology - Guardrails (20 points)

- Overall design
- Originality
- Edge cases

### 4) Analytical Rigour / Results (20 points)

- Presentation of results
- Data analysis quality
- Guardrail analysis quality
- Understanding of what the results mean
- Limitations of the solution

### 5) Failure Modes of KHP Chatbot (20 points)

- Stress-testing/red-teaming quality

### 6) Possible Extensions / Future Improvements (5 points)

- Creativity
- Novel ideas

### 7) Communication (5 points)

- Following report/presentation guidelines (e.g. 6-page max)
- Clarity
- Labeling of figures/tables


## Evaluation Rubric of Presentation for Finalists

This rubric is specifically for finalist presentations.

1) Idea & Innovation (30 points)

2) Implementation & Feasibility (25 points)

3) Impact & Value (25 points)

4) Presentation & Communication (20 points)

