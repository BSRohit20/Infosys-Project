from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Dict, List
from pydantic import BaseModel
import logging
from datetime import datetime
import json
import os

from app.services.sentiment_service import sentiment_service
from app.services.recommendation_service import recommendation_service
from app.api.auth import require_auth, require_admin, require_staff
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

# Pydantic models for request validation
class FeedbackSubmission(BaseModel):
    category: str
    rating: int
    subject: str
    comment: str
    location: Optional[str] = None
    staff_member: Optional[str] = None
    anonymous: bool = False

# In-memory feedback storage (in production, use a database)
feedback_storage = []
admin_alerts = []

def save_feedback_to_file(feedback_record):
    """Save feedback to JSON file for persistence"""
    try:
        feedback_file = os.path.join(os.path.dirname(__file__), "../data/feedback_submissions.json")
        
        # Load existing feedback
        existing_feedback = []
        if os.path.exists(feedback_file):
            with open(feedback_file, 'r') as f:
                existing_feedback = json.load(f)
        
        # Add new feedback
        existing_feedback.append(feedback_record)
        
        # Save back to file
        with open(feedback_file, 'w') as f:
            json.dump(existing_feedback, f, indent=2)
            
        logger.info(f"💾 Feedback saved to file: {feedback_record['feedback_id']}")
    except Exception as e:
        logger.error(f"❌ Error saving feedback to file: {e}")

def create_admin_alert(feedback_record):
    """Create alert for admin dashboard"""
    rating = feedback_record["rating"]
    sentiment = feedback_record["sentiment_analysis"]["sentiment"]
    is_negative = feedback_record["sentiment_analysis"].get("is_negative", False)
    
    # Determine priority based on rating and sentiment
    if rating <= 2 or is_negative:
        priority = "high"
        priority_emoji = "🔴"
    elif rating == 3 or sentiment == "neutral":
        priority = "medium" 
        priority_emoji = "🟡"
    else:  # rating 4-5 with positive sentiment
        priority = "low"
        priority_emoji = "🟢"
    
    alert = {
        "alert_id": f"ALERT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        "type": "feedback",
        "priority": priority,
        "priority_emoji": priority_emoji,
        "title": f"New Feedback: {feedback_record['subject']}",
        "message": f"Guest {feedback_record['guest_name']} rated {rating}/5 stars",
        "feedback_id": feedback_record["feedback_id"],
        "guest_id": feedback_record["guest_id"],
        "guest_name": feedback_record["guest_name"],
        "sentiment": sentiment,
        "rating": rating,
        "category": feedback_record["category"],
        "created_at": datetime.utcnow().isoformat(),
        "status": "unread"
    }
    
    admin_alerts.insert(0, alert)  # Add to beginning for most recent first
    
    # Keep only last 50 alerts
    if len(admin_alerts) > 50:
        admin_alerts.pop()
    
    logger.info(f"🔔 Admin alert created: {alert['alert_id']} (Priority: {priority})")
    return alert

@router.post("/submit")
async def submit_feedback(
    feedback: FeedbackSubmission,
    current_user: User = Depends(require_auth)
):
    """Submit guest feedback with real-time sentiment analysis and admin alerts"""
    try:
        # Enhanced validation
        if not feedback.category or feedback.category.strip() == "":
            raise HTTPException(status_code=422, detail="Category is required")
        
        if not feedback.rating or not 1 <= feedback.rating <= 5:
            raise HTTPException(status_code=422, detail="Rating must be between 1 and 5")
        
        if not feedback.subject or feedback.subject.strip() == "":
            raise HTTPException(status_code=422, detail="Subject is required")
            
        if not feedback.comment or feedback.comment.strip() == "":
            raise HTTPException(status_code=422, detail="Comment is required")
        
        # Perform sentiment analysis
        sentiment_result = await sentiment_service.analyze_sentiment(feedback.comment)
        
        # Create feedback record
        feedback_record = {
            "feedback_id": f"FB_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "guest_id": current_user.user_id,
            "guest_name": f"{current_user.first_name} {current_user.last_name}",
            "guest_username": current_user.username,
            "rating": feedback.rating,
            "subject": feedback.subject,
            "comment": feedback.comment,
            "category": feedback.category,
            "location": feedback.location,
            "staff_member": feedback.staff_member,
            "anonymous": feedback.anonymous,
            "sentiment_analysis": sentiment_result,
            "submitted_at": datetime.utcnow().isoformat(),
            "status": "new"
        }
        
        # Store feedback
        feedback_storage.append(feedback_record)
        save_feedback_to_file(feedback_record)
        
        # Create admin alert for ALL feedback submissions
        # This ensures admins are aware of all guest feedback
        alert_created = True
        create_admin_alert(feedback_record)
        
        logger.info(f"📝 Feedback submitted: {feedback_record['feedback_id']} (Alert: {alert_created})")
        
        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "message": "Feedback submitted successfully",
                "feedback_id": feedback_record["feedback_id"],
                "sentiment": sentiment_result["sentiment"],
                "confidence": sentiment_result["confidence"],
                "alert_triggered": alert_created
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

@router.get("/my-feedback")
async def get_my_feedback(current_user: User = Depends(require_auth)):
    """Get current user's feedback history"""
    try:
        user_feedback = [
            fb for fb in feedback_storage 
            if fb["guest_id"] == current_user.user_id
        ]
        
        # Sort by most recent first
        user_feedback.sort(key=lambda x: x["submitted_at"], reverse=True)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "feedback": user_feedback,
                "total_count": len(user_feedback)
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error retrieving user feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve feedback")

@router.get("/guest/{guest_id}")
async def get_guest_feedback(
    guest_id: str,
    current_user: User = Depends(require_staff)
):
    """Get feedback for a specific guest (admin/staff only)"""
    try:
        guest_feedback = [
            fb for fb in feedback_storage 
            if fb["guest_id"] == guest_id
        ]
        
        # Sort by most recent first
        guest_feedback.sort(key=lambda x: x["submitted_at"], reverse=True)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "guest_id": guest_id,
                "feedback": guest_feedback,
                "total_count": len(guest_feedback),
                "average_rating": sum(fb["rating"] for fb in guest_feedback) / len(guest_feedback) if guest_feedback else 0
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error retrieving guest feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve guest feedback")

@router.get("/alerts")
async def get_admin_alerts(current_user: User = Depends(require_staff)):
    """Get feedback alerts for admin dashboard"""
    try:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "alerts": admin_alerts,
                "unread_count": len([a for a in admin_alerts if a["status"] == "unread"]),
                "total_count": len(admin_alerts)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error retrieving admin alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve alerts")

@router.post("/alerts/{alert_id}/mark-read")
async def mark_alert_read(
    alert_id: str,
    current_user: User = Depends(require_staff)
):
    """Mark an alert as read"""
    try:
        # Find and update alert
        for alert in admin_alerts:
            if alert["alert_id"] == alert_id:
                alert["status"] = "read"
                alert["read_at"] = datetime.utcnow().isoformat()
                alert["read_by"] = current_user.username
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "success": True,
                        "message": "Alert marked as read"
                    }
                )
        
        raise HTTPException(status_code=404, detail="Alert not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error marking alert as read: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark alert as read")

@router.get("/analyze")
async def analyze_text(
    text: str,
    current_user: User = Depends(require_auth)
):
    """Analyze sentiment of provided text"""
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        sentiment_result = await sentiment_service.analyze_sentiment(text)
        
        return JSONResponse(
            status_code=200,
            content={
                "text": text,
                "sentiment": sentiment_result["sentiment"],
                "confidence": sentiment_result["confidence"],
                "scores": sentiment_result["scores"],
                "is_negative": sentiment_result.get("is_negative", False)
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error analyzing sentiment: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze sentiment")

@router.post("/batch-analyze")
async def batch_analyze(
    texts: List[str],
    current_user: User = Depends(require_auth)
):
    """Analyze sentiment for multiple texts"""
    try:
        if not texts:
            raise HTTPException(status_code=400, detail="Text list cannot be empty")
        
        if len(texts) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 texts allowed per batch")
        
        results = await sentiment_service.analyze_batch(texts)
        
        return JSONResponse(
            status_code=200,
            content={
                "results": results,
                "total_analyzed": len(results),
                "negative_count": sum(1 for r in results if r.get("is_negative", False))
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error batch analyzing sentiment: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze sentiment batch")
