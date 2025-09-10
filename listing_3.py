from apsimNGpy.core.apsim import ApsimModel
from apsimNGpy.core.mult_cores import MultiCoreManager
from pathlib import Path
import shutil
if __name__ == "__main__":
    base_dir = Path(__file__).parent/'demo'
    base_dir.mkdir(parents=True, exist_ok=True)
    # create some jobs for the demo

    create_jobs = (ApsimModel('Maize').path for _ in range(100))
    # initialize multicore manager
    task_manager = MultiCoreManager(str(base_dir/'demo.db'), agg_func='mean')

    # run all jobs
    task_manager.run_all_jobs(create_jobs, n_cores=16, threads=False, clear_db=True)
    # clear scratch directory
    task_manager.clear_scratch()
    # get the results
    df = task_manager.get_simulated_output(axis=0)
    # same as
    data = task_manager.results