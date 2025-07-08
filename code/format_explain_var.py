#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Format AA permutation results with dataset labels.")
    parser.add_argument('--labels', default='conf/dataset_labels.tsv', help='Path to dataset labels file (TSV)')
    parser.add_argument('--input', default='results/aa_perm.tsv', help='Path to input results file (TSV)')
    parser.add_argument('--output', default='results/aa_perm_formatted.tsv', help='Path to output file (TSV)')

    args = parser.parse_args()

    # Load files
    dataset_labels = pd.read_csv(args.labels, sep='\t', index_col=0)
    df = pd.read_csv(args.input, sep='\t', index_col=0)

    # Clean index
    df.index = df.index.str.replace('.tsv', '').str.replace('.*/', '', regex=True)
    df = df.dropna()

    # Drop unnamed column if present
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Join and format
    df = df.join(dataset_labels[['name', 'class']]).set_index('name')

    # Save
    df.to_csv(args.output, sep='\t')

if __name__ == '__main__':
    main()
