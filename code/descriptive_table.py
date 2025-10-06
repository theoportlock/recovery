#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate descriptive statistics by refeeding method.
- Categorical: count (percent)
- Continuous: mean (SD)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# === CONFIGURATION ===
meta_file = Path("results/filtered/meta.tsv")
surveil_file = Path("results/filtered/surveillance.tsv")
REFEED_COL = "Feed"

# === LOAD DATA ===
meta = pd.read_csv(meta_file, sep="\t", index_col=0)
meta = meta.dropna(subset=[REFEED_COL])
surveil = pd.read_csv(surveil_file, sep="\t", index_col=0)
df = meta.join(surveil)

# Define variables
categorical_cols = ['Recovery', 'Sex', 'Delivery_Mode', 'PoB']
continuous_cols = ['BF', 'fail_no.failure', 'days_of_catchup']

# === PROCESS CATEGORICAL VARIABLES ===
summary_rows = []
groups = df[REFEED_COL].unique()

for col in categorical_cols:
    if col not in df.columns:
        continue
    # Drop NA to ensure accurate counts
    sub_df = df.dropna(subset=[col])
    categories = sub_df[col].unique()
    for cat in categories:
        row = {"Variable": f"{col}_{cat}"}
        for group in groups:
            subset = sub_df[sub_df[REFEED_COL] == group]
            n_total = len(subset)
            n_cat = (subset[col] == cat).sum()
            perc = (n_cat / n_total * 100) if n_total > 0 else np.nan
            row[group] = f"{n_cat} ({perc:.1f}%)"
        summary_rows.append(row)

# === PROCESS CONTINUOUS VARIABLES ===
for col in continuous_cols:
    if col not in df.columns:
        continue
    row = {"Variable": col}
    for group in groups:
        vals = df.loc[df[REFEED_COL] == group, col].dropna()
        mean = vals.mean()
        sd = vals.std()
        row[group] = f"{mean:.2f} ({sd:.2f})"
    summary_rows.append(row)

# === CREATE SUMMARY TABLE ===
summary_df = pd.DataFrame(summary_rows)
summary_df.set_index("Variable", inplace=True)

# Rename group columns with (n=...) format
column_renames = {
    group: f"{group} (n={len(df[df[REFEED_COL] == group])})"
    for group in groups
}
summary_df.rename(columns=column_renames, inplace=True)

# === SAVE TSV ===
tsv_output = Path("results/refeed_summary_descriptive.tsv")
summary_df.to_csv(tsv_output, sep="\t")
print(f"Saved TSV summary to {tsv_output}")
