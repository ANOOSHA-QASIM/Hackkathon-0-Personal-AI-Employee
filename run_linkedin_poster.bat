@echo off
REM Digital FTE - LinkedIn Poster Launcher
REM 
REM Usage: run_linkedin_poster.bat
REM
REM Prerequisites:
REM   - Python 3.11+ installed
REM   - Dependencies installed (pip install -r requirements.txt)
REM   - Playwright browser installed (playwright install chromium)

echo ============================================================
echo Digital FTE - LinkedIn Poster
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
    echo Installing Playwright browser...
    .venv\Scripts\playwright install chromium
    echo.
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if Playwright is installed
playwright install chromium >nul 2>&1

REM Run the LinkedIn poster
echo Starting LinkedIn Poster...
echo Monitoring /Approved for LinkedIn posts every 2 minutes...
echo Press Ctrl+C to stop
echo.

python src/linkedin/linkedin_poster.py

pause
