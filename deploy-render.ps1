# Deploy to Render.com - Quick Setup Script
Write-Host "Preparing deployment to Render.com..." -ForegroundColor Cyan

# Check if we're in a git repository
if (!(Test-Path .git)) {
    Write-Host "Not in a git repository. Run 'git init' first." -ForegroundColor Red
    exit 1
}

Write-Host "Checking required files..." -ForegroundColor Yellow

if (Test-Path "render.yaml") { Write-Host "✓ render.yaml exists" -ForegroundColor Green } else { Write-Host "✗ render.yaml missing" -ForegroundColor Red }
if (Test-Path "requirements-render.txt") { Write-Host "✓ requirements-render.txt exists" -ForegroundColor Green } else { Write-Host "✗ requirements-render.txt missing" -ForegroundColor Red }
if (Test-Path "Dockerfile") { Write-Host "✓ Dockerfile exists" -ForegroundColor Green } else { Write-Host "✗ Dockerfile missing" -ForegroundColor Red }
if (Test-Path "app/main.py") { Write-Host "✓ app/main.py exists" -ForegroundColor Green } else { Write-Host "✗ app/main.py missing" -ForegroundColor Red }

Write-Host "Committing changes to git..." -ForegroundColor White
git add .
git commit -m "Prepare for Render deployment"
git push origin main

Write-Host ""
Write-Host "Ready for Render deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://render.com" -ForegroundColor White
Write-Host "2. Sign up with GitHub" -ForegroundColor White
Write-Host "3. Click 'New +' -> 'Web Service'" -ForegroundColor White
Write-Host "4. Connect your Infosys-Project repository" -ForegroundColor White
Write-Host "5. Use these build settings:" -ForegroundColor White
Write-Host "   Build Command: pip install -r requirements-render.txt" -ForegroundColor Gray
Write-Host "   Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT" -ForegroundColor Gray
Write-Host ""
Write-Host "Environment variables to set:" -ForegroundColor Yellow
Write-Host "   SECRET_KEY=your-secret-key" -ForegroundColor Gray
Write-Host "   HF_API_TOKEN=your-huggingface-token (optional)" -ForegroundColor Gray
