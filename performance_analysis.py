"""
Plot CPU scaling and speedup from APSIM NG simulation benchmarks.

Overview
--------
This script reads per-batch runtime results from a SQLite database and produces two figures:
1) **cpu.png** — total runtime (seconds) vs. batch size, with lines colored by CPU core count.
2) **cpu_performance_cores.png** — relative speed gain (baseline = 1 core) vs. batch size,
   again colored by core count.

Data source
-----------
- Database path is derived from `new_core_runner.data` and expected to contain a file
  named `simulated_core_size.db`.
- All tables are read and concatenated. Expected columns include:
  - `core` (int): number of CPU cores
  - `size` (int): number of simulations in the batch
  - `seconds` (float): total runtime in seconds for that batch

Processing
----------
- Converts `core` into an ordered categorical to control legend ordering.
- Computes helper metrics:
  - `s/s` : seconds per simulation (`seconds / size`)
  - `performance` : ratio vs. 1-core runtime (`seconds / baseline_seconds`)
  - `ptimes` : speedup vs. 1-core (`baseline_seconds / seconds`)

Outputs
-------
- Saves figures to `cpu.png` and `cpu_performance_cores.png`.
- Attempts to open the images:
  - On Windows: uses `os.startfile`.
  - Otherwise: calls the system `open` command.

Dependencies
------------
- pandas, seaborn, matplotlib
- apsimNGpy.core_utils.database_utils: `read_db_table`, `get_db_table_names`
- constants: `x_font_size`, `y_font_size`, `custom_colors`

Notes
-----
- Ensure the database has consistent schemas across tables.
- If running on non-macOS Unix where `open` is not available, replace the final
  `subprocess.call(['open', ...])` with `xdg-open` or another launcher.
"""
import os
from constants import x_font_size, y_font_size
from apsimNGpy.core_utils.database_utils import read_db_table, get_db_table_names
from matplotlib import pyplot as plt
from config_utils import RESULT
from new_core_runner import data
import pandas as pd
from constants import custom_colors
import seaborn as sns
import subprocess
database = data/'simulated_core_size.db'
tables = get_db_table_names(database)
dat = (read_db_table(database, table) for table in tables)
df = pd.concat(dat, ignore_index=True)
df['s/s']  =df.seconds.values/df['size']
print(df)
order = [1, 4, 8, 12, 16]
df['core'] = df['core'].astype(pd.CategoricalDtype(categories=order, ordered=True))
g = sns.relplot(
    x="size",
    y="seconds",
    hue="core",
    data=df,
    kind="line",
    palette=[*custom_colors, "cyan"],
#aspect =1.1, height=8,
)

# Ensure a legend exists (build if missing), then grab it
if getattr(g, "_legend", None) is None:
    g.add_legend(title="CPU cores")
legend = g._legend  # seaborn stores it here on FacetGrid

# Style & position

legend.set_frame_on(False)
legend.set_bbox_to_anchor((0.2, 0.98))

# Remove legend frame
legend.set_frame_on(False)
# Ensure legend is in the upper-left position
legend.set_loc("upper left")
# Remove legend title
legend.set_title('CPU cores')

plt.ylabel("Runtime (seconds)", fontsize=y_font_size)
plt.xlabel("APSIM simulations batch size", fontsize=x_font_size)
plt.savefig(RESULT/'fig_2.png')
if hasattr(os, 'startfile'):
    os.startfile(RESULT/'fig_2.png')
else:

    subprocess.call(['open',str(RESULT/'fig_2.png')])

#step 1: keep only core=1 as baseline
baseline = df[df['core'] == 1][['size', 'seconds']].rename(columns={'seconds': 'baseline_seconds'})

# step 2: merge baseline with all other cores by size
merged = df.merge(baseline, on='size')

# step 3: compute ratio relative to core=1
merged['performance'] = (merged['seconds']/merged['baseline_seconds'])
merged['ptimes'] = merged['baseline_seconds']/merged['seconds']

# step 4: drop core=1 rows if you only want comparisons
result = merged[merged['core'] != 1].sort_values(['size', 'core'])
plt.close()
cc = custom_colors[-3:]
order = [4, 8, 12, 16]
result['core'] = result['core'].astype(pd.CategoricalDtype(categories=order, ordered=True))
g = sns.relplot(
    x='size',
    y='ptimes',
    hue='core',
    data=result,
    kind='line',
    palette=[*cc, 'cyan'],
    #aspect =1.1, height=8,

)
# Remove legend title
if getattr(g, "_legend", None) is None:
    g.add_legend(title="CPU cores")
legend = g._legend  # seaborn stores it here on FacetGrid

# Style & position

legend.set_frame_on(False)
legend.set_title('CPU cores')
legend.set_bbox_to_anchor((0.99, 0.98))
legend.set_loc("upper right")
plt.ylabel("Runtime speed gain", fontsize=y_font_size)
plt.xlabel("APSIM simulations batch size", fontsize=x_font_size)
plt.savefig(RESULT/'anon.png')
plt.tight_layout()
if hasattr(os, 'startfile'):
    os.startfile(RESULT/'anon.png')
else:

    subprocess.call(['open', str(RESULT/'anon.png')])
plt.close()