@echo off
echo Starting AI Chatbot Backend (Hybrid Mode - Memory + Supabase)...
cd /d "E:\chatbot\chatbot-mvp\Chatbot - Copy\backend"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the hybrid backend
uvicorn main_hybrid:app --reload --host 0.0.0.0 --port 8000