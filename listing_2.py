"""
This code runs listing 3
"""
from pathlib import Path
import os
from constants import custom_colors
from apsimNGpy.core.experimentmanager import ExperimentManager as Experiment
if __name__ == '__main__':
    wd = Path(__file__).parent / 'apsimx'
    wd.mkdir(exist_ok=True)
    os.chdir(wd)
    experiment = Experiment('Maize', out_path=(wd / 'out_maizer.apsimx').resolve())
    experiment.init_experiment()
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




    os.startfile(wd / 'experiment.png')



