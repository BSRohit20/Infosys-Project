import json
import os
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import logging

from app.models.guest import Guest, GuestType, PreferenceCategory
from app.models.feedback import Feedback, SentimentLabel

logger = logging.getLogger(__name__)

class CRMService:
    """
    Service for managing Customer Relationship Management data
    """
    
    def __init__(self, data_path: str = "app/data"):
        """
        Initialize CRM service with data file paths
        """
        self.data_path = data_path
        self.guests_file = os.path.join(data_path, "comprehensive_guests_data.json")
        self.feedback_file = os.path.join(data_path, "comprehensive_feedback_data.json")
        self._guests_cache = {}
        self._feedback_cache = {}
        self._load_data()
    
    def _load_data(self):
        """
        Load CRM data from JSON files
        """
        try:
            # Load guests data
            logger.info(f"Looking for guests file at: {self.guests_file}")
            logger.info(f"File exists: {os.path.exists(self.guests_file)}")
            if os.path.exists(self.guests_file):
                with open(self.guests_file, 'r', encoding='utf-8') as f:
                    guests_data = json.load(f)
                    self._guests_cache = {guest['guest_id']: guest for guest in guests_data.get('guests', [])}
                    logger.info(f"Loaded {len(self._guests_cache)} guests from comprehensive data")
            else:
                self._guests_cache = {}
                self._create_sample_guests_data()
                logger.info("Created sample guests data")
            
            # Load feedback data
            logger.info(f"Looking for feedback file at: {self.feedback_file}")
            logger.info(f"File exists: {os.path.exists(self.feedback_file)}")
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    feedback_data = json.load(f)
                    self._feedback_cache = {fb['feedback_id']: fb for fb in feedback_data.get('feedback', [])}
                    logger.info(f"Loaded {len(self._feedback_cache)} feedback records from comprehensive data")
            else:
                self._feedback_cache = {}
                self._create_sample_feedback_data()
                logger.info("Created sample feedback data")
                
            logger.info(f"Loaded {len(self._guests_cache)} guests and {len(self._feedback_cache)} feedback items")
            
        except Exception as e:
            logger.error(f"Error loading CRM data: {str(e)}")
            self._guests_cache = {}
            self._feedback_cache = {}
    
    def _create_sample_guests_data(self):
        """
        Create sample guests data for demonstration
        """
        sample_guests = [
            {
                "guest_id": "G001",
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@email.com",
                "phone": "+1-555-0123",
                "guest_type": "business",
                "loyalty_tier": "Gold",
                "preferences": {
                    "dining": ["italian", "vegetarian", "wine"],
                    "amenities": ["spa", "gym", "business_center"],
                    "activities": ["golf", "tennis"],
                    "room_type": ["suite", "high_floor", "city_view"]
                },
                "stay_history": [
                    {"date": "2024-06-15", "nights": 3, "room_type": "deluxe", "total_spent": 1200},
                    {"date": "2024-08-20", "nights": 2, "room_type": "suite", "total_spent": 800}
                ],
                "total_stays": 15,
                "average_rating": 4.2,
                "created_at": "2023-01-15T10:00:00",
                "last_updated": "2024-08-20T14:30:00"
            },
            {
                "guest_id": "G002",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.johnson@email.com",
                "phone": "+1-555-0456",
                "guest_type": "leisure",
                "loyalty_tier": "Silver",
                "preferences": {
                    "dining": ["seafood", "local_cuisine", "cocktails"],
                    "amenities": ["pool", "spa", "concierge"],
                    "activities": ["shopping", "sightseeing", "beach"],
                    "room_type": ["ocean_view", "balcony"]
                },
                "stay_history": [
                    {"date": "2024-07-10", "nights": 5, "room_type": "ocean_view", "total_spent": 2500}
                ],
                "total_stays": 8,
                "average_rating": 4.8,
                "created_at": "2023-03-20T09:15:00",
                "last_updated": "2024-07-15T11:45:00"
            },
            {
                "guest_id": "G003",
                "first_name": "Michael",
                "last_name": "Chen",
                "email": "michael.chen@email.com",
                "phone": "+1-555-0789",
                "guest_type": "family",
                "loyalty_tier": "Bronze",
                "preferences": {
                    "dining": ["family_friendly", "kids_menu", "buffet"],
                    "amenities": ["kids_club", "pool", "playground"],
                    "activities": ["family_activities", "entertainment"],
                    "room_type": ["family_suite", "connecting_rooms"]
                },
                "stay_history": [
                    {"date": "2024-06-01", "nights": 7, "room_type": "family_suite", "total_spent": 3200}
                ],
                "total_stays": 3,
                "average_rating": 4.0,
                "created_at": "2024-01-10T16:20:00",
                "last_updated": "2024-06-08T10:30:00"
            },
            {
                "guest_id": "G004",
                "first_name": "Emily",
                "last_name": "Williams",
                "email": "emily.williams@email.com",
                "phone": "+1-555-0321",
                "guest_type": "vip",
                "loyalty_tier": "Platinum",
                "preferences": {
                    "dining": ["fine_dining", "chef_table", "wine_pairing"],
                    "amenities": ["butler_service", "private_pool", "spa"],
                    "activities": ["exclusive_tours", "private_dining"],
                    "room_type": ["presidential_suite", "penthouse"]
                },
                "stay_history": [
                    {"date": "2024-05-15", "nights": 4, "room_type": "presidential_suite", "total_spent": 8000},
                    {"date": "2024-07-20", "nights": 3, "room_type": "penthouse", "total_spent": 12000}
                ],
                "total_stays": 25,
                "average_rating": 4.9,
                "created_at": "2022-06-01T12:00:00",
                "last_updated": "2024-07-23T15:45:00"
            }
        ]
        
        self._guests_cache = {guest['guest_id']: guest for guest in sample_guests}
        self._save_guests_data()
    
    def _create_sample_feedback_data(self):
        """
        Create sample feedback data for demonstration
        """
        sample_feedback = [
            {
                "feedback_id": "F001",
                "guest_id": "G001",
                "feedback_type": "review",
                "source": "mobile_app",
                "content": "Great stay! The staff was very professional and the room was clean. The business center had everything I needed.",
                "rating": 4,
                "category": "service",
                "sentiment_score": 0.8,
                "sentiment_label": "POSITIVE",
                "confidence_score": 0.92,
                "keywords": ["staff", "professional", "clean", "business"],
                "action_required": False,
                "acknowledged": True,
                "resolved": True,
                "created_at": "2024-08-22T10:30:00",
                "processed_at": "2024-08-22T10:31:00"
            },
            {
                "feedback_id": "F002",
                "guest_id": "G002",
                "content": "The ocean view was absolutely stunning! Loved the spa treatments and the seafood restaurant was amazing.",
                "feedback_type": "compliment",
                "source": "website",
                "rating": 5,
                "category": "amenities",
                "sentiment_score": 0.95,
                "sentiment_label": "POSITIVE",
                "confidence_score": 0.98,
                "keywords": ["ocean", "view", "spa", "seafood", "amazing"],
                "action_required": False,
                "acknowledged": True,
                "resolved": True,
                "created_at": "2024-07-15T14:20:00",
                "processed_at": "2024-07-15T14:21:00"
            },
            {
                "feedback_id": "F003",
                "guest_id": "G003",
                "feedback_type": "complaint",
                "source": "in_person",
                "content": "The kids club was closed during our stay and we weren't informed. The room was also quite noisy.",
                "rating": 2,
                "category": "amenities",
                "sentiment_score": -0.7,
                "sentiment_label": "NEGATIVE",
                "confidence_score": 0.85,
                "keywords": ["kids", "club", "closed", "noisy", "room"],
                "action_required": True,
                "acknowledged": True,
                "resolved": False,
                "created_at": "2024-06-05T09:15:00",
                "processed_at": "2024-06-05T09:16:00"
            },
            {
                "feedback_id": "F004",
                "guest_id": "G004",
                "feedback_type": "review",
                "source": "email",
                "content": "As always, exceptional service. The butler was attentive and the private dining experience was unforgettable.",
                "rating": 5,
                "category": "service",
                "sentiment_score": 0.9,
                "sentiment_label": "POSITIVE",
                "confidence_score": 0.95,
                "keywords": ["exceptional", "service", "butler", "private", "dining"],
                "action_required": False,
                "acknowledged": True,
                "resolved": True,
                "created_at": "2024-07-23T16:45:00",
                "processed_at": "2024-07-23T16:46:00"
            }
        ]
        
        self._feedback_cache = {fb['feedback_id']: fb for fb in sample_feedback}
        self._save_feedback_data()
    
    def _save_guests_data(self):
        """
        Save guests data to JSON file
        """
        try:
            os.makedirs(self.data_path, exist_ok=True)
            with open(self.guests_file, 'w', encoding='utf-8') as f:
                json.dump({"guests": list(self._guests_cache.values())}, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving guests data: {str(e)}")
    
    def _save_feedback_data(self):
        """
        Save feedback data to JSON file
        """
        try:
            os.makedirs(self.data_path, exist_ok=True)
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump({"feedback": list(self._feedback_cache.values())}, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving feedback data: {str(e)}")
    
    # Guest management methods
    def get_all_guests(self) -> List[Dict[str, Any]]:
        """Get all guests"""
        return list(self._guests_cache.values())
    
    def get_guest(self, guest_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific guest by ID"""
        return self._guests_cache.get(guest_id)
    
    def create_guest(self, guest_data: Dict[str, Any]) -> str:
        """Create a new guest"""
        guest_id = f"G{len(self._guests_cache) + 1:03d}"
        guest_data['guest_id'] = guest_id
        guest_data['created_at'] = datetime.now().isoformat()
        guest_data['last_updated'] = datetime.now().isoformat()
        
        self._guests_cache[guest_id] = guest_data
        self._save_guests_data()
        return guest_id
    
    def update_guest(self, guest_id: str, update_data: Dict[str, Any]) -> bool:
        """Update an existing guest"""
        if guest_id not in self._guests_cache:
            return False
        
        update_data['last_updated'] = datetime.now().isoformat()
        self._guests_cache[guest_id].update(update_data)
        self._save_guests_data()
        return True
    
    # Feedback management methods
    def get_guest_feedback(self, guest_id: str) -> List[Dict[str, Any]]:
        """Get all feedback for a specific guest"""
        return [fb for fb in self._feedback_cache.values() if fb.get('guest_id') == guest_id]
    
    def get_recent_feedback(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent feedback within specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_feedback = []
        
        for fb in self._feedback_cache.values():
            try:
                fb_date = datetime.fromisoformat(fb.get('created_at', ''))
                if fb_date >= cutoff_date:
                    recent_feedback.append(fb)
            except ValueError:
                continue
        
        return sorted(recent_feedback, key=lambda x: x.get('created_at', ''), reverse=True)
    
    def add_feedback(self, feedback_data: Dict[str, Any]) -> str:
        """Add new feedback"""
        feedback_id = f"F{len(self._feedback_cache) + 1:03d}"
        feedback_data['feedback_id'] = feedback_id
        feedback_data['created_at'] = datetime.now().isoformat()
        
        self._feedback_cache[feedback_id] = feedback_data
        self._save_feedback_data()
        return feedback_id
    
    def update_feedback(self, feedback_id: str, update_data: Dict[str, Any]) -> bool:
        """Update existing feedback"""
        if feedback_id not in self._feedback_cache:
            return False
        
        self._feedback_cache[feedback_id].update(update_data)
        self._save_feedback_data()
        return True
    
    def get_feedback_by_guest(self, guest_id: str, days: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get feedback for a specific guest, optionally within specified days"""
        guest_feedback = [fb for fb in self._feedback_cache.values() if fb.get('guest_id') == guest_id]
        
        if days is not None:
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_feedback = []
            
            for fb in guest_feedback:
                try:
                    fb_date = datetime.fromisoformat(fb.get('created_at', ''))
                    if fb_date >= cutoff_date:
                        filtered_feedback.append(fb)
                except ValueError:
                    continue
            
            guest_feedback = filtered_feedback
        
        return sorted(guest_feedback, key=lambda x: x.get('created_at', ''), reverse=True)

    # Analytics methods
    def get_guest_stats(self, guest_id: str) -> Dict[str, Any]:
        """Get comprehensive stats for a guest"""
        guest = self.get_guest(guest_id)
        if not guest:
            return {}
        
        feedback = self.get_guest_feedback(guest_id)
        
        # Calculate sentiment statistics
        sentiment_scores = [fb.get('sentiment_score', 0) for fb in feedback if fb.get('sentiment_score') is not None]
        
        stats = {
            "guest_info": guest,
            "total_feedback": len(feedback),
            "average_sentiment": sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0,
            "positive_feedback": len([fb for fb in feedback if fb.get('sentiment_label') == 'POSITIVE']),
            "negative_feedback": len([fb for fb in feedback if fb.get('sentiment_label') == 'NEGATIVE']),
            "total_stays": guest.get('total_stays', 0),
            "loyalty_tier": guest.get('loyalty_tier', 'Bronze'),
            "last_stay": max([stay.get('date', '') for stay in guest.get('stay_history', [])]) if guest.get('stay_history') else None
        }
        
        return stats
    
    def get_system_analytics(self) -> Dict[str, Any]:
        """Get overall system analytics"""
        all_feedback = list(self._feedback_cache.values())
        all_guests = list(self._guests_cache.values())
        
        # Sentiment distribution
        positive_count = len([fb for fb in all_feedback if fb.get('sentiment_label') == 'POSITIVE'])
        negative_count = len([fb for fb in all_feedback if fb.get('sentiment_label') == 'NEGATIVE'])
        neutral_count = len(all_feedback) - positive_count - negative_count
        
        # Guest type distribution
        guest_types = {}
        for guest in all_guests:
            guest_type = guest.get('guest_type', 'unknown')
            guest_types[guest_type] = guest_types.get(guest_type, 0) + 1
        
        return {
            "total_guests": len(all_guests),
            "total_feedback": len(all_feedback),
            "sentiment_distribution": {
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count
            },
            "guest_type_distribution": guest_types,
            "alerts_pending": len([fb for fb in all_feedback if fb.get('action_required', False) and not fb.get('resolved', False)])
        }
