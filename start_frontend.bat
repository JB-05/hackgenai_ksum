@echo off
echo Starting Story-to-Video Generator Frontend...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo Error: npm is not installed or not in PATH
    pause
    exit /b 1
)

REM Navigate to frontend directory
cd frontend-nextjs

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
)

REM Start the frontend server
echo Starting frontend server on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.
npm run dev 