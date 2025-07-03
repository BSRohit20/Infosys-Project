@echo off
echo 🚀 Starting AI-Driven Guest Experience System for Local Development...

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist "env\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call env\Scripts\activate.bat
) else (
    echo ⚠️ No virtual environment found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📦 Installing requirements...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    if exist ".env.example" (
        echo ⚠️ Creating .env file from .env.example...
        copy ".env.example" ".env"
    )
)

echo 🌟 Starting FastAPI server...
echo 🔗 Open your browser to: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Try to start with python -m uvicorn (most reliable)
python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1

REM If it fails, show error message
if errorlevel 1 (
    echo.
    echo ❌ Failed to start server. Please ensure uvicorn is installed:
    echo   pip install uvicorn
    echo   python -m uvicorn app.main:app --reload --port 8000
    pause
)
