import httpx
import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"

class ElevenLabsService:
    def __init__(self):
        self.api_key = ELEVENLABS_API_KEY
        self.base_url = ELEVENLABS_BASE_URL
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
    
    async def generate_voice(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
        """
        Generate voice using ElevenLabs API
        Uses free tier compatible models
        """
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        # Try free tier compatible models in order
        models_to_try = [
            "eleven_turbo_v2_5",  # Latest free tier model
            "eleven_turbo_v2",    # Fallback option
            "eleven_multilingual_v2",  # Multilingual option
        ]
        
        async with httpx.AsyncClient() as client:
            last_error = None
            for model_id in models_to_try:
                try:
                    data = {
                        "text": text,
                        "model_id": model_id,
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.5
                        }
                    }
                    
                    print(f"🎤 Trying model: {model_id}", flush=True)
                    response = await client.post(url, json=data, headers=self.headers)
                    response.raise_for_status()
                    print(f"✅ Voice generated successfully with model: {model_id}", flush=True)
                    return response.content
                    
                except httpx.HTTPStatusError as e:
                    error_text = e.response.text
                    print(f"⚠️ Model {model_id} failed: {e.response.status_code} - {error_text}", flush=True)
                    last_error = e
                    # If it's a model deprecation error, try next model
                    if "model_deprecated" in error_text or "model_deprecated_free_tier" in error_text:
                        continue
                    # If it's a different error, raise it
                    raise Exception(f"Voice generation failed: {error_text}")
                except Exception as e:
                    print(f"⚠️ Unexpected error with model {model_id}: {e}", flush=True)
                    last_error = e
                    continue
            
            # If all models failed, raise the last error
            if last_error:
                raise Exception(f"Voice generation failed: All models failed. Last error: {last_error.response.text if hasattr(last_error, 'response') else str(last_error)}")
            raise Exception("Voice generation failed: No models available")
    
    async def get_voices(self):
        """
        Get available voices
        """
        url = f"{self.base_url}/voices"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error fetching voices: {e}")
                return []





