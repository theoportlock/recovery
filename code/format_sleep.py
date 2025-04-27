#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import pandas as pd

# Sleep
df = pd.read_excel('../data/DhakaBangladeshLEAPE_BISQ.xlsx', sheet_name='Final_2024-01_2024_BISQ_Cleaned', index_col=0).dropna()

df.index = df.index + df.visit_timepoint.replace({'12_month':'000', '24_month':'052'})
df['Q16'] = df['Q16'].astype(str).str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))
df = df.select_dtypes(include='number')
df = df.set_axis(['Bedtime_difficulty','Fall_asleep_time(mins)','Times_woken_up','Night_sleep(mins)','Day_sleep(mins)', 'Sleep_problematic'], axis=1)

idcol, timecol = df.index.str[:7], df.index.str[8:].astype(int)
df.insert(0, 'timepoint',timecol)
df.insert(0, 'subjectID',idcol)
df = df.set_index(['subjectID', 'timepoint'])

df.columns = df.columns.str.replace('(mins)','')

mapping = df.index.to_frame()
mapping['sampleID'] = mapping['subjectID'] + '_' + mapping['timepoint'].astype(str)
mapping = mapping[['sampleID', 'subjectID', 'timepoint']]
df.index = mapping['sampleID']

df.to_csv('../results/sleep.tsv', sep='\t')

