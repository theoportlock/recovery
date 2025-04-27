#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Theo Portlock
Script to format MetaPhlAn3 output for downstream analysis
"""

import pandas as pd

# Load MetaPhlAn3 output file, skipping the first row (contains description/metadata)
df = pd.read_csv('../data/m4efad_metaphlan3_profiles_april2024.tsv',
                 sep='\t', index_col=0, header=1)

# Load the sample metadata
samplesheet = pd.read_csv('../results/samplesheet.tsv',
                          sep='\t', index_col=0)

# Clean column names: remove ".metaphlan" suffix
df.columns = df.columns.str.replace(r'\.metaphlan$', '', regex=True)

# Remove the first column (usually relative abundance or taxonomy rank info)
df = df.iloc[:, 1:]

# Transpose so rows are samples and columns are taxa
df = df.T

# Join sample metadata (subjectID and timepoint) and drop unmatched samples
df = df.join(samplesheet[['subjectID', 'timepoint']]).dropna()

# Convert timepoint to integer for consistency
df['timepoint'] = df['timepoint'].astype(int)

# Set multi-index for subjectID and timepoint
df = df.set_index(['subjectID', 'timepoint'])

mapping = df.index.to_frame()
mapping['sampleID'] = mapping['subjectID'] + '_' + mapping['timepoint'].astype(str)
mapping = mapping[['sampleID', 'subjectID', 'timepoint']]
df.index = mapping['sampleID']

# Save formatted data
df.to_csv('../results/metaphlan.tsv', sep='\t')
