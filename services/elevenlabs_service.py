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
        """
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data, headers=self.headers)
                response.raise_for_status()
                return response.content
            except httpx.HTTPStatusError as e:
                print(f"ElevenLabs API error: {e.response.status_code} - {e.response.text}")
                raise Exception(f"Voice generation failed: {e.response.text}")
            except Exception as e:
                print(f"Unexpected error: {e}")
                raise Exception("Voice generation failed")
    
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





