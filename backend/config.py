import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent of backend/)
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./health_intelligence.db")
ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "his-admin-2024")
