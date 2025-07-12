#!/usr/bin/env python3
"""
Test script to verify the analytics dashboard API and data loading
"""

import requests
import json
import pprint

BASE_URL = "http://localhost:8001"

def test_analytics_api():
    """Test the analytics dashboard API endpoint"""
    
    print("🧪 Testing Analytics Dashboard API")
    print("=" * 60)
    
    # Step 1: Login as admin
    print("\n1️⃣ Logging in as admin...")
    admin_session = requests.Session()
    admin_login = {"username": "admin", "password": "admin123"}
    
    response = admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_login)
    if response.status_code != 200:
        print(f"❌ Admin login failed: {response.text}")
        return False
    
    print("✅ Admin logged in successfully")
    
    # Step 2: Test analytics dashboard endpoint
    print("\n2️⃣ Fetching analytics dashboard data...")
    response = admin_session.get(f"{BASE_URL}/api/analytics/dashboard")
    
    if response.status_code != 200:
        print(f"❌ Analytics dashboard API failed: {response.status_code}")
        print(response.text)
        return False
    
    try:
        data = response.json()
        if not data.get('success'):
            print(f"❌ API returned error: {data}")
            return False
        
        analytics_data = data.get('data', {})
        
        # Check overview data
        print("\n📊 Analytics Dashboard Overview:")
        overview = analytics_data.get('overview', {})
        print(f"   Total Guests: {overview.get('total_guests', 'N/A')}")
        print(f"   Total Feedback: {overview.get('total_feedback', 'N/A')}")
        print(f"   Average Rating: {overview.get('average_rating', 'N/A')}")
        print(f"   Satisfaction Rate: {overview.get('satisfaction_rate', 'N/A')}%")
        print(f"   Alert Count: {overview.get('alert_count', 'N/A')}")
        
        # Check sentiment breakdown
        sentiment = analytics_data.get('sentiment_analysis', {})
        print("\n😊 Sentiment Breakdown:")
        print(f"   Positive: {sentiment.get('positive', 0)} ({sentiment.get('positive_percentage', 0)}%)")
        print(f"   Neutral: {sentiment.get('neutral', 0)} ({sentiment.get('neutral_percentage', 0)}%)")
        print(f"   Negative: {sentiment.get('negative', 0)} ({sentiment.get('negative_percentage', 0)}%)")
        
        # Check alerts
        alerts = analytics_data.get('recent_alerts', [])
        print(f"\n🔔 Recent Alerts: {len(alerts)}")
        for i, alert in enumerate(alerts[:3]):  # Display first 3 alerts
            print(f"   Alert {i+1}: Priority: {alert.get('priority', 'N/A')}, " +
                  f"Guest: {alert.get('guest_name', alert.get('guest_id', 'N/A'))}")
        
        print("\n✅ Analytics dashboard data loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error parsing analytics response: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Analytics Dashboard API")
    
    # Test analytics API
    success = test_analytics_api()
    
    if success:
        print("\n🎉 Analytics API is working correctly!")
    else:
        print("\n❌ Issues detected with Analytics API")
    
    print("\n🏁 Test Complete!")
