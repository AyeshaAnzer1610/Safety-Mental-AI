# Mental Health Safety Primer

<br>

---

<br>

## Why this topic needs extra care

Mental health conversations can involve crisis risk, trauma, self-harm, abuse, or severe emotional distress. Participants may disclose sensitive information unexpectedly, and model responses can influence real behaviour. Safety should be treated as a core requirement, not an optional feature.

<br>

---

<br>

## Safety disclaimer

This guide is for educational and hackathon prototyping purposes only. No tool developed during this event should be marketed as a clinical diagnostic tool or a replacement for professional medical intervention.

<br>

---

<br>

## Mental health guardrails: what they are

Mental health guardrails are detection mechanisms and corresponding policy-based response rules designed to minimize harm during high-risk conversations. Essentially, they ensure an AI system operates within its defined safety boundaries.

### Core elements

- Automatic flagging of certain 'high-risk' topics, including: suicide ideation, safety & abuse, and physical violence.
- Detection of high-level risk in any mental health-related conversation. (Refer to the Taxonomy x Risk Signal Table for high-risk signals per category.)
- Response switches to safe, supportive, non-instructional messaging and escalates to human interaction upon identification of a high-risk conversation.
- Immediate human escalation when risk exceeds a defined threshold or the conversation topic demands immediate attention.
- Strict boundary enforcement of responses to prevent dangerous instructions or clinical overreach.
- Continuous safety audit: logging and review of safety-related events for ongoing system improvement.

<br>

---

<br>

## How to detect distress and youth safety risk

### Distress indicators

- Direct language about self-harm or not wanting to live.
- Indirect cues such as hopelessness, burden language, and extreme isolation.
- Rapid worsening tone, urgency, farewell statements, or method-seeking behaviour.
- Functional collapse, such as inability to eat, sleep, or complete daily tasks.
- Interpersonal issues that indicate abuse, neglect, or unhealthy relational dynamics.

### Youth safety indicators

- Age disclosure or context indicating the participant is a minor.
- Mentions of abuse, neglect, exploitation, grooming, or coercion.
- Runaway planning, unsafe substance pressure, or sexual coercion.
- Signals that the youth has no trusted adult support.

<br>

---

<br>

## Common failure patterns

- Literal-only detection that misses indirect or coded signals
- Single-turn analysis that misses risk building over multiple turns
- Context loss from prior disclosures
- Generic template responses that feel dismissive
- Escalation delays when urgent review is needed
- Reassurance without adequate risk assessment
- Escalation or refusal to respond when someone is exploring mental health-related topics

<br>

---

<br>

## False negatives vs. false positives

False negatives (missed real risk) can lead to severe harm and delayed intervention. In mental health safety, high-severity risk categories should be tuned for high sensitivity.

False positives (incorrect risk flags) can overwhelm human counsellors, create alert fatigue, and reduce system trust. This can delay response for truly urgent cases.

In general false negatives can be disastrous in mental health, as a missed detection is a missed opportunity for life-saving intervention. However, we can not ignore false positives, as they can be just as harmful.

A practical balance:

- Use risk-tiered thresholds, with strict handling for imminent harm
- Combine model scores, rules, and conversation trajectory
- Use confidence bands for immediate escalation vs. secondary rapid triage
- Monitor crisis recall, escalation precision, counsellor load, and time-to-human-response

<br>

---

<br>

## Quick operating protocol

1. If high risk is detected, trigger crisis-safe messaging and immediate escalation.
2. Log decisions for quality review and guardrail tuning.
