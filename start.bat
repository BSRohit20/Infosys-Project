@echo off
echo Running AI-Driven Guest Experience System locally

REM Check for Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH! Please install Python.
    pause
    exit /b
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating new virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the application
echo Starting FastAPI server at http://localhost:8000
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
