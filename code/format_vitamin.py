#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

df = pd.read_excel('../data/LEAP-WSV MS Results_Feb-Mar_2024.xlsx',sheet_name='Results Summary', index_col=0).iloc[1:,:]
df = df.set_index('Sample ID')

out = df.drop('Sample Label', axis=1)
out = out.replace('NF', np.nan)
out = out.dropna(axis=1, thresh=300).dropna()
out = out.loc[out.index.str[3] != '7']
out = out.loc[out.index.str[-4] != '1']
out.index = out.index.str.replace('3301','000')
out.index = out.index.str.replace('3302','012')
out.index = out.index.str.replace('3303','052')
out = out.astype(float)
out = out.loc[out.index.str[2] != 'M'] # lose 10 samples to mothers
out = out.reset_index()
out.loc[out['Sample ID'].str[3] == '3', 'Sample ID'] = out.loc[out['Sample ID'].str[3] == '3', 'Sample ID'].str[:-3] + '104'
out = out.set_index('Sample ID')

f.save(out, 'vitamin')
