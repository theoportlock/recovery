#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Theo Portlock
For project setup
'''

import numpy as np
import pandas as pd

# for functions - in cpm
pathways = pd.read_csv("data/m4efad_humann3_pathway_cpm_april2024.tsv", index_col=0, sep='\t').T
samplesheet = pd.read_csv('results/samplesheet.tsv', sep='\t', index_col=0)

pathways.index = pathways.index.str.replace('_Abundance','')
#pathways = pathways.loc[:, ~pathways.columns.str.contains('UNMAPPED|UNINTEGRATED')]
pathways = pathways.join(samplesheet[['subjectID','timepoint']]).dropna().set_index(['subjectID','timepoint'])
df = pathways.reset_index()
df['timepoint'] = df.timepoint.astype(int)
pathways = df.set_index(['subjectID','timepoint'])

df = pathways.loc[:,pathways.columns[pathways.columns.str.contains('s__')]]
df.columns = df.columns.str.replace(r'\:.*s__',': ', regex=True)
df = df.loc[df.sum(axis=1) != 0, df.sum(axis=0) !=0]
df.columns.name = 'stratified_pathway'
#df = df.stack().to_frame('relative_abundance')
#df = df.loc[df.relative_abundance != 0]
df.to_csv('results/pathwaysstrat.tsv', sep='\t')

df = pathways.loc[:, ~pathways.columns.str.contains('\|')]
df.columns = df.columns.str.replace(r'\:.*','', regex=True)
df = df.T.div(df.sum(axis=1), axis=1).T
df.columns.name = 'pathway'
#df = df.stack().to_frame('relative_abundance')
#df = df.loc[df.relative_abundance != 0]

mapping = df.index.to_frame()
mapping['sampleID'] = mapping['subjectID'] + '_' + mapping['timepoint'].astype(str)
mapping = mapping[['sampleID', 'subjectID', 'timepoint']]
df.index = mapping['sampleID']

df.to_csv('results/pathways.tsv', sep='\t')
