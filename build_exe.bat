@echo off
REM Build Blink as a Windows executable (.exe)
REM This script requires Python and PyInstaller to be installed

echo.
echo ======================================================================
echo [BLINK] Building Executable
echo ======================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [HELP] Install Python from python.org
    pause
    exit /b 1
)

REM Check if venv is activated
if not defined VIRTUAL_ENV (
    echo [WARN] Virtual environment not activated
    echo.
    echo Activating venv...
    if exist venv (
        call venv\Scripts\activate.bat
    ) else (
        echo [ERROR] Virtual environment not found
        echo Please run: python -m venv venv
        pause
        exit /b 1
    )
)

REM Install PyInstaller if needed
echo [CHECK] Verifying PyInstaller installation...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing PyInstaller...
    python -m pip install pyinstaller>=6.0.0 requests pathvalidate python-dotenv
)

echo [OK] PyInstaller is ready
echo.

REM Clean old builds
echo [CLEAN] Removing old build artifacts...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist blink.spec del blink.spec
echo [OK] Cleaned old builds
echo.

REM Build the executable
echo [BUILD] Creating executable...
python -m PyInstaller ^
    --name Blink ^
    --onefile ^
    --console ^
    --add-data "src;src" ^
    --hidden-import=pathvalidate ^
    --hidden-import=requests ^
    --hidden-import=dotenv ^
    --hidden-import=token_manager ^
    --collect-all=pathvalidate ^
    --collect-all=requests ^
    --collect-all=dotenv ^
    --clean ^
    main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo [OK] Build Complete!
echo ======================================================================
echo.
echo Your executable is ready at:
echo   dist\Blink.exe
echo.
echo Next steps:
echo   1. Run it: dist\Blink.exe
echo   2. Enter your API token when prompted
echo   3. Enjoy Blink!
echo.
pause

)

echo.
echo ======================================================================
echo [OK] Build Complete!
echo ======================================================================
echo.
echo [LOCATION] Your executable is at:
echo            dist\Blink.exe
echo.
echo [READY] You can now:
echo         1. Run the exe: Blink.exe
echo         2. Share the 'dist' folder with others
echo         3. Move Blink.exe anywhere on your system
echo.
pause
