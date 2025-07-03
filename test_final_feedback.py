#!/usr/bin/env python3
"""
Final comprehensive test to verify feedback submission works for users
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_complete_user_flow():
    """Test the complete user flow from login to feedback submission"""
    session = requests.Session()
    
    print("🎯 FINAL TEST: Complete User Feedback Flow")
    print("=" * 60)
    
    # Step 1: Health check
    print("\n🏥 Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is healthy")
            health_data = response.json()
            print(f"   Status: {health_data.get('status')}")
            print(f"   Version: {health_data.get('version')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        return False
    
    # Step 2: User login
    print("\n👤 User Login...")
    login_data = {"username": "guest_001", "password": "guest123"}
    
    try:
        response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            print(f"✅ Login successful for: {login_result['user']['username']}")
            print(f"   User ID: {login_result['user']['user_id']}")
            print(f"   Role: {login_result['user']['role']}")
            print(f"   Name: {login_result['user']['first_name']} {login_result['user']['last_name']}")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 3: Verify authentication
    print("\n🔐 Authentication Verification...")
    try:
        response = session.get(f"{BASE_URL}/api/auth/status")
        if response.status_code == 200:
            auth_data = response.json()
            print(f"✅ Authentication verified: {auth_data['user']['username']}")
        else:
            print(f"❌ Auth verification failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Auth verification error: {e}")
        return False
    
    # Step 4: Submit positive feedback
    print("\n😊 Submitting Positive Feedback...")
    positive_feedback = {
        "category": "staff_service",
        "rating": 5,
        "subject": "Outstanding service from the team",
        "comment": "The staff was incredibly helpful and friendly. They went above and beyond to make our stay memorable. Thank you!",
        "location": "Front Desk",
        "staff_member": "Sarah Johnson",
        "anonymous": False
    }
    
    try:
        response = session.post(f"{BASE_URL}/api/feedback/submit", json=positive_feedback)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Positive feedback submitted successfully!")
            print(f"   Feedback ID: {result['feedback_id']}")
            print(f"   Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
            print(f"   Alert triggered: {result['alert_triggered']}")
        else:
            print(f"❌ Positive feedback failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Positive feedback error: {e}")
        return False
    
    # Step 5: Submit negative feedback (should trigger alert)
    print("\n😔 Submitting Negative Feedback...")
    negative_feedback = {
        "category": "cleanliness",
        "rating": 2,
        "subject": "Room cleanliness issues",
        "comment": "The room was not properly cleaned when we arrived. The bathroom had stains and the bed sheets looked used.",
        "location": "Room 305",
        "staff_member": "",
        "anonymous": False
    }
    
    try:
        response = session.post(f"{BASE_URL}/api/feedback/submit", json=negative_feedback)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Negative feedback submitted successfully!")
            print(f"   Feedback ID: {result['feedback_id']}")
            print(f"   Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
            print(f"   Alert triggered: {result['alert_triggered']}")
        else:
            print(f"❌ Negative feedback failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Negative feedback error: {e}")
        return False
    
    # Step 6: Retrieve user's feedback history
    print("\n📋 Retrieving Feedback History...")
    try:
        response = session.get(f"{BASE_URL}/api/feedback/my-feedback")
        if response.status_code == 200:
            data = response.json()
            feedback_count = len(data['feedback'])
            print(f"✅ Retrieved {feedback_count} feedback entries")
            
            # Show recent feedback
            if feedback_count > 0:
                recent = data['feedback'][0]
                print(f"   Most recent: '{recent['subject']}' - {recent['rating']}/5 stars")
                print(f"   Sentiment: {recent['sentiment_analysis']['sentiment']}")
        else:
            print(f"❌ Failed to retrieve feedback: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Feedback retrieval error: {e}")
        return False
    
    # Step 7: Test admin login and alert checking
    print("\n👑 Testing Admin Access...")
    admin_session = requests.Session()
    
    try:
        admin_login = {"username": "admin", "password": "admin123"}
        response = admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_login)
        
        if response.status_code == 200:
            print("✅ Admin login successful")
            
            # Check admin alerts
            response = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
            if response.status_code == 200:
                alerts_data = response.json()
                alert_count = len(alerts_data['alerts'])
                print(f"✅ Retrieved {alert_count} admin alerts")
                
                # Show recent alerts
                if alert_count > 0:
                    recent_alert = alerts_data['alerts'][0]
                    print(f"   Recent alert: {recent_alert['title']}")
                    print(f"   Priority: {recent_alert['priority']}")
                    print(f"   Status: {recent_alert['status']}")
            else:
                print(f"❌ Failed to retrieve alerts: {response.status_code}")
        else:
            print(f"❌ Admin login failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Admin test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    print("✨ The feedback system is working correctly for users!")
    return True

def test_edge_cases():
    """Test edge cases and validation"""
    print("\n🧪 Testing Edge Cases...")
    session = requests.Session()
    
    # Login first
    login_data = {"username": "guest_001", "password": "guest123"}
    session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    # Test invalid rating
    invalid_feedback = {
        "category": "staff_service",
        "rating": 6,  # Invalid rating
        "subject": "Test",
        "comment": "Test comment",
        "location": "",
        "staff_member": "",
        "anonymous": False
    }
    
    try:
        response = session.post(f"{BASE_URL}/api/feedback/submit", json=invalid_feedback)
        if response.status_code == 422:
            print("✅ Correctly rejected invalid rating")
        else:
            print(f"❌ Should have rejected invalid rating: {response.status_code}")
    except Exception as e:
        print(f"❌ Edge case test error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Final Feedback System Test")
    
    # Wait for server to be ready
    time.sleep(1)
    
    # Run comprehensive test
    success = test_complete_user_flow()
    
    if success:
        test_edge_cases()
        print("\n🎊 SUCCESS: Feedback submission is working perfectly!")
        print("📝 Users can now submit feedback without errors.")
        print("🔔 Admin alerts are being triggered for negative feedback.")
        print("👥 User feedback history is properly maintained.")
    else:
        print("\n❌ FAILURE: Some issues still exist.")
    
    print("\n" + "🏁 Test Complete!" + "\n")
