#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from pathlib import Path

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Create subjectID/timepoint mapping from datasets.")
    parser.add_argument('-i', '--input-file', type=Path, default=Path('conf/timedatasets.txt'),
                        help='Path to input file listing datasets (default: conf/timedatasets.txt)')
    parser.add_argument('-d', '--datasets-dir', type=Path, default=Path('results'),
                        help='Directory where dataset files are located (default: results)')
    parser.add_argument('-o', '--output-file', type=Path, default=Path('results/mapping.tsv'),
                        help='Path to output mapping TSV file (default: results/mapping.tsv)')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Read dataset list
    with args.input_file.open('r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Collect mappings
    all_mappings = []
    for filepath in lines:
        dataset_path = args.datasets_dir / f'{filepath}.tsv'
        if not dataset_path.exists():
            print(f"Warning: {dataset_path} not found. Skipping.")
            continue
        df = pd.read_csv(dataset_path, sep='\t', index_col=0)
        mapping = df.index.to_series().str.split('_', expand=True).iloc[:, :2]
        mapping.columns = ['subjectID', 'timepoint']
        mapping.index = df.index
        all_mappings.append(mapping)

    if not all_mappings:
        print("No mappings collected. Exiting.")
        return

    # Merge all mappings
    combined_mapping = pd.concat(all_mappings, axis=0, join='inner').drop_duplicates()

    # Ensure output directory exists
    args.output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save
    combined_mapping.to_csv(args.output_file, sep='\t', index=True)
    print(f"Saved combined mapping to {args.output_file}")

if __name__ == "__main__":
    main()
