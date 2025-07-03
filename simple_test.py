#!/usr/bin/env python3
"""
Simple test to verify feedback submission works via direct API call
"""

import requests
import json

def test_simple_feedback():
    """Test basic feedback submission"""
    BASE_URL = "http://localhost:8001"
    
    print("🧪 Simple Feedback Test")
    print("=" * 40)
    
    # Login as guest
    guest_session = requests.Session()
    login_response = guest_session.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "guest_001", "password": "guest123"}
    )
    
    if login_response.status_code != 200:
        print("❌ Login failed:", login_response.text)
        return False
    
    print("✅ Logged in successfully")
    
    # Submit feedback
    feedback_data = {
        "category": "room_service",
        "rating": 2,
        "subject": "Test feedback",
        "comment": "This is a test feedback submission",
        "location": "Room 101",
        "staff_member": "Test Staff",
        "anonymous": False
    }
    
    feedback_response = guest_session.post(
        f"{BASE_URL}/api/feedback/submit",
        json=feedback_data
    )
    
    if feedback_response.status_code != 201:
        print("❌ Feedback submission failed:", feedback_response.text)
        return False
    
    result = feedback_response.json()
    print("✅ Feedback submitted successfully!")
    print(f"   Feedback ID: {result['feedback_id']}")
    print(f"   Alert triggered: {result['alert_triggered']}")
    print(f"   Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
    
    return True

if __name__ == "__main__":
    success = test_simple_feedback()
    if success:
        print("\n🎉 All tests passed! Feedback system is working.")
    else:
        print("\n❌ Tests failed!")
