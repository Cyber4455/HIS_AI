import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

def show_disease_predict():
    st.title("❤️ Disease Prediction")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🩸 Diabetes", "❤️ Heart Disease", "🦟 Malaria", "🌡️ Typhoid", "🩺 Hypertension"
    ])
    
    with tab1:
        st.markdown("### Diabetes Risk Assessment")
        
        with st.form("diabetes_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age", min_value=1, max_value=120, value=40)
                gender = st.selectbox("Gender", ["Male", "Female"])
                glucose_level = st.number_input("Glucose Level (mg/dL)", min_value=50, max_value=500, value=100, help="Normal: <100, Prediabetes: 100-125, Diabetes: >126")
                bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, help="Normal: 18.5-24.9, Overweight: 25-29.9, Obese: 30+")
            
            with col2:
                blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=60, max_value=200, value=120)
                family_history = st.selectbox("Family History of Diabetes", ["No", "Yes"])
                physical_activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
            
            submit = st.form_submit_button("Predict Diabetes Risk", use_container_width=True)
            
            if submit:
                with st.spinner("Analyzing risk factors..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/predict/diabetes",
                            json={
                                "age": age,
                                "gender": gender,
                                "glucose_level": glucose_level,
                                "blood_pressure": blood_pressure,
                                "bmi": bmi,
                                "family_history": family_history,
                                "physical_activity": physical_activity
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            risk_color = "🔴" if result["risk_level"] == "High" else "🟡" if result["risk_level"] == "Medium" else "🟢"
                            
                            st.markdown(f"""
                            <div class="glass-card">
                                <h2>{risk_color} Risk Level: {result['risk_level']}</h2>
                                <h3>Risk Percentage: {result['risk_percentage']}%</h3>
                                <p>{result['explanation']}</p>
                                <h4>Recommendations:</h4>
                                <ul>
                                    {"".join([f"<li>{r}</li>" for r in result['recommendations']])}
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                tips_response = requests.post(
                                    f"{API_BASE_URL}/health-tips/generate",
                                    json={
                                        "risk_level": result["risk_level"],
                                        "context": "diabetes prediction"
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
                        else:
                            st.error("Error getting prediction")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        st.info("Make sure the backend server is running on port 8000")
    
    with tab2:
        st.markdown("### Heart Disease Risk Assessment")
        
        with st.form("heart_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age_h = st.number_input("Age", min_value=1, max_value=120, value=50, key="heart_age")
                gender_h = st.selectbox("Gender", ["Male", "Female"], key="heart_gender")
                cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=400, value=200, help="Desirable: <200, Borderline: 200-239, High: 240+")
                blood_pressure_sys = st.number_input("Systolic BP (mmHg)", min_value=70, max_value=250, value=120, help="Normal: <120, Elevated: 120-129, High: 130+")
            
            with col2:
                blood_pressure_dia = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=150, value=80, help="Normal: <80, High: 80+")
                heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
                smoking = st.selectbox("Smoking", ["No", "Yes"])
                diabetes = st.selectbox("Diabetes", ["No", "Yes"], key="heart_diabetes")
            
            family_history_h = st.selectbox("Family History of Heart Disease", ["No", "Yes"])
            physical_activity_h = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
            
            submit_h = st.form_submit_button("Predict Heart Disease Risk", use_container_width=True)
            
            if submit_h:
                with st.spinner("Analyzing risk factors..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/predict/heart",
                            json={
                                "age": age_h,
                                "gender": gender_h,
                                "cholesterol": cholesterol,
                                "blood_pressure_sys": blood_pressure_sys,
                                "blood_pressure_dia": blood_pressure_dia,
                                "heart_rate": heart_rate,
                                "smoking": smoking,
                                "diabetes": diabetes,
                                "family_history": family_history_h,
                                "physical_activity": physical_activity_h
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            risk_color = "🔴" if result["risk_level"] == "High" else "🟡" if result["risk_level"] == "Medium" else "🟢"
                            
                            st.markdown(f"""
                            <div class="glass-card">
                                <h2>{risk_color} Risk Level: {result['risk_level']}</h2>
                                <h3>Risk Percentage: {result['risk_percentage']}%</h3>
                                <p>{result['explanation']}</p>
                                <h4>Recommendations:</h4>
                                <ul>
                                    {"".join([f"<li>{r}</li>" for r in result['recommendations']])}
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                tips_response = requests.post(
                                    f"{API_BASE_URL}/health-tips/generate",
                                    json={
                                        "risk_level": result["risk_level"],
                                        "context": "heart disease prediction"
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
                        else:
                            st.error("Error getting prediction")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        st.info("Make sure the backend server is running on port 8000")
    
    with tab3:
        st.markdown("### Malaria Risk Assessment")
        st.markdown("<small style='color: #333333;'>Malaria is endemic in Uganda - take precautions!</small>", unsafe_allow_html=True)
        
        with st.form("malaria_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age_m = st.number_input("Age", min_value=1, max_value=120, value=25, key="malaria_age")
                fever_duration = st.number_input("Fever Duration (days)", min_value=0, max_value=30, value=2, help="How many days have you had fever?")
                headache = st.selectbox("Headache", ["No", "Yes"], key="malaria_headache")
                chills = st.selectbox("Chills/Shaking", ["No", "Yes"], key="malaria_chills")
            
            with col2:
                vomiting = st.selectbox("Vomiting", ["No", "Yes"], key="malaria_vomiting")
                travel_to_endemic = st.selectbox("Recent Travel to Malaria Endemic Area", ["No", "Yes"], key="malaria_travel")
                use_mosquito_net = st.selectbox("Use of Mosquito Net", ["Yes", "No"], key="malaria_net")
                previous_malaria = st.selectbox("Previous Malaria Episode", ["No", "Yes"], key="malaria_prev")
            
            submit_m = st.form_submit_button("Predict Malaria Risk", use_container_width=True)
            
            if submit_m:
                with st.spinner("Analyzing risk factors..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/predict/malaria",
                            json={
                                "age": age_m,
                                "fever_duration": fever_duration,
                                "headache": headache,
                                "chills": chills,
                                "vomiting": vomiting,
                                "travel_to_endemic_area": travel_to_endemic,
                                "use_of_mosquito_net": use_mosquito_net,
                                "previous_malaria": previous_malaria
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            risk_color = "🔴" if result["risk_level"] == "High" else "🟡" if result["risk_level"] == "Medium" else "🟢"
                            
                            st.markdown(f"""
                            <div class="glass-card">
                                <h2>{risk_color} Risk Level: {result['risk_level']}</h2>
                                <h3>Risk Percentage: {result['risk_percentage']}%</h3>
                                <p>{result['explanation']}</p>
                                <h4>Recommendations:</h4>
                                <ul>
                                    {"".join([f"<li>{r}</li>" for r in result['recommendations']])}
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                tips_response = requests.post(
                                    f"{API_BASE_URL}/health-tips/generate",
                                    json={
                                        "risk_level": result["risk_level"],
                                        "context": "malaria prediction"
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
                        else:
                            st.error("Error getting prediction")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        st.info("Make sure the backend server is running on port 8000")
    
    with tab4:
        st.markdown("### Typhoid Risk Assessment")
        
        with st.form("typhoid_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age_t = st.number_input("Age", min_value=1, max_value=120, value=25, key="typhoid_age")
                fever_duration_t = st.number_input("Fever Duration (days)", min_value=0, max_value=30, value=3, help="Prolonged fever is a key symptom")
                abdominal_pain = st.selectbox("Abdominal Pain", ["No", "Yes"], key="typhoid_abdominal")
                diarrhea = st.selectbox("Diarrhea", ["No", "Yes"], key="typhoid_diarrhea")
            
            with col2:
                headache_t = st.selectbox("Headache", ["No", "Yes"], key="typhoid_headache")
                loss_of_appetite = st.selectbox("Loss of Appetite", ["No", "Yes"], key="typhoid_appetite")
                contaminated_water = st.selectbox("Contaminated Water Exposure", ["No", "Yes"], key="typhoid_water")
            
            submit_t = st.form_submit_button("Predict Typhoid Risk", use_container_width=True)
            
            if submit_t:
                with st.spinner("Analyzing risk factors..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/predict/typhoid",
                            json={
                                "age": age_t,
                                "fever_duration": fever_duration_t,
                                "abdominal_pain": abdominal_pain,
                                "diarrhea": diarrhea,
                                "headache": headache_t,
                                "loss_of_appetite": loss_of_appetite,
                                "contaminated_water_exposure": contaminated_water
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            risk_color = "🔴" if result["risk_level"] == "High" else "🟡" if result["risk_level"] == "Medium" else "🟢"
                            
                            st.markdown(f"""
                            <div class="glass-card">
                                <h2>{risk_color} Risk Level: {result['risk_level']}</h2>
                                <h3>Risk Percentage: {result['risk_percentage']}%</h3>
                                <p>{result['explanation']}</p>
                                <h4>Recommendations:</h4>
                                <ul>
                                    {"".join([f"<li>{r}</li>" for r in result['recommendations']])}
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                tips_response = requests.post(
                                    f"{API_BASE_URL}/health-tips/generate",
                                    json={
                                        "risk_level": result["risk_level"],
                                        "context": "typhoid prediction"
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
                        else:
                            st.error("Error getting prediction")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        st.info("Make sure the backend server is running on port 8000")
    
    with tab5:
        st.markdown("### Hypertension (High Blood Pressure) Risk Assessment")
        
        with st.form("hypertension_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age_hyp = st.number_input("Age", min_value=1, max_value=120, value=40, key="hyp_age")
                gender_hyp = st.selectbox("Gender", ["Male", "Female"], key="hyp_gender")
                bmi_hyp = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, help="Normal: 18.5-24.9")
                blood_pressure_sys_hyp = st.number_input("Systolic BP (mmHg)", min_value=70, max_value=250, value=120, help="Normal: <120")
            
            with col2:
                blood_pressure_dia_hyp = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=150, value=80, help="Normal: <80")
                family_history_hyp = st.selectbox("Family History of Hypertension", ["No", "Yes"])
                salt_intake = st.selectbox("Salt Intake", ["Low", "Moderate", "High"])
                physical_activity_hyp = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
            
            col3, col4 = st.columns(2)
            with col3:
                smoking_hyp = st.selectbox("Smoking", ["No", "Yes"], key="hyp_smoking")
            with col4:
                stress_level = st.selectbox("Stress Level", ["Low", "Moderate", "High"], key="hyp_stress")
            
            submit_hyp = st.form_submit_button("Predict Hypertension Risk", use_container_width=True)
            
            if submit_hyp:
                with st.spinner("Analyzing risk factors..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/predict/hypertension",
                            json={
                                "age": age_hyp,
                                "gender": gender_hyp,
                                "blood_pressure_sys": blood_pressure_sys_hyp,
                                "blood_pressure_dia": blood_pressure_dia_hyp,
                                "bmi": bmi_hyp,
                                "family_history": family_history_hyp,
                                "salt_intake": salt_intake,
                                "physical_activity": physical_activity_hyp,
                                "smoking": smoking_hyp,
                                "stress_level": stress_level
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            risk_color = "🔴" if result["risk_level"] == "High" else "🟡" if result["risk_level"] == "Medium" else "🟢"
                            
                            st.markdown(f"""
                            <div class="glass-card">
                                <h2>{risk_color} Risk Level: {result['risk_level']}</h2>
                                <h3>Risk Percentage: {result['risk_percentage']}%</h3>
                                <p>{result['explanation']}</p>
                                <h4>Recommendations:</h4>
                                <ul>
                                    {"".join([f"<li>{r}</li>" for r in result['recommendations']])}
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                tips_response = requests.post(
                                    f"{API_BASE_URL}/health-tips/generate",
                                    json={
                                        "risk_level": result["risk_level"],
                                        "context": "hypertension prediction"
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
                        else:
                            st.error("Error getting prediction")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        st.info("Make sure the backend server is running on port 8000")
