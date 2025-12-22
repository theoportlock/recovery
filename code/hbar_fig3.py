#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---- Load data ----
df = pd.read_csv('results/figure3/rec_merged.tsv', sep='\t', index_col=0)
df.index.name = 'dataset'

# Stack A/B improvement into long format
stacked = (
    df[['A_improvement(%)','B_improvement(%)']]
    .stack()
    .to_frame('improvement')
    .reset_index()
    .rename(columns={'level_1': 'Feed'})
)

# Optional: sort by average improvement (nice ordering)
stacked['dataset'] = stacked['dataset'].astype(str)
ordered = (
    stacked.groupby('dataset')['improvement']
    .mean()
    .sort_values(ascending=False)
    .index
)

# ---- Plot ----
plt.figure(figsize=(4, 4))

sns.barplot(
    data=stacked,
    x='improvement',
    y='dataset',
    hue='Feed',
    orient='h',
    order=ordered,
    dodge=True,
)

# <-- Add symlog here!
plt.xscale("symlog")

plt.xlabel('Improvement (%)')
plt.ylabel('')
plt.legend(title='Feed', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig('results/figure3/hbar.svg')
plt.show()

