from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, UserResponse, Token
from utils.jwt_handler import verify_password, get_password_hash, create_access_token, verify_token
from datetime import timedelta

router = APIRouter()

# OAuth2PasswordBearer with auto_error=False to allow OPTIONS preflight requests
# This is critical for CORS to work properly
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"📝 Registration attempt for email: {user.email}", flush=True)
        
        # Check if user already exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            print(f"⚠️ Email already registered: {user.email}", flush=True)
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create new user
        print(f"🔐 Hashing password for user: {user.email}", flush=True)
        hashed_password = get_password_hash(user.password)
        
        print(f"👤 Creating user object: {user.name}, {user.email}", flush=True)
        db_user = User(
            name=user.name,
            email=user.email,
            password_hash=hashed_password,
            plan="Free",
            daily_voice_count=0,
        )

        print(f"💾 Adding user to database...", flush=True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"✅ User created successfully: ID={db_user.id}, Email={db_user.email}", flush=True)

        return UserResponse(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            plan=db_user.plan,
            daily_voice_count=db_user.daily_voice_count or 0,
            created_at=db_user.created_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions (they already have proper status codes and CORS headers)
        raise
    except Exception as e:
        # Log the error and re-raise as HTTPException with CORS-friendly response
        import traceback
        error_detail = str(e)
        traceback_str = traceback.format_exc()
        print(f"❌ Registration error: {error_detail}", flush=True)
        print(f"Traceback: {traceback_str}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {error_detail}"
        )


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get current authenticated user from JWT token.
    Raises exception if token is missing or invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Token is required for authenticated endpoints
    if token is None:
        raise credentials_exception

    email = verify_token(token)
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        plan=current_user.plan,
        daily_voice_count=(current_user.daily_voice_count or 0) if hasattr(current_user, 'daily_voice_count') else 0,
        created_at=current_user.created_at
    )
