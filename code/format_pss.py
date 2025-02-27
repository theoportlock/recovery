#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

# Mother stress Perceived stress scale
df = pd.read_csv('../data/DhakaBangladeshLEAPE-PSS_DATA_LABELS_2024-07-18_2240.csv',index_col=0)
translated = pd.read_csv('../data/PSS_translated.tsv', sep='\t', header=None)
df.index = df.index + df['Event Name'].replace(
        {'12_month (Arm 2: Intervention)':'000',
         '12_month  (Arm 1: Control)':'000',
         '24_month (Arm 1: Control)':'052',
         '24_month (Arm 2: Intervention)':'052',
         '36_month (Arm 2: Intervention)':'104',
         '36_month (Arm 3: Outcome Reference)':'104'})
df = df.iloc[:,3:-1]
df.columns = translated[0]
mapper = {'Never':0,
          'Almost Never':1,
          'Sometimes':2,
          'Fairly Often':3,
          'Very Often':4}
df = df.replace(mapper)
df = df.loc[~df.index.str.contains('ol')]

f.save(df, 'pss')
