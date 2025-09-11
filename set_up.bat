@echo off
REM Usage:
REM   setup_venv.bat          -> setup, install, run scripts, then exit
REM   setup_venv.bat shell    -> setup, install, run scripts, then open an ACTIVATED CMD

REM --- Ensure Python is available ---
where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found on PATH.
  pause
  exit /b 1
)

REM --- Create venv if missing ---
if not exist ".venv" (
  echo [INFO] Creating virtual environment .venv ...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
  )
)

REM --- Activate venv (CMD) ---
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo [ERROR] Failed to activate virtual environment.
  pause
  exit /b 1
)

REM --- Install requirements ---
if exist "requirements.txt" (
  echo [INFO] Installing from requirements.txt ...
  pip install -r requirements.txt
  if errorlevel 1 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
  )
) else (
  echo [WARN] requirements.txt not found in %cd%.
)

REM --- Run scripts in order ---
for %%S in (listing_1.py listing_2.py listing_3.py performance_analysis.py) do (
  if exist "%%S" (
    echo [RUN] python %%S
    python "%%S"
    if errorlevel 1 (
      echo [ERROR] Script %%S failed. Aborting.
      pause
      exit /b 1
    )
  ) else (
    echo [WARN] Missing script %%S
  )
)

REM --- If you passed "shell", open an ACTIVATED CMD that stays open
if /i "%~1"=="shell" (
  echo [OK] Opening an activated shell. Close it to exit.
  cmd /k call ".venv\Scripts\activate.bat"
  exit /b 0
)

echo [OK] Done.
