@echo off
REM Digital FTE - Auto Agent Launcher
REM 
REM Usage: run_agent.bat
REM
REM Prerequisites:
REM   - Python 3.11+ installed
REM   - Dependencies installed (pip install -r requirements.txt)
REM   - GROQ_API_KEY environment variable set

echo ============================================================
echo Digital FTE - Auto Agent (Groq-powered)
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

REM Check if GROQ_API_KEY is set
if "%GROQ_API_KEY%"=="" (
    echo WARNING: GROQ_API_KEY environment variable not set
    echo The agent will use template fallback instead of AI
    echo.
    echo To use Groq AI:
    echo 1. Get API key from https://console.groq.com
    echo 2. Set: setx GROQ_API_KEY "your_api_key_here"
    echo.
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

REM Run the auto agent
echo Starting Auto Agent...
echo Monitoring /Needs_Action for email alerts...
echo Press Ctrl+C to stop
echo.

python src/agent/auto_drafter.py

pause
