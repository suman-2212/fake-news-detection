@echo off
echo ============================================================
echo Starting Flask Backend Server
echo ============================================================
echo.

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment found, using system Python
)

echo.
echo Starting Flask API on http://localhost:5000
echo Keep this window open!
echo.

python app.py

pause
