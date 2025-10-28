@echo off
echo Setting up Simple Chatbot Backend...
cd /d "E:\chatbot\chatbot-mvp\Chatbot\backend"
call venv\Scripts\activate.bat
pip install -r requirements_simple.txt
echo Setup complete!
pause