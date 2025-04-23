#!/usr/bin/env python
from itertools import combinations, product
from pathlib import Path
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import metatoolkit.functions as f
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sys

dataset_names = [
'pss',
'aa',
'anthro',
'bayley',
'fnirs',
'glitter',
'lipids',
'pathways',
'psd',
'pots',
'pci',
'sleep',
'taxo',
'vep',
'wolkes',
'micro',
'head',
'fcis',
'vitamin']

# Load data
meta = f.load('meta')
datasets = {data:f.load(data) for data in dataset_names}

df = pd.concat(datasets, axis=1)
df['ID'] = df.index.astype(str).str[:7]
df['time'] = df.index.astype(str).str[-3:].astype(int)
#mamdf = df.loc[df.ID.isin(meta.loc[meta.Condition == 'MAM'].index)].drop(['ID', 'time'], axis=1)
mamdf = df.loc[df.ID.isin(meta.loc[(meta.Condition == 'MAM') & (meta.index.str[3] != '3')].index)].drop(['ID', 'time'], axis=1)
hdf = df.loc[df.ID.isin(meta.loc[meta.Condition == 'Well-nourished'].index)].drop(['ID', 'time'], axis=1)
#cmamdf = df.loc[df.index.astype(str).str.startswith('3')].drop(['ID', 'time'], axis=1)

f.setupplot(figsize=(5,5))
X, name = mamdf, 'mdata'
X, name = hdf, 'hdata'
#X, name = cmamdf, 'cmamdf'
def plot(X, name):
    ndf = (~X.isna())
    ndf = ndf.groupby(level=0, axis=1).any()
    ndf['time'] = ndf.index.astype(str).str[-3:].astype(int)
    ndf = ndf.groupby('time').sum()
    ndf = ndf.loc[ndf.nunique(axis=1).gt(2)]
    g = sns.heatmap(
        data=ndf.T,
        square=True,
        cmap="vlag",
        center=True,
        yticklabels=True,
        xticklabels=True,
        annot=True,
        fmt='',
        linewidth=0.5,
    )
    f.savefig(name)

plot(hdf, 'hdata')
plot(mamdf, 'mdata')
#plot(cmamdf, 'cmamdf')
#sns.set()
#f.upset({key: dataset.dropna().index for key, dataset in datasets.items()}, sort_by='cardinality')
