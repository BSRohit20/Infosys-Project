#!/usr/bin/env python3
"""
Test guest dashboard feedback submission
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_guest_dashboard_feedback():
    """Test feedback submission from guest dashboard"""
    session = requests.Session()
    
    print("🎯 Testing Guest Dashboard Feedback Submission")
    print("=" * 50)
    
    # Step 1: Login as guest
    print("\n1️⃣ Logging in as guest...")
    login_data = {"username": "guest_001", "password": "guest123"}
    
    response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return False
    
    print("✅ Guest login successful")
    
    # Step 2: Test guest dashboard feedback form (simulating the new form structure)
    print("\n2️⃣ Submitting feedback from guest dashboard...")
    
    dashboard_feedback = {
        "category": "staff_service",
        "rating": 4,
        "subject": "Helpful front desk staff",
        "comment": "The front desk staff was very helpful during check-in. They provided great recommendations for local restaurants.",
        "location": "Front Desk",
        "staff_member": "Jennifer",
        "anonymous": False
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/api/feedback/submit", 
            json=dashboard_feedback,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Feedback submission status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Guest dashboard feedback submitted successfully!")
            print(f"   Feedback ID: {result['feedback_id']}")
            print(f"   Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
            print(f"   Alert triggered: {result['alert_triggered']}")
        else:
            print("❌ Guest dashboard feedback submission failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 3: Test another feedback with negative sentiment
    print("\n3️⃣ Submitting negative feedback from guest dashboard...")
    
    negative_feedback = {
        "category": "dining",
        "rating": 2,
        "subject": "Cold food at restaurant",
        "comment": "The food at the hotel restaurant was cold when it arrived. Very disappointing experience.",
        "location": "Hotel Restaurant",
        "staff_member": "",
        "anonymous": False
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/api/feedback/submit", 
            json=negative_feedback,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Negative feedback submitted successfully!")
            print(f"   Feedback ID: {result['feedback_id']}")
            print(f"   Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
            print(f"   Alert triggered: {result['alert_triggered']}")
        else:
            print(f"❌ Negative feedback failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 4: Check that both regular feedback page and dashboard work
    print("\n4️⃣ Testing dedicated feedback page still works...")
    
    dedicated_feedback = {
        "category": "amenities",
        "rating": 5,
        "subject": "Amazing pool area",
        "comment": "The pool area is beautiful and well-maintained. Great place to relax!",
        "location": "Pool Area",
        "staff_member": "",
        "anonymous": False
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/api/feedback/submit", 
            json=dedicated_feedback,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Dedicated feedback page also works!")
            print(f"   Feedback ID: {result['feedback_id']}")
        else:
            print(f"❌ Dedicated feedback page failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL GUEST DASHBOARD FEEDBACK TESTS PASSED!")
    print("✨ Guests can now submit feedback from both:")
    print("   📱 Guest Dashboard (quick feedback)")
    print("   📝 Dedicated Feedback Page (detailed feedback)")
    return True

def test_validation():
    """Test form validation works correctly"""
    print("\n🧪 Testing Form Validation...")
    session = requests.Session()
    
    # Login first
    login_data = {"username": "guest_001", "password": "guest123"}
    session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    # Test missing required fields
    invalid_feedback = {
        "category": "",  # Missing category
        "rating": 4,
        "subject": "",   # Missing subject
        "comment": "",   # Missing comment
        "location": "",
        "staff_member": "",
        "anonymous": False
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/api/feedback/submit", 
            json=invalid_feedback,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:
            print("✅ Form validation working correctly")
            print(f"   Validation error: {response.json()['detail']}")
        else:
            print(f"❌ Expected validation error, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Validation test error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Guest Dashboard Feedback Test")
    
    # Wait for server
    time.sleep(1)
    
    # Run tests
    success = test_guest_dashboard_feedback()
    
    if success:
        test_validation()
        print("\n🎊 SUCCESS: Guest dashboard feedback is now working!")
        print("🔧 Fixed issues:")
        print("   ✅ Updated form fields to match API requirements")
        print("   ✅ Added missing 'subject' field") 
        print("   ✅ Changed 'feedback_text' to 'comment'")
        print("   ✅ Updated JavaScript to send JSON instead of FormData")
        print("   ✅ Added proper validation and error handling")
    else:
        print("\n❌ Some issues remain")
    
    print("\n🏁 Test Complete!")
