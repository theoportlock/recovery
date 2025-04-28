import pandas as pd
import sys

# Use default file if none provided
datatable = sys.argv[1] if len(sys.argv) > 1 else '../conf/timedatasets.txt'

# Read all dataset filenames listed in the datatable
with open(datatable, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# Collect mappings from all files
all_mappings = []

for filepath in lines:
    df = pd.read_csv(f'../results/{filepath}noyr3.tsv', sep='\t', index_col=0)
    mapping = df.index.to_series().str.split('_', expand=True).iloc[:, :2]
    mapping.columns = ['subjectID', 'timepoint']
    mapping.index = df.index
    all_mappings.append(mapping)

# Merge all mappings into a single DataFrame
combined_mapping = pd.concat(all_mappings, axis=0, join='inner').drop_duplicates()

combined_mapping.to_csv('../results/mapping.tsv', sep='\t')

