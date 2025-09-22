"""
Listing — Parallel batch execution with MultiCoreManager
=======================================================

Purpose
-------
Demonstrate how to execute many APSIM NG simulations in parallel using
:class:`apsimNGpy.core.mult_cores.MultiCoreManager`, aggregate results, and
retrieve outputs as pandas DataFrames.

What this script does
---------------------
1) Creates a demo working directory under ``BASE_DIR/demo`` and a SQLite database
   path (``demo.db``) to store results.
2) Loads a base APSIM NG *Maize* model from disk via ``load_crop_from_disk(...)``.
3) Materializes a list of **independent jobs** by copying the base model to
   unique files (``_0_.apsimx``, ``_1_.apsimx``, …).  Each copied file is a
   runnable simulation unit.
4) Instantiates **MultiCoreManager** with the database location and an
   aggregation function (``agg_func='mean'``).
5) Runs all jobs in parallel with a user-specified core count
   (``n_cores=4``, process-based unless ``threads=True``) and optionally
   clears any previous DB content (``clear_db=True``).
6) Cleans the scratch workspace used during parallel execution.
7) Retrieves results via:
   - ``get_simulated_output(axis=0)`` (aggregated view), and
   - ``results`` (raw/combined DataFrame).

Inputs & assumptions
--------------------
- ``BASE_DIR`` and ``logger`` are provided by your local ``config`` module.
- ``load_crop_from_disk(model_name, out=...)`` returns a path to a runnable
  APSIM NG ``.apsimx`` file for the requested crop template (here: "Maize").
- MultiCoreManager handles launching APSIM NG processes and persisting outputs
  into the SQLite database at ``data_base``.
- The **order of imports inside ``if __name__ == "__main__":``** is kept as-is
  to avoid side effects and to remain multiprocessing-safe on Windows.

Outputs
-------
- SQLite database: ``BASE_DIR/demo/demo.db`` (simulation outputs and metadata).
- In-memory results:
  - ``df = task_manager.get_simulated_output(axis=0)``  → aggregated DataFrame
  - ``data = task_manager.results``                     → detailed/combined DataFrame
- Log messages describing progress and completion.

Notes
-----
- On Windows, the guarded main block (``if __name__ == "__main__":``) is required
  for safe multiprocessing. If needed, add ``from multiprocessing import freeze_support; freeze_support()``.
- ``n_cores`` controls parallelism; set ``threads=True`` to switch to threads if
  your APSIM runner benefits from I/O-bound concurrency.
- ``clear_db=True`` wipes prior runs in the same database; set to ``False`` if
  you want to append runs instead.
- The demo creates 100 identical jobs by file copy; in real studies, generate
  model variants (treatments) before submitting.

"""
import math
import shutil
import os
from config_utils import NotEnoughCpuCores

if os.cpu_count() == 1:  # although uncommon today
    raise NotEnoughCpuCores('No need to test a single cpu core for apsimNGpy multiprocessing')

if __name__ == "__main__":
    # running code below this guard implies that line is executed once for all processes, the code above is executed
    # once for all processes
    CPU = int(max(2, math.ceil(os.cpu_count() * 0.85)))  # I know math.ceil return an approximate int, but safety is
    # better than confidence,
    # please maintain the oder of imports here
    from config import logger, BASE_DIR  # loaded here to avoid repetitive logs in multi-processing mode

    from apsimNGpy.core.mult_cores import MultiCoreManager
    from apsimNGpy.core.config import load_crop_from_disk

    logger.info('Loading data for parallel processing..')
    base_dir = BASE_DIR / 'demo'
    base_dir.mkdir(parents=True, exist_ok=True)
    # create some jobs for the demo
    data_base = base_dir / 'demo.db'
    CHUNK_size = int(CPU * 30)
    try:
        data_base.unlink(missing_ok=True)
    except PermissionError:
        pass
    base_model = load_crop_from_disk("Maize", out=base_dir / "base.apsimx")
    create_jobs = [shutil.copy2(base_model, str(base_dir / f'_{i}_.apsimx')) for i in range(CHUNK_size)]
    # initialize multicore manager
    task_manager = MultiCoreManager(str(data_base), agg_func='mean')
    # run all jobs
    task_manager.run_all_jobs(create_jobs, n_cores=CPU, threads=False, clear_db=True)
    # clear scratch directory
    task_manager.clear_scratch()
    # get the results
    df = task_manager.get_simulated_output(axis=0)
    # same as
    data = task_manager.results
    logger.info('successfully completed listing 3')
