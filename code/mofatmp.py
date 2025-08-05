#!/usr/bin/env python

import pandas as pd
import io
import scanpy as sc
import muon as mu
import numpy as np
import pandas as pd
import mofax as mofa
import os
from glob import glob
from pathlib import Path
import matplotlib.pyplot as plt

data_dir = 'results/timepoints/yr1'
obs = pd.read_csv('results/filtered/meta.tsv', sep='\t', index_col=0)

data = glob(f'{data_dir}/*')
mods = {Path(i).stem:sc.AnnData(pd.read_csv(i, sep='\t', index_col=0)) for i in data}

mdata = mu.MuData(mods)
mdata.obs = mdata.obs.join(obs)

mu.tl.mofa(mdata,
           use_obs='union',
           n_factors=15,
           convergence_mode='medium',
           outfile='results/mofa/t1.hdf5')

model = mofa.mofa_model("results/mofa/t1.hdf5")

mofa.plot_r2(model, x='View', vmax=15)

mu.pl.mofa_r2(mdata, x='View', vmax=15)  # ← this is what you want

mu.pl.mofa(mdata, color='Recovery')
#mu.pp.intersect_obs(mdata)

print(model.factors.keys())     # should list factors
print(model.weights.keys())     # should list views

print(model.r2_per_view)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Extract view names
views = list(mdata.uns['mofa']['variance'].keys())

# Extract R² values per view and assemble into a DataFrame
r2_dict = {
    view: mdata.uns['mofa']['variance'][view]
    for view in views
}

# Create DataFrame with views as rows and factors as columns
r2_df = pd.DataFrame(r2_dict).T  # transpose so rows = views

# Optional: label the factor columns
r2_df.columns = [f"Factor {i}" for i in range(r2_df.shape[1])]

# Plot the heatmap
sns.heatmap(r2_df, cmap='viridis', vmax=15)
plt.title('R² per View and Factor')
plt.xlabel('Factors')
plt.ylabel('Views')
plt.tight_layout()
plt.show()

