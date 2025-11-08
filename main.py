import sys
import os
import shutil

# Force output immediately
sys.stdout.flush()
sys.stderr.flush()

# Configure ffmpeg PATH before any imports that might use it (pydub, moviepy)
# This ensures ffmpeg is available when pydub/moviepy check for it at import time
try:
    import imageio_ffmpeg
    ffmpeg_binary = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_binary)
    if ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    print(f"✅ Configured ffmpeg from imageio-ffmpeg: {ffmpeg_binary}", flush=True)
except Exception:
    # Fallback to system ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        if ffmpeg_dir not in os.environ.get("PATH", ""):
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        print(f"✅ Configured system ffmpeg: {ffmpeg_path}", flush=True)
    else:
        print("⚠️ ffmpeg not found in PATH - video/audio features may not work", flush=True)

print("=" * 50, flush=True)
print("Starting FastAPI application...", flush=True)
print("=" * 50, flush=True)

try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.middleware.cors import CORSMiddleware
    print("✅ FastAPI imported", flush=True)
    
    from database import engine, Base
    print("✅ Database imported", flush=True)
    
    from routes import auth, tts, payments, video
    print("✅ Routes imported", flush=True)
    
    print("DEBUG_DATABASE_URL:", os.getenv("DATABASE_URL"), flush=True)
    print("=" * 50, flush=True)
except Exception as e:
    print(f"❌ Import error: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Don't create tables here - let Alembic handle all migrations
# Base.metadata.create_all() can conflict with Alembic migrations
print("Database tables will be managed by Alembic migrations")

# Initialize FastAPI app
app = FastAPI(
    title="MyAIStudio API",
    description="Text-to-Speech API with ElevenLabs integration",
    version="1.0.0"
)

# ✅ FIXED: Proper CORS setup for both local + production
# CORS middleware must be added BEFORE routers to handle OPTIONS preflight requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://picvoice3labc.netlify.app",         # your deployed frontend
        "https://pakistani-project-frontend.netlify.app",  # backup / test domain
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(tts.router, prefix="/api", tags=["text-to-speech"])
app.include_router(payments.router, prefix="/api/payment", tags=["payments"])
app.include_router(video.router, prefix="/api/video", tags=["video"])

# ✅ Static files for generated videos
# Use app directory for generated_videos (writable location on Railway)
videos_dir = os.path.join(os.path.dirname(__file__), "generated_videos")
os.makedirs(videos_dir, exist_ok=True)
print(f"Video files directory: {os.path.abspath(videos_dir)}")

# Direct route handler to serve video files (more reliable than mount)
from fastapi.responses import FileResponse
from fastapi import HTTPException

@app.get("/static/videos/{filename}")
async def serve_video(filename: str):
    """Direct route handler to serve video files"""
    # Remove query parameters if present
    filename = filename.split('?')[0]
    file_path = os.path.join(videos_dir, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path, media_type="video/mp4")
    raise HTTPException(status_code=404, detail=f"Video file not found: {filename}")

@app.get("/")
async def root():
    return {"message": "MyAIStudio API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Print server startup info
print("=" * 50)
print("✅ FastAPI application initialized successfully!")
print("Routes registered:")
print("  - /auth/* (authentication)")
print("  - /api/* (text-to-speech)")
print("  - /api/payment/* (payments)")
print("  - /api/video/* (video generation)")
print("  - /static/videos/* (video files)")
print("=" * 50)
print("🚀 Starting Uvicorn server...")
print("=" * 50)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)