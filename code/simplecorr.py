#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('results/numbersfilter.tsv', index_col=0, sep='\t')
cor = df.corr()

def to_edges(df, thresh=0.5, directional=True):
    df = df.rename_axis('source', axis=0).rename_axis("target", axis=1)
    edges = df.stack().to_frame()[0]
    nedges = edges.reset_index()
    edges = nedges[nedges.target != nedges.source].set_index(['source','target']).drop_duplicates()[0]
    if directional:
        fin = edges.loc[(edges < 0.99) & (edges.abs() > thresh)].dropna().reset_index().rename(columns={'level_0': 'source', 'level_1':'target', 0:'weight'}).set_index('source').sort_values('weight')
    else:
        fin = edges.loc[(edges < 0.99) & (edges > thresh)].dropna().reset_index().rename(columns={'level_0': 'source', 'level_1':'target', 0:'weight'}).set_index('source').sort_values('weight')
    return fin

edges = to_edges(cor)

edges.to_csv('results/numbersfiltercorrsimple.tsv', sep='\t')
