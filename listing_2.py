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
   copy to ``out_maizer.apsimx`` in the working folder.
3) Declares two factors:
   - **Fertilise at sowing → Amount**: ``0, 300`` (kg N ha⁻¹)
   - **Sow using a variable rule → CultivarName**:
     ``Dekalb_XL82, Melkassa, B_110, Pioneer_34K77``
4) Runs the factorial (cartesian) set of treatments via ``experiment.run()``.
5) Accesses the combined results as a pandas DataFrame via ``experiment.results``.
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
from pathlib import Path
import os
from constants import custom_colors
from apsimNGpy.core.experimentmanager import ExperimentManager as Experiment
from config import logger
from apsimNGpy.core.pythonet_config import is_file_format_modified
if not is_file_format_modified():
    # just import ApsimModel
    from apsimNGpy.core.apsim import ApsimModel
else:
    ApsimModel = None
if __name__ == '__main__':
    wd = Path(__file__).parent / 'apsimx'
    wd.mkdir(exist_ok=True)
    os.chdir(wd)
    Experiment =ApsimModel or Experiment
    experiment = Experiment('Maize', out_path=(wd / 'out_maizer.apsimx').resolve())
    if is_file_format_modified():
       experiment.init_experiment()
    else:
        experiment.create_experiment()
    experiment.add_factor('[Fertilise at sowing].Script.Amount = 0, 300')
    experiment.add_factor(
        '[Sow using a variable rule].Script.CultivarName= Dekalb_XL82, Melkassa, B_110, Pioneer_34K77')
    # run the experiment
    experiment.run()
    df = experiment.results
    g = experiment.cat_plot(x='Amount', y='Yield', hue='CultivarName', kind='bar', height=8, aspect=1,
                            palette=custom_colors)
    g._legend.set_title('Cultivar names')
    g._legend.set_bbox_to_anchor((0.1, 0.98))
    g._legend.set_frame_on(False)
    g._legend.set_loc("upper left")
    experiment.render_plot(save_as=(wd / 'experiment.png').resolve(), dpi=600, show=False,
                           ylabel='Simulated corn grain yield (kg ha $^{-1}$)',
                           xlabel='Nitrogen fertilizer (kg ha $^{-1}$)')

    logger.info('succeeded')
    if hasattr(os, 'startfile'): # windows platfform
        os.startfile(wd / 'experiment.png')
    else:
        subprocess.call(['open', 'experiment.png'])