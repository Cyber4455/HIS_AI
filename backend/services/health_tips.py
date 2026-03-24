from typing import List, Optional
import random

def generate_health_tips(
    symptoms: Optional[List[str]] = None,
    risk_level: Optional[str] = None,
    health_score: Optional[int] = None,
    context: Optional[str] = None
) -> List[str]:
    tips = []
    
    general_tips = [
        "Stay hydrated by drinking at least 8 glasses of water daily.",
        "Get 7-9 hours of quality sleep each night for optimal health.",
        "Exercise for at least 30 minutes most days of the week.",
        "Eat a balanced diet rich in fruits, vegetables, and whole grains.",
        "Wash your hands frequently to prevent the spread of germs.",
        "Manage stress through meditation, deep breathing, or yoga.",
        "Schedule regular check-ups with your healthcare provider.",
        "Avoid smoking and limit alcohol consumption.",
        "Maintain a healthy weight through diet and exercise.",
        "Keep your vaccinations up to date.",
    ]
    
    symptom_based_tips = {
        "fever": [
            "Rest and stay hydrated when you have a fever.",
            "Take over-the-counter fever reducers if needed.",
            "Monitor your temperature regularly.",
        ],
        "cough": [
            "Stay hydrated to soothe your throat.",
            "Use honey to help relieve cough symptoms.",
            "Avoid smoking and exposure to irritants.",
        ],
        "headache": [
            "Rest in a quiet, dark room.",
            "Stay hydrated and eat regular meals.",
            "Try over-the-counter pain relievers if appropriate.",
        ],
        "fatigue": [
            "Ensure you're getting enough sleep each night.",
            "Eat iron-rich foods if you suspect anemia.",
            "Consider checking your thyroid function.",
        ],
        "chest pain": [
            "Seek immediate medical attention for chest pain.",
            "Rest and avoid strenuous activity.",
            "Avoid smoking and manage stress.",
        ],
        "shortness of breath": [
            "Seek medical attention if breathing difficulties are severe.",
            "Practice deep breathing exercises.",
            "Avoid smoking and air pollutants.",
        ],
        "nausea": [
            "Eat small, frequent meals.",
            "Stay hydrated with small sips of water.",
            "Avoid strong odors that may trigger nausea.",
        ],
        "abdominal pain": [
            "Rest and avoid eating until pain subsides.",
            "Stay hydrated with clear fluids.",
            "Avoid self-medicating without professional advice.",
        ],
    }
    
    risk_based_tips = {
        "High": [
            "Schedule a follow-up appointment with your doctor immediately.",
            "Monitor your symptoms closely and track any changes.",
            "Consider getting a second opinion from a specialist.",
            "Follow all prescribed treatment plans strictly.",
        ],
        "Emergency": [
            "Seek immediate medical attention at an emergency department.",
            "Call emergency services if symptoms worsen.",
            "Do not delay treatment - your health is critical.",
        ],
        "Medium": [
            "Schedule an appointment with your healthcare provider soon.",
            "Monitor your symptoms and note any changes.",
            "Consider lifestyle modifications to reduce risk factors.",
        ],
        "Low": [
            "Maintain healthy lifestyle habits.",
            "Continue regular health monitoring.",
            "Stay informed about preventive care.",
        ],
    }
    
    if health_score is not None:
        if health_score >= 80:
            tips.append("Excellent health score! Keep up your healthy habits.")
        elif health_score >= 60:
            tips.append("Good health score. Consider minor lifestyle improvements.")
        elif health_score >= 40:
            tips.append("Your health score indicates room for improvement. Focus on diet and exercise.")
        else:
            tips.append("Your health score suggests you should consult a healthcare provider.")
    
    if risk_level and risk_level in risk_based_tips:
        tips.extend(risk_based_tips[risk_level])
    
    if symptoms:
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for key, value in symptom_based_tips.items():
                if key in symptom_lower:
                    tips.extend(value)
                    break
    
    tips.extend(random.sample(general_tips, min(3, len(general_tips))))
    
    unique_tips = []
    seen = set()
    for tip in tips:
        if tip not in seen:
            seen.add(tip)
            unique_tips.append(tip)
    
    return unique_tips[:5]
