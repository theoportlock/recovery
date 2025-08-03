#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Theo Portlock
Script to extract species-level relative abundances from MetaPhlAn output
"""

import pandas as pd

# Load MetaPhlAn output with multi-index: (subjectID, timepoint)
df = pd.read_csv('results/metaphlan.tsv', sep='\t', index_col=0)

# Keep only species-level taxa (those containing 's__')
df = df.loc[:, ~df.columns.str.contains('s__')]
df = df.loc[:, df.columns.str.contains('g__')]

# Simplify species names: strip the full taxonomic path, keep only species name
df.columns = df.columns.str.replace(r'.*\|g__', '', regex=True)

# Label the columns as 'genus'
df.columns.name = 'genus'

# Save
df.to_csv('results/genus.tsv', sep='\t')

