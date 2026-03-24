from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import chat, predict, health_score, analytics, health_tips
from routes import doctor, admin, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Health Intelligence System API",
    description="HIS AI — Hybrid AI-Powered Clinical Decision Support Platform",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(predict.router)
app.include_router(health_score.router)
app.include_router(analytics.router)
app.include_router(health_tips.router)
app.include_router(doctor.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {
        "message": "Health Intelligence System API",
        "version": "2.0.0",
        "status": "running",
        "system": "HIS AI — Clinical Decision Support Platform"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
