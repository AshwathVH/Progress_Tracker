@echo off
title ML/GenAI Progress Tracker - Backend Server
color 0A

echo.
echo ============================================================
echo    🚀 ML/GenAI Progress Tracker Backend
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo    Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if requirements are installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo ✅ Dependencies ready
echo.

echo ============================================================
echo Starting Backend Server...
echo ============================================================
echo.
echo 🌐 Server URL: http://localhost:5000
echo 💾 Database: progress_tracker.db
echo.
echo ✅ Frontend: Open ML_GenAI_Roadmap.html in your browser
echo.
echo ⚠️  IMPORTANT: Keep this window open while studying!
echo    If you close this, the database connection will stop.
echo.
echo ============================================================
echo.

python app.py

pause
