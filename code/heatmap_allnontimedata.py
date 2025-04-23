#!/usr/bin/env python
from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap

def parse_arguments():
    """Parse command line arguments using argparse."""
    parser = argparse.ArgumentParser(description='Analyze non-timeseries datasets')
    parser.add_argument('-d', '--datasets-file', type=Path, default='../conf/notimedatasets.txt',
                        help='Path to file containing dataset names (one per line)')
    return parser.parse_args()

def load_datasets(dataset_file):
    """Load dataset names from the specified file."""
    with open(dataset_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def create_heatmap(data, name):
    """
    Create and save a one-column heatmap visualization.
    Each row represents one dataset (or column from the input DataFrame),
    and the cell is colored according to its total count of nonzero values.
    """
    # Count nonzero values for each column
    ndf = (~data.isna())
    ndf = ndf.groupby(level=0, axis=1).any()
    ndf = ndf.sum()
    # Convert Series to DataFrame with one column
    ndf = ndf.to_frame(name="Total nonzero count")

    # Calculate dynamic size based on data dimensions
    n_rows = len(ndf)
    size_per_cell = 0.4  # inches per cell
    fig_width = size_per_cell * 1  # Single column
    fig_height = size_per_cell * n_rows
    
    plt.figure(figsize=(fig_width, fig_height))
    ax = sns.heatmap(
        ndf, 
        cmap="Reds",          # Using Reds colormap
        cbar=False,           # No colorbar
        linewidths=0.5,       # Grid line thickness
        linecolor='black',    # Black grid lines
        square=True, 
        annot=ndf, 
        fmt="d", 
        annot_kws={"size": 10, "color": "black"},
        vmin=0,               # Minimum value for color scale
        vmax=200              # Maximum value for color scale (same as other script)
    )

    # Set tick parameters to 0.4 pt
    ax.tick_params(axis='both', which='both', width=0.4, length=2)

    ax.set_ylabel('Dataset')
    ax.set_xlabel('')
    plt.tight_layout()
    output_file = Path('../results') / f'{name}_nontime_heatmap.svg'
    plt.savefig(output_file)
    plt.close()
    print(f"Saved heatmap to {output_file}")

def main():
    args = parse_arguments()
    
    # Load dataset names from file
    dataset_names = load_datasets(args.datasets_file)
    
    # Load datasets from ../results/
    datasets = {name: pd.read_csv(Path('../results') / f'{name}.tsv', sep='\t', index_col=0)
                for name in dataset_names}
    
    # Concatenate all datasets into a single DataFrame with a hierarchical column index
    df = pd.concat(datasets, axis=1)
    
    # Load meta data and filter as required
    meta = pd.read_csv('../results/meta.tsv', sep='\t', index_col=0)
    mam_filter = (meta.Condition == 'MAM') & (meta.index.str[3] != '3')
    h_filter = (meta.Condition == 'Well-nourished')
    
    mamdf = (df.reset_index()
             .set_index('subjectID')
             .loc[mam_filter]
             .reset_index()
             .set_index('subjectID'))
    hdf = (df.reset_index()
           .set_index('subjectID')
           .loc[h_filter]
           .reset_index()
           .set_index('subjectID'))
    
    # Create and save heatmaps for each filtered dataset
    create_heatmap(mamdf, 'mamdf')
    create_heatmap(hdf, 'hdf')

if __name__ == '__main__':
    main()
