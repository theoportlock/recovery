#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

#df = pd.read_csv('../data/DhakaBangladeshLEAPE-FNIRSProcessedVariab_DATA_2024-02-12_1130 (1).csv', index_col=1, sep='\t')
df = pd.read_csv('../data/DhakaBangladeshLEAPE-FNIRSProcessedVariab_DATA_LABELS_2024-07-18_2304.csv', index_col=0)
df = df.iloc[:, :-2]

df.index = df.index + df['Event Name'].replace(
        {'12_month (Arm 2: Intervention)':'000',
         '12_month  (Arm 1: Control)':'000',
         '24_month (Arm 1: Control)':'052',
         '24_month (Arm 2: Intervention)':'052',
         '36_month (Arm 2: Intervention)':'104',
         '36_month (Arm 3: Outcome Reference)':'104'})

df = df.iloc[:,1:]
df = df.dropna() # loses 60

f.save(df, 'fnirs')

