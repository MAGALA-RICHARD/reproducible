#!/usr/bin/env bash
# Usage:
#   ./setup_venv.sh          -> setup, install, run scripts, then exit
#   ./setup_venv.sh shell    -> setup, install, run scripts, then open an ACTIVATED shell

set -Eeuo pipefail

# --- Ensure we're running from the script's folder ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- Config ---
VENV_DIR=".venv"
PYTHON_BIN="${PYTHON:-python3}"     # allow override via: PYTHON=python3.12 ./setup_venv.sh

# --- Ensure Python is available ---
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "[ERROR] Python not found on PATH (looked for '$PYTHON_BIN')."
  echo "        Install Python 3 and/or set PYTHON=/path/to/python before running."
  exit 1
fi

# --- Create venv if missing ---
if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO] Creating virtual environment $VENV_DIR ..."
  "$PYTHON_BIN" -m venv "$VENV_DIR" || { echo "[ERROR] Failed to create virtual environment."; exit 1; }
fi

# --- Activate venv ---
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate" || { echo "[ERROR] Failed to activate virtual environment."; exit 1; }

PIP="$VENV_DIR/bin/pip"
PY="$VENV_DIR/bin/python"

# --- Install requirements ---
if [ -f "requirements.txt" ]; then
  echo "[INFO] Installing from requirements.txt ..."
  "$PIP" install -r requirements.txt || { echo "[ERROR] pip install failed."; exit 1; }
else
  echo "[WARN] requirements.txt not found in $PWD."
fi

# --- Run scripts in order ---
SCRIPTS=(listing_1.py listing_2.py listing_3.py performance_analysis.py)

for S in "${SCRIPTS[@]}"; do
  if [ -f "$S" ]; then
    echo "[RUN] $PY $S"
    "$PY" "$S" || { echo "[ERROR] Script $S failed. Aborting."; exit 1; }
  else
    echo "[WARN] Missing script $S"
  fi
done

# --- Open an ACTIVATED shell that stays open (optional) ---
if [[ "${1:-}" == "shell" ]]; then
  echo "[OK] Opening an activated shell. Type 'exit' to close."
  # Prefer the user's default shell
  exec "${SHELL:-/bin/bash}" -i
fi

echo "[OK] Done."

