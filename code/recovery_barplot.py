#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('results/timepoints/yr2/anthro.tsv', sep='\t', index_col=0)
meta = pd.read_csv('results/filtered/meta.tsv', sep='\t', index_col=0)
 
# Just filter MAM
meta = meta.loc[meta.Condition == 'MAM']
df = df.loc[meta.index]

# Recovered at yr2
yr2_recovered = df['WLZ_WHZ'].gt(-1)

# Define categories
meta['Recovery_status'] = 'No recovery'  # default

# Recovery (sustained recovery at yr2)
meta.loc[(meta.Recovery == 'Recovered') & yr2_recovered, 'Recovery_status'] = 'Sustained recovery'

# Unsustained recovery (recovered before 15mo, but not at yr2)
meta.loc[(meta.Recovery == 'Recovered') & (~yr2_recovered), 'Recovery_status'] = 'Unsustained recovery'

# Delayed recovery (not recovered before 15mo, but recovered at yr2)
meta.loc[(meta.Recovery != 'Recovered') & yr2_recovered, 'Recovery_status'] = 'Delayed recovery'

# --- Count and percentage calculation ---
status_order = ['No recovery', 'Unsustained recovery', 'Delayed recovery', 'Sustained recovery']
colors = {
    'Sustained recovery': '#0571b0',
    'No recovery': '#d73027',
    'Unsustained recovery': '#fc8d59',
    'Delayed recovery': '#2ca25f'
}

counts = (
    meta.groupby(['Feed', 'Recovery_status'])
    .size()
    .reset_index(name='Count')
    .pivot(index='Feed', columns='Recovery_status', values='Count')
    .fillna(0)
    .reindex(columns=status_order)
)

percentages = counts.div(counts.sum(axis=1), axis=0) * 100

# --- Plotting ---
fig, ax = plt.subplots(figsize=(3.2, 1.8))

bottom = None
for status in status_order:
    ax.bar(
        counts.index,
        percentages[status],
        bottom=bottom,
        color=colors[status],
        label=status
    )

    for i, (pct, cnt) in enumerate(zip(percentages[status], counts[status])):
        if pct > 0:
            y_pos = (bottom[i] if bottom is not None else 0) + pct / 2
            ax.text(
                i, y_pos, int(cnt),
                ha='center', va='center',
                fontsize=5, color='white', fontweight='bold'
            )

    bottom = (bottom + percentages[status]) if bottom is not None else percentages[status]

# --- Formatting ---
ax.set_ylabel('Percentage of participants')
ax.set_xlabel('Feed')
ax.set_ylim(0, 100)
ax.legend(title='Recovery status', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('results/stacked_bar_recovery.svg')
# plt.show()

