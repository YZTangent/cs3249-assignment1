"""
Content moderation module for safety enforcement.
Students must complete TODO sections according to POLICY.md.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

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
        """Initialize the moderator with a DistilBERT model."""
        self.safety_mode = SAFETY_MODE
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "distilbert-base-uncased", num_labels=3
        )
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
            "disclaimer": """Hi, I'm PsychPal, your friendly Psychological Pre-Consultation Support System! Here's how I can assist:
- Offer a safe space to talk about your feelings and concerns.
- Provide information on mental health topics and resources.
- Help explore coping strategies for stress and anxiety.
- Support you in identifying your needs and goals for emotional well-being.
- Guide you on how to seek professional help when needed.

IMPORTANT DISCLAIMER:
I am an AI support system designed to provide initial emotional support and guidance. Please note:
- I am an AI, not a human. My responses are generated based on patterns in data.
- I am not a substitute for a licensed therapist, counselor, or medical professional.
- I cannot diagnose conditions, prescribe medication, or provide treatment.
- Our conversations are not confidential in the same way as with a doctor or therapist. Please do not share sensitive personal information.
- I am a tool to help you explore your feelings, not a crisis service.

When to Seek Immediate Help:
If you are in immediate danger or having thoughts of harming yourself or others, please contact a crisis hotline or emergency services immediately. You can call 1767 in Singapore to reach the Samaritans of Singapore hotline.


Remember: Your wellbeing is important! How can I support you today?""",
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
        content_check = self._check_content(user_prompt)
        if content_check.action != ModerationAction.ALLOW:
            logger.warning(f"Content detected: {content_check.reason}")
            return content_check

        if model_response:
            output_check = self._check_content(model_response)
            if output_check.action != ModerationAction.ALLOW:
                logger.warning(f"Output violation: {output_check.reason}")
                return output_check

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Content passes all safety checks",
            confidence=1.0,
        )

    def _check_content(self, text: str) -> ModerationResult:
        """
        Check content using a DistilBERT model.
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)
        confidence, predicted_class = torch.max(probabilities, dim=-1)

        tags = []
        action = ModerationAction.ALLOW
        fallback_response = None
        reason = "Content passes all safety checks"

        if predicted_class.item() == 0:  # Crisis
            tags.append("crisis")
            threshold = self.confidence_thresholds[self.safety_mode]["crisis"]
            if confidence.item() >= threshold:
                action = ModerationAction.BLOCK
                fallback_response = self.fallback_templates["crisis"]
                reason = f"Crisis indicators detected with confidence {confidence.item():.2f}."
        elif predicted_class.item() == 1:  # Medical
            tags.append("medical")
            threshold = self.confidence_thresholds[self.safety_mode]["medical"]
            if confidence.item() >= threshold:
                action = ModerationAction.SAFE_FALLBACK
                fallback_response = self.fallback_templates["medical"]
                reason = f"Medical request detected with confidence {confidence.item():.2f}."
        elif predicted_class.item() == 2:  # Harmful
            tags.append("harmful")
            threshold = self.confidence_thresholds[self.safety_mode]["harmful"]
            if confidence.item() >= threshold:
                action = ModerationAction.BLOCK
                fallback_response = self.fallback_templates["harmful"]
                reason = f"Harmful content detected with confidence {confidence.item():.2f}."

        return ModerationResult(
            action=action,
            tags=tags,
            reason=reason,
            confidence=confidence.item(),
            fallback_response=fallback_response,
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