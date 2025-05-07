#!/usr/bin/env python

import pandas as pd

df = pd.read_csv('../results/filtered/surveillance.tsv', sep='\t', index_col=0)
meta = pd.read_csv('../results/filtered/meta.tsv', sep='\t', index_col=0)



#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kruskal

# Load data
df = pd.read_csv('../results/filtered/surveillance.tsv', sep='\t', index_col=0)
meta = pd.read_csv('../results/filtered/meta.tsv', sep='\t', index_col=0)

# Merge on subjectID
merged = df[['days_to_recovery']].join(meta)

# Drop rows with missing days_to_recovery
merged = merged.dropna(subset=['days_to_recovery'])

# Define categorical columns to compare
categorical_cols = ['Sex', 'Ethnicity', 'Condition', 'Feed', 'Recovery', 'Delivery_Mode', 'Supplementation', 'PoB']

# Loop through each categorical variable
for col in categorical_cols:
    if col not in merged.columns:
        continue

    print(f"\n=== {col} ===")

    # Grouped data
    grouped = merged.groupby(col)['days_to_recovery'].apply(list)

    # Ensure there are at least 2 groups with data
    if len(grouped) < 2:
        print("Not enough groups to compare.")
        continue

    # Statistical test
    stat, p = kruskal(*grouped)
    print(f"Kruskal-Wallis H-test: H={stat:.2f}, p={p:.4f}")

    # Boxplot
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=merged, x=col, y='days_to_recovery')
    plt.title(f"Days to Recovery by {col}\nKruskal-Wallis p={p:.4f}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

