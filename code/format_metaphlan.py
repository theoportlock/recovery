#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
'''
import numpy as np
import pandas as pd

taxo = pd.read_csv('../data/m4efad_metaphlan3_profiles_april2024.tsv', sep='\t', index_col=0, header=1)
samplesheet = pd.read_csv('../results/samplesheet.tsv', sep='\t', index_col=0)

taxo.columns = taxo.columns.str.replace('\.metaphlan','', regex=True)
taxo = taxo.loc[~taxo.index.str.contains('k__Viruses')]
taxo = taxo.loc[~taxo.index.str.contains('UNKNOWN')]
taxo = taxo.iloc[:, 1:]
species = taxo.loc[taxo.index.str.contains('s__')]
species.index = species.index.str.replace('.*\|s__','', regex=True)
df = species
df = df.T.div(df.sum(axis=1), axis=1) # renormalize
df = df.join(samplesheet[['subjectID','timepoint']]).dropna().set_index(['subjectID','timepoint'])
df.columns.name = 'species'
df = df.stack().to_frame('relative_abundance').reset_index()
df = df.loc[df.relative_abundance != 0]
df['timepoint'] = df.timepoint.astype(int)

df.to_csv('../results/species.tsv', sep='\t', index=False)

