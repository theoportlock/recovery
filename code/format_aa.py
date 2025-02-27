#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

# for amino acids
sampleout = []
sample_list = pd.read_excel('../data/Results-LEAP_Plasma_Oct 2023.xlsx', sheet_name='Sample list', index_col=0, header=1)
sampleout.append(sample_list.iloc[:, 0].dropna())
sample_list = sample_list.iloc[:,3:].set_index(sample_list.iloc[:,2])
sampleout.append(sample_list.iloc[:, 0].dropna())
sample_list = sample_list.iloc[:,3:].set_index(sample_list.iloc[:,2])
sampleout.append(sample_list.iloc[:, 0].dropna())
sample_list = sample_list.iloc[:,3:].set_index(sample_list.iloc[:,2])
sampleout.append(sample_list.iloc[:, 0].dropna())
sample_list = sample_list.iloc[:,3:].set_index(sample_list.iloc[:,2])
sampleout.append(sample_list.iloc[:, 0].dropna())
sample_list = sample_list.iloc[:,3:].set_index(sample_list.iloc[:,2])
sampleout.append(sample_list.iloc[:, 0].dropna())
sampleout = pd.concat(sampleout)
sampleout.index = sampleout.index.astype(float)
aaout=[]
for ind in range(1,7):
    df = pd.read_excel('../data/Results-LEAP_Plasma_Oct 2023.xlsx',sheet_name=f'Assay#{ind}', index_col=0).iloc[1:,:]
    df.index = pd.to_numeric(df.index, errors='coerce')
    df = df.loc[~df.index.isna()]
    aaout.append(df)
aaout = pd.concat(aaout)
out = aaout.join(sampleout.to_frame('id')).set_index('id')

# filtering
out = out.loc[out.index.str[3] != '7']
out = out.loc[out.index.str[-4] != '1']
out.index = out.index.str.replace('3301','000')
out.index = out.index.str.replace('3302','052')
out = out.loc[~(out == 'n.a.').sum(axis=1).gt(0)]
out = out.astype(float)
out = out.groupby(level=0).first()
out = out.reset_index()
out.loc[out.id.str[3] == '3', 'id'] = out.loc[out.id.str[3] == '3', 'id'].str[:-3] + '104'
out = out.set_index('id')
out = out.loc[out.index.str[2] != 'M'] # mother filter
out.columns = out.columns.str.replace(' ','_')
out.columns = out.columns.str.lower()

idcol, timecol = out.index.str[:7], out.index.str[8:].astype(int)
out.insert(0, 'timepoint',timecol)
out.insert(0, 'subjectID',idcol)
out = out.set_index(['subjectID', 'timepoint'])
f.save(out, 'aa')


