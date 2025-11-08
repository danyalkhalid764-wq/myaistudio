from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status
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

# Configure MoviePy to use imageio-ffmpeg's ffmpeg binary
try:
    import imageio_ffmpeg
    ffmpeg_binary = imageio_ffmpeg.get_ffmpeg_exe()
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_binary
    # Set MoviePy's ffmpeg path
    import moviepy.config
    moviepy.config.FFMPEG_BINARY = ffmpeg_binary
except Exception as e:
    # If imageio-ffmpeg is not available, try to use system ffmpeg
    import shutil
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        import moviepy.config
        moviepy.config.FFMPEG_BINARY = ffmpeg_path

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
    try:
        print(f"🎬 Video slideshow request from user: {current_user.email} (ID: {current_user.id})", flush=True)
        print(f"📸 Number of images: {len(images)}", flush=True)
        print(f"⏱️ Duration: {duration_seconds} seconds", flush=True)
        
        # Daily limit removed - no restrictions on video generation
        # Validate number of images
        if not (2 <= len(images) <= 3):
            raise HTTPException(status_code=400, detail="Please upload 2 to 3 images.")

        # Validate formats and persist temporarily
        # Use app directory for tmp_uploads (writable location on Railway)
        temp_dir = os.path.join(os.path.dirname(__file__), "..", "tmp_uploads")
        temp_dir = os.path.abspath(temp_dir)
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
            
            print(f"🎨 Canvas size: {W}x{H}", flush=True)
            print(f"🎬 Slide effect: {slide_effect}, Transition: {transition}", flush=True)

            for idx, path in enumerate(saved_paths):
                clip = ImageClip(path)
                iw, ih = clip.size
                print(f"📷 Image {idx+1} size: {iw}x{ih}", flush=True)

                # Scale image to fill canvas while maintaining aspect ratio
                # Use max scale to fill canvas (ensures image fills screen, may crop edges)
                scale = max(W / iw, H / ih)
                new_w, new_h = int(iw * scale), int(ih * scale)
                print(f"🔍 Scaled to: {new_w}x{new_h} (scale: {scale:.2f})", flush=True)
                
                # Resize image to fill canvas
                clip = clip.resize((new_w, new_h))
                
                # Apply slide effects if enabled
                if slide_effect and transition != "none":
                    if transition == "ken_burns":
                        # Ken Burns effect: slow zoom and pan
                        # Use relative scaling for animation
                        clip = clip.resize(lambda t: 0.95 + 0.1 * t / dur)
                        # Pan from top-left to center
                        clip = clip.set_position(lambda t: (
                            -(new_w * (0.95 + 0.1 * t / dur) - W) / 2,
                            -(new_h * (0.95 + 0.1 * t / dur) - H) / 2
                        ))
                    elif transition == "zoom_in":
                        # Zoom in effect: start normal, zoom in
                        clip = clip.resize(lambda t: 1.0 + 0.15 * t / dur)
                        clip = clip.set_position("center")
                    elif transition == "zoom_out":
                        # Zoom out effect: start zoomed, zoom out
                        clip = clip.resize(lambda t: 1.15 - 0.15 * t / dur)
                        clip = clip.set_position("center")
                    elif transition == "slide":
                        # Slide effect: image slides in from right
                        clip = clip.set_position(lambda t: (
                            W - (W + new_w) * (1 - t / dur),
                            (H - new_h) / 2
                        ))
                    else:
                        # Default: center position, no animation
                        clip = clip.set_position("center")
                else:
                    # No slide effect: center the image, fill canvas
                    clip = clip.set_position("center")

                # Create background (black for contrast)
                background = ColorClip(size=(W, H), color=(0, 0, 0), duration=dur)

                # Composite image on background - ensure image is on top
                final_clip = CompositeVideoClip(
                    [background, clip],
                    size=(W, H)
                ).set_duration(dur)
                
                print(f"✅ Clip {idx+1} created: {final_clip.size}, duration: {dur}s", flush=True)

                clips.append(final_clip)

            # Apply transitions between clips
            if len(clips) > 1:
                if crossfade:
                    # Crossfade transition
                    cf_duration = min(0.5, dur * 0.3)  # 30% of clip duration or 0.5s max
                    final = concatenate_videoclips(clips, method="compose", padding=-cf_duration)
                elif transition in ["fade", "crossfade"]:
                    # Fade transition
                    cf_duration = min(0.5, dur * 0.3)
                    final = concatenate_videoclips(clips, method="compose", padding=-cf_duration)
                else:
                    # No transition: direct cut
                    final = concatenate_videoclips(clips, method="compose")
            else:
                final = clips[0] if clips else None
                
            if final is None:
                raise HTTPException(status_code=500, detail="Failed to create video")

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

            # Return full URL for production, relative URL for local dev
            from config import settings
            backend_url = os.getenv("BACKEND_URL", settings.BACKEND_URL)
            if backend_url and not backend_url.startswith("http://localhost"):
                # Production: return full URL
                video_url = f"{backend_url}/static/videos/{filename}"
            else:
                # Local dev: return relative URL (frontend will handle it)
                video_url = f"/static/videos/{filename}"

            print(f"✅ Video generated successfully: {filename}", flush=True)
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
    except HTTPException:
        # Re-raise HTTP exceptions (they already have proper status codes and CORS headers)
        raise
    except Exception as e:
        # Log the error and re-raise as HTTPException with CORS-friendly response
        import traceback
        error_detail = str(e)
        traceback_str = traceback.format_exc()
        print(f"❌ Video generation error: {error_detail}", flush=True)
        print(f"Traceback: {traceback_str}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Video generation failed: {error_detail}"
        )

