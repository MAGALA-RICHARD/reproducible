@echo off
setlocal enabledelayedexpansion

REM --- Ensure Python is available ---
where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found on PATH.
  exit /b 1
)

REM --- Create venv if it doesn't exist ---
if not exist ".venv" (
  echo [INFO] Creating virtual environment .venv ...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    exit /b 1
  )
)

REM --- Activate venv (CMD) ---
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo [ERROR] Failed to activate virtual environment.
  exit /b 1
)

REM --- (Optional) Upgrade packaging tools ---
python -m pip install --upgrade pip setuptools wheel

REM --- Install requirements ---
if exist "requirements.txt" (
  echo [INFO] Installing from requirements.txt ...
  pip install -r requirements.txt
  if errorlevel 1 (
    echo [ERROR] pip install failed.
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
      exit /b 1
    )
  ) else (
    echo [WARN] Missing script %%S
  )
)

echo [OK] All scripts completed successfully.
endlocal
