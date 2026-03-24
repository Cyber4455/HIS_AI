import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

ADMIN_SECRET = "his-admin-2024"

def show_admin_analytics():
    st.title("⚙️ Admin Analytics — System Overview")
    st.markdown("*System-level summaries, risk distribution, and platform monitoring*")
    
    tab1, tab2 = st.tabs(["📊 System Analytics", "👥 User Management"])
    
    with tab1:
        try:
            response = requests.get(f"{API_BASE_URL}/admin/summary")
            
            if response.status_code == 200:
                data = response.json()
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("📊 Total Consultations", data.get("total_consultations", 0))
                with col2:
                    st.metric("🚨 Emergencies", data.get("emergency_count", 0))
                with col3:
                    st.metric("🔴 High Risk", data.get("high_risk_count", 0))
                with col4:
                    st.metric("💯 Avg Health Score", data.get("avg_health_score", 0))
                with col5:
                    st.metric("🔬 Predictions Made", data.get("total_predictions", 0))
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Risk Distribution")
                    risk_dist = data.get("risk_distribution", {})
                    if risk_dist:
                        for level, count in risk_dist.items():
                            emoji = "🚨" if level == "Emergency" else "🔴" if level == "High" else "🟡" if level in ["Medium", "Moderate"] else "🟢"
                            total = sum(risk_dist.values())
                            pct = (count / total * 100) if total > 0 else 0
                            bar = "█" * int(pct / 5)
                            st.markdown(f"{emoji} **{level}**: {count} ({pct:.1f}%) {bar}")
                    else:
                        st.info("No risk data available yet")
                
                with col2:
                    st.markdown("### 🏥 Priority Distribution")
                    priority_dist = data.get("priority_distribution", {})
                    if priority_dist:
                        for priority, count in priority_dist.items():
                            emoji = "🚨" if priority == "Emergency" else "🔴" if priority == "High Risk" else "🟡" if priority == "Moderate Risk" else "🟢"
                            total = sum(priority_dist.values())
                            pct = (count / total * 100) if total > 0 else 0
                            bar = "█" * int(pct / 5)
                            st.markdown(f"{emoji} **{priority}**: {count} ({pct:.1f}%) {bar}")
                    else:
                        st.info("No priority data available yet")
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🔬 Disease Prediction Types")
                    pred_types = data.get("prediction_types", {})
                    if pred_types:
                        for disease_type, count in pred_types.items():
                            st.markdown(f"- **{disease_type}**: {count} predictions")
                    else:
                        st.info("No predictions made yet")
                
                with col2:
                    st.markdown("### 👥 User Role Distribution")
                    role_dist = data.get("role_distribution", {})
                    if role_dist:
                        role_emojis = {"patient": "🩺", "doctor": "👨‍⚕️", "admin": "⚙️"}
                        for role, count in role_dist.items():
                            emoji = role_emojis.get(role, "👤")
                            st.markdown(f"- {emoji} **{role.capitalize()}**: {count} consultations")
                    else:
                        st.info("No role data available yet")
                
                st.markdown("---")
                
                st.markdown("### 📋 Recent Consultations")
                recent = data.get("recent_consultations", [])
                if recent:
                    for c in recent:
                        is_emerg = c.get("is_emergency", 0)
                        priority = c.get("priority", "Low Risk")
                        risk = c.get("risk_level", "Unknown")
                        
                        prefix = "🚨" if is_emerg else ("🔴" if risk == "High" else "🟡" if risk in ["Medium", "Moderate"] else "🟢")
                        
                        st.markdown(
                            f"{prefix} **#{c['id']}** — "
                            f"Risk: {risk} | Priority: {priority} | "
                            f"Symptoms: _{c.get('symptoms', 'N/A')[:80]}{'...' if len(c.get('symptoms', '')) > 80 else ''}_ — "
                            f"{c.get('created_at', 'N/A')}"
                        )
                else:
                    st.info("No consultations yet")
            
            else:
                st.error("Error loading admin data")
                
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            st.info("Make sure the backend server is running on port 8000")
            
            st.markdown("### Preview")
            st.info("System analytics will appear here once the API is running.")
    
    with tab2:
        st.markdown("### 👥 User Management")
        
        try:
            headers = {"admin-secret": ADMIN_SECRET}
            users_response = requests.get(f"{API_BASE_URL}/auth/users", headers=headers)
            
            if users_response.status_code == 200:
                users = users_response.json()
                
                if users:
                    st.markdown(f"**Total Users:** {len(users)}")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    active_count = sum(1 for u in users if u.get("status", "active") == "active")
                    inactive_count = len(users) - active_count
                    with col1:
                        st.metric("Total", len(users))
                    with col2:
                        st.metric("Active", active_count)
                    with col3:
                        st.metric("Inactive", inactive_count)
                    with col4:
                        st.metric("Doctors", sum(1 for u in users if u.get("role") == "doctor"))
                    
                    st.markdown("---")
                    
                    for user in users:
                        user_status = user.get("status", "active")
                        status_color = "🟢" if user_status == "active" else "🔴"
                        
                        with st.expander(f"{status_color} {user['username']} — {user['role'].capitalize()} ({user_status})"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"**Email:** {user['email']}")
                                st.markdown(f"**Role:** {user['role']}")
                                st.markdown(f"**Status:** {status_color} {user_status.upper()}")
                                st.markdown(f"**Created:** {user['created_at']}")
                            
                            with col2:
                                st.markdown("**Actions:**")
                                
                                new_role = st.selectbox(
                                    "Change Role", 
                                    ["patient", "doctor"], 
                                    index=0 if user['role'] == "patient" else 1,
                                    key=f"role_{user['id']}"
                                )
                                
                                if st.button(f"Update Role", key=f"update_role_{user['id']}"):
                                    update_response = requests.put(
                                        f"{API_BASE_URL}/auth/users/{user['id']}/role",
                                        headers=headers,
                                        params={"new_role": new_role}
                                    )
                                    if update_response.status_code == 200:
                                        st.success(f"Role updated to {new_role}")
                                        st.rerun()
                                    else:
                                        st.error("Failed to update role")
                                
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if user_status == "active":
                                        if st.button("Deactivate", key=f"deact_{user['id']}"):
                                            status_response = requests.put(
                                                f"{API_BASE_URL}/auth/users/{user['id']}/status",
                                                headers=headers,
                                                params={"status": "inactive"}
                                            )
                                            if status_response.status_code == 200:
                                                st.success("User deactivated")
                                                st.rerun()
                                            else:
                                                st.error("Failed to update status")
                                    else:
                                        if st.button("Activate", key=f"act_{user['id']}"):
                                            status_response = requests.put(
                                                f"{API_BASE_URL}/auth/users/{user['id']}/status",
                                                headers=headers,
                                                params={"status": "active"}
                                            )
                                            if status_response.status_code == 200:
                                                st.success("User activated")
                                                st.rerun()
                                            else:
                                                st.error("Failed to update status")
                                
                                with col_b:
                                    new_pwd = st.text_input("New Password", type="password", key=f"pwd_{user['id']}")
                                    if st.button("Reset Password", key=f"reset_{user['id']}"):
                                        if new_pwd:
                                            reset_response = requests.put(
                                                f"{API_BASE_URL}/auth/users/{user['id']}/reset-password",
                                                headers=headers,
                                                json={"new_password": new_pwd}
                                            )
                                            if reset_response.status_code == 200:
                                                st.success("Password reset successfully")
                                            else:
                                                st.error("Failed to reset password")
                                        else:
                                            st.error("Enter a new password")
                else:
                    st.info("No registered users yet. Users will appear after they register.")
            else:
                st.error("Error loading users")
                
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            st.info("Make sure the backend server is running")
        
        st.markdown("---")
        st.markdown("### ➕ Create Doctor Account")
        
        with st.form("create_doctor_form"):
            st.info("Doctor accounts must be created directly in the database. Use the registration endpoint with role modification.")
            
            doc_username = st.text_input("Username")
            doc_email = st.text_input("Email")
            doc_password = st.text_input("Password", type="password")
            
            submit_doc = st.form_submit_button("Create Account")
            
            if submit_doc:
                if not doc_username or not doc_email or not doc_password:
                    st.error("Please fill in all fields")
                else:
                    try:
                        reg_response = requests.post(
                            f"{API_BASE_URL}/auth/register",
                            json={
                                "username": doc_username,
                                "email": doc_email,
                                "password": doc_password
                            }
                        )
                        
                        if reg_response.status_code == 200:
                            new_user = reg_response.json()
                            st.success(f"Account created! Now update their role to doctor.")
                            
                            update_response = requests.put(
                                f"{API_BASE_URL}/auth/users/{new_user['id']}/role",
                                headers=headers,
                                params={"new_role": "doctor"}
                            )
                            if update_response.status_code == 200:
                                st.success("Doctor account created successfully!")
                            st.rerun()
                        else:
                            error_detail = reg_response.json().get("detail", "Registration failed")
                            st.error(error_detail)
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
