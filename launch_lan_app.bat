@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

REM ============================================
REM LAN Game One-Click Launcher (Windows)
REM Double-click this file to start backend+frontend
REM ============================================

set "ROOT=%~dp0"
set "BACKEND_DIR=%ROOT%backend"
set "FRONTEND_DIR=%ROOT%frontend"
set "ROOT_VENV_PY=%ROOT%.venv\Scripts\python.exe"
set "BACKEND_VENV_PY=%BACKEND_DIR%\.venv\Scripts\python.exe"
set "BACKEND_PY="

REM -------- Resolve host LAN IP (best effort) --------
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /R /C:"IPv4 Address"') do (
  set "RAW_IP=%%i"
  set "RAW_IP=!RAW_IP: =!"
  if not "!RAW_IP!"=="" if /I not "!RAW_IP!"=="127.0.0.1" (
    set "LAN_IP=!RAW_IP!"
    goto :ip_found
  )
)

:ip_found
if "%LAN_IP%"=="" set "LAN_IP=127.0.0.1"

echo.
echo [LAN-GAME] Starting services...
echo [LAN-GAME] Backend URL for this PC: http://127.0.0.1:8000
echo [LAN-GAME] Frontend URL for this PC: http://127.0.0.1:5173
echo [LAN-GAME] Share this URL with LAN users: http://%LAN_IP%:5173
echo.

REM -------- Backend checks --------
if not exist "%BACKEND_DIR%\manage.py" (
  echo [ERROR] backend\manage.py not found.
  pause
  exit /b 1
)

if exist "%BACKEND_VENV_PY%" (
  set "BACKEND_PY=%BACKEND_VENV_PY%"
) else if exist "%ROOT_VENV_PY%" (
  set "BACKEND_PY=%ROOT_VENV_PY%"
) else (
  where py >nul 2>&1
  if not errorlevel 1 (
    set "BACKEND_PY=py"
  ) else (
    where python >nul 2>&1
    if not errorlevel 1 (
      set "BACKEND_PY=python"
    )
  )
)

if "%BACKEND_PY%"=="" (
  echo [ERROR] Could not find a Python executable for backend.
  echo         Checked:
  echo           - backend\.venv\Scripts\python.exe
  echo           - .venv\Scripts\python.exe
  echo           - py launcher on PATH
  echo           - python on PATH
  echo         Ask setup person to run initial install once.
  pause
  exit /b 1
)

REM -------- Frontend checks --------
if not exist "%FRONTEND_DIR%\package.json" (
  echo [ERROR] frontend\package.json not found.
  pause
  exit /b 1
)

where node >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Node.js is not installed or not on PATH.
  echo         Install Node.js LTS once on this host.
  pause
  exit /b 1
)

REM -------- Start backend in new window --------
start "LAN Backend" cmd /k "cd /d ""%BACKEND_DIR%"" && %BACKEND_PY% manage.py runserver 0.0.0.0:8000"

REM -------- Start frontend in new window --------
start "LAN Frontend" cmd /k "cd /d ""%FRONTEND_DIR%"" && npm run dev -- --host 0.0.0.0 --port 5173"

REM Give Vite a short head start before opening browser
ping -n 3 127.0.0.1 >nul
start "" "http://127.0.0.1:5173"

echo [LAN-GAME] Done. Keep the two opened windows running.
echo [LAN-GAME] Close those windows to stop the app.
echo.
pause
