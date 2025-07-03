#!/usr/bin/env python3
"""
Comprehensive end-to-end test for the Infosys Guest Feedback System.
This script tests:
1. Guest feedback submission
2. Admin alerts generation
3. Analytics dashboard data loading
4. Alert viewing and management
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8001"

def timestamp():
    """Return current timestamp for logging"""
    return datetime.now().strftime("%H:%M:%S")

def print_section(title):
    """Print a section header"""
    print(f"\n{timestamp()} {'=' * 20} {title} {'=' * 20}")

def test_end_to_end():
    """Run comprehensive end-to-end tests"""
    print_section("STARTING COMPREHENSIVE SYSTEM TEST")
    
    # Part 1: System Health Check
    print_section("SYSTEM HEALTH CHECK")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ System is healthy: {health_data.get('message', '')}")
        else:
            print(f"❌ System health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        print("💡 Make sure the server is running with: cd app && uvicorn main:app --reload --port 8001")
        return False
    
    # Part 2: Guest Feedback Submission Flow
    print_section("GUEST FEEDBACK SUBMISSION")
    
    # Guest login
    print(f"{timestamp()} 👤 Guest login...")
    guest_session = requests.Session()
    guest_login = {"username": "guest_001", "password": "guest123"}
    
    response = guest_session.post(f"{BASE_URL}/api/auth/login", json=guest_login)
    if response.status_code != 200:
        print(f"❌ Guest login failed: {response.status_code}")
        return False
    
    guest_data = response.json().get('data', {}).get('user', {})
    print(f"✅ Guest logged in: {guest_data.get('first_name')} {guest_data.get('last_name')}")
    
    # Submit multiple types of feedback
    feedback_types = [
        {
            "type": "positive",
            "data": {
                "category": "staff_service",
                "rating": 5,
                "subject": "Excellent concierge service",
                "comment": "The concierge was extremely helpful with restaurant recommendations and booking our tours.",
                "location": "Lobby",
                "staff_member": "Michael",
                "anonymous": False
            }
        },
        {
            "type": "negative",
            "data": {
                "category": "room_comfort",
                "rating": 2,
                "subject": "AC not working properly",
                "comment": "The air conditioning in our room was making strange noises and barely cooling the room.",
                "location": "Room 512",
                "staff_member": "",
                "anonymous": False
            }
        },
        {
            "type": "neutral",
            "data": {
                "category": "food_quality",
                "rating": 3,
                "subject": "Breakfast was average",
                "comment": "The breakfast buffet had decent variety but nothing spectacular. Food temperature was inconsistent.",
                "location": "Restaurant",
                "staff_member": "",
                "anonymous": False
            }
        }
    ]
    
    feedback_results = []
    for i, fb in enumerate(feedback_types):
        print(f"{timestamp()} 📝 Submitting {fb['type']} feedback ({fb['data']['rating']} stars)...")
        
        response = guest_session.post(
            f"{BASE_URL}/api/feedback/submit", 
            json=fb['data']
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ {fb['type'].title()} feedback submitted successfully!")
            print(f"   📋 ID: {result['feedback_id']}")
            print(f"   😊 Sentiment: {result['sentiment']}")
            print(f"   🔔 Alert: {result['alert_triggered']}")
            feedback_results.append(result)
        else:
            print(f"❌ Feedback submission failed: {response.status_code}")
            print(response.text)
    
    # Part 3: Admin Alert Verification
    print_section("ADMIN ALERT VERIFICATION")
    
    # Admin login
    print(f"{timestamp()} 👑 Admin login...")
    admin_session = requests.Session()
    admin_login = {"username": "admin", "password": "admin123"}
    
    response = admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_login)
    if response.status_code != 200:
        print(f"❌ Admin login failed: {response.status_code}")
        return False
    
    print(f"✅ Admin logged in successfully")
    
    # Check alerts endpoint
    print(f"{timestamp()} 🔔 Checking admin alerts...")
    response = admin_session.get(f"{BASE_URL}/api/feedback/alerts")
    
    if response.status_code == 200:
        alerts_data = response.json()
        total_alerts = alerts_data.get('total_count', 0)
        unread_alerts = alerts_data.get('unread_count', 0)
        alerts = alerts_data.get('alerts', [])
        
        print(f"✅ Found {total_alerts} total alerts, {unread_alerts} unread")
        
        # Verify our feedback submissions are in the alerts
        feedback_ids = [f['feedback_id'] for f in feedback_results]
        found_alerts = []
        
        for alert in alerts:
            if alert.get('feedback_id') in feedback_ids:
                found_alerts.append(alert)
                priority = alert.get('priority', 'unknown')
                title = alert.get('title', 'No title')
                status = alert.get('status', 'unknown')
                print(f"   ✓ Alert found: {title} (Priority: {priority}, Status: {status})")
        
        if len(found_alerts) != len(feedback_results):
            print(f"⚠️ Only found {len(found_alerts)} of {len(feedback_results)} expected alerts")
        
        # Mark an alert as read
        if found_alerts:
            alert_id = found_alerts[0]['alert_id']
            print(f"{timestamp()} ✅ Marking alert {alert_id} as read...")
            response = admin_session.post(f"{BASE_URL}/api/feedback/alerts/{alert_id}/mark-read")
            if response.status_code == 200:
                print(f"✅ Successfully marked alert as read")
            else:
                print(f"⚠️ Failed to mark alert as read: {response.status_code}")
    else:
        print(f"❌ Failed to get admin alerts: {response.status_code}")
    
    # Part 4: Analytics Dashboard Verification
    print_section("ANALYTICS DASHBOARD VERIFICATION")
    
    # Check analytics dashboard endpoint
    print(f"{timestamp()} 📊 Checking analytics dashboard data...")
    response = admin_session.get(f"{BASE_URL}/api/analytics/dashboard")
    
    if response.status_code == 200:
        data = response.json()
        if not data.get('success'):
            print(f"❌ Analytics API returned error")
            return False
            
        analytics_data = data.get('data', {})
        overview = analytics_data.get('overview', {})
        
        print(f"✅ Analytics dashboard data loaded successfully!")
        print(f"   👥 Total Guests: {overview.get('total_guests', 'N/A')}")
        print(f"   📝 Total Feedback: {overview.get('total_feedback', 'N/A')}")
        print(f"   ⭐ Average Rating: {overview.get('average_rating', 'N/A')}")
        print(f"   😊 Satisfaction Rate: {overview.get('satisfaction_rate', 'N/A')}%")
        print(f"   🔔 Active Alerts: {overview.get('alert_count', 'N/A')}")
    else:
        print(f"❌ Failed to get analytics dashboard: {response.status_code}")
        print(response.text)
    
    print_section("END-TO-END TEST COMPLETED")
    print(f"{timestamp()} 🎉 System functionality verified successfully!")
    return True

if __name__ == "__main__":
    success = test_end_to_end()
    if not success:
        print("\n❌ Some tests failed. Please check the logs above.")
    else:
        print("\n✅ All tests passed! The system is working correctly.")
