#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from pathlib import Path
from mofapy2.run.entry_point import entry_point


def parse_args():
    parser = argparse.ArgumentParser(description="Merge multiple omics with timemeta")
    parser.add_argument("--timemeta", required=True, help="Path to timemeta table (TSV)")
    parser.add_argument("--omics", nargs="+", required=True, help="List of omics TSV files")
    parser.add_argument("--out", required=True, help="Output merged TSV (long format)")
    return parser.parse_args()


def main(args):
    # Read timemeta (index = sampleID, keep subjectID and metadata)
    timemeta = pd.read_csv(args.timemeta, sep="\t", index_col=0)
    merged_long = []

    for f in args.omics:
        fpath = Path(f)
        view = fpath.stem  # use filename (e.g. "head" from head.tsv)
        df = pd.read_csv(f, sep="\t", index_col=0)  # sampleID as index

        # Join with timemeta (align by sampleID)
        df = timemeta.join(df, how="inner")

        # Melt into long format
        df_long = df.reset_index().melt(
            id_vars=["index", "subjectID", "timepoint"]
            + [c for c in timemeta.columns if c not in ["subjectID", "timepoint"]],
            var_name="feature",
            value_name="value"
        )

        df_long["view"] = view
        merged_long.append(df_long)

    # Concatenate all omics into one long table
    final = pd.concat(merged_long, ignore_index=True)

    # Rename columns
    final = final.rename(columns={"subjectID": "group", "index": "sample"})
    print(final)

    # Save
    final.to_csv(args.out, sep="\t", index=False)


if __name__ == "__main__":
    args = parse_args()
    main(args)

