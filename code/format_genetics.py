#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Theo Portlock
For genetics data setup
'''

import pandas as pd
from glob import glob
from scipy.stats import zscore

# Load and process data
genetics_datasets = glob('data/Bang*.txt')
dfs = []
for file in genetics_datasets:
    df = pd.read_csv(file, sep='\t')
    df['ID'] = df['Unique_sample_identifier'].str[:-4]
    df = df.drop_duplicates(subset='ID', keep='first').set_index('ID').iloc[:, -1].to_frame()
    dfs.append(df)

# Merge
joined = pd.concat(dfs, join='outer', axis=1).T.groupby(level=0).max().T

# Standardize
#joined = joined.apply(zscore) Just removed this
joined.index.name = 'subjectID'

# Save
joined.to_csv('results/cleaned/genetics.tsv', sep='\t')
