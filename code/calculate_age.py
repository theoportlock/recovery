#!/usr/bin/env python3
"""Calculate age at each anthropometry measurement (DOM - DOB) and save to a TSV.

Takes one or more files (xlsx/xls/csv/tsv), concatenates them in the order given
(like pd.concat([anthro1, anthro2])), and writes the original columns plus age.
Requires pandas (and openpyxl for .xlsx). Example:

    python calculate_anthro_age.py \
        -i "data/06. LEAP_Child_anthropometry_for_1_Yrs_MAM ... .xlsx" \
           "data/07. LEAP_Child_Anthropometry_for_1_Yrs_Normal ... .xlsx" \
        -o anthro_age.tsv
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

DAYS_PER_MONTH = 30.4375  # 365.25 / 12
DAYS_PER_YEAR = 365.25


def parse_args():
    p = argparse.ArgumentParser(
        description="Calculate age (DOM - DOB) from anthropometry files and "
                    "write it to a separate TSV.")
    p.add_argument("-i", "--input", required=True, nargs="+", type=Path,
                   help="one or more input files (xlsx/xls/csv/tsv), concatenated in order")
    p.add_argument("-o", "--output", type=Path, default=None,
                   help="output TSV (default: <input>_age.tsv for one input, "
                        "combined_age.tsv for several, next to the first input)")
    p.add_argument("--dob-col", default="DOB", help="date of birth column (default: DOB)")
    p.add_argument("--dom-col", default="DOM",
                   help="date of measurement column (default: DOM)")
    p.add_argument("--sheet", default=0,
                   help="Excel sheet name or index (default: first sheet)")
    p.add_argument("--sep", default=None,
                   help="delimiter for text inputs (default: comma for .csv, else tab)")
    p.add_argument("--date-format", default=None,
                   help="strptime format for text dates, e.g. '%%d/%%m/%%Y'; "
                        "default lets pandas infer")
    p.add_argument("--units", nargs="+", choices=["days", "months", "years"],
                   default=["days", "months", "years"],
                   help="age units to output (default: all three)")
    p.add_argument("--keep", nargs="+", default=None, metavar="COL",
                   help="only carry these input columns into the output "
                        "(default: all input columns)")
    p.add_argument("--decimals", type=int, default=2,
                   help="decimal places for months/years (default: 2)")
    return p.parse_args()


def read_one(path, sheet, sep):
    if not path.exists():
        sys.exit(f"error: {path} not found")
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xlsm", ".xls"):
        if isinstance(sheet, str) and sheet.isdigit():
            sheet = int(sheet)
        return pd.read_excel(path, sheet_name=sheet)
    if sep is None:
        sep = "," if suffix == ".csv" else "\t"
    return pd.read_csv(path, sep=sep.encode().decode("unicode_escape"))


def to_dates(series, fmt):
    """Parse to datetime; anything unparseable becomes NaT (counted by the caller)."""
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    return pd.to_datetime(series, format=fmt, errors="coerce")


def main():
    args = parse_args()

    frames = []
    for path in args.input:
        df = read_one(path, args.sheet, args.sep)
        for col in (args.dob_col, args.dom_col):
            if col not in df.columns:
                sys.exit(f"error: column '{col}' not in {path}. "
                         f"Found: {', '.join(map(str, df.columns))}")
        print(f"read {len(df)} rows from {path}", file=sys.stderr)
        frames.append(df)
    anthro = pd.concat(frames, ignore_index=True)

    if args.keep:
        missing = [c for c in args.keep if c not in anthro.columns]
        if missing:
            sys.exit(f"error: --keep columns not found: {', '.join(missing)}")

    dob = to_dates(anthro[args.dob_col], args.date_format)
    dom = to_dates(anthro[args.dom_col], args.date_format)

    # Non-empty values that failed to parse (genuinely empty cells are not counted)
    n_bad = int(((dob.isna() & anthro[args.dob_col].notna())
                 | (dom.isna() & anthro[args.dom_col].notna())).sum())
    n_missing = int((anthro[args.dob_col].isna() | anthro[args.dom_col].isna()).sum())

    days = (dom - dob).dt.days
    ages = {}
    if "days" in args.units:
        ages["age_days"] = days.astype("Int64")
    if "months" in args.units:
        ages["age_months"] = (days / DAYS_PER_MONTH).round(args.decimals)
    if "years" in args.units:
        ages["age_years"] = (days / DAYS_PER_YEAR).round(args.decimals)

    out = anthro[args.keep] if args.keep else anthro.copy()
    for name, values in ages.items():
        out[name] = values

    if args.output:
        out_path = args.output
    else:
        first = args.input[0]
        stem = first.stem if len(args.input) == 1 else "combined"
        out_path = first.with_name(stem + "_age.tsv")
    #out = out.loc[out.An_Time == 1.0].set_index('subjectID')
    out = out.loc[out.An_Time == 1.0]
    out = out.rename(columns={'SID_LCC': 'subjectID'})
    out = out.set_index('subjectID')
    out.index = 'LCC' + out.index.astype(str)
    out[['age_days','age_months','age_years']].to_csv(out_path, sep="\t")

    print(f"wrote {len(out)} rows to {out_path}", file=sys.stderr)
    if n_missing:
        print(f"warning: {n_missing} row(s) with missing DOB or DOM (age left blank)",
              file=sys.stderr)
    if n_bad:
        print(f"warning: {n_bad} row(s) with unparseable dates (age left blank); "
              "try --date-format", file=sys.stderr)
    n_neg = int((days < 0).sum())
    if n_neg:
        print(f"warning: {n_neg} row(s) with DOM before DOB (negative age)",
              file=sys.stderr)


if __name__ == "__main__":
    main()
