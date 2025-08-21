#!/usr/bin/env python
import pandas as pd
from mofapy2.run.entry_point import entry_point

# This part of the code is unchanged from your original script
df = pd.read_csv("results/mofa/mefisto_input.tsv", sep="\t")
df['sample'] = df['sample'].str.strip()
df['group'] = df['group'].str.strip()
df = df.set_index('sample', drop=False)

# ----------------------------------------------------
# Create samples_metadata
# ----------------------------------------------------
# We need to create a dictionary of dataframes, one for each group.
# This structure is what the MOFA+ `set_covariates` method expects.
samples_metadata_dict = {}

# Iterate over each unique group in your main DataFrame
for g in df['group'].unique():
    # Filter the main DataFrame to get only the data for the current group
    # We select the 'timepoint' and 'sample' columns
    tmp_df = df[df['group'] == g][['timepoint', 'sample']]

    # Drop any duplicate rows to ensure one row per sample in this group
    tmp_df = tmp_df.drop_duplicates()

    # Set the 'sample' column as the index
    tmp_df = tmp_df.set_index('sample')

    # Store this cleaned DataFrame in our dictionary with the group name as the key
    samples_metadata_dict[g] = tmp_df

# ----------------------------------------------------
# Initialize and set options
# ----------------------------------------------------
# Initialize the entry point object
ent = entry_point()

# Set the main data DataFrame
ent.set_data_df(df)

# Now, set the covariates using the correctly structured dictionary
# The keys of the dictionary ('g') will be recognized as the groups.
# The `covariates_names` should be the name of the column you want to use as a covariate.
ent.set_covariates(samples_metadata_dict, covariates_names="timepoint")

# Set other model options as per your original script
ent.set_model_options(factors=10)
ent.set_train_options(seed=42)
ent.set_smooth_options(n_grid=10, start_opt=50, opt_freq=50)

# ----------------------------------------------------
# Build, run, save
# ----------------------------------------------------
# Build the MEFISTO model
ent.build()

# Run the model
ent.run()

# Save the model
ent.save("results/mofa/mofa_model.hdf5")

