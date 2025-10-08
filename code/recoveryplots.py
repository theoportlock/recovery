#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('results/filtered/anthro.tsv', sep='\t', index_col=0)
meta = pd.read_csv('results/filtered/meta.tsv', sep='\t', index_col=0)
timemeta = pd.read_csv('results/filtered/timemeta.tsv', sep='\t', index_col=0)
 
allvars = timemeta.join(df.WLZ_WHZ.gt(-1)).dropna()

filt = allvars.query('timepoint <= 15').copy()
yr1_recovered = filt.groupby('subjectID')['WLZ_WHZ'].any().astype(bool)
filt = allvars.query('timepoint == 52').copy()
yr2_recovered = filt.groupby('subjectID')['WLZ_WHZ'].any().astype(bool)

meta = meta.loc[meta.Condition == 'MAM']

# Define categories
meta['Recovery_status'] = 'No recovery'  # default

# Recovery (sustained recovery at yr2)
meta.loc[(yr1_recovered) & (yr2_recovered), 'Recovery_status'] = 'Sustained recovery'

# Unsustained recovery (recovered before 15mo, but not at yr2)
meta.loc[(meta.Recovery == 'Recovered') & (~yr2_recovered), 'Recovery_status'] = 'Unsustained recovery'

# Delayed recovery (not recovered before 15mo, but recovered at yr2)
meta.loc[(meta.Recovery != 'Recovered') & yr2_recovered, 'Recovery_status'] = 'Delayed recovery'



import matplotlib.pyplot as plt
plt.figure(figsize=(8, 6))

# --- KDE plots ---
# MAM (LCC1)
df.loc[df.index.str.contains('_0') & df.index.str.contains('LCC1'), 'WLZ_WHZ'].plot.kde(
    label='MAM (LCC1) - Week 0', color='#1f77b4', lw=2, linestyle='-')
df.loc[df.index.str.contains('_52') & df.index.str.contains('LCC1'), 'WLZ_WHZ'].plot.kde(
    label='MAM (LCC1) - Week 52', color='#1f77b4', lw=2, linestyle='--')

# Healthy (LCC2)
df.loc[df.index.str.contains('_0') & df.index.str.contains('LCC2'), 'WLZ_WHZ'].plot.kde(
    label='Healthy (LCC2) - Week 0', color='#2ca02c', lw=2, linestyle='-')
df.loc[df.index.str.contains('_52') & df.index.str.contains('LCC2'), 'WLZ_WHZ'].plot.kde(
    label='Healthy (LCC2) - Week 52', color='#2ca02c', lw=2, linestyle='--')

# --- Recovery line ---
plt.axvline(x=-1, color='red', lw=2, linestyle=':', label='Recovery threshold (WLZ/WHZ = -1)')

# --- Labels & Styling ---
plt.title('WLZ/WHZ Density by Group and Timepoint', fontsize=14, weight='bold')
plt.xlabel('WLZ / WHZ', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.legend(title='Group', fontsize=10, title_fontsize=11, frameon=False)
plt.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()


import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
from itertools import combinations
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt

# --- Define groups ---
groups = {
    'MAM_Week0':  df.loc[df.index.str.contains('_0') & df.index.str.contains('LCC1'), 'WLZ_WHZ'].dropna(),
    'MAM_Week52': df.loc[df.index.str.contains('_52') & df.index.str.contains('LCC1'), 'WLZ_WHZ'].dropna(),
    'Healthy_Week0':  df.loc[df.index.str.contains('_0') & df.index.str.contains('LCC2'), 'WLZ_WHZ'].dropna(),
    'Healthy_Week52': df.loc[df.index.str.contains('_52') & df.index.str.contains('LCC2'), 'WLZ_WHZ'].dropna(),
}

# --- Check group sizes ---
for name, data in groups.items():
    print(f"{name}: n={len(data)}")

# --- Perform pairwise Mann–Whitney tests with effect sizes ---
results = []
for (name1, data1), (name2, data2) in combinations(groups.items(), 2):
    if len(data1) == 0 or len(data2) == 0:
        results.append({
            'Group1': name1, 'Group2': name2,
            'U_stat': np.nan, 'p_value': np.nan,
            'median1': np.nan, 'median2': np.nan,
            'median_diff': np.nan, 'log2FC': np.nan
        })
        continue

    # Perform test
    stat, p = mannwhitneyu(data1, data2, alternative='two-sided')

    # Get medians
    median1, median2 = np.median(data1), np.median(data2)

    # Ensure direction is always Week0 → Week52 within same group
    if ('Week0' in name2 and 'Week52' in name1):  # if order is reversed
        name1, name2 = name2, name1
        data1, data2 = data2, data1
        median1, median2 = median2, median1

    # Median difference (52 - 0 → positive = improvement)
    median_diff = median2 - median1

    # Log2 fold change (same direction)
    shift = abs(min(data1.min(), data2.min(), 0)) + 1
    log2fc = np.log2((np.mean(data2 + shift)) / (np.mean(data1 + shift)))

    results.append({
        'Group1': name1,
        'Group2': name2,
        'U_stat': stat,
        'p_value': p,
        'median1': median1,
        'median2': median2,
        'median_diff': median_diff,
        'log2FC': log2fc
    })


res_df = pd.DataFrame(results)

# --- Correct for multiple testing ---
if res_df['p_value'].notna().any():
    _, qvals, _, _ = multipletests(res_df['p_value'].dropna(), method='fdr_bh')
    res_df.loc[res_df['p_value'].notna(), 'q_value'] = qvals
else:
    res_df['q_value'] = np.nan

res_df = res_df.sort_values('q_value', na_position='last')

print("\n=== Pairwise Mann–Whitney U Comparisons (WLZ/WHZ) ===")
print(res_df.to_string(index=False, float_format="%.3e"))

# --- KDE Plot ---
plt.figure(figsize=(8, 6))
colors = {'MAM': '#1f77b4', 'Healthy': '#2ca02c'}
styles = {'Week0': '-', 'Week52': '--'}

for label, data in groups.items():
    if len(data) > 0:
        group, time = label.split('_')
        data.plot.kde(color=colors[group], linestyle=styles[time], lw=2,
                      label=f"{group} {time.replace('Week','Week ')}")

plt.axvline(x=-1, color='red', lw=2, linestyle=':', label='Recovery threshold (WLZ/WHZ = -1)')
plt.title('WLZ/WHZ Density by Group and Timepoint', fontsize=14, weight='bold')
plt.xlabel('WLZ / WHZ', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.legend(title='Group', fontsize=10, title_fontsize=11, frameon=False)
plt.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

# --- Optional: Save results ---
res_df.to_csv("WLZ_WHZ_pairwise_MannWhitney.tsv", sep='\t', index=False)

