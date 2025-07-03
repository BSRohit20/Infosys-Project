# Script to run the AI-Driven Guest Experience System locally
Write-Host "🚀 Running the AI-Driven Guest Experience System locally" -ForegroundColor Cyan

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
} elseif (Test-Path "env\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    & .\env\Scripts\Activate.ps1
} else {
    Write-Host "� Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    
    Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start the FastAPI server
Write-Host "🌐 Starting FastAPI server at http://localhost:8000" -ForegroundColor Green
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
