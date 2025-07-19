@echo off
echo 🎬 Starting Story-to-Video Generator Frontend...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if package.json exists
if not exist "package.json" (
    echo ❌ package.json not found. Please run this script from the frontend-nextjs directory.
    pause
    exit /b 1
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    echo 🔧 Creating .env.local file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
)

echo ✅ Starting development server...
echo 🌐 Frontend will be available at: http://localhost:3000
echo 🔗 Make sure the backend API is running on: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

npm run dev 