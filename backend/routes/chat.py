import json
from fastapi import APIRouter, HTTPException
from typing import Optional

from database import save_consultation
from services.gemini_service import GeminiService
from services.emergency_detector import detect_emergency
from services.intent_classifier import classify_intent
from schemas.chat import ChatMessage, ChatResponse, SymptomSelectRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

DISCLAIMER = "⚕️ Note: This is a preliminary AI assessment and not a medical diagnosis. If symptoms persist or worsen, please consult a healthcare professional."

@router.post("/message", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    symptoms = message.message
    role = message.user_role.lower()
    
    # Combine selected symptoms with free text if provided
    if message.selected_symptoms:
        combined = ", ".join(message.selected_symptoms)
        if symptoms:
            symptoms = f"{symptoms}. Additional symptoms: {combined}"
        else:
            symptoms = combined
    
    # 1. Classify intent
    intent = classify_intent(symptoms)
    
    # 2. Emergency check (highest priority, overrides intent)
    is_emergency, emergency_msg = detect_emergency(symptoms)
    if is_emergency or intent == "emergency":
        # Save emergency consultation
        save_consultation(
            symptoms=symptoms,
            predicted_diseases="Emergency Pattern Detected",
            health_score=0,
            risk_level="Emergency",
            is_emergency=1,
            user_role=role,
            priority="Emergency"
        )
        return ChatResponse(
            response=(
                "🚨 **MEDICAL EMERGENCY DETECTED**\n\n"
                f"⚠️ {emergency_msg if emergency_msg else 'Your symptoms indicate a potential medical emergency.'}\n\n"
                "**Please seek immediate medical attention.**\n"
                "- Call emergency services (999 or 112) immediately\n"
                "- Do not delay seeking professional help\n"
                "- Stay calm and follow emergency protocols"
            ),
            intent="emergency",
            is_emergency=True,
            emergency_message=emergency_msg if emergency_msg else "Potential medical emergency detected.",
            risk_level="Emergency",
            needs_followup=False,
            disclaimer=DISCLAIMER
        )
    
    # 3. Handle greeting
    if intent == "greeting":
        greeting = GeminiService.get_greeting(role)
        return ChatResponse(
            response=greeting,
            intent="greeting",
            needs_followup=False
        )
    
    # 4. Handle general question
    if intent == "general_question":
        answer = GeminiService.answer_general_question(symptoms, role)
        return ChatResponse(
            response=answer,
            intent="general_question",
            needs_followup=False,
            disclaimer=DISCLAIMER
        )
    
    # 5. Symptom analysis
    gemini_response = GeminiService.chat_symptom_analysis(
        symptoms, 
        role=role,
        conversation_history=None
    )
    
    if gemini_response.get("type") == "followup":
        return ChatResponse(
            response="Thank you for that information. To help you better, could you please provide more details about your symptoms?",
            intent="symptom",
            needs_followup=True,
            disclaimer=DISCLAIMER
        )
    
    elif gemini_response.get("type") == "diagnosis":
        diseases = gemini_response.get("diagnosis", gemini_response.get("diseases", []))
        risk_level = gemini_response.get("risk_level", "Low")
        
        if diseases:
            max_prob = max(d.get("probability", 0.5) for d in diseases)
            health_score = max(0, min(100, int((1 - max_prob) * 100)))
            
            # Determine priority for doctor view
            if risk_level == "High":
                priority = "High Risk"
            elif risk_level == "Moderate":
                priority = "Moderate Risk"
            else:
                priority = "Low Risk"
            
            predicted_diseases_json = json.dumps(diseases)
            save_consultation(
                symptoms=symptoms,
                predicted_diseases=predicted_diseases_json,
                health_score=health_score,
                risk_level=risk_level,
                is_emergency=0,
                user_role=role,
                priority=priority
            )
        
        explanation = gemini_response.get("explanation", "Based on your symptoms:")
        
        # Format response based on role
        if role == "doctor":
            response_text = (
                f"📋 **Clinical Summary**\n\n"
                f"**Reported Symptoms:** {symptoms}\n\n"
                f"**Risk Level:** {'🔴' if risk_level == 'High' else '🟡' if risk_level == 'Moderate' else '🟢'} {risk_level}\n\n"
                f"**Assessment:** {explanation}\n\n"
                f"{DISCLAIMER}"
            )
        else:
            response_text = f"{explanation}\n\n{DISCLAIMER}"
        
        return ChatResponse(
            response=response_text,
            intent="symptom",
            diagnosis=diseases,
            risk_level=risk_level,
            confidence_score=gemini_response.get("confidence_score", 0),
            needs_followup=False,
            disclaimer=DISCLAIMER
        )
    
    return ChatResponse(
        response="I need more information to help you. Could you describe your symptoms in more detail?",
        intent="symptom",
        needs_followup=True,
        disclaimer=DISCLAIMER
    )


@router.post("/symptom-select", response_model=ChatResponse)
async def symptom_select(request: SymptomSelectRequest):
    """Handle structured symptom selection from checkboxes."""
    combined_symptoms = ", ".join(request.symptoms)
    if request.additional_notes:
        combined_symptoms += f". Additional notes: {request.additional_notes}"
    
    # Create a ChatMessage and delegate to the main handler
    msg = ChatMessage(
        message=combined_symptoms,
        user_role=request.user_role,
        selected_symptoms=request.symptoms
    )
    return await send_message(msg)
