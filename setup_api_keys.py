#!/usr/bin/env python3
"""
Setup API keys for MyAIStudio Backend
"""

import os

def setup_environment():
    """Setup environment variables"""
    
    # ElevenLabs API Key
    elevenlabs_key = "cd2d1a0fae74330e901929b4a5e8a51a40e060e34c56147bafb4c7a999b5a129"
    
    # Create .env file content
    env_content = f"""DATABASE_URL=postgresql://user:password@localhost:5432/myaistudio
ELEVENLABS_API_KEY={elevenlabs_key}
EASYPAY_API_KEY=your_easypay_api_key_here
EASYPAY_MERCHANT_ID=your_merchant_id_here
EASYPAY_STORE_ID=your_store_id_here
JWT_SECRET=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("SUCCESS: .env file created with your ElevenLabs API key!")
    print("ElevenLabs API Key configured successfully!")
    print("\nNext steps:")
    print("1. Restart your backend server: uvicorn main:app --reload")
    print("2. Test voice generation in the frontend")
    print("3. Your ElevenLabs API is ready to use!")

if __name__ == "__main__":
    setup_environment()
