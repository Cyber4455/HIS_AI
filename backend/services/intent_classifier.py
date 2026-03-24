"""
Intent Classification Service for HIS AI
Classifies user messages into: greeting, general_question, symptom, emergency
"""

import re
from typing import Tuple

GREETING_PATTERNS = [
    r'\b(hi|hello|hey|good morning|good afternoon|good evening|howdy|greetings)\b',
    r'\b(what\'s up|whats up|sup|yo)\b',
    r'^(hi|hello|hey)[\s!.?]*$',
]

GENERAL_QUESTION_PATTERNS = [
    r'\b(what is|what are|what\'s|how does|how do|can you explain|tell me about|define|meaning of)\b',
    r'\b(difference between|why do|why does|is it normal|should i|when should)\b',
    r'\b(how to|tips for|advice on|information about|info on)\b',
    r'\b(prevention|prevent|cause|causes|treatment|treatments)\b.*\?',
    r'\?$',  # ends with question mark (general query)
]

EMERGENCY_KEYWORDS = [
    "chest pain", "sweating", "arm pain", "pain radiating",
    "slurred speech", "numbness", "tingling", "confusion",
    "severe breathing", "cannot breathe", "difficulty breathing", "shortness of breath",
    "loss of consciousness", "unconscious", "fainted", "unresponsive",
    "seizure", "convulsions",
    "severe bleeding", "uncontrolled bleeding",
    "anaphylaxis", "throat swelling",
]

SYMPTOM_KEYWORDS = [
    "headache", "fever", "cough", "cold", "pain", "ache", "sore",
    "nausea", "vomiting", "diarrhea", "constipation", "bloating",
    "fatigue", "tired", "weakness", "dizzy", "dizziness",
    "rash", "itching", "swelling", "inflammation",
    "runny nose", "sneezing", "congestion",
    "burning", "cramps", "stiffness",
    "anxiety", "insomnia", "palpitations",
    "bleeding", "bruising", "numbness",
    "shortness of breath", "wheezing",
    "back pain", "joint pain", "muscle pain",
    "stomach pain", "abdominal pain", "chest tightness",
    "sore throat", "ear pain", "eye pain",
    "weight loss", "weight gain", "appetite loss",
    "frequent urination", "blood in urine",
    "i have", "i feel", "i am experiencing", "suffering from",
    "my symptoms", "symptom",
]


def classify_intent(message: str) -> str:
    """
    Classify user message intent.
    Returns: 'emergency', 'symptom', 'greeting', or 'general_question'
    Priority: emergency > symptom > greeting > general_question
    """
    text = message.strip().lower()

    # 1. Emergency check (highest priority)
    emergency_matches = sum(1 for kw in EMERGENCY_KEYWORDS if kw in text)
    if emergency_matches >= 2:
        return "emergency"

    # 2. Symptom check
    symptom_matches = sum(1 for kw in SYMPTOM_KEYWORDS if kw in text)
    if symptom_matches >= 1:
        return "symptom"

    # 3. Greeting check
    for pattern in GREETING_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            # Only classify as greeting if message is short (likely pure greeting)
            if len(text.split()) <= 6:
                return "greeting"

    # 4. General question check
    for pattern in GENERAL_QUESTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "general_question"

    # Default: treat as general question if short, symptom if longer
    if len(text.split()) <= 5:
        return "general_question"
    return "symptom"
