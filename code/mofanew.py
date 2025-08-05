#!/usr/bin/env python

import pandas as pd
import scanpy as sc
import muon as mu
import mofax as mofa
import os
from glob import glob
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. Setup and Data Loading ---
DATA_DIR = 'results/timepoints/yr1'
META_FILE = 'results/filtered/meta.tsv'
OUTPUT_DIR = 'results/mofa'
MOFA_MODEL_FILE = os.path.join(OUTPUT_DIR, 't1.hdf5')

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

try:
    obs = pd.read_csv(META_FILE, sep='\t', index_col=0)
except FileNotFoundError:
    print(f"Error: Metadata file not found at {META_FILE}")
    exit()

print("Loading data modalities...")
data_files = glob(f'{DATA_DIR}/*')
if not data_files:
    print(f"Error: No data files found in {DATA_DIR}")
    exit()

mods = {Path(i).stem: sc.AnnData(pd.read_csv(i, sep='\t', index_col=0)) for i in data_files}
mdata = mu.MuData(mods)
print(f"MuData object created with views: {list(mdata.mod.keys())}")
mdata.obs = mdata.obs.join(obs, how='inner')
print("Metadata joined to MuData object.")

# --- 2. MOFA+ Analysis ---
print("\nRunning MOFA+ analysis...")
mu.tl.mofa(
    mdata,
    use_obs='union',
    n_factors=15,
    convergence_mode='medium',
    outfile=MOFA_MODEL_FILE
)
print(f"MOFA+ analysis complete. Model saved to {MOFA_MODEL_FILE}")

try:
    model = mofa.mofa_model(MOFA_MODEL_FILE)
except FileNotFoundError:
    print(f"Error: MOFA model not found at {MOFA_MODEL_FILE}")
    exit()

# --- 3. Visualization and Analysis ---
print("\nPerforming visualizations...")

# Use the model object to get the R^2 values as a long-format DataFrame
r2_long_df = model.get_variance_explained()

# Plot R^2 per view using seaborn, which is more reliable
print("Plotting R² per view...")
plt.figure(figsize=(10, 6))
sns.barplot(data=r2_long_df, x='View', y='R2', errorbar=None, estimator=np.sum)
plt.title('Total R² per View')
plt.ylabel('Total R²')
plt.xlabel('View')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Heatmap of R^2 per view and factor
print("Generating R² heatmap...")
try:
    r2_df = r2_long_df.pivot_table(
        index='View',
        columns='Factor',
        values='R2'
    )

    plt.figure(figsize=(12, 10))
    sns.heatmap(r2_df, cmap='viridis', vmax=15, annot=True, fmt=".2f")
    plt.title('R² Explained per View and Factor')
    plt.xlabel('Factors')
    plt.ylabel('Views')
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"An error occurred while generating the R² heatmap: {e}")
    print("The heatmap could not be generated.")

# --- 4. Exporting Results (Loadings and Factors) ---
print("\nExporting loadings and factors...")

# Get factor values (numpy array) and convert to a DataFrame
factors_arr = model.get_factors()
factors_df = pd.DataFrame(factors_arr, index=model.get_samples(), columns=[f"Factor_{i+1}" for i in range(model.nfactors)])
factors_output_file = os.path.join(OUTPUT_DIR, 'sample_factors.tsv')
factors_df.to_csv(factors_output_file, sep='\t')
print(f"Sample factors exported to {factors_output_file}")

# Get loadings
weights = model.get_weights()

# Force the weights into a dictionary format for consistent processing
if not isinstance(weights, dict):
    single_view_name = model.get_views()[0]
    weights = {single_view_name: weights}

# Now, we can reliably loop through the dictionary
for view_name, weights_arr in weights.items():
    # Use the feature names directly from the MuData object, which is more reliable
    try:
        features = mdata[view_name].var_names
    except KeyError:
        print(f"Warning: Could not find features for view '{view_name}' in the MuData object. Skipping export.")
        continue

    # Check for shape mismatch before creating the DataFrame
    if weights_arr.shape[0] != len(features):
        print(f"Warning: Shape mismatch for view '{view_name}'.")
        print(f"Weights shape: {weights_arr.shape}, Features length: {len(features)}")
        print("Skipping export for this view.")
        continue

    # Create the DataFrame with the correct number of rows and labels
    weights_df = pd.DataFrame(weights_arr, index=features, columns=[f"Factor_{i+1}" for i in range(model.nfactors)])
    weights_output_file = os.path.join(OUTPUT_DIR, f'loadings_{view_name}.tsv')
    weights_df.to_csv(weights_output_file, sep='\t')
    print(f"Loadings for view '{view_name}' exported to {weights_output_file}")

print("\nScript finished successfully.")
