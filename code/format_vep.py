#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import numpy as np
import pandas as pd

vep1 = pd.read_csv("../data/Dhaka_control_1yo_AllSubsAve_generatedERPvals_VEP_07-07-2023_KWC.csv", index_col=0)
vep2 = pd.read_csv("../data/Dhaka_control_2yo_AllSubsAve_generatedERPvals_VEP_13-11-2023.csv", index_col=0)
vep3 = pd.read_csv("../data/Dhaka_intervention_1yo_AllSubsAve_generatedERPvals_VEP_13-11-2023.csv", index_col=0)
vep4 = pd.read_csv("../data/Dhaka_intervention_2yo_AllSubsAve_generatedERPvals_VEP_13-11-2023.csv", index_col=0)

vep = pd.concat([vep1,vep2,vep3,vep4], axis=0)
vep.drop('Average ERP Waveform', axis=0, inplace=True)
vep.dropna(axis=1, inplace=True)
vep.index = vep.index.str.replace('_1yo.*','000', regex=True)
vep.index = vep.index.str.replace('_2yo.*','052', regex=True)
vep = vep.loc[~vep.index.str.contains('_')] # drop all with underscores as 2 (4 replicates)
vep = vep.loc[:, ~vep.columns.str.contains('All')] # drop mins
df = vep.loc[~vep.index.str.contains('1003')] # random error point

idcol, timecol = df.index.str[:7], df.index.str[8:].astype(int)
df.insert(0, 'timepoint',timecol)
df.insert(0, 'subjectID',idcol)
df = df.set_index(['subjectID', 'timepoint'])
df.columns = df.columns.str.replace(' ', '_')
df.columns.name = 'vep_feature'
#df = df.stack().to_frame('vep_value')

mapping = df.index.to_frame()
mapping['sampleID'] = mapping['subjectID'] + '_' + mapping['timepoint'].astype(str)
mapping = mapping[['sampleID', 'subjectID', 'timepoint']]
df.index = mapping['sampleID']

df.to_csv('../results/vep.tsv', sep='\t')
