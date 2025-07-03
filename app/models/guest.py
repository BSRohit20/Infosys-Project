from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class GuestType(str, Enum):
    BUSINESS = "business"
    LEISURE = "leisure"
    FAMILY = "family"
    COUPLE = "couple"
    GROUP = "group"

class PreferenceCategory(str, Enum):
    CUISINE = "cuisine"
    ACTIVITY_LEVEL = "activity_level"
    ROOM_TYPE = "room_type"
    AMENITIES = "amenities"

class Guest(BaseModel):
    guest_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    guest_type: Optional[GuestType] = GuestType.LEISURE
    loyalty_tier: str = "standard"
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    room_number: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = {}
    previous_stays: int = 0
    total_spent: float = 0.0
    created_at: Optional[str] = None
    last_updated: Optional[str] = None

class GuestPreference(BaseModel):
    guest_id: str
    category: PreferenceCategory
    preference_value: str
    confidence: float = 1.0
    source: str = "explicit"
