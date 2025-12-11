#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simplified Descriptive Table Generator (Table 1)

Usage:
    python descriptive_table1_clean.py \
        -i results/table1/work/formatted/Demographics.tsv \
        --meta results/filtered/meta.tsv \
        -g Feed \
        -o table1.tsv

Description:
    - Merges metadata on index, keeping only the grouping column (-g)
    - Continuous variables: mean (SD)
    - Binary variables: show n (%) with a clean label (no ", 1")
    - Categorical variables: show all levels as n (%)

At some point convert this to proportion.py and groupby changes
"""

import pandas as pd
import numpy as np
import argparse


def descriptive_table(df, groupby=None):
    summary = []

    # Setup grouping
    if groupby and groupby in df.columns:
        groups = df[groupby].dropna().unique()
    else:
        df = df.copy()
        df["Overall"] = "Overall"
        groupby = "Overall"
        groups = ["Overall"]

    for col in df.columns:
        if col == groupby:
            continue

        col_data = df[col].dropna()
        if col_data.empty:
            continue

        unique_vals = col_data.unique()

        # --- Binary variable (0/1 or Yes/No etc.) ---
        if len(unique_vals) == 2 and (
            set(unique_vals).issubset({0, 1})
            or set(unique_vals).issubset({"Yes", "No"})
            or df[col].dtype == bool
        ):
            # Determine label for the "1" or "Yes" category
            if set(unique_vals).issubset({0, 1}):
                label = col
                target_val = 1
            elif set(unique_vals).issubset({"Yes", "No"}):
                label = col
                target_val = "Yes"
            else:
                label = col
                target_val = list(unique_vals)[0]  # fallback

            row = {"Variable": label}
            for g in groups:
                subset = df[df[groupby] == g]
                n_total = len(subset)
                if n_total == 0:
                    row[g] = ""
                    continue
                n_val = (subset[col] == target_val).sum()
                perc = n_val / n_total * 100 if n_total else np.nan
                row[g] = f"{n_val} ({perc:.1f}%)" if n_val > 0 else ""
            summary.append(row)

        # --- Categorical variable ---
        elif df[col].dtype == "object" or df[col].dtype.name == "category":
            for val in sorted(unique_vals):
                row = {"Variable": f"{col}, {val}"}
                for g in groups:
                    subset = df[df[groupby] == g]
                    n_total = len(subset)
                    n_val = (subset[col] == val).sum()
                    perc = n_val / n_total * 100 if n_total else np.nan
                    row[g] = f"{n_val} ({perc:.1f}%)" if n_val > 0 else ""
                summary.append(row)

        # --- Continuous variable ---
        else:
            row = {"Variable": col}
            for g in groups:
                subset = df[df[groupby] == g][col].dropna()
                if len(subset) > 0:
                    mean, sd = subset.mean(), subset.std()
                    row[g] = f"{mean:.2f} ({sd:.2f})"
                else:
                    row[g] = ""
            summary.append(row)

    # Build summary DataFrame
    summary_df = pd.DataFrame(summary)

    # Add (n=...) to group headers
    summary_df.rename(columns={
        g: f"{g} (n={len(df[df[groupby]==g])})" for g in groups
    }, inplace=True)

    return summary_df


def main():
    parser = argparse.ArgumentParser(description="Generate Table 1 descriptive summary (with metadata merge).")
    parser.add_argument("-i", "--input", required=True, help="Input TSV file (main data)")
    parser.add_argument("--meta", required=True, help="Metadata TSV file (to merge on index)")
    parser.add_argument("-g", "--groupby", required=True, help="Column name to group by (must exist in metadata)")
    parser.add_argument("-o", "--output", default="table1.tsv", help="Output TSV file")
    args = parser.parse_args()

    # Load files
    df = pd.read_csv(args.input, sep="\t", index_col=0)
    meta = pd.read_csv(args.meta, sep="\t", index_col=0)

    # Ensure grouping column exists
    if args.groupby not in meta.columns:
        raise ValueError(f"Grouping column '{args.groupby}' not found in metadata file.")

    # Merge on index, keeping only the group column from metadata
    merged = df.join(meta[[args.groupby]], how="inner")

    # Generate summary table
    summary = descriptive_table(merged, groupby=args.groupby)

    # Save
    summary.to_csv(args.output, sep="\t", index=False)
    print(f"✅ Table 1 saved to {args.output}")


if __name__ == "__main__":
    main()

