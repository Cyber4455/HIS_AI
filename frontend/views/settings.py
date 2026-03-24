import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

def show_settings():
    user_info = st.session_state.get("user_info", {})
    user_role = st.session_state.get("user_role", "patient")
    is_guest = st.session_state.get("is_guest", False)
    
    st.title("⚙️ Settings")
    
    theme = st.session_state.get("theme", "dark")
    
    with st.expander("🎨 Theme Settings", expanded=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            new_theme = st.radio(
                "Select Theme",
                ["dark", "light"],
                index=0 if theme == "dark" else 1,
                horizontal=True
            )
        with col2:
            st.markdown(f"**Current:** {'🌙 Dark' if theme == 'dark' else '☀️ Light'}")
        
        if new_theme != theme:
            st.session_state.theme = new_theme
            st.rerun()
    
    st.markdown("---")
    
    with st.expander("👤 Account Settings", expanded=True):
        if is_guest:
            st.info("You are logged in as a guest. Create an account to save your data.")
            st.markdown("**Username:** Guest")
            st.markdown("**Role:** Patient (Guest)")
        else:
            st.markdown(f"**Username:** {user_info.get('username', 'N/A')}")
            st.markdown(f"**Email:** {user_info.get('email', 'N/A')}")
            st.markdown(f"**Role:** {user_role.capitalize()}")
            role_emoji = {"patient": "🩺", "doctor": "👨‍⚕️", "admin": "⚙️"}
            st.markdown(f"**Account Type:** {role_emoji.get(user_role, '❓')} {user_role.capitalize()}")
    
    st.markdown("---")
    
    if not is_guest and user_role == "doctor":
        with st.expander("🔑 Change Password", expanded=False):
            with st.form("change_password_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                submit_pwd = st.form_submit_button("Change Password", use_container_width=True)
                
                if submit_pwd:
                    if not current_password or not new_password or not confirm_password:
                        st.error("Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                    elif len(new_password) < 4:
                        st.error("Password must be at least 4 characters")
                    else:
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/auth/change-password",
                                json={
                                    "current_password": current_password,
                                    "new_password": new_password
                                },
                                params={"username": user_info.get("username")}
                            )
                            
                            if response.status_code == 200:
                                st.success("Password changed successfully!")
                            else:
                                error_detail = response.json().get("detail", "Failed to change password")
                                st.error(error_detail)
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")
    
    st.markdown("---")
    
    if user_role != "admin" and not is_guest:
        with st.expander("🔐 Admin Access", expanded=False):
            st.markdown("""
            <div style="background: rgba(102, 51, 153, 0.05); padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid rgba(102, 51, 153, 0.1);">
                <p style="color: #333333; font-size: 0.9em;">
                    Enter the admin secret key to access the admin panel.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            admin_key = st.text_input("Admin Secret Key", type="password", key="admin_key_settings")
            if st.button("Access Admin Panel", use_container_width=True):
                if admin_key == "his-admin-2024":
                    st.session_state.user_role = "admin"
                    st.session_state.current_page = "Admin Analytics"
                    st.success("Admin access granted!")
                    st.rerun()
                else:
                    st.error("Invalid admin key")
    
    st.markdown("---")
    
    if not is_guest:
        with st.expander("🚪 Logout", expanded=False):
            st.markdown("Are you sure you want to logout?")
            if st.button("Logout", use_container_width=True, type="primary"):
                st.session_state.logged_in = False
                st.session_state.user_info = {}
                st.session_state.user_role = "patient"
                st.session_state.is_guest = False
                st.session_state.current_page = "Dashboard"
                st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em; padding: 20px;">
        <p>Health Intelligence System v4.0</p>
        <p>Hybrid AI-Powered Clinical Decision Support Platform</p>
    </div>
    """, unsafe_allow_html=True)
