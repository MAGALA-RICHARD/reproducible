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

from apsimNGpy.core.apsim import ApsimModel
from pathlib import Path
from config_utils import logger, BASE_DIR
wd = BASE_DIR / 'demo'
wd.mkdir(exist_ok=True)
if __name__ == '__main__':
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
    model.get_weather_from_web(lonlat=lonlat, start=1981, end=2022)
    # change the start and end dates
    model.edit_model(model_type='Models.Clock', model_name='Clock', start='1990-01-01', end='2021-12-31')
    # run the model
    # you may need to check the available report names
    report_tables = model.inspect_model('Models.Report', fullpath=False)
    # output: ['Report']
    model.run(report_name="Report")
    # retrieve results
    df = model.results
    # same as
    dfs = model.get_simulated_output(report_names='Report')
    mn =dfs.mean(numeric_only=True)
    logger.info(f"mean summary of the data:\n {mn}")
    # save edited file
    filename = str((wd / 'my-edited-maize-model.apsimx').resolve())
    # save simulated data
    csv_file_name= str((wd / 'simulated.csv'))
    df.to_csv(csv_file_name, index=False)
    logger.info(f"simulated data saved to: {csv_file_name}")
    model.save(file_name=filename)
    logger.info(f'Saved edited model to {filename}\n')
    logger.info(f"see simulated results below:\n{df}")
    logger.info(f"successfully executed listing code 1")
