@echo off
title RZD Service Desk

echo ================================
echo    RZD Service Desk - Start
echo ================================
echo.

echo [1/2] Starting Backend...
cd /d "%~dp0backend"
start "RZD Backend" cmd /k "python app.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend...
cd /d "%~dp0frontend"
start "RZD Frontend" cmd /k "npm run dev -- --host"

echo.
echo ================================
echo    Ready!
echo.
echo    Backend:  http://localhost:5000
echo    Frontend: http://localhost:5173
echo ================================
pause