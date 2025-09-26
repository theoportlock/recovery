#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup
input_file='data/recipe.xlsx'
output='results/recipe'
os.makedirs(output, exist_ok=True)

# Plotting
var = 'SQLNS'
df = pd.read_excel(input_file, index_col=0, sheet_name=var)
# Just select 100s
fdf = df.loc[:,df.columns.str.contains('100')]
# All na are 0
fdf = fdf.fillna(0)
# Inulin and FOS
fdf.index = fdf.index.str.replace(
    "Prebiotics (combined Inulin & FOS)",
    "Prebiotics (combined Inulin & FOS) (g)"
)
# Sort out zeaxanthin
fdf.loc['Zeaxanthin (mg)','eSQ-LNS (100g)'] = 0.417
# Fix format
fdf = fdf.astype(float)
# Convert all to grams
mask = fdf.index.str.contains(r"\(mg\)")
fdf.loc[mask] = fdf.loc[mask].div(1000)
mask = fdf.index.str.contains(r"µg")
fdf.loc[mask] = fdf.loc[mask].div(1000000)
# Drop non weight columns
fdf = fdf.loc[fdf.index.str.contains(r'g\)')]
# Drop labels for units
fdf.index = fdf.index.str.replace(r'\ \(.*\)', '', regex=True)
fdf.columns = fdf.columns.str.replace(r'\ \(.*\)', '', regex=True)
# Log adjust
fdf = np.log10(fdf + 1e-6)
# Sort
fdf = fdf.loc[fdf.median(axis=1).sort_values(ascending=False).index]
# Plot
sns.clustermap(fdf, cmap='coolwarm', figsize=(1.32,4), yticklabels=True, row_cluster=False)
plt.savefig(f'{output}/{var}.svg')
plt.show()

var = 'RUTF'
df = pd.read_excel(input_file, index_col=0, sheet_name=var)
# Just select 100s
fdf = df.loc[:,df.columns.str.contains('100')]
# All na are 0
fdf = fdf.fillna(0)
# Inulin and FOS
fdf.index = fdf.index.str.replace(
    "Prebiotics (combined Inulin & FOS)",
    "Prebiotics (combined Inulin & FOS) (g)"
)
# Sort out zeaxanthin
fdf.loc['Zeaxanthin (mg)','eRUTF (100g)'] = 0.109
# Fix format
fdf = fdf.astype(float)
# Convert all to grams
mask = fdf.index.str.contains(r"\(mg\)")
fdf.loc[mask] = fdf.loc[mask].div(1000)
mask = fdf.index.str.contains(r"µg")
fdf.loc[mask] = fdf.loc[mask].div(1000000)
# Drop non weight columns
fdf = fdf.loc[fdf.index.str.contains(r'g\)')]
# Drop labels for units
fdf.index = fdf.index.str.replace(r'\ \(.*\)', '', regex=True)
fdf.columns = fdf.columns.str.replace(r'\ \(.*\)', '', regex=True)
# Log adjust
fdf = np.log10(fdf + 1e-6)
# Sort
fdf = fdf.loc[fdf.median(axis=1).sort_values(ascending=False).index]
# Plot
sns.clustermap(fdf, cmap='coolwarm', figsize=(1.37,4), yticklabels=True, row_cluster=False)
plt.savefig(f'{output}/{var}.svg')
plt.show()

