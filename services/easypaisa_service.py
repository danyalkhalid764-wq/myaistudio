import httpx
import uuid
import os
from dotenv import load_dotenv
from config import settings

load_dotenv()

EASYPAY_API_KEY = os.getenv("EASYPAY_API_KEY")
EASYPAY_MERCHANT_ID = os.getenv("EASYPAY_MERCHANT_ID")
EASYPAY_STORE_ID = os.getenv("EASYPAY_STORE_ID")
EASYPAY_BASE_URL = "https://api.easypay.com.pk"  # Replace with actual Easypaisa API URL

class EasypaisaService:
    def __init__(self):
        self.api_key = EASYPAY_API_KEY
        self.merchant_id = EASYPAY_MERCHANT_ID
        self.store_id = EASYPAY_STORE_ID
        self.base_url = EASYPAY_BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def create_payment(self, amount: float, user_id: int, plan: str) -> dict:
        """
        Create payment request with Easypaisa
        """
        transaction_id = str(uuid.uuid4())
        
        # Use environment variables for URLs, fallback to localhost for development
        frontend_url = settings.FRONTEND_URL or "http://localhost:3000"
        backend_url = settings.BACKEND_URL or "http://localhost:8000"
        
        data = {
            "merchant_id": self.merchant_id,
            "store_id": self.store_id,
            "amount": amount,
            "currency": "PKR",
            "transaction_id": transaction_id,
            "description": f"Upgrade to {plan} plan",
            "return_url": f"{frontend_url}/payment/success",
            "cancel_url": f"{frontend_url}/payment/cancel",
            "callback_url": f"{backend_url}/api/payment/callback",
            "customer": {
                "user_id": user_id
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/v1/payments",
                    json=data,
                    headers=self.headers
                )
                response.raise_for_status()
                result = response.json()
                
                return {
                    "success": True,
                    "payment_url": result.get("payment_url"),
                    "transaction_id": transaction_id
                }
            except httpx.HTTPStatusError as e:
                print(f"Easypaisa API error: {e.response.status_code} - {e.response.text}")
                return {
                    "success": False,
                    "error": f"Payment creation failed: {e.response.text}"
                }
            except Exception as e:
                print(f"Unexpected error: {e}")
                return {
                    "success": False,
                    "error": "Payment creation failed"
                }
    
    async def verify_payment(self, transaction_id: str) -> dict:
        """
        Verify payment status with Easypaisa
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/payments/{transaction_id}/status",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error verifying payment: {e}")
                return {"status": "failed"}





