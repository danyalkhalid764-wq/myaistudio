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

        # Step 1: Determine canvas size based on the largest image
        # Use the largest image's dimensions as the canvas to show images at full size
        max_w, max_h = 0, 0
        for path in saved_paths:
            clip_temp = ImageClip(path)
            iw, ih = clip_temp.size
            max_w = max(max_w, iw)
            max_h = max(max_h, ih)
            clip_temp.close()  # Close temporary clip
        
        # Canvas size matches the largest image dimensions
        W = max_w
        H = max_h
        
        # Ensure minimum dimensions for very small images
        if W < 640 or H < 480:
            # Scale up small images to minimum size while maintaining aspect ratio
            min_scale = max(640 / W, 480 / H)
            W = int(W * min_scale)
            H = int(H * min_scale)
        
        # Limit maximum dimensions to prevent extremely large videos
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

        for idx, path in enumerate(saved_paths):
            clip = ImageClip(path)
            iw, ih = clip.size

            # Calculate scale to fit image to canvas while maintaining aspect ratio
            # Use scale_to_fit to show full image without cropping
            base_scale = min(W / iw, H / ih)
            base_w, base_h = int(iw * base_scale), int(ih * base_scale)
            
            # Ensure image fills canvas better - if image is much smaller, scale it up
            # But don't crop - show full image
            if base_w < W * 0.8 or base_h < H * 0.8:
                # Image is significantly smaller than canvas, scale up slightly
                fill_scale = min(W / iw, H / ih) * 1.1  # Scale up 10% but don't exceed canvas
                fill_scale = min(fill_scale, min(W / iw, H / ih) * 1.2)  # Cap at 20% larger
                base_scale = fill_scale
                base_w, base_h = int(iw * base_scale), int(ih * base_scale)
                # Ensure we don't exceed canvas
                if base_w > W:
                    base_scale = W / iw
                    base_w, base_h = int(iw * base_scale), int(ih * base_scale)
                if base_h > H:
                    base_scale = H / ih
                    base_w, base_h = int(iw * base_scale), int(ih * base_scale)
            
            # Apply transition effects based on transition parameter
            if transition == "kenburns" and slide_effect:
                # Ken Burns effect: slow zoom in (from 1.0x to 1.2x)
                def kenburns_zoom(t):
                    progress = min(t / dur, 1.0) if dur > 0 else 0
                    zoom_factor = 1.0 + (0.2 * progress)  # Zoom from 1.0 to 1.2
                    return base_scale * zoom_factor
                clip = clip.resize(kenburns_zoom)
            elif transition == "zoom_in" and slide_effect:
                # Zoom in effect (from 1.0x to 1.3x)
                def zoom_in_func(t):
                    progress = min(t / dur, 1.0) if dur > 0 else 0
                    zoom_factor = 1.0 + (0.3 * progress)  # Zoom from 1.0 to 1.3
                    return base_scale * zoom_factor
                clip = clip.resize(zoom_in_func)
            elif transition == "zoom_out" and slide_effect:
                # Zoom out effect (from 1.3x to 1.0x)
                def zoom_out_func(t):
                    progress = min(t / dur, 1.0) if dur > 0 else 0
                    zoom_factor = 1.3 - (0.3 * progress)  # Zoom from 1.3 to 1.0
                    return base_scale * zoom_factor
                clip = clip.resize(zoom_out_func)
            elif transition == "none" or not slide_effect:
                # No zoom effect - use base size
                clip = clip.resize((base_w, base_h))
            else:
                # Default: no zoom effect
                clip = clip.resize((base_w, base_h))
            
            # Set position - slide effect moves from right to center
            if transition == "slide" and slide_effect and idx > 0:
                # Slide effect: slide in from right to center
                def slide_position(t):
                    progress = min(t / dur, 1.0) if dur > 0 else 0
                    # Smooth easing function for better animation
                    eased_progress = progress * progress * (3.0 - 2.0 * progress)  # Smoothstep
                    # Start off-screen right (x = W), slide to center (x = "center")
                    # Calculate actual x position
                    clip_w = base_w if not hasattr(clip, 'w') or clip.w is None else clip.w
                    start_x = W  # Start off-screen right
                    end_x = (W - clip_w) / 2  # Center position
                    x_pos = start_x - (start_x - end_x) * eased_progress
                    return (x_pos, "center")
                clip = clip.set_position(slide_position)
            else:
                # Center position for all other cases
                clip = clip.set_position(("center", "center"))

            # Create black background same size as canvas
            background = ColorClip(size=(W, H), color=(0, 0, 0), duration=dur)

            # Center image on black background
            final_clip = CompositeVideoClip(
                [background, clip],
                size=(W, H)
            ).set_duration(dur)

            clips.append(final_clip)

        # Concatenate clips with transitions
        if not clips:
            raise HTTPException(status_code=500, detail="No clips generated")
        
        if len(clips) > 1:
            # Use crossfade if enabled for smoother transitions
            if crossfade:
                cf = min(1.0, dur * 0.3)  # 30% of duration or max 1 second
                final = concatenate_videoclips(clips, method="compose", padding=-cf)
            else:
                # Simple concatenation without crossfade
                final = concatenate_videoclips(clips, method="compose")
        else:
            final = clips[0]

        # Output directory for generated videos
        # Use project root generated_videos directory
        videos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_videos"))
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

        # Return full URL for the video
        # Use localhost for local development, or get from config for production
        from config import settings
        base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        if base_url == "http://localhost:8000" or not base_url:
            video_url = f"http://localhost:8000/static/videos/{filename}"
        else:
            video_url = f"{base_url}/static/videos/{filename}"

        return {
            "success": True,
            "message": "Slideshow video generated successfully.",
            "video_url": video_url,
        }
    finally:
        # Cleanup temporary files
        for p in saved_paths:
            try:
                os.remove(p)
            except Exception:
                pass

