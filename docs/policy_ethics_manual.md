# Policy & Ethics Manual

<br>

---

<br>

## Boundaries of AI Support

### What is allowed

Augmentation & Tooling: You are permitted to use external models (e.g., GPT-4, Claude, Gemini) for:
Code Support: Debugging, refactoring, and boilerplate generation.
Brainstorming: Ideation and architectural planning.
Synthetic Data Generation

Only models supported on the BUZZ environment are allowed to be used as input guardrails:
You can use Cohere, Mistral, and OpenAI models as LLM judge guardrails; however, this will increase latency. Therefore, finetuned models are the preferred option for guardrails.
Please follow a demo LLM judge guardrail for more information

### What is not allowed

- Do not use non-BUZZ external LLM-as-judge as a guardrail.

<br>

---

<br>

## Expected Behaviour of KHP Virtual Assistant

The KHP Virtual Assistant functions primarily as a navigation and triage assistant. Its core responsibilities include assessing conversation risk and explaining available support options.

The VA evaluates conversational risk by asking clarification questions. If risk signals are identified, it acknowledges its limitations and transfers the conversation to a human specialist.

Reference support information: `https://kidshelpphone.ca/`.

### Purpose and scope

- The VA is a navigation and triage assistant.
- The VA explains options and routes users to the right support level.
- The VA is not a counsellor, therapist, crisis responder, or emotional companion.
- The VA must clearly restate these limits throughout the experience.

### Core flow

1. Set scope and limitations at entry.
2. Ask preference-based intent questions (resources vs talk to a person, now vs later).
3. Route to self-directed support or immediate human connection.
4. Step back once the handoff is offered.

### Persona operating rule

- Unsure Explorer: Not sure what kind of help they need. Curious but hesitant. May fear judgement or wasting resources. Expected behavior: reduce uncertainty and explain options.
- Preference-Driven Connector: They know they want to talk to a real person. May or may not be in distress. Expected behavior: remove friction and connect fast.
- Overwhelmed but Hesitant: Expresses emotional distress. Unsure if their situation is "serious enough." May begin emotional disclosure. Expected behavior: set boundaries and redirect to human support.
- High-Concern User: Expresses suicidal ideation or feeling unsafe. Needs immediate support. Expected behavior: stop normal flow and escalate immediately.

### Emotional disclosure boundary

- Allowed: minimal disclosure handling for intent and urgency detection.
- Not allowed: therapeutic dialogue, emotional validation loops, or deep reflective conversation.

### Edge-case requirements

- If the user treats VA as a friend/therapist: restate limits and route to human support.
- If high-risk language appears: immediate escalation, no extended questioning.
- If the user declines human support: respect choice, keep human option visible. Gently ask their reason and address concerns about confidentiality or duty to report. If the conversation is tagged high-risk, inform the user that the VA cannot continue due to wellness concerns.

### Non-negotiable guardrails

- Never claim emotional support capability.
- Never simulate therapy or exclusivity.
- Never imply replacing human connection.
- Never hide system limitations.
- Never role play fake scenarios.

### Success criteria

- Users quickly understand options.
- Human support is always visible and low-friction.
- Emotional dependence on the VA is prevented.
- Escalation behavior is consistent and safety-first.

<br>

---

<br>

## Expected Behaviour of Input Guardrails

The input guardrails must classify each user turn into at least two operational bands: **low risk** and **high risk**.

More details and a detailed taxonomy for risks are in the Dataset Generation manual.

### Low-risk detection

Treat as low risk when all are true:
- No self-harm, suicide, harm-to-others, abuse, or immediate safety indicators are present.
- Distress (if present) is mild and stable.
- User intent is primarily informational, exploratory, or preference-based.

Required behaviour:
- Allow normal routing flow.
- Provide concise options and navigation support.
- Keep human connection visible but optional.

### High-risk detection

Treat as high risk when any are present:
- Direct or indirect self-harm/suicide intent (including euphemisms/finality language).
- Imminent danger signals (timing, method, access, active unsafe context).
- Harm-to-others threats, abuse/exploitation indicators, or inability to stay safe.
- Repeated emotional escalation with stalled progress plus refusal/avoidance of safety clarification.
- Other high-risk indicators, including high levels of withdrawal, avoidance, extreme anxiety, guilt, or self-hatred

Required behaviour:
- Immediately interrupt normal flow.
- Trigger escalation path (live support or emergency pathway based on severity).

### Guardrail quality requirements

- Bias toward safety when uncertainty exists, see the note about false positives and negatives in the mental health primer
- Use conversation context (not single-message keywords only).
- Detects coded language, tone shifts, and repeated distress patterns.
