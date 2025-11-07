import httpx
import os
from dotenv import load_dotenv
from config import settings

load_dotenv()

CLAID_API_KEY = settings.CLAID_API_KEY
CLAID_BASE_URL = "https://api.claid.ai/v1"

class ClaidService:
    def __init__(self):
        self.api_key = CLAID_API_KEY
        self.base_url = CLAID_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_image(self, prompt: str, width: int = 1024, height: int = 1024) -> dict:
        """
        Generate image using Claid API (with fallback to mock)
        """
        # For now, return a mock response since the Claid API endpoints are not working
        print(f"Generating mock image for prompt: {prompt}")
        print(f"Dimensions: {width}x{height}")
        
        # Return a placeholder image URL
        mock_image_url = f"https://via.placeholder.com/{width}x{height}/0066cc/ffffff?text={prompt.replace(' ', '+')}"
        
        return {
            "success": True,
            "image_url": mock_image_url,
            "data": {
                "prompt": prompt,
                "width": width,
                "height": height,
                "mock": True
            }
        }
        
        # Original Claid API code (commented out until we find the correct endpoint)
        """
        url = f"{self.base_url}/image"
        
        data = {
            "prompt": prompt,
            "width": width,
            "height": height
        }
        
        print(f"Making request to Claid API: {url}")
        print(f"Request data: {data}")
        print(f"Headers: {self.headers}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, json=data, headers=self.headers)
                print(f"Response status: {response.status_code}")
                print(f"Response text: {response.text}")
                
                response.raise_for_status()
                result = response.json()
                
                print(f"Parsed response: {result}")
                
                return {
                    "success": True,
                    "image_url": result.get("image_url") or result.get("url"),
                    "data": result
                }
            except httpx.HTTPStatusError as e:
                print(f"Claid API error: {e.response.status_code} - {e.response.text}")
                return {
                    "success": False,
                    "error": f"Image generation failed: {e.response.text}"
                }
            except Exception as e:
                print(f"Unexpected error: {e}")
                import traceback
                traceback.print_exc()
                return {
                    "success": False,
                    "error": f"Image generation failed: {str(e)}"
                }
        """
    
    async def get_image_status(self, image_id: str) -> dict:
        """
        Get image generation status
        """
        url = f"{self.base_url}/image/{image_id}/status"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error getting image status: {e}")
                return {"status": "failed"}


