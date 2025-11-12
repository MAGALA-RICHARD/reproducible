"""
Listing 3 — Factorial experiment with apsimNGpy (ExperimentManager)
==================================================================

Purpose
-------
Run a small factorial experiment on the APSIM NG *Maize* template using
:class:`apsimNGpy.core.experimentmanager.ExperimentManager`:
- build an experiment from a base model,
- vary fertiliser amount at sowing and cultivar,
- execute all treatments,
- collect results, and
- render a publication-quality bar plot.

What this script does
---------------------
1) Creates/enters a working folder ``./apsimx`` next to this script.
2) Instantiates an ``ExperimentManager`` for the *Maize* model; writes an edited
   copy to ``out_maize.apsimx`` in the working folder.
3) Declares two factors:
   - **Fertilise at sowing → Amount**: ``0, 300`` (kg N ha⁻¹)
   - **Sow using a variable rule → CultivarName**:
     ``Dekalb_XL82, Melkassa, B_110, Pioneer_34K77``
4) Runs the factorial (cartesian) set of treatments via ``experiment.run()``.
5) Access the combined results as a pandas DataFrame via ``experiment.results``.
6) Produces a seaborn bar plot of **Yield** by **Amount** (hue = **CultivarName**),
   styles the legend, and saves the figure as ``experiment.png`` (600 dpi).
7) Opens the saved figure using the platform launcher (``os.startfile`` on Windows,
   ``open`` on macOS).

Inputs & assumptions
--------------------
    - APSIM NG *Maize* template is available to apsimNGpy.
    - Manager node paths used in factors exist in the base model:
      - ``[Fertilise at sowing].Script.Amount``
      - ``[Sow using a variable rule].Script.CultivarName``
    - ``constants.custom_colors`` is defined for plot palette.
    - Network/weather settings are handled by the base template (not modified here).

Outputs
-------
    - Edited APSIM NG model: ``apsimx/out_maizer.apsimx``
    - Factorial results (in-memory): ``experiment.results`` (pandas DataFrame)
    - Figure: ``apsimx/experiment.png`` (saved at 600 dpi)

Notes
-----
    - Factor syntax is **path = value1, value2, …**; apsimNGpy expands the cartesian design.
    - Use ``experiment.cat_plot(...)`` for quick seaborn plots; call
    ``experiment.render_plot(...)`` to save with labels/ DPI.
    - On Linux, replace the macOS ``open`` call with ``xdg-open`` if needed.
    - added backward compatibility check to support safe experiment set up

"""

import subprocess
import time
from pathlib import Path
import os
from xlwings import view
import pandas as pd
from matplotlib import pyplot as plt

from constants import custom_colors
from apsimNGpy.core.config import apsim_bin_context
from apsimNGpy.core_utils.database_utils import read_db_table, get_db_table_names
from apsimNGpy.validation.evaluator import Validate

with apsim_bin_context(dotenv_path=r'env_config/.env', bin_key='PROJECT_BIN'):
    from apsimNGpy.core.pythonet_config import is_file_format_modified
    from apsimNGpy.core.experimentmanager import ExperimentManager as Experiment
    from apsimNGpy.core.apsim import ApsimModel as Apsim

    if not is_file_format_modified():
        # just import ApsimModel
        from apsimNGpy.core.apsim import ApsimModel
    else:
        ApsimModel = None
from config_utils import logger, RESULT


def open_file(file_name):
    if hasattr(os, 'startfile'):  # windows platform
        os.startfile(file_name)
    else:
        subprocess.call(['open', file_name])


if __name__ == '__main__':
    Base_dir = Path(__file__).parent
    wd = Base_dir / 'apsimx'
    gui_dir = Base_dir / 'GUI'
    gui_dir.mkdir(parents=True, exist_ok=True)
    gui_fileName = gui_dir / 'ExperimentManager_gui_test.apsimx'
    df_from_gui = read_db_table(gui_fileName.with_suffix('.db'), report_name='Report')
    Amounts_unique = ",".join(df_from_gui.Amount.unique().tolist())
    cultivars_unique = ",".join(df_from_gui.CultivarName.unique())
    wd.mkdir(exist_ok=True)
    os.chdir(wd)
    with Apsim(gui_fileName, out_path='gui_extract.apsimx') as gui_model:
        dt = gui_model.inspect_model_parameters(model_type='Models.Clock', model_name='Clock')
        start, end = dt['Start'].strftime('%Y-%m-%d'), dt['End'].strftime('%Y-%m-%d')
    Experiment = ApsimModel or Experiment

    experiment = Experiment('Maize', out_path=(wd / 'out_maizer.apsimx').resolve())
    if is_file_format_modified():
        experiment.init_experiment()
    else:
        experiment.create_experiment()
    experiment.add_report_variable(variable_spec=['[Clock].Today.Year as year', '[Weather].Rain as rain',
                                                 'sum([Nutrient].TotalC[:2] as soc',
                                                  'sum([Soil].Nutrient.NO3.ppm[:2]) as nitrate',
                                                  '[Maize].AboveGround.Wt * 10 as agb', '[Nutrient].N2Oatm[1] as n20'],
                                   report_name='Report')
    experiment.add_factor(f'[Fertilise at sowing].Script.Amount = {Amounts_unique}')
    experiment.edit_model('Models.Clock', 'Clock', start_date= start, end_date=end)
    experiment.add_factor(
        f'[Sow using a variable rule].Script.CultivarName= {cultivars_unique}')
    # run the experiment
    experiment.run(verbose=True)
    df = experiment.results  # assumes that only oen report table exists
    df_from_apsimNgpy = experiment.get_simulated_output('Report')
    g = experiment.cat_plot(table=df, x='Amount', y='Yield', hue='CultivarName', kind='bar', height=8, aspect=1,
                            palette=custom_colors)
    g._legend.set_title('Cultivar names')
    g._legend.set_bbox_to_anchor((0.1, 0.98))
    g._legend.set_frame_on(False)
    g._legend.set_loc("upper left")
    experiment.render_plot(save_as=(RESULT / 'fig_3.png').resolve(), dpi=600, show=False,
                           ylabel='Simulated corn grain yield (kg ha $^{-1}$)',
                           xlabel='Nitrogen fertilizer (kg ha $^{-1}$)')

    logger.info('succeeded')
    if hasattr(os, 'startfile'):  # windows platform
        os.startfile(RESULT / 'fig_3.png')
    else:
        subprocess.call(['open', str(RESULT / 'fig_3.png')])

    db = gui_fileName.with_suffix('.db')

    # ____________________VALIDATION___________________________________
    # Validation with GUI simulated results
    if Path(gui_fileName).exists() and 'Report' in get_db_table_names(
            db):  # if the report is there, it has already been executed
        df_from_apsimNgpy.sort_values(by=['year', 'year', 'Amount', 'CultivarName'],
                                      inplace=True)  # do not sort by SimulationID, the process is not deterministic

        df_from_gui.sort_values(by=['year', 'year', 'Amount', 'CultivarName'], inplace=True)
        dif = list(df_from_apsimNgpy.columns.difference(df_from_gui.columns)) == ['source_table']
        # validate Yield
        metrics_yield = Validate(df_from_apsimNgpy.Yield.values / 1000, df_from_gui.Yield / 1000).evaluate_all(
            verbose=True)
        metrics_yield['variable'] = 'Maize yield'
        # validate above ground biomass
        metrics_agb = Validate(df_from_apsimNgpy.agb.values / 1000, df_from_gui.agb / 1000).evaluate_all(verbose=True)
        metrics_agb['variable'] = 'Above ground maize biomass'
        # validate carbon. First 2 layer only
        metrics_carbon = Validate(df_from_apsimNgpy.soc.values / 1000, df_from_gui.soc / 1000).evaluate_all(
            verbose=True)
        metrics_carbon['variable'] = 'Soil organic carbon'
        # validate nitrate First 2 layers only
        metrics_n20 = Validate(df_from_apsimNgpy.nitrate.values/1000, df_from_gui.nitrate/1000).evaluate_all(verbose=True)
        metrics_n20['variable'] = 'Nitrate'
        sel_columns = ['year', 'Yield', 'Amount', 'agb', 'soc', 'nitrate', 'CultivarName']
        df_py = df_from_apsimNgpy[sel_columns].assign(Engine='apsimNGpy')
        df_gui = df_from_gui[sel_columns].assign(Engine='APSIM GUI')
        all_df = pd.concat([df_py, df_gui])
        all_df.eval('grain =Yield/1000', inplace=True)
        all_metrics = pd.DataFrame([metrics_yield, metrics_agb, metrics_carbon, metrics_n20])
        all_metrics.to_csv(gui_dir / 'evaluation metrics.csv')
        labels = dict(nitrate='Nitrate (kg ha⁻¹)', Yield="Maize Yield (Mg ha⁻¹)", grain="Maize Yield (Mg ha⁻¹)",
                      soc='Soil organic carbon (Mg ha⁻¹)',
                      agb="Above ground biomass (Mg ha⁻¹)")
        all_df[['soc', 'agb',]] = all_df[['soc', 'agb']] / 1000
        # bar plots
        for label in labels:
            try:
                experiment.cat_plot(table=all_df, kind='box', x='Engine', y=label, hue='Amount')
                plt.ylabel(labels.get(label), fontsize=18)
                plt.xlabel("Simulation source", fontsize=18)
                gui_fileName = gui_dir / f"{label}.png"
                # plt.tight_layout()
                plt.savefig(gui_fileName, dpi=600, bbox_inches='tight')

                open_file(gui_fileName)
            finally:
                plt.close()


    else:
        logger.info('GUI not yet excuted')

        # now plot
