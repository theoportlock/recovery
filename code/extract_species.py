#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Theo Portlock
Script to extract species-level relative abundances from MetaPhlAn output
"""

import pandas as pd

# Load MetaPhlAn output with multi-index: (subjectID, timepoint)
df = pd.read_csv('../results/metaphlan.tsv', sep='\t', index_col=0)

# Return to original shape: rows = samples, columns = taxa
df = df.T

# Keep only species-level taxa (those containing 's__')
df = df.loc[:, df.columns.str.contains('s__')]

# Simplify species names: strip the full taxonomic path, keep only species name
df.columns = df.columns.str.replace(r'.*\|s__', '', regex=True)

# Label the columns as 'species'
df.columns.name = 'species'

# Transpose for normalization: rows = samples, columns = species
df = df.T.div(df.sum(axis=1), axis=1)  # Normalize so each sample sums to 1

# Transpose back to original shape: rows = samples, columns = species
df = df.T

# Export the normalized species-level table (flatten index for readability)
df.to_csv('../results/species.tsv', sep='\t')

