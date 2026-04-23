@echo off
title RZD Service Desk
echo ================================
echo    RZD Service Desk - Start
echo ================================
cd /d "%~dp0backend"
start "RZD Backend" python app.py
cd /d "%~dp0frontend"
start "RZD Frontend" npm run dev -- --host
echo Ready! Backend: localhost:5000, Frontend: localhost:5173
pause