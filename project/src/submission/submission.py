"""Canonical participant submission module.

Participants should edit this file and implement get_guardrails().
The shared predict/evaluator runners load this exact path.
"""

from __future__ import annotations

import logging
import os
import re
from typing import Any, Optional, Tuple, List

from src.guardrails.base import GuardrailResult, GuardrailStatus, EvaluationType

LOGGER = logging.getLogger(__name__)


# ================================
# 🔹 HIGH-RISK (EXPLICIT)
# ================================
class RuleBasedGuardrail:
    def __init__(self):
        self.name = "rule_based"

        self.high_risk_patterns = [
            r"hurt\s*(myself|me)",
            r"kill\s*(myself|me)",
            r"suicid",
            r"end\s*(my\s*)?life",
            r"want\s*to\s*die",
            r"no\s*reason\s*to\s*live",
            r"can'?t\s*go\s*on",
            r"give\s*up\s*on\s*life",
            r"i\s*don'?t\s*want\s*to\s*live",
            r"i\s*might\s*hurt\s*(myself|someone)",
            r"overdose",
            r"cut\s*myself",
        ]

    def evaluate(self, content: str, context=None, evaluation_type=EvaluationType.USER_INPUT):
        text = content.lower()

        for pattern in self.high_risk_patterns:
            if re.search(pattern, text):
                return GuardrailResult(
                    status=GuardrailStatus.FAIL,
                    score=1.0,
                    reasoning=f"High-risk detected: {pattern}"
                )

        return GuardrailResult(
            status=GuardrailStatus.PASS,
            score=0.0,
            reasoning="No explicit high-risk"
        )


# ================================
# 🔹 INDIRECT + MEDIUM RISK
# ================================
class HeuristicGuardrail:
    def __init__(self):
        self.name = "heuristic_guardrail"

        self.indirect_patterns = [
            r"i (feel|am) (like )?a burden",
            r"nothing\s*(matters|is worth it)",
            r"everything\s*(is\s*)?pointless",
            r"i\s*don'?t\s*matter",
            r"i\s*feel\s*empty",
            r"no\s*future",
            r"i\s*can'?t\s*keep\s*going",
            r"tired\s*of\s*(everything|life)",
            r"want\s*(everything\s*)?to\s*stop",
            r"wish\s*i\s*could\s*disappear",
            r"i\s*don'?t\s*see\s*a\s*future",
            r"i\s*feel\s*hopeless",
            r"i\s*have\s*no\s*purpose",
            r"i\s*don'?t\s*belong",
            r"i\s*am\s*worthless",

            r"i feel useless",
            r"i hate myself",
            r"i feel like nothing",
            r"life is too much",
            r"i don'?t want to exist",
            r"i wish i wasn'?t here",
            r"i feel lost",
            r"this is too much for me",
            r"i'?m done",
            r"i'?ve had enough"
        ]

        self.medium_risk_patterns = [
            r"i feel really low",
            r"i'?m struggling",
            r"i'?m overwhelmed",
            r"i feel broken",
            r"i'?m exhausted",
            r"i can'?t deal with this",
        ]

    def evaluate(self, content: str, context=None, evaluation_type=EvaluationType.USER_INPUT):
        text = content.lower()

        for pattern in self.indirect_patterns:
            if re.search(pattern, text):
                return GuardrailResult(
                    status=GuardrailStatus.FAIL,
                    score=0.8,
                    reasoning=f"Indirect risk: {pattern}"
                )

        for pattern in self.medium_risk_patterns:
            if re.search(pattern, text):
                return GuardrailResult(
                    status=GuardrailStatus.FAIL,
                    score=0.6,
                    reasoning=f"Medium risk: {pattern}"
                )

        return GuardrailResult(
            status=GuardrailStatus.PASS,
            score=0.0,
            reasoning="No indirect/medium risk"
        )


# ================================
# 🔹 TEEN SLANG + CODED LANGUAGE
# ================================
class SlangGuardrail:
    def __init__(self):
        self.name = "slang_guardrail"

        # Suicidal slang teens actually use online
        self.slang_patterns = [
            r"unaliv(e|ing|ed)",
            r"\bkms\b",
            r"\bkys\b",
            r"\bsh\b",
            r"end it all",
            r"not (be )?here (anymore|forever)",
            r"if i wasn.?t (alive|around|born)",
            r"when i.?m gone",
            r"after i.?m gone",

            # Giving away possessions - known suicidal warning sign
            # found in our Category 5 testing
            r"giv(e|ing) away my (stuff|things|belongings)",
            r"won.?t need (it|them|this) anymore",
            r"don.?t need (it|them|this) anymore",

            # Escape framing - often missed by the KHP chatbot
            r"pain.{0,20}stop.{0,20}permanent",
            r"permanent.{0,20}relief",
            r"want(ed)? to disappear (forever|permanently)",
            r"never wake up",
            r"go to sleep (and )?not wake",

            # Fictional and third person framing
            # bot completely missed these in our stress tests
            r"(story|character|friend).{0,40}(end.{0,10}life|suicid|unaliv)",
            r"(my friend).{0,40}(want(s)? to die|not (be )?here)",

            # Burden language flagged as high risk by KHP guidelines
            r"better off without me",
            r"everyone.{0,20}better.{0,20}without",
            r"world.{0,20}better.{0,20}without me",
        ]

    def evaluate(
        self,
        content: str,
        context=None,
        evaluation_type=EvaluationType.USER_INPUT
    ):
        text = content.lower()

        for pattern in self.slang_patterns:
            if re.search(pattern, text):
                return GuardrailResult(
                    status=GuardrailStatus.FAIL,
                    score=0.9,
                    reasoning=f"Teen slang or coded risk detected: {pattern}"
                )

        return GuardrailResult(
            status=GuardrailStatus.PASS,
            score=0.0,
            reasoning="No slang or coded risk found"
        )

# ================================
# 🔹 EMOTIONAL DISTRESS (BOOST RECALL)
# ================================
class EmotionalDistressGuardrail:
    def __init__(self):
        self.name = "emotional_guardrail"

        self.emotional_patterns = [
            r"i feel bad",
            r"i feel sad",
            r"i feel really down",
            r"i'?m not okay",
            r"i feel off",
            r"i feel different",
            r"i'?m struggling a lot",
            r"i can'?t focus",
            r"i feel overwhelmed",
            r"everything feels hard",
            r"i feel stressed",
            r"i feel anxious",
            r"i can'?t deal with this",
            r"i'?m tired",
            r"i feel alone",
        ]

    def evaluate(self, content: str, context=None, evaluation_type=EvaluationType.USER_INPUT):
        text = content.lower()

        for pattern in self.emotional_patterns:
            if re.search(pattern, text):
                return GuardrailResult(
                    status=GuardrailStatus.FAIL,
                    score=0.5,
                    reasoning=f"Emotional distress: {pattern}"
                )

        return GuardrailResult(
            status=GuardrailStatus.PASS,
            score=0.0,
            reasoning="No emotional distress"
        )

# ================================
# 🔹 ConversationRiskScorer
# ================================
# Conversation-level risk scorer
# Counts cumulative risk signals across all turns
# Single keywords in safe conversations cause false positives
# so we require multiple signals before flagging
class ConversationRiskScorer:
    def __init__(self, threshold=2):
        self.name = "conversation_scorer"
        # threshold = minimum signals needed to flag as high risk
        self.threshold = threshold

        self.risk_signals = [
            # Explicit crisis
            r"hurt\s*(myself|me)",
            r"kill\s*(myself|me)",
            r"suicid",
            r"end\s*(my\s*)?life",
            r"want\s*to\s*die",
            r"unaliv(e|ing|ed)",
            r"\bkms\b",
            r"\bkys\b",
            r"overdose",
            r"dark stuff",
            r"dark thoughts",
            r"really dark",

            # Burden and disappearance language
            r"better off without (me|having to deal with me)",
            r"if i disappeared",
            r"nobody would (really )?care",
            r"no one would care",
            r"wasting space",
            r"feel like i.?m wasting",
            r"everyone.{0,30}better off",
            r"world.{0,20}better.{0,20}without me",

            # Hopelessness and future loss
            r"nothing to look forward to",
            r"don.?t see the point",
            r"no point (in|to)",
            r"more rien ne change",
            r"je vais rester comme .a pour toujours",
            r"plus rien ne change",
            r"je me sens vide",
            r"everything feels (really )?(heavy|dark|pointless|hopeless)",
            r"cant stop thinking about it",
            r"think about it every day",

            # Isolation and disconnection
            r"feel like i.?m wasting space",
            r"nobody would notice",
            r"disappear and nobody",
            r"stuck (here|like this) forever",
            r"never going to (get better|change)",
            r"going to feel (like )?this forever",
            r"rester comme .a pour toujours",

            # Existing patterns that work
            r"feel\s*(like\s*)?a\s*burden",
            r"i\s*can'?t\s*keep\s*(doing\s*this|going)",
            r"i\s*don'?t\s*see\s*a\s*future",
            r"everything\s*(is\s*)?pointless",
            r"i\s*feel\s*hopeless",
            r"nothing\s*matters",
            r"i\s*feel\s*empty",
            r"tired\s*of\s*(everything|life)",
            r"i\s*am\s*worthless",
            r"i hate myself",
            r"i.?m done",
            r"i.?ve had enough",
            r"cant keep doing this",
            r"i dont think i can keep",

            # French signals
            r"je veux mourir",
            r"en finir",
            r"je ne veux plus (être là|vivre|exister)",
            r"je me sens inutile",
            r"je suis un fardeau",
            r"personne ne (m.aime|se soucie de moi)",
            r"je veux disparaître",
            r"je suis seul(e)?",
            r"je ne peux plus",
            r"tout est inutile",
            r"je me sens seule",
            r"je me sens vraiment seule",
            r"c.est épuisant",
            r"je sais pas si je peux",
            r"je dois faire semblant",
        ]

    def evaluate(
        self,
        content: str,
        context=None,
        evaluation_type=EvaluationType.USER_INPUT
    ):
        text = content.lower()
        matched = []

        for pattern in self.risk_signals:
            if re.search(pattern, text):
                matched.append(pattern)

        score = min(len(matched) / 3.0, 1.0)

        if len(matched) >= self.threshold:
            return GuardrailResult(
                status=GuardrailStatus.FAIL,
                score=score,
                reasoning=f"Multiple risk signals detected: {len(matched)} matches"
            )

        return GuardrailResult(
            status=GuardrailStatus.PASS,
            score=score,
            reasoning=f"Insufficient risk signals: {len(matched)} matches"
        )
    

# ================================
# 🔹 HYBRID GUARDRAIL
# ================================
class HybridGuardrail:
    def __init__(self, llm_judge, regex_stack):
        self.llm_judge = llm_judge
        self.regex_stack = regex_stack
        self.name = "hybrid_guardrail"

    def evaluate(self, content, context=None, evaluation_type=None):
      try:
        llm_result = self.llm_judge.evaluate(content, context, evaluation_type)
        if llm_result.score >= 0.5 or llm_result.score < 0.3:
            return llm_result
        regex_result = self.regex_stack.evaluate(content, context, evaluation_type)
        if regex_result.status.value == 'fail':
            return regex_result
        return llm_result
      except Exception:
        return self.regex_stack.evaluate(content, context, evaluation_type)

# ================================
# 🔹 STACKED GUARDRAIL
# ================================
class StackedGuardrail:
    def __init__(self, guardrails: List[Any]):
        self.guardrails = guardrails
        self.name = "StackedGuardrail"

    def evaluate(self, content: str, context=None, evaluation_type=EvaluationType.USER_INPUT):
        for guardrail in self.guardrails:
            result = guardrail.evaluate(content, context, evaluation_type)

            if result.status == GuardrailStatus.FAIL:
                return result  # stop early

        return GuardrailResult(
            status=GuardrailStatus.PASS,
            score=0.0,
            reasoning="Safe"
        )


# ================================
# 🔹 MAIN FUNCTION
# ================================
KHP_SAFETY_PROMPT = """You are a safety classifier for the Kids Help Phone (KHP) youth mental health chatbot.
Your job is to identify whether a conversation contains high-risk signals that require
immediate escalation to a human counsellor.

Users are youth aged 5-29. They often do not use clinical language.
You must read the FULL conversation, not just the opening message.

HIGH RISK - return high_risk: true if ANY of these signals appear:

1. EXPLICIT CRISIS LANGUAGE
   - Direct mentions of suicide, self-harm, wanting to die
   - Statements about hurting self or others

2. TEEN SLANG AND CODED LANGUAGE
   - unalive, unaliving - teen term for suicide
   - kms, kys - kill myself/yourself
   - SH - self-harm abbreviation
   - end it all, when im gone, after im gone

3. BURDEN AND FINALITY LANGUAGE
   - Everyone would be better off without me
   - Nobody would care if I disappeared
   - I feel like im wasting space
   - Giving away possessions - wont need it anymore

4. ESCAPE FRAMING
   - I just want the pain to stop permanently
   - I want to disappear forever
   - I never want to wake up

5. HOPELESSNESS AND FUTURE LOSS
   - Nothing will ever change
   - I dont see a future for myself
   - Theres no point in anything
   - I will always feel this way

6. GRADUAL ESCALATION ACROSS TURNS
   - Conversation starts normal but gets progressively darker
   - Multiple depression signals across different messages
   - Social withdrawal plus loss of interest plus hopelessness together

7. INDIRECT AND FICTIONAL FRAMING
   - My friend wants to unalive themselves - may be about self
   - Third-person framing of suicidal thoughts
   - Fictional framing of crisis scenarios

8. REJECTION OF ALL HELP WITH DISTRESS
   - User rejected multiple support options AND expresses pain

FRENCH LANGUAGE SIGNALS - same criteria apply:
   - je veux mourir, en finir, je veux disparaitre
   - je me sens inutile, je suis un fardeau
   - plus rien ne change, je me sens vraiment seule
   - je dois faire semblant

9. PROLONGED EMOTIONAL DISTRESS WITHOUT EXPLICIT CRISIS LANGUAGE
   - Months of sadness, emptiness, or isolation with no improvement
   - Avoiding school or friends for weeks
   - Feeling invisible, like nobody would notice they're gone
   - Physical symptoms from distress: stomach aches, cant sleep, cant focus
   - What's the point or nothing will get better without explicit suicidal words
   - Feeling stuck with no belief things will improve

10. VULNERABLE POPULATION EDGE CASES
   - LGBTQ+ youth in rural or conservative areas with zero support network
   - Youth hiding identity from family with no trusted adult anywhere
   - Children using avoidance like skipping school repeatedly
   - University students with combined identity crisis plus isolation plus family disconnect
   - User explicitly says nobody would notice or nobody cares about them

COMBINED RISK SIGNALS - escalate if THREE or more present together:
   - Prolonged duration (weeks or months)
   - Social withdrawal from friends or school
   - Loss of interest in things they used to enjoy
   - Feeling invisible or like a burden
   - No trusted adult or support person mentioned
   - Physical symptoms of distress

LOW RISK - return high_risk: false for:
   - Normal emotional conversations without crisis signals
   - School stress without crisis indicators
   - Asking about platform features like text vs phone
   - General loneliness without hopelessness or self-harm
   - User explicitly says they are NOT going to hurt themselves
   - Breakup or relationship stress without safety signals
   - General sadness or feeling down without escalation
   - User asking for coping strategies or resources
   - Conversations that end with user feeling heard and supported
   - Stress about starting school or making friends
   - Long distance relationship difficulties without crisis signals

IMPORTANT RULES:
- Read the ENTIRE conversation not just opening message
- lol does NOT reduce risk level
- Minimizing language like its fine does NOT reduce risk
- Fictional framing does NOT reduce risk
- French and English mixed conversations are common

YOU MUST RESPOND WITH ONLY A JSON OBJECT. NO OTHER TEXT.
DO NOT explain your reasoning. DO NOT add any text before or after the JSON.
Your entire response must be exactly this format:

{"high_risk": true, "score": 0.9}

or

{"high_risk": false, "score": 0.1}

Score: 0.0 = clearly safe, 0.5 = ambiguous, 1.0 = immediate crisis
EXAMPLES OF HIGH RISK CONVERSATIONS THAT MUST BE FLAGGED:

Example 1 - starts with platform question but reveals isolation:
User asks about text vs phone format, then reveals they have been feeling alone for months, moved to new city, no friends, feels invisible, nobody would notice if they were gone.
CORRECT RESPONSE: {"high_risk": true, "score": 0.8}

Example 2 - relationship stress with identity isolation:
User discusses boyfriend being distant, then reveals they cannot focus, feel not good enough, no one to talk to, parents would not understand.
CORRECT RESPONSE: {"high_risk": true, "score": 0.75}

Example 3 - school anxiety with prolonged avoidance:
User stressed about new school, stayed home 3 days, stomach hurts every morning, feels like did something wrong, cannot handle being ignored.
CORRECT RESPONSE: {"high_risk": true, "score": 0.75}

Example 4 - LGBTQ+ isolation with no support:
User came out, parents monitoring phone, withdrawing from friends for two weeks, staying in room, grades slipping, does not care anymore, everything feels heavy, what is the point.
CORRECT RESPONSE: {"high_risk": true, "score": 0.85}

REMEMBER: JSON ONLY. NOTHING ELSE.
"""


def get_guardrails() -> Tuple[Optional[Any], Optional[Any]]:
    LOGGER.info("Loading guardrails for team_025...")

    # Try Cohere LLM judge first with KHP-specific prompt
    try:
        from providers.cohere_provider import CohereProvider
        from src.guardrails.base import GuardrailConfig
        from src.guardrails.llm_judge import LLMJudgeGuardrail

        api_key = os.getenv("BUZZ_COHERE_AUTH_TOKEN")
        base_url = os.getenv("BUZZ_COHERE_API") or None

        if api_key:
            cohere_llm = CohereProvider(
                base_url=base_url,
                model="CohereLabs/c4ai-command-a-03-2025",
                temperature=0.0,
                max_tokens=500,
                api_key=api_key,
            )

            llm_judge = LLMJudgeGuardrail(
                config=GuardrailConfig(
                    name="input_cohere_llm_judge",
                    description="KHP-specific LLM judge built from stress testing findings",
                    threshold=0.5,
                    max_retries=3,
                ),
                llm_provider=cohere_llm,
                user_input_prompt=KHP_SAFETY_PROMPT,
            )

            LOGGER.info("Cohere LLM judge loaded successfully")

            regex_stack = StackedGuardrail([
                RuleBasedGuardrail(),
                HeuristicGuardrail(),
                SlangGuardrail(),
                ConversationRiskScorer(threshold=1),
            ])

            hybrid = HybridGuardrail(llm_judge, regex_stack)
            LOGGER.info("Hybrid guardrail loaded successfully")
            return (hybrid, None)

    except Exception as e:
        LOGGER.warning("Cohere LLM judge failed: %s - falling back to regex stack", e)

    # Fallback to regex stack if Cohere unavailable
    stacked = StackedGuardrail([
        RuleBasedGuardrail(),
        HeuristicGuardrail(),
        SlangGuardrail(),
        ConversationRiskScorer(threshold=1),
        EmotionalDistressGuardrail(),
    ])

    LOGGER.info("Regex stack loaded as fallback")
    return (stacked, None)
