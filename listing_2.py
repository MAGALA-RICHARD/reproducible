"""
Listing 3 — Factorial Experiment with apsimNGpy (ExperimentManager)
====================================================================

Purpose
-------
Run a small factorial experiment on the APSIM NG *Maize* template using
:class:`apsimNGpy.core.experimentmanager.ExperimentManager` to:
    • build an experiment from a base model
    • vary fertilizer amount at sowing and cultivar
    • execute all treatments and collect results
    • render publication-quality plots, and
    • validate against APSIM GUI outputs.

Workflow
---------
1. Create a working directory (`./apsimx`).
2. Instantiate an `ExperimentManager` based on *Maize*; save to `out_maizer.apsimx`.
3. Define factorial treatments:
       - `[Fertilise at sowing].Script.Amount = 0, 300` (kg N ha⁻¹)
       - `[Sow using a variable rule].Script.CultivarName = Dekalb_XL82, Melkassa, B_110, Pioneer_34K77`
4. Execute all treatment combinations and collect `Report` tables.
5. Visualize yield by fertilizer and cultivar as a seaborn bar plot.
6. Compare outputs with APSIM GUI simulation results for validation.
7. Export metrics and plots to the `GUI` directory.

Inputs & Assumptions
--------------------
• The APSIM NG *Maize* template and corresponding managers exist.
• Required manager node paths:
  `[Fertilise at sowing].Script.Amount`, `[Sow using a variable rule].Script.CultivarName`.
• `constants.custom_colors` defines the plot palette.
• Weather and management logic remain unchanged.

Outputs
-------
• Edited APSIM NG file → `apsimx/out_maizer.apsimx`
• Results → `experiment.results` (pandas DataFrame)
• Figures → `apsimx/fig_3.png`, `GUI/*.png`
• Validation metrics → `GUI/evaluation metrics.csv`

Notes
-----
• Factors use *path = values…* syntax; apsimNGpy automatically expands the Cartesian design.
• `experiment.cat_plot()` and `experiment.render_plot()` produce reproducible figures.
• On Linux, replace `open` with `xdg-open` to preview figures.
"""

import os
import subprocess
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xlwings import view
from constants import custom_colors
from apsimNGpy.core.config import apsim_bin_context, configuration
from apsimNGpy.core_utils.database_utils import read_db_table, get_db_table_names
from apsimNGpy.validation.evaluator import Validate
from config_utils import logger, RESULT
from utils import open_file, plot_reg_fit

SEED = 40
os.environ["PYTHONHASHSEED"] = str(SEED)

with apsim_bin_context(dotenv_path="env_config/.env", bin_key="PROJECT_BIN"):
    from apsimNGpy.core.pythonet_config import is_file_format_modified
    from apsimNGpy.core.experimentmanager import ExperimentManager as Experiment
    from apsimNGpy.core.apsim import ApsimModel as Apsim
    if not is_file_format_modified():
        from apsimNGpy.core.apsim import ApsimModel
    else:
        ApsimModel = None

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    wd = base_dir / "apsimx"
    gui_dir = base_dir / "GUI"
    gui_dir.mkdir(parents=True, exist_ok=True)

    gui_file = gui_dir / "ExperimentManager_gui_test.apsimx"
    df_gui = read_db_table(gui_file.with_suffix(".db"), report_name="Report")
    amounts = ",".join(df_gui.Amount.unique().tolist())
    cultivars = ",".join(df_gui.CultivarName.unique())
    wd.mkdir(exist_ok=True)
    os.chdir(wd)

    with Apsim(gui_file, out_path="gui_extract.apsimx") as gui_model:
        dates = gui_model.inspect_model_parameters(model_type="Models.Clock", model_name="Clock")
        start, end = dates["Start"].strftime("%Y-%m-%d"), dates["End"].strftime("%Y-%m-%d")

    Experiment = ApsimModel or Experiment
    experiment = Experiment("Maize", out_path=(wd / "out_maizer.apsimx").resolve())
    experiment.init_experiment() if is_file_format_modified() else experiment.create_experiment()

    experiment.add_report_variable(
        variable_spec=[
            "[Clock].Today.Year as year",
            "[Weather].Rain as rain",
            "sum([Nutrient].TotalC[:2]) as soc",
            "sum([Soil].Nutrient.NO3.ppm[:2]) as nitrate",
            "[Maize].AboveGround.Wt * 10 as agb",
            "[Nutrient].N2Oatm[1] as n2o",
        ],
        report_name="Report",
    )

    experiment.add_factor(f"[Fertilise at sowing].Script.Amount = {amounts}")
    experiment.edit_model("Models.Clock", "Clock", start_date=start, end_date=end)
    experiment.add_factor(f"[Sow using a variable rule].Script.CultivarName = {cultivars}")

    experiment.run(verbose=True)
    df_res = experiment.results
    df_sim = experiment.get_simulated_output("Report")

    g = experiment.cat_plot(
        table=df_res, x="Amount", y="Yield", hue="CultivarName",
        kind="bar", height=8, aspect=1, palette=custom_colors
    )
    g._legend.set(title="Cultivar names", bbox_to_anchor=(0.1, 0.98), frame_on=False, loc="upper left")

    experiment.render_plot(
        save_as=(RESULT / "fig_3.png").resolve(),
        dpi=600, show=False,
        ylabel="Simulated corn grain yield (kg ha⁻¹)",
        xlabel="Nitrogen fertilizer (kg ha⁻¹)",
    )

    logger.info("Experiment completed successfully.")
    fig_path = RESULT / "fig_3.png"
    if hasattr(os, "startfile"):
        os.startfile(fig_path)
    else:
        subprocess.call(["open", str(fig_path)])

    # ____________________ VALIDATION ____________________
    if Path(gui_file).exists() and "Report" in get_db_table_names(gui_file.with_suffix(".db")):
        df_sim.sort_values(by=["year", "Amount", "CultivarName"], inplace=True)
        df_gui.sort_values(by=["year", "Amount", "CultivarName"], inplace=True)

        # Compute validation metrics
        metrics = []
        for var, label in [
            ("Yield", "Maize yield"),
            ("agb", "Aboveground biomass"),
            ("soc", "Soil organic carbon"),
            ("nitrate", "Nitrate"),
        ]:
            print(var)
            val = Validate(df_sim[var].values / 1000, df_gui[var].values / 1000).evaluate_all(verbose=True)
            val["variable"] = label
            metrics.append(val)

        metrics_df = pd.DataFrame(metrics)
        metrics_df.to_csv(gui_dir / "evaluation_metrics.csv", index=False)
        logger.info("Validation metrics saved.")

        # Plot comparisons
        labels = {
            "nitrate": "Nitrate (kg ha⁻¹)",
            "Yield": "Maize yield (Mg ha⁻¹)",
            "agb": "Aboveground biomass (Mg ha⁻¹)",
            "soc": "Soil organic carbon (Mg ha⁻¹)",
            "year": "Year",
        }

        df_sim[["soc", "agb"]] /= 1000
        df_gui[["soc", "agb"]] /= 1000
        df_sim["Engine"], df_gui["Engine"] = "apsimNGpy", "APSIM GUI"
        all_df = pd.concat([df_sim, df_gui])

        for var, label in labels.items():

            try:
                experiment.relplot(x='year', y=var, kind="line", hue='Engine', table=all_df, errorbar=None)
                plt.savefig(gui_dir / f"{gui_dir/var}_line.png")
                plt.ylabel(label, fontsize=18)
                plt.xlabel('Time (Years)', fontsize=18)
                logger.info(f'figure saved at: `{gui_dir/var}_line.png`')
                open_file(gui_dir / f"{gui_dir/var}_line.png")
                experiment.cat_plot(table=all_df, kind="box", x="Engine", y=var, hue="Amount")
                plt.ylabel(label, fontsize=18)
                plt.xlabel("Simulation source", fontsize=18)
                plt.savefig(gui_dir / f"{var}.png", dpi=600, bbox_inches="tight")
                logger.info(f'figure saved at: `{gui_dir / f"{var}.png"}`')
                #open_file(gui_dir / f"{var}.png")
            finally:
                plt.close()

    else:
        logger.warning("GUI simulation not found; skipping validation.")
    from apsimNGpy.optimizer.problems.back_end import eval_observed
    df_gui['gui'] =df_gui['soc']
    eval_observed(obs=df_gui, pred=df_sim, pred_col='soc', obs_col='gui', index=("year",'Clock.Today', "Amount", "CultivarName"))
