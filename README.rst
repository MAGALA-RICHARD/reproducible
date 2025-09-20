Reproducible Tests for apsimNGpy
================================

Scope
-----
This folder provides a minimal, reproducible environment for testing **apsimNGpy**.
It targets **Windows** or MacOS only because the bundled APSIM binaries are compiled for Windows and MacOS.

Cross-platform use (macOS/Linux)
--------------------------------
This repository is prepared for Windows and MacOS (tested on intel not apple silicon), but you can still run it on  **Linux**. Although this has not been comprehensively tested
You will need to install APSIM NG for your platform (or build it), then follow the normal steps and
**supply the APSIM binary path** using ``configure_bin_path`` `from **config_utils.py**`. Noted that this is implemented in **config.py**.
So, everything should be edited in that .py file. An example usage is given below.

.. note::

    Note that if your platform is windows/Macos, no need to change this :

.. code-block:: python

   from apsimNGpy.core import config
   config.set_apsim_bin_path("/path/to/APSIM/bin", verbose=True)

Prerequisites
-------------
- Windows 10 or 11 (recommended windows 11)
- Python 3.10+ (recommended:  3.12.2)
- Git (to clone this repository)
- .NET 8.0 (install from https://dotnet.microsoft.com/en-us/download/dotnet/8.0)  see the requirements for each platform https://apsimnextgeneration.netlify.app/install/macos/

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

.. note::

   Some version of python may require specifying python3 instead of python


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

Recap
-----
- This directory targets Windows or intel-based MacOS only. For others, install or build APSIM NG for your platform
  and set the binary path via ``set_apsim_bin_path`` (see *Cross-platform use* above).
- Ensure Git is installed and available on your PATH before cloning.
- Check the APSIM NG installation procedure for each of these platform: MacOS: https://apsimnextgeneration.netlify.app/install/macos
linux: https://apsimnextgeneration.netlify.app/install/linux


Troubleshooting
---------------
- **Packages fail to install**: confirm the virtual environment is active, then rerun ``pip install -r requirements.txt``.
- **APSIM binaries not found**: verify the expected folder layout and any environment variables or configuration used by your setup
  (e.g., paths referenced in ``config.py``). On macOS/Linux, ensure you set ``set_apsim_bin_path`` correctly.
- **APSIM version**: if needed, (re)install APSIM (e.g., build 7844) and provide the path in your configuration.
- **PowerShell execution policy**: if activation fails in PowerShell, run it with
  ``-ExecutionPolicy Bypass`` or use CMD: ``call .venv\Scripts\activate.bat``.

Runtime directories
======================

demo/ – Created automatically at runtime in the project root.
Used as a scratch/workspace for examples and listings (e.g., edited .apsimx json files, and .db files, temporary inputs, quick CSVs).

results/ – Also created at runtime in the project root.
Stores persisted outputs such as simulation tables, plots, and logs you want to keep.

Behavior & customization
===============================
Both folders are created on demand if they don’t exist.

You can change their locations via config or environment variables (e.g., APSIMGN_DEMO_DIR, APSIMGN_RESULTS_DIR) or by passing explicit paths to the relevant APIs in your scripts.

On cleanup, scripts may remove temporary files in demo/, but results/ is treated as durable output and is not deleted automatically.

Ensure the process has write permissions to the chosen paths (especially in Docker/CI).

scratch directory is created by apsimNGpy internally for storing temporally files


===============================
Project Layout (``reproducible``)
===============================



Quick view
==========
Below is what to expect in each folder/file. Paths below are shown relative to the project root (e.g., ``D:\code\reproducible``).

.. code-block:: text

   .
   ├─ .idea/                       # IDE metadata (ignored by tooling)
   ├─ apsimx/                      # Working directory for APSIM NG models produced by listings
   ├─ bin_dist/                    # (Optional) distributed APSIM NG binaries / runtime stubs
   ├─ data/                        # keeps db files from the performance experiment
   ├─ demo/                        # Runtime scratch/workspace for examples (created on demand)
   ├─ Results/                     # Durable outputs (plots, CSVs) created at runtime
   ├─ scratch/                     # Ad-hoc experiments, temporary artifacts created by apsimNGpy
   ├─ __pycache__/                 # Python bytecode (auto-generated)
   ├─ .gitignore
   ├─ config.py                    # Central settings (paths, logging, environment)
   ├─ configs.ini                  # Optional INI overrides for defaults in ``config.py``
   ├─ config_utils.py              # Helpers to locate/validate APSIM NG binaries; logging utilities
   ├─ constants.py                 # Plot styles, font sizes, palettes used across scripts
   ├─ jupiter_note_book_tests.ipynb# Notebook for interactive smoke tests/demos
   ├─ lincense.txt                 # Project license
   ├─ listing_1.py                 # Listing 1: minimal APSIM NG workflow with apsimNGpy
   ├─ listing_2.py                 # Listing 2: (factorial/manager-focused) workflow
   ├─ listing_3.py                 # Listing 3: multiprocessing/parallel example (progress-aware)
   ├─ new_core_runner.py           # Shared runners/utilities for listings (e.g., data paths)
   ├─ performance_analysis.py      # Benchmark plots (cores vs. runtime, speedups)
   ├─ README.md
   ├─ README.rst                   # Long-form docs (this .rst style)
   ├─ requirements.txt             # Python dependencies
   ├─ set_up.bat                   # Windows bootstrap (env, deps)
   ├─ set_up.sh                    # POSIX bootstrap (env, deps)
   ├─ test_configuration.py        # Unit tests for APSIM bin detection/config (edge cases)
   └─ __init__.py                  # Package marker (keeps relative imports stable)

Directory details
=================

``apsimx/``
-----------

Working folder where listings write **edited** APSIM NG models (``*.apsimx``). Created when you run a listing that targets
this directory.

``bin_dist/``
-------------

If present, holds APSIM NG **runtime binaries** or a vendor snapshot used by
``config_utils.py`` to auto-detect the executable path. Contents are platform-specific
and may be excluded from version control depending on licensing.

``data/``
---------

Canonical **inputs** for simulations and examples (weather, soils, small fixtures).
Keep file names and formats stable so scripts can run reproducibly.

``demo/``  *(runtime)*
-----------------------

Created **on demand** by listings (e.g., Listing 1). Used as a scratch/workspace for:
edited ``.apsimx`` models, quick CSVs (e.g., ``simulated.csv``), and temporary
artifacts safe to delete. Scripts will create it if missing.

``Results/``  *(runtime)*
--------------------------

Durable outputs you want to **keep** (final plots, tables). Also created on demand.
Unlike ``demo/``, this directory is not automatically cleaned by scripts.

``scratch/``
------------

Ad-hoc playground for local experiments; not part of the public API. Treat as
temporary—move stabilized utilities into the codebase proper.

Key scripts & modules
=====================

``listing_1.py`` — Minimal APSIM NG workflow
--------------------------------------------

Instantiates an ``ApsimModel`` (e.g., *Maize*), inspects and edits parameters (e.g., sowing
population), fetches weather from the web, adjusts the Clock, runs the simulation,
and saves both the edited model (``my-edited-maize-model.apsimx``) and results CSV.

Outputs: written under ``demo/`` and/or ``apsimx/``.

``listing_2.py`` — Factorial/manager workflow
---------------------------------------------

Builds factorial scenarios programmatically (e.g., fertilizer amount × cultivar) using
``ExperimentManager``, executes treatments, and plots results. Figures land in ``apsimx/`` or ``Results/``.

``listing_3.py`` — Parallel execution with progress
---------------------------------------------------

Runs many simulations in parallel (multiprocessing) and shows a **tqdm** progress bar.
Prefer running as a module (``python -m listing_3`` or ``python -m package.path.listing_3``)
to keep relative imports stable. In non-TTY environments, fall back to plain updates.

``performance_analysis.py`` — Benchmark visualizations
------------------------------------------------------

Reads timing results from a SQLite DB and produces figures:

- ``f.png`` — total runtime vs. number of simulations (hue=cores)
- ``f2.png`` — seconds-per-simulation vs. number of simulations
- ``c.png`` — bar chart summary

Relies on ``constants.py`` for palettes and font sizes.

``config.py``
---------------------------------

Centralized configuration.

``config_utils.py``
-------------------

Validation and selection of the **APSIM NG binary path** across platforms.
Unit tests (``test_configuration.py``) cover edge cases such as missing executables,
unsupported OS labels, and temporary fake bin layouts.

Runtime directories
===================

These folders are **created at runtime** in the project root if missing:

- **``demo/``** — transient scratch space for examples and quick outputs.
- **``Results/``** — durable outputs (plots, tables, logs) you want to retain.

You can relocate these via config_utils.py (e.g., environment variables or explicit paths
passed to the API). Ensure the process has write permission, especially when running
inside containers or CI.

Running the listings
====================

Windows (PowerShell/CMD):

.. code-block:: bat

   rem Create/activate venv and install deps
   call set_up.bat

   rem Run listings
   py listing_1.py
   py listing_2.py
   py -m listing_3   rem use -m for multiprocessing safety

POSIX (macOS/Linux):

.. code-block:: bash

   # Create/activate venv and install deps
   bash set_up.sh

   # Run listings
   python listing_1.py
   python listing_2.py
   python -m listing_3   # module mode preferred with multiprocessing

Notes & conventions
===================

- **APSIM binaries**: ``config_utils.py`` + ``config.py`` locate executables.
  Use ``test_configuration.py`` to verify your setup if runs fail early.
- **Plots**: Scripts attempt to open images after saving.
  - Windows: ``os.startfile(...)``
  - macOS: ``open ...`` (adjust to ``xdg-open`` on Linux if needed)
- **Progress bars**: In headless/CI, tqdm may disable animation.
  The code auto-disables or degrades gracefully; you can also add a ``--no-progress`` mode.
