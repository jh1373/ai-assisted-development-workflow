@echo off
setlocal
title Project Structure Map
cd /d "%~dp0"

set "PYTHON_COMMAND="
where py >nul 2>&1
if not errorlevel 1 (
  py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
  if not errorlevel 1 set "PYTHON_COMMAND=py -3"
)

if not defined PYTHON_COMMAND (
  where python >nul 2>&1
  if not errorlevel 1 (
    python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
    if not errorlevel 1 set "PYTHON_COMMAND=python"
  )
)

if not defined PYTHON_COMMAND (
  echo [ERROR] Python 3.10 or later was not found.
  echo Install or update Python, then double-click this file again.
  echo.
  pause
  exit /b 1
)

echo Starting Project Structure Map...
echo Keep this window open while using the viewer.
echo Press Ctrl+C in this window to stop it.
echo.

%PYTHON_COMMAND% scripts\project-structure.py serve --open-browser
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
  echo.
  echo [ERROR] Project Structure Map could not start.
  echo Review the error above, then press any key to close this window.
  pause >nul
)

exit /b %EXIT_CODE%
