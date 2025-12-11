#!/usr/bin/env python3
import pandas as pd
from sklearn.metrics import adjusted_rand_score

# ---- Load data ----
meta = pd.read_csv('results/filtered/meta.tsv', index_col=0, sep='\t')
clusters = pd.read_csv('digital_twin/outcomes/subject_cluster_assignments_small.tsv', index_col=0, sep='\t')
mothers_meta = pd.read_csv('results/filtered/mothers.tsv', index_col=0, sep='\t')

# Drop BF column if present
if 'BF' in meta.columns:
    meta = meta.drop('BF', axis=1)

# Align indexes
meta = meta.loc[clusters.index]

# ---- Fill NaNs with "healthy" ----
#meta = meta.fillna('healthy')

# ---- Compute ARI for each column ----
ari_results = {}
for col in meta.columns:
    labels = meta[col].astype(str)  # ensure categorical
    cluster_labels = clusters['cluster_id']
    ari = adjusted_rand_score(labels, cluster_labels)
    ari_results[col] = ari

# ---- Save results ----
ari_df = pd.DataFrame.from_dict(ari_results, orient='index', columns=['ARI']).sort_values('ARI', ascending=False)
ari_df.to_csv('results/adjusted_rand_results.tsv', sep='\t')

print(ari_df)

outdf = pd.concat([meta,clusters,mothers_meta], axis=1, join='inner')


outdf.to_csv('results/cat_clusters.tsv', sep='\t')
