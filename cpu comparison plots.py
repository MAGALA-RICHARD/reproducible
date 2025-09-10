import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from os import startfile
custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']
data4 = [dict(cores=4, av=1.11, elapsed='00:01:49.670', size=100),
         dict(cores=4, av=1.06, elapsed='00:03:32.918', size=200),
         dict(cores=4, av=1.03, elapsed='00:05:09.154', size=300),
         dict(cores=4, av=1.02, elapsed='00:07:04.486', size=400),
         dict(cores=4, av=1.03, elapsed='00:08:42.846', size=500),
         dict(cores=4, av=1.01, elapsed='00:11:47.194', size =700),
         dict(cores=4, av=1.05, elapsed='00:17:29.922', size=1000)
         ]

data8 = [dict(cores=8, av=0.72, elapsed='00:01:11.656', size=100),
         dict(cores=8, av=0.59, elapsed='00:01:58.774', size=200),
         dict(cores=8, av=0.61, elapsed=' 00:03:00.233', size=300),
         dict(cores=8, av=0.59, elapsed='00:03:54.932', size=400),
         dict(cores=8, av=0.62, elapsed='00:05:07.543', size=500),
         dict(cores=8, av = 0.64, elapsed='00:07:27.575', size =700),
         dict(cores=8, av=0.60, elapsed='00:10:04.325', size=1000)
         ]

data12 = [dict(cores=12, av=0.58, elapsed='00:00:57.595', size=100),
          dict(cores=12, av=0.53, elapsed='00:01:46.816', size=200),
          dict(cores=12, av=0.52, elapsed='00:02:36.863', size=300),
          dict(cores=12, av=0.52, elapsed='00:03:29.415', size=400),
          dict(cores=12, av=0.54, elapsed='00:04:31.260', size=500),
          dict(cores=12, av=0.56, elapsed='00:06:29.109', size=700),
          dict(cores=12, av=0.51, elapsed='00:08:33.275', size=1000)
          ]

data16 = [dict(cores=16, av=0.63, elapsed='00:01:02.647', size=100),
          dict(cores=16, av=0.65, elapsed='00:02:09.177', size=200),
          dict(cores=16, av=0.51, elapsed='00:02:32.991', size=300),
          dict(cores=16, av=0.52, elapsed='00:03:29.989', size=400),
          dict(cores=16, av=0.48, elapsed='00:04:00.230', size=500),
          dict(cores=16, av = 0.52, elapsed='00:06:05.621', size=700),
          dict(cores=16, av=0.48, elapsed=' 00:07:55.209', size=1000)
          ]
df = pd.DataFrame([*data8, *data12, *data16, *data4])
df['seconds'] = (
    pd.to_timedelta(df['elapsed']).dt.total_seconds()
)
df['perf'] = (df.seconds / df.size) * df.size
plt.close()
gg= sns.lineplot(x='size', y='seconds', hue='cores', data=df, palette=custom_colors)
# Remove legend title
# Get the legend object from the Axes
legend = gg.legend_
legend.set_title('CPU cores')  # Remove legend title
legend.set_bbox_to_anchor((0.02, 0.98))  # Move legend inside
legend.set_frame_on(False)  # Remove legend frame

# Ensure legend is in the upper-left position
legend.set_loc("upper left")

# Axis labels
plt.ylabel('Total number of seconds', fontsize=16)
plt.xlabel('Total number of simulations', fontsize=16)
plt.tight_layout()
# Save and open
plt.savefig('f.png', dpi=600)
startfile('f.png')
plt.close()
df['sim_per_second'] = (df.size / df.seconds)
df['secs_per_sim'] = (df.seconds / df.size)
df['perf'] = (df.seconds / df.size) * (df.size/df.cores)
sns.lineplot(x='size', y='secs_per_sim', hue='cores', data=df)
plt.savefig('f2.png', dpi=600)
startfile('f2.png')
df8 = pd.DataFrame(data8)
df12 = pd.DataFrame(data12)
df16 = pd.DataFrame(data16)
tfs = [df16, df12, df8]
df4 = pd.DataFrame(data4)
df4['seconds'] = pd.to_timedelta(df4['elapsed']).dt.total_seconds()

for dft in tfs:
    dft['seconds'] = (
        pd.to_timedelta(dft['elapsed']).dt.total_seconds()
    )
    dft['gain'] = ((df4.seconds / dft.size) - (dft.seconds / dft.size)) / (df4.seconds / dft.size)
    dft['gain'] *= 100

tf = pd.concat(tfs)
plt.close()
data = df.copy()

data['s/p'] = df.size/df.seconds
# Custom palette for 4 categories (change hex codes as you like)
custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']
plt.close()
# Create the plot
g = sns.catplot(
    x='size',
    y='seconds',
    hue='cores',
    data=data,
    kind='bar',
    palette=custom_colors,

)

# Remove legend title
g._legend.set_title('CPU cores')
g._legend.set_bbox_to_anchor((0.5, 0.98))
g._legend.set_frame_on(True)
plt.legend(loc='upper right')

# Axis labels
plt.ylabel('Number of seconds per simulation', fontsize=16)
plt.xlabel('Total number of simulations', fontsize=16)
plt.tight_layout()
# Save and open
plt.savefig('c.png', dpi=600, bbox_inches='tight')
startfile('c.png')
plt.close()
