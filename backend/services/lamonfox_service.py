import httpx
import os
from dotenv import load_dotenv

load_dotenv()

LAMONFOX_API_KEY = os.getenv("LAMONFOX_API_KEY")
LAMONFOX_BASE_URL = "https://api.lemonfox.ai/v1"

# List of free proxies to rotate through
PROXIES = [
    "http://proxy.scrape.center:8080",
    "http://51.158.68.68:8811",
    "http://103.187.98.25:8080",
    "http://34.146.64.228:3128",
    "http://185.199.229.156:7492"
]

def get_proxy():
    """Get proxy configuration for httpx"""
    # Return first proxy (will be rotated in the request logic)
    # httpx uses string URL format, not dict
    return PROXIES[0] if PROXIES else None

class LamonfoxService:
    def __init__(self):
        self.api_key = LAMONFOX_API_KEY
        self.base_url = LAMONFOX_BASE_URL
        
        # Validate API key on initialization
        if not self.api_key:
            print("⚠️ WARNING: LAMONFOX_API_KEY is not set in environment variables", flush=True)
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key or ''}",
            "Content-Type": "application/json",
            "User-Agent": "MyAIStudio/1.0",  # Add user agent to identify the application
            "Accept": "audio/mpeg"  # Explicitly request audio response
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
        
        # Try each proxy until one works
        last_error = None
        for proxy_url in PROXIES:
            try:
                print(f"🎤 Generating voice with Lamonfox API (voice: {voice}, format: {response_format})", flush=True)
                print(f"🔗 API URL: {url}", flush=True)
                print(f"🌐 Trying proxy: {proxy_url}", flush=True)
                
                # Log API key info (safely)
                if self.api_key:
                    key_preview = f"{self.api_key[:10]}...{self.api_key[-5:]}" if len(self.api_key) > 15 else f"{self.api_key[:5]}***"
                    print(f"🔑 Using API key: {key_preview}", flush=True)
                else:
                    print(f"🔑 API key: NOT SET", flush=True)
                
                # Create client with proxy
                proxies = {
                    "http://": proxy_url,
                    "https://": proxy_url
                }
                
                async with httpx.AsyncClient(timeout=60.0, proxies=proxies) as client:
                    response = await client.post(url, json=data, headers=self.headers)
                    
                    # Log response status
                    print(f"📡 Response status: {response.status_code}", flush=True)
                    
                    response.raise_for_status()
                    print(f"✅ Voice generated successfully with Lamonfox API using proxy: {proxy_url}", flush=True)
                    return response.content
                    
            except httpx.ProxyError as e:
                print(f"⚠️ Proxy {proxy_url} failed: {e}", flush=True)
                last_error = e
                continue  # Try next proxy
            except httpx.HTTPStatusError as e:
                # If we get an HTTP error (not proxy error), don't try other proxies
                # This means the request reached the API but got an error response
                error_text = e.response.text if e.response else "Unknown error"
                status_code = e.response.status_code if e.response else 0
                
                # Try to parse JSON error response
                try:
                    if e.response:
                        error_json = e.response.json()
                        if isinstance(error_json, dict):
                            if "detail" in error_json:
                                detail = error_json["detail"]
                                if isinstance(detail, dict):
                                    message = detail.get("message", error_text)
                                    status_msg = detail.get("status", "")
                                    error_text = f"{status_msg}: {message}" if status_msg else message
                                else:
                                    error_text = str(detail)
                except:
                    pass  # If JSON parsing fails, use original error_text
                
                print(f"⚠️ Lamonfox API error: {status_code} - {error_text}", flush=True)
                print(f"🔑 API Key (first 10 chars): {self.api_key[:10] if self.api_key else 'None'}...", flush=True)
                
                # Handle specific error cases
                if status_code == 401:
                    raise Exception("Lamonfox API key is invalid or expired. Please check your API key configuration.")
                elif status_code == 402:
                    raise Exception("Payment required. Your API key may be on a free tier that has been disabled. Please upgrade to a paid plan or contact Lamonfox support.")
                elif status_code == 429:
                    raise Exception("Lamonfox API rate limit exceeded. Please try again later.")
                elif status_code == 400:
                    # Check for unusual activity error
                    if "unusual_activity" in error_text.lower() or "free tier" in error_text.lower():
                        error_msg = (
                            "Lamonfox API Error: Your account is being treated as Free Tier and has been flagged for unusual activity. "
                            "This can happen if:\n"
                            "1. Your API key is from a free account (even if you purchased credits)\n"
                            "2. Railway's IP address is flagged as a proxy/VPN\n"
                            "3. Your paid account needs to be activated\n\n"
                            "SOLUTION: Please contact Lamonfox support at https://lemonfox.ai with:\n"
                            "- Your API key (they can verify if it's paid)\n"
                            "- Request to whitelist Railway's IP addresses\n"
                            "- Ask them to activate your paid subscription\n\n"
                            f"Original error: {error_text}"
                        )
                        raise Exception(error_msg)
                    raise Exception(f"Invalid request: {error_text}")
                else:
                    raise Exception(f"Voice generation failed (HTTP {status_code}): {error_text}")
                    
            except httpx.TimeoutException:
                print(f"⚠️ Proxy {proxy_url} timed out", flush=True)
                last_error = Exception("Voice generation request timed out. Please try again.")
                continue  # Try next proxy
            except Exception as e:
                print(f"⚠️ Error with proxy {proxy_url}: {e}", flush=True)
                last_error = e
                continue  # Try next proxy
        
        # If all proxies failed, raise the last error
        if last_error:
            raise Exception(f"All proxies failed. Last error: {str(last_error)}")
        raise Exception("No proxies available")
    
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

