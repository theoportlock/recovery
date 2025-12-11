#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Theo Portlock
'''

import pandas as pd

sheets = pd.read_excel("data/04._LEAP-Mother_Enrollment_CRF.xlsx", sheet_name=[0,1], index_col=0)
labels = sheets[1].copy()
labels = labels.set_index('Field Name/Variable Name')['Description'].to_frame()
labels = labels.dropna()

df = sheets[0].copy()
df.index = 'LCC' + df.index.astype(str) 
df.index.name = 'subjectID'

var=[
'Age',
'M_Num',
'Menarche',
'Pregnanc',
'live_bir',
'BDA',
'Outcome',
'Delivery',
'Status',
'Mode',
'ANC',
'Supple',
'Hyperten',
'Diabetes',
'Prenatal',
'Depress',
'Tetanus',
'Weight',
'Height']

outdf = df[var]
outdf.loc[:, 'maternal_bmi'] = outdf['Weight'] / ((outdf['Height'] / 100) ** 2)

bools = {'Outcome':'MAMatBirth',
         'Delivery':'FacilityDelivered',
         'Status':'Twin',
         'Mode':'Caesarian',
         'ANC':'ANC',
         'Supple':'Supple',
         'Hyperten':'Hyperten',
         'Diabetes':'Diabetes',
         'Prenatal':'Prenatal',
         'Depress':'Depress',
         'Tetanus':'Tetanus'}

outdf = outdf.rename(columns=bools)
outdf['MAMatBirth'] -= 1
outdf['FacilityDelivered'] -= 1
outdf['Twin'] -= 1
outdf['Caesarian'] -= 1
outdf['ANC'] = outdf['ANC'].sub(2).mul(-1)
outdf['Supple'] = outdf['Supple'].sub(2).mul(-1)
outdf['Hyperten'] = outdf['Hyperten'].sub(2).mul(-1)
outdf['Diabetes'] = outdf['Diabetes'].sub(2).mul(-1)
outdf['Prenatal'] = outdf['Prenatal'].sub(2).mul(-1)
outdf['Depress'] = outdf['Depress'].sub(2).mul(-1)
outdf['Tetanus'] = outdf['Tetanus'].sub(2).mul(-1)
outdf.loc[:, bools.values()] = outdf.loc[:, bools.values()].astype(bool)

outdf.to_csv('results/cleaned/mothers.tsv', sep='\t')
