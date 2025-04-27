#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import pandas as pd

df = pd.read_csv('../data/DhakaBangladeshLEAPE-SpinThePotsScoring_DATA_LABELS_2024-07-18_2302.csv',index_col=0)

df.index = df.index +  df['Event Name'].replace(
        {'12_month (Arm 2: Intervention)':'000',
         '12_month  (Arm 1: Control)':'000',
         '24_month (Arm 1: Control)':'052',
         '24_month (Arm 2: Intervention)':'052',
         '36_month (Arm 3: Outcome Reference)':'104'})
df = df.iloc[:, -4:-1].dropna() # only the scores, only lose 4 samples
df = df.astype(int)

idcol, timecol = df.index.str[:7], df.index.str[8:].astype(int)
df.insert(0, 'timepoint',timecol)
df.insert(0, 'subjectID',idcol)
df = df.set_index(['subjectID', 'timepoint'])

df.columns = df.columns.str.replace(' ','_')

# Drop timepoint as all 52
df = df.droplevel(1)

df.to_csv('../results/pots.tsv', sep='\t')

