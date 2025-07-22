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
df = df.loc[:, df.columns.str.contains('t__')]

# Simplify species names: strip the full taxonomic path, keep only species name
df.columns = df.columns.str.replace(r'.*\|s__', '', regex=True)

# Label the columns as 'species'
df.columns.name = 'species'

# Save
df.to_csv('results/species.tsv', sep='\t')

