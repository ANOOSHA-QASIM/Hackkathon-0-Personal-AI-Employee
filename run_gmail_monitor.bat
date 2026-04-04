@echo off
REM Digital FTE - Gmail Monitor Launcher
REM 
REM Usage: run_gmail_monitor.bat
REM
REM Prerequisites:
REM   - Python 3.11+ installed
REM   - Dependencies installed (pip install -r requirements.txt)
REM   - credentials.json in vault root (Gmail API OAuth2 credentials)

echo ============================================================
echo Digital FTE - Gmail Monitor
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo.
    echo Installing dependencies...
    .venv\Scripts\pip install -r requirements.txt
    echo.
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the Gmail monitor
echo Starting Gmail Monitor...
echo Checking for unread emails every 5 minutes...
echo Press Ctrl+C to stop
echo.

python src/gmail/gmail_monitor.py

pause
