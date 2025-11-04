@echo off
echo Setting up AI Chatbot Backend with Supabase...
cd /d "E:\chatbot\chatbot-mvp\Chatbot - Copy\backend"

REM Activate virtual environment
echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ❌ Virtual environment not found at venv\Scripts\activate.bat
    echo Please create a virtual environment first or check the path
    pause
    exit /b 1
)

REM Check if Python is installed in venv
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not working in virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo Installing Python dependencies for Supabase integration...
pip install -r requirements_supabase.txt

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit the .env file and add your API keys:
    echo    - GOOGLE_API_KEY: Get from Google AI Studio
    echo    - SUPABASE_ANON_KEY: Get from your Supabase project settings
    echo.
) else (
    echo ✅ .env file already exists
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Make sure your .env file has the correct API keys
echo 2. Run: .\start_supabase.bat
echo.
pause