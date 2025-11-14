import httpx
import os
from dotenv import load_dotenv

load_dotenv()

LAMONFOX_API_KEY = os.getenv("LAMONFOX_API_KEY")
LAMONFOX_BASE_URL = "https://api.lemonfox.ai/v1"

class LamonfoxService:
    def __init__(self):
        self.api_key = LAMONFOX_API_KEY
        self.base_url = LAMONFOX_BASE_URL
        
        # Validate API key on initialization
        if not self.api_key:
            print("⚠️ WARNING: LAMONFOX_API_KEY is not set in environment variables", flush=True)
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key or ''}",
            "Content-Type": "application/json"
        }
    
    async def generate_voice(self, text: str, voice: str = "sarah", response_format: str = "mp3") -> bytes:
        """
        Generate voice using Lamonfox (Lemonfox.ai) API
        """
        # Validate API key before making request
        if not self.api_key:
            raise Exception("Lamonfox API key is not configured. Please set LAMONFOX_API_KEY environment variable.")
        
        # Validate text input
        if not text or not text.strip():
            raise Exception("Text input is required for voice generation")
        
        url = f"{self.base_url}/audio/speech"
        
        data = {
            "input": text,
            "voice": voice,  # Default: sarah, can be changed based on available voices
            "response_format": response_format  # Options: mp3, opus, aac, flac, wav, pcm
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                print(f"🎤 Generating voice with Lamonfox API (voice: {voice}, format: {response_format})", flush=True)
                response = await client.post(url, json=data, headers=self.headers)
                response.raise_for_status()
                print(f"✅ Voice generated successfully with Lamonfox API", flush=True)
                return response.content
                
            except httpx.HTTPStatusError as e:
                error_text = e.response.text if e.response else "Unknown error"
                status_code = e.response.status_code if e.response else 0
                print(f"⚠️ Lamonfox API error: {status_code} - {error_text}", flush=True)
                
                # Handle specific error cases
                if status_code == 401:
                    raise Exception("Lamonfox API key is invalid or expired. Please check your API key configuration.")
                elif status_code == 429:
                    raise Exception("Lamonfox API rate limit exceeded. Please try again later.")
                elif status_code == 400:
                    raise Exception(f"Invalid request: {error_text}")
                else:
                    raise Exception(f"Voice generation failed (HTTP {status_code}): {error_text}")
                    
            except httpx.TimeoutException:
                raise Exception("Voice generation request timed out. Please try again.")
            except Exception as e:
                print(f"⚠️ Unexpected error with Lamonfox API: {e}", flush=True)
                raise Exception(f"Voice generation failed: {str(e)}")
    
    async def get_voices(self):
        """
        Get available voices from Lamonfox API
        Note: This endpoint may vary - check Lamonfox documentation
        """
        # If Lamonfox provides a voices endpoint, implement it here
        # For now, return common voices
        return [
            {"id": "sarah", "name": "Sarah"},
            {"id": "james", "name": "James"},
            {"id": "emma", "name": "Emma"},
            {"id": "william", "name": "William"},
        ]

