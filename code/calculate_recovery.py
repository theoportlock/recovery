#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import sys

# --- Load data ---
df = pd.read_csv('results/filtered/anthro.tsv', sep='\t', index_col=0)
meta = pd.read_csv('results/filtered/meta.tsv', sep='\t', index_col=0)
timemeta = pd.read_csv('results/filtered/timemeta.tsv', sep='\t', index_col=0)
surveil = pd.read_csv('results/filtered/surveillance.tsv', sep='\t', index_col=0)

# --- Merge anthropometry with time metadata ---
allvars = timemeta.join(df[['WLZ_WHZ']]).dropna(subset=['WLZ_WHZ'])

# --- Define recovery booleans ---
#thresh = -2
thresh = float(sys.argv[1])
allvars['Recovered'] = allvars['WLZ_WHZ'] > thresh

# Year 1 recovery (≤15 months)
filt = allvars.query('timepoint <= 15').copy()
yr1_recovered = filt.groupby('subjectID')['Recovered'].any().astype(bool)

# Year 2 recovery (52 weeks)
filt = allvars.query('timepoint == 52').copy()
yr2_recovered = filt.groupby('subjectID')['Recovered'].any().astype(bool)

# --- Focus on MAM participants ---
meta = meta.loc[meta['Condition'] == 'MAM'].copy()
# meta is already indexed by subjectID; no need to reassign index

# --- Define Recovery_status categories ---
meta['Recovery_status'] = 'No recovery'  # default

# Sustained recovery
sustained = yr1_recovered & yr2_recovered
meta.loc[meta.index.isin(sustained[sustained].index), 'Recovery_status'] = 'Sustained recovery'

# Unsustained recovery
unsustained = yr1_recovered & ~yr2_recovered
meta.loc[meta.index.isin(unsustained[unsustained].index), 'Recovery_status'] = 'Unsustained recovery'

# Delayed recovery
delayed = ~yr1_recovered & yr2_recovered
meta.loc[meta.index.isin(delayed[delayed].index), 'Recovery_status'] = 'Delayed recovery'

# --- Optional: Check category counts ---
print(meta['Recovery_status'].value_counts())

# --- Days to recovery (first day WLZ_WHZ > thresh) ---
# Ensure index is string
df = df.copy()
idx = df.index.to_series().astype(str)

# Split sampleID into ID and Day
split_index = idx.str.split('_', expand=True)
df['ID'] = split_index[0]
df['Day'] = split_index[1].astype(int)

# Boolean recovered column
df['Recovered_bool'] = df['WLZ_WHZ'] > thresh

# First day of recovery per subject
first_day = df[df['Recovered_bool']].groupby('ID')['Day'].min()
meta['Days_to_recovery'] = meta.index.map(first_day)

# Recovered flag for meta
meta['Recovered'] = meta['Days_to_recovery'].notna().map({True: 'Recovered', False: 'No recovery'})

# --- Select output columns ---
outmeta = meta[['Recovered', 'Recovery_status', 'Days_to_recovery']]

# --- Save ---
outmeta.to_csv('results/filtered/recovery_status.tsv', sep='\t')

