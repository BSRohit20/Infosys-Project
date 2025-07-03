from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    GUEST = "guest"
    CUSTOMER = "customer"

class User(BaseModel):
    user_id: str
    username: str
    email: str
    role: UserRole
    first_name: str
    last_name: str
    created_at: Optional[str] = None
    last_login: Optional[str] = None
    is_active: bool = True

class UserLogin(BaseModel):
    username: str
    password: str

class UserSession(BaseModel):
    user_id: str
    username: str
    role: str
    session_token: str
    expires_at: datetime
    created_at: Optional[datetime] = None

class CustomerProfile(BaseModel):
    user_id: str
    preferences: Optional[Dict[str, Any]] = {}
    loyalty_tier: Optional[str] = "standard"
    total_spent: Optional[float] = 0.0
    visit_count: Optional[int] = 0
