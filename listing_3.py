import shutil
from apsimNGpy.core.mult_cores import MultiCoreManager
if __name__ == "__main__":

    # please maintain the oder of imports here

    from config import logger, BASE_DIR
    from apsimNGpy.core.config import load_crop_from_disk

    logger.info('Loading data for parallel processing..')
    base_dir = BASE_DIR / 'demo'
    base_dir.mkdir(parents=True, exist_ok=True)
    # create some jobs for the demo
    data_base = base_dir / 'demo.db'
    try:
        data_base.unlink(missing_ok=True)
    except PermissionError:
        pass
    from multiprocessing import freeze_support

    freeze_support()
    base_model = load_crop_from_disk("Maize", out=base_dir / "base.apsimx")
    create_jobs = (shutil.copy2(base_model, str(base_dir / f'_{i}_.apsimx')) for i in range(100))# test a few
    # initialize multicore manager
    task_manager = MultiCoreManager(str(data_base), agg_func='mean')
    # run all jobs
    task_manager.run_all_jobs(create_jobs, n_cores=4, threads=False, clear_db=True)
    # clear scratch directory
    task_manager.clear_scratch()
    # get the results
    df = task_manager.get_simulated_output(axis=0)
    # same as
    data = task_manager.results
    logger.info('successfully completed listing 3')
