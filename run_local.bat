@echo off
echo 🚀 Running the AI-Driven Guest Experience System locally

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist "env\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call env\Scripts\activate.bat
) else (
    echo 🔧 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

REM Start the FastAPI server
echo 🌐 Starting FastAPI server at http://localhost:8000
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
