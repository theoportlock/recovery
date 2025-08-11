#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('results/timepoints/yr2/anthro.tsv', sep='\t', index_col=0)
meta = pd.read_csv('results/filtered/meta.tsv', sep='\t', index_col=0)

# Just recovered
recovered = meta.loc[meta.Recovery == 'Recovered']
sus_recovered = df.loc[recovered.index, 'WLZ_WHZ'].gt(-1)
meta['Sus_recovered'] = sus_recovered



