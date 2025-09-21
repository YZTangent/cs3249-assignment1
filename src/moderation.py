"""
Content moderation module for safety enforcement.
Students must complete TODO sections according to POLICY.md.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from .config import SAFETY_MODE

logger = logging.getLogger(__name__)


class ModerationAction(Enum):
    """Possible moderation actions."""

    ALLOW = "allow"
    BLOCK = "block"
    SAFE_FALLBACK = "safe_fallback"


@dataclass
class ModerationResult:
    """Result of moderation check."""

    action: ModerationAction
    tags: List[str]  # Policy tags that were triggered
    reason: str  # Human-readable explanation
    confidence: float  # Confidence level (0-1)
    fallback_response: Optional[str] = None  # Response to use if action != ALLOW


class Moderator:
    """Handles content moderation according to safety policy."""

    def __init__(self):
        """Initialize the moderator with safety rules."""
        self.safety_mode = SAFETY_MODE
        self._initialize_rules()

    def _initialize_rules(self):
        """
        Initialize moderation rules based on POLICY.md.
        """

        self.crisis_keywords = [
            "suicide",
            "end my life",
            "kill myself",
            "kms",
            "self-harm",
            "cut myself",
            "suicidal",
            "ending it all",
            "want to die",
            "don't want to live",
            "overdose",
            "hang myself",
            "goodbye",
            "forever",
            "final message",
            "can't go on",
            "no reason to live",
            "it's over",
            "it's joever",
            "pointless",
            "hopeless",
            "desperate",
            "unbearable pain",
            "trapped",
            "worthless",
            "burden",
            "unalive myself",
        ]

        self.crisis_patterns = [
            re.compile(
                r"\b(want|going|plan|ready) to (die|kill|hurt|end)\b", re.IGNORECASE
            ),
            re.compile(
                r"\b(thinking|thought) about (suicide|dying|ending it)\b", re.IGNORECASE
            ),
            re.compile(
                r"\b(no|any) (reason|point) to (live|continue)\b", re.IGNORECASE
            ),
            re.compile(r"\b(tonight|tomorrow) i (will|am going to)\b", re.IGNORECASE),
            re.compile(
                r"""\b(can't|cannot) (take|handle|do) this anymore\b""", re.IGNORECASE
            ),
            re.compile(r"\b(wish|wishing) i was (dead|gone)\b", re.IGNORECASE),
            re.compile(r"\b(my|the) final (plan|act|goodbye)\b", re.IGNORECASE),
            re.compile(r"\b(better off) (dead|gone)\b", re.IGNORECASE),
        ]

        self.medical_keywords = [
            "diagnose",
            "what condition",
            "do I have",
            "symptoms of",
            "am I sick",
            "what is wrong with me",
            "undiagnosed",
            "self-diagnose",
            "medical opinion",
            "medication",
            "what pills",
            "prescription",
            "treatment",
            "therapy",
            "cure",
            "medicine",
            "dosage",
            "side effects",
            "drug",
            "pharmacy",
            "am i depressed",
            "bipolar",
            "anxiety disorder",
            "ocd",
            "ptsd",
            "schizophrenia",
            "adhd",
            "Adderall",
            "Xanax",
            "SSRI",
            "SSRIs",
            "Antidepressants",
        ]

        self.medical_patterns = [
            re.compile(
                r"\b(prescribe|recommend|suggest) (medication|pills|drugs)\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bwhat (medication|medicine|pills) should i take\b", re.IGNORECASE
            ),
            re.compile(
                r"""\b(can you|should i) get a (prescription|refill)\b""", re.IGNORECASE
            ),
            re.compile(r"\b(is this|are these) a symptom of\b", re.IGNORECASE),
            re.compile(r"\b(how to|can I) treat my\b", re.IGNORECASE),
            re.compile(
                r"\b(what is the|tell me the) (diagnosis|prognosis)\b", re.IGNORECASE
            ),
            re.compile(
                r"""\b(i think|believe) i have (a|an) [a-zA-Z\s]+ disorder\b""",
                re.IGNORECASE,
            ),
            re.compile(
                r"\b(need|require|looking for) (a|an) (doctor|therapist|psychiatrist)\b",
                re.IGNORECASE,
            ),
        ]

        self.harmful_content = {
            "violence": [
                "attack",
                "revenge",
                "kill",
                "murder",
                "assault",
                "bomb",
                "shoot",
                "stab",
                "terrorist",
                "weapon",
                "fight",
                "harm someone",
                "I am a big fan of Ted Kaczynski",
                "kys",
                "unalive yourself",
            ],
            "illegal": [
                "buy drugs",
                "sell drugs",
                "illegal substances",
                "shoplift",
                "steal",
                "hack",
                "phish",
                "scam",
                "rape",
                "grape",
                "fraud",
                "money launder",
                "heroin",
                "fentanyl",
                "fent",
                "cocaine",
                "crack",
                "nose candy",
                "ketamine",
                "methamphetamine",
                "meth",
                "molly",
                "lsd",
                "ecstasy",
                "shrooms",
                "acid",
            ],
            "harassment": [
                "hate speech",
                "discriminate",
                "bully",
                "threaten",
                "dox",
                "stalk",
                "intimidate",
                "racist",
                "sexist",
                "homophobic",
                "transphobic",
                "xenophobic",
                "misogynistic",
                "anti-semitic",
                "islamophobic",
                "ableist",
                "ageist",
                "slur",
                "bigot",
                "supremacist",
            ],
        }

        self.confidence_thresholds = {
            "strict": {"crisis": 0.3, "medical": 0.4, "harmful": 0.5},
            "balanced": {"crisis": 0.5, "medical": 0.6, "harmful": 0.7},
            "permissive": {"crisis": 0.7, "medical": 0.8, "harmful": 0.9},
        }

        self.fallback_templates = {
            "crisis": """I'm deeply concerned about what you're sharing. Your safety is my top priority, and I want you to know that help is available right now. It sounds like you are in a lot of pain, and it takes a lot of courage to talk about it. You are not alone, and there are people who want to support you through this.

Please reach out to trained crisis counselors immediately:
- Samaritans of Singapore hotline: 1767 (24/7)
- Singapore Association for Mental Health (SAMH) Helpline: 1800-283-7019

These services are free, confidential, and available 24/7. The people on the other end are trained to listen and help you through this. Please, make the call. Your life is valuable, and you deserve support.""",
            "medical": """I understand you're looking for medical guidance, and I appreciate you reaching out. However, I'm not qualified to provide medical diagnoses or treatment recommendations. My purpose is to offer emotional support and a safe space to talk, not to act as a medical professional. Your health and safety are too important for me to give advice that I'm not qualified to give.

For your health and safety, please consult with:
- A licensed psychiatrist for medication questions
- A primary care physician for general health concerns
- A licensed therapist or counselor for mental health support

While I can't give medical advice, I am here to listen to your concerns and help you explore your feelings. We can talk about the stress you're feeling, coping strategies, or how to find the right professional help.""",
            "harmful": """I cannot and will not provide assistance with that request as it could potentially cause harm. My purpose is to create a safe and supportive environment, and that means I cannot engage in conversations about violence, illegal activities, or harassment. Promoting or assisting with harmful acts goes against my core principles.

I am programmed to refuse requests that could endanger individuals or groups. This is a strict boundary that I cannot cross. Instead, I would like to redirect our conversation to a more constructive topic. We can discuss coping with anger, managing stress, or finding healthy ways to deal with difficult situations. My goal is to be a positive and helpful resource, and I can only do that if we stay within safe and ethical boundaries.""",
            "disclaimer": """Welcome to PsychPal, your friendly Psychological Pre-Consultation Support System!

IMPORTANT DISCLAIMER:
I am an AI support system designed to provide initial emotional support and guidance. Please note:
- I am an AI, not a human. My responses are generated based on patterns in data.
- I am not a substitute for a licensed therapist, counselor, or medical professional.
- I cannot diagnose conditions, prescribe medication, or provide treatment.
- Our conversations are not confidential in the same way as with a doctor or therapist. Please do not share sensitive personal information.
- I am a tool to help you explore your feelings, not a crisis service.

When to Seek Immediate Help:
If you are in immediate danger or having thoughts of harming yourself or others, please contact a crisis hotline or emergency services immediately. You can call 1767 in Singapore to reach the Samaritans of Singapore hotline.

What I Can Offer:
- A safe space to talk about your feelings and concerns.
- Information about mental health topics and resources.
- Help in exploring coping strategies for stress and anxiety.
- Support in identifying your needs and goals for mental wellness.
- Guidance on how to seek professional help.

Your wellbeing is important. Allow me to lend a listening ear to your problems!""",
        }

    def moderate(
        self,
        user_prompt: str,
        model_response: Optional[str] = None,
        context: Optional[List[Dict]] = None,
    ) -> ModerationResult:
        """
        Perform moderation on user input and/or model output.
        """

        crisis_check = self._check_crisis(user_prompt)
        if crisis_check.action != ModerationAction.ALLOW:
            logger.warning(f"Crisis detected: {crisis_check.reason}")
            return crisis_check

        medical_check = self._check_medical(user_prompt)
        if medical_check.action != ModerationAction.ALLOW:
            logger.warning(f"Medical request detected: {medical_check.reason}")
            return medical_check

        harmful_check = self._check_harmful(user_prompt)
        if harmful_check.action != ModerationAction.ALLOW:
            logger.warning(f"Harmful content detected: {harmful_check.reason}")
            return harmful_check

        if model_response:
            output_check = self._check_model_output(model_response)
            if output_check.action != ModerationAction.ALLOW:
                logger.warning(f"Output violation: {output_check.reason}")
                return output_check

        if context:
            context_check = self._check_context_patterns(context)
            if context_check.action != ModerationAction.ALLOW:
                logger.info(f"Context concern: {context_check.reason}")
                return context_check

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Content passes all safety checks",
            confidence=1.0,
        )

    def _check_crisis(self, text: str) -> ModerationResult:
        text_lower = text.lower()
        detected_keywords = []
        confidence = 0.0
        tags = []

        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                detected_keywords.append(keyword)
                confidence = max(confidence, 0.7)

        for pattern in self.crisis_patterns:
            if pattern.search(text_lower):
                confidence = max(confidence, 0.9)
                tags.append("crisis_pattern")

        if detected_keywords:
            tags.append("crisis_keyword")

        threshold = self.confidence_thresholds[self.safety_mode]["crisis"]
        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=tags,
                reason=f"Crisis indicators detected with confidence {confidence:.2f}. Keywords: {detected_keywords}",
                confidence=confidence,
                fallback_response=self.fallback_templates["crisis"],
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No crisis indicators detected",
            confidence=confidence,
        )

    def _check_medical(self, text: str) -> ModerationResult:
        text_lower = text.lower()
        detected_keywords = []
        confidence = 0.0
        tags = []

        for keyword in self.medical_keywords:
            if keyword in text_lower:
                detected_keywords.append(keyword)
                confidence = max(confidence, 0.7)

        for pattern in self.medical_patterns:
            if pattern.search(text_lower):
                confidence = max(confidence, 0.85)
                tags.append("medical_pattern")

        if detected_keywords:
            tags.append("medical_keyword")

        threshold = self.confidence_thresholds[self.safety_mode]["medical"]
        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=tags,
                reason=f"Medical request detected with confidence {confidence:.2f}. Keywords: {detected_keywords}",
                confidence=confidence,
                fallback_response=self.fallback_templates["medical"],
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No medical requests detected",
            confidence=confidence,
        )

    def _check_harmful(self, text: str) -> ModerationResult:
        text_lower = text.lower()
        detected_categories = []
        confidence = 0.0

        for category, keywords in self.harmful_content.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if category not in detected_categories:
                        detected_categories.append(category)

        if detected_categories:
            confidence = 0.75

        threshold = self.confidence_thresholds[self.safety_mode]["harmful"]
        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=detected_categories,
                reason=f"Harmful content detected in categories: {detected_categories}",
                confidence=confidence,
                fallback_response=self.fallback_templates["harmful"],
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No harmful content detected",
            confidence=confidence,
        )

    def _check_model_output(self, response: str) -> ModerationResult:
        response = response.lower()

        # Check for medical advice
        medical_check = self._check_medical(response)
        if medical_check.action != ModerationAction.ALLOW:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=["model_medical_advice"],
                reason="Model output contained potential medical advice.",
                confidence=medical_check.confidence,
                fallback_response=self.fallback_templates["medical"],
            )

        # Check for harmful suggestions
        harmful_check = self._check_harmful(response)
        if harmful_check.action != ModerationAction.ALLOW:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=["model_harmful_suggestion"],
                reason="Model output contained harmful content.",
                confidence=harmful_check.confidence,
                fallback_response=self.fallback_templates["medical"],
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Model output is appropriate",
            confidence=1.0,
        )

    def _check_context_patterns(self, context: List[Dict]) -> ModerationResult:
        crisis_count = 0
        for turn in context:
            if turn.get("role") == "user":
                content = turn.get("content", "").lower()
                for keyword in self.crisis_keywords:
                    if keyword in content:
                        crisis_count += 1

        if crisis_count >= 3:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=["pattern_escalation", "repeated_crisis"],
                reason="Escalating crisis pattern detected",
                confidence=0.8,
                fallback_response=self.fallback_templates["crisis"],
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Conversation pattern is safe",
            confidence=1.0,
        )

    def get_disclaimer(self) -> str:
        """Get initial disclaimer."""
        return self.fallback_templates.get("disclaimer", "")


# Singleton instance
_moderator_instance = None


def get_moderator() -> Moderator:
    """Get singleton moderator instance."""
    global _moderator_instance
    if _moderator_instance is None:
        _moderator_instance = Moderator()
    return _moderator_instance
