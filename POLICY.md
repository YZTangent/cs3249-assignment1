# Safety and Moderation Policy

## Overview

This document defines the safety boundaries and moderation policies for the psychological pre-consultation CUI system. The system prioritizes user safety while providing supportive dialogue within appropriate boundaries.

## Policy Framework

### 1. Safety Categories

#### 1.1 Crisis Situations

**Definition**: Immediate risk of harm to self or others

**Implementation Requirements**: 
- Add more crisis keywords
- Create more regex patterns for complex expressions
- Use highest sensitivity in all safety modes

```python
# Student Implementation Required:
# Minimum 20 keywords covering various crisis expressions
CRISIS_KEYWORDS = [
    # Direct suicide/self-harm mentions
    "suicide", "end my life", "kill myself", "kms",  "suicidal", "ending it all",
    "want to die", "don't want to live", "overdose", "hang myself",

    # Self-harm expressions
    "hurt myself", "self-harm", "cut myself",
    
    # Immediate danger indicators
    "goodbye forever", "final message", "can't go on", "no reason to live", "it's over", "it's joever", "pointless",
    
    # Emotional crisis expressions
    "hopeless", "desperate", "unbearable pain", "trapped", "worthless", "burden"
]

# Minimum 8 regex patterns for complex expressions
CRISIS_PATTERNS = [
    r"\b(want|going|plan|ready) to (die|kill|hurt|end)\b",
    r"\b(thinking|thought) about (suicide|dying|ending it)\b",
    r"\b(no|any) (reason|point) to (live|continue)\b",
    r"\b(tonight|tomorrow) i (will|am going to)\b",
    r"\b(can't|cannot) (take|handle|do) this anymore\b",
    r"\b(wish|wishing) i was (dead|gone)\b",
    r"\b(my|the) final (plan|act|goodbye)\b",
    r"\b(better off) (dead|gone)\b"
]
```

**Action**: `BLOCK` + Crisis referral

**Example Response Template (Complete this with 150-200 words)**: 

```text
I'm deeply concerned about what you're sharing. Your safety is my top priority, and I want you to know that help is available right now. It sounds like you are in a lot of pain, and it takes a lot of courage to talk about it. You are not alone, and there are people who want to support you through this.

Please reach out to trained crisis counselors immediately:
- National Suicide Prevention Lifeline: 988 (24/7)
- Crisis Text Line: Text HOME to 741741
- The Trevor Project: 1-866-488-7386 (for LGBTQ youth)

These services are free, confidential, and available 24/7. The people on the other end are trained to listen and help you through this. Please, make the call. Your life is valuable, and you deserve support.
```

#### 1.2 Medical Requests

**Definition**: Requests for diagnosis, treatment, or medication advice

**Implementation Requirements**:
- Define more medical keywords
- Create more regex patterns
- Use SAFE_FALLBACK action

```python
# Student Implementation Required:
# Minimum 20 keywords
MEDICAL_INDICATORS = [
    # Diagnosis requests
    "diagnose", "what condition", "do I have", "symptoms of", "am I sick", "what is wrong with me",
    "undiagnosed", "self-diagnose", "medical opinion",
    
    # Medication/treatment
    "medication", "what pills", "prescription", "treatment", "therapy", "cure", "medicine", "dosage",
    "side effects", "drug", "pharmacy",
    
    # Mental health specific
    "am i depressed", "bipolar", "anxiety disorder", "ocd", "ptsd", "schizophrenia", "adhd"
]

# Minimum 8 regex patterns for complex expressions
MEDICAL_PATTERNS = [
    r"\b(prescribe|recommend|suggest) (medication|pills|drugs)\b",
    r"\bwhat (medication|medicine|pills) should i take\b",
    r"\b(can you|should i) get a (prescription|refill)\b",
    r"\b(is this|are these) a symptom of\b",
    r"\b(how to|can I) treat my\b",
    r"\b(what is the|tell me the) (diagnosis|prognosis)\b",
    r"\b(i think|believe) i have (a|an) [a-zA-Z\s]+ disorder\b",
    r"\b(need|require|looking for) (a|an) (doctor|therapist|psychiatrist)\b"
]
```

**Action**: `SAFE_FALLBACK`

**Response Template (Complete with structured format)**: 

```text
I understand you're looking for medical guidance, and I appreciate you reaching out. However, I'm not qualified to provide medical diagnoses or treatment recommendations. My purpose is to offer emotional support and a safe space to talk, not to act as a medical professional. Your health and safety are too important for me to give advice that I'm not qualified to give.

For your health and safety, please consult with:
- A licensed psychiatrist for medication questions
- A primary care physician for general health concerns
- A licensed therapist or counselor for mental health support

While I can't give medical advice, I am here to listen to your concerns and help you explore your feelings. We can talk about the stress you're feeling, coping strategies, or how to find the right professional help.
```

#### 1.3 Harmful Content

**Definition**: Violence, illegal activities, harassment

**Implementation Requirements**:
- Minimum 20 keywords
- Consider both direct and indirect expressions

```python
# Student Implementation Required:
HARMFUL_CATEGORIES = {
    "violence": [
        "attack", "revenge", "kill", "murder", "assault", "bomb", "shoot", "terrorist", "weapon", "fight", "harm someone"
    ],
    
    "illegal": [
        "buy drugs", "sell drugs", "illegal substances", "shoplift", "steal", "hack", "phish", "scam", "fraud", "money launder"
    ],
    
    "harassment": [
        "hate speech", "discriminate", "bully", "threaten", "dox", "stalk", "intimidate", "racist", "sexist", "homophobic"
    ]
}
```

**Action**: `BLOCK`

**Example Response Template (Complete this with 150-200 words)**: 

```text
I cannot and will not provide assistance with that request as it could potentially cause harm. My purpose is to create a safe and supportive environment, and that means I cannot engage in conversations about violence, illegal activities, or harassment. Promoting or assisting with harmful acts goes against my core principles.

I am programmed to refuse requests that could endanger individuals or groups. This is a strict boundary that I cannot cross. Instead, I would like to redirect our conversation to a more constructive topic. We can discuss coping with anger, managing stress, or finding healthy ways to deal with difficult situations. My goal is to be a positive and helpful resource, and I can only do that if we stay within safe and ethical boundaries.
```

#### 1.4 Supportive Dialogue

**Definition**: General emotional support, stress discussion, life challenges

**Acceptable Topics** (define at least 10):
```python
SUPPORTIVE_TOPICS = [
    "stress management",
    "relationship challenges",
    "work-life balance",
    "anxiety coping",
    "grief and loss",
    "personal growth",
    "mindfulness",
    "self-esteem",
    "loneliness",
    "academic pressure"
]
```

**Action**: `ALLOW`

### 2. Action Definitions

- **ALLOW**: Proceed with normal dialogue
- **BLOCK**: Refuse interaction with safety message and resources
- **SAFE_FALLBACK**: Redirect to appropriate resources while maintaining support

### 3. Confidence and Ambiguity

**Confidence Score Guidelines**:
- Keyword match: 0.7 confidence
- Pattern match: 0.8-0.9 confidence
- Multiple matches: Use maximum confidence

**Implementation Requirements**:
- Complete confidence thresholds by safety mode

**Confidence Thresholds by Safety Mode**:

```python
CONFIDENCE_THRESHOLDS = {
    "strict": {
        # Maximum sensitivity - err on side of caution
        "crisis": 0.3,   # Very low threshold for crisis detection
        "medical": 0.4,  # Low threshold for medical boundaries
        "harmful": 0.5   # Moderate threshold for harmful content
    },
    "balanced": {
        # Balanced approach for production use
        "crisis": 0.5,
        "medical": 0.6,
        "harmful": 0.7
    },
    "permissive": {
        # Minimum filtering - only clear violations
        "crisis": 0.7,
        "medical": 0.8,
        "harmful": 0.9
    }
}
```

### 5. Response Templates

**Implementation Requirements**:
- Copy the complete crisis template from your completed 1.1 Crisis Situations above.
- Copy the complete medical template from your completed 1.2 Medical Requests above.
- Copy the complete harmful template from your completed 1.3 Harmful Content above.
- Complete disclaimer template.

```python
RESPONSE_TEMPLATES = {
    "crisis": '''
I'm deeply concerned about what you're sharing. Your safety is my top priority, and I want you to know that help is available right now. It sounds like you are in a lot of pain, and it takes a lot of courage to talk about it. You are not alone, and there are people who want to support you through this.

Please reach out to trained crisis counselors immediately:
- National Suicide Prevention Lifeline: 988 (24/7)
- Crisis Text Line: Text HOME to 741741
- The Trevor Project: 1-866-488-7386 (for LGBTQ youth)

These services are free, confidential, and available 24/7. The people on the other end are trained to listen and help you through this. Please, make the call. Your life is valuable, and you deserve support.
    ''',
    
    "medical": '''
I understand you're looking for medical guidance, and I appreciate you reaching out. However, I'm not qualified to provide medical diagnoses or treatment recommendations. My purpose is to offer emotional support and a safe space to talk, not to act as a medical professional. Your health and safety are too important for me to give advice that I'm not qualified to give.

For your health and safety, please consult with:
- A licensed psychiatrist for medication questions
- A primary care physician for general health concerns
- A licensed therapist or counselor for mental health support

While I can't give medical advice, I am here to listen to your concerns and help you explore your feelings. We can talk about the stress you're feeling, coping strategies, or how to find the right professional help.
    ''',

     "harmful": '''
I cannot and will not provide assistance with that request as it could potentially cause harm. My purpose is to create a safe and supportive environment, and that means I cannot engage in conversations about violence, illegal activities, or harassment. Promoting or assisting with harmful acts goes against my core principles.

I am programmed to refuse requests that could endanger individuals or groups. This is a strict boundary that I cannot cross. Instead, I would like to redirect our conversation to a more constructive topic. We can discuss coping with anger, managing stress, or finding healthy ways to deal with difficult situations. My goal is to be a positive and helpful resource, and I can only do that if we stay within safe and ethical boundaries.
    ''',
    
    "disclaimer": '''
Welcome to the Psychological Pre-Consultation Support System.

IMPORTANT DISCLAIMER:
This is an AI support system designed to provide initial emotional support and guidance. Please note:
- I am an AI, not a human. My responses are generated based on patterns in data.
- I am not a substitute for a licensed therapist, counselor, or medical professional.
- I cannot diagnose conditions, prescribe medication, or provide treatment.
- Our conversations are not confidential in the same way as with a doctor or therapist. Please do not share sensitive personal information.
- I am a tool to help you explore your feelings, not a crisis service.

When to Seek Immediate Help:
If you are in immediate danger or having thoughts of harming yourself or others, please contact a crisis hotline or emergency services immediately. You can call 988 in the US and Canada to reach the Suicide & Crisis Lifeline.

What I Can Offer:
- A safe space to talk about your feelings and concerns.
- Information about mental health topics and resources.
- Help in exploring coping strategies for stress and anxiety.
- Support in identifying your needs and goals for mental wellness.
- Guidance on how to seek professional help.

Your wellbeing is important. How can I support you today?
    '''
}
