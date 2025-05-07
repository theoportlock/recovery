import pandas as pd

df = pd.read_csv('../results/filtered/anthro.tsv', sep='\t', index_col=0)

t2 = df.query('(sampleID.str.contains("_52")) & (sampleID.str.contains("LCC1"))', engine='python')

t2 = df.query('(sampleID.str.contains("_12")) & (sampleID.str.contains("LCC1"))', engine='python')

t2 = df.query('(sampleID.str.contains("_0")) & (sampleID.str.contains("LCC1"))', engine='python')

t2.WLZ_WHZ.gt(-1).sum()

