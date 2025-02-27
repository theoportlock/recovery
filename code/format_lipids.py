#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For lipid data setup
'''
import pandas as pd
import numpy as np
import metatoolkit.functions as f

# Define mapping
LEAP_COLUMN_MAPPING = {r'1001$':'000', r'3301$':'000', r'3302$':'012', r'3303$':'052'}

# Load and clean dataset1
dataset1 = pd.read_excel('../data/LEAP03_for_Theo.xlsx', index_col=0).iloc[:, 5:].reset_index()
dataset1['LEAP'] = dataset1['LEAP'].replace(LEAP_COLUMN_MAPPING, regex=True) # fix ID
dataset1.set_index('LEAP', inplace=True)
dataset1.columns = dataset1.columns.str[4:] # remove POS/NEG
dataset1.columns = dataset1.columns.str.replace('^\d*\ -\ ','', regex=True) # remove lipid ID
dataset1.columns = dataset1.columns.str.replace('\|.*','', regex=True) # remove uncertain annotations
dataset1.replace({'',np.nan}, inplace=True) # replace missing annotations with null - one sample
dataset1.dropna(inplace=True) # remove that one sample
dataset1 = dataset1.loc[:, ~dataset1.columns.str.contains('&')] # remove ambiguous peaks
dataset1 = dataset1.astype(float) # only select max reading for each metabolite:
dataset1 = dataset1.groupby(level=0, axis=1).max() # drops 126 duplicate lipids

# load and clean dataset2
dataset2 = pd.read_excel('../data/LEAP05_combined_Theo.xlsx', index_col=1).iloc[:, 4:].reset_index()
dataset2 = dataset2.loc[dataset2['M4EFaD'].astype(str).str.startswith('L')] # remove QC
dataset2['M4EFaD'] = dataset2['M4EFaD'].replace(LEAP_COLUMN_MAPPING, regex=True) # fix ID
dataset2.set_index('M4EFaD', inplace=True)
dataset2.columns = dataset2.columns.str[10:] # remove POS/NEG 
dataset2.columns = dataset2.columns.str.replace('^\d*\_','', regex=True) # remove lipid ID
dataset2 = dataset2.astype(float) # only select max reading for each metabolite:
dataset2 = dataset2.groupby(level=0, axis=1).max() # drops 58 duplicate lipids

# Load and clean baseline_dataset (dataset3)
dfp = pd.read_excel("../data/LEAP_01_&_02_combined_Theo_v03.xlsx", sheet_name='POS', index_col=0).iloc[1:,:]
dfn = pd.read_excel("../data/LEAP_01_&_02_combined_Theo_v03.xlsx", sheet_name='NEG', index_col=0).iloc[1:,:]
metabid = pd.read_excel("../data/LEAP_01_&_02_combined_Theo_v03.xlsx", sheet_name='sample IDs', index_col=0)
dfn.index = dfn.index.str.replace(r'.*_S','', regex=True).str.replace(r'.*_Q','Q', regex=True).str.replace(r'_RT_shift','', regex=True)
dfp.index = dfp.index.str.replace(r'.*_S','', regex=True).str.replace(r'.*_Q','Q', regex=True).str.replace(r'_RT_shift','', regex=True)
dfn = dfn.loc[~dfn.index.str.startswith('Q')]
dfp = dfp.loc[~dfp.index.str.startswith('Q')]
dfn.index = dfn.index.astype(int)
dfp.drop('106B', inplace=True)
dfp.index = dfp.index.astype(int)
dfp = dfp.reset_index().rename(columns={'Unnamed: 1':'treatment', 'index':'Liggins sample'}).set_index(['treatment','Liggins sample'])
dfn = dfn.reset_index().rename(columns={'Unnamed: 1':'treatment', 'index':'Liggins sample'}).set_index(['treatment','Liggins sample'])
dfn.columns = dfn.columns.str.replace('\|.*','', regex=True)
dfp.columns = dfp.columns.str.replace('\|.*','', regex=True)
df = pd.concat([dfp,dfn], join='inner', axis=1)
df = df.groupby(level=0, axis=1).max()
metabid['sample'] = metabid['sample'].str[:-4] + '1001'
metabid['Liggins sample'] = metabid['Liggins sample'].str.extract('(\d+)').astype(int)
metabid.treatment = metabid.treatment.str.upper()
metabid.set_index(['treatment','Liggins sample'], inplace=True)
metab = df.join(metabid['sample'], how='inner').set_index('sample')
df = metab.astype(float)
# filtering names
df = df.loc[:,df.columns.str.contains('\:')]
df = df.loc[:,~df.columns.str.contains('nsettled')]
df = df.loc[:,~df.columns.str.contains('Unnamed')]
df.index = df.index.to_series().replace(LEAP_COLUMN_MAPPING, regex=True)
dataset3 = df.copy()

# Merge datasets
#df = pd.concat([dataset1, dataset2], join='inner').sort_index() # 493 metabolites shared
df = pd.concat([dataset1, dataset2, dataset3]).sort_index() # 493 metabolites shared
#df = df.dropna() # Remove 3 incomplete samples
# Some of dataset3 is contained within dataset1. For BL manuscript just d3 is enough
# CHANGE THIS FOR RECOVERY
#df = dataset3.copy()
df = df.loc[df.index.str[3] != '7']
samp = 500
mol = 500
df = df.dropna(axis=0, thresh=samp).dropna(axis=1, thresh=mol).dropna()
df = df.groupby(level=0).first()

# Save
#df.to_csv('../results/lipids.tsv', sep='\t') # 468 samples, 493 lipids
f.save(df, 'lipids')
