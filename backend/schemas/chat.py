from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    message: str
    user_role: str = "patient"  # patient, doctor, admin
    session_id: Optional[str] = None
    selected_symptoms: Optional[List[str]] = None  # from structured symptom selector

class DiseaseInfo(BaseModel):
    name: str
    probability: float
    precautions: List[str]
    medicines: List[str]

class ChatResponse(BaseModel):
    response: str
    intent: str = "general_question"  # greeting, general_question, symptom, emergency
    diagnosis: Optional[List[DiseaseInfo]] = None
    confidence_score: Optional[float] = None
    risk_level: Optional[str] = None
    is_emergency: bool = False
    emergency_message: Optional[str] = None
    needs_followup: bool = False
    disclaimer: Optional[str] = None

class ChatStartResponse(BaseModel):
    session_id: str
    message: str

class SymptomSelectRequest(BaseModel):
    user_role: str = "patient"
    symptoms: List[str]
    additional_notes: Optional[str] = None
