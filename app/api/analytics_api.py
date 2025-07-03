from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

from app.api.auth import require_admin
from app.models.user import User
from app.services.sentiment_service import sentiment_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_analytics_dashboard(
    current_user: User = Depends(require_admin)
):
    """Get comprehensive analytics dashboard data"""
    try:
        # Load feedback data for analysis
        feedback_data = _load_feedback_data()
        guest_data = _load_guest_data()
        
        # Calculate metrics
        total_guests = len(guest_data)
        total_feedback = len(feedback_data)
        
        # Sentiment analysis
        sentiment_breakdown = _calculate_sentiment_breakdown(feedback_data)
        
        # Rating analysis
        rating_breakdown = _calculate_rating_breakdown(feedback_data)
        
        # Recent alerts (negative sentiment)
        recent_alerts = _get_recent_alerts(feedback_data)
        
        # Guest satisfaction trends
        satisfaction_trends = _calculate_satisfaction_trends(feedback_data)
        
        # Loyalty tier distribution
        loyalty_distribution = _calculate_loyalty_distribution(guest_data)
        
        dashboard_data = {
            "overview": {
                "total_guests": total_guests,
                "total_feedback": total_feedback,
                "average_rating": rating_breakdown["average_rating"],
                "satisfaction_rate": sentiment_breakdown["positive_percentage"],
                "alert_count": len(recent_alerts)
            },
            "sentiment_analysis": sentiment_breakdown,
            "rating_breakdown": rating_breakdown,
            "recent_alerts": recent_alerts,
            "satisfaction_trends": satisfaction_trends,
            "loyalty_distribution": loyalty_distribution,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": dashboard_data
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error generating analytics dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate analytics dashboard")

@router.get("/sentiment-trends")
async def get_sentiment_trends(
    days: int = 30,
    current_user: User = Depends(require_admin)
):
    """Get sentiment trends over specified number of days"""
    try:
        feedback_data = _load_feedback_data()
        
        # Filter feedback by date range
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        recent_feedback = [
            f for f in feedback_data 
            if datetime.fromisoformat(f.get("submitted_at", f.get("date", "2024-01-01")).replace("Z", "")) > cutoff_date
        ]
        
        # Group by date and calculate sentiment trends
        trends = _calculate_daily_sentiment_trends(recent_feedback)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "period_days": days,
                    "total_feedback": len(recent_feedback),
                    "trends": trends
                }
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting sentiment trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to get sentiment trends")

@router.get("/alerts")
async def get_active_alerts(
    limit: int = 50,
    current_user: User = Depends(require_admin)
):
    """Get active alerts for negative sentiment and issues"""
    try:
        # Import feedback alerts from feedback API
        from app.api.feedback_api import admin_alerts
        
        # Get recent feedback alerts
        recent_alerts = admin_alerts[:limit]
        
        # Also get alerts from feedback data analysis
        feedback_data = _load_feedback_data()
        sentiment_alerts = _get_recent_alerts(feedback_data, limit=limit)
        
        # Combine and deduplicate alerts
        all_alerts = recent_alerts + sentiment_alerts
        
        # Sort by most recent and limit
        all_alerts.sort(key=lambda x: x.get("created_at", x.get("timestamp", "")), reverse=True)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "total_alerts": len(all_alerts[:limit]),
                    "unread_count": len([a for a in recent_alerts if a.get("status") == "unread"]),
                    "alerts": all_alerts[:limit]
                }
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alerts")

@router.get("/guest-insights/{guest_id}")
async def get_guest_insights(
    guest_id: str,
    current_user: User = Depends(require_admin)
):
    """Get detailed insights for a specific guest"""
    try:
        feedback_data = _load_feedback_data()
        guest_data = _load_guest_data()
        
        # Find guest
        guest = next((g for g in guest_data if g.get("guest_id") == guest_id), None)
        if not guest:
            raise HTTPException(status_code=404, detail="Guest not found")
        
        # Get guest's feedback
        guest_feedback = [f for f in feedback_data if f.get("guest_id") == guest_id]
        
        # Calculate insights
        insights = {
            "guest_profile": guest,
            "feedback_history": guest_feedback,
            "total_feedback": len(guest_feedback),
            "average_rating": sum(f.get("rating", 0) for f in guest_feedback) / len(guest_feedback) if guest_feedback else 0,
            "sentiment_summary": _calculate_sentiment_breakdown(guest_feedback),
            "preference_analysis": _analyze_guest_preferences(guest, guest_feedback),
            "recommendations_effectiveness": _analyze_recommendation_effectiveness(guest_id, guest_feedback)
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": insights
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting guest insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to get guest insights")

def _load_feedback_data() -> List[Dict]:
    """Load feedback data from JSON file"""
    try:
        # Load from the actual feedback submissions file
        feedback_file = os.path.join(os.path.dirname(__file__), "../data/feedback_submissions.json")
        with open(feedback_file, 'r') as f:
            data = json.load(f)
            # Return the data directly as it's an array of feedback objects
            feedback_data = data if isinstance(data, list) else []
            
            # If no feedback data found, generate sample data
            if not feedback_data:
                logger.warning("No feedback data found, generating sample data")
                feedback_data = _generate_sample_feedback_data()
                
            return feedback_data
    except FileNotFoundError:
        logger.warning("Feedback submissions file not found, generating sample data")
        return _generate_sample_feedback_data()
    except Exception as e:
        logger.error(f"Error loading feedback data: {e}")
        return _generate_sample_feedback_data()

def _generate_sample_feedback_data() -> List[Dict]:
    """Generate sample feedback data for testing"""
    current_time = datetime.utcnow().isoformat()
    yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat()
    
    return [
        {
            "feedback_id": "FB_SAMPLE_001",
            "guest_id": "guest_001",
            "guest_name": "Emily Johnson",
            "guest_username": "guest_001",
            "rating": 5,
            "subject": "Outstanding service from the team",
            "comment": "The staff was incredibly helpful and friendly. They went above and beyond to make our stay memorable. Thank you!",
            "category": "staff_service",
            "location": "Front Desk",
            "staff_member": "Sarah Johnson",
            "sentiment_analysis": {
                "text": "The staff was incredibly helpful and friendly. They went above and beyond to make our stay memorable. Thank you!",
                "sentiment": "positive",
                "confidence": 0.95,
                "is_negative": False
            },
            "submitted_at": current_time
        },
        {
            "feedback_id": "FB_SAMPLE_002",
            "guest_id": "guest_002",
            "guest_name": "Robert Smith",
            "guest_username": "guest_002",
            "rating": 2,
            "subject": "Room cleanliness issues",
            "comment": "The room was not properly cleaned when we arrived. The bathroom had stains and the bed sheets looked used.",
            "category": "cleanliness",
            "location": "Room 305",
            "sentiment_analysis": {
                "text": "The room was not properly cleaned when we arrived. The bathroom had stains and the bed sheets looked used.",
                "sentiment": "negative",
                "confidence": 0.92,
                "is_negative": True
            },
            "submitted_at": yesterday
        },
        {
            "feedback_id": "FB_SAMPLE_003",
            "guest_id": "guest_003",
            "guest_name": "Maria Garcia",
            "guest_username": "guest_003",
            "rating": 3,
            "subject": "Average experience overall",
            "comment": "The hotel was okay. Nothing special but nothing terrible either. Breakfast was decent.",
            "category": "general",
            "sentiment_analysis": {
                "text": "The hotel was okay. Nothing special but nothing terrible either. Breakfast was decent.",
                "sentiment": "neutral",
                "confidence": 0.85,
                "is_negative": False
            },
            "submitted_at": current_time
        }
    ]

def _load_guest_data() -> List[Dict]:
    """Load guest data from JSON file"""
    try:
        # Try to load from users.json first (more likely to exist)
        users_file = os.path.join(os.path.dirname(__file__), "../data/users.json")
        if os.path.exists(users_file):
            with open(users_file, 'r') as f:
                users_data = json.load(f)
                if isinstance(users_data, list) and len(users_data) > 0:
                    # Convert users to guest format
                    guests = []
                    for user in users_data:
                        if user.get('role') == 'guest':
                            guests.append({
                                'guest_id': user.get('user_id'),
                                'username': user.get('username'),
                                'first_name': user.get('first_name'),
                                'last_name': user.get('last_name'),
                                'email': user.get('email', ''),
                                'loyalty_tier': user.get('loyalty_tier', 'Standard')
                            })
                    if guests:
                        return guests
        
        # If users.json didn't work, try comprehensive_guests_data.json
        guest_file = os.path.join(os.path.dirname(__file__), "../data/comprehensive_guests_data.json")
        if os.path.exists(guest_file):
            with open(guest_file, 'r') as f:
                data = json.load(f)
                guests = data.get('guests', []) if isinstance(data, dict) else data if isinstance(data, list) else []
                if guests:
                    return guests
        
        # If no data found, generate sample data
        logger.warning("No guest data found, generating sample data")
        return _generate_sample_guest_data()
    except FileNotFoundError:
        logger.warning("Guest data files not found")
        return _generate_sample_guest_data()
    except Exception as e:
        logger.error(f"Error loading guest data: {e}")
        return _generate_sample_guest_data()

def _generate_sample_guest_data() -> List[Dict]:
    """Generate sample guest data for testing"""
    return [
        {
            "guest_id": "guest_001",
            "username": "emilyjohnson",
            "first_name": "Emily",
            "last_name": "Johnson",
            "email": "emily.johnson@example.com",
            "loyalty_tier": "Gold"
        },
        {
            "guest_id": "guest_002",
            "username": "robertsmith",
            "first_name": "Robert",
            "last_name": "Smith",
            "email": "robert.smith@example.com",
            "loyalty_tier": "Silver"
        },
        {
            "guest_id": "guest_003",
            "username": "mariagarcia",
            "first_name": "Maria",
            "last_name": "Garcia",
            "email": "maria.garcia@example.com",
            "loyalty_tier": "Standard"
        },
        {
            "guest_id": "guest_004",
            "username": "davidlee",
            "first_name": "David",
            "last_name": "Lee",
            "email": "david.lee@example.com",
            "loyalty_tier": "Platinum"
        },
        {
            "guest_id": "guest_005",
            "username": "sarahwilson",
            "first_name": "Sarah",
            "last_name": "Wilson",
            "email": "sarah.wilson@example.com",
            "loyalty_tier": "Gold"
        }
    ]

def _calculate_sentiment_breakdown(feedback_data: List[Dict]) -> Dict:
    """Calculate sentiment breakdown from feedback data"""
    if not feedback_data:
        return {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "positive_percentage": 0,
            "negative_percentage": 0,
            "neutral_percentage": 0
        }
    
    # Count sentiments from sentiment_analysis field
    positive = 0
    negative = 0
    neutral = 0
    
    for f in feedback_data:
        sentiment_data = f.get("sentiment_analysis", {})
        sentiment = sentiment_data.get("sentiment", "").lower()
        
        if sentiment == "positive":
            positive += 1
        elif sentiment == "negative":
            negative += 1
        else:
            neutral += 1
    
    total = len(feedback_data)
    
    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_percentage": round((positive / total) * 100, 1) if total > 0 else 0,
        "negative_percentage": round((negative / total) * 100, 1) if total > 0 else 0,
        "neutral_percentage": round((neutral / total) * 100, 1) if total > 0 else 0
    }

def _calculate_rating_breakdown(feedback_data: List[Dict]) -> Dict:
    """Calculate rating breakdown from feedback data"""
    if not feedback_data:
        return {
            "average_rating": 0,
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
    
    ratings = [f.get("rating", 0) for f in feedback_data if f.get("rating")]
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    
    rating_distribution = {i: 0 for i in range(1, 6)}
    for rating in ratings:
        if 1 <= rating <= 5:
            rating_distribution[rating] += 1
    
    return {
        "average_rating": round(average_rating, 2),
        "rating_distribution": rating_distribution
    }

def _get_recent_alerts(feedback_data: List[Dict], limit: int = 10) -> List[Dict]:
    """Get recent alerts for negative sentiment"""
    alerts = []
    
    for feedback in feedback_data:
        sentiment_analysis = feedback.get("sentiment_analysis", {})
        sentiment = sentiment_analysis.get("sentiment", "").lower()
        confidence = sentiment_analysis.get("confidence", 0)
        rating = feedback.get("rating", 3)
        
        # Create alerts for negative sentiment or low ratings
        if sentiment == "negative" or rating <= 2:
            # Determine priority
            if rating <= 2 or sentiment == "negative":
                priority = "high"
                priority_emoji = "🔴"
            elif rating == 3 or sentiment == "neutral":
                priority = "medium"
                priority_emoji = "🟡"
            else:
                priority = "low"
                priority_emoji = "🟢"
            
            alert = {
                "alert_id": f"ALERT_{feedback.get('feedback_id', 'unknown')}",
                "type": "feedback",
                "priority": priority,
                "priority_emoji": priority_emoji,
                "title": f"Feedback Alert: {feedback.get('subject', 'No subject')}",
                "message": feedback.get("comment", "")[:150] + ("..." if len(feedback.get("comment", "")) > 150 else ""),
                "feedback_id": feedback.get("feedback_id", ""),
                "guest_id": feedback.get("guest_id", ""),
                "guest_name": feedback.get("guest_name", "Unknown"),
                "sentiment": sentiment,
                "rating": rating,
                "confidence": confidence,
                "category": feedback.get("category", "general"),
                "created_at": feedback.get("submitted_at", datetime.utcnow().isoformat()),
                "status": "unread"
            }
            alerts.append(alert)
    
    # Sort by timestamp (most recent first) and limit
    alerts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return alerts[:limit]

def _calculate_satisfaction_trends(feedback_data: List[Dict]) -> List[Dict]:
    """Calculate satisfaction trends over time"""
    # Group feedback by date and calculate average satisfaction
    trends = []
    
    # Get last 7 days of data
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # Filter feedback for this day
        day_feedback = [
            f for f in feedback_data 
            if f.get("submitted_at", "").startswith(date_str)
        ]
        
        if day_feedback:
            # Calculate average rating
            avg_rating = sum(f.get("rating", 0) for f in day_feedback) / len(day_feedback)
            
            # Calculate positive sentiment percentage
            positive_sentiment = sum(1 for f in day_feedback 
                                   if f.get("sentiment_analysis", {}).get("sentiment", "").lower() == "positive")
            satisfaction_rate = (positive_sentiment / len(day_feedback)) * 100
        else:
            avg_rating = 0
            satisfaction_rate = 0
        
        # Format date for display (e.g., "Jul 2")
        display_date = date.strftime("%b %d")
        
        trends.append({
            "date": date_str,
            "display_date": display_date,
            "average_rating": round(avg_rating, 2),
            "satisfaction_rate": round(satisfaction_rate, 1),
            "feedback_count": len(day_feedback)
        })
    
    return list(reversed(trends))  # Most recent last

def _calculate_loyalty_distribution(guest_data: List[Dict]) -> Dict:
    """Calculate distribution of guests by loyalty tier"""
    if not guest_data:
        return {
            "tiers": [],
            "total_guests": 0
        }
    
    # Default tiers if none defined
    default_tiers = ["Bronze", "Silver", "Gold", "Platinum", "Diamond"]
    
    tiers = {}
    for guest in guest_data:
        tier = guest.get("loyalty_tier", "Standard")
        tiers[tier] = tiers.get(tier, 0) + 1
    
    # If no tiers found in data, create sample data
    if not tiers:
        tiers = {
            "Standard": len(guest_data) // 3,
            "Silver": len(guest_data) // 3,
            "Gold": len(guest_data) - (len(guest_data) // 3) * 2
        }
    
    # Format for chart display
    tier_data = []
    for tier, count in tiers.items():
        tier_data.append({
            "name": tier,
            "count": count,
            "percentage": round((count / len(guest_data)) * 100, 1)
        })
    
    return {
        "tiers": tier_data,
        "total_guests": len(guest_data)
    }
    
    return tiers

def _analyze_guest_preferences(guest: Dict, feedback_history: List[Dict]) -> Dict:
    """Analyze guest preferences based on profile and feedback"""
    preferences = guest.get("preferences", {})
    
    # Analyze feedback topics
    feedback_topics = {}
    for feedback in feedback_history:
        category = feedback.get("category", "general")
        feedback_topics[category] = feedback_topics.get(category, 0) + 1
    
    return {
        "stated_preferences": preferences,
        "feedback_topics": feedback_topics,
        "most_discussed_topic": max(feedback_topics.keys(), key=feedback_topics.get) if feedback_topics else None
    }

def _analyze_recommendation_effectiveness(guest_id: str, feedback_history: List[Dict]) -> Dict:
    """Analyze effectiveness of recommendations for the guest"""
    # This would analyze if recommendations led to positive feedback
    # Simplified implementation
    
    recent_feedback = feedback_history[-3:] if len(feedback_history) >= 3 else feedback_history
    
    if not recent_feedback:
        return {"effectiveness_score": 0, "sample_size": 0}
    
    positive_feedback = sum(1 for f in recent_feedback if f.get("rating", 0) >= 4)
    effectiveness_score = (positive_feedback / len(recent_feedback)) * 100
    
    return {
        "effectiveness_score": round(effectiveness_score, 1),
        "sample_size": len(recent_feedback),
        "recent_positive_feedback": positive_feedback
    }

def _calculate_daily_sentiment_trends(feedback_data: List[Dict]) -> List[Dict]:
    """Calculate daily sentiment trends"""
    daily_trends = {}
    
    for feedback in feedback_data:
        date = feedback.get("date", feedback.get("submitted_at", "")).split("T")[0]
        if date not in daily_trends:
            daily_trends[date] = {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
        
        sentiment = feedback.get("sentiment", {}).get("label", "").upper()
        if sentiment == "POSITIVE":
            daily_trends[date]["positive"] += 1
        elif sentiment == "NEGATIVE":
            daily_trends[date]["negative"] += 1
        else:
            daily_trends[date]["neutral"] += 1
        
        daily_trends[date]["total"] += 1
    
    # Convert to list and calculate percentages
    trends = []
    for date, data in sorted(daily_trends.items()):
        total = data["total"]
        trends.append({
            "date": date,
            "positive_percentage": round((data["positive"] / total) * 100, 1) if total > 0 else 0,
            "negative_percentage": round((data["negative"] / total) * 100, 1) if total > 0 else 0,
            "neutral_percentage": round((data["neutral"] / total) * 100, 1) if total > 0 else 0,
            "total_feedback": total
        })
    
    return trends
