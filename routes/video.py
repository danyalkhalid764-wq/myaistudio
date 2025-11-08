from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime, timedelta
from database import get_db
from models import GeneratedVideo
from models import User as UserModel
from routes.auth import get_current_user
from sqlalchemy import and_

# Fix for Pillow 10.0.0+ compatibility with MoviePy
# Pillow removed Image.ANTIALIAS, but MoviePy still uses it
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        # Map ANTIALIAS to LANCZOS (which was the actual implementation)
        Image.ANTIALIAS = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS
except ImportError:
    pass

# MoviePy imports
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, ColorClip, vfx

router = APIRouter()


@router.post("/slideshow")
async def create_slideshow_video(
    images: List[UploadFile] = File(..., description="2-3 image files"),
    duration_seconds: int = Form(2),
    crossfade: bool = Form(False),
    slide_effect: bool = Form(True),
    transition: str = Form("slide"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Daily limit removed - no restrictions on video generation
    # Validate number of images
    if not (2 <= len(images) <= 3):
        raise HTTPException(status_code=400, detail="Please upload 2 to 3 images.")

    # Validate formats and persist temporarily
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tmp_uploads"))
    os.makedirs(temp_dir, exist_ok=True)

    saved_paths: List[str] = []
    try:
        for idx, f in enumerate(images):
            if not f.content_type or not f.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail=f"Invalid file type for image {idx + 1}.")
            ext = os.path.splitext(f.filename or "")[1].lower() or ".jpg"
            # Restrict to raster formats supported by PIL/moviepy
            if ext not in {".jpg", ".jpeg", ".png"}:
                raise HTTPException(status_code=400, detail=f"Unsupported image format '{ext}'. Please upload JPG or PNG.")
            temp_name = f"{uuid.uuid4().hex}{ext}"
            temp_path = os.path.join(temp_dir, temp_name)
            with open(temp_path, "wb") as out:
                out.write(await f.read())
            saved_paths.append(temp_path)

        # Step 1: Determine dynamic canvas size based on all uploaded images
        # Get maximum width and height from all images
        max_w, max_h = 0, 0
        for path in saved_paths:
            clip_temp = ImageClip(path)
            iw, ih = clip_temp.size
            max_w = max(max_w, iw)
            max_h = max(max_h, ih)
            clip_temp.close()  # Close temporary clip
        
        # Canvas size is the maximum dimensions from all images
        W = max_w
        H = max_h
        
        # Ensure minimum dimensions (optional, but helps with very small images)
        W = max(W, 1280)
        H = max(H, 720)
        
        # Limit maximum dimensions to prevent extremely large videos (faster encoding)
        # Cap at Full HD for faster processing while maintaining good quality
        MAX_WIDTH = 1920
        MAX_HEIGHT = 1080
        if W > MAX_WIDTH or H > MAX_HEIGHT:
            # Scale down proportionally if exceeding max dimensions
            scale_w = MAX_WIDTH / W if W > MAX_WIDTH else 1
            scale_h = MAX_HEIGHT / H if H > MAX_HEIGHT else 1
            scale = min(scale_w, scale_h)
            W = int(W * scale)
            H = int(H * scale)
        
        dur = max(1, int(duration_seconds))
        clips = []

        for path in saved_paths:
            clip = ImageClip(path)
            iw, ih = clip.size

            # Calculate scale factor to fit inside canvas (no cropping)
            scale = min(W / iw, H / ih)
            new_w, new_h = int(iw * scale), int(ih * scale)
            clip = clip.resize((new_w, new_h))

            # Create black background same size as canvas
            background = ColorClip(size=(W, H), color=(0, 0, 0), duration=dur)

            # Center image on black background
            final_clip = CompositeVideoClip(
                [background, clip.set_position(("center", "center"))],
                size=(W, H)
            ).set_duration(dur)

            clips.append(final_clip)

        if crossfade and len(clips) > 1:
            cf = 1  # 1 second crossfade looks reasonable for short durations
            final = concatenate_videoclips(clips, method="compose", padding=-cf)
        else:
            final = concatenate_videoclips(clips, method="compose")

        # Output directory for generated videos
        # Use app directory for generated_videos (writable location on Railway)
        videos_dir = os.path.join(os.path.dirname(__file__), "..", "generated_videos")
        videos_dir = os.path.abspath(videos_dir)
        os.makedirs(videos_dir, exist_ok=True)

        filename = f"slideshow_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(videos_dir, filename)

        # Write video file with optimized settings for faster generation
        final.write_videofile(
            output_path,
            fps=24,  # Standard framerate (lower = faster)
            codec="libx264",
            preset="ultrafast",  # Fastest preset for quick generation
            bitrate="2000k",  # Lower bitrate for faster encoding (still good quality)
            audio=False,
            verbose=False,
            logger=None,
            threads=4,  # Use multiple threads for faster encoding
            write_logfile=False,  # Disable logfile for faster processing
        )

        # Persist GeneratedVideo record for current user
        try:
            gv = GeneratedVideo(user_id=current_user.id, video_url=f"/static/videos/{filename}")
            db.add(gv)
            db.commit()
        except Exception:
            db.rollback()

        return {
            "success": True,
            "message": "Slideshow video generated successfully.",
            "video_url": f"/static/videos/{filename}",
        }
    finally:
        # Cleanup temporary files
        for p in saved_paths:
            try:
                os.remove(p)
            except Exception:
                pass

