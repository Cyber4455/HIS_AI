import streamlit as st
import requests
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

def show_history():
    if st.session_state.get("is_guest", False):
        st.warning("⚠️ Access Restricted")
        st.markdown("""
        <div style="background: rgba(255, 200, 0, 0.1); padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #FFC800;">
            <h3 style="color: #663399; margin-bottom: 10px;">Guest users cannot access History</h3>
            <p style="color: #333333;">
                Your consultations are not saved because you're using a guest session. 
                Please <strong>login</strong> or <strong>register</strong> an account to save your consultation history.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to Dashboard", use_container_width=True):
            st.session_state.current_page = "Dashboard"
            st.rerun()
        return
    
    st.title("📋 Consultation History")
    
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/dashboard")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total_consultations", 0)
            
            if total > 0:
                st.markdown(f"### Total Consultations: {total}")
                
                disease_freq = data.get("disease_frequency", [])
                if disease_freq:
                    st.markdown("**Recent Disease Predictions:**")
                    for d in disease_freq:
                        st.markdown(f"- {d.get('disease', 'Unknown')}: {d.get('count', 0)} times")
                
                risk_dist = data.get("risk_distribution", {})
                if risk_dist:
                    st.markdown("**Risk Level Distribution:**")
                    for level, count in risk_dist.items():
                        emoji = "🔴" if level == "High" else "🟡" if level == "Medium" else "🟢"
                        st.markdown(f"- {emoji} {level}: {count}")
                
                st.markdown("---")
                st.info("Note: Consultations are automatically saved when you receive a diagnosis from the AI chatbot")
            else:
                st.info("No consultations yet. Start a chat with the AI chatbot to get started!")
        else:
            st.error("Error loading consultation history")
            
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.info("Make sure the backend server is running")
