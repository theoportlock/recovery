import pandas as pd

dataset_lables = pd.read_csv('../conf/dataset_labels.tsv', sep='\t', index_col=0)
df = pd.read_csv('../results/aa_perm.tsv', sep='\t', index_col=0)

df.index = df.index.str.replace('.tsv','').str.replace('.*/','', regex=True)
df = df.dropna()

df.drop(columns=['Unnamed: 1'], inplace=True)

df = df.join(dataset_lables[['name','class']]).set_index('name')

df.to_csv('../results/aa_perm_formatted.tsv', sep='\t')

