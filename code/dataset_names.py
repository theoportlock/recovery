#!/usr/bin/env python3

import argparse
from pathlib import Path

import pandas as pd


DATASET_NAMES = {
    "aa.tsv": "Plasma amino acids",
    "alpha_diversity.tsv": "Gut microbiome alpha diversity",
    "anthro.tsv": "Anthropometry",
    "head.tsv": "Head measurements",
    "pathways.tsv": "Gut microbiome pathways",
    "sleep.tsv": "Sleep",
    "species.tsv": "Gut microbiome species",
    "vitamin.tsv": "Plasma vitamins",
}


def main():
    parser = argparse.ArgumentParser(
        description="Convert dataset file paths to human-readable dataset names."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input TSV file",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Output TSV file",
    )

    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t")

    # Assumes the first column contains paths such as results/filtered/aa.tsv
    path_column = df.columns[0]

    df.insert(
        0,
        "dataset",
        df[path_column].map(
            lambda x: DATASET_NAMES.get(Path(x).name, Path(x).stem)
        ),
    )

    df = df.drop(columns="Unnamed: 0")


    df.to_csv(args.output, sep="\t", index=False)


if __name__ == "__main__":
    main()
