# Enhanced Render Deployment Script with CLI Support
Write-Host "🚀 Render.com Deployment Options" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Check for npm (needed for Render CLI)
$npmAvailable = Get-Command npm -ErrorAction SilentlyContinue
if ($npmAvailable) {
    Write-Host "✓ npm available - CLI deployment possible" -ForegroundColor Green
} else {
    Write-Host "⚠ npm not found - CLI deployment not available" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Choose deployment method:" -ForegroundColor Yellow
Write-Host "1. Render CLI (fastest - automated)" -ForegroundColor White
Write-Host "2. Web Dashboard (recommended for first time)" -ForegroundColor White
Write-Host "3. Git push + YAML (current setup)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        if (!$npmAvailable) {
            Write-Host "❌ npm required for CLI deployment. Choose option 2 or 3." -ForegroundColor Red
            exit 1
        }
        
        Write-Host "Installing Render CLI..." -ForegroundColor Cyan
        npm install -g "@render.com/cli"
        
        Write-Host "Preparing deployment..." -ForegroundColor Cyan
        git add .
        git commit -m "Deploy via Render CLI"
        git push origin main
        
        Write-Host ""
        Write-Host "🔑 Next steps:" -ForegroundColor Yellow
        Write-Host "1. Run: render login" -ForegroundColor White
        Write-Host "2. Run: render deploy" -ForegroundColor White
        Write-Host ""
        Write-Host "Or create service directly:" -ForegroundColor Yellow
        Write-Host "render create web --name ai-hospitality-system --build-command 'pip install -r requirements-render.txt' --start-command 'python -m uvicorn app.main:app --host 0.0.0.0 --port `$PORT'" -ForegroundColor Gray
    }
    
    "2" {
        Write-Host "Preparing for web dashboard deployment..." -ForegroundColor Cyan
        git add .
        git commit -m "Deploy to Render via dashboard"
        git push origin main
        
        Write-Host ""
        Write-Host "🌐 Web Dashboard Steps:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://render.com" -ForegroundColor White
        Write-Host "2. Sign up with GitHub" -ForegroundColor White
        Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor White
        Write-Host "4. Connect Infosys-Project repository" -ForegroundColor White
        Write-Host "5. Settings are auto-configured from render.yaml!" -ForegroundColor Green
        
        # Open browser
        Start-Process "https://render.com"
    }
    
    "3" {
        Write-Host "Using YAML-based deployment..." -ForegroundColor Cyan
        git add .
        git commit -m "Deploy with render.yaml config"
        git push origin main
        
        Write-Host ""
        Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
        Write-Host "📋 render.yaml includes all configuration:" -ForegroundColor Yellow
        Write-Host "   - Build command: pip install -r requirements-render.txt" -ForegroundColor Gray
        Write-Host "   - Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT" -ForegroundColor Gray
        Write-Host "   - Environment variables setup" -ForegroundColor Gray
        Write-Host "   - Disk storage for ML models" -ForegroundColor Gray
        Write-Host ""
        Write-Host "🌐 Just connect your GitHub repo at: https://render.com" -ForegroundColor Cyan
        
        # Open browser
        Start-Process "https://render.com"
    }
    
    default {
        Write-Host "❌ Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🔑 Environment Variables to Set in Render:" -ForegroundColor Yellow
Write-Host "   SECRET_KEY=your-secret-key" -ForegroundColor Gray
Write-Host "   HF_API_TOKEN=your-huggingface-token (optional)" -ForegroundColor Gray
Write-Host "   SLACK_WEBHOOK_URL=your-slack-webhook (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 For detailed help, see RENDER_CLI_GUIDE.md" -ForegroundColor Cyan
