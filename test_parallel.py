from pathlib import Path
import pandas as pd
from apsimNGpy.core_utils.database_utils import read_db_table
from apsimNGpy.core.apsim import ApsimModel
from apsimNGpy.core.mult_cores import MultiCoreManager
from apsimNGpy.validation.evaluator import Validate
job = list((Path(__file__).parent / 'GUI/parallel_dir').rglob("*__.apsimx"))
db_gui = [i.with_suffix('.db') for i in job]
if __name__ == '__main__':
    mp = MultiCoreManager(db_path='par.db', agg_func=None)
    mp.run_all_jobs(jobs=job)
    py =mp.get_simulated_output(axis=1)
    py["stem"] = py["source_name"].str.split('.', n=1).str[0]
    df_g = [read_db_table(i, "Report").assign(stem=i.stem) for i in db_gui]
    df_g = pd.concat(df_g)
    df_g.set_index(['stem', 'Clock.Today'], inplace=True)
    py.set_index(['stem', 'Clock.Today'], inplace=True)
    data = py.join(df_g, lsuffix='_py', rsuffix='_g')
    Validate(data.Yield_py/1000, data.Yield_g/1000).evaluate_all(verbose=True)
