#!/usr/bin/env python

import mofax
import argparse
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser(description="Extract weights and factors from mefisto model")
parser.add_argument('--model')
parser.add_argument('--output_dir')
args = parser.parse_args()

# Create output directory safely
output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

print("Loading MOFA model...")
m = mofax.mofa_model(args.model)

print('Extracting weights')
weights = m.get_weights(df=True)
weights.to_csv(output_dir / 'weights.tsv', sep='\t')

print('Extracting factors')
factors = m.get_factors(df=True)
factors.to_csv(output_dir / 'factors.tsv', sep='\t')

