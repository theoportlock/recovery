#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Determine recovery status and days-to-recovery from anthropometry data."
    )

    parser.add_argument(
        "--anthro",
        default="results/filtered/anthro.tsv",
        help="Anthropometry table (default: %(default)s)",
    )

    parser.add_argument(
        "--meta",
        default="results/filtered/meta.tsv",
        help="Participant metadata (default: %(default)s)",
    )

    parser.add_argument(
        "--timemeta",
        default="results/filtered/timemeta.tsv",
        help="Timepoint metadata (default: %(default)s)",
    )

    parser.add_argument(
        "--surveillance",
        default="results/filtered/surveillance.tsv",
        help="Surveillance table (default: %(default)s)",
    )

    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=-2,
        help="WLZ/WAZ threshold defining recovery (default: %(default)s)",
    )

    parser.add_argument(
        "-o", "--output",
        default="results/filtered/recovery_status.tsv",
        help="Output TSV file (default: %(default)s)",
    )

    return parser.parse_args()


def main():

    args = parse_args()

    # --- Load data ---
    df = pd.read_csv(args.anthro, sep="\t", index_col=0)
    meta = pd.read_csv(args.meta, sep="\t", index_col=0)
    timemeta = pd.read_csv(args.timemeta, sep="\t", index_col=0)
    surveil = pd.read_csv(args.surveillance, sep="\t", index_col=0)

    thresh = args.threshold

    # --- Merge anthropometry with time metadata ---
    allvars = timemeta.join(df[["WLZ_WHZ"]]).dropna(subset=["WLZ_WHZ"])

    # --- Define recovery booleans ---
    allvars["Recovered"] = allvars["WLZ_WHZ"] > thresh

    # Year 1 recovery (≤15 months)
    filt = allvars.query("timepoint <= 15").copy()
    yr1_recovered = filt.groupby("subjectID")["Recovered"].any().astype(bool)

    # Year 2 recovery (52 weeks)
    filt = allvars.query("timepoint == 52").copy()
    yr2_recovered = filt.groupby("subjectID")["Recovered"].any().astype(bool)

    # --- Focus on MAM participants ---
    meta = meta.loc[meta["Condition"] == "MAM"].copy()

    # --- Define Recovery_status categories ---
    meta["Recovery_status"] = "No recovery"

    sustained = yr1_recovered & yr2_recovered
    meta.loc[meta.index.isin(sustained[sustained].index),
             "Recovery_status"] = "Sustained recovery"

    unsustained = yr1_recovered & ~yr2_recovered
    meta.loc[meta.index.isin(unsustained[unsustained].index),
             "Recovery_status"] = "Unsustained recovery"

    delayed = ~yr1_recovered & yr2_recovered
    meta.loc[meta.index.isin(delayed[delayed].index),
             "Recovery_status"] = "Delayed recovery"

    # --- Optional: Check category counts ---
    print(meta["Recovery_status"].value_counts())

    # --- Days to recovery (first day WLZ_WHZ > thresh) ---
    df = df.copy()
    idx = df.index.to_series().astype(str)

    split_index = idx.str.split("_", expand=True)
    df["ID"] = split_index[0]
    df["Day"] = split_index[1].astype(int)

    df["Recovered_bool"] = df["WLZ_WHZ"] > thresh

    first_day = df[df["Recovered_bool"]].groupby("ID")["Day"].min()
    meta["Days_to_recovery"] = meta.index.map(first_day)

    meta["Recovered"] = meta["Days_to_recovery"].notna().map(
        {True: "Recovered", False: "No recovery"}
    )

    # --- Select output columns ---
    outmeta = meta[["Recovered", "Recovery_status", "Days_to_recovery"]]

    # --- Save ---
    outmeta.to_csv(args.output, sep="\t")


if __name__ == "__main__":
    main()
