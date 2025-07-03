from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class FeedbackCategory(str, Enum):
    GENERAL = "general"
    ROOM = "room"
    DINING = "dining"
    SERVICE = "service"
    AMENITIES = "amenities"
    ACTIVITIES = "activities"
    BUSINESS_SERVICES = "business_services"

class Feedback(BaseModel):
    feedback_id: str
    guest_id: str
    rating: int
    comment: str
    category: FeedbackCategory
    feedback_type: str = "review"
    source: str = "web"
    date: Optional[str] = None
    sentiment: Optional[Dict[str, Any]] = None

class SentimentAnalysis(BaseModel):
    score: float
    label: SentimentLabel
    confidence: float
    keywords: Optional[List[str]] = []
