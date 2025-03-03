#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import numpy as np
import pandas as pd

wolkes = pd.read_csv('../data/DhakaBangladeshLEAPE-Wolkes_DATA_LABELS_2024-02-29_1620.csv', index_col=0).iloc[1:]

wolkes.index = wolkes.index +  wolkes['Unnamed: 1'].replace(
        {'12_month (Arm 2: Intervention)':'000',
         '12_month  (Arm 1: Control)':'000',
         '24_month (Arm 1: Control)':'052',
         '24_month (Arm 2: Intervention)':'052',
         '36_month (Arm 3: Outcome Reference)':'104'})
wolkes = wolkes.loc[:, wolkes.columns.str.contains('wolke')]
wolkes.columns = wolkes.columns.str.replace('_bangla','')
wolkes.columns = wolkes.columns.str.replace('_bangle','')
wolkes = wolkes.iloc[:, :-1]
df = wolkes.astype(float)

idcol, timecol = df.index.str[:7], df.index.str[8:].astype(int)
df.insert(0, 'timepoint',timecol)
df.insert(0, 'subjectID',idcol)
df = df.set_index(['subjectID', 'timepoint'])

df.columns = df.columns.str.replace('wolke_','')
df.columns.name = 'wolkes_category'
df = df.stack().to_frame('score')

df.to_csv("../results/wolkes.tsv", sep='\t')
