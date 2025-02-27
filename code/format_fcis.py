#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

# FUNCTIONING IN CHRONIC ILLNESS SCORE
df = pd.read_csv('../data/DhakaBangladeshLEAPE-FCIScoringQC_DATA_LABELS_2024-07-18_2309.csv', index_col=0)

df.index = df.index + df['Event Name'].replace(
        {'12_month (Arm 2: Intervention)':'000',
         '12_month  (Arm 1: Control)':'000',
         '24_month (Arm 1: Control)':'052',
         '24_month (Arm 2: Intervention)':'052',
         '36_month (Arm 1: Control)':'104',
         '36_month (Arm 2: Intervention)':'104',
         '36_month (Arm 3: Outcome Reference)':'104'})

df = df.iloc[:,3:-3]
df['Total_FCIS'] = df['5. TOTAL SCORE  (Add all numbers in right column, including questions 3a and 3b)']
df = df['Total_FCIS'].to_frame().dropna() # loses 20

# save
f.save(df, 'fcis')

