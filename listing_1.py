"""
Listing 1 — Minimal APSIM NG workflow with apsimNGpy
====================================================

Created: 2025-09-06
Author: Dr. Richard Magala

Purpose
-------
Demonstrate a compact, end-to-end workflow using **apsimNGpy**:
1) instantiate an APSIM Next Generation model,
2) inspect and edit parameters (e.g., sowing population),
3) fetch and replace weather data from the web,
4) adjust the simulation window via the Clock,
5) run the simulation and retrieve results,
6) saves both the edited model and simulated outputs.

What this script does
---------------------
- Creates a demo working directory under ``BASE_DIR/demo``.
- Builds an ``ApsimModel`` instance for the "Maize" template and directs
  the edited model to ``out_maize_1111.apsimx``.
- Inspects the Manager script **"Sow using a variable rule"** to show current
  sowing parameters, then updates **Population** (plants/m²).
- Downloads weather data for a given ``(lon, lat)`` and time span and
  wires it into the model automatically.
- Edits the **Clock** (start/end dates) to match the analysis window.
- Runs the model, collects the default **Report** output as a pandas DataFrame,
  computes a quick mean summary, logs it, and saves results to CSV.
- Saves an edited copy of the model as ``my-edited-maize-model.apsimx``.

Inputs & assumptions
--------------------
- The "Maize" APSIM NG template is available to apsimNGpy on your system.
- The Manager node named **"Sow using a variable rule"** exists in the template.
- Network access is available to fetch weather (for ``get_weather_from_web``).

Outputs
-------
- Edited model file: ``BASE_DIR/demo/my-edited-maize-model.apsimx``
- Simulation CSV:   ``BASE_DIR/demo/simulated.csv``
- Logging to the configured ``logger`` (INFO level).

Notes
-----
- Use ``model.inspect_model('Models.Report', fullpath=False)`` to list report names.
- If your environment lacks outbound HTTP access, replace the weather step with
  a local weather file and the corresponding apsimNGpy API.
- For reproducible runs, consider pinning the start/end years and random seeds (if any).
"""
import os
import subprocess
import time

import pandas as pd
from apsimNGpy.core.apsim import ApsimModel
from pathlib import Path
from matplotlib import pyplot as plt
from apsimNGpy.core_utils.database_utils import read_db_table

from config_utils import logger, BASE_DIR, RESULT
from apsimNGpy.validation.evaluator import Validate
import os

wd = BASE_DIR / 'demo'
wd.mkdir(exist_ok=True)
if __name__ == '__main__':
    gui_dir = BASE_DIR / 'GUI'

    gui_filename = gui_dir / 'ApsimModel_GUI_test.apsimx'
    db = gui_filename.with_suffix('.db')
    g = read_db_table(db, 'Report')
    logger.info('Starting APSIM Next Generation')
    _out_path = wd / 'out_maize_1111.apsimx'
    # Create a model instance (using "Maize" as an example)
    model = ApsimModel("Maize", out_path=_out_path)
    # change the planting density
    # first inspect the manager script that is implementing population density
    sow_params = model.inspect_model_parameters(model_type='Models.Manager', model_name='Sow using a variable rule')
    # output
    # {'Crop': 'Maize',
    #  'StartDate': '1-nov',
    #  'EndDate': '10-jan',
    #  'MinESW': '100.0',
    #  'MinRain': '25.0',
    #  'RainDays': '7',
    #  'CultivarName': 'Dekalb_XL82',
    #  'SowingDepth': '30.0',
    #  'RowSpacing': '750.0',
    #  'Population': '12'}

    model.edit_model(model_type='Models.Manager', model_name='Sow using a variable rule', Population=12)
    # download and replace weather data automatically
    lonlat = (-93.44, 41.1234)
    model.get_weather_from_web(lonlat=lonlat, start=1981, end=2022, filename=str(gui_dir/'met_1990_2021.met'))
    # change the start and end dates based on the GUi model
    with ApsimModel(gui_filename, out_path='extract.apsimx') as gui_model:
        dt= gui_model.inspect_model_parameters(model_type='Models.Clock', model_name='Clock')
        start, end = dt['Start'].strftime('%Y-%m-%d'), dt['End'].strftime('%Y-%m-%d')
        # for weather, I first downloaded and then inserted it the same manually

    model.edit_model(model_type='Models.Clock', model_name='Clock', start_date=start, end_date=end, )
    # run the model
    # you may need to check the available report names
    report_tables = model.inspect_model('Models.Report', fullpath=False)
    # let's add a new report columns
    model.add_report_variable(variable_spec=['[Clock].Today.Year as year', '[Weather].Rain as rain'], report_name='Report')
    # output: ['Report']
    model.run(report_name="Report")
    # retrieve results
    df = model.results
    # same as
    dfs = model.get_simulated_output(report_names='Report')
    mn = dfs.mean(numeric_only=True)
    logger.info(f"mean summary of the data:\n {mn}")
    # save edited file
    filename = str((RESULT / 'my-edited-maize-model.apsimx').resolve())
    # save simulated data
    csv_file_name = str((RESULT / 'simulated_saved_example.csv'))
    df.to_csv(csv_file_name, index=False)
    logger.info(f"simulated data saved to: {csv_file_name}")

    logger.info(f'Saved edited model to {filename}\n')
    logger.info(f"see simulated results below:\n{df}")
    logger.info(f"successfully executed listing code 1")
    # test GUI output with simulated ones
    # first the save the generated model

    p = dfs

    # just to be sure, run the same file again
    df = model.results
    df.sort_values(by=['year', 'rain'], inplace=True)
    g.sort_values(by=['year', 'rain'], inplace=True)
    Validate(df.Yield.values / 1000, g.Yield.values / 1000).evaluate_all(verbose=True)  # /1000 to convert to Mg
    # All the results are perfectly identical, with some minro difference in RMSE 0f 0.0059 Mg/ha
    # The results confirm that apsimNGpy produces identical simulation outputs to APSIM-NG itself.
    # Any minor discrepancies observed are likely attributable to differences in how .NET and Python
    # handle floating-point precision during calculations.

    # now plot
    df_py = df[['year', 'Yield']].assign(Engine='apsimNGpy')
    df_gui = g[['year', 'Yield']].assign(Engine='APSIM GUI')
    all_df = pd.concat([df_py, df_gui])
    all_df.eval('grain =Yield/1000', inplace=True)
    model.relplot(table=all_df, kind='line', x='year', y='Yield', hue='Engine')

    try:
        model.cat_plot(table=all_df, kind='box', x='Engine', y='grain', )
        plt.xlabel("Simulation source")
        plt.ylabel("Maize Yield (Mg ha⁻¹)")
        plt.savefig(gui_filename.with_suffix('.png'), dpi=600, bbox_inches='tight')
        if hasattr(os, 'startfile'):
            os.startfile(gui_filename.with_suffix('.png'))
        else:
            subprocess.call(['open', str(gui_filename.with_suffix('.png'))])
    finally:
        plt.close()
