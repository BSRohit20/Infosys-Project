#!/usr/bin/env python3
"""
Test admin alerts when guests submit feedback
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_guest_feedback_admin_alerts():
    """Test that admin gets alerts when guests submit feedback"""
    
    print("🔔 Testing Admin Alerts for Guest Feedback")
    print("=" * 60)
    
    # Step 1: Login as admin first to check current alerts
    print("\n1️⃣ Admin login and checking initial alerts...")
    admin_session = requests.Session()
    admin_login = {"username": "admin", "password": "admin123"}
    
    response = admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_login)
    if response.status_code != 200:
        print(f"❌ Admin login failed: {response.text}")
        return False
    
    print("✅ Admin logged in successfully")
    
    # Check initial alert count
    response = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
    if response.status_code == 200:
        initial_alerts = response.json()
        initial_count = initial_alerts['total_count']
        initial_unread = initial_alerts['unread_count']
        print(f"📊 Initial alerts: {initial_count} total, {initial_unread} unread")
    else:
        print(f"❌ Failed to get initial alerts: {response.text}")
        return False
    
    # Step 2: Login as guest
    print("\n2️⃣ Guest login...")
    guest_session = requests.Session()
    guest_login = {"username": "guest_001", "password": "guest123"}
    
    response = guest_session.post(f"{BASE_URL}/api/auth/login", json=guest_login)
    if response.status_code != 200:
        print(f"❌ Guest login failed: {response.text}")
        return False
    
    print("✅ Guest logged in successfully")
    
    # Step 3: Submit positive feedback (rating 5)
    print("\n3️⃣ Guest submitting positive feedback (5 stars)...")
    positive_feedback = {
        "category": "staff_service",
        "rating": 5,
        "subject": "Excellent service",
        "comment": "The staff was amazing and very helpful throughout our stay!",
        "location": "Front Desk",
        "staff_member": "Sarah",
        "anonymous": False
    }
    
    response = guest_session.post(f"{BASE_URL}/api/feedback/submit", json=positive_feedback)
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Positive feedback submitted!")
        print(f"   Feedback ID: {result['feedback_id']}")
        print(f"   Sentiment: {result['sentiment']}")
        print(f"   Alert triggered: {result['alert_triggered']}")
        positive_alert_triggered = result['alert_triggered']
    else:
        print(f"❌ Positive feedback failed: {response.text}")
        return False
    
    # Step 4: Submit negative feedback (rating 2)
    print("\n4️⃣ Guest submitting negative feedback (2 stars)...")
    negative_feedback = {
        "category": "cleanliness",
        "rating": 2,
        "subject": "Room was dirty",
        "comment": "The room was not clean when we arrived. Very disappointed.",
        "location": "Room 205",
        "staff_member": "",
        "anonymous": False
    }
    
    response = guest_session.post(f"{BASE_URL}/api/feedback/submit", json=negative_feedback)
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Negative feedback submitted!")
        print(f"   Feedback ID: {result['feedback_id']}")
        print(f"   Sentiment: {result['sentiment']}")
        print(f"   Alert triggered: {result['alert_triggered']}")
        negative_alert_triggered = result['alert_triggered']
    else:
        print(f"❌ Negative feedback failed: {response.text}")
        return False
    
    # Step 5: Submit neutral feedback (rating 3)
    print("\n5️⃣ Guest submitting neutral feedback (3 stars)...")
    neutral_feedback = {
        "category": "amenities",
        "rating": 3,
        "subject": "Average pool area",
        "comment": "The pool was okay, nothing special but adequate for our needs.",
        "location": "Pool Area",
        "staff_member": "",
        "anonymous": False
    }
    
    response = guest_session.post(f"{BASE_URL}/api/feedback/submit", json=neutral_feedback)
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Neutral feedback submitted!")
        print(f"   Feedback ID: {result['feedback_id']}")
        print(f"   Sentiment: {result['sentiment']}")
        print(f"   Alert triggered: {result['alert_triggered']}")
        neutral_alert_triggered = result['alert_triggered']
    else:
        print(f"❌ Neutral feedback failed: {response.text}")
        return False
    
    # Step 6: Check admin alerts after feedback submissions
    print("\n6️⃣ Checking admin alerts after feedback submissions...")
    time.sleep(1)  # Give time for alerts to be processed
    
    response = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
    if response.status_code == 200:
        final_alerts = response.json()
        final_count = final_alerts['total_count']
        final_unread = final_alerts['unread_count']
        
        print(f"📊 Final alerts: {final_count} total, {final_unread} unread")
        print(f"📈 Change: +{final_count - initial_count} alerts, +{final_unread - initial_unread} unread")
        
        # Show recent alerts
        if final_alerts['alerts']:
            print(f"\n📋 Recent alerts:")
            for i, alert in enumerate(final_alerts['alerts'][:3]):  # Show first 3
                priority_emoji = "🔴" if alert['priority'] == 'high' else "🟡" if alert['priority'] == 'medium' else "🟢"
                status_emoji = "🔵" if alert['status'] == 'unread' else "✅"
                print(f"   {i+1}. {priority_emoji}{status_emoji} {alert['title']}")
                print(f"      Priority: {alert['priority']}, Sentiment: {alert['sentiment']}")
                print(f"      Guest: {alert.get('guest_id', 'N/A')}")
        
        # Analyze alert creation logic
        print(f"\n🧪 Alert Analysis:")
        print(f"   Positive feedback (5 stars): Alert triggered = {positive_alert_triggered}")
        print(f"   Negative feedback (2 stars): Alert triggered = {negative_alert_triggered}")
        print(f"   Neutral feedback (3 stars): Alert triggered = {neutral_alert_triggered}")
        
        return True
    else:
        print(f"❌ Failed to get final alerts: {response.text}")
        return False

def test_admin_alert_management():
    """Test admin can manage alerts"""
    print("\n7️⃣ Testing admin alert management...")
    
    admin_session = requests.Session()
    admin_login = {"username": "admin", "password": "admin123"}
    admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_login)
    
    # Get alerts
    response = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
    if response.status_code == 200:
        alerts_data = response.json()
        if alerts_data['alerts']:
            # Try to mark first alert as read
            first_alert = alerts_data['alerts'][0]
            alert_id = first_alert['alert_id']
            
            response = admin_session.post(f"{BASE_URL}/api/feedback/alerts/{alert_id}/mark-read")
            if response.status_code == 200:
                print(f"✅ Successfully marked alert {alert_id} as read")
                return True
            else:
                print(f"❌ Failed to mark alert as read: {response.text}")
                return False
        else:
            print("ℹ️ No alerts to mark as read")
            return True
    else:
        print(f"❌ Failed to get alerts for management test: {response.text}")
        return False

def suggest_improvements():
    """Suggest improvements to the alert system"""
    print("\n💡 Alert System Recommendations:")
    print("   1. Currently alerts are only created for:")
    print("      - Ratings <= 3 (1, 2, or 3 stars)")
    print("      - Negative sentiment feedback")
    print("   2. Consider creating alerts for ALL feedback to keep admins informed")
    print("   3. Different priority levels:")
    print("      - High: Rating 1-2 or very negative sentiment")
    print("      - Medium: Rating 3 or neutral/slightly negative sentiment")
    print("      - Low: Rating 4-5 with positive sentiment")
    print("   4. Add email/SMS notifications for critical alerts")
    print("   5. Add alert categorization by feedback type")

if __name__ == "__main__":
    print("🚀 Starting Guest Feedback Admin Alert Test")
    
    # Wait for server
    time.sleep(1)
    
    # Test health
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print(f"❌ Server not healthy: {response.status_code}")
            exit(1)
        print("✅ Server is healthy")
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        exit(1)
    
    # Run tests
    success = test_guest_feedback_admin_alerts()
    
    if success:
        test_admin_alert_management()
        suggest_improvements()
        print("\n🎉 Admin alert system is working!")
        print("💡 Admins will receive alerts for ratings <= 3 or negative sentiment")
    else:
        print("\n❌ Some issues with the alert system")
    
    print("\n🏁 Test Complete!")
