#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from scipy.stats import zscore
from matplotlib.patches import Patch

# --- Load data ---
meta = pd.read_csv('results/filtered/meta.tsv', sep='\t', index_col=0)
clusters = pd.read_csv('data/subject_cluster_assignments.tsv', sep='\t', index_col=0)
df = pd.read_csv('data/population_wlz_deltas_neg1.tsv', sep='\t', index_col=0)

meta['Cat_cluster'] = clusters.cluster_id.astype(int)

# Pivot to wide format
cor = df.set_index(['subjectID', 'feature']).unstack().droplevel(0, axis=1)

# Optional: remove low-variance features
cor = cor.loc[:, ~cor.std().lt(0.6)]

# Align meta to heatmap rows
meta = meta.loc[cor.index]

# --- Generate row_colors for all meta columns ---
row_colors_list = []
palette_dict = {}  # For legend

for col in meta.columns:
    # Check if column is categorical (object, bool, or low unique count)
    if meta[col].dtype == 'object' or meta[col].nunique() < 20:
        unique_vals = meta[col].dropna().unique()
        colors = sns.color_palette('husl', n_colors=len(unique_vals))
        color_map = dict(zip(unique_vals, colors))
        row_colors_list.append(meta[col].map(color_map))
        palette_dict[col] = color_map

# Combine into DataFrame for clustermap
row_colors = pd.concat(row_colors_list, axis=1)
row_colors.columns = [col for col in meta.columns if (meta[col].dtype == 'object' or meta[col].nunique() < 20)]

# --- Plot clustermap ---
g = sns.clustermap(
    cor,
    cmap="vlag", center=0,
    figsize=(8, 8),
    dendrogram_ratio=(0.25, 0.25),
    row_cluster=True,
    col_cluster=True,
    row_colors=row_colors,   # Add metadata colors
    yticklabels=False,
    xticklabels=True
)

# --- Add legends ---
legend_patches = []
for col, color_map in palette_dict.items():
    for label, color in color_map.items():
        legend_patches.append(Patch(facecolor=color, edgecolor='black', label=f"{col}: {label}"))

# Place legend outside plot
plt.legend(
    handles=legend_patches,
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    title="Metadata"
)

# Save plot
output = "results/clustermap_with_metadata.svg"
plt.savefig(output, bbox_inches='tight')
print(f"Saved to {output}")


# Another plot comparing clusters with WLZ
'''
baselineanthro = pd.read_csv('results/timepoints/yr1/anthro.tsv', sep='\t', index_col=0)

joined = baselineanthro.join(meta, how='inner')
joined['Cat_cluster'] = joined.Cat_cluster.astype(int).astype(str)

sns.boxplot(data=joined, x = 'Cat_cluster', y='WLZ_WHZ', linewidth=0.4)

'''
# Another plot comparing clusters with PRS
genetics = pd.read_csv('results/filtered/genetics.tsv', sep='\t', index_col=0)

joined = genetics.join(meta, how='inner')
joined['Cat_cluster'] = joined.Cat_cluster.astype(int).astype(str)

# For stacked plotting
plotdf = joined.set_index('Cat_cluster')
plotdf = plotdf.loc[:, plotdf.columns.str.contains('PRS')]
plotdf = plotdf.stack().reset_index().set_axis(['Cat_cluster','PRS','Score'], axis=1)

#sns.boxplot(data=plotdf, x = 'Cat_cluster', y='Score', hue='PRS', linewidth=0.4)
#sns.stripplot(data=plotdf, x = 'Cat_cluster', y='Score', hue='PRS', linewidth=0.4)
# Z-score the Score within each PRS group
plotdf['Score_z'] = plotdf.groupby('PRS')['Score'].transform(zscore)

# Plot
plt.figure(figsize=(7, 5))

# Boxplot (colored by PRS)
sns.violinplot(
    data=plotdf,
    x='PRS',
    y='Score_z',
    hue='Cat_cluster',
    linewidth=0.4
)

# Stripplot (small black points)
sns.stripplot(
    data=plotdf,
    x='PRS',
    y='Score_z',
    hue='Cat_cluster',
    dodge=True,
    color='black',   # override hue color
    size=2,          # small points
    alpha=0.6        # slightly transparent
)

# Remove duplicate legends from stripplot
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[:len(plotdf['PRS'].unique())], labels[:len(plotdf['PRS'].unique())], title='PRS')

plt.ylabel('Z-scored Score (per PRS)')
plt.title('PRS Score Distribution by Cat_cluster (Z-scored)')
plt.tight_layout()
plt.savefig('prscluster.svg')
plt.show()


