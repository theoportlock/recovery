#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('results/timepoints/yr2/anthro.tsv', sep='\t', index_col=0)
meta = pd.read_csv('results/filtered/meta.tsv', sep='\t', index_col=0)

# Just recovered
recovered = meta.loc[meta.Recovery == 'Recovered']
sus_recovered = df.loc[recovered.index, 'WLZ_WHZ'].gt(-1)
meta['Sus_recovered'] = sus_recovered

counts = meta.reset_index().groupby(['Feed','Recovery','Sus_recovered']).count()['subjectID'].reset_index()

# meta must already have: Feed, Recovery, Sus_recovered
def classify_recovery(row):
    if row['Recovery'] == 'Recovered' and row['Sus_recovered']:
        return 'Sustained recovery'
    elif row['Recovery'] == 'Recovered':
        return 'Recovered'
    else:
        return 'No recovery'

meta['Recovery_status'] = meta.apply(classify_recovery, axis=1)

# --- Count and percentage calculation ---
status_order = ['Recovered', 'Sustained recovery', 'No recovery']
colors = {
    'Recovered': '#91bfdb',           # light blue
    'Sustained recovery': '#0571b0',  # darker blue
    'No recovery': '#d73027'          # red
}

# Count per Feed × Recovery_status
counts = (
    meta.groupby(['Feed', 'Recovery_status'])
    .size()
    .reset_index(name='Count')
    .pivot(index='Feed', columns='Recovery_status', values='Count')
    .fillna(0)
    .reindex(columns=status_order)  # ensure order
)

# Percentages
percentages = counts.div(counts.sum(axis=1), axis=0) * 100

# --- Plotting ---
fig, ax = plt.subplots(figsize=(2.6, 1.5))

bottom = None
for status in status_order:
    ax.bar(
        counts.index,
        percentages[status],
        bottom=bottom,
        color=colors[status],
        label=status
    )

    # Annotate counts in the middle of each section
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
#plt.show()

