@echo off
chcp 65001 >nul 2>&1
title Python Learning Plan - Web Reader

echo ================================================
echo   Python Learning Plan - Web Reader
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Installing dependencies...
pip install flask mistune -q

if %errorlevel% neq 0 (
    echo [WARN] Dependency installation may have failed, trying to continue...
)

echo.
echo [INFO] Starting web server...
echo [INFO] Open http://localhost:5000 in your browser
echo [INFO] Press Ctrl+C to stop
echo.

python server.py

pause
