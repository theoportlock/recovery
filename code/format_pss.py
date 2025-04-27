#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import numpy as np
import pandas as pd

# Mother stress Perceived stress scale
df = pd.read_csv('../data/DhakaBangladeshLEAPE-PSS_DATA_LABELS_2024-07-18_2240.csv', index_col=0)
translated = pd.read_csv('../conf/PSS_translated.tsv', sep='\t')

# Create unique subjectID + timepoint index
df.index = df.index + df['Event Name'].replace({
    '12_month (Arm 2: Intervention)': '000',
    '12_month  (Arm 1: Control)': '000',
    '24_month (Arm 1: Control)': '052',
    '24_month (Arm 2: Intervention)': '052',
    '36_month (Arm 2: Intervention)': '104',
    '36_month (Arm 3: Outcome Reference)': '104'
})

# Keep only relevant columns and rename
df = df.iloc[:, 3:-1]
df.columns = translated.shorthand

# Map string responses to numeric values
mapper = {
    'Never': 0,
    'Almost Never': 1,
    'Sometimes': 2,
    'Fairly Often': 3,
    'Very Often': 4
}

# Only apply mapping to object (string) columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].map(mapper)

# Remove non-numeric index entries (like 'ol')
df = df.loc[~df.index.str.contains('ol')]

# Extract subject ID and timepoint from index
idcol = df.index.str[:7]
timecol = df.index.str[8:].astype(int)
df.insert(0, 'timepoint', timecol)
df.insert(0, 'subjectID', idcol)
df = df.set_index(['subjectID', 'timepoint'])

# Clean up column names
df.columns = df.columns.str.replace(' ', '_')

mapping = df.index.to_frame()
mapping['sampleID'] = mapping['subjectID'] + '_' + mapping['timepoint'].astype(str)
mapping = mapping[['sampleID', 'subjectID', 'timepoint']]
df.index = mapping['sampleID']

# Save final output
df.to_csv('../results/pss.tsv', sep='\t')
