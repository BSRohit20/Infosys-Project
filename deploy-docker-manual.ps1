# Manual Docker Deployment Script for Render
Write-Host "🐳 DOCKER DEPLOYMENT GUIDE FOR RENDER" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Since Render keeps defaulting to Python buildpack, follow these steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Go to https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Click 'New +' → 'Web Service'" -ForegroundColor White
Write-Host "3. Connect your GitHub repo: BSRohit20/Infosys-Project" -ForegroundColor White
Write-Host "4. IMPORTANT: Select 'Docker' as the Environment (NOT Python!)" -ForegroundColor Red
Write-Host "5. Use these settings:" -ForegroundColor White
Write-Host "   - Name: ai-hospitality-docker" -ForegroundColor Gray
Write-Host "   - Environment: Docker" -ForegroundColor Gray
Write-Host "   - Build Command: (leave blank)" -ForegroundColor Gray
Write-Host "   - Start Command: (leave blank, uses Dockerfile CMD)" -ForegroundColor Gray
Write-Host "   - Plan: Free" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Environment Variables to add:" -ForegroundColor White
Write-Host "   - ENVIRONMENT=production" -ForegroundColor Gray
Write-Host "   - SECRET_KEY=(generate new)" -ForegroundColor Gray
Write-Host ""
Write-Host "7. Advanced Settings:" -ForegroundColor White
Write-Host "   - Health Check Path: /health" -ForegroundColor Gray
Write-Host "   - Dockerfile Path: ./Dockerfile" -ForegroundColor Gray
Write-Host ""
Write-Host "8. Deploy!" -ForegroundColor Green
Write-Host ""
Write-Host "This will force Render to use our Python 3.11 Docker container" -ForegroundColor Green
Write-Host "instead of their problematic Python 3.13 buildpack." -ForegroundColor Green
