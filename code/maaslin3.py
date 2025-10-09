#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path
import pandas as pd


def run_maaslin3(row, input_dir, output_dir):
    """
    Run MaAsLin3 for one dataset row from the config.
    """
    name = row["data"]
    dataset_input = Path(input_dir) / f"{name}.tsv"
    dataset_output = Path(output_dir) / name
    dataset_output.mkdir(parents=True, exist_ok=True)
    metadata = row["metadata"]
    metadata_input = Path(input_dir) / f"{metadata}.tsv"

    # Required arguments
    cmd = [
        "Rscript", "maaslin3/R/maaslin3.R",
        str(dataset_input),
        str(metadata_input),
        str(dataset_output),
    ]

    # Loop through all other columns, drop NAs/empties
    for col, value in row.items():
        if col in ("data", "metadata"):
            continue
        if pd.isna(value) or str(value).strip() == "":
            continue
        cmd.append(f"--{col}")
        cmd.append(str(value))

    print(f"\n>>> Running MaAsLin3 for dataset: {name}")
    print("Command:", " ".join(map(str, cmd)))
    #subprocess.run(cmd, check=True)
    print(cmd)
    print(f">>> Finished dataset: {name}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Run MaAsLin3 for multiple datasets from a config TSV"
    )
    parser.add_argument("-c", "--config_tsv", help="Config TSV with dataset parameters")
    parser.add_argument("-i", "--input_dir", help="Input directory with dataset TSV files")
    parser.add_argument("-o", "--output_dir", help="Output directory for MaAsLin3 results")
    args = parser.parse_args()

    config = pd.read_csv(args.config_tsv, sep="\t")

    for _, row in config.iterrows():
        #if row.name == 'species': breakpoint()
        run_maaslin3(row, args.input_dir, args.output_dir)
        #print(row, args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()

