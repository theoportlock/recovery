#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Compute log differences between baseline and one-year samples.")
    parser.add_argument('-i', '--input', type=Path, required=True,
                        help='Path to input dataset file (e.g., results/aanoyr3.tsv)')
    parser.add_argument('-m', '--meta', type=Path, required=True,
                        help='Path to timemeta.tsv file')
    parser.add_argument('-o', '--output', type=Path, required=True,
                        help='Path to output file (e.g., results/aadiff.tsv)')
    return parser.parse_args()

def calculate_deltas(df):
    """Compute differences between baseline (week 0) and one-year (week 52)."""
    bl = df.query('timepoint == 0').drop(columns=['timepoint'])
    oneyr = df.query('timepoint == 52').drop(columns=['timepoint'])
    
    # Ensure indices match
    common_idx = bl.index.intersection(oneyr.index)
    bl, oneyr = bl.loc[common_idx], oneyr.loc[common_idx]
    
    diff = oneyr.sub(bl)
    return diff

def main():
    args = parse_arguments()

    # Load data
    dataset = pd.read_csv(args.input, sep='\t', index_col=0)
    timemeta = pd.read_csv(args.meta, sep='\t', index_col=0)

    # Merge metadata with dataset
    df = timemeta[['subjectID', 'timepoint']].join(dataset, how='inner').set_index('subjectID')

    # Calculate deltas
    diff = calculate_deltas(df)

    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Save
    diff.to_csv(args.output, sep='\t')
    print(f"Saved delta file to {args.output}")

if __name__ == "__main__":
    main()
