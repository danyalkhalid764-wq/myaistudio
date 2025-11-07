from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import auth, tts, payments, video
from config import settings
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MyAIStudio API",
    description="Text-to-Speech API with ElevenLabs integration",
    version="1.0.0"
)

# Configure CORS - TEMPORARY FIX: ALLOW ALL ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← CHANGED THIS LINE
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(tts.router, prefix="/api", tags=["text-to-speech"])
app.include_router(payments.router, prefix="/api/payment", tags=["payments"])
app.include_router(video.router, prefix="/api/video", tags=["video"])

# Static files for generated videos - FIXED for Railway
videos_dir = "/tmp/generated_videos"
os.makedirs(videos_dir, exist_ok=True)

# Mount static files - allow access to video files
try:
    app.mount("/static/videos", StaticFiles(directory=videos_dir, check_dir=True), name="videos")
except ValueError:
    # If already mounted, skip
    pass

@app.get("/")
async def root():
    return {"message": "MyAIStudio API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)