#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Theo Portlock
'''

import numpy as np
import pandas as pd

quality = pd.read_csv('data/m4efad_kneaddata_read_counts_april2024.tsv', sep='\t', index_col=0)
samplesheet = pd.read_csv('results/samplesheet.tsv', sep='\t', index_col=0)

quality = quality.loc[:,quality.columns.str.contains('final')].sum(axis=1).div(1e6).to_frame('HQ read depth (million reads)')
quality = quality.join(samplesheet.reset_index().set_index('Seq_ID')[['subjectID','timepoint']], how='inner').set_index(['subjectID','timepoint'])
df = quality.set_axis(['hq_read_depth_million_reads'], axis=1)

mapping = df.index.to_frame()
mapping['sampleID'] = mapping['subjectID'] + '_' + mapping['timepoint'].astype(str)
mapping = mapping[['sampleID', 'subjectID', 'timepoint']]
df.index = mapping['sampleID']

df.to_csv('results/quality.tsv', sep='\t')
