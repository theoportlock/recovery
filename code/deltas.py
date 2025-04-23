#!/usr/bin/env python
import pandas as pd
import numpy as np

# Function to compute log differences between baseline (week 0) and one-year (week 52)
def calculatedeltas(filepath):
    bl = dataset.query('timepoint == 0').drop(columns=['timepoint'])
    oneyr = dataset.query('timepoint == 52').drop(columns=['timepoint'])
    
    # Ensure indices match before division
    common_idx = bl.index.intersection(oneyr.index)
    bl, oneyr = bl.loc[common_idx], oneyr.loc[common_idx]
    
    #diff = oneyr.div(bl).apply(np.log)  # Log fold-change
    diff = oneyr.sub(bl)  # Just subtraction
    return diff

# Process timepoint datasets
with open('../conf/timedatasets.txt') as f:
    for filepath in f:
        dataset_path = filepath.strip()
        try:
            dataset = pd.read_csv(f'../results/{dataset_path}.tsv', sep='\t', index_col=0)
            diff = calculatedeltas(dataset_path)
            diff.to_csv(f'../results/{dataset_path}diff.tsv', sep='\t')
        except Exception as e:
            print(f"Error processing {dataset_path}: {e}")

