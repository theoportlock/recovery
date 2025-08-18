#!/usr/bin/env python

import argparse
import pandas as pd
from mofapy2.run.entry_point import entry_point


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run MEFISTO on multi-omic input data with optional covariates"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input TSV file containing merged omics data (with SampleID, SubjectID, Timepoint)"
    )
    parser.add_argument(
        "-o", "--output",
        default="results/mofa/mofa_model.hdf5",
        help="Output path for the trained MEFISTO model (HDF5 format)"
    )
    parser.add_argument(
        "--factors",
        type=int,
        default=10,
        help="Number of factors to train (default: 10)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--n_grid",
        type=int,
        default=10,
        help="Number of grid points for temporal smoothing (default: 10)"
    )
    return parser.parse_args()


def main(args):
    # Load merged data
    df = pd.read_csv(args.input, sep="\t")

    # Setup MEFISTO entry point
    ent = entry_point()
    ent.set_data_options(
        center_groups=False,
        scale_groups=False,
        likelihoods="gaussian"
    )
    ent.set_data_df(df, sample_id_name="SampleID", group_id_name="SubjectID")

    # Add covariates if present
    if "timepoint" in df.columns:
        ent.set_covariates(sample_covariates=df[["SampleID", "timepoint"]],
                           covariates_names="timepoint")

    # Model and training options
    ent.set_model_options(factors=args.factors)
    ent.set_train_options(seed=args.seed)
    ent.set_smooth_options(n_grid=args.n_grid, start_opt=50, opt_freq=50)

    # Train model
    ent.build()
    ent.run()

    # Save output
    ent.save(args.output)
    print(f"Model saved to {args.output}")


if __name__ == "__main__":
    args = parse_args()
    main(args)

