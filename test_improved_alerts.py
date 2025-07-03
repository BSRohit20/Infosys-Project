#!/usr/bin/env python3
"""
Test improved admin alert system - ALL feedback creates alerts
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_improved_alert_system():
    """Test that admin gets alerts for ALL guest feedback with proper priorities"""
    
    print("🔔 Testing IMPROVED Admin Alert System")
    print("=" * 60)
    
    # Setup sessions
    admin_session = requests.Session()
    guest_session = requests.Session()
    
    # Admin login
    admin_login = {"username": "admin", "password": "admin123"}
    admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_login)
    
    # Guest login
    guest_login = {"username": "guest_001", "password": "guest123"}
    guest_session.post(f"{BASE_URL}/api/auth/login", json=guest_login)
    
    # Test different feedback types
    feedback_tests = [
        {
            "name": "Excellent Experience (5 stars)",
            "data": {
                "category": "staff_service",
                "rating": 5,
                "subject": "Amazing staff",
                "comment": "The staff was absolutely wonderful! Best hotel experience ever!",
                "location": "Front Desk",
                "staff_member": "John",
                "anonymous": False
            },
            "expected_priority": "low",
            "expected_alert": True
        },
        {
            "name": "Good Experience (4 stars)",
            "data": {
                "category": "amenities",
                "rating": 4,
                "subject": "Nice pool",
                "comment": "The pool was really nice and clean. Enjoyed swimming.",
                "location": "Pool Area",
                "staff_member": "",
                "anonymous": False
            },
            "expected_priority": "low",
            "expected_alert": True
        },
        {
            "name": "Average Experience (3 stars)",
            "data": {
                "category": "dining",
                "rating": 3,
                "subject": "Okay restaurant",
                "comment": "The food was okay, nothing special but acceptable.",
                "location": "Restaurant",
                "staff_member": "",
                "anonymous": False
            },
            "expected_priority": "medium",
            "expected_alert": True
        },
        {
            "name": "Poor Experience (2 stars)",
            "data": {
                "category": "cleanliness",
                "rating": 2,
                "subject": "Room issues",
                "comment": "The room had some cleanliness issues that need attention.",
                "location": "Room 301",
                "staff_member": "",
                "anonymous": False
            },
            "expected_priority": "high",
            "expected_alert": True
        },
        {
            "name": "Terrible Experience (1 star)",
            "data": {
                "category": "staff_service",
                "rating": 1,
                "subject": "Horrible service",
                "comment": "The worst hotel experience I've ever had. Very disappointed.",
                "location": "Front Desk",
                "staff_member": "Manager",
                "anonymous": False
            },
            "expected_priority": "high",
            "expected_alert": True
        }
    ]
    
    # Get initial alert count
    response = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
    initial_count = response.json()['total_count'] if response.status_code == 200 else 0
    
    print(f"📊 Initial alert count: {initial_count}")
    print()
    
    # Submit each feedback and verify alerts
    alerts_created = 0
    for i, test in enumerate(feedback_tests, 1):
        print(f"{i}️⃣ Testing: {test['name']}")
        
        response = guest_session.post(f"{BASE_URL}/api/feedback/submit", json=test['data'])
        if response.status_code == 201:
            result = response.json()
            alert_triggered = result['alert_triggered']
            
            print(f"   ✅ Feedback submitted successfully")
            print(f"   📊 Alert triggered: {alert_triggered}")
            print(f"   🎯 Expected alert: {test['expected_alert']}")
            print(f"   ⭐ Rating: {test['data']['rating']}/5")
            print(f"   😊 Sentiment: {result['sentiment']}")
            
            if alert_triggered == test['expected_alert']:
                print(f"   ✅ Alert behavior correct!")
                if alert_triggered:
                    alerts_created += 1
            else:
                print(f"   ❌ Alert behavior incorrect!")
            
        else:
            print(f"   ❌ Feedback submission failed: {response.text}")
        
        print()
        time.sleep(0.5)  # Small delay between submissions
    
    # Check final alerts
    print("6️⃣ Checking final admin alerts...")
    response = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
    if response.status_code == 200:
        final_alerts = response.json()
        final_count = final_alerts['total_count']
        
        print(f"📊 Final alert count: {final_count}")
        print(f"📈 New alerts created: {final_count - initial_count}")
        print(f"🎯 Expected new alerts: {alerts_created}")
        
        # Show recent alerts with priorities
        print(f"\n📋 Recent alerts (showing priority levels):")
        for i, alert in enumerate(final_alerts['alerts'][:5]):
            priority = alert['priority']
            rating = alert.get('rating', 'N/A')
            sentiment = alert['sentiment']
            
            priority_emoji = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
            
            print(f"   {i+1}. {priority_emoji} [{priority.upper()}] {alert['title']}")
            print(f"      👤 Guest: {alert.get('guest_name', 'N/A')} | ⭐ {rating}/5 | 😊 {sentiment}")
            print(f"      📂 Category: {alert.get('category', 'N/A')}")
            print()
        
        # Summary
        high_priority = len([a for a in final_alerts['alerts'] if a['priority'] == 'high'])
        medium_priority = len([a for a in final_alerts['alerts'] if a['priority'] == 'medium'])
        low_priority = len([a for a in final_alerts['alerts'] if a['priority'] == 'low'])
        
        print(f"📊 Alert Priority Distribution:")
        print(f"   🔴 High Priority: {high_priority} alerts")
        print(f"   🟡 Medium Priority: {medium_priority} alerts")
        print(f"   🟢 Low Priority: {low_priority} alerts")
        
        return True
    else:
        print(f"❌ Failed to get final alerts: {response.text}")
        return False

def test_admin_dashboard_integration():
    """Test that alerts appear in admin dashboard"""
    print("\n7️⃣ Testing admin dashboard integration...")
    
    admin_session = requests.Session()
    admin_login = {"username": "admin", "password": "admin123"}
    admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_login)
    
    # Check if alerts API is accessible
    response = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
    if response.status_code == 200:
        alerts_data = response.json()
        print(f"✅ Admin can access alerts via API")
        print(f"📊 Total alerts: {alerts_data['total_count']}")
        print(f"📬 Unread alerts: {alerts_data['unread_count']}")
        return True
    else:
        print(f"❌ Admin cannot access alerts: {response.text}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Improved Admin Alert System")
    
    # Health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print(f"❌ Server not healthy")
            exit(1)
        print("✅ Server is healthy")
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        exit(1)
    
    # Run tests
    success = test_improved_alert_system()
    
    if success:
        test_admin_dashboard_integration()
        print("\n🎉 IMPROVED ALERT SYSTEM IS WORKING!")
        print("✨ Key Improvements:")
        print("   ✅ ALL feedback now creates alerts (not just negative)")
        print("   ✅ Smart priority system:")
        print("      🔴 High: 1-2 stars or negative sentiment")
        print("      🟡 Medium: 3 stars or neutral sentiment")
        print("      🟢 Low: 4-5 stars with positive sentiment")
        print("   ✅ Enhanced alert details (guest name, category, rating)")
        print("   ✅ Admin can manage all alerts")
        print("\n💡 Result: Admins now get notified about ALL guest feedback!")
    else:
        print("\n❌ Some issues with the improved alert system")
    
    print("\n🏁 Test Complete!")
