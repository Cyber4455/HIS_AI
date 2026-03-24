import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="HIS AI — Health Intelligence System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "css", "style.css")
if os.path.exists(css_file):
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

theme = st.session_state.get("theme", "dark")

if theme == "dark":
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-color: #663399;
            --background-color: #FFFFFF;
            --secondary-background-color: #F5F5F5;
            --text-color: #000000;
            --card-background: #F5F5F5;
            --border-color: #E0E0E0;
        }
        
        .stApp {
            background: var(--background-color);
            font-family: 'Poppins', sans-serif;
            color: var(--text-color);
        }
        
        .feature-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F0F0F5 100%);
            border-radius: 16px;
            padding: 24px;
            margin: 12px 0;
            border: 1px solid rgba(102, 51, 153, 0.15);
            transition: transform 0.3s ease, border-color 0.3s ease;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary-color);
        }
        
        .gradient-text {
            background: linear-gradient(90deg, #663399, #F5A623);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .gradient-button {
            background: linear-gradient(90deg, #663399, #7B42B8);
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            color: #FFFFFF;
            font-weight: bold;
            cursor: pointer;
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(102, 51, 153, 0.1);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        .emergency-banner {
            background: linear-gradient(90deg, #FF0000, #FF4444);
            color: white;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 15px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #663399, #7B42B8);
            border: none;
            border-radius: 8px;
            color: #FFFFFF;
            font-weight: 600;
        }
        
        .stTextInput > div > div > input {
            background: #FFFFFF;
            color: #000000;
            border: 1px solid #E0E0E0;
        }
        
        .stTextArea > div > div > textarea {
            background: #FFFFFF;
            color: #000000;
            border: 1px solid #E0E0E0;
        }
        
        .stSelectbox > div > div > div {
            background: #FFFFFF;
            color: #000000;
        }
        
        /* Fix Streamlit default warning/error/info text for white background */
        .stAlert > div {
            color: #000000 !important;
        }
        .stAlert [data-testid="stMarkdownContainer"] p {
            color: #000000 !important;
        }
        
        /* Fix input placeholders */
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: #666666 !important;
            opacity: 1 !important;
        }
        
        /* Fix inactive tab labels */
        .stTabs [data-baseweb="tab"] {
            color: #333333 !important;
        }
        .stTabs [aria-selected="true"] {
            color: #FFFFFF !important;
        }
        
        /* Fix metric labels and values */
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {
            color: #000000 !important;
        }
        
        /* Fix sidebar text */
        [data-testid="stSidebar"] {
            color: #000000;
        }
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown li,
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: #000000 !important;
        }
        
        /* Fix expander headers */
        .streamlit-expanderHeader {
            color: #000000 !important;
        }
        
        /* Fix all markdown text in main area */
        .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #000000;
        }
        
        /* Fix chat messages */
        [data-testid="stChatMessage"] {
            color: #000000 !important;
        }
        [data-testid="stChatMessage"] p {
            color: #000000 !important;
        }
        
        /* Fix number input */
        .stNumberInput > div > div > input {
            color: #000000 !important;
        }
        
        /* Fix radio and checkbox labels */
        .stRadio label, .stCheckbox label {
            color: #000000 !important;
        }
        
        /* Fix selectbox text */
        [data-testid="stSelectbox"] label,
        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stNumberInput"] label {
            color: #000000 !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-color: #663399;
            --background-color: #F5F7FA;
            --secondary-background-color: #FFFFFF;
            --text-color: #1A1A2E;
            --card-background: #FFFFFF;
            --border-color: #E0E0E0;
        }
        
        .stApp {
            background: var(--background-color);
            font-family: 'Poppins', sans-serif;
            color: var(--text-color);
        }
        
        .feature-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F0F4F8 100%);
            border-radius: 16px;
            padding: 24px;
            margin: 12px 0;
            border: 1px solid rgba(102, 51, 153, 0.2);
            transition: transform 0.3s ease, border-color 0.3s ease;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary-color);
        }
        
        .gradient-text {
            background: linear-gradient(90deg, #663399, #F5A623);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .gradient-button {
            background: linear-gradient(90deg, #663399, #7B42B8);
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(0, 0, 0, 0.05);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        .emergency-banner {
            background: linear-gradient(90deg, #CC0000, #FF4444);
            color: white;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 15px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #663399, #7B42B8);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
        }
        
        .stTextInput > div > div > input {
            background: #FFFFFF;
            color: #000000;
            border: 1px solid #E0E0E0;
        }
        
        .stTextArea > div > div > textarea {
            background: #FFFFFF;
            color: #000000;
            border: 1px solid #E0E0E0;
        }
        
        .stSelectbox > div > div > div {
            background: #FFFFFF;
            color: #000000;
        }
        
        /* Fix Streamlit default warning/error/info text for white background */
        .stAlert > div {
            color: #000000 !important;
        }
        .stAlert [data-testid="stMarkdownContainer"] p {
            color: #000000 !important;
        }
        
        /* Fix input placeholders */
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: #666666 !important;
            opacity: 1 !important;
        }
        
        /* Fix inactive tab labels */
        .stTabs [data-baseweb="tab"] {
            color: #333333 !important;
        }
        .stTabs [aria-selected="true"] {
            color: #FFFFFF !important;
        }
        
        /* Fix metric labels and values */
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {
            color: #000000 !important;
        }
        
        /* Fix sidebar text */
        [data-testid="stSidebar"] {
            color: #000000;
        }
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown li,
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: #000000 !important;
        }
        
        /* Fix expander headers */
        .streamlit-expanderHeader {
            color: #000000 !important;
        }
        
        /* Fix all markdown text in main area */
        .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #000000;
        }
        
        /* Fix chat messages */
        [data-testid="stChatMessage"] {
            color: #000000 !important;
        }
        [data-testid="stChatMessage"] p {
            color: #000000 !important;
        }
        
        /* Fix number input */
        .stNumberInput > div > div > input {
            color: #000000 !important;
        }
        
        /* Fix radio and checkbox labels */
        .stRadio label, .stCheckbox label {
            color: #000000 !important;
        }
        
        /* Fix selectbox text */
        [data-testid="stSelectbox"] label,
        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stNumberInput"] label {
            color: #000000 !important;
        }
    </style>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'patient'
if 'is_guest' not in st.session_state:
    st.session_state.is_guest = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def main():
    if not st.session_state.logged_in:
        from views.login import show_login
        show_login()
    else:
        page = st.session_state.current_page
        
        if page == 'Landing':
            st.session_state.current_page = 'Dashboard'
            from views.dashboard import show_dashboard
            show_dashboard()
        else:
            from components.sidebar import show_sidebar
            show_sidebar()
            
            if page == 'Chat':
                from views.chatbot import show_chatbot
                show_chatbot()
            elif page == 'Disease Prediction':
                from views.disease_predict import show_disease_predict
                show_disease_predict()
            elif page == 'Health Score':
                from views.health_score import show_health_score
                show_health_score()
            elif page == 'Dashboard':
                from views.dashboard import show_dashboard
                show_dashboard()
            elif page == 'History':
                from views.history import show_history
                show_history()
            elif page == 'Doctor Dashboard':
                from views.doctor_dashboard import show_doctor_dashboard
                show_doctor_dashboard()
            elif page == 'Admin Analytics':
                from views.admin_analytics import show_admin_analytics
                show_admin_analytics()
            elif page == 'Settings':
                from views.settings import show_settings
                show_settings()

main()
