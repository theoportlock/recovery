#!/usr/bin/env python

import argparse
import pandas as pd
from pathlib import Path

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Filter rows where 4th character in index is not '3'.")
    parser.add_argument('input_file', type=Path, help='Path to input TSV file')
    parser.add_argument('-o', '--output-file', type=Path, default=None, help='Optional path to save output file')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Read input
    df = pd.read_csv(args.input_file, index_col=0, sep='\t')

    # Filter
    df = df.loc[df.index.str[3] != '3']

    # Prepare output path
    if args.output_file is None:
        output_dir = args.input_file.parent
        output_file = output_dir / f"{args.input_file.stem}noyr3.tsv"
    else:
        output_file = args.output_file

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save
    df.to_csv(output_file, sep="\t", index=True)
    print(f"Saved filtered data to {output_file}")

if __name__ == "__main__":
    main()
