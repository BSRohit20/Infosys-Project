#!/usr/bin/env python3
"""
Open the admin dashboard in a web browser for visual inspection
"""

import webbrowser
import requests
import time
import sys

BASE_URL = "http://localhost:8001"

def open_admin_dashboard():
    """Test that the admin dashboard can be accessed in a browser"""
    
    print("🌐 Opening Admin Dashboard in Browser")
    print("=" * 60)
    
    # Check if server is running
    try:
        print("\n1️⃣ Checking if server is running...")
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the server is running with: cd app && uvicorn main:app --reload --port 8001")
        return False
    
    # Login as admin via API to get cookies
    print("\n2️⃣ Logging in as admin...")
    admin_session = requests.Session()
    admin_login = {"username": "admin", "password": "admin123"}
    
    response = admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_login)
    if response.status_code != 200:
        print(f"❌ Admin login failed: {response.text}")
        return False
    
    print("✅ Admin logged in successfully")
    
    # Open browser to admin dashboard
    print("\n3️⃣ Opening browser to admin dashboard...")
    print("💡 NOTE: You will need to login with username 'admin' and password 'admin123'")
    print("   because browser cookies can't be passed programmatically")
    
    dashboard_url = f"{BASE_URL}/admin"
    
    try:
        # Add a delay to let the user see instructions before browser opens
        time.sleep(2)
        webbrowser.open(dashboard_url)
        print(f"✅ Browser opened to {dashboard_url}")
        
        print("\n4️⃣ Also opening admin alerts page...")
        alerts_url = f"{BASE_URL}/admin/alerts"
        time.sleep(1)
        webbrowser.open(alerts_url)
        print(f"✅ Browser opened to {alerts_url}")
        
        print("\n✅ Dashboard and Alerts pages opened in browser")
        print("💡 Please visually verify that:")
        print("   1. Dashboard analytics are displaying correctly")
        print("   2. Alerts are showing up properly")
        print("   3. Both positive and negative feedback alerts appear")
        return True
        
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        return False

if __name__ == "__main__":
    success = open_admin_dashboard()
    
    if success:
        print("\n🎉 Browser opened successfully!")
        print("   Please login with: username='admin', password='admin123'")
    else:
        print("\n❌ Failed to open browser")
        sys.exit(1)
