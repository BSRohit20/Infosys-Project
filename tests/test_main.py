import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_redirect():
    """Test root endpoint redirects to login"""
    response = client.get("/", allow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["location"]

def test_login_page():
    """Test login page loads"""
    response = client.get("/login")
    assert response.status_code == 200
    assert "login" in response.text.lower()

@pytest.mark.asyncio
async def test_sentiment_analysis():
    """Test sentiment analysis service"""
    from app.services.sentiment_service import sentiment_service
    
    # Test positive sentiment
    result = await sentiment_service.analyze_sentiment("This hotel is amazing! Great service!")
    assert result["sentiment"] in ["positive", "negative", "neutral"]
    assert "confidence" in result
    assert 0 <= result["confidence"] <= 1

@pytest.mark.asyncio  
async def test_recommendation_service():
    """Test recommendation service"""
    from app.services.recommendation_service import recommendation_service
    
    # Test default recommendations
    recommendations = recommendation_service._get_default_recommendations()
    assert "dining" in recommendations
    assert "amenities" in recommendations
    assert "activities" in recommendations
    assert isinstance(recommendations["dining"], list)

def test_api_endpoints_require_auth():
    """Test that protected endpoints require authentication"""
    protected_endpoints = [
        "/api/feedback/submit",
        "/api/recommendations/guest/test",
        "/api/analytics/dashboard"
    ]
    
    for endpoint in protected_endpoints:
        if endpoint.startswith("/api/feedback/submit"):
            response = client.post(endpoint, data={"guest_id": "test", "rating": 5, "feedback_text": "test"})
        else:
            response = client.get(endpoint)
        
        # Should redirect to login or return 401/403
        assert response.status_code in [302, 401, 403]

if __name__ == "__main__":
    pytest.main([__file__])
