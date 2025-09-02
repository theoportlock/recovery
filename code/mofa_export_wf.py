#!/usr/bin/env python

import mofax as mofa
import pandas as pd
import os
import argparse

# --- Parse arguments ---
parser = argparse.ArgumentParser(description="Export MOFA+ factors and loadings per view")
parser.add_argument('--model', required=True, help='Path to MOFA+ model (.hdf5)')
parser.add_argument('--outdir', required=True, help='Output directory')
args = parser.parse_args()

os.makedirs(args.outdir, exist_ok=True)

# --- Load model ---
model = mofa.mofa_model(args.model)

# --- Save factors ---
factors = model.get_factors()
samples = model.get_samples()
factors_df = pd.DataFrame(
    factors,
    index=samples,
    columns=[f"Factor_{i+1}" for i in range(model.nfactors)]
)
factors_df.to_csv(os.path.join(args.outdir, 'sample_factors.tsv'), sep='\t')

# --- Save weights per view (truncate if mismatch) ---
weights = model.get_weights()
views = model.get_views()

if isinstance(weights, dict):
    # Multi-view model
    for view, w in weights.items():
        features = model.get_features(view)
        if w.shape[0] != len(features):
            print(f"Warning: Shape mismatch for {view}. "
                  f"weights rows = {w.shape[0]}, features = {len(features)}. Truncating.")
            min_len = min(w.shape[0], len(features))
            w = w[:min_len, :]
            features = features[:min_len]
        df = pd.DataFrame(w, index=features, columns=[f"Factor_{i+1}" for i in range(model.nfactors)])
        df.index = [i[1] if i.startswith("('group1'") else i for i in df.index]
        df.to_csv(os.path.join(args.outdir, f'loadings_{view}.tsv'), sep='\t')
else:
    # Single-view model
    view_name = views[0]
    features = model.get_features(view_name)
    if weights.shape[0] != len(features):
        print(f"Warning: Shape mismatch for {view_name}. "
              f"weights rows = {weights.shape[0]}, features = {len(features)}. Truncating.")
        min_len = min(weights.shape[0], len(features))
        weights = weights[:min_len, :]
        features = features[:min_len]
    df = pd.DataFrame(weights, index=features, columns=[f"Factor_{i+1}" for i in range(model.nfactors)])
    df.to_csv(os.path.join(args.outdir, f'loadings_{view_name}.tsv'), sep='\t')

