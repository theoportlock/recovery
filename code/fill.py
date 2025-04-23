import pandas as pd
import sys

file = '../results/pathways.tsv'
file = sys.argv[1]

df = pd.read_csv(file, sep='\t', index_col=[0,1])
df = df.fillna(0.0)
df.to_csv(file, sep='\t')

