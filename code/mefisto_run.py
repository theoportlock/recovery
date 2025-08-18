#!/usr/bin/env python
from mofapy2.run.entry_point import entry_point
import pandas as pd

# Load long-format input
df = pd.read_csv("results/mofa/mefisto_input.tsv", sep='\t')

ent = entry_point()
ent.set_data_options(center_groups=False)
ent.set_data_df(df)

# --- Create samples_metadata for each group ---
groups = df['group'].unique()
samples_metadata = []
for g in groups:
    # select unique rows for this group, with sampleID and covariates
    tmp = df[df['group']==g][['sample', 'timepoint']].drop_duplicates().set_index('sample')
    samples_metadata.append(tmp)

ent.data_opts["samples_metadata"] = samples_metadata

# Now set covariates
ent.set_covariates("timepoint", covariates_names="timepoint")

# Model options
ent.set_model_options(factors=10)
ent.set_train_options(seed=42)
ent.set_smooth_options(n_grid=10, start_opt=50, opt_freq=50)

# Build, run, save
ent.build()
ent.run()
ent.save("results/mofa/mofa_model.hdf5")

