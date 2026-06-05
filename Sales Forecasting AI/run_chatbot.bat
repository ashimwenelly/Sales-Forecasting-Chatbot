@echo off
REM Sales Forecasting AI Chatbot Startup Script

echo.
echo ====================================================
echo   Sales Forecasting AI Chatbot
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
echo.
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully

echo.
echo [2/3] Starting FastAPI server...
echo.
echo The server will start on http://localhost:8000
echo.
python -m uvicorn chatbot_backend:app --reload --host 0.0.0.0 --port 8000
