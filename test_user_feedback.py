#!/usr/bin/env python3
"""
Test script to check user feedback submission issues
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_user_feedback_submission():
    """Test feedback submission as a regular user"""
    session = requests.Session()
    
    print("🧪 Testing User Feedback Submission...")
    print("=" * 50)
    
    # Step 1: Login as a regular user
    print("\n1️⃣ Logging in as user...")
    login_data = {
        "username": "guest_001", 
        "password": "guest123"
    }
    
    try:
        response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"Login status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code != 200:
            print("❌ Login failed!")
            return False
            
        login_result = response.json()
        print(f"✅ Login successful for user: {login_result.get('user', {}).get('username')}")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 2: Check authentication status
    print("\n2️⃣ Checking authentication status...")
    try:
        response = session.get(f"{BASE_URL}/api/auth/status")
        print(f"Auth status: {response.status_code}")
        if response.status_code == 200:
            auth_result = response.json()
            print(f"✅ Authenticated as: {auth_result.get('user', {}).get('username')}")
        else:
            print(f"❌ Auth check failed: {response.text}")
    except Exception as e:
        print(f"❌ Auth check error: {e}")
    
    # Step 3: Submit feedback
    print("\n3️⃣ Submitting feedback...")
    feedback_data = {
        "category": "room_service",
        "rating": 4,
        "subject": "Great room service experience",
        "comment": "The staff was very professional and food arrived quickly. Really enjoyed my stay!",
        "location": "Room 302",
        "staff_member": "John Smith",
        "anonymous": False
    }
    
    try:
        # Check cookies first
        print(f"Session cookies: {dict(session.cookies)}")
        
        response = session.post(f"{BASE_URL}/api/feedback/submit", json=feedback_data)
        print(f"Feedback submission status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Feedback submitted successfully!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   Sentiment: {result.get('sentiment')}")
            print(f"   Alert triggered: {result.get('alert_triggered')}")
        else:
            print(f"❌ Feedback submission failed!")
            try:
                error_detail = response.json()
                print(f"   Error details: {error_detail}")
            except:
                print(f"   Raw error: {response.text}")
                
    except Exception as e:
        print(f"❌ Feedback submission error: {e}")
        return False
    
    # Step 4: Retrieve user's feedback
    print("\n4️⃣ Retrieving user's feedback...")
    try:
        response = session.get(f"{BASE_URL}/api/feedback/my-feedback")
        print(f"My feedback status: {response.status_code}")
        if response.status_code == 200:
            my_feedback = response.json()
            print(f"✅ Retrieved {len(my_feedback.get('feedback', []))} feedback entries")
        else:
            print(f"❌ Failed to retrieve feedback: {response.text}")
    except Exception as e:
        print(f"❌ Feedback retrieval error: {e}")
    
    print("\n" + "=" * 50)
    print("🧪 Test completed!")
    
    return True

def test_direct_api_call():
    """Test direct API call without session to see if it's an auth issue"""
    print("\n🔬 Testing direct API call without authentication...")
    
    feedback_data = {
        "category": "room_service",
        "rating": 4,
        "subject": "Test feedback",
        "comment": "This is a test comment",
        "location": "Test location",
        "staff_member": "Test staff",
        "anonymous": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/feedback/submit", json=feedback_data)
        print(f"Direct API call status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("✅ Correctly requires authentication")
        else:
            print("❌ Unexpected response for unauthenticated request")
            
    except Exception as e:
        print(f"❌ Direct API error: {e}")

if __name__ == "__main__":
    print("🚀 Starting User Feedback Submission Test")
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Test health endpoint first
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        exit(1)
    
    # Run tests
    test_user_feedback_submission()
    test_direct_api_call()
    
    print("\n✨ All tests completed!")
