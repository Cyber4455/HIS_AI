import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

def show_health_score():
    st.title("📊 Health Score Calculator")
    
    st.markdown("""
    Calculate your overall **Health Score (0–100)** based on vitals and lifestyle factors.
    
    | Score Range | Classification |
    |------------|---------------|
    | 80–100 | 🟢 Excellent |
    | 60–79 | 🟡 Moderate |
    | 40–59 | 🟠 At Risk |
    | Below 40 | 🔴 High Risk |
    """)
    
    with st.form("health_score_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=35)
            gender = st.selectbox("Gender", ["Male", "Female"])
            blood_pressure_sys = st.number_input("Systolic Blood Pressure (mmHg)", min_value=70, max_value=250, value=120)
            blood_pressure_dia = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=40, max_value=150, value=80)
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=72)
        
        with col2:
            bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=24.0)
            glucose_level = st.number_input("Glucose Level (mg/dL)", min_value=50, max_value=500, value=90, help="Normal: <100, Prediabetes: 100-125, Diabetes: >126")
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=400, value=180, help="Desirable: <200, Borderline: 200-239, High: 240+")
        
        smoking = st.selectbox("Smoking", ["No", "Yes"])
        physical_activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
        sleep_hours = st.slider("Sleep Hours (per night)", 3.0, 12.0, 7.0, 0.5)
        stress_level = st.select_slider("Stress Level", ["Low", "Moderate", "High"], value="Moderate")
        
        submit = st.form_submit_button("Calculate Health Score")
        
        if submit:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/health-score/calculate",
                    json={
                        "age": age,
                        "gender": gender,
                        "blood_pressure_sys": blood_pressure_sys,
                        "blood_pressure_dia": blood_pressure_dia,
                        "heart_rate": heart_rate,
                        "bmi": bmi,
                        "glucose_level": glucose_level if glucose_level else None,
                        "cholesterol": cholesterol if cholesterol else None,
                        "smoking": smoking,
                        "physical_activity": physical_activity,
                        "sleep_hours": sleep_hours,
                        "stress_level": stress_level
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    score = result["score"]
                    classification = result.get("classification", "Unknown")
                    risk_level = result.get("risk_level", "Unknown")
                    
                    # Color based on classification
                    if classification == "Excellent":
                        color_emoji = "🟢"
                        bar_color = "#22C55E"
                    elif classification == "Moderate":
                        color_emoji = "🟡"
                        bar_color = "#FFAA00"
                    elif classification == "At Risk":
                        color_emoji = "🟠"
                        bar_color = "#FF6B00"
                    else:  # High Risk
                        color_emoji = "🔴"
                        bar_color = "#FF0000"
                    
                    st.markdown("---")
                    st.markdown(f"## {color_emoji} Health Score: **{score}/100**")
                    st.markdown(f"### Classification: **{classification}** | Risk Level: **{risk_level}**")
                    st.progress(score / 100)
                    
                    # Breakdown
                    st.markdown("### 📋 Breakdown")
                    breakdown = result.get("breakdown", {})
                    for key, value in breakdown.items():
                        status_emoji = "✅" if value in ["Normal", "High", "Moderate"] else "⚠️"
                        st.markdown(f"- {status_emoji} **{key}**: {value}")
                    
                    # Lifestyle Suggestions
                    st.markdown("### 💡 Lifestyle Suggestions")
                    suggestions = result.get("lifestyle_suggestions", [])
                    for suggestion in suggestions:
                        st.success(f"💡 {suggestion}")
                    
                    # Health Tips
                    try:
                        tips_response = requests.post(
                            f"{API_BASE_URL}/health-tips/generate",
                            json={
                                "health_score": score,
                                "risk_level": risk_level,
                                "context": "health score assessment"
                            },
                            timeout=5
                        )
                        if tips_response.status_code == 200:
                            tips_data = tips_response.json()
                            tips = tips_data.get("tips", [])
                            if tips:
                                st.markdown("### 🧠 Personalized Health Tips")
                                for i, tip in enumerate(tips, 1):
                                    st.markdown(f"💡 **{tip}**")
                    except:
                        pass
                    
                    st.markdown("---")
                    st.markdown("*⚕️ This is a preliminary AI assessment and not a medical diagnosis.*")
                    
                else:
                    st.error("Error calculating health score")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
                st.info("Make sure the backend server is running on port 8000")
