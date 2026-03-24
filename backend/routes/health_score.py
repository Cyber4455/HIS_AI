import json
from fastapi import APIRouter
from schemas.health_score import HealthScoreInput, HealthScoreResult

router = APIRouter(prefix="/health-score", tags=["Health Score"])

@router.post("/calculate", response_model=HealthScoreResult)
async def calculate_health_score(input_data: HealthScoreInput):
    score = 100
    
    # Blood Pressure
    if input_data.blood_pressure_sys > 140 or input_data.blood_pressure_dia > 90:
        score -= 20
    elif input_data.blood_pressure_sys > 130 or input_data.blood_pressure_dia > 85:
        score -= 10
    elif input_data.blood_pressure_sys < 90 or input_data.blood_pressure_dia < 60:
        score -= 10
    
    # Heart Rate
    if input_data.heart_rate > 100:
        score -= 10
    elif input_data.heart_rate < 60:
        score -= 5
    
    # BMI
    if input_data.bmi > 30:
        score -= 15
    elif input_data.bmi > 25:
        score -= 10
    elif input_data.bmi < 18.5:
        score -= 10
    
    # Glucose
    if input_data.glucose_level:
        if input_data.glucose_level > 140:
            score -= 20
        elif input_data.glucose_level > 100:
            score -= 10
    
    # Cholesterol
    if input_data.cholesterol:
        if input_data.cholesterol > 240:
            score -= 15
        elif input_data.cholesterol > 200:
            score -= 10
    
    # Smoking
    if input_data.smoking == "Yes":
        score -= 15
    
    # Physical Activity
    if input_data.physical_activity == "Low":
        score -= 10
    elif input_data.physical_activity == "High":
        score += 5
    
    # Sleep
    if input_data.sleep_hours < 6 or input_data.sleep_hours > 9:
        score -= 5
    
    # Stress
    if input_data.stress_level == "High":
        score -= 10
    elif input_data.stress_level == "Low":
        score += 5
    
    # Age
    if input_data.age > 60:
        score -= 5
    elif input_data.age > 45:
        score -= 2
    
    score = max(0, min(100, score))
    
    # ─── Classification per HIS AI Spec ───
    # 80–100 = Excellent
    # 60–79  = Moderate
    # 40–59  = At Risk
    # Below 40 = High Risk
    if score >= 80:
        classification = "Excellent"
        risk_level = "Low"
    elif score >= 60:
        classification = "Moderate"
        risk_level = "Medium"
    elif score >= 40:
        classification = "At Risk"
        risk_level = "High"
    else:
        classification = "High Risk"
        risk_level = "Critical"
    
    breakdown = {
        "Blood Pressure": "Normal" if input_data.blood_pressure_sys < 130 else "Elevated",
        "Heart Rate": "Normal" if 60 <= input_data.heart_rate <= 100 else "Abnormal",
        "BMI": "Normal" if 18.5 <= input_data.bmi < 25 else "Outside normal range",
        "Lifestyle": input_data.physical_activity
    }
    
    lifestyle_suggestions = []
    
    if input_data.bmi > 25:
        lifestyle_suggestions.append("Consider a balanced diet and regular exercise to achieve a healthy weight")
    
    if input_data.blood_pressure_sys > 130:
        lifestyle_suggestions.append("Reduce sodium intake and monitor blood pressure regularly")
    
    if input_data.physical_activity == "Low":
        lifestyle_suggestions.append("Aim for at least 30 minutes of moderate exercise daily")
    
    if input_data.sleep_hours < 7:
        lifestyle_suggestions.append("Prioritize getting 7-9 hours of quality sleep each night")
    
    if input_data.stress_level == "High":
        lifestyle_suggestions.append("Consider stress management techniques like meditation or yoga")
    
    if input_data.smoking == "Yes":
        lifestyle_suggestions.append("Quitting smoking would significantly improve your overall health")
    
    if input_data.glucose_level and input_data.glucose_level > 100:
        lifestyle_suggestions.append("Monitor glucose levels and consider dietary changes to manage blood sugar")
    
    if input_data.cholesterol and input_data.cholesterol > 200:
        lifestyle_suggestions.append("Reduce saturated fat intake and consider regular cholesterol monitoring")
    
    if not lifestyle_suggestions:
        lifestyle_suggestions.append("Great job! Maintain your current healthy lifestyle")
    
    return HealthScoreResult(
        score=score,
        classification=classification,
        risk_level=risk_level,
        breakdown=breakdown,
        lifestyle_suggestions=lifestyle_suggestions
    )
