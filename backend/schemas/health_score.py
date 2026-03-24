from pydantic import BaseModel
from typing import List, Optional

class HealthScoreInput(BaseModel):
    age: int
    gender: str
    blood_pressure_sys: int
    blood_pressure_dia: int
    heart_rate: int
    bmi: float
    glucose_level: Optional[float] = None
    cholesterol: Optional[int] = None
    smoking: str = "No"
    physical_activity: str = "Moderate"
    sleep_hours: float = 7.0
    stress_level: str = "Moderate"
    symptoms: Optional[List[str]] = None

class HealthScoreResult(BaseModel):
    score: int
    classification: str  # Excellent, Moderate, At Risk, High Risk
    risk_level: str
    breakdown: dict
    lifestyle_suggestions: List[str]
