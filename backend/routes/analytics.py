from fastapi import APIRouter
from collections import Counter
import re
import json
from database import get_analytics_data

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard")
async def get_dashboard():
    data = get_analytics_data()
    
    all_symptoms_text = " ".join(data["symptoms_list"]).lower()
    symptom_words = re.findall(r'\b\w+\b', all_symptoms_text)
    common_symptoms = Counter(symptom_words).most_common(10)
    
    disease_list = []
    for diseases_str in data["diseases_list"]:
        try:
            diseases = json.loads(diseases_str)
            for d in diseases:
                disease_list.append(d.get("name", "Unknown"))
        except:
            pass
    
    disease_frequency = Counter(disease_list).most_common(10)
    
    return {
        "total_consultations": data["total_consultations"],
        "high_risk_count": data["high_risk_count"],
        "avg_health_score": data["avg_health_score"],
        "common_symptoms": [{"symptom": s[0], "count": s[1]} for s in common_symptoms],
        "disease_frequency": [{"disease": d[0], "count": d[1]} for d in disease_frequency],
        "risk_distribution": data["risk_distribution"]
    }
