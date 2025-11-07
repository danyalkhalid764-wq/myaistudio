import base64
import io
import os
from dotenv import load_dotenv

load_dotenv()

# Try to import pydub, fallback if not available
try:
    from pydub import AudioSegment
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





