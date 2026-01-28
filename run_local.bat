@echo off
echo Starting local test server...
echo Opening browser in 2 seconds...
start "" http://localhost:8000
timeout /t 2 /nobreak >nul
python main.py
pause
