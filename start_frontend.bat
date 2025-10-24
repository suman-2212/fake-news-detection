@echo off
echo ============================================================
echo Starting Next.js Frontend Server
echo ============================================================
echo.

cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting Next.js on http://localhost:3000
echo Keep this window open!
echo.
echo Open your browser to: http://localhost:3000
echo.

call npm run dev

pause
