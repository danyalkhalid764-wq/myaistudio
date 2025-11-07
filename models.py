from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    plan = Column(String, default="Free")  # Free, Paid
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ Only daily voice counter (video removed)
    daily_voice_count = Column(Integer, nullable=True, default=0, server_default="0")
    last_reset_date = Column(Date, nullable=True)
    
    # Token tracking for TTS generation
    total_tokens_used = Column(Integer, nullable=True, default=0, server_default="0")

    # Relationships
    voice_history = relationship("VoiceHistory", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    generated_videos = relationship("GeneratedVideo", back_populates="user")  # NEW


class VoiceHistory(Base):
    __tablename__ = "voice_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    audio_url = Column(String, nullable=True)  # For paid users
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="voice_history")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, completed, failed
    transaction_id = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="payments")


# ✅ NEW MODEL: GeneratedVideo
class GeneratedVideo(Base):
    __tablename__ = "generated_videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_url = Column(String, nullable=False)
    duration_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="generated_videos")
