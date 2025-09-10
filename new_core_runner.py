import sys
import time

from apsimNGpy.core.mult_cores import MultiCoreManager
from apsimNGpy.core.apsim import ApsimModel
from pathlib import Path
from itertools import product
from sqlalchemy import create_engine
import os, shutil
import pandas as pd
import config
base_dir = Path(r'D:\test')

from apsimNGpy.core.mult_cores import MultiCoreManager

job = ['Maize', 'Soybean', 'Barley', 'Canola', "Wheat", 'Oats', "Potato", 'MungBean']


# --- Your loop with per-iteration saving ---

def insert_data_with_pd(db, table, results, if_exists):
    engine = create_engine(f'sqlite:///{db}')
    results.to_sql(table, engine, index=False, if_exists=if_exists)


base = Path(r'D:/test')
data = Path(__file__).parent / 'data'
if __name__ == "__main__":
    def clean_up():
        apsimx_files = base_dir.rglob("temp_*.apsimx")
        for file in apsimx_files:
            try:
                file.unlink(missing_ok=True)
                print(file)
            except PermissionError:
                pass


    from itertools import product
    import shutil

    data.mkdir(parents=True, exist_ok=True)
    base.mkdir(parents=True, exist_ok=True)
    os.chdir(base)
    import time

    prod = product([12, 8, 4, 1, 16], (100, 200, 300, 500, 700, 1000, 1500))
    # for core, size in prod:
    #     if size ==1500:
    #         print(core, size)
    #         path_dir = base/f'{size}_{core}'
    #         if  path_dir.exists():
    #             shutil.rmtree(path_dir)
    #         path_dir.mkdir(parents=True, exist_ok=True)
    #         create_jobs = [ApsimModel('Maize', out_path = path_dir/f"{core}_{size}_{i}.apsimx").path for i in range(size)]
    # sys.exit(1)
    for core, size in prod:
        table_name = f"table_{core}{size}"
        csf_file = data / f"{table_name}.csv"
        if not csf_file.exists():
            print(f"running:  {core} workers and jobs: {size}")
            path_dir = base / f'{size}_{core}'
            files = [str(i) for i in list(path_dir.glob(f'*{core}_{size}*.apsimx')) if 'APSIM' not in str(i)]
            if len(files) != size:
                raise ValueError(
                    f"could not find all matching files in {path_dir} len is {len(files)} and expected {size}")
            Parallel = MultiCoreManager(db_path='testingy.db', agg_func=None)
            Parallel.clear_scratch()
            start = time.perf_counter()
            Parallel.run_all_jobs(jobs=files, n_cores=core, threads=False, clear_db=True)
            end = time.perf_counter()
            Parallel.clear_scratch()

            df = pd.DataFrame(dict(size=size, core=core, seconds=end - start), index=[f"{core}-{size}"])
            insert_data_with_pd(str(data / 'simulated_core_size.db'), table_name, df, 'replace')

            df.to_csv(csf_file)
            time.sleep(1)
