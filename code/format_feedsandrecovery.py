#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
'''
import pandas as pd

df = pd.read_excel("../data/LEAP Anthro Recovery status files including samples_batch4_5.xlsx", index_col=0)

df.loc[:,"Recovery"] = df.Recovery.replace({True:'Recovered',False:'No recovery'})
df.index = df.index.set_names('ID')

cols = ['Feeds by Randomization','Recovery']
df = df[cols]
df = df.rename(columns={'Feeds by Randomization':'Feed'})
df.index.name='subjectID'

df.to_csv('../results/feedandrecovery.tsv', sep='\t')

