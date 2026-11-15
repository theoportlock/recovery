#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Theo Portlock
For genetics data setup
'''
import os

import pandas as pd
from glob import glob
from scipy.stats import zscore

# Load and process data
genetics_datasets = glob(os.path.join(os.environ["DATA"], 'Bang*.txt'))
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

# Drop the EF score as not right
joined = joined.drop(['EF_PRS'], axis=1)

# Save
joined.to_csv(os.path.join(os.environ["WORK"], 'cleaned/genetics.tsv'), sep='\t')
