from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.responses import RedirectResponse
from app.models.user import UserLogin, User
from app.services.auth_service import auth_service
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def get_current_user(request: Request) -> Optional[User]:
    """Get current user from session"""
    session_token = request.cookies.get('session_token')
    logger.info(f"🔍 Checking session token: {session_token}")
    if session_token:
        user = auth_service.get_user_from_session(session_token)
        logger.info(f"🔍 User from session: {user.username if user else 'None'}")
        return user
    logger.info("🔍 No session token found in cookies")
    return None

def require_auth(request: Request) -> User:
    """Require authentication - redirect to login if not authenticated"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def require_admin(request: Request) -> User:
    """Require admin role"""
    user = require_auth(request)
    if not auth_service.is_admin(user):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_staff(request: Request) -> User:
    """Require staff or admin role"""
    user = require_auth(request)
    if not auth_service.is_staff(user):
        raise HTTPException(status_code=403, detail="Staff access required")
    return user

@router.post("/login")
async def login(user_login: UserLogin, response: Response):
    """Login endpoint"""
    user = auth_service.authenticate_user(user_login.username, user_login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    session = auth_service.create_session(user)
    
    # Set session cookie with localhost-compatible settings
    response.set_cookie(
        key="session_token",
        value=session.session_token,
        max_age=86400,  # 24 hours
        path="/",       # Explicitly set path
        httponly=False, # Allow JavaScript access
        secure=False,   # Allow on HTTP for local development
        samesite="lax"  # More compatible than "none" for localhost
    )
    
    logger.info(f"🍪 Setting cookie for user {user.username}: {session.session_token[:20]}...")
    
    return {
        "message": "Login successful",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }

@router.post("/logout")
async def logout(request: Request, response: Response):
    """Logout endpoint"""
    session_token = request.cookies.get('session_token')
    if session_token:
        auth_service.logout_user(session_token)
    
    response.delete_cookie("session_token")
    return {"message": "Logout successful"}

@router.get("/status")
async def auth_status(request: Request):
    """Check authentication status"""
    user = get_current_user(request)
    if user:
        return {
            "authenticated": True,
            "user": {
                "user_id": user.user_id,
                "username": user.username,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }
    else:
        return {"authenticated": False}

@router.get("/me")
async def get_current_user_info(user: User = Depends(require_auth)):
    """Get current user information"""
    user_info = {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }
    
    # Add customer-specific info if customer
    if auth_service.is_customer(user):
        customer_profile = auth_service.get_customer_profile(user.user_id)
        if customer_profile:
            user_info.update({
                "guest_id": customer_profile.guest_id,
                "loyalty_number": customer_profile.loyalty_number,
                "preferences": customer_profile.preferences
            })
    
    return user_info
