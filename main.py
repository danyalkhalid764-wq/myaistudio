import sys
import os

# Force output immediately
sys.stdout.flush()
sys.stderr.flush()

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

# Create database tables if they don't exist (with error handling)
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified successfully")
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")
    print("Server will start, but database operations may fail until database is available")

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
# Use project root generated_videos directory to match video.py
videos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "generated_videos"))
os.makedirs(videos_dir, exist_ok=True)
print(f"Video files directory: {videos_dir}")

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