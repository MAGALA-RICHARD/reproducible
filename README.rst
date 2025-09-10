Reproducible Tests for apsimNGpy
================================

Scope
-----
This folder provides a minimal, reproducible environment for testing **apsimNGpy**.
It is intended for **Windows** only, because the bundled APSIM binaries are compiled for Windows.

Prerequisites
-------------
- Windows 10 or 11
- Python 3.9+ (recommended 3.10–3.12)
- Git (to clone this repository)

Clone the repository
--------------------
.. code-block:: bash

   git clone https://github.com/MAGALA-RICHARD/reproducible.git
   cd reproducible

Create and activate a virtual environment
-----------------------------------------
.. code-block:: bash

   python -m venv .venv

   # Activate it
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # Windows (CMD):
   .venv\Scripts\activate.bat

Upgrade pip (optional but recommended)
-------------------------------------
.. code-block:: bash

   python -m pip install --upgrade pip setuptools wheel

Install dependencies (pinned)
-----------------------------
.. code-block:: bash

   pip install -r requirements.txt

Using uv (optional)
-------------------
.. code-block:: bash

   python -m pip install -U uv
   uv pip install -r requirements.txt

Run the example listings
------------------------
All scripts are in this folder.

.. code-block:: bash

   python listing_1.py
   python listing_2.py
   python listing_3.py
   python performance_analysis.py

Notes
-----
- This directory targets Windows only. If you need macOS or Linux, rebuild the APSIM binaries for your platform and adjust paths.
- Ensure Git is installed and available on your PATH before cloning.

Troubleshooting
---------------
- If package installation fails, confirm the virtual environment is active and retry ``pip install -r requirements.txt``.
- If a script cannot find APSIM binaries, verify the folder layout and environment variables expected by your configuration.
- you may also rebuild or install apsim version 7844 and provide the path to config.py