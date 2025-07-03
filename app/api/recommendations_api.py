from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Dict
import logging

from app.services.recommendation_service import recommendation_service
from app.api.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

@router.get("/guest/{guest_id}")
async def get_guest_recommendations(
    guest_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get personalized recommendations for a specific guest"""
    try:
        recommendations = await recommendation_service.get_personalized_recommendations(guest_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": recommendations
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting recommendations for guest {guest_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recommendations")

@router.get("/default")
async def get_default_recommendations(
    current_user: User = Depends(get_current_user)
):
    """Get default recommendations for new or unknown guests"""
    try:
        recommendations = recommendation_service._get_default_recommendations()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": recommendations
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting default recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get default recommendations")

@router.get("/dining")
async def get_dining_recommendations(
    guest_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get dining recommendations specifically"""
    try:
        if guest_id:
            recommendations = await recommendation_service.get_personalized_recommendations(guest_id)
            dining_recs = recommendations.get("dining", [])
        else:
            default_recs = recommendation_service._get_default_recommendations()
            dining_recs = default_recs.get("dining", [])
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "guest_id": guest_id,
                    "dining_recommendations": dining_recs
                }
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting dining recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dining recommendations")

@router.get("/activities")
async def get_activity_recommendations(
    guest_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get activity recommendations specifically"""
    try:
        if guest_id:
            recommendations = await recommendation_service.get_personalized_recommendations(guest_id)
            activity_recs = recommendations.get("activities", [])
        else:
            default_recs = recommendation_service._get_default_recommendations()
            activity_recs = default_recs.get("activities", [])
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "guest_id": guest_id,
                    "activity_recommendations": activity_recs
                }
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting activity recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get activity recommendations")

@router.get("/amenities")
async def get_amenity_recommendations(
    guest_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get amenity recommendations specifically"""
    try:
        if guest_id:
            recommendations = await recommendation_service.get_personalized_recommendations(guest_id)
            amenity_recs = recommendations.get("amenities", [])
        else:
            default_recs = recommendation_service._get_default_recommendations()
            amenity_recs = default_recs.get("amenities", [])
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "guest_id": guest_id,
                    "amenity_recommendations": amenity_recs
                }
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting amenity recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get amenity recommendations")
