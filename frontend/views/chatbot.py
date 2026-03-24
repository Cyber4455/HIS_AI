import streamlit as st
import requests
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

# Symptom categories for structured selector
SYMPTOM_CATEGORIES = {
    "🤒 General": ["Fever", "Fatigue", "Weakness", "Chills", "Weight Loss", "Weight Gain", "Loss of Appetite"],
    "🫁 Respiratory": ["Cough", "Shortness of Breath", "Wheezing", "Sore Throat", "Runny Nose", "Sneezing", "Congestion"],
    "❤️ Cardiac": ["Chest Pain", "Chest Tightness", "Palpitations", "Rapid Heart Rate", "Sweating"],
    "🧠 Neurological": ["Headache", "Dizziness", "Numbness", "Tingling", "Confusion", "Slurred Speech", "Blurred Vision"],
    "🤢 Digestive": ["Nausea", "Vomiting", "Diarrhea", "Constipation", "Stomach Pain", "Bloating", "Abdominal Pain"],
    "💪 Musculoskeletal": ["Back Pain", "Joint Pain", "Muscle Pain", "Stiffness", "Swelling", "Cramps"],
    "🩹 Skin": ["Rash", "Itching", "Bruising", "Skin Discoloration"],
    "😰 Mental Health": ["Anxiety", "Insomnia", "Stress", "Mood Changes"],
}

def show_chatbot():
    role = st.session_state.get("user_role", "patient")
    
    if role == "doctor":
        st.title("🏥 Clinical Symptom Analyzer")
        st.markdown("*Enter patient symptoms for structured clinical analysis*")
    else:
        st.title("🏥 HIS AI Health Chatbot")
        st.markdown("*Describe your symptoms or ask health questions*")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # ─── Structured Symptom Selector ───
    with st.expander("📋 Structured Symptom Selector", expanded=False):
        st.markdown("Select symptoms from the categories below:")
        
        selected_symptoms = []
        
        cols = st.columns(2)
        for i, (category, symptoms) in enumerate(SYMPTOM_CATEGORIES.items()):
            with cols[i % 2]:
                st.markdown(f"**{category}**")
                for symptom in symptoms:
                    if st.checkbox(symptom, key=f"sym_{symptom}"):
                        selected_symptoms.append(symptom)
        
        additional_notes = st.text_area("Additional notes (optional):", key="sym_notes", height=60)
        
        if st.button("🔍 Analyze Selected Symptoms", use_container_width=True, key="analyze_selected"):
            if selected_symptoms:
                combined = ", ".join(selected_symptoms)
                display_msg = f"**Selected symptoms:** {combined}"
                if additional_notes:
                    display_msg += f"\n**Notes:** {additional_notes}"
                
                st.session_state.chat_history.append({"role": "user", "content": display_msg})
                
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/chat/symptom-select",
                        json={
                            "user_role": role,
                            "symptoms": selected_symptoms,
                            "additional_notes": additional_notes if additional_notes else None
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        _process_response(data, role)
                    else:
                        st.error("Error getting response from server")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
                    st.info("Make sure the backend server is running on port 8000")
                
                st.rerun()
            else:
                st.warning("Please select at least one symptom")
    
    st.markdown("---")
    
    # ─── Chat History ───
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # ─── Chat Input ───
    placeholder = "Enter patient symptoms..." if role == "doctor" else "Describe your symptoms, say hello, or ask a health question..."
    user_input = st.chat_input(placeholder)
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat/message",
                json={
                    "message": user_input,
                    "user_role": role
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                _process_response(data, role)
            else:
                st.error("Error getting response from server")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            st.info("Make sure the backend server is running on port 8000")
    
    # ─── Clear Button ───
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


def _process_response(data, role):
    """Process the API response and add to chat history."""
    intent = data.get("intent", "general_question")
    
    if data.get("is_emergency"):
        response_text = data.get("response", "")
        st.error(f"🚨 EMERGENCY DETECTED")
        
        with st.chat_message("assistant"):
            st.markdown(response_text)
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response_text
        })
        return
    
    response_text = data.get("response", "")
    
    # Build diagnosis display
    if data.get("diagnosis"):
        if intent == "symptom":
            response_text += "\n\n**Possible Conditions:**\n"
            for disease in data["diagnosis"]:
                prob_pct = disease.get("probability", 0) * 100
                response_text += f"\n- **{disease.get('name', 'Unknown')}**: {prob_pct:.1f}%\n"
                
                if disease.get("precautions"):
                    response_text += "  - 🛡️ Precautions: " + ", ".join(disease["precautions"]) + "\n"
                if disease.get("medicines"):
                    response_text += "  - 💊 Suggested medicines: " + ", ".join(disease["medicines"]) + "\n"
            
            if data.get("risk_level"):
                risk_emoji = "🔴" if data["risk_level"] == "High" else "🟡" if data["risk_level"] == "Moderate" else "🟢"
                response_text += f"\n**Risk Level:** {risk_emoji} {data['risk_level']}"
            
            if data.get("confidence_score"):
                response_text += f"\n**Confidence Score**: {data['confidence_score']*100:.1f}%"
            
            # Offer health score calculation
            response_text += "\n\n💡 *You can calculate your overall Health Score in the Health Score section.*"
    
    with st.chat_message("assistant"):
        st.markdown(response_text)
    
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": response_text
    })
    
    # Add health tips if diagnosis was made
    if data.get("diagnosis") or data.get("risk_level"):
        try:
            symptoms_list = []
            if data.get("diagnosis"):
                for d in data["diagnosis"]:
                    symptoms_list.append(d.get("name", ""))
            
            tips_response = requests.post(
                f"{API_BASE_URL}/health-tips/generate",
                json={
                    "symptoms": symptoms_list if symptoms_list else None,
                    "risk_level": data.get("risk_level"),
                    "context": "chatbot diagnosis"
                },
                timeout=5
            )
            if tips_response.status_code == 200:
                tips_data = tips_response.json()
                tips = tips_data.get("tips", [])
                if tips:
                    tips_text = "\n\n### 🧠 Personalized Health Tips\n"
                    for i, tip in enumerate(tips, 1):
                        tips_text += f"\n💡 **{tip}**\n"
                    
                    with st.chat_message("assistant"):
                        st.markdown(tips_text)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": tips_text
                    })
        except:
            pass
