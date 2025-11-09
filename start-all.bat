@echo off
REM Startup script for LeafDoc - Runs both frontend and backend

echo =========================================
echo LeafDoc - Starting Full Stack Application
echo =========================================
echo.

REM Set terminal title
title LeafDoc - Backend

REM Check if backend is set up
if not exist "backend\venv" (
    echo Setting up backend...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    if not exist ".env" copy .env.example .env
    if not exist "storage\images" mkdir storage\images
    if not exist "storage\heatmaps" mkdir storage\heatmaps
    cd ..
)

REM Check if frontend is set up
if not exist "leafdoc-plant-aid\node_modules" (
    echo Setting up frontend...
    cd leafdoc-plant-aid
    call npm install
    if not exist ".env" copy .env.example .env
    cd ..
)

echo.
echo =========================================
echo Starting Backend on http://localhost:8000
echo =========================================
echo.

REM Start backend in new window
start "LeafDoc Backend" cmd /k "cd backend && venv\Scripts\activate.bat && uvicorn app.main:app --reload"

REM Wait a bit for backend to start
timeout /t 5 /nobreak > nul

echo.
echo =========================================
echo Starting Frontend on http://localhost:5173
echo =========================================
echo.

REM Start frontend in new window
start "LeafDoc Frontend" cmd /k "cd leafdoc-plant-aid && npm run dev"

echo.
echo =========================================
echo LeafDoc Started Successfully!
echo =========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to open frontend in browser...
pause > nul

REM Open browser
start http://localhost:5173

echo.
echo Both services are running in separate windows.
echo Close those windows to stop the services.
echo.
pause
