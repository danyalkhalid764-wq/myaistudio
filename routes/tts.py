from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, VoiceHistory
from schemas import VoiceGenerateRequest, VoiceGenerateResponse
from services.elevenlabs_service import ElevenLabsService
from utils.audio_utils import add_watermark_to_audio, audio_to_base64
from routes.auth import get_current_user
import os
from datetime import datetime, date

router = APIRouter()
elevenlabs_service = ElevenLabsService()

@router.post("/generate-voice", response_model=VoiceGenerateResponse)
async def generate_voice(
    request: VoiceGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Reset daily counters if needed
    today = date.today()
    if current_user.last_reset_date != today:
        current_user.daily_voice_count = 0
        current_user.daily_video_count = 0
        # Note: total_tokens_used is NOT reset daily - it's a lifetime limit
        current_user.last_reset_date = today
        db.commit()

    # Count words in the text (treat each word as 1 token)
    word_count = len(request.text.split())
    
    # Enforce plan limits based on tokens/words
    if current_user.plan == "Free":
        # Free users: 150 words max per generation, 300 total tokens max
        MAX_WORDS_PER_GENERATION = 150
        MAX_TOTAL_TOKENS = 300
        
        # Check word limit per generation
        if word_count > MAX_WORDS_PER_GENERATION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Text exceeds maximum word limit. Maximum {MAX_WORDS_PER_GENERATION} words allowed for free plan. Your text has {word_count} words."
            )
        
        # Check total tokens used
        if current_user.total_tokens_used is None:
            current_user.total_tokens_used = 0
        
        if current_user.total_tokens_used + word_count > MAX_TOTAL_TOKENS:
            remaining = MAX_TOTAL_TOKENS - current_user.total_tokens_used
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Token limit reached. You have used {current_user.total_tokens_used}/{MAX_TOTAL_TOKENS} tokens. You can generate up to {remaining} more words."
            )
    else:
        # Paid users: unlimited generations but max 800 tokens per person
        MAX_TOTAL_TOKENS = 800
        
        # Check total tokens used
        if current_user.total_tokens_used is None:
            current_user.total_tokens_used = 0
        
        if current_user.total_tokens_used + word_count > MAX_TOTAL_TOKENS:
            remaining = MAX_TOTAL_TOKENS - current_user.total_tokens_used
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Token limit reached. You have used {current_user.total_tokens_used}/{MAX_TOTAL_TOKENS} tokens. You can generate up to {remaining} more words."
            )
    
    try:
        # Generate voice using ElevenLabs
        audio_data = await elevenlabs_service.generate_voice(request.text)
        
        # Handle trial vs paid users
        if current_user.plan == "Free":
            # Add watermark for trial users
            watermarked_audio = add_watermark_to_audio(audio_data)
            
            # Save to voice history (no permanent URL for trial)
            voice_entry = VoiceHistory(
                user_id=current_user.id,
                text=request.text,
                audio_url=None  # No permanent URL for trial users
            )
            db.add(voice_entry)
            
            # Update token usage
            if current_user.total_tokens_used is None:
                current_user.total_tokens_used = 0
            current_user.total_tokens_used += word_count
            
            # Increment daily count
            current_user.daily_voice_count += 1
            db.commit()
            
            remaining_tokens = 300 - current_user.total_tokens_used
            return VoiceGenerateResponse(
                success=True,
                message="Voice generated successfully (Trial version with watermark)",
                audio_data=watermarked_audio,
                audio_url=None,
                daily_count=current_user.daily_voice_count,
                limit_reached=current_user.total_tokens_used >= 300,
                tokens_used=current_user.total_tokens_used,
                tokens_remaining=remaining_tokens
            )
        else:
            # Paid users get full quality without watermark
            # In production, you'd save the audio file and return a URL
            audio_base64 = audio_to_base64(audio_data)
            
            # Save to voice history with URL
            voice_entry = VoiceHistory(
                user_id=current_user.id,
                text=request.text,
                audio_url=None  # Will be set after commit
            )
            db.add(voice_entry)
            
            # Update token usage
            if current_user.total_tokens_used is None:
                current_user.total_tokens_used = 0
            current_user.total_tokens_used += word_count
            
            db.commit()
            db.refresh(voice_entry)
            
            # Update with actual URL
            voice_entry.audio_url = f"generated_audio_{voice_entry.id}.mp3"  # In production, actual URL
            db.commit()
            
            remaining_tokens = 800 - current_user.total_tokens_used
            return VoiceGenerateResponse(
                success=True,
                message="Voice generated successfully",
                audio_data=audio_base64,  # For immediate playback
                audio_url=voice_entry.audio_url,
                daily_count=current_user.daily_voice_count,
                limit_reached=current_user.total_tokens_used >= 800,
                tokens_used=current_user.total_tokens_used,
                tokens_remaining=remaining_tokens
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice generation failed: {str(e)}"
        )

@router.get("/history")
async def get_voice_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's voice generation history"""
    history = db.query(VoiceHistory).filter(VoiceHistory.user_id == current_user.id).all()
    
    return [
        {
            "id": entry.id,
            "text": entry.text,
            "audio_url": entry.audio_url,
            "created_at": entry.created_at
        }
        for entry in history
    ]

@router.get("/plan")
async def get_plan_info(current_user: User = Depends(get_current_user)):
    """Get user's current plan information"""
    if current_user.total_tokens_used is None:
        current_user.total_tokens_used = 0
    
    if current_user.plan == "Free":
        tokens_remaining = max(0, 300 - current_user.total_tokens_used)
        features = [
            "150 words max per generation",
            "300 tokens total limit",
            "Watermarked audio",
            "No download option"
        ]
        return {
            "plan": current_user.plan,
            "max_words_per_generation": 150,
            "max_total_tokens": 300,
            "tokens_used": current_user.total_tokens_used,
            "tokens_remaining": tokens_remaining,
            "features": features
        }
    else:  # Paid
        tokens_remaining = max(0, 800 - current_user.total_tokens_used)
        features = [
            "Unlimited generations",
            "800 tokens total limit per person",
            "High-quality audio",
            "Download enabled",
            "No watermarks",
            "Priority processing"
        ]
        return {
            "plan": current_user.plan,
            "max_total_tokens": 800,
            "tokens_used": current_user.total_tokens_used,
            "tokens_remaining": tokens_remaining,
            "features": features
        }
