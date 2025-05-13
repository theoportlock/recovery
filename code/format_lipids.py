#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Theo Portlock
Purpose: Setup and clean lipid data for analysis
"""

import pandas as pd
import numpy as np

# Define a mapping to fix LEAP IDs using regular expressions.
LEAP_COLUMN_MAPPING = {
    r'1001$': '000',
    r'3301$': '000',
    r'3302$': '012',
    r'3303$': '052'
}

# ------------------------------
# Load and clean dataset1
# ------------------------------
# Read the Excel file, skipping the first 5 columns and resetting the index.
dataset1 = pd.read_excel('data/LEAP03_for_Theo.xlsx', index_col=0).iloc[:, 5:].reset_index()

# Fix the LEAP IDs using the mapping
dataset1['LEAP'] = dataset1['LEAP'].replace(LEAP_COLUMN_MAPPING, regex=True)
# Set the 'LEAP' column as the new index
dataset1.set_index('LEAP', inplace=True)

# Clean column names:
dataset1.columns = dataset1.columns.str[4:]                              # Remove leading 4 characters (POS/NEG)
dataset1.columns = dataset1.columns.str.replace(r'^\d*\ -\ ', '', regex=True)  # Remove numeric IDs and hyphen
dataset1.columns = dataset1.columns.str.replace(r'\|.*', '', regex=True)     # Remove uncertain annotations

# Replace empty strings with NaN for proper missing value handling
dataset1.replace({'': np.nan}, inplace=True)
# Remove any rows that now contain NaN values (e.g., one problematic sample)
dataset1.dropna(inplace=True)
# Remove columns with ambiguous peaks (columns containing '&')
dataset1 = dataset1.loc[:, ~dataset1.columns.str.contains('&')]

# Convert all values to float for numerical operations
dataset1 = dataset1.astype(float)
# Remove duplicate lipid entries by grouping on column names.
# Transpose, group by the duplicate column labels and take the maximum value, then transpose back.
dataset1 = dataset1.T.groupby(level=0).max().T  # drops 126 duplicate lipids

# ------------------------------
# Load and clean dataset2
# ------------------------------
# Read the Excel file and skip the first 4 columns, then reset index.
dataset2 = pd.read_excel('data/LEAP05_combined_Theo.xlsx', index_col=1).iloc[:, 4:].reset_index()

# Remove QC samples by filtering rows where the 'M4EFaD' column starts with 'L'
dataset2 = dataset2.loc[dataset2['M4EFaD'].astype(str).str.startswith('L')]
# Fix the IDs in 'M4EFaD' using the defined mapping
dataset2['M4EFaD'] = dataset2['M4EFaD'].replace(LEAP_COLUMN_MAPPING, regex=True)
# Set 'M4EFaD' as the index
dataset2.set_index('M4EFaD', inplace=True)

# Clean column names:
dataset2.columns = dataset2.columns.str[10:]                              # Remove leading 10 characters (POS/NEG)
dataset2.columns = dataset2.columns.str.replace(r'^\d*\_', '', regex=True)   # Remove numeric IDs and underscore

# Convert values to float and group duplicates:
dataset2 = dataset2.astype(float)
# Remove duplicate lipid entries (grouping on column names)
dataset2 = dataset2.T.groupby(level=0).max().T  # drops 58 duplicate lipids

# ------------------------------
# Load and clean baseline dataset (dataset3)
# ------------------------------
# Read the POS and NEG sheets, skipping the first row (assumed header)
dfp = pd.read_excel("data/LEAP_01_&_02_combined_Theo_v03.xlsx", sheet_name='POS', index_col=0).iloc[1:, :]
dfn = pd.read_excel("data/LEAP_01_&_02_combined_Theo_v03.xlsx", sheet_name='NEG', index_col=0).iloc[1:, :]

# Load the sample IDs
metabid = pd.read_excel("data/LEAP_01_&_02_combined_Theo_v03.xlsx", sheet_name='sample IDs', index_col=0)

# Clean up row indices for dfn and dfp using regex substitutions:
dfn.index = dfn.index.str.replace(r'.*_S', '', regex=True) \
                     .str.replace(r'.*_Q', 'Q', regex=True) \
                     .str.replace(r'_RT_shift', '', regex=True)
dfp.index = dfp.index.str.replace(r'.*_S', '', regex=True) \
                     .str.replace(r'.*_Q', 'Q', regex=True) \
                     .str.replace(r'_RT_shift', '', regex=True)

# Remove rows starting with 'Q'
dfn = dfn.loc[~dfn.index.str.startswith('Q')]
dfp = dfp.loc[~dfp.index.str.startswith('Q')]

# Convert indices to integers (after cleaning)
dfn.index = dfn.index.astype(int)
dfp.drop('106B', inplace=True)  # Drop problematic sample
dfp.index = dfp.index.astype(int)

# Reset index and rename columns for consistency, then set a multi-index (treatment, Liggins sample)
dfp = dfp.reset_index().rename(columns={'Unnamed: 1': 'treatment', 'index': 'Liggins sample'}) \
       .set_index(['treatment', 'Liggins sample'])
dfn = dfn.reset_index().rename(columns={'Unnamed: 1': 'treatment', 'index': 'Liggins sample'}) \
       .set_index(['treatment', 'Liggins sample'])

# Clean column names by removing uncertain annotations in both dataframes:
dfn.columns = dfn.columns.str.replace(r'\|.*', '', regex=True)
dfp.columns = dfp.columns.str.replace(r'\|.*', '', regex=True)

# Concatenate the POS and NEG datasets along columns, keeping only shared columns.
df = pd.concat([dfp, dfn], join='inner', axis=1)
# Group duplicate lipid entries by transposing, grouping, taking maximum values, then transposing back.
df = df.T.groupby(level=0).max().T

# Process the sample ID dataframe (metabid):
metabid['sample'] = metabid['sample'].str[:-4] + '1001'
metabid['Liggins sample'] = metabid['Liggins sample'].str.extract('(\d+)').astype(int)
metabid.treatment = metabid.treatment.str.upper()
metabid.set_index(['treatment', 'Liggins sample'], inplace=True)

# Join the metadata sample information to the combined data
metab = df.join(metabid['sample'], how='inner').set_index('sample')
df = metab.astype(float)

# ------------------------------
# Filtering and merging datasets
# ------------------------------
# Filter columns: keep only those with names that contain ':' and remove unwanted columns
df = df.loc[:, df.columns.str.contains('\:')]
df = df.loc[:, ~df.columns.str.contains('nsettled')]
df = df.loc[:, ~df.columns.str.contains('Unnamed')]

# Replace sample IDs in the index using the mapping
df.index = df.index.to_series().replace(LEAP_COLUMN_MAPPING, regex=True)
# Save a copy as dataset3 for later merge
dataset3 = df.copy()

# Merge datasets (dataset1, dataset2, and dataset3) and sort by index.
df = pd.concat([dataset1, dataset2, dataset3]).sort_index()

# Remove samples where the 4th character of the index is '7'
df = df.loc[df.index.str[3] != '7']

# Further filtering: drop rows/columns with too many missing values.
samp = 500  # threshold for rows
mol = 500   # threshold for columns
df = df.dropna(axis=0, thresh=samp).dropna(axis=1, thresh=mol).dropna()
# Group by the index and keep the first occurrence to resolve duplicates
df = df.groupby(level=0).first()

# ------------------------------
# Final formatting before export
# ------------------------------
# Clean up column names: replace spaces with underscores and convert to lowercase
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.lower()

# Extract subject ID and timepoint information from the index:
idcol, timecol = df.index.str[:7], df.index.str[8:].astype(int)
df.insert(0, 'timepoint', timecol)
df.insert(0, 'subjectID', idcol)
# Set a multi-index with subjectID and timepoint
df = df.set_index(['subjectID', 'timepoint'])
# Rename the column index to 'lipid'
df.columns.name = 'lipid'

mapping = df.index.to_frame()
mapping['sampleID'] = mapping['subjectID'] + '_' + mapping['timepoint'].astype(str)
mapping = mapping[['sampleID', 'subjectID', 'timepoint']]
df.index = mapping['sampleID']

# Export the final data to a TSV file
df.to_csv('results/lipids.tsv', sep='\t')
