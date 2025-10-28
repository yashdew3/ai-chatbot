@echo off
echo Starting Simple Chatbot Backend...
cd /d "E:\chatbot\chatbot-mvp\Chatbot - Copy\backend"
call venv\Scripts\activate.bat
uvicorn main:app --reload --host 0.0.0.0 --port 8000