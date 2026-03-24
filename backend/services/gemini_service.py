import json
from typing import List, Dict, Any, Optional

# Try to import google.generativeai, but don't crash if it fails
_gemini_available = False
model = None

try:
    import google.generativeai as genai
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import GEMINI_API_KEY
    
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        _gemini_available = True
except Exception:
    _gemini_available = False

# ─── HIS AI SYSTEM PROMPT ───
HIS_AI_SYSTEM_PROMPT = """
You are HIS AI (Health Intelligence System), a Hybrid AI-Powered Clinical Decision Support Platform.

System Identity:
HIS AI is a multi-role, privacy-focused, intelligent healthcare assistant designed for preliminary medical assessment.

Core Behavior:
You must behave like a helpful, professional, calm, and knowledgeable medical guide.
You must ALWAYS provide useful, actionable health guidance. NEVER refuse to help or respond with only a disclaimer.

Response Rules:
- ALWAYS analyze the user's symptoms or health question thoroughly
- ALWAYS suggest possible conditions related to the symptoms
- ALWAYS provide general precautions (rest, hydration, monitoring symptoms, etc.)
- ALWAYS suggest common over-the-counter medications when appropriate
- ALWAYS recommend consulting a healthcare professional if symptoms persist, worsen, or seem severe
- Keep responses helpful, short, and supportive
- Be professional and calm — no exaggeration, no guaranteed diagnosis
- Prioritize safety, clarity, and early detection

Disclaimer Rule:
- Include a SHORT disclaimer at the END of your response: "⚕️ Note: This is a preliminary AI assessment and not a medical diagnosis."
- The disclaimer must NEVER be the entire response — always provide helpful analysis BEFORE the disclaimer
"""

PATIENT_PROMPT = HIS_AI_SYSTEM_PROMPT + """
You are speaking with a PATIENT. Interact conversationally but in a caring medical tone.
- If the user sends a greeting, respond politely and introduce yourself briefly.
- If asked a general health question, provide a clear, helpful educational explanation with practical tips.
- If symptoms are described, you MUST:
  1. Analyze the symptoms and explain what they could indicate
  2. List possible conditions (bullet points with brief descriptions)
  3. Provide general precautions (rest, hydration, monitoring, etc.)
  4. Suggest common over-the-counter medications when appropriate
  5. Indicate risk level: Low / Moderate / High
  6. Recommend seeing a doctor if symptoms persist or worsen
  7. End with a short disclaimer
- NEVER respond with only a disclaimer or refuse to analyze symptoms
- Guide the user — be helpful and supportive
"""

DOCTOR_PROMPT = HIS_AI_SYSTEM_PROMPT + """
You are providing information to a DOCTOR. Provide structured clinical summaries:
- Show symptom breakdown
- Show possible conditions with probabilities
- Show calculated risk level
- Highlight emergency flags clearly
- Keep output concise and professional
- Use clinical terminology
"""

ADMIN_PROMPT = HIS_AI_SYSTEM_PROMPT + """
You are providing information to an ADMIN. Provide system-level insights:
- Summarize clinical patterns
- Highlight risk trends
- Keep output analytical and data-driven
"""

# Rule-based fallback symptom database
SYMPTOM_DATABASE = {
    "headache": {
        "diseases": [
            {"name": "Tension Headache", "probability": 0.6, "precautions": ["Rest in a dark room", "Stay hydrated", "Avoid screen time"], "medicines": ["Ibuprofen", "Acetaminophen"]},
            {"name": "Migraine", "probability": 0.3, "precautions": ["Avoid triggers", "Rest", "Cold compress"], "medicines": ["Sumatriptan", "Ibuprofen"]},
        ],
        "explanation": "Headaches can be caused by tension, migraine, dehydration, or eye strain."
    },
    "fever": {
        "diseases": [
            {"name": "Common Cold", "probability": 0.5, "precautions": ["Rest", "Drink fluids", "Monitor temperature"], "medicines": ["Acetaminophen", "Ibuprofen"]},
            {"name": "Flu (Influenza)", "probability": 0.35, "precautions": ["Bed rest", "Hydration", "Isolation"], "medicines": ["Oseltamivir", "Acetaminophen"]},
        ],
        "explanation": "Fever is typically a sign that your body is fighting an infection."
    },
    "cough": {
        "diseases": [
            {"name": "Upper Respiratory Infection", "probability": 0.5, "precautions": ["Stay hydrated", "Rest", "Humidify air"], "medicines": ["Dextromethorphan", "Guaifenesin"]},
            {"name": "Bronchitis", "probability": 0.3, "precautions": ["Avoid irritants", "Rest", "Drink warm fluids"], "medicines": ["Cough suppressant", "Ibuprofen"]},
        ],
        "explanation": "Cough can be caused by infections, allergies, or irritants."
    },
    "stomach pain": {
        "diseases": [
            {"name": "Gastritis", "probability": 0.4, "precautions": ["Avoid spicy food", "Eat smaller meals", "Reduce stress"], "medicines": ["Antacids", "Omeprazole"]},
            {"name": "Food Poisoning", "probability": 0.3, "precautions": ["Stay hydrated", "Rest", "Bland diet"], "medicines": ["ORS", "Bismuth subsalicylate"]},
        ],
        "explanation": "Stomach pain can be caused by gastritis, food poisoning, or other digestive issues."
    },
    "fatigue": {
        "diseases": [
            {"name": "Anemia", "probability": 0.3, "precautions": ["Iron-rich diet", "Regular exercise", "Adequate sleep"], "medicines": ["Iron supplements", "Vitamin B12"]},
            {"name": "Chronic Fatigue Syndrome", "probability": 0.2, "precautions": ["Pace activities", "Sleep hygiene", "Stress management"], "medicines": ["Consult doctor"]},
        ],
        "explanation": "Fatigue can stem from anemia, poor sleep, stress, or underlying conditions."
    },
    "sore throat": {
        "diseases": [
            {"name": "Pharyngitis", "probability": 0.5, "precautions": ["Gargle warm salt water", "Rest voice", "Stay hydrated"], "medicines": ["Throat lozenges", "Ibuprofen"]},
            {"name": "Strep Throat", "probability": 0.3, "precautions": ["See a doctor for testing", "Rest", "Avoid spreading"], "medicines": ["Antibiotics (if bacterial)", "Acetaminophen"]},
        ],
        "explanation": "Sore throat is commonly caused by viral or bacterial infections."
    },
    "back pain": {
        "diseases": [
            {"name": "Muscle Strain", "probability": 0.5, "precautions": ["Rest", "Apply ice/heat", "Gentle stretching"], "medicines": ["Ibuprofen", "Muscle relaxants"]},
            {"name": "Sciatica", "probability": 0.2, "precautions": ["Physical therapy", "Proper posture", "Avoid heavy lifting"], "medicines": ["NSAIDs", "Gabapentin"]},
        ],
        "explanation": "Back pain is often caused by muscle strain, poor posture, or disc issues."
    },
    "nausea": {
        "diseases": [
            {"name": "Gastroenteritis", "probability": 0.4, "precautions": ["Hydrate", "Rest", "BRAT diet"], "medicines": ["Ondansetron", "Bismuth subsalicylate"]},
            {"name": "Motion Sickness", "probability": 0.2, "precautions": ["Focus on horizon", "Fresh air", "Avoid reading in car"], "medicines": ["Dimenhydrinate", "Meclizine"]},
        ],
        "explanation": "Nausea can be caused by infections, motion, food, or stress."
    },
    "dizziness": {
        "diseases": [
            {"name": "Vertigo", "probability": 0.4, "precautions": ["Avoid sudden movements", "Sit down when dizzy", "Stay hydrated"], "medicines": ["Meclizine", "Dimenhydrinate"]},
            {"name": "Low Blood Pressure", "probability": 0.3, "precautions": ["Stand up slowly", "Stay hydrated", "Eat regularly"], "medicines": ["Increase fluid intake", "Consult doctor"]},
        ],
        "explanation": "Dizziness can be due to inner ear issues, low blood pressure, dehydration, or other conditions."
    },
    "chest tightness": {
        "diseases": [
            {"name": "Anxiety", "probability": 0.4, "precautions": ["Deep breathing", "Relaxation techniques", "Reduce caffeine"], "medicines": ["Consult doctor for appropriate treatment"]},
            {"name": "Costochondritis", "probability": 0.3, "precautions": ["Rest", "Apply heat", "Avoid strain"], "medicines": ["NSAIDs", "Acetaminophen"]},
        ],
        "explanation": "Chest tightness can be caused by anxiety, musculoskeletal issues, or cardiac conditions. Always seek medical attention for persistent chest symptoms."
    },
}

DEFAULT_RESPONSE = {
    "diseases": [
        {"name": "General Consultation Needed", "probability": 0.5, 
         "precautions": ["Monitor symptoms", "Stay hydrated", "Rest well", "Seek medical attention if symptoms worsen"],
         "medicines": ["Consult a healthcare provider for proper diagnosis"]}
    ],
    "explanation": "Based on your symptoms, a professional medical consultation is recommended for accurate diagnosis."
}

GREETING_RESPONSES = {
    "patient": (
        "Hello! I'm **HIS AI**, your Health Intelligence System assistant. "
        "I'm here to help you with preliminary medical assessments, symptom analysis, "
        "and health information.\n\n"
        "How can I help you today? You can:\n"
        "- Describe your symptoms for analysis\n"
        "- Ask general health questions\n"
        "- Use the symptom selector for structured input\n\n"
        "*Please remember: I provide preliminary assessments only and do not replace professional medical care.*"
    ),
    "doctor": (
        "Welcome, Doctor. HIS AI Clinical Decision Support is ready.\n\n"
        "You can submit patient symptoms for structured clinical analysis, "
        "including condition matching, risk stratification, and emergency flagging."
    ),
    "admin": (
        "Welcome, Administrator. HIS AI System Dashboard is active.\n\n"
        "You can query system analytics, consultation statistics, and risk distribution data."
    ),
}


class GeminiService:
    
    @staticmethod
    def generate_response(prompt: str) -> str:
        if not _gemini_available:
            return "AI service is not available. Using rule-based analysis."
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    @staticmethod
    def generate_json_response(prompt: str) -> Dict[str, Any]:
        if not _gemini_available:
            return {"error": "AI service not available"}
        try:
            response = model.generate_content(
                prompt + "\n\nRespond in valid JSON format only.",
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_greeting(role: str) -> str:
        return GREETING_RESPONSES.get(role, GREETING_RESPONSES["patient"])
    
    @staticmethod
    def answer_general_question(question: str, role: str = "patient") -> str:
        """Answer a general health question."""
        if _gemini_available:
            try:
                prompt_prefix = PATIENT_PROMPT if role == "patient" else DOCTOR_PROMPT if role == "doctor" else ADMIN_PROMPT
                prompt = f"""{prompt_prefix}

The user asks a general health question: "{question}"

You MUST provide a helpful, informative answer. Include:
1. A clear explanation of the topic
2. Practical tips or precautions the user can follow
3. Common over-the-counter remedies if relevant
4. When to see a doctor
5. A short disclaimer at the END (not as the main response)

Keep it under 200 words. Be helpful and supportive."""
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                pass
        
        # Fallback — still provide helpful guidance
        return (
            f"Great question! Here's some general guidance:\n\n"
            f"While specific advice depends on individual circumstances, here are some general tips:\n"
            f"- Stay hydrated and maintain a balanced diet\n"
            f"- Get adequate rest and regular exercise\n"
            f"- Monitor your symptoms and note any changes\n"
            f"- Consider common OTC options like multivitamins for general wellness\n\n"
            f"If you have specific symptoms you'd like me to analyze, feel free to describe them!\n\n"
            f"💡 *If symptoms persist or worsen, please consult a healthcare professional.*\n\n"
            f"⚕️ *Note: This is a preliminary AI assessment and not a medical diagnosis.*"
        )
    
    @staticmethod
    def chat_symptom_analysis(symptoms: str, role: str = "patient", 
                              conversation_history: List[str] = None) -> Dict[str, Any]:
        """Analyze symptoms with role-aware responses."""
        # Try Gemini first
        if _gemini_available:
            try:
                result = GeminiService._gemini_analysis(symptoms, role, conversation_history)
                if "error" not in result:
                    return result
            except Exception:
                pass
        
        # Fallback to rule-based analysis
        return GeminiService._rule_based_analysis(symptoms, role)
    
    @staticmethod
    def _gemini_analysis(symptoms: str, role: str = "patient",
                         conversation_history: List[str] = None) -> Dict[str, Any]:
        history_text = ""
        if conversation_history:
            history_text = "Previous conversation:\n" + "\n".join(conversation_history)
        
        prompt_prefix = PATIENT_PROMPT if role == "patient" else DOCTOR_PROMPT if role == "doctor" else ADMIN_PROMPT
        
        if role == "doctor":
            prompt = f"""{prompt_prefix}

{history_text}
Patient symptoms: {symptoms}

Provide a structured clinical summary in JSON format:
{{
    "type": "diagnosis",
    "diseases": [
        {{"name": "Disease Name", "probability": 0.85, "precautions": ["precaution1"], "medicines": ["medicine1"]}}
    ],
    "confidence_score": 0.85,
    "risk_level": "High",
    "explanation": "Structured clinical summary with symptom breakdown",
    "emergency_flags": ["any emergency indicators"]
}}
"""
        else:
            prompt = f"""{prompt_prefix}

{history_text}
User's current symptoms: {symptoms}

You MUST analyze the symptoms thoroughly and provide helpful guidance. Respond in JSON format:
{{
    "type": "diagnosis",
    "diseases": [
        {{"name": "Condition Name", "probability": 0.85, "precautions": ["Rest well", "Stay hydrated", "Monitor symptoms"], "medicines": ["Common OTC medication"]}}
    ],
    "confidence_score": 0.85,
    "risk_level": "Low",
    "explanation": "Provide a helpful, patient-friendly explanation that: 1) Analyzes the symptoms, 2) Explains what they could indicate, 3) Lists precautions the patient should take, 4) Suggests common OTC medications when appropriate, 5) Recommends seeing a doctor if symptoms persist or worsen. End with a short disclaimer."
}}

IMPORTANT: The explanation field MUST contain a thorough, helpful analysis — NOT just a disclaimer. Always suggest precautions and OTC medications in the diseases array.
"""
        return GeminiService.generate_json_response(prompt)
    
    @staticmethod
    def _rule_based_analysis(symptoms: str, role: str = "patient") -> Dict[str, Any]:
        symptoms_lower = symptoms.lower()
        
        matched_diseases = []
        matched_explanation = ""
        
        for keyword, data in SYMPTOM_DATABASE.items():
            if keyword in symptoms_lower:
                matched_diseases.extend(data["diseases"])
                if matched_explanation:
                    matched_explanation += " "
                matched_explanation += data["explanation"]
        
        if not matched_diseases:
            matched_diseases = DEFAULT_RESPONSE["diseases"]
            matched_explanation = DEFAULT_RESPONSE["explanation"]
        
        # Remove duplicates and limit
        seen = set()
        unique_diseases = []
        for d in matched_diseases:
            if d["name"] not in seen:
                seen.add(d["name"])
                unique_diseases.append(d)
        
        # Calculate risk level from disease probabilities
        max_prob = max(d["probability"] for d in unique_diseases) if unique_diseases else 0.5
        if max_prob > 0.7:
            risk_level = "High"
        elif max_prob > 0.4:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
        
        # Format for doctor role
        if role == "doctor":
            matched_explanation = (
                f"**Clinical Summary:**\n"
                f"Reported symptoms: {symptoms}\n\n"
                f"**Assessment:** {matched_explanation}\n\n"
                f"**Risk Level:** {risk_level}"
            )
        
        return {
            "type": "diagnosis",
            "diseases": unique_diseases[:5],
            "diagnosis": unique_diseases[:5],
            "confidence_score": 0.7,
            "risk_level": risk_level,
            "explanation": matched_explanation
        }
