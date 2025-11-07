from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# =======================
# User Schemas
# =======================
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    plan: str
    daily_voice_count: int
    daily_video_count: Optional[int] = 0  # Optional since you don't need it
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    plan: str
    daily_voice_count: int
    daily_video_count: Optional[int] = 0
    created_at: datetime


# =======================
# Token Schemas
# =======================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# =======================
# Voice Generation Schemas
# =======================
class VoiceGenerateRequest(BaseModel):
    text: str

class VoiceGenerateResponse(BaseModel):
    success: bool
    message: str
    audio_data: Optional[str] = None  # Base64 encoded audio for trial users
    audio_url: Optional[str] = None   # URL for paid users
    daily_count: int
    limit_reached: bool = False
    tokens_used: Optional[int] = None
    tokens_remaining: Optional[int] = None


# =======================
# Payment Schemas
# =======================
class PaymentCreateRequest(BaseModel):
    plan: str  # Starter, Pro
    amount: float

class PaymentCreateResponse(BaseModel):
    success: bool
    payment_url: str
    transaction_id: str

class PaymentCallback(BaseModel):
    transaction_id: str
    status: str
    amount: float


# =======================
# Voice History Schemas
# =======================
class VoiceHistoryResponse(BaseModel):
    id: int
    text: str
    audio_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# =======================
# Plan Info Schemas
# =======================
class PlanInfo(BaseModel):
    plan: str
    daily_limit: int
    remaining_generations: int
    features: List[str]


# =======================
# Video Generation Schemas
# =======================
class VideoGenerateResponse(BaseModel):
    success: bool
    message: str
    video_url: Optional[str] = None
    daily_count: int
    limit_reached: bool = False
