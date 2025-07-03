# AI-Driven Guest Experience System Startup Script for Local Development

Write-Host "🚀 Starting AI-Driven Guest Experience System for Local Development..." -ForegroundColor Cyan

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
} elseif (Test-Path "env\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    & .\env\Scripts\Activate.ps1
} else {
    Write-Host "⚠️ No virtual environment found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    Write-Host "📦 Installing requirements..." -ForegroundColor Green
    pip install -r requirements.txt
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️ No .env file found. Creating from .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env file. Please update with your settings." -ForegroundColor Green
    }
}

# Install dependencies if needed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
$dependenciesInstalled = $true

try {
    python -c "import fastapi, transformers, uvicorn" 2>$null
    if ($LASTEXITCODE -ne 0) {
        $dependenciesInstalled = $false
    }
} catch {
    $dependenciesInstalled = $false
}

if (-not $dependenciesInstalled) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies. Try manually:" -ForegroundColor Red
        Write-Host "  pip install fastapi uvicorn transformers torch jinja2" -ForegroundColor White
        Read-Host "Press Enter to continue anyway..."
    }
}

Write-Host "🌟 Starting FastAPI server..." -ForegroundColor Green
Write-Host "🔗 Open your browser to: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server using python -m uvicorn (most reliable method)
Write-Host "🌟 Starting server with: python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1" -ForegroundColor Green
python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1

# If the above fails, the error will be displayed and the script will end
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start server. Please ensure uvicorn is installed:" -ForegroundColor Red
    Write-Host "  pip install uvicorn" -ForegroundColor White
    Write-Host "  python -m uvicorn app.main:app --reload --port 8000" -ForegroundColor White
    Read-Host "Press Enter to exit..."
}
