@echo off
REM Blink - Quick Setup for Windows
REM Copy and paste these commands to get started

cls
echo ==========================================
echo Blink - Quick Setup for Windows
echo ==========================================
echo.

echo Step 1: Create virtual environment
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create venv. Make sure Python is installed.
    echo Get Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Step 2: Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate venv
    pause
    exit /b 1
)

echo.
echo Step 3: Install dependencies
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 4: Configure API token
echo Running setup helper...
python setup.py
if errorlevel 1 (
    echo [ERROR] Setup failed
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo You can now run Blink:
echo   python main.py
echo.
pause
