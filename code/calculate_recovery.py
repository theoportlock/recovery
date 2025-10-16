#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

# --- Load data ---
df = pd.read_csv('results/filtered/anthro.tsv', sep='\t', index_col=0)
meta = pd.read_csv('results/filtered/meta.tsv', sep='\t', index_col=0)
timemeta = pd.read_csv('results/filtered/timemeta.tsv', sep='\t', index_col=0)

# --- Merge anthropometry with time metadata ---
# Join on index, add WLZ_WHZ column, and filter out missing values
allvars = timemeta.join(df[['WLZ_WHZ']]).dropna(subset=['WLZ_WHZ'])

# --- Define recovery booleans ---
# Recovered = WLZ_WHZ > -1
allvars['Recovered'] = allvars['WLZ_WHZ'] > -1

# Year 1 recovery (≤15 months)
filt = allvars.query('timepoint <= 15').copy()
yr1_recovered = filt.groupby('subjectID')['Recovered'].any().astype(bool)

# Year 2 recovery (52 weeks)
filt = allvars.query('timepoint == 52').copy()
yr2_recovered = filt.groupby('subjectID')['Recovered'].any().astype(bool)

# --- Focus on MAM participants ---
meta = meta.loc[meta['Condition'] == 'MAM'].copy()

# --- Define categories ---
meta['Recovery_status'] = 'No recovery'  # default

# Sustained recovery (recovered early and still recovered at year 2)
meta.loc[
    meta.index.isin(yr1_recovered[yr1_recovered & yr2_recovered].index),
    'Recovery_status'
] = 'Sustained recovery'

# Unsustained recovery (recovered early but not at year 2)
meta.loc[
    meta.index.isin(meta.loc[meta['Recovery'] == 'Recovered'].index)
    & ~meta.index.isin(yr2_recovered[yr2_recovered].index),
    'Recovery_status'
] = 'Unsustained recovery'

# Delayed recovery (not recovered early but recovered at year 2)
meta.loc[
    meta.index.isin(yr2_recovered[yr2_recovered].index)
    & ~meta.index.isin(yr1_recovered[yr1_recovered].index),
    'Recovery_status'
] = 'Delayed recovery'

# --- Optional: Check category counts ---
print(meta['Recovery_status'].value_counts())

# Add any recovered
meta.loc[:, 'Recovered'] = (meta.Recovery_status != 'No recovery')
meta.loc[meta.Recovered == 1 , 'Recovered'] = 'Recovered'
meta.loc[meta.Recovered == 0, 'Recovered'] = 'No recovery'

# Save
meta[['Recovered','Recovery_status']].to_csv('results/filtered/recovery_status.tsv', sep='\t')

