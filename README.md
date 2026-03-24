# 🏥 HIS AI — Health Intelligence System

**A smart health assistant powered by AI.**

HIS AI helps you check your health by chatting with an AI doctor, predicting disease risks, and calculating your health score. It's built for patients, doctors, and admins — each with their own dashboard and tools.

---

## ✨ Features

- **💬 AI Health Chatbot** — Describe your symptoms, and the AI gives you possible conditions and advice
- **❤️ Disease Prediction** — Check your risk for Diabetes, Heart Disease, Malaria, Typhoid, and Hypertension
- **📊 Health Score** — Get a health score (0–100) based on your vitals and lifestyle
- **🧠 AI Health Tips** — Personalized health tips shown on the dashboard and after results
- **👨‍⚕️ Doctor Dashboard** — Doctors see patients ranked by priority (Emergency → High → Moderate → Low)
- **⚙️ Admin Panel** — Admins manage users, view system analytics, and create doctor accounts
- **🔐 Login System** — Register as a patient, login, or use guest mode (no account needed)
- **🌙 Dark & Light Themes** — Switch between dark and light mode in Settings
- **🚨 Emergency Detection** — The AI detects emergencies and shows urgent warnings
- **📋 Consultation History** — Your past chats and diagnoses are saved (for logged-in users)

---

## 📁 Folder Structure

```
Health Intelligence System - V4/
│
├── backend/                  ← The server (handles data and AI logic)
│   ├── main.py               ← Starts the backend server
│   ├── config.py             ← Loads settings (API keys, database)
│   ├── database.py           ← Manages the database (SQLite)
│   ├── routes/               ← API endpoints (chat, predict, auth, etc.)
│   ├── services/             ← AI services (Gemini AI, emergency detection)
│   └── schemas/              ← Data models (what data looks like)
│
├── frontend/                 ← The user interface (what you see in the browser)
│   ├── app.py                ← Main app file (starts the frontend)
│   ├── config.py             ← Frontend settings
│   ├── views/                ← Pages (dashboard, chatbot, login, etc.)
│   └── components/           ← Reusable parts (sidebar)
│
├── static/                   ← CSS styles and assets
├── utils/                    ← Helper tools (PDF reports)
├── .env                      ← Secret keys and settings (don't share this!)
└── requirements.txt          ← List of packages needed to run the project
```

---

## 🛠️ How to Install

### What You Need First

- **Python 3.10 or newer** — [Download Python](https://www.python.org/downloads/)
- **A Gemini API Key** — [Get one free from Google](https://aistudio.google.com/apikey)

### Step-by-Step Setup

**1. Open a terminal** (Command Prompt or PowerShell) and go to the project folder:

```bash
cd "d:\projects\Health Intelligence System - V4"
```

**2. Install the required packages:**

```bash
pip install -r requirements.txt
```

**3. Set up your secret keys:**

Open the `.env` file and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
JWT_SECRET=your_jwt_secret_key_here
DATABASE_URL=sqlite:///./health_intelligence.db
ADMIN_SECRET_KEY=his-admin-2024
```

---

## 🚀 How to Run

You need **two terminals** — one for the backend server, one for the frontend.

### Terminal 1 — Start the Backend

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see: `Application startup complete`

### Terminal 2 — Start the Frontend

```bash
streamlit run frontend/app.py
```

You should see: `You can now view your Streamlit app in your browser`

**Open your browser** and go to: **http://localhost:8501**

---

## 📖 How to Use

### As a Patient

1. **Register** — Click "Register" tab, create a username and password
2. **Login** — Use your username and password to log in
3. **Or use Guest Mode** — Click "Quick Access (Guest)" to try without an account
4. **Chat with AI** — Go to "Chat" and describe your symptoms
5. **Predict Disease Risk** — Go to "Disease Prediction" and fill in your health data
6. **Check Health Score** — Go to "Health Score" and enter your vitals

### As a Doctor

1. Doctors are created by the admin (they don't register themselves)
2. Login with your doctor account
3. See the **Doctor Dashboard** with patients ranked by priority
4. Use the chatbot in **Clinical Mode** for structured analysis

### As an Admin

1. Go to **Settings → Admin Access**
2. Enter the admin secret key: `his-admin-2024`
3. View system analytics, manage users, and create doctor accounts

---

## 🔧 Technologies Used

| Technology | What It Does |
|---|---|
| **Python** | The programming language used for everything |
| **Streamlit** | Creates the web interface (what you see in the browser) |
| **FastAPI** | Runs the backend server (handles requests and data) |
| **Google Gemini AI** | Powers the AI chatbot and health tips |
| **SQLite** | Stores user accounts, consultations, and predictions |
| **Plotly** | Creates charts and graphs on the dashboard |
| **bcrypt** | Keeps passwords safe (encrypts them) |

---

## 📝 Important Notes

- ⚠️ **This is NOT a real medical tool.** It's for learning and preliminary assessment only. Always see a real doctor for health concerns.
- 🔑 The **admin secret key** is `his-admin-2024` — change this in `.env` for production use.
- 🗄️ The database file (`health_intelligence.db`) is created automatically when you first start the backend.
- 🌐 The backend runs on **port 8000** and the frontend on **port 8501** by default.
- 👤 **Guest users** can use all features, but their data is not saved.
- 🇺🇬 Emergency contact numbers are set for **Uganda** (999, 112, 911).

---

## 🆘 Troubleshooting

| Problem | Solution |
|---|---|
| "Connection error" on the frontend | Make sure the backend is running on port 8000 |
| "Port already in use" | Close other programs using that port, or use a different port: `--port 8502` |
| "Module not found" error | Run `pip install -r requirements.txt` again |
| Pages not loading | Refresh the browser or restart both servers |

---

<div align="center">

**Built with ❤️ for better health awareness**

*HIS AI — Hybrid AI-Powered Clinical Decision Support Platform*

</div>
