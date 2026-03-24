import re
from typing import Dict, List, Any, Tuple

EMERGENCY_PATTERNS = [
    (["chest pain", "sweating", "pain radiate", "arm pain"], 
     "Possible Heart Attack", 
     "Call emergency services (999 or 112) immediately. Chew aspirin if not allergic."),
    
    (["shortness of breath", "breath difficulty", "breathing problem", "cannot breathe"],
     "Respiratory Emergency",
     "Seek immediate medical attention. Call 999 or 112. Sit upright and try to stay calm."),
    
    (["severe headache", "confusion", "slurred speech", "numbness", "tingling"],
     "Possible Stroke",
     "Call emergency services (999 or 112) immediately. Note the time symptoms started. Uganda Stroke Hotline: +256 414 340 340"),
    
    (["high fever", "stiff neck", "sensitivity to light", "meningitis signs"],
     "Possible Meningitis",
     "Seek immediate medical attention at nearest health center."),
    
    (["severe bleeding", "uncontrolled bleeding", "deep wound"],
     "Severe Bleeding",
     "Apply pressure and call 999 or 112 for emergency care."),
    
    (["severe allergic reaction", "anaphylaxis", "throat swelling", "difficulty swallowing"],
     "Anaphylactic Reaction",
     "Use epinephrine auto-injector if available and call emergency services (999 or 112)."),
    
    (["seizure", "convulsions", "uncontrolled shaking"],
     "Seizure Emergency",
     "Protect from injury, do not restrain, call emergency services (999 or 112)."),
    
    (["loss of consciousness", "fainted", "unresponsive"],
     "Unconsciousness",
     "Check breathing, call 999 or 112, place in recovery position."),
     
    (["malaria danger signs", "severe malaria", "cannot drink", "vomiting everything"],
     "Severe Malaria Emergency",
     "Go to nearest health center immediately. In Uganda, visit URCS emergency or call 0800-100-225."),
]

def detect_emergency(symptoms: str) -> Tuple[bool, str]:
    symptoms_lower = symptoms.lower()
    
    for pattern_keywords, emergency_type, action in EMERGENCY_PATTERNS:
        matches = sum(1 for keyword in pattern_keywords if keyword in symptoms_lower)
        if matches >= 2:
            return True, f"{emergency_type}: {action}"
    
    return False, ""

def analyze_symptom_severity(symptoms: List[str]) -> Dict[str, Any]:
    severity_keywords = {
        "critical": ["chest pain", "severe bleeding", "unconscious", "seizure", "stroke"],
        "high": ["high fever", "severe headache", "difficulty breathing", "severe pain"],
        "moderate": ["mild fever", "cough", "fatigue", "nausea"],
        "low": ["runny nose", "mild headache", "sore throat"]
    }
    
    symptoms_text = " ".join(symptoms).lower()
    max_severity = "low"
    
    for severity, keywords in severity_keywords.items():
        if any(kw in symptoms_text for kw in keywords):
            if severity in ["critical", "high"]:
                max_severity = severity
                break
            elif severity == "moderate" and max_severity != "high":
                max_severity = severity
    
    return {
        "severity": max_severity,
        "requires_immediate_attention": max_severity in ["critical", "high"]
    }
