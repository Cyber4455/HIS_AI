import streamlit as st
import requests
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

def show_doctor_dashboard():
    st.title("👨‍⚕️ Doctor Dashboard — Patient Priority Queue")
    st.markdown("*Patients ranked by clinical priority: Emergency → High Risk → Moderate → Low*")
    
    try:
        response = requests.get(f"{API_BASE_URL}/doctor/patients")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total_patients", 0)
            emergency = data.get("emergency_count", 0)
            high_risk = data.get("high_risk_count", 0)
            
            # ─── Summary Metrics ───
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Patients", total)
            with col2:
                st.metric("🚨 Emergency", emergency)
            with col3:
                st.metric("🔴 High Risk", high_risk)
            with col4:
                st.metric("📋 Queue Size", total)
            
            st.markdown("---")
            
            if total == 0:
                st.info("No patient consultations yet. Patients will appear here after they interact with the chatbot.")
                return
            
            patients = data.get("patients", [])
            
            # ─── Priority Sections ───
            priority_groups = {
                "Emergency": {"emoji": "🚨", "color": "#FF0000"},
                "High Risk": {"emoji": "🔴", "color": "#FF4444"},
                "Moderate Risk": {"emoji": "🟡", "color": "#FFAA00"},
                "Low Risk": {"emoji": "🟢", "color": "#44FF44"},
            }
            
            for priority, config in priority_groups.items():
                group_patients = [p for p in patients if p.get("priority") == priority]
                if not group_patients:
                    continue
                
                st.markdown(f"### {config['emoji']} {priority} ({len(group_patients)})")
                
                for p in group_patients:
                    is_emergency = p.get("is_emergency", False)
                    border_color = config["color"]
                    
                    with st.expander(
                        f"{'🚨 ' if is_emergency else ''}"
                        f"Patient #{p['id']} — {p.get('risk_level', 'Unknown')} Risk — "
                        f"{p.get('created_at', 'N/A')}"
                    ):
                        # Clinical Summary
                        st.markdown("**📋 Symptoms:**")
                        st.markdown(f"> {p.get('symptoms', 'N/A')}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            risk = p.get("risk_level", "Unknown")
                            risk_emoji = "🔴" if risk in ["High", "Emergency"] else "🟡" if risk == "Moderate" else "🟢"
                            st.markdown(f"**Risk Level:** {risk_emoji} {risk}")
                        with col2:
                            st.markdown(f"**Health Score:** {p.get('health_score', 'N/A')}")
                        with col3:
                            st.markdown(f"**Priority:** {priority}")
                        
                        # Parse and show predicted diseases
                        diseases_str = p.get("predicted_diseases", "")
                        if diseases_str and diseases_str != "Emergency Pattern Detected":
                            try:
                                diseases = json.loads(diseases_str)
                                if isinstance(diseases, list):
                                    st.markdown("**🔬 Possible Conditions:**")
                                    for d in diseases:
                                        prob = d.get("probability", 0) * 100
                                        st.markdown(f"- **{d.get('name', 'Unknown')}**: {prob:.0f}%")
                                        if d.get("precautions"):
                                            st.markdown(f"  - Precautions: {', '.join(d['precautions'])}")
                            except (json.JSONDecodeError, TypeError):
                                st.markdown(f"**Assessment:** {diseases_str}")
                        elif diseases_str == "Emergency Pattern Detected":
                            st.error("⚠️ Emergency pattern was detected in this patient's symptoms.")
                        
                        if is_emergency:
                            st.error("🚨 **EMERGENCY FLAG** — This patient requires immediate attention!")
                
                st.markdown("---")
        else:
            st.error("Error loading patient data")
            
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.info("Make sure the backend server is running on port 8000")
        
        st.markdown("### Preview")
        st.info("Patient queue will appear here once the API is running and patients have been assessed.")
