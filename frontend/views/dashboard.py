import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

def show_dashboard():
    user_info = st.session_state.get("user_info", {})
    username = user_info.get("username", "User")
    user_role = st.session_state.get("user_role", "patient")
    is_guest = st.session_state.get("is_guest", False)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F5F5F5 0%, #F0F0F5 100%); padding: 30px; border-radius: 16px; margin-bottom: 30px; border: 1px solid rgba(102, 51, 153, 0.15); box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h1 style="margin-bottom: 10px; color: #663399;">Welcome back, {}!</h1>
        <p style="color: #000000; font-size: 1.1em;">Health Intelligence System — Your AI-Powered Health Assistant</p>
    </div>
    """.format(username), unsafe_allow_html=True)
    
    st.markdown("### 🚀 Quick Access")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="cursor: pointer; text-align: center;" onclick="document.querySelector('[key=nav_Chat]').click();">
            <h2 style="font-size: 2.5em; margin-bottom: 10px;">💬</h2>
            <h3 style="color: #663399;">AI Chat</h3>
            <p style="color: #333; font-size: 0.9em;">Chat with our AI assistant</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💬 Go to Chat", use_container_width=True, key="quick_chat"):
            st.session_state.current_page = "Chat"
            st.rerun()
    
    with col2:
        if st.button("❤️ Disease Prediction", use_container_width=True, key="quick_predict"):
            st.session_state.current_page = "Disease Prediction"
            st.rerun()
    
    with col3:
        if st.button("📊 Health Score", use_container_width=True, key="quick_score"):
            st.session_state.current_page = "Health Score"
            st.rerun()
    
    with col4:
        if not is_guest:
            if st.button("📋 History", use_container_width=True, key="quick_history"):
                st.session_state.current_page = "History"
                st.rerun()
        else:
            st.markdown("""
            <div style="background: rgba(102, 51, 153, 0.08); padding: 15px; border-radius: 8px; text-align: center; color: #663399;">
                <p>History unavailable for guests</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.expander("🧠 AI Health Tips", expanded=True):
        try:
            tips_response = requests.get(f"{API_BASE_URL}/health-tips/general")
            if tips_response.status_code == 200:
                tips_data = tips_response.json()
                tips = tips_data.get("tips", [])
                
                if tips:
                    for i, tip in enumerate(tips, 1):
                        st.markdown("""
                        <div style="background: rgba(102, 51, 153, 0.1); padding: 15px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #663399;">
                            <strong style="color: #663399;">💡 Tip {}:</strong> {}
                        </div>
                        """.format(i, tip), unsafe_allow_html=True)
                else:
                    st.info("No health tips available at the moment.")
            else:
                st.info("Loading health tips...")
        except Exception as e:
            st.info("Connect to the API to see personalized health tips.")
    
    st.markdown("---")
    
    st.markdown("### 📈 Analytics Summary")
    
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/dashboard", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Consultations", data.get("total_consultations", 0), delta_color="normal")
            with col2:
                st.metric("High Risk Cases", data.get("high_risk_count", 0), delta_color="inverse")
            with col3:
                st.metric("Avg Health Score", f"{data.get('avg_health_score', 0)}")
            with col4:
                risk_dist = data.get("risk_distribution", {})
                total_risk = sum(risk_dist.values()) if risk_dist else 1
                high_pct = (risk_dist.get("High", 0) / total_risk * 100) if total_risk > 0 else 0
                st.metric("High Risk %", f"{high_pct:.1f}%")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Common Symptoms")
                symptoms = data.get("common_symptoms", [])
                if symptoms:
                    symptom_names = [s.get("symptom", "") for s in symptoms[:6]]
                    symptom_counts = [s.get("count", 0) for s in symptoms[:6]]
                    
                    fig_symptoms = px.bar(
                        x=symptom_counts,
                        y=symptom_names,
                        orientation='h',
                        labels={'x': 'Count', 'y': 'Symptom'},
                        title="Top Symptoms",
                        color=symptom_counts,
                        color_continuous_scale='Blues'
                    )
                    fig_symptoms.update_layout(yaxis={'categoryorder': 'total ascending'}, height=300)
                    st.plotly_chart(fig_symptoms, use_container_width=True)
                else:
                    st.info("No symptom data available yet")
            
            with col2:
                st.markdown("#### Risk Distribution")
                risk_dist = data.get("risk_distribution", {})
                if risk_dist:
                    risk_levels = list(risk_dist.keys())
                    risk_counts = list(risk_dist.values())
                    risk_colors = {'High': '#FF4444', 'Medium': '#FFAA00', 'Low': '#44FF44', 'Emergency': '#FF0000'}
                    colors = [risk_colors.get(r, '#888888') for r in risk_levels]
                    
                    fig_risk = px.pie(
                        values=risk_counts,
                        names=risk_levels,
                        title="Risk Level Distribution",
                        color_discrete_sequence=colors
                    )
                    fig_risk.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_risk, use_container_width=True)
                else:
                    st.info("No risk distribution data available")
            
            st.markdown("---")
            st.markdown("#### Disease Frequency")
            diseases = data.get("disease_frequency", [])
            if diseases:
                disease_names = [d.get("disease", "Unknown") for d in diseases[:6]]
                disease_counts = [d.get("count", 0) for d in diseases[:6]]
                
                fig_diseases = px.bar(
                    x=disease_counts,
                    y=disease_names,
                    orientation='h',
                    labels={'x': 'Count', 'y': 'Disease'},
                    title="Disease Frequency",
                    color=disease_counts,
                    color_continuous_scale='Reds'
                )
                fig_diseases.update_layout(yaxis={'categoryorder': 'total ascending'}, height=300)
                st.plotly_chart(fig_diseases, use_container_width=True)
            else:
                st.info("No disease data available yet. Start using the chatbot to generate data!")
        else:
            st.error("Error loading dashboard data")
            
    except Exception as e:
        st.warning("Unable to connect to API. Showing sample preview.")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Consultations", "0")
        with col2:
            st.metric("High Risk Cases", "0")
        with col3:
            st.metric("Avg Health Score", "0")
        with col4:
            st.metric("High Risk %", "0%")
        
        st.info("Data will appear here after you start using the app. Make sure the backend server is running on port 8000.")
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #CC0000; font-size: 0.85em; padding: 15px; background: rgba(204, 0, 0, 0.05); border-radius: 8px;">
        ⚠️ This platform is for preliminary assessment only and does NOT replace professional medical care.
    </div>
    """, unsafe_allow_html=True)
