#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data
anthro = pd.read_csv('results/anthro.tsv', sep='\t', index_col=0)
timemeta = pd.read_csv('results/timemeta.tsv', sep='\t', index_col=0)
df = anthro.join(timemeta)

# Add condition to timemeta
df.loc[df.Condition == 'Well-nourished', 'Recovery'] = 'Healthy'
df.loc[df.Condition == 'Well-nourished', 'Feed'] = 'Healthy'

# Define custom color palette
palette = {'Healthy':'magenta','Recovered': 'orange', 'No recovery': 'red'}
#palette = {'Healthy':'magenta','ERUSF (B)': 'blue', 'Local RUSF (A)': 'red'}

# Drop all after 52 weeks
df = df.loc[df.timepoint <= 52]

# Function to plot individual lines and mean trend
def line(df, x, y, hue, ax):
    df_reset = df.reset_index()
    # Individual subject lines
    sns.lineplot(
        data=df_reset, x=x, y=y, units='subjectID',
        estimator=None, hue=hue, palette=palette,
        ax=ax, alpha=0.1, linewidth=0.4, legend=False
    )
    # Mean trend with confidence interval
    sns.lineplot(
        data=df_reset, x=x, y=y,
        hue=hue, palette=palette,
        ax=ax, linewidth=1, legend=False
    )
    ax.set_title(y)
    ax.set_ylabel("")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if y == 'WLZ_WHZ':
        ax.axhline(-1, color='lightcoral', linestyle='--')

# Create a row of 3 subplots
fig, axs = plt.subplots(1, 3, figsize=(6, 2.5), sharex=True)

# Plot each metric
line(df, 'timepoint', 'WLZ_WHZ', 'Recovery', axs[0])
line(df, 'timepoint', 'MUAC', 'Recovery', axs[1])
line(df, 'timepoint', 'Weight', 'Recovery', axs[2])

# Layout tweaks
plt.subplots_adjust(wspace=0.4)
plt.tight_layout()
plt.savefig('results/anthro_time.svg')
