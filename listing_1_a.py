"""
Listing A1 — Minimal APSIM NG workflow with apsimNGpy
====================================================
Demonstrates how to use the apsim_bin_context manager to work with a specific APSIM version without altering the global path.
The rest of the code below focuses on demonstrating model inspections and simulation tree console mapping as well as opening the file in GUI
.
"""
# pinning workflow to a specific APSIM version or bin_path
from apsimNGpy.core.config import apsim_bin_context
with apsim_bin_context(dotenv_path='./config_env/.env', bin_key='BIN'):
    from apsimNGpy.core.apsim import ApsimModel  # uses this bin path for loading

from config_utils import BASE_DIR

wd = BASE_DIR / 'demo'
wd.mkdir(exist_ok=True)

if __name__ == '__main__':
    gui_dir = BASE_DIR / 'GUI'

    gui_filename = gui_dir / 'ApsimModel_GUI_test.apsimx'
    # use a context manager to delete temporal files automatically
    with ApsimModel(gui_filename) as model:
        manager_scripts = model.inspect_model('Models.Manager', fullpath=True)
        print(manager_scripts)
        ['.Simulations.Simulation.Field.Sow using a variable rule',
         '.Simulations.Simulation.Field.Fertilise at sowing', '.Simulations.Simulation.Field.Harvest']
        # get the names of the manager scripts only
        manager_scripts = model.inspect_model('Models.Manager', fullpath=False)
        print(manager_scripts)
        ['Sow using a variable rule', 'Fertilise at sowing', 'Harvest']
        # inspect the parameters for sow using a variable rule
        # we have the path from above
        sowp = model.inspect_model_parameters_by_path('.Simulations.Simulation.Field.Sow using a variable rule', )
        print(sowp)
        {'Crop': '[Maize]',
         'StartDate': '1-nov',
         'EndDate': '10-jan',
         'MinESW': '100',
         'MinRain': '25',
         'RainDays': '7',
         'CultivarName': 'Dekalb_XL82',
         'SowingDepth': '30',
         'RowSpacing': '750',
         'Population': '12'}
        # inspect the simulation structure and see the relationship between models
        model.inspect_file(cultivar=False)  # cultivar specific node are so many turn them off
        # if that is not enough, open the file in the GUI

        model.preview_simulation(
            watch=True)  # watch is a boolean that makes it possible to stream live the changes. Please close
        # the GUI when completed before proceeding back
        # Press `Ctrl+C` in the corresponding cell to stop watching.
