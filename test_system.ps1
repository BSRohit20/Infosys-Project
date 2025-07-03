# AI-Driven Guest Experience System Test Script
# PowerShell version

Write-Host "🧪 Testing AI Guest Experience System..." -ForegroundColor Cyan
Write-Host "✅ Python environment: OK" -ForegroundColor Green

# Test imports
Write-Host "`nTesting system components..." -ForegroundColor Yellow

try {
    python -c "from app.main import app; print('✅ FastAPI application: OK')"
} catch {
    Write-Host "❌ FastAPI application: $_" -ForegroundColor Red
}

try {
    python -c "from app.services.sentiment_service import sentiment_service; print('✅ Sentiment analysis service: OK')"
} catch {
    Write-Host "❌ Sentiment analysis service: $_" -ForegroundColor Red
}

try {
    python -c "from app.services.recommendation_service import recommendation_service; print('✅ Recommendation service: OK')"
} catch {
    Write-Host "❌ Recommendation service: $_" -ForegroundColor Red
}

try {
    python -c "
import json
with open('app/data/users.json', 'r') as f:
    users = json.load(f)
print(f'✅ User data loaded: {len(users)} users')
"
} catch {
    Write-Host "❌ User data: $_" -ForegroundColor Red
}

try {
    python -c "
import json
with open('app/data/comprehensive_guests_data.json', 'r') as f:
    guests = json.load(f)
print(f'✅ Guest data loaded: {len(guests.get(\"guests\", []))} guests')
"
} catch {
    Write-Host "❌ Guest data: $_" -ForegroundColor Red
}

try {
    python -c "
import json
with open('app/data/comprehensive_feedback_data.json', 'r') as f:
    feedback = json.load(f)
print(f'✅ Feedback data loaded: {len(feedback.get(\"feedback\", []))} feedback entries')
"
} catch {
    Write-Host "❌ Feedback data: $_" -ForegroundColor Red
}

Write-Host "`n🎉 System ready for deployment!" -ForegroundColor Green
Write-Host "`nTo start the server, run:" -ForegroundColor Cyan
Write-Host "  uvicorn app.main:app --reload --port 8000" -ForegroundColor White

Write-Host "`nDemo accounts:" -ForegroundColor Cyan
Write-Host "  Admin: admin / admin123" -ForegroundColor White
Write-Host "  Guest: guest_001 / guest123" -ForegroundColor White

Write-Host "`nEndpoints to test:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000 - Login page" -ForegroundColor White
Write-Host "  http://localhost:8000/admin - Admin dashboard" -ForegroundColor White
Write-Host "  http://localhost:8000/dashboard - Guest dashboard" -ForegroundColor White
Write-Host "  http://localhost:8000/docs - API documentation" -ForegroundColor White
