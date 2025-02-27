#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

#df = pd.read_csv('../data/DhakaBangladeshLEAPE-GlitterWandAttractiv_DATA_LABELS_2024-03-11_0414.csv',index_col=0)
df = pd.read_csv('../data/DhakaBangladeshLEAPE-GlitterWandAttractiv_DATA_LABELS_2024-07-18_2238.csv',index_col=0)

df.index = df.index +  df['Event Name'].replace(
        {'12_month (Arm 2: Intervention)':'000',
         '12_month  (Arm 1: Control)':'000',
         '24_month (Arm 1: Control)':'052',
         '24_month (Arm 2: Intervention)':'052',
         '36_month (Arm 2: Intervention)':'104',
         '36_month (Arm 3: Outcome Reference)':'104'})
df = df.iloc[:,1:-2]
df = df.loc[~df.index.str.contains('ol')] # remove the arm1 control 36 month
df['glitter_seconds'] = df['Number of seconds child refrains from touching the glitter wand']
df = df['glitter_seconds'].to_frame()
df = df.dropna()

f.save(df, 'glitter')

