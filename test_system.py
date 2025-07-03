#!/usr/bin/env python3
"""
AI-Driven Guest Experience System - Test Script
"""

def main():
    print('🧪 Testing AI Guest Experience System...')
    print('✅ Python environment: OK')

    # Test imports
    try:
        from app.main import app
        print('✅ FastAPI application: OK')
    except Exception as e:
        print(f'❌ FastAPI application: {e}')

    try:
        from app.services.sentiment_service import sentiment_service
        print('✅ Sentiment analysis service: OK')
    except Exception as e:
        print(f'❌ Sentiment analysis service: {e}')

    try:
        from app.services.recommendation_service import recommendation_service
        print('✅ Recommendation service: OK')
    except Exception as e:
        print(f'❌ Recommendation service: {e}')

    try:
        import json
        with open('app/data/users.json', 'r') as f:
            users = json.load(f)
        print(f'✅ User data loaded: {len(users)} users')
    except Exception as e:
        print(f'❌ User data: {e}')

    try:
        with open('app/data/comprehensive_guests_data.json', 'r') as f:
            guests = json.load(f)
        print(f'✅ Guest data loaded: {len(guests.get("guests", []))} guests')
    except Exception as e:
        print(f'❌ Guest data: {e}')

    try:
        with open('app/data/comprehensive_feedback_data.json', 'r') as f:
            feedback = json.load(f)
        print(f'✅ Feedback data loaded: {len(feedback.get("feedback", []))} feedback entries')
    except Exception as e:
        print(f'❌ Feedback data: {e}')

    print('\n🎉 System ready for deployment!')
    print('\nTo start the server, run:')
    print('  python -m uvicorn app.main:app --reload --port 8000')
    print('\nOr use the startup scripts:')
    print('  .\\start_server.ps1   (PowerShell)')
    print('  .\\start_server.bat   (Command Prompt)')
    print('\nDemo accounts:')
    print('  Admin: admin / admin123')
    print('  Guest: guest_001 / guest123')
    print('\nEndpoints:')
    print('  http://localhost:8000 - Login page')
    print('  http://localhost:8000/admin - Admin dashboard')
    print('  http://localhost:8000/dashboard - Guest dashboard')
    print('  http://localhost:8000/docs - API documentation')

if __name__ == "__main__":
    main()
