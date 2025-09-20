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



data = Path(__file__).parent.parent/ 'data'
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
           # insert_data_with_pd(str(data / 'simulated_core_size.db'), table_name, df, 'replace')

            df.to_csv(csf_file)
            time.sleep(1)
