#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import metatoolkit.functions as f
import seaborn as sns

# Load data
#subject = 'taxoDist'
subject = sys.argv[1]
df = f.load(subject)

# Load metadata
timemeta = f.load('fulltimemeta')
timemeta['Refeed'] = timemeta['Feeds_by_Randomization'].str.replace('.*\(','', regex=True).str.replace(')','').str.replace('Healthy','H', regex=True)
timemeta = timemeta[['ID', 'timepoint','Refeed']]

# Stack data
df.index = df.index.set_names('source')
df.columns = df.columns.set_names('target')
stacked = df.stack().to_frame('dist').reset_index()

# Map the ID and timepoint
stacked = stacked.merge(timemeta, left_on='source', right_index=True).rename(columns={'ID':'source_ID','timepoint':'source_timepoint', 'Refeed':'source_refeed'})
stacked = stacked.merge(timemeta, left_on='target', right_index=True).rename(columns={'ID':'target_ID','timepoint':'target_timepoint', 'Refeed':'target_refeed'})

# filter from baseline
t1distances = stacked.query("source_timepoint == 0 and target_timepoint == 0 and target_refeed == 'H'")
t1distances = t1distances[['source_ID','dist']].groupby('source_ID').mean().set_axis(['t1_dist'], axis=1)

t2distances = stacked.query("source_timepoint == 52 and target_timepoint == 52 and target_refeed == 'H'")
t2distances = t2distances[['source_ID','dist']].groupby('source_ID').mean().set_axis(['t2_dist'], axis=1)

outdf = pd.concat([t1distances, t2distances], axis=1)
foutdf = outdf.dropna()
foutdf['improvement'] = np.log(foutdf.t1_dist.div(foutdf.t2_dist))
foutdf['improvement'] = outdf.t1_dist.div(foutdf.t2_dist)

sns.histplot(foutdf.improvement)
f.savefig(subject + 'improvementhist')

# 25% improvement
odf = foutdf.improvement.gt(1.25).to_frame(subject)
f.save(odf, subject + 'recovered')

