"""
Benchmarking parallel APSIM NG runs by core count and batch size
================================================================

Purpose
-------
Measure how total runtime scales with:
- **CPU cores**: {1, 4, 8, 12, 16}
- **Batch sizes**: {100, 200, 300, 500, 700, 1000, 1500}

For each (cores, size) pair, the script:
1) batch simulations `size` APSIM NG model files (Maize) into some times each placed in its folder,
2) executes them in parallel via ``MultiCoreManager``,
3) records wall-clock elapsed seconds, and
4) writes a CSV artifact to ``data/table_{cores}{size}.csv`` (one row).

Inputs & dependencies
---------------------
- **APSIM NG** accessible to ``apsimNGpy`` (Maize template available).
- ``apsimNGpy.core.apsim.ApsimModel`` for model instantiation.
- ``apsimNGpy.core.mult_cores.MultiCoreManager`` for parallel execution.
- ``config_utils.base_dir`` for project-relative paths.
- Python packages: ``pandas``, ``sqlalchemy`` (optional; see DB note).

Key variables
-------------
- ``job``: list of crop names (not used in this benchmark loop).
- ``data``: path to the project ``data/`` directory (created if missing).
- ``base``: workspace under ``<base_dir>/demo`` where per-case folders are created.
- ``prod``: Cartesian product of cores × sizes to iterate over.

Outputs
-------
- **Per-case CSV**: ``data/table_{cores}{size}.csv`` with columns:
  - ``size``  (int): number of simulations in the batch
  - ``core``  (int): worker processes used
  - ``seconds`` (float): wall-clock time to complete the batch
- **Optional (commented)**: a SQLite table write via ``insert_data_with_pd(...)`` if
  you uncomment the call; target DB would be ``data/simulated_core_size.db``.

Workflow details
----------------
- For each (core, size), a subdirectory ``demo/_{size}_{core}`` is created.
- ``size`` individual Maize models are generated and saved in that folder
  (e.g., ``{core}_{size}_{i}.apsimx``).
- A ``MultiCoreManager`` is initialized with a scratch DB (``testiy.db``), then
  ``run_all_jobs(...)`` is invoked with ``n_cores=core`` and ``threads=False``.
- Elapsed time is computed with ``time.perf_counter()`` and stored in a one-row
  DataFrame; the CSV is written under ``data/`` and used as a cache
  (subsequent runs skip existing files).

Notes & tips
------------
- **Idempotency**: If a CSV already exists for a (core, size) case, the script
  skips re-running it (simple caching).
- **Scratch cleanup**: ``Parallel.clear_scratch()`` is called before and after runs.
- **Database logging (optional)**: To aggregate results in a single SQLite DB,
  uncomment the ``insert_data_with_pd(...)`` call and ensure SQLAlchemy is installed.
- **Working directory**: The script ``chdir``s into ``demo/`` so paths are local;
  CSVs are still written to the project’s ``data/`` folder.
- **Reproducibility**: The benchmark reflects system load and I/O; run on an
  otherwise idle machine for cleaner comparisons.

Example result row
------------------
.. code-block:: text

   size,core,seconds
   300,8,123.456

"""
import os
from pathlib import Path
import pandas as pd
from apsimNGpy.core.apsim import ApsimModel
from sqlalchemy import create_engine

job = ['Maize', 'Soybean', 'Barley', 'Canola', "Wheat", 'Oats', "Potato", 'MungBean']


# --- Your loop with per-iteration saving ---

def insert_data_with_pd(db, table, results, if_exists):
    engine = create_engine(f'sqlite:///{db}')
    results.to_sql(table, engine, index=False, if_exists=if_exists)

data = Path(__file__).parent/ 'data' # imported in performance_analysis.py
if __name__ == "__main__":
    from config_utils import base_dir
    from apsimNGpy.core.mult_cores import MultiCoreManager
    base = base_dir/'demo'
    from itertools import product

    data.mkdir(parents=True, exist_ok=True)
    base.mkdir(parents=True, exist_ok=True)
    os.chdir(base)
    import time

    prod = product([12, 8, 4, 1, 16], (100, 200, 300, 500, 700, 1000, 1500))

    for core, size in prod:
        table_name = f"table_{core}{size}"
        csf_file = data / f"{table_name}.csv"
        if not csf_file.exists():
            print(f"running:  {core} workers and jobs: {size}")
            path_dir = base / f'_{size}_{core}'
            path_dir.mkdir(exist_ok=True)
            files = (ApsimModel('Maize', out_path=path_dir / f"{core}_{size}_{i}.apsimx").path for i in range(size))

            Parallel = MultiCoreManager(db_path='testiy.db', agg_func=None)
            Parallel.clear_scratch()
            start = time.perf_counter()
            Parallel.run_all_jobs(jobs=files, n_cores=core, threads=False, clear_db=True)
            end = time.perf_counter()
            Parallel.clear_scratch()

            df = pd.DataFrame(dict(size=size, core=core, seconds=end - start), index=[f"{core}-{size}"])
            insert_data_with_pd(str(data / 'simulated_core_size.db'), table_name, df, 'replace')

            df.to_csv(csf_file)
            time.sleep(1)
