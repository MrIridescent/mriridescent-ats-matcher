from fastapi import APIRouter, HTTPException, Depends, Response, Cookie, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from ..models.database import get_db
from ..models.user_models import User
from ..config import settings
from ..utils.security import create_access_token, verify_password

router = APIRouter(prefix="/api/users", tags=["Users"])

class UserLogin(BaseModel):
    username: str
    password: str

async def get_current_user_from_token(
    session_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
) -> User:
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = jwt.decode(
            session_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
        )
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    return user

@router.post("/login")
async def login_user(
    login_data: UserLogin, 
    response: Response, 
    db: Session = Depends(get_db)
):
    """Login user and create session using JWT"""
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not user.check_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="session_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite='lax',
        secure=not settings.DEBUG  # Only send over HTTPS in production
    )
    
    return {
        "status": "success",
        "message": "Login successful",
        "user": user.to_dict(),
        "session_token": access_token
    }

@router.post("/logout")
async def logout_user(response: Response):
    """Logout user and clear session cookie"""
    response.delete_cookie("session_token")
    return {"status": "success", "message": "Logged out successfully"}

@router.get("/current")
async def get_current_user(user: User = Depends(get_current_user_from_token)):
    """Get the current authenticated user"""
    return {
        "status": "success",
        "user": user.to_dict()
    }

@router.get("/validate")
async def validate_session(session_token: Optional[str] = Cookie(None)):
    """Validating session status without throwing exceptions"""
    if not session_token:
        return {"status": "invalid", "authenticated": False}
    
    try:
        payload = jwt.decode(
            session_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return {
            "status": "valid",
            "authenticated": True,
            "username": payload.get("sub")
        }
    except JWTError:
        return {"status": "expired", "authenticated": False}

def get_current_user_from_session(session_token: Optional[str], db: Session) -> Optional[User]:
    """Helper function for non-async contexts"""
    if not session_token:
        return None
    try:
        payload = jwt.decode(
            session_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        return db.query(User).filter(User.username == username).first()
    except:
        return None
