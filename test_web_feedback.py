#!/usr/bin/env python3
"""
Test the feedback submission through the browser-like interface
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_web_interface_simulation():
    """Simulate web interface feedback submission"""
    session = requests.Session()
    
    print("🌐 Testing Web Interface Feedback Submission...")
    print("=" * 50)
    
    # Step 1: Login as user via API (like the web would)
    print("\n1️⃣ Logging in via API...")
    login_data = {"username": "guest_001", "password": "guest123"}
    
    response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return False
    
    print("✅ Login successful")
    print(f"Session cookies: {dict(session.cookies)}")
    
    # Step 2: Test feedback submission with credentials (as JavaScript would)
    print("\n2️⃣ Submitting feedback with credentials...")
    feedback_data = {
        "category": "staff_service",
        "rating": 3,
        "subject": "Room could be cleaner",
        "comment": "Overall good service but the room needs better cleaning attention",
        "location": "Room 205",
        "staff_member": "",
        "anonymous": False
    }
    
    # This simulates JavaScript fetch with credentials: 'include'
    response = session.post(
        f"{BASE_URL}/api/feedback/submit", 
        json=feedback_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Submission status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Feedback submitted successfully!")
        print(f"   Feedback ID: {result.get('feedback_id')}")
        print(f"   Alert triggered: {result.get('alert_triggered')}")
        return True
    else:
        print("❌ Feedback submission failed!")
        return False

def test_missing_credentials():
    """Test what happens without session cookies"""
    print("\n❌ Testing without credentials (should fail)...")
    
    feedback_data = {
        "category": "staff_service",
        "rating": 3,
        "subject": "Test",
        "comment": "Test comment",
        "location": "",
        "staff_member": "",
        "anonymous": False
    }
    
    # This simulates JavaScript fetch without credentials
    response = requests.post(
        f"{BASE_URL}/api/feedback/submit", 
        json=feedback_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"No-credentials status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 401:
        print("✅ Correctly rejected unauthenticated request")
    else:
        print("❌ Should have rejected unauthenticated request")

if __name__ == "__main__":
    print("🚀 Testing Web Interface Feedback Submission")
    
    test_web_interface_simulation()
    test_missing_credentials()
    
    print("\n✨ Test completed!")
