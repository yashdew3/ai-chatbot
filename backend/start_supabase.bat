@echo off
echo Starting AI Chatbot Backend (Supabase Edition)...
cd /d "E:\chatbot\chatbot-mvp\Chatbot - Copy\backend"

REM Activate virtual environment
echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ❌ Virtual environment not found at venv\Scripts\activate.bat
    echo Please run .\setup_supabase.bat first
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found
    echo Please run .\setup_supabase.bat first
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import supabase" >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Supabase dependencies not installed
    echo Please run .\setup_supabase.bat first
    pause
    exit /b 1
)

echo ✅ Starting server on http://localhost:8000
echo ✅ API docs available at http://localhost:8000/docs
echo ✅ Supabase integration enabled
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main_supabase:app --reload --host 0.0.0.0 --port 8000