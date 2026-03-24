import os
from dotenv import load_dotenv

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_project_root, ".env"))

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
