Reproducible Tests for apsimNGpy
================================

Scope
-----
This folder provides a minimal, reproducible environment for testing **apsimNGpy**.
It targets **Windows** only because the bundled APSIM binaries are compiled for Windows.

Cross-platform use (macOS/Linux)
--------------------------------
This repository is prepared for Windows only, but you can still run it on **macOS** or **Linux**.
You will need to install APSIM NG for your platform (or build it), then follow the normal steps and
**supply the APSIM binary path** using ``set_apsim_bin_path``:

.. code-block:: python

   from apsimNGpy.core import config
   config.set_apsim_bin_path("/path/to/APSIM/bin", verbose=True)

Prerequisites
-------------
- Windows 10 or 11 (recommended windows 11)
- Python 3.10+ (recommended: 3.11 - 3.13)
- Git (to clone this repository)
- .NET 8.0 (install from https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

Quick Start (recommended)
-------------------------
**This is the fastest path.** It installs dependencies and runs the examples automatically.

1. Open **Command Prompt** and run:

   .. code-block:: bat

      git clone https://github.com/MAGALA-RICHARD/reproducible.git
      cd reproducible
      start set_up.bat

2. When the script finishes, the environment is prepared and the example listings will run.
   If the window closes immediately, re-run from an already-open Command Prompt.

Manual Setup (command line)
---------------------------
If you prefer to run steps yourself:

1. Clone the repository:

   .. code-block:: bat

      git clone https://github.com/MAGALA-RICHARD/reproducible.git
      cd reproducible

2. Create and activate a virtual environment:

   .. code-block:: bat

      python -m venv .venv
      REM Activate it:
      REM Windows (PowerShell):
      .\.venv\Scripts\Activate.ps1
      REM Windows (CMD):
      call .venv\Scripts\activate.bat

3. (Optional) Upgrade packaging tools:

   .. code-block:: bat

      python -m pip install --upgrade pip setuptools wheel

4. Install pinned dependencies:

   .. code-block:: bat

      pip install -r requirements.txt

5. Run the example listings (all scripts live in the ``reproducible`` folder):

   .. code-block:: bat

      python listing_1.py
      python listing_2.py
      python listing_3.py
      python performance_analysis.py

Using uv (optional)
-------------------
If you prefer the faster ``uv`` installer:

.. code-block:: bat

   python -m pip install -U uv
   uv pip install -r requirements.txt

Jupyter Notebook (optional)
---------------------------
If you want to explore the notebook interactively:

1. Ensure Jupyter is installed (either via ``requirements.txt`` or manually):

   .. code-block:: bat

      pip install jupyter

2. Launch the notebook (replace the filename if yours differs):

   .. code-block:: bat

      jupyter notebook jupiter_note_book_tests.ipynb

Notes
-----
- This directory targets Windows only. For macOS or Linux, install or build APSIM NG for your platform
  and set the binary path via ``set_apsim_bin_path`` (see *Cross-platform use* above).
- Ensure Git is installed and available on your PATH before cloning.
- Also, check the APSIM NG installation procedure for each of these platform: MacOS: https://apsimnextgeneration.netlify.app/install/macos
linnux: https://apsimnextgeneration.netlify.app/install/linux


Troubleshooting
---------------
- **Packages fail to install**: confirm the virtual environment is active, then rerun ``pip install -r requirements.txt``.
- **APSIM binaries not found**: verify the expected folder layout and any environment variables or configuration used by your setup
  (e.g., paths referenced in ``config.py``). On macOS/Linux, ensure you set ``set_apsim_bin_path`` correctly.
- **APSIM version**: if needed, (re)install APSIM (e.g., build 7844) and provide the path in your configuration.
- **PowerShell execution policy**: if activation fails in PowerShell, run it with
  ``-ExecutionPolicy Bypass`` or use CMD: ``call .venv\Scripts\activate.bat``.
