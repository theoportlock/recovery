#!/usr/bin/env python3
import pandas as pd

# ---- Load data ----
meta = pd.read_csv('results/filtered/meta.tsv', index_col=0, sep='\t')
clusters = pd.read_csv('digital_twin/outcomes/subject_cluster_assignments_small.tsv', index_col=0, sep='\t')
mothers_meta = pd.read_csv('results/filtered/mothers.tsv', index_col=0, sep='\t')

outdf = pd.concat([meta,clusters,mothers_meta], axis=1, join='inner')

outdf.to_csv('results/cat_clusters.tsv', sep='\t')
