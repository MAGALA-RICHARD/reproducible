import shutil

if __name__ == "__main__":
    def enable_vt100_on_windows():
        import os
        if os.name != 'nt':
            return
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            h = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_uint32()
            if kernel32.GetConsoleMode(h, ctypes.byref(mode)):
                kernel32.SetConsoleMode(h, mode.value | 0x0004)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        except Exception as e:

            pass
    enable_vt100_on_windows()
    # please maintain the oder of imports here
    from config import logger, BASE_DIR
    from apsimNGpy.core.config import load_crop_from_disk
    from apsimNGpy.core.mult_cores import MultiCoreManager

    logger.info('Loading data for parallel processing..')
    base_dir = BASE_DIR / 'demo'
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
