import shutil
from pathlib import Path


if __name__ == "__main__":
    # please maintain the oder of imports here
    from config import logger
    from apsimNGpy.core.config import load_crop_from_disk
    from apsimNGpy.core.mult_cores import MultiCoreManager

    logger.info('Loading data. for parallel processing..')
    base_dir = Path(__file__).parent / 'demo'
    base_dir.mkdir(parents=True, exist_ok=True)
    # create some jobs for the demo
    base_model = load_crop_from_disk("Maize", out=base_dir / "base.apsimx")
    create_jobs = (shutil.copy2(base_model, str(base_dir / f'_{i}_.apsimx')) for i in range(100))
    # initialize multicore manager
    task_manager = MultiCoreManager(str(base_dir / 'demo.db'), agg_func='mean')

    # run all jobs
    task_manager.run_all_jobs(create_jobs, n_cores=8, threads=False, clear_db=True)
    # clear scratch directory
    task_manager.clear_scratch()
    # get the results
    df = task_manager.get_simulated_output(axis=0)
    # same as
    data = task_manager.results
    logger.info('successfully completed listing 3')
