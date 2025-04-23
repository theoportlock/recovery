#!/usr/bin/env python
from pathlib import Path
import argparse
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import metatoolkit.functions as f
import numpy as np
import os
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap

def parse_arguments():
    """Parse command line arguments using argparse."""
    parser = argparse.ArgumentParser(description='Analyze time-dependent datasets')
    parser.add_argument('-d', '--datasets-file', type=Path, default='../conf/timedatasets.txt',
                       help='Path to file containing dataset names (one per line)')
    return parser.parse_args()

def load_datasets(dataset_file):
    """Load dataset names from specified file."""
    with open(dataset_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def create_heatmap(data, name):
    """Create and save a Reds heatmap with max color intensity at 200, no colorbar, and 0.4 pt ticks."""
    ndf = (~data.isna())
    ndf = ndf.groupby(level=0, axis=1).any()
    ndf = ndf.groupby(level=1).sum()
    ndf = ndf.loc[ndf.nunique(axis=1).gt(2)]

    # Calculate dynamic size based on data dimensions
    n_rows, n_cols = ndf.T.shape
    size_per_cell = 0.4  # inches per cell
    fig_width = size_per_cell * n_cols
    fig_height = size_per_cell * n_rows
    
    plt.figure(figsize=(fig_width, fig_height))
    ax = sns.heatmap(
        data=ndf.T,
        cmap="Reds",
        cbar=False,
        square=True,
        linewidths=0.5,
        linecolor="black",
        annot=ndf.T,
        fmt='d',
        annot_kws={"size": 7, "color": "black"},
        vmin=0,
        vmax=200
    )

    # Set tick parameters to 0.4 pt
    ax.tick_params(axis='both', which='both', width=0.4, length=2)  # 0.4 pt width, 2 pt length
    
    plt.gca().set_facecolor("white")
    plt.tight_layout()

    output_file = Path('../results/') / f'{name}_heatmap.svg'
    plt.savefig(output_file)
    plt.close()
    print(f"Saved heatmap to {output_file}")

def main():
    args = parse_arguments()
    
    # Load data
    meta = f.load('meta')
    dataset_names = load_datasets(args.datasets_file)
    datasets = {data: pd.read_csv(f'../results/{data}.tsv', sep='\t', index_col=[0,1]) for data in dataset_names}
    
    df = pd.concat(datasets, axis=1)
    
    # Create filtered datasets
    mam_filter = (meta.Condition == 'MAM') & (meta.index.str[3] != '3')
    h_filter = (meta.Condition == 'Well-nourished')

    mamdf = df.reset_index().set_index('subjectID').loc[mam_filter].reset_index().set_index(['subjectID','timepoint'])
    hdf = df.reset_index().set_index('subjectID').loc[h_filter].reset_index().set_index(['subjectID','timepoint'])

    # Generate visualizations
    create_heatmap(hdf, 'hdata')
    create_heatmap(mamdf, 'mdata')

if __name__ == '__main__':
    main()
