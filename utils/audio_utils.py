import base64
import io
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

# Configure pydub to use ffmpeg BEFORE importing pydub
# This prevents the warning from appearing when pydub checks for ffmpeg at import time
ffmpeg_binary = None
try:
    import imageio_ffmpeg
    ffmpeg_binary = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_binary)
    # Add to PATH so pydub can find it
    if ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    # Set environment variable that pydub checks
    os.environ["FFMPEG_BINARY"] = ffmpeg_binary
except Exception:
    # Fallback to system ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        if ffmpeg_dir not in os.environ.get("PATH", ""):
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        os.environ["FFMPEG_BINARY"] = ffmpeg_path
        ffmpeg_binary = ffmpeg_path

# Suppress pydub's warning by setting the converter before import
# pydub checks for ffmpeg in utils.py at import time, so we need to configure it first
import warnings
warnings.filterwarnings("ignore", message=".*ffmpeg.*", category=RuntimeWarning)

# Try to import pydub, fallback if not available
try:
    from pydub import AudioSegment
    # Configure AudioSegment to use our ffmpeg binary if found
    if ffmpeg_binary:
        # Set the converter directly to avoid pydub's check
        AudioSegment.converter = ffmpeg_binary
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Watermarking will be disabled.")

def add_watermark_to_audio(audio_data: bytes) -> str:
    """
    Add watermark audio to the generated voice for trial users
    """
    if not PYDUB_AVAILABLE:
        # If pydub is not available, just return the original audio
        return base64.b64encode(audio_data).decode('utf-8')
    
    try:
        # Load the main audio
        main_audio = AudioSegment.from_file(io.BytesIO(audio_data))
        
        # Create watermark text as audio (you might want to use TTS for this)
        # For now, we'll create a simple beep as watermark
        watermark_audio = AudioSegment.sine(440, duration=1000)  # 1 second beep
        
        # Add watermark at the end
        watermarked_audio = main_audio + watermark_audio
        
        # Convert to base64 for streaming
        output = io.BytesIO()
        watermarked_audio.export(output, format="mp3")
        watermarked_data = output.getvalue()
        
        return base64.b64encode(watermarked_data).decode('utf-8')
    
    except Exception as e:
        print(f"Error adding watermark: {e}")
        # Return original audio if watermarking fails
        return base64.b64encode(audio_data).decode('utf-8')

def audio_to_base64(audio_data: bytes) -> str:
    """
    Convert audio bytes to base64 string
    """
    return base64.b64encode(audio_data).decode('utf-8')





