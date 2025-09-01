#!/usr/bin/env python
import pandas as pd
import sys
from mofapy2.run.entry_point import entry_point

# ----------------------------------------------------
# Load and preprocess the data
# ----------------------------------------------------
data = sys.argv[1]
output = sys.argv[2]

# Read input data
df = pd.read_csv(data, sep="\t")
df['sample'] = df['sample'].str.strip()
df['group'] = df['group'].str.strip()
df = df.set_index('sample', drop=False)

# ----------------------------------------------------
# Create samples_metadata dictionary
# ----------------------------------------------------
unique_samples_df = df[['group', 'timepoint', 'sample']].drop_duplicates().set_index('sample')
samples_metadata_dict = {}

for g in df['group'].unique():
    group_samples = df[df['group'] == g]['sample'].unique()
    tmp_df = (
        df.loc[df['sample'].isin(group_samples), ['sample', 'timepoint']]
        .drop_duplicates()
        .set_index('sample')
    )
    tmp_df = tmp_df.loc[group_samples]

    if tmp_df.shape[0] != len(group_samples):
        print(f"⚠ Mismatch in group {g}: data has {len(group_samples)} samples, meta has {tmp_df.shape[0]}")

    samples_metadata_dict[g] = tmp_df

# ----------------------------------------------------
# Initialize and configure MEFISTO
# ----------------------------------------------------
ent = entry_point()

# Filter groups with at least 2 samples
valid_groups = [g for g, meta in samples_metadata_dict.items() if meta.shape[0] > 1]
df = df[df['group'].isin(valid_groups)]
samples_metadata_dict = {g: samples_metadata_dict[g] for g in valid_groups}

# Set the main data and covariates
ent.set_data_df(df)
ent.set_covariates(samples_metadata_dict, covariates_names="timepoint")

# ----------------------------------------------------
# Options: Data, Model, Training, Smoothing
# ----------------------------------------------------
ent.set_data_options(scale_views=True)

# Model options: Start with 20 factors, let dropping handle pruning
ent.set_model_options(
    factors=10,  # initial high number
)

# Train options with factor dropping enabled
ent.set_train_options(
    iter=500,          # max iterations
    tolerance=0.01,    # stopping criterion
    startDrop=50,      # when to start dropping factors
    freqDrop=5,        # check every 5 iterations
    dropR2=0.02,       # drop factors explaining <2% variance
    seed=42
)

# Smooth options (MEFISTO temporal structure)
ent.set_smooth_options(n_grid=10, start_opt=50, opt_freq=50)

# ----------------------------------------------------
# Build, train, and save model
# ----------------------------------------------------
ent.build()
ent.run()
ent.save(output)

