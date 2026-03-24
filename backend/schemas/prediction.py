from pydantic import BaseModel
from typing import Optional, Dict, Any

class PredictionInput(BaseModel):
    age: int
    gender: str
    symptoms: str
    additional_data: Dict[str, Any]

class PredictionResult(BaseModel):
    disease: str
    risk_percentage: float
    risk_level: str
    explanation: str
    recommendations: list[str]

class DiabetesInput(BaseModel):
    age: int
    gender: str
    glucose_level: float
    blood_pressure: int
    bmi: float
    insulin_level: Optional[float] = None
    family_history: str = "No"
    physical_activity: str = "Moderate"

class HeartInput(BaseModel):
    age: int
    gender: str
    cholesterol: int
    blood_pressure_sys: int
    blood_pressure_dia: int
    heart_rate: int
    smoking: str = "No"
    diabetes: str = "No"
    family_history: str = "No"
    physical_activity: str = "Moderate"

class MalariaInput(BaseModel):
    age: int
    fever_duration: int
    headache: str
    chills: str
    vomiting: str
    travel_to_endemic_area: str
    use_of_mosquito_net: str
    previous_malaria: str

class TyphoidInput(BaseModel):
    age: int
    fever_duration: int
    abdominal_pain: str
    diarrhea: str
    headache: str
    loss_of_appetite: str
    contaminated_water_exposure: str

class HypertensionInput(BaseModel):
    age: int
    gender: str
    blood_pressure_sys: int
    blood_pressure_dia: int
    bmi: float
    family_history: str
    salt_intake: str
    physical_activity: str
    smoking: str
    stress_level: str
