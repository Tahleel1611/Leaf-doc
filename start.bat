@echo off
REM Quick start script for LeafDoc API

echo ========================================
echo LeafDoc API - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if requirements are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Create directories
echo Creating storage directories...
if not exist "storage\images" mkdir storage\images
if not exist "storage\heatmaps" mkdir storage\heatmaps
if not exist "models" mkdir models
echo.

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo.
)

REM Run migrations
echo Running database migrations...
alembic upgrade head
echo.

REM Seed database (optional)
set /p SEED="Seed database with sample data? (y/n): "
if /i "%SEED%"=="y" (
    echo Seeding database...
    python seed_db.py 10
    echo.
)

echo ========================================
echo Starting LeafDoc API...
echo ========================================
echo.
echo API will be available at:
echo   - http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
