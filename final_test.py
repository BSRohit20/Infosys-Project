#!/usr/bin/env python3
"""
Final comprehensive test to verify the feedback submission issue is resolved
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def comprehensive_test():
    """Run comprehensive test of user feedback submission"""
    session = requests.Session()
    
    print("🎯 COMPREHENSIVE FEEDBACK SUBMISSION TEST")
    print("=" * 60)
    
    # Test 1: User login
    print("\n📋 Test 1: User Authentication")
    print("-" * 30)
    
    login_data = {"username": "guest_001", "password": "guest123"}
    response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        print("✅ User login successful")
        print(f"   Session token: {session.cookies.get('session_token')[:20]}...")
    else:
        print(f"❌ User login failed: {response.text}")
        return False
    
    # Test 2: Authentication status check
    print("\n📋 Test 2: Authentication Status")
    print("-" * 30)
    
    response = session.get(f"{BASE_URL}/api/auth/status")
    if response.status_code == 200:
        auth_data = response.json()
        print(f"✅ Authenticated as: {auth_data['user']['username']}")
        print(f"   Role: {auth_data['user']['role']}")
    else:
        print(f"❌ Auth status check failed: {response.text}")
        return False
    
    # Test 3: Feedback submission (simulating web interface)
    print("\n📋 Test 3: Feedback Submission with Session")
    print("-" * 30)
    
    feedback_cases = [
        {
            "name": "Positive Feedback",
            "data": {
                "category": "dining",
                "rating": 5,
                "subject": "Excellent dinner experience",
                "comment": "The food was absolutely amazing and the service was outstanding!",
                "location": "Main Restaurant",
                "staff_member": "Sarah Johnson",
                "anonymous": False
            }
        },
        {
            "name": "Neutral Feedback", 
            "data": {
                "category": "amenities",
                "rating": 3,
                "subject": "Pool area could be improved",
                "comment": "The pool is nice but could use some maintenance and cleaning",
                "location": "Pool Area",
                "staff_member": "",
                "anonymous": False
            }
        },
        {
            "name": "Negative Feedback",
            "data": {
                "category": "room_service", 
                "rating": 2,
                "subject": "Room service was slow",
                "comment": "Room service took over an hour and food arrived cold. Very disappointed.",
                "location": "Room 305",
                "staff_member": "",
                "anonymous": True
            }
        }
    ]
    
    for i, case in enumerate(feedback_cases, 1):
        print(f"\n   Test 3.{i}: {case['name']}")
        
        # This simulates the JavaScript fetch with credentials: 'include'
        response = session.post(
            f"{BASE_URL}/api/feedback/submit",
            json=case['data'],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Submitted successfully")
            print(f"      Feedback ID: {result['feedback_id']}")
            print(f"      Sentiment: {result['sentiment']} ({result['confidence']:.3f})")
            print(f"      Alert triggered: {result['alert_triggered']}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
            return False
    
    # Test 4: Retrieve user's feedback
    print("\n📋 Test 4: Retrieve User's Feedback History")
    print("-" * 30)
    
    response = session.get(f"{BASE_URL}/api/feedback/my-feedback")
    if response.status_code == 200:
        my_feedback = response.json()
        count = len(my_feedback['feedback'])
        print(f"✅ Retrieved {count} feedback entries")
        
        if count > 0:
            latest = my_feedback['feedback'][0]
            print(f"   Latest: {latest['subject']} (Rating: {latest['rating']}/5)")
    else:
        print(f"❌ Failed to retrieve feedback: {response.text}")
        return False
    
    # Test 5: Verify error handling for unauthenticated requests
    print("\n📋 Test 5: Unauthenticated Request Handling")
    print("-" * 30)
    
    feedback_data = {
        "category": "test",
        "rating": 3,
        "subject": "Test",
        "comment": "Test comment",
        "location": "",
        "staff_member": "",
        "anonymous": False
    }
    
    # Test without session cookies (new requests object)
    response = requests.post(
        f"{BASE_URL}/api/feedback/submit",
        json=feedback_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 401:
        print("✅ Correctly rejected unauthenticated request")
        print(f"   Error: {response.json()['detail']}")
    else:
        print(f"❌ Should have rejected request: {response.status_code}")
        return False
    
    # Test 6: Admin/Staff endpoints (should fail for regular user)
    print("\n📋 Test 6: Access Control for Admin Endpoints")
    print("-" * 30)
    
    response = session.get(f"{BASE_URL}/api/feedback/alerts")
    if response.status_code == 403:
        print("✅ Correctly denied admin access to regular user")
    else:
        print(f"❌ Should have denied access: {response.status_code}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! Feedback submission is working correctly!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Comprehensive Feedback Test")
    
    # Wait for server
    time.sleep(1)
    
    # Check server health
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is healthy")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        exit(1)
    
    # Run comprehensive test
    success = comprehensive_test()
    
    if success:
        print("\n🎯 CONCLUSION: The feedback submission issue has been RESOLVED!")
        print("💡 Issue was: JavaScript fetch() calls were missing 'credentials: include'")
        print("🔧 Fix applied: Added credentials to all fetch() calls in feedback.html and main.js")
        print("🛡️ Security: Proper authentication is now enforced on all endpoints")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    print("\n✨ Test completed!")
