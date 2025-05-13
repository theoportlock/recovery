#!/usr/bin/env python

from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def parse_arguments():
    """Parse command line arguments using argparse."""
    parser = argparse.ArgumentParser(description='Analyze time-dependent datasets')
    parser.add_argument('-d', '--datasets-file', type=Path, default='conf/timedatasets.txt',
                       help='Path to file containing dataset names (one per line)')
    return parser.parse_args()

def load_datasets(dataset_file):
    """Load dataset names from specified file."""
    with open(dataset_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def prepare_heatmap_data(data):
    """Prepare data for heatmap plotting."""
    ndf = (~data.isna())
    ndf = ndf.groupby(level=0, axis=1).any()
    ndf = ndf.groupby(level=1).sum()
    ndf = ndf.loc[ndf.nunique(axis=1).gt(2)]
    plotdf = ndf.T

    # Load dataset labels
    labels = pd.read_csv('conf/dataset_labels.tsv', sep='\t', index_col=0)
    plotdf = plotdf.join(labels['name'], how='inner').set_index('name')
    
    return plotdf

def main():
    args = parse_arguments()
    
    # Load data
    meta = pd.read_csv('results/timemeta.tsv', sep='\t', index_col=0)
    dataset_names = load_datasets(args.datasets_file)
    datasets = {data: pd.read_csv(f'results/filtered/{data}.tsv', sep='\t', index_col=0) for data in dataset_names}
    
    df = pd.concat(datasets, axis=1)
    
    # Create filtered datasets
    mam_RA_filter = (meta['Feed'] == 'Local RUSF (A)') & (meta['Condition'] == 'MAM') & ((meta['timepoint'] == 0) | (meta['timepoint'] == 52))
    mam_RB_filter = (meta['Feed'] == 'ERUSF (B)') & (meta['Condition'] == 'MAM') & ((meta['timepoint'] == 0) | (meta['timepoint'] == 52))
    h_filter = (meta['Condition'] == 'Well-nourished') & ((meta['timepoint'] == 0) | (meta['timepoint'] == 52))

    mamAdf = df.loc[mam_RA_filter]
    mamBdf = df.loc[mam_RB_filter]
    hdf = df.loc[h_filter]

    mamAdf.index = mamAdf.index.str.split('_', expand=True)
    mamBdf.index = mamBdf.index.str.split('_', expand=True)
    hdf.index = hdf.index.str.split('_', expand=True)

    # Prepare data for heatmaps
    mamA_plotdf = prepare_heatmap_data(mamAdf)
    mamB_plotdf = prepare_heatmap_data(mamBdf)
    h_plotdf = prepare_heatmap_data(hdf)

    # To ensure row matching across plots
    common_rows = mamA_plotdf.index.intersection(mamB_plotdf.index).intersection(h_plotdf.index)

    mamA_plotdf = mamA_plotdf.loc[common_rows]
    mamB_plotdf = mamB_plotdf.loc[common_rows]
    h_plotdf = h_plotdf.loc[common_rows]

    # Plot all three side by side
    n_rows, n_cols = mamA_plotdf.shape
    size_per_cell = 0.4
    fig_width = size_per_cell * (mamA_plotdf.shape[1] + mamB_plotdf.shape[1] + h_plotdf.shape[1])
    fig_height = size_per_cell * n_rows

    fig, axes = plt.subplots(1, 3, figsize=(fig_width, fig_height), sharey=True)

    for ax, data, title in zip(
        axes,
        [mamA_plotdf, mamB_plotdf, h_plotdf],
        ['Local RUSF (A)', 'ERUSF (B)', 'Well-nourished']
    ):
        sns.heatmap(
            data=data,
            cmap="Reds",
            cbar=False,
            square=True,
            linewidths=0.5,
            linecolor="black",
            annot=data,
            fmt='d',
            annot_kws={"size": 7, "color": "black"},
            vmin=0,
            vmax=100,
            ax=ax
        )
        ax.set_title(title, fontsize=7)
        ax.tick_params(axis='both', which='both', width=0.4, length=2)
        ax.set_xlabel('')
        ax.set_ylabel('')

    axes[0].set_ylabel('')  # First plot shows y-labels
    plt.gca().set_facecolor("white")
    plt.tight_layout()

    output_file = Path('results/combined_heatmap.svg')
    plt.savefig(output_file)
    plt.close()
    print(f"Saved combined heatmap to {output_file}")

if __name__ == '__main__':
    main()

