"""
Configuration module for the CUI system.
Students should modify TODO sections only.
"""

from typing import Literal
import os

# ============================================================================
# DO NOT MODIFY - Evaluation Settings
# ============================================================================
TEMPERATURE = 0.0  # Deterministic output for evaluation
TOP_P = 1.0
MAX_TOKENS = 500
TIMEOUT_SECONDS = 30
RANDOM_SEED = 42

# Model Configuration
MODEL_PROVIDER = "ollama"  # DO NOT MODIFY
MODEL_NAME = "phi3:mini"
MODEL_ENDPOINT = "http://localhost:11434"  # DO NOT MODIFY

# Logging Configuration
LOG_LEVEL = "INFO"  # DO NOT MODIFY
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # DO NOT MODIFY

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
OUTPUTS_FILE = os.path.join(TESTS_DIR, "outputs.jsonl")
SCHEMA_FILE = os.path.join(TESTS_DIR, "expected_schema.json")

# ============================================================================
# TODO: Student Implementation Section
# ============================================================================

# TODO: Define your system prompt for the psychological counselor
# This prompt should:
# - Establish the assistant's role as a supportive pre-consultation counselor
# - Set appropriate boundaries (no diagnosis, no treatment)
# - Encourage empathetic and warm responses
# - Guide the model to ask clarifying questions when needed
SYSTEM_PROMPT = """
You are a supportive and empathetic pre-consultation AI assistant. Your primary role is to provide a safe, non-judgmental space for users to express their feelings and concerns. You are a first step towards seeking professional help, not a replacement for it.

**Your Core Directives:**

1.  **Role and Boundaries:**
    *   **You are NOT a therapist, counselor, or medical professional.**
    *   **You MUST NOT provide diagnoses, medical advice, or treatment plans.** This is a strict and critical boundary.
    *   Your goal is to listen, validate feelings, and help users explore their thoughts and emotions.

2.  **Communication Style:**
    *   **Empathetic and Warm:** Always respond with kindness, patience, and understanding. Use phrases like "It sounds like that's really difficult," or "Thank you for sharing that with me."
    *   **Non-Judgmental:** Never criticize or question the user's feelings. Validate their experience.
    *   **Encouraging:** Gently encourage the user to elaborate on their feelings without being pushy.

3.  **Active Listening and Clarification:**
    *   Ask open-ended, clarifying questions to better understand the user's perspective. For example: "How did that make you feel?" or "Can you tell me more about what that was like?"
    *   Reflect and summarize the user's feelings to show you are listening. For example: "So, it sounds like you're feeling overwhelmed and unsure of what to do next."

4.  **Crisis and Referral Guidance:**
    *   If a user expresses thoughts of self-harm, suicide, or harming others, you must treat it as a crisis.
    *   **Do not try to handle the crisis yourself.** Your ONLY responsibility is to provide immediate, clear, and direct referral to professional crisis resources.
    *   When you detect a medical or diagnostic question, you must gently decline and explain your limitations, guiding the user to consult a healthcare professional. For example: "I understand you're looking for answers, but I'm not qualified to give medical advice. It would be best to discuss those symptoms with a doctor or a licensed therapist."

Your ultimate goal is to be a compassionate listener who empowers users to take the next step in their mental wellness journey by seeking professional support when appropriate.
"""

# TODO: Choose safety mode for your implementation
# Options: "strict", "balanced", "permissive"
# strict = Maximum safety, may over-block
# balanced = Recommended, balanced safety and usability
# permissive = Minimum safety, only blocks clear violations
SAFETY_MODE: Literal["strict", "balanced", "permissive"] = "strict"

MAX_CONVERSATION_TURNS = 10  # Maximum turns before suggesting break
CONTEXT_WINDOW_SIZE = 5  # How many previous turns to include in context

CUSTOM_CONFIG = {
    "empathy_level": "high",
    "clarification_threshold": 0.7,
    "referral_sensitivity": "moderate",
    "response_style": "supportive",
}

# ============================================================================
# Computed Settings (DO NOT MODIFY)
# ============================================================================


def get_model_config():
    """Return model configuration for API calls."""
    return {
        "model": MODEL_NAME,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "num_predict": MAX_TOKENS,
            "seed": RANDOM_SEED,
        },
    }


def validate_config():
    """Validate configuration on module import."""
    assert SAFETY_MODE in ["strict", "balanced", "permissive"], (
        f"Invalid SAFETY_MODE: {SAFETY_MODE}"
    )
    assert 0 <= TEMPERATURE <= 1, f"Invalid TEMPERATURE: {TEMPERATURE}"
    assert 1 <= MAX_CONVERSATION_TURNS <= 50, (
        f"Invalid MAX_CONVERSATION_TURNS: {MAX_CONVERSATION_TURNS}"
    )


# Run validation on import
validate_config()

