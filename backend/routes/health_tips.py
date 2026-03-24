from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from services.health_tips import generate_health_tips

router = APIRouter(prefix="/health-tips", tags=["Health Tips"])

class HealthTipsRequest(BaseModel):
    symptoms: Optional[List[str]] = None
    risk_level: Optional[str] = None
    health_score: Optional[int] = None
    context: Optional[str] = None

class HealthTipsResponse(BaseModel):
    tips: List[str]

@router.post("/generate", response_model=HealthTipsResponse)
async def create_health_tips(request: HealthTipsRequest):
    tips = generate_health_tips(
        symptoms=request.symptoms,
        risk_level=request.risk_level,
        health_score=request.health_score,
        context=request.context
    )
    return HealthTipsResponse(tips=tips)

@router.get("/general", response_model=HealthTipsResponse)
async def get_general_health_tips():
    tips = generate_health_tips()
    return HealthTipsResponse(tips=tips)
