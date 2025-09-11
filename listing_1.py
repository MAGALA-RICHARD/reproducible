"""
This code corresponds to Listing 1.
Created on: 2025-09-06
Author: Dr. Richard Magala

Description:
------------
Demonstrates the basic usage of apsimNGpy by instantiating
an APSIM Next Generation model object and accessing its path.
"""

from apsimNGpy.core.apsim import ApsimModel
from pathlib import Path
from config import logger, BASE_DIR
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
    csv_file_name= str((wd / 'simulated'))
    df.to_csv(csv_file_name)
    logger.info(f"simulated data saved to: {csv_file_name}")
    model.save(file_name=filename)
    logger.info(f'Saved edited model to {filename}\n')
    logger.info(f"see simulated results below:\n{df}")
    logger.info(f"successfully executed listing code 1")
