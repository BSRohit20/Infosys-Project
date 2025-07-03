from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any
from pydantic import BaseModel
import logging
from app.api.auth import require_admin
from app.services.auth_service import auth_service

logger = logging.getLogger(__name__)
router = APIRouter()

class GuestCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    loyalty_tier: str = "Standard"

@router.post("/add-guest")
async def add_guest(guest_data: GuestCreate, user = Depends(require_admin)):
    """Add a new guest user (admin only)"""
    logger.info(f"Attempting to create new guest: {guest_data.username}")
    
    # Check if username already exists
    for existing_user in auth_service.users_data:
        if existing_user.get('username') == guest_data.username.lower():
            logger.warning(f"Username '{guest_data.username}' is already taken")
            raise HTTPException(
                status_code=400, 
                detail=f"Username '{guest_data.username}' is already taken"
            )
    
    # Create the new user
    user_dict = guest_data.dict()
    user_dict['role'] = 'customer'  # Set the role to customer
    
    new_user = auth_service.create_user(user_dict)
    
    if not new_user:
        raise HTTPException(
            status_code=500,
            detail="Failed to create new guest account"
        )
        
    logger.info(f"✅ New guest account created: {new_user.username}")
    return {"success": True, "user": new_user}
