from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, VoiceHistory
from schemas import VoiceGenerateRequest, VoiceGenerateResponse
from services.lamonfox_service import LamonfoxService
from utils.audio_utils import add_watermark_to_audio, audio_to_base64
from routes.auth import get_current_user
import os
from datetime import datetime, date

router = APIRouter()
lamonfox_service = LamonfoxService()

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
        # Validate Lamonfox API key before attempting generation
        if not lamonfox_service.api_key:
            print("❌ Lamonfox API key is not configured", flush=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Voice generation service is not configured. Please contact support."
            )
        
        print(f"🎤 Generating voice for user {current_user.email} (Plan: {current_user.plan})", flush=True)
        print(f"📝 Text length: {len(request.text)} characters, Word count: {word_count}", flush=True)
        
        # Generate voice using Lamonfox
        audio_data = await lamonfox_service.generate_voice(request.text)
        
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
            
    except HTTPException:
        # Re-raise HTTP exceptions as-is (they already have proper status codes)
        raise
    except Exception as e:
        # Log detailed error information for debugging
        import traceback
        error_detail = str(e)
        traceback_str = traceback.format_exc()
        print(f"❌ Voice generation error: {error_detail}", flush=True)
        print(f"Traceback: {traceback_str}", flush=True)
        
        # Determine appropriate status code and error message
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_message = error_detail  # Use the actual error message by default
        
        # Map specific errors to appropriate status codes and messages
        if "API key" in error_detail or "api_key" in error_detail.lower() or "not configured" in error_detail.lower():
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_message = "Voice generation service configuration error. Please contact support."
        elif "Payment required" in error_detail or "free tier" in error_detail.lower() or "unusual activity" in error_detail.lower():
            status_code = status.HTTP_402_PAYMENT_REQUIRED
            error_message = error_detail  # Preserve the actual error message from Lamonfox
        elif "quota" in error_detail.lower() or "limit" in error_detail.lower():
            status_code = status.HTTP_429_TOO_MANY_REQUESTS
            error_message = "Voice generation quota exceeded. Please try again later."
        elif "rate limit" in error_detail.lower():
            status_code = status.HTTP_429_TOO_MANY_REQUESTS
            error_message = error_detail
        elif "network" in error_detail.lower() or "connection" in error_detail.lower() or "timeout" in error_detail.lower():
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            error_message = "Network error. Please check your connection and try again."
        elif "invalid" in error_detail.lower() and "request" in error_detail.lower():
            status_code = status.HTTP_400_BAD_REQUEST
            error_message = error_detail
        
        raise HTTPException(
            status_code=status_code,
            detail=error_message
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

@router.get("/debug")
async def debug_tts_service(current_user: User = Depends(get_current_user)):
    """Debug endpoint to check TTS service configuration"""
    api_key_set = bool(lamonfox_service.api_key)
    api_key_preview = f"{lamonfox_service.api_key[:10]}...{lamonfox_service.api_key[-5:]}" if lamonfox_service.api_key and len(lamonfox_service.api_key) > 15 else ("Set" if api_key_set else "Not Set")
    
    return {
        "service": "Lamonfox",
        "api_key_configured": api_key_set,
        "api_key_preview": api_key_preview,
        "base_url": lamonfox_service.base_url,
        "status": "ready" if api_key_set else "missing_api_key"
    }

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
