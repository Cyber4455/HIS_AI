import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

def show_login():
    import base64
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static", "images", "aviu_logo.png")
    logo_html = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_b64 = base64.b64encode(img_file.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 160px; margin-bottom: 15px;" />'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 20px;">
        {logo_html}
        <h1 style="font-size: 3em; margin-bottom: 10px;">
            <span class="gradient-text">HIS AI</span>
        </h1>
        <h2 style="font-size: 1.4em; color: #663399; margin-bottom: 10px; font-weight: 400;">
            Health Intelligence System
        </h2>
        <p style="font-size: 1.1em; color: #000000;">
            Hybrid AI-Powered Clinical Decision Support Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Register", "🚀 Quick Access (Guest)"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/auth/login",
                            json={"username": username, "password": password}
                        )
                        
                        if response.status_code == 200:
                            user = response.json()
                            st.session_state.logged_in = True
                            st.session_state.user_info = user
                            st.session_state.user_role = user["role"]
                            st.session_state.is_guest = False
                            st.session_state.current_page = "Dashboard"
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        st.info("Make sure the backend server is running")
    
    with tab2:
        st.markdown("### Create New Account")
        
        with st.form("register_form"):
            new_username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
            email = st.text_input("Email", placeholder="your@email.com", key="reg_email")
            new_password = st.text_input("Password", type="password", placeholder="Choose a password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_confirm")
            
            submit_reg = st.form_submit_button("Register", use_container_width=True)
            
            if submit_reg:
                if not new_username or not email or not new_password:
                    st.error("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 4:
                    st.error("Password must be at least 4 characters")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/auth/register",
                            json={
                                "username": new_username,
                                "email": email,
                                "password": new_password
                            }
                        )
                        
                        if response.status_code == 200:
                            st.success("Account created successfully! Please login.")
                        else:
                            error_detail = response.json().get("detail", "Registration failed")
                            st.error(error_detail)
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        st.info("Make sure the backend server is running")
    
    with tab3:
        st.markdown("### Quick Access (Guest)")
        st.markdown("""
        <div style="background: rgba(102, 51, 153, 0.05); padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid rgba(102, 51, 153, 0.1);">
            <p style="color: #000000;">
                Continue as a guest to explore the platform's features. 
                Note: Your consultations and predictions will not be saved to your account.
            </p>
            <ul style="color: #333; font-size: 0.9em;">
                <li>✅ Access all AI chat features</li>
                <li>✅ Use disease prediction tools</li>
                <li>✅ Calculate health scores</li>
                <li>❌ History won't be saved</li>
                <li>❌ Cannot access doctor dashboard</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue as Guest", use_container_width=True, key="guest_login"):
            st.session_state.logged_in = True
            st.session_state.user_info = {"username": "Guest", "role": "patient"}
            st.session_state.user_role = "patient"
            st.session_state.is_guest = True
            st.session_state.current_page = "Dashboard"
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #CC0000; font-size: 0.85em; padding: 10px;">
        ⚠️ This platform is for preliminary assessment only and does NOT replace professional medical care.
    </div>
    """, unsafe_allow_html=True)
