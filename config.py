import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/myaistudio")

    # JWT Settings
    JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # ElevenLabs API
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

    # Easypaisa API
    EASYPAY_API_KEY = os.getenv("EASYPAY_API_KEY")
    EASYPAY_MERCHANT_ID = os.getenv("EASYPAY_MERCHANT_ID")
    EASYPAY_STORE_ID = os.getenv("EASYPAY_STORE_ID")

    # Claid API
    CLAID_API_KEY = os.getenv("CLAID_API_KEY")

    # Frontend and Backend URLs - UPDATED FOR PRODUCTION
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://picvoice3labc.netlify.app")
    BACKEND_URL = os.getenv("BACKEND_URL", "https://pakistani-project-backend.up.railway.app")

    # CORS Settings - UPDATED WITH NETLIFY DOMAIN
    NETLIFY_URL = os.getenv("NETLIFY_URL", "https://picvoice3labc.netlify.app")
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "https://picvoice3labc.netlify.app",  # ← ADDED YOUR NETLIFY DOMAIN HERE
    ]
    # Add FRONTEND_URL to allowed origins if it's different from defaults
    if FRONTEND_URL not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(FRONTEND_URL)
    if NETLIFY_URL and NETLIFY_URL not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(NETLIFY_URL)

    # Allow all origins in production if CORS_ALLOW_ALL is set
    if os.getenv("CORS_ALLOW_ALL", "false").lower() == "true":
        ALLOWED_ORIGINS = ["*"]

    # Plan Settings
    TRIAL_DAILY_LIMIT = 3
    PLAN_PRICES = {
        "Starter": 500.0,
        "Pro": 1000.0
    }


settings = Settings()