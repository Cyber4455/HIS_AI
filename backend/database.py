import sqlite3
from datetime import datetime
from contextlib import contextmanager
from config import DATABASE_URL

db_path = DATABASE_URL.replace("sqlite:///", "")

@contextmanager
def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'patient',
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symptoms TEXT NOT NULL,
                predicted_diseases TEXT,
                health_score INTEGER,
                risk_level TEXT,
                is_emergency INTEGER DEFAULT 0,
                user_role TEXT DEFAULT 'patient',
                priority TEXT DEFAULT 'Low Risk',
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_type TEXT NOT NULL,
                input_data TEXT NOT NULL,
                risk_percentage REAL,
                risk_level TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Add new columns to existing tables if they don't exist
        try:
            cursor.execute("ALTER TABLE consultations ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute("ALTER TABLE predictions ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute("ALTER TABLE consultations ADD COLUMN user_role TEXT DEFAULT 'patient'")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active'")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE consultations ADD COLUMN priority TEXT DEFAULT 'Low Risk'")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        conn.commit()

def save_consultation(symptoms: str, predicted_diseases: str, 
                      health_score: int, risk_level: str, is_emergency: int = 0,
                      user_role: str = "patient", priority: str = "Low Risk"):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO consultations 
               (symptoms, predicted_diseases, health_score, risk_level, is_emergency, user_role, priority) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (symptoms, predicted_diseases, health_score, risk_level, is_emergency, user_role, priority)
        )
        conn.commit()
        return cursor.lastrowid

def get_consultations():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM consultations ORDER BY created_at DESC"
        )
        return [dict(row) for row in cursor.fetchall()]

def save_prediction(disease_type: str, input_data: str, 
                   risk_percentage: float, risk_level: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO predictions 
               (disease_type, input_data, risk_percentage, risk_level) 
               VALUES (?, ?, ?, ?)""",
            (disease_type, input_data, risk_percentage, risk_level)
        )
        conn.commit()
        return cursor.lastrowid

def get_analytics_data():
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM consultations")
        total_consultations = cursor.fetchone()["total"]
        
        cursor.execute("SELECT COUNT(*) as high_risk FROM consultations WHERE risk_level = 'High'")
        high_risk_count = cursor.fetchone()["high_risk"]
        
        cursor.execute("SELECT AVG(health_score) as avg_score FROM consultations WHERE health_score IS NOT NULL")
        avg_health_score = cursor.fetchone()["avg_score"] or 0
        
        cursor.execute("SELECT symptoms FROM consultations")
        all_symptoms = [row["symptoms"] for row in cursor.fetchall()]
        
        cursor.execute("SELECT predicted_diseases FROM consultations WHERE predicted_diseases IS NOT NULL")
        all_diseases = [row["predicted_diseases"] for row in cursor.fetchall()]
        
        cursor.execute("SELECT risk_level, COUNT(*) as count FROM consultations GROUP BY risk_level")
        risk_distribution = {row["risk_level"]: row["count"] for row in cursor.fetchall()}
        
        return {
            "total_consultations": total_consultations,
            "high_risk_count": high_risk_count,
            "avg_health_score": round(avg_health_score, 1),
            "symptoms_list": all_symptoms,
            "diseases_list": all_diseases,
            "risk_distribution": risk_distribution
        }

def get_patients_by_priority():
    """Get all consultations for doctor priority view."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM consultations 
            ORDER BY 
                CASE priority 
                    WHEN 'Emergency' THEN 0 
                    WHEN 'High Risk' THEN 1 
                    WHEN 'Moderate Risk' THEN 2 
                    WHEN 'Low Risk' THEN 3 
                    ELSE 4 
                END,
                created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_admin_summary():
    """Get system-level analytics for admin view."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM consultations")
        total_consultations = cursor.fetchone()["total"]
        
        cursor.execute("SELECT COUNT(*) as emergency FROM consultations WHERE is_emergency = 1")
        emergency_count = cursor.fetchone()["emergency"]
        
        cursor.execute("SELECT COUNT(*) as high_risk FROM consultations WHERE risk_level = 'High' OR risk_level = 'Emergency'")
        high_risk_count = cursor.fetchone()["high_risk"]
        
        cursor.execute("SELECT AVG(health_score) as avg_score FROM consultations WHERE health_score IS NOT NULL AND health_score > 0")
        avg_health_score = cursor.fetchone()["avg_score"] or 0
        
        cursor.execute("SELECT risk_level, COUNT(*) as count FROM consultations GROUP BY risk_level")
        risk_distribution = {row["risk_level"]: row["count"] for row in cursor.fetchall()}
        
        cursor.execute("SELECT priority, COUNT(*) as count FROM consultations GROUP BY priority")
        priority_distribution = {row["priority"]: row["count"] for row in cursor.fetchall()}
        
        cursor.execute("SELECT COUNT(*) as total FROM predictions")
        total_predictions = cursor.fetchone()["total"]
        
        cursor.execute("SELECT disease_type, COUNT(*) as count FROM predictions GROUP BY disease_type")
        prediction_types = {row["disease_type"]: row["count"] for row in cursor.fetchall()}
        
        cursor.execute("SELECT user_role, COUNT(*) as count FROM consultations GROUP BY user_role")
        role_distribution = {}
        for row in cursor.fetchall():
            role = row["user_role"] or "patient"
            role_distribution[role] = row["count"]
        
        # Recent consultations (last 10)
        cursor.execute("""
            SELECT id, symptoms, risk_level, priority, is_emergency, created_at 
            FROM consultations ORDER BY created_at DESC LIMIT 10
        """)
        recent = [dict(row) for row in cursor.fetchall()]
        
        return {
            "total_consultations": total_consultations,
            "emergency_count": emergency_count,
            "high_risk_count": high_risk_count,
            "avg_health_score": round(avg_health_score, 1),
            "total_predictions": total_predictions,
            "risk_distribution": risk_distribution,
            "priority_distribution": priority_distribution,
            "prediction_types": prediction_types,
            "role_distribution": role_distribution,
            "recent_consultations": recent
        }

def get_all_users():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_user_by_username(username: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_user_role(user_id: int, new_role: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
        conn.commit()

def update_user_status(user_id: int, status: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
        conn.commit()

def update_user_details(user_id: int, username: str = None, email: str = None):
    with get_db() as conn:
        cursor = conn.cursor()
        if username:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
        if email:
            cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
        conn.commit()

def reset_user_password(user_id: int, password_hash: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
        conn.commit()
