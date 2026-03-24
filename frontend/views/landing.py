import streamlit as st

def show_landing():
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1 style="font-size: 3.5em; margin-bottom: 10px;">
            <span class="gradient-text">HIS AI</span>
        </h1>
        <h2 style="font-size: 1.6em; color: #663399; margin-bottom: 10px; font-weight: 400;">
            Health Intelligence System
        </h2>
        <p style="font-size: 1.2em; color: #000000; max-width: 700px; margin: 0 auto 30px;">
            Hybrid AI-Powered Clinical Decision Support Platform<br>
            <span style="font-size: 0.85em;">Preliminary medical assessment • Symptom analysis • Disease prediction • Health monitoring</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get("logged_in"):
        st.markdown("### Welcome back!")
        col1, col2 = st.columns(2)
        
        with col1:
            role = st.session_state.get("user_role", "patient")
            role_emoji = {"patient": "🩺", "doctor": "👨‍⚕️", "admin": "⚙️"}.get(role, "👤")
            st.markdown(f"**{role_emoji} Logged in as: {role.capitalize()}**")
        
        with col2:
            if st.button("Go to Chat", use_container_width=True):
                st.session_state.current_page = "Chat"
                st.rerun()
        
        st.markdown("---")
    
    st.markdown("### 👤 Select Your Role")
    st.markdown("<p style='color: #333; margin-bottom: 20px;'>Choose your role to access the appropriate features and interface.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center; min-height: 220px;">
            <h2 style="font-size: 2.5em; margin-bottom: 10px;">🩺</h2>
            <h3 style="color: #663399;">Patient</h3>
            <p style="color: #000000; font-size: 0.9em;">
                Chat with AI about symptoms, get preliminary assessments, 
                health score calculator, and disease risk prediction.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Continue as Patient", use_container_width=True, key="role_patient"):
            st.session_state.user_role = "patient"
            st.session_state.current_page = "Chat"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center; min-height: 220px;">
            <h2 style="font-size: 2.5em; margin-bottom: 10px;">👨‍⚕️</h2>
            <h3 style="color: #F5A623;">Doctor</h3>
            <p style="color: #000000; font-size: 0.9em;">
                View priority-ranked patient queue, structured clinical summaries, 
                emergency flags, and risk stratification.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Continue as Doctor", use_container_width=True, key="role_doctor"):
            st.session_state.user_role = "doctor"
            st.session_state.current_page = "Doctor Dashboard"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ⚡ Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Chatbot</h3>
            <p>Describe symptoms and get AI-powered analysis with intent classification and role-based responses</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>❤️ Disease Prediction</h3>
            <p>Predict risks for Diabetes, Heart Disease, Malaria, Typhoid, and Hypertension</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Emergency Detection</h3>
            <p>Instant alerts for dangerous symptom combinations requiring immediate medical attention</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Health Score (0-100)</h3>
            <p>Calculate your health score: Excellent (80-100), Moderate (60-79), At Risk (40-59), High Risk (&lt;40)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>👨‍⚕️ Doctor Priority Queue</h3>
            <p>Automatic patient ranking by severity: Emergency → High Risk → Moderate → Low</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Analytics Dashboard</h3>
            <p>System-wide health trends, risk distribution, and consultation statistics</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About HIS AI")
    st.markdown("""
    <div class="glass-card">
        <p style="color: #000000;">
            HIS AI (Health Intelligence System) is a hybrid AI-powered clinical decision support platform designed 
            for preliminary medical assessment and health monitoring. It uses advanced AI to analyze symptoms, 
            predict disease risks, and provide health recommendations.
        </p>
        <p style="color: #333; font-size: 0.9em;">
            <strong>Target Region:</strong> Uganda (East Africa)<br>
            <strong>Emergency Contacts:</strong> Police 999/112 | Ambulance 911 | Uganda Red Cross 0800-100-225
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #333333; font-size: 1em;">
            <strong>Tech Stack:</strong> Streamlit • FastAPI • Gemini AI • SQLite
        </p>
        <p style="color: #CC0000; font-size: 0.85em;">
            ⚠️ This platform is for preliminary assessment only and does NOT replace professional medical care.
        </p>
    </div>
    """, unsafe_allow_html=True)
