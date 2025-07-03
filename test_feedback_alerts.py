#!/usr/bin/env python3
"""
Test script for feedback submission and admin alert system
Tests the complete flow: feedback submission -> alert creation -> visibility
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_feedback_and_alerts():
    """Test the complete feedback and alert system"""
    print("🧪 Testing AI-Driven Guest Experience Feedback & Alert System")
    print("=" * 60)
    
    # Test data
    guest_credentials = {"username": "guest_001", "password": "guest123"}
    admin_credentials = {"username": "admin", "password": "admin123"}
    
    negative_feedback = {
        "category": "room_service",
        "rating": 2,
        "subject": "Poor room service experience",
        "comment": "The room service was very slow and the food was cold when it arrived. Very disappointing experience.",
        "location": "Test Room",
        "staff_member": "Test Staff",
        "anonymous": False
    }
    
    positive_feedback = {
        "category": "dining",
        "rating": 5,
        "subject": "Amazing dining experience", 
        "comment": "The food was absolutely delicious and the service was outstanding! We had a wonderful time and really enjoyed our meal.",
        "location": "Test Restaurant",
        "staff_member": "Test Chef",
        "anonymous": False
    }
    
    try:
        # Step 1: Login as guest
        print("\n1️⃣ Logging in as guest...")
        guest_session = requests.Session()
        guest_login = guest_session.post(
            f"{BASE_URL}/api/auth/login",
            json=guest_credentials
        )
        assert guest_login.status_code == 200, f"Guest login failed: {guest_login.text}"
        print("   ✅ Guest login successful")
        
        # Step 2: Submit negative feedback (should trigger alert)
        print("\n2️⃣ Submitting negative feedback...")
        negative_response = guest_session.post(
            f"{BASE_URL}/api/feedback/submit",
            json=negative_feedback
        )
        assert negative_response.status_code == 201, f"Negative feedback failed: {negative_response.text}"
        negative_data = negative_response.json()
        assert negative_data["alert_triggered"] == True, "Alert should be triggered for negative feedback"
        print(f"   ✅ Negative feedback submitted: {negative_data['feedback_id']}")
        print(f"   ✅ Alert triggered: {negative_data['alert_triggered']}")
        print(f"   ✅ Sentiment: {negative_data['sentiment']} (confidence: {negative_data['confidence']:.2f})")
        
        # Step 3: Submit positive feedback (should NOT trigger alert)
        print("\n3️⃣ Submitting positive feedback...")
        positive_response = guest_session.post(
            f"{BASE_URL}/api/feedback/submit",
            json=positive_feedback
        )
        assert positive_response.status_code == 201, f"Positive feedback failed: {positive_response.text}"
        positive_data = positive_response.json()
        assert positive_data["alert_triggered"] == False, "Alert should NOT be triggered for positive feedback"
        print(f"   ✅ Positive feedback submitted: {positive_data['feedback_id']}")
        print(f"   ✅ Alert triggered: {positive_data['alert_triggered']}")
        print(f"   ✅ Sentiment: {positive_data['sentiment']} (confidence: {positive_data['confidence']:.2f})")
        
        # Step 4: Check guest feedback visibility
        print("\n4️⃣ Checking guest feedback visibility...")
        guest_feedback = guest_session.get(f"{BASE_URL}/api/feedback/my-feedback")
        assert guest_feedback.status_code == 200, f"Get guest feedback failed: {guest_feedback.text}"
        guest_feedback_data = guest_feedback.json()
        print(f"   ✅ Guest can see {guest_feedback_data['total_count']} feedback entries")
        
        # Verify the new feedback is visible
        feedback_ids = [fb["feedback_id"] for fb in guest_feedback_data["feedback"]]
        assert negative_data["feedback_id"] in feedback_ids, "Negative feedback not visible in guest profile"
        assert positive_data["feedback_id"] in feedback_ids, "Positive feedback not visible in guest profile"
        print("   ✅ Both new feedback entries are visible in guest profile")
        
        # Step 5: Login as admin
        print("\n5️⃣ Logging in as admin...")
        admin_session = requests.Session()
        admin_login = admin_session.post(
            f"{BASE_URL}/api/auth/login",
            json=admin_credentials
        )
        assert admin_login.status_code == 200, f"Admin login failed: {admin_login.text}"
        print("   ✅ Admin login successful")
        
        # Step 6: Check admin alerts
        print("\n6️⃣ Checking admin alerts...")
        admin_alerts = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
        assert admin_alerts.status_code == 200, f"Get admin alerts failed: {admin_alerts.text}"
        alerts_data = admin_alerts.json()
        print(f"   ✅ Admin can see {alerts_data['total_count']} total alerts")
        print(f"   ✅ {alerts_data['unread_count']} alerts are unread")
        
        # Verify the negative feedback alert is present
        alert_feedback_ids = [alert.get("feedback_id") for alert in alerts_data["alerts"]]
        assert negative_data["feedback_id"] in alert_feedback_ids, "Negative feedback alert not found"
        print(f"   ✅ Alert for negative feedback {negative_data['feedback_id']} is visible")
        
        # Step 7: Mark alert as read
        print("\n7️⃣ Testing mark alert as read...")
        target_alert = None
        for alert in alerts_data["alerts"]:
            if alert.get("feedback_id") == negative_data["feedback_id"]:
                target_alert = alert
                break
        
        if target_alert:
            mark_read = admin_session.post(
                f"{BASE_URL}/api/feedback/alerts/{target_alert['alert_id']}/mark-read"
            )
            assert mark_read.status_code == 200, f"Mark alert as read failed: {mark_read.text}"
            print(f"   ✅ Alert {target_alert['alert_id']} marked as read")
            
            # Verify the alert status changed
            updated_alerts = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
            updated_data = updated_alerts.json()
            updated_alert = None
            for alert in updated_data["alerts"]:
                if alert["alert_id"] == target_alert["alert_id"]:
                    updated_alert = alert
                    break
            
            assert updated_alert["status"] == "read", "Alert status should be 'read'"
            print("   ✅ Alert status successfully changed to 'read'")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("✅ Feedback submission works correctly")
        print("✅ Admin alerts are triggered for negative feedback")
        print("✅ Admin alerts are NOT triggered for positive feedback") 
        print("✅ Guest feedback is visible in guest profile")
        print("✅ Admin alerts are visible in admin dashboard")
        print("✅ Mark alert as read functionality works")
        print("\n🚀 The AI-Driven Guest Experience system is working perfectly!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise

if __name__ == "__main__":
    test_feedback_and_alerts()
