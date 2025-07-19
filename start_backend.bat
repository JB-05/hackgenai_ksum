@echo off
echo ========================================
echo Starting Story-to-Video Backend Server
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check Python version for ElevenLabs compatibility
echo Checking Python version...
python -c "import sys; version=sys.version_info; print(f'Python {version.major}.{version.minor}.{version.micro}'); exit(0 if version.major==3 and version.minor in [10,11,12] else 1)"
if errorlevel 1 (
    echo WARNING: Python 3.13 detected. ElevenLabs may have compatibility issues.
    echo Recommended: Use Python 3.10, 3.11, or 3.12 for best compatibility.
    echo Continuing anyway...
    echo.
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Test imports first
echo Testing imports...
python test_imports.py
if errorlevel 1 (
    echo ERROR: Import test failed. Please check the errors above.
    echo.
    echo If you see ElevenLabs import errors with Python 3.13:
    echo 1. Consider downgrading to Python 3.11 or 3.12
    echo 2. Or try: pip install --upgrade elevenlabs pydantic
    echo.
    pause
    exit /b 1
)

REM Test backend functionality
echo Testing backend functionality...
python test_backend_fixed.py
if errorlevel 1 (
    echo WARNING: Backend test failed. Continuing anyway...
)

REM Start the server
echo Starting FastAPI server...
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Test Page: http://localhost:8000/test_downloads.html
echo.
echo Press Ctrl+C to stop the server
echo.

cd api
python main.py

pause 