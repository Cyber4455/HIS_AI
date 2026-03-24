"""
Doctor Route — Priority-ranked patient queue and clinical summaries.
"""
from fastapi import APIRouter
from database import get_patients_by_priority

router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.get("/patients")
async def get_patients():
    """Get all consultations ranked by priority: Emergency > High Risk > Moderate Risk > Low Risk."""
    patients = get_patients_by_priority()
    
    priority_order = {"Emergency": 0, "High Risk": 1, "Moderate Risk": 2, "Low Risk": 3}
    
    result = []
    for p in patients:
        priority = p.get("priority", "Low Risk") or "Low Risk"
        result.append({
            "id": p["id"],
            "symptoms": p["symptoms"],
            "predicted_diseases": p["predicted_diseases"],
            "health_score": p["health_score"],
            "risk_level": p["risk_level"],
            "priority": priority,
            "is_emergency": bool(p["is_emergency"]),
            "created_at": p["created_at"],
            "user_role": p.get("user_role", "patient"),
            "priority_rank": priority_order.get(priority, 4)
        })
    
    # Sort by priority rank
    result.sort(key=lambda x: x["priority_rank"])
    
    return {
        "total_patients": len(result),
        "emergency_count": sum(1 for p in result if p["priority"] == "Emergency"),
        "high_risk_count": sum(1 for p in result if p["priority"] == "High Risk"),
        "patients": result
    }
