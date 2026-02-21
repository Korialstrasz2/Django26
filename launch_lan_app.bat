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
set "SYSTEM_PY="

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
echo [LAN-GAME] Preparing startup...
echo [LAN-GAME] This PC URL: http://127.0.0.1:5173
echo [LAN-GAME] Share with LAN users: http://%LAN_IP%:5173
echo.

REM -------- Project checks --------
if not exist "%BACKEND_DIR%\manage.py" (
  echo [ERROR] backend\manage.py not found.
  timeout /t 5 >nul
  exit /b 1
)

if not exist "%FRONTEND_DIR%\package.json" (
  echo [ERROR] frontend\package.json not found.
  timeout /t 5 >nul
  exit /b 1
)

REM -------- Find Python launcher on PATH for fallback/setup --------
where py >nul 2>&1
if not errorlevel 1 set "SYSTEM_PY=py"
if "%SYSTEM_PY%"=="" (
  where python >nul 2>&1
  if not errorlevel 1 set "SYSTEM_PY=python"
)

REM -------- Choose backend Python --------
if exist "%BACKEND_VENV_PY%" (
  set "BACKEND_PY=%BACKEND_VENV_PY%"
) else if exist "%ROOT_VENV_PY%" (
  set "BACKEND_PY=%ROOT_VENV_PY%"
)

REM -------- Auto-create root venv if missing --------
if "%BACKEND_PY%"=="" (
  if "%SYSTEM_PY%"=="" (
    echo [ERROR] Could not find Python to create a virtual environment.
    echo         Install Python 3, then run this launcher again.
    timeout /t 8 >nul
    exit /b 1
  )

  echo [LAN-GAME] Creating .venv (one-time setup)...
  cd /d "%ROOT%"
  %SYSTEM_PY% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create .venv.
    timeout /t 8 >nul
    exit /b 1
  )
  set "BACKEND_PY=%ROOT_VENV_PY%"
)

REM -------- Ensure backend deps are installed --------
"%BACKEND_PY%" -c "import django, channels, ninja" >nul 2>&1
if errorlevel 1 (
  echo [LAN-GAME] Installing backend dependencies (one-time setup)...
  "%BACKEND_PY%" -m pip install --upgrade pip >nul
  "%BACKEND_PY%" -m pip install -r "%BACKEND_DIR%\requirements.txt"
  if errorlevel 1 (
    echo [ERROR] Failed to install backend dependencies.
    timeout /t 8 >nul
    exit /b 1
  )
)

REM -------- Ensure frontend runtime exists --------
where node >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Node.js is not installed or not on PATH.
  echo         Install Node.js LTS once on this host.
  timeout /t 8 >nul
  exit /b 1
)

if not exist "%FRONTEND_DIR%\node_modules" (
  echo [LAN-GAME] Installing frontend dependencies (one-time setup)...
  cd /d "%FRONTEND_DIR%"
  npm install
  if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies.
    timeout /t 8 >nul
    exit /b 1
  )
)

REM -------- Start services in their own windows --------
start "LAN Backend" cmd /k "cd /d ""%BACKEND_DIR%"" && ""%BACKEND_PY%"" manage.py migrate && ""%BACKEND_PY%"" manage.py runserver 0.0.0.0:8000"
start "LAN Frontend" cmd /k "cd /d ""%FRONTEND_DIR%"" && npm run dev -- --host 0.0.0.0 --port 5173"

REM open browser (small delay)
timeout /t 3 >nul
start "" "http://127.0.0.1:5173"

REM Do not keep this launcher window open.
exit /b 0
