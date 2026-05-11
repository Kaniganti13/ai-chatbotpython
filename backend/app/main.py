# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = FastAPI(title="AI Chatbot", version="1.0")

# Allow CORS for local development (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder so frontend files are served
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API router
app.include_router(api_router)

# Root route can redirect or serve index; api.py already serves index at "/"
@app.get("/health")
async def health():
    return {"status": "ok"}
