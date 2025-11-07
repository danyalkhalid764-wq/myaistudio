from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import auth, tts, payments, video
from config import settings
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# ⚡ IMMEDIATE CORS FIX - CREATE APP WITH CORS BUILT-IN
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
    )
]

app = FastAPI(
    title="MyAIStudio API",
    description="Text-to-Speech API with ElevenLabs integration",
    version="1.0.0",
    middleware=middleware  # CORS built into the app
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(tts.router, prefix="/api", tags=["text-to-speech"])
app.include_router(payments.router, prefix="/api/payment", tags=["payments"])
app.include_router(video.router, prefix="/api/video", tags=["video"])

# Static files for generated videos
videos_dir = "/tmp/generated_videos"
os.makedirs(videos_dir, exist_ok=True)

# Mount static files
try:
    app.mount("/static/videos", StaticFiles(directory=videos_dir, check_dir=True), name="videos")
except ValueError:
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