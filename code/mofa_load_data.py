#!/usr/bin/env python

import pandas as pd
import scanpy as sc
import muon as mu
from pathlib import Path
import os
import argparse
from glob import glob

parser = argparse.ArgumentParser(description="Load modalities and metadata into MuData object")
parser.add_argument('--data-dir', default='results/timepoints/yr1')
parser.add_argument('--meta-file', default='results/filtered/meta.tsv')
parser.add_argument('--output', default='results/mofa/mdata.h5mu')
args = parser.parse_args()

Path(os.path.dirname(args.output)).mkdir(parents=True, exist_ok=True)

print("Loading metadata...")
obs = pd.read_csv(args.meta_file, sep='\t', index_col=0)

print("Loading modalities...")
data_files = glob(f'{args.data_dir}/*')
if not data_files:
    print(f"Error: No data files found in {args.data_dir}")
    exit()

mods = {Path(f).stem: sc.AnnData(pd.read_csv(f, sep='\t', index_col=0)) for f in data_files}
mdata = mu.MuData(mods)
mdata.obs = mdata.obs.join(obs, how='inner')

print("Saving MuData object...")
mdata.write(args.output)
print(f"Saved MuData to {args.output}")

