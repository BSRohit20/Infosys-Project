#!/usr/bin/env python3
"""
Debug feedback submission error
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_feedback_submission_debug():
    """Debug the feedback submission error"""
    session = requests.Session()
    
    print("🔍 Debugging Feedback Submission Error")
    print("=" * 50)
    
    # Step 1: Login as guest
    print("\n1️⃣ Logging in as guest...")
    login_data = {"username": "guest_001", "password": "guest123"}
    
    try:
        response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"Login status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Login failed: {response.text}")
            return False
        print("✅ Login successful")
        print(f"Session cookies: {dict(session.cookies)}")
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 2: Test minimal feedback submission
    print("\n2️⃣ Testing minimal feedback submission...")
    
    minimal_feedback = {
        "category": "staff_service",
        "rating": 4,
        "subject": "Test feedback",
        "comment": "This is a test comment to debug the submission issue."
    }
    
    print(f"Submitting feedback data: {json.dumps(minimal_feedback, indent=2)}")
    
    try:
        response = session.post(
            f"{BASE_URL}/api/feedback/submit", 
            json=minimal_feedback,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Feedback submitted successfully!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   Sentiment: {result.get('sentiment')}")
        else:
            print("❌ Feedback submission failed!")
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Raw error: {response.text}")
                
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False
    
    # Step 3: Test with all optional fields
    print("\n3️⃣ Testing with all fields...")
    
    complete_feedback = {
        "category": "dining",
        "rating": 3,
        "subject": "Restaurant experience",
        "comment": "The food was okay but service was slow.",
        "location": "Hotel Restaurant",
        "staff_member": "John",
        "anonymous": False
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/api/feedback/submit", 
            json=complete_feedback,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Complete feedback status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Complete feedback submitted successfully!")
        else:
            print(f"❌ Complete feedback failed: {response.text}")
                
    except Exception as e:
        print(f"❌ Complete feedback error: {e}")
    
    # Step 4: Test validation errors
    print("\n4️⃣ Testing validation...")
    
    invalid_feedback = {
        "category": "",  # Empty category
        "rating": 4,
        "subject": "Test",
        "comment": "Test comment"
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/api/feedback/submit", 
            json=invalid_feedback,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Invalid feedback status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Validation working correctly")
            print(f"   Validation error: {response.json().get('detail')}")
        else:
            print(f"❌ Expected validation error: {response.text}")
                
    except Exception as e:
        print(f"❌ Validation test error: {e}")
    
    print("\n" + "=" * 50)
    return True

def test_browser_like_submission():
    """Test submission similar to browser JavaScript"""
    print("\n🌐 Testing Browser-like Submission")
    print("=" * 30)
    
    session = requests.Session()
    
    # Login
    login_data = {"username": "guest_001", "password": "guest123"}
    session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    # Test form data submission (like JavaScript FormData)
    feedback_data = {
        "category": "amenities",
        "rating": 5,
        "subject": "Great pool area",
        "comment": "The pool is amazing!",
        "location": "",
        "staff_member": "",
        "anonymous": "false"  # String like form data
    }
    
    try:
        # Test with credentials like browser
        response = session.post(
            f"{BASE_URL}/api/feedback/submit",
            json=feedback_data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        print(f"Browser-like status: {response.status_code}")
        print(f"Browser-like response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Browser-like submission works!")
        else:
            print("❌ Browser-like submission failed!")
            
    except Exception as e:
        print(f"❌ Browser-like error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Feedback Submission Debug")
    
    test_feedback_submission_debug()
    test_browser_like_submission()
    
    print("\n🏁 Debug Complete!")
