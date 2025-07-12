#!/usr/bin/env python3
"""
Test that admin dashboard is rendering correctly
"""

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8001"

def test_admin_dashboard_rendering():
    """Test that the admin dashboard HTML is rendering correctly"""
    
    print("🧪 Testing Admin Dashboard Rendering")
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
    
    # Step 2: Fetch admin dashboard page
    print("\n2️⃣ Loading admin dashboard page...")
    response = admin_session.get(f"{BASE_URL}/admin")
    
    if response.status_code != 200:
        print(f"❌ Failed to load admin dashboard page: {response.status_code}")
        return False
    
    # Step 3: Check for 'Loading analytics dashboard...' text
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check for the loading message
    loading_element = soup.select_one('#analytics-dashboard .loading p')
    if loading_element and "Loading analytics dashboard..." in loading_element.text:
        print("ℹ️ Found 'Loading analytics dashboard...' message in the initial HTML")
        print("   This is expected as analytics are loaded via JavaScript")
    
    # Check if dashboard structure is correct
    dashboard_element = soup.select_one('#analytics-dashboard')
    if dashboard_element:
        print("✅ Found analytics dashboard element")
    else:
        print("❌ Could not find analytics dashboard element")
        return False
    
    # Check for required JS scripts
    main_js = soup.select_one('script[src*="main.js"]')
    if main_js:
        print("✅ Found main.js script reference")
    else:
        print("❌ Missing main.js script reference")
        return False
    
    chart_js = soup.select_one('script[src*="chart.js"]')
    if chart_js:
        print("✅ Found Chart.js library reference")
    else:
        print("❌ Missing Chart.js library reference")
        return False
    
    # Check for alerts section
    alerts_section = soup.select_one('.alerts-section')
    if alerts_section:
        print("✅ Found alerts section")
    else:
        print("❌ Could not find alerts section")
        return False
    
    print("\n✅ Admin dashboard structure looks correct!")
    print("   Analytics data is loaded via JavaScript after page load")
    return True

if __name__ == "__main__":
    print("🚀 Testing Admin Dashboard Rendering")
    
    success = test_admin_dashboard_rendering()
    
    if success:
        print("\n🎉 Admin dashboard page structure is correct!")
        print("   Note: For full functionality testing, please manually verify in a browser")
    else:
        print("\n❌ Issues detected with admin dashboard page structure")
    
    print("\n🏁 Test Complete!")
