import pandas as pd

df = pd.read_csv('../results/filtered/anthro.tsv', sep='\t', index_col=0)
meta = pd.read_csv('../results/filtered/meta.tsv', sep='\t', index_col=0)

t2 = df.query('(sampleID.str.contains("_52")) & (sampleID.str.contains("LCC1"))', engine='python')

t2 = t2.loc[t2.WLZ_WHZ.gt(-1)]

t2.index  = t2.index.str.replace('_52', '', regex=False)
t2['sus_recovery'] = True
