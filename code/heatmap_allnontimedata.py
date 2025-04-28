#!/usr/bin/env python

from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Analyze non-timeseries datasets split by RUSF type')
    parser.add_argument('-d', '--datasets-file', type=Path, default='../conf/notimedatasets.txt',
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
    ndf = ndf.sum()
    plotdf = ndf.to_frame(name='count')
    
    # Load dataset labels
    labels = pd.read_csv('../conf/dataset_labels.tsv', sep='\t', index_col=0)
    plotdf = plotdf.join(labels['name'], how='inner').set_index('name')
    return plotdf.T

def main():
    args = parse_arguments()
    
    # Load data
    meta = pd.read_csv('../results/meta.tsv', sep='\t', index_col=0)
    dataset_names = load_datasets(args.datasets_file)
    datasets = {name: pd.read_csv(f'../results/{name}.tsv', sep='\t', index_col=0) for name in dataset_names}
    
    df = pd.concat(datasets, axis=1)
    
    # Define filters
    erusf_filter = (meta['Feed'] == 'ERUSF (B)') & (meta['Condition'] == 'MAM')
    localrusf_filter = (meta['Feed'] == 'Local RUSF (A)') & (meta['Condition'] == 'MAM')
    h_filter = (meta['Condition'] == 'Well-nourished')
    
    # Create filtered DataFrames
    erusf_df = df.loc[erusf_filter]
    localrusf_df = df.loc[localrusf_filter]
    hdf = df.loc[h_filter]

    # Split index if needed (sometimes you have multiple levels like 'subjectID_time')
    erusf_df.index = erusf_df.index.str.split('_', expand=True)
    localrusf_df.index = localrusf_df.index.str.split('_', expand=True)
    hdf.index = hdf.index.str.split('_', expand=True)
    
    # Prepare each for plotting
    erusf_plotdf = prepare_heatmap_data(erusf_df)
    localrusf_plotdf = prepare_heatmap_data(localrusf_df)
    h_plotdf = prepare_heatmap_data(hdf)

    # Align rows
    common_rows = erusf_plotdf.columns.intersection(localrusf_plotdf.columns).intersection(h_plotdf.columns)

    erusf_plotdf = erusf_plotdf[common_rows]
    localrusf_plotdf = localrusf_plotdf[common_rows]
    h_plotdf = h_plotdf[common_rows]

    # Transmute
    erusf_plotdf = erusf_plotdf.T
    localrusf_plotdf = localrusf_plotdf.T
    h_plotdf = h_plotdf.T

    # Plot side-by-side
    n_rows, n_cols = erusf_plotdf.shape
    size_per_cell = 0.4
    fig_width = size_per_cell * (n_cols * 3)  # 3 groups
    fig_height = size_per_cell * n_rows

    fig, axes = plt.subplots(1, 3, figsize=(fig_width, fig_height), sharey=True)

    for ax, data, title in zip(
        axes,
        [localrusf_plotdf, erusf_plotdf, h_plotdf],
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

    axes[0].set_ylabel('Dataset')
    plt.gca().set_facecolor("white")
    plt.tight_layout()

    output_file = Path('../results/combined_nontime_heatmap_splitmam.svg')
    plt.savefig(output_file)
    plt.close()
    print(f"Saved combined heatmap to {output_file}")

if __name__ == '__main__':
    main()

