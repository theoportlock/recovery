#!/usr/bin/env python

import pandas as pd
from glob import glob
import os

# Collect files
notp_files = glob('results/timepoints/notp/*')
filenames = [
    'results/mofa_mbiome/extract/sample_factors.tsv',
    'results/mofa_metabolome/extract/sample_factors.tsv',
    'results/timepoints/yr1/alpha_diversity.tsv',
    'results/timepoints/yr1/anthro.tsv',
    'results/timepoints/yr1/fcis.tsv',
    'results/timepoints/yr1/glitter.tsv',
    'results/timepoints/yr1/head.tsv',
    'results/timepoints/yr1/pci.tsv',
    'results/timepoints/yr1/pss.tsv',
    'results/timepoints/yr1/sleep.tsv',
    'results/timepoints/yr1/bayley.tsv',
    'results/timepoints/yr1/wolkes.tsv'
]
files = filenames + notp_files

dfs = []
for file in files:
    # Load data
    df = pd.read_csv(file, sep='\t', index_col=0)

    # Determine dataset name
    if 'mofa_mbiome' in file:
        dataset_name = 'mofa_mbiome'
    elif 'mofa_metabolome' in file:
        dataset_name = 'mofa_metabolome'
    else:
        dataset_name = os.path.splitext(os.path.basename(file))[0]

    # Rename columns to dataset:feature
    df.columns = [f"{dataset_name}:{col}" for col in df.columns]

    dfs.append(df)

# Merge all dataframes
ndf = pd.concat(dfs, axis=1)

# Impute
ndf = ndf.apply(lambda col: col.fillna(col.mean()), axis=0)

# Save merged dataset
ndf.to_csv('results/merged_dataset.tsv', sep='\t')

