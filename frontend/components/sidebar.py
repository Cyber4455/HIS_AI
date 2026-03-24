import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL

def show_sidebar():
    role = st.session_state.get("user_role", "patient")
    is_guest = st.session_state.get("is_guest", False)
    
    with st.sidebar:
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static", "images", "aviu_logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=150)
        st.markdown("### 🏥 HIS AI")
        
        if st.session_state.get("logged_in"):
            user_info = st.session_state.get("user_info", {})
            username = user_info.get("username", "User")
            role_label = {"patient": "🩺 Patient", "doctor": "👨‍⚕️ Doctor", "admin": "⚙️ Admin"}.get(role, "🩺 Patient")
            st.markdown(f"**User:** {username}")
            st.markdown(f"**Role:** {role_label}")
            if is_guest:
                st.markdown("<small style='color: #663399;'>👤 Guest Session</small>", unsafe_allow_html=True)
        st.markdown("---")
        
        if role == "patient" and not is_guest:
            pages = [
                ("Dashboard", "📈", "Dashboard"),
                ("Chat", "💬", "Chat"),
                ("Disease Prediction", "❤️", "Disease Prediction"),
                ("Health Score", "📊", "Health Score"),
                ("History", "📋", "History"),
                ("Settings", "⚙️", "Settings"),
            ]
        elif role == "patient" and is_guest:
            pages = [
                ("Dashboard", "📈", "Dashboard"),
                ("Chat", "💬", "Chat"),
                ("Disease Prediction", "❤️", "Disease Prediction"),
                ("Health Score", "📊", "Health Score"),
                ("Settings", "⚙️", "Settings"),
            ]
        elif role == "doctor":
            pages = [
                ("Doctor Dashboard", "🏥", "Doctor Dashboard"),
                ("Dashboard", "📈", "Dashboard"),
                ("Chat", "💬", "Chat"),
                ("Disease Prediction", "❤️", "Disease Prediction"),
                ("History", "📋", "History"),
                ("Settings", "⚙️", "Settings"),
            ]
        elif role == "admin":
            pages = [
                ("Admin Analytics", "⚙️", "Admin Analytics"),
                ("Dashboard", "📈", "Dashboard"),
                ("History", "📋", "History"),
                ("Settings", "⚙️", "Settings"),
            ]
        else:
            pages = [
                ("Dashboard", "📈", "Dashboard"),
                ("Chat", "💬", "Chat"),
                ("Settings", "⚙️", "Settings"),
            ]
        
        current_page = st.session_state.get("current_page", "Dashboard")
        
        for page_name, icon, page_key in pages:
            is_active = current_page == page_key
            if st.button(
                f"{icon} {page_name}", 
                use_container_width=True, 
                key=f"nav_{page_key}",
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <div style="font-size: 0.8em; color: #333; margin-top: 20px;">
            <p><strong>🚨 Uganda Emergency:</strong></p>
            <p>• Police: 999 / 112</p>
            <p>• Ambulance: 911</p>
            <p>• Fire: 112</p>
            <p>• Uganda Red Cross: 0800-100-225</p>
        </div>
        """, unsafe_allow_html=True)
