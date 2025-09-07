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

# Find cat cols
cols = cor.abs().sum().sort_values().tail(10).index

# Filter
cor = cor.loc[:, cols]

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














'''
# Cats code
def create_full_clustermap(intervention_data: pd.DataFrame, top_n_features: int = 10):
    """
    Generates a clustered heatmap for ALL individuals in the dataset,
    revealing population-level patterns and clusters.
    """
    mean_abs_delta = intervention_data.groupby('feature')['delta'].apply(lambda x: x.abs().mean())
    top_features = mean_abs_delta.nlargest(top_n_features).index.tolist()
 
    heatmap_data = intervention_data[intervention_data['feature'].isin(top_features)]
 
    heatmap_matrix = heatmap_data.pivot(
        index='subjectID',
        columns='feature',
        values='delta'
    ).fillna(0)
   
    heatmap_matrix = heatmap_matrix[top_features]
   
    plt.style.use('seaborn-v0_8-whitegrid')
   
    g = sns.clustermap(
        heatmap_matrix,
        method='ward',
        cmap='vlag',
        center=0,
        figsize=(15, 12),
        yticklabels=False,
        cbar_kws={'label': 'Recommended Change (Δ)'}
    )
 
    g.ax_heatmap.set_title('Population-wide Intervention Patterns', fontsize=16, fontweight='bold', pad=20)
    g.ax_heatmap.set_xlabel('Top 10 Features', fontsize=12, fontweight='bold')
    g.ax_heatmap.set_ylabel('')
   
    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90)
    g.savefig('catclustermap.pdf')
 

create_full_clustermap(df)

'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def create_full_clustermap(
    intervention_data: pd.DataFrame,
    meta: pd.DataFrame,
    top_n_features: int = 10,
    output: str = "catclustermap_with_meta.svg"
):
    """
    Generates a clustered heatmap for ALL individuals in the dataset with row colors
    for metadata categories.

    Parameters:
    - intervention_data: DataFrame with columns ['subjectID', 'feature', 'delta']
    - meta: DataFrame with metadata, indexed by subjectID
    - top_n_features: Number of top features (by mean absolute delta) to include
    - output: Path to save the figure
    """

    # ---- Select Top Features ----
    mean_abs_delta = intervention_data.groupby('feature')['delta'].apply(lambda x: x.abs().mean())
    top_features = mean_abs_delta.nlargest(top_n_features).index.tolist()

    # ---- Prepare Heatmap Matrix ----
    heatmap_data = intervention_data[intervention_data['feature'].isin(top_features)]
    heatmap_matrix = heatmap_data.pivot(
        index='subjectID',
        columns='feature',
        values='delta'
    ).fillna(0)
    heatmap_matrix = heatmap_matrix[top_features]

    # Align meta to heatmap rows
    meta = meta.loc[heatmap_matrix.index]

    # ---- Generate Row Colors for Categorical Metadata ----
    row_colors_list = []
    palette_dict = {}  # For legend

    for col in meta.columns:
        if meta[col].dtype == 'object' or meta[col].nunique() < 20:  # categorical check
            unique_vals = meta[col].dropna().unique()
            colors = sns.color_palette('husl', n_colors=len(unique_vals))
            color_map = dict(zip(unique_vals, colors))
            row_colors_list.append(meta[col].map(color_map))
            palette_dict[col] = color_map

    if row_colors_list:
        row_colors = pd.concat(row_colors_list, axis=1)
        row_colors.columns = [
            col for col in meta.columns if (meta[col].dtype == 'object' or meta[col].nunique() < 20)
        ]
    else:
        row_colors = None

    # ---- Plot Clustermap ----
    plt.style.use('seaborn-v0_8-whitegrid')
    g = sns.clustermap(
        heatmap_matrix,
        method='ward',
        cmap='vlag',
        center=0,
        figsize=(15, 12),
        row_colors=row_colors,
        yticklabels=False,
        cbar_kws={'label': 'Recommended Change (Δ)'}
    )

    g.ax_heatmap.set_title('Population-wide Intervention Patterns', fontsize=16, fontweight='bold', pad=20)
    g.ax_heatmap.set_xlabel(f'Top {top_n_features} Features', fontsize=12, fontweight='bold')
    g.ax_heatmap.set_ylabel('')

    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90)

    # ---- Add Legends ----
    legend_patches = []
    for col, color_map in palette_dict.items():
        for label, color in color_map.items():
            legend_patches.append(Patch(facecolor=color, edgecolor='black', label=f"{col}: {label}"))

    plt.legend(
        handles=legend_patches,
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        title="Metadata"
    )

    # ---- Save ----
    plt.savefig(output, bbox_inches='tight')
    print(f"Saved clustermap with metadata colors to {output}")


create_full_clustermap(df, meta, top_n_features=10, output="results/clustermap_with_metadata.svg")
