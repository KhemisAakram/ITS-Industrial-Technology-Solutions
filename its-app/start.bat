@echo off
rem ============================================================
rem  ITS Command Center - local web app (double-click to run)
rem  Your ITS Profile folder IS the database.
rem  Opens http://localhost:5000 in your browser.
rem ============================================================
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install it from https://www.python.org
  pause
  exit /b 1
)

python -c "import flask, openpyxl, yaml" 2>nul
if errorlevel 1 (
  echo Installing required packages once...
  python -m pip install flask openpyxl PyYAML
)

start "" "http://localhost:5000"
python app.py
pause