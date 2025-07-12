#!/usr/bin/env python3
"""
Test script to verify that when a guest submits feedback, 
the admin receives an alert.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_guest_feedback_alert():
    """Test guest feedback submission and admin alert generation"""
    
    print("🧪 Testing Guest Feedback Alert System")
    print("=" * 50)
    
    # Step 1: Login as guest
    print("\n1. 📋 Logging in as guest...")
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "guest_001", 
        "password": "guest123"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    login_data = login_response.json()
    print(f"✅ Guest login successful: {login_data['data']['user']['username']}")
    
    # Extract cookies for authentication
    guest_cookies = login_response.cookies
    
    # Step 2: Submit feedback as guest
    print("\n2. 📝 Submitting feedback as guest...")
    feedback_data = {
        "category": "room_service",
        "rating": 4,  # Positive rating
        "subject": "Great room service experience",
        "comment": "The room service was prompt and the food was delicious. Staff was very courteous and professional.",
        "location": "Room 412",
        "staff_member": "Maria Rodriguez",
        "anonymous": False
    }
    
    feedback_response = requests.post(
        f"{BASE_URL}/api/feedback/submit",
        json=feedback_data,
        cookies=guest_cookies
    )
    
    if feedback_response.status_code != 201:
        print(f"❌ Feedback submission failed: {feedback_response.status_code}")
        print(feedback_response.text)
        return
    
    feedback_result = feedback_response.json()
    print(f"✅ Feedback submitted successfully!")
    print(f"   📄 Feedback ID: {feedback_result['feedback_id']}")
    print(f"   😊 Sentiment: {feedback_result['sentiment']}")
    print(f"   🔔 Alert triggered: {feedback_result['alert_triggered']}")
    
    # Step 3: Logout guest and login as admin
    print("\n3. 🔐 Switching to admin account...")
    admin_login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "admin", 
        "password": "admin123"
    })
    
    if admin_login_response.status_code != 200:
        print(f"❌ Admin login failed: {admin_login_response.status_code}")
        return
    
    admin_data = admin_login_response.json()
    print(f"✅ Admin login successful: {admin_data['data']['user']['username']}")
    
    admin_cookies = admin_login_response.cookies
    
    # Step 4: Check admin alerts
    print("\n4. 🔔 Checking admin alerts...")
    alerts_response = requests.get(
        f"{BASE_URL}/api/analytics/alerts",
        cookies=admin_cookies
    )
    
    if alerts_response.status_code != 200:
        print(f"❌ Failed to get alerts: {alerts_response.status_code}")
        print(alerts_response.text)
        return
    
    alerts_data = alerts_response.json()
    
    if not alerts_data.get('success'):
        print(f"❌ Alert API returned error: {alerts_data}")
        return
    
    alerts = alerts_data['data']['alerts']
    total_alerts = alerts_data['data']['total_alerts']
    unread_count = alerts_data['data']['unread_count']
    
    print(f"📊 Alert Summary:")
    print(f"   Total alerts: {total_alerts}")
    print(f"   Unread alerts: {unread_count}")
    
    # Step 5: Find our feedback in alerts
    print("\n5. 🔍 Looking for our feedback alert...")
    feedback_id = feedback_result['feedback_id']
    found_alert = None
    
    for alert in alerts:
        if alert.get('feedback_id') == feedback_id:
            found_alert = alert
            break
    
    if found_alert:
        print(f"✅ Alert found for our feedback!")
        print(f"   🆔 Alert ID: {found_alert['alert_id']}")
        print(f"   📋 Title: {found_alert['title']}")
        print(f"   💬 Message: {found_alert['message']}")
        print(f"   🎯 Priority: {found_alert['priority']} {found_alert.get('priority_emoji', '')}")
        print(f"   👤 Guest: {found_alert['guest_name']}")
        print(f"   ⭐ Rating: {found_alert['rating']}/5")
        print(f"   😊 Sentiment: {found_alert['sentiment']}")
        print(f"   📂 Category: {found_alert['category']}")
        print(f"   📅 Created: {found_alert['created_at']}")
        print(f"   📘 Status: {found_alert['status']}")
        
        print("\n🎉 SUCCESS: Guest feedback triggered admin alert correctly!")
        
    else:
        print(f"❌ FAILED: No alert found for feedback ID {feedback_id}")
        print("Available alerts:")
        for i, alert in enumerate(alerts[:3]):
            print(f"   {i+1}. {alert.get('title', 'No title')} - {alert.get('feedback_id', 'No ID')}")
    
    # Step 6: Test with negative feedback too
    print("\n6. 🧪 Testing with negative feedback...")
    negative_feedback = {
        "category": "cleanliness",
        "rating": 2,  # Negative rating
        "subject": "Room was not clean",
        "comment": "The room was dirty when we arrived. Bathroom was not properly cleaned and bed sheets had stains.",
        "location": "Room 205",
        "staff_member": "",
        "anonymous": False
    }
    
    # Re-login as guest (session might have expired)
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "guest_001", 
        "password": "guest123"
    })
    guest_cookies = login_response.cookies
    
    negative_response = requests.post(
        f"{BASE_URL}/api/feedback/submit",
        json=negative_feedback,
        cookies=guest_cookies
    )
    
    if negative_response.status_code == 201:
        negative_result = negative_response.json()
        print(f"✅ Negative feedback submitted: {negative_result['feedback_id']}")
        print(f"   😔 Sentiment: {negative_result['sentiment']}")
        print(f"   🔔 Alert triggered: {negative_result['alert_triggered']}")
        
        # Check alerts again
        alerts_response = requests.get(
            f"{BASE_URL}/api/analytics/alerts",
            cookies=admin_cookies
        )
        
        if alerts_response.status_code == 200:
            new_alerts_data = alerts_response.json()
            new_alerts = new_alerts_data['data']['alerts']
            
            # Look for the negative feedback alert
            negative_alert = None
            for alert in new_alerts:
                if alert.get('feedback_id') == negative_result['feedback_id']:
                    negative_alert = alert
                    break
            
            if negative_alert:
                print(f"✅ Negative feedback alert found!")
                print(f"   🎯 Priority: {negative_alert['priority']} {negative_alert.get('priority_emoji', '')}")
                print(f"   😔 Sentiment: {negative_alert['sentiment']}")
            else:
                print(f"❌ Negative feedback alert not found")
    
    print("\n" + "=" * 50)
    print("✅ Guest Feedback Alert Test Complete!")

if __name__ == "__main__":
    test_guest_feedback_alert()
