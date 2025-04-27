#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import numpy as np
import pandas as pd

# Load data
df1 = pd.read_excel('../data/LEAP Surveillance (Group-A) till 31-Aug-2023 [Full Variable].xlsx', index_col=0)
df2 = pd.read_excel('../data/LEAP Surveillance (Group-B) till 31-Aug-2023 [Full Variable].xlsx', index_col=0)

# Clean and merge
df1 = df1.replace(99, np.nan)
df2 = df2.replace(99, np.nan)
df = pd.concat([df1, df2], axis=0)

# Convert symptom responses to boolean cleanly
cols = ['Cough', 'Rash', 'Antibio', 'ORS', 'Zinc']
df_bool = (df[cols] - 2).mul(-1).astype(bool)
df[cols] = df_bool.astype('boolean')  # Nullable BooleanDtype for compatibility

# Drop irrelevant columns
df.drop(['Food', 'Date', 'Recover', 'Reason', 'Remarks'], axis=1, inplace=True)

# Index renaming
df.index = 'LCC' + df.index.astype(str)

# Exclusive breast feeding (1 = True)
df['BF'] = df['BF'] == 1

# Fever defined as temperature > 38
df['Fever'] = df['Temp'].gt(38)

# Capsule calculation (half = 0.5)
df['Capsule'] = (df['Capsule'] - 1).div(2)

# Calculate timepoint in weeks, then round up
df['timepoint'] = pd.to_timedelta(df['Day'] - 1, unit='D') / np.timedelta64(1, 'W')
df = df.dropna(subset=['timepoint'])
df['timepoint'] = df['timepoint'].apply(np.ceil).astype(int)

# Set index
df['subjectID'] = df.index
df = df.set_index(['subjectID', 'timepoint'])

# LOOK TO CREATE SUMMARY STATS FROM THIS TABLE
# May have to revisit this

# Save result
df.to_csv('../results/surveillance.tsv', sep='\t')
