import json
from fastapi import APIRouter, HTTPException
from database import save_prediction
from services.gemini_service import GeminiService
from schemas.prediction import DiabetesInput, HeartInput, MalariaInput, TyphoidInput, HypertensionInput, PredictionResult

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/diabetes")
async def predict_diabetes(input_data: DiabetesInput):
    input_dict = input_data.model_dump()
    
    if input_data.glucose_level > 140:
        risk_percentage = min(90, 40 + (input_data.glucose_level - 140) * 0.5)
    elif input_data.glucose_level > 100:
        risk_percentage = 20 + (input_data.glucose_level - 100) * 0.5
    else:
        risk_percentage = 10
    
    if input_data.family_history == "Yes":
        risk_percentage += 15
    
    if input_data.physical_activity == "Low":
        risk_percentage += 10
    elif input_data.physical_activity == "High":
        risk_percentage -= 10
    
    if input_data.bmi > 30:
        risk_percentage += 15
    elif input_data.bmi > 25:
        risk_percentage += 5
    
    risk_percentage = min(95, max(5, risk_percentage))
    
    if risk_percentage > 70:
        risk_level = "High"
    elif risk_percentage > 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    explanation = f"Based on your glucose level of {input_data.glucose_level} mg/dL, BMI of {input_data.bmi}, and other factors."
    
    recommendations = [
        "Maintain a healthy diet with balanced carbohydrates",
        "Exercise regularly for at least 30 minutes daily",
        "Monitor blood sugar levels regularly",
        "Limit sugar and refined carb intake",
        "Stay hydrated"
    ]
    if risk_level == "High":
        recommendations.append("Consult a healthcare provider for further testing")
    
    save_prediction(
        disease_type="Diabetes",
        input_data=json.dumps(input_dict),
        risk_percentage=risk_percentage,
        risk_level=risk_level
    )
    
    return PredictionResult(
        disease="Diabetes",
        risk_percentage=round(risk_percentage, 1),
        risk_level=risk_level,
        explanation=explanation,
        recommendations=recommendations
    )

@router.post("/heart")
async def predict_heart(input_data: HeartInput):
    input_dict = input_data.model_dump()
    
    risk_percentage = 10
    
    if input_data.cholesterol > 240:
        risk_percentage += 25
    elif input_data.cholesterol > 200:
        risk_percentage += 15
    
    if input_data.blood_pressure_sys > 140 or input_data.blood_pressure_dia > 90:
        risk_percentage += 25
    elif input_data.blood_pressure_sys > 130 or input_data.blood_pressure_dia > 85:
        risk_percentage += 15
    
    if input_data.heart_rate > 100:
        risk_percentage += 10
    
    if input_data.smoking == "Yes":
        risk_percentage += 20
    
    if input_data.diabetes == "Yes":
        risk_percentage += 15
    
    if input_data.family_history == "Yes":
        risk_percentage += 15
    
    if input_data.physical_activity == "Low":
        risk_percentage += 10
    elif input_data.physical_activity == "High":
        risk_percentage -= 10
    
    if input_data.age > 55:
        risk_percentage += 10
    
    risk_percentage = min(95, max(5, risk_percentage))
    
    if risk_percentage > 70:
        risk_level = "High"
    elif risk_percentage > 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    explanation = f"Based on your cholesterol level of {input_data.cholesterol} mg/dL, blood pressure of {input_data.blood_pressure_sys}/{input_data.blood_pressure_dia} mmHg, and other risk factors."
    
    recommendations = [
        "Maintain a heart-healthy diet low in saturated fats",
        "Exercise regularly for at least 150 minutes per week",
        "Quit smoking if you smoke",
        "Limit alcohol consumption",
        "Manage stress levels"
    ]
    if risk_level == "High":
        recommendations.append("Consult a cardiologist for further evaluation")
    
    save_prediction(
        disease_type="Heart Disease",
        input_data=json.dumps(input_dict),
        risk_percentage=risk_percentage,
        risk_level=risk_level
    )
    
    return PredictionResult(
        disease="Heart Disease",
        risk_percentage=round(risk_percentage, 1),
        risk_level=risk_level,
        explanation=explanation,
        recommendations=recommendations
    )

@router.post("/malaria")
async def predict_malaria(input_data: MalariaInput):
    input_dict = input_data.model_dump()
    
    risk_percentage = 10
    
    if input_data.fever_duration >= 3:
        risk_percentage += 30
    elif input_data.fever_duration >= 2:
        risk_percentage += 20
    elif input_data.fever_duration >= 1:
        risk_percentage += 10
    
    if input_data.headache == "Yes":
        risk_percentage += 15
    
    if input_data.chills == "Yes":
        risk_percentage += 15
    
    if input_data.vomiting == "Yes":
        risk_percentage += 10
    
    if input_data.travel_to_endemic_area == "Yes":
        risk_percentage += 25
    
    if input_data.use_of_mosquito_net == "No":
        risk_percentage += 15
    
    if input_data.previous_malaria == "Yes":
        risk_percentage += 10
    
    if input_data.age < 5:
        risk_percentage += 10
    elif input_data.age > 60:
        risk_percentage += 10
    
    risk_percentage = min(95, max(5, risk_percentage))
    
    if risk_percentage > 70:
        risk_level = "High"
    elif risk_percentage > 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    explanation = f"Based on fever duration of {input_data.fever_duration} days, symptoms, and exposure risk factors for malaria (common in Uganda)."
    
    recommendations = [
        "Visit a health center for malaria testing (RDT or microscopy)",
        "If positive, start ACT treatment as per Uganda Ministry of Health guidelines",
        "Use mosquito net every night",
        "Remove stagnant water around your home",
        "Take mosquito repellent measures"
    ]
    if risk_level == "High":
        recommendations.append("Seek immediate medical attention - severe malaria can be life-threatening")
    
    save_prediction(
        disease_type="Malaria",
        input_data=json.dumps(input_dict),
        risk_percentage=risk_percentage,
        risk_level=risk_level
    )
    
    return PredictionResult(
        disease="Malaria",
        risk_percentage=round(risk_percentage, 1),
        risk_level=risk_level,
        explanation=explanation,
        recommendations=recommendations
    )

@router.post("/typhoid")
async def predict_typhoid(input_data: TyphoidInput):
    input_dict = input_data.model_dump()
    
    risk_percentage = 10
    
    if input_data.fever_duration >= 5:
        risk_percentage += 30
    elif input_data.fever_duration >= 3:
        risk_percentage += 20
    elif input_data.fever_duration >= 2:
        risk_percentage += 10
    
    if input_data.abdominal_pain == "Yes":
        risk_percentage += 15
    
    if input_data.diarrhea == "Yes":
        risk_percentage += 10
    
    if input_data.headache == "Yes":
        risk_percentage += 10
    
    if input_data.loss_of_appetite == "Yes":
        risk_percentage += 15
    
    if input_data.contaminated_water_exposure == "Yes":
        risk_percentage += 25
    
    if input_data.age < 5:
        risk_percentage += 10
    
    risk_percentage = min(95, max(5, risk_percentage))
    
    if risk_percentage > 70:
        risk_level = "High"
    elif risk_percentage > 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    explanation = f"Based on fever duration of {input_data.fever_duration} days, gastrointestinal symptoms, and exposure to potentially contaminated water (common in areas with poor sanitation)."
    
    recommendations = [
        "Visit a health center for Widal test or Typhoid rapid test",
        "Drink only boiled or bottled water",
        "Eat hot, freshly cooked food",
        "Wash hands with soap regularly",
        "Avoid raw fruits and vegetables from unknown sources"
    ]
    if risk_level == "High":
        recommendations.append("Seek medical attention - typhoid fever requires antibiotic treatment")
    
    save_prediction(
        disease_type="Typhoid",
        input_data=json.dumps(input_dict),
        risk_percentage=risk_percentage,
        risk_level=risk_level
    )
    
    return PredictionResult(
        disease="Typhoid",
        risk_percentage=round(risk_percentage, 1),
        risk_level=risk_level,
        explanation=explanation,
        recommendations=recommendations
    )

@router.post("/hypertension")
async def predict_hypertension(input_data: HypertensionInput):
    input_dict = input_data.model_dump()
    
    risk_percentage = 10
    
    if input_data.blood_pressure_sys >= 180 or input_data.blood_pressure_dia >= 120:
        risk_percentage += 40
    elif input_data.blood_pressure_sys >= 160 or input_data.blood_pressure_dia >= 100:
        risk_percentage += 30
    elif input_data.blood_pressure_sys >= 140 or input_data.blood_pressure_dia >= 90:
        risk_percentage += 20
    elif input_data.blood_pressure_sys >= 130 or input_data.blood_pressure_dia >= 85:
        risk_percentage += 10
    
    if input_data.family_history == "Yes":
        risk_percentage += 15
    
    if input_data.salt_intake == "High":
        risk_percentage += 15
    elif input_data.salt_intake == "Moderate":
        risk_percentage += 5
    
    if input_data.smoking == "Yes":
        risk_percentage += 15
    
    if input_data.physical_activity == "Low":
        risk_percentage += 15
    elif input_data.physical_activity == "High":
        risk_percentage -= 10
    
    if input_data.stress_level == "High":
        risk_percentage += 15
    elif input_data.stress_level == "Moderate":
        risk_percentage += 5
    
    if input_data.bmi > 30:
        risk_percentage += 15
    elif input_data.bmi > 25:
        risk_percentage += 10
    
    if input_data.age > 55:
        risk_percentage += 10
    elif input_data.age > 45:
        risk_percentage += 5
    
    if input_data.gender == "Male":
        risk_percentage += 5
    
    risk_percentage = min(95, max(5, risk_percentage))
    
    if risk_percentage > 70:
        risk_level = "High"
    elif risk_percentage > 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    explanation = f"Based on blood pressure of {input_data.blood_pressure_sys}/{input_data.blood_pressure_dia} mmHg, BMI of {input_data.bmi}, and lifestyle factors."
    
    recommendations = [
        "Reduce salt intake to less than 5g per day",
        "Exercise regularly for at least 30 minutes daily",
        "Maintain healthy weight (BMI < 25)",
        "Quit smoking if you smoke",
        "Limit alcohol consumption",
        "Manage stress through relaxation techniques"
    ]
    if risk_level == "High":
        recommendations.append("Consult a doctor for blood pressure medication evaluation")
    
    save_prediction(
        disease_type="Hypertension",
        input_data=json.dumps(input_dict),
        risk_percentage=risk_percentage,
        risk_level=risk_level
    )
    
    return PredictionResult(
        disease="Hypertension",
        risk_percentage=round(risk_percentage, 1),
        risk_level=risk_level,
        explanation=explanation,
        recommendations=recommendations
    )
