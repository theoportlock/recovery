#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Theo Portlock
Script to format MetaPhlAn4 output for downstream analysis
"""

import pandas as pd

# Load MetaPhlAn3 output file, skipping the first row (contains description/metadata)
df = pd.read_csv('data/metaphlan_merged_profiles.tsv',
                 sep='\t', index_col=0, header=1)

# Load the sample metadata
samplesheet = pd.read_csv('results/cleaned/standards.tsv',
                          sep='\t', index_col=0)

# Clean column names: remove ".metaphlan" suffix
df.columns = df.columns.str.replace(r'\.metaphlan$', '', regex=True)

# Remove the first column (usually relative abundance or taxonomy rank info)
df = df.iloc[:, 1:]

# Transpose so rows are samples and columns are taxa
df = df.T

# Join sample metadata (subjectID and timepoint) and drop unmatched samples
df = df.join(samplesheet['batch']).dropna().set_index('batch').sort_index()

# Transmute and save formatted data - for alpha-diversity analysis
df.to_csv('results/cleaned/standards_metaphlan.tsv', sep='\t')


from scipy.spatial.distance import pdist, squareform
import numpy as np

# ==========================================
# 1. Inter-Batch Beta Diversity (Bray-Curtis)
# ==========================================
# Calculate pairwise Bray-Curtis distances between the standard samples across batches
# Since biological variance is 0, any distance > 0 represents technical batch variance
bray_curtis_dist = pdist(df, metric='braycurtis')
dist_matrix = pd.DataFrame(squareform(bray_curtis_dist), index=df.index, columns=df.index)

print("--- Inter-Batch Bray-Curtis Distance ---")
print(dist_matrix.T)
dist_matrix.to_csv('results/cleaned/batch_braycurtis_distances.tsv', sep='\t')

# ==========================================
# 2. Deviation from Theoretical Baseline
# ==========================================
# Define the Zymo theoretical composition (species level, relative abundance %)
theoretical_abundances = {
    's__Listeria_monocytogenes': 12.0,
    's__Pseudomonas_aeruginosa': 12.0,
    's__Bacillus_subtilis': 12.0,
    's__Escherichia_coli': 12.0,
    's__Salmonella_enterica': 12.0,
    's__Limosilactobacillus_fermentum': 12.0,
    's__Enterococcus_faecalis': 12.0,
    's__Staphylococcus_aureus': 12.0,
    's__Saccharomyces_cerevisiae': 2.0,
    's__Cryptococcus_neoformans': 2.0
}

# Extract observed abundances for the standard species from the MetaPhlAn dataframe
observed_df = pd.DataFrame(index=df.index)
for species in theoretical_abundances.keys():
    # MetaPhlAn columns are full taxonomy strings; match the species identifier
    # Summing in case of multiple strain-level (t__) columns falling under the species
    #matching_cols = [col for col in df.columns if species in col]
    matching_cols = [c for c in df.columns if c.split('|')[-1] == species]
    if matching_cols:
        observed_df[species] = df[matching_cols].sum(axis=1)
    else:
        observed_df[species] = 0.0

# Calculate the deviation (Observed % - Theoretical %)
deviation_df = observed_df.copy()
for species, theoretical_val in theoretical_abundances.items():
    deviation_df[species] = deviation_df[species] - theoretical_val

print("\n--- Deviation from Theoretical Composition (Observed - Expected %) ---")
print(deviation_df.T)
deviation_df.to_csv('results/cleaned/batch_theoretical_deviations.tsv', sep='\t')

# ==========================================
# 3. Overall Batch Bias (Mean Absolute Error)
# ==========================================
# Quantify the total distortion per batch to easily identify the most/least biased runs
batch_mae = deviation_df.abs().mean(axis=1)
batch_mae.name = 'Mean_Absolute_Error'

print("\n--- Mean Absolute Error (MAE) by Batch ---")
print(batch_mae)
batch_mae.to_csv('results/cleaned/batch_mae.tsv', sep='\t', header=True)
