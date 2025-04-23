import pandas as pd

with open('../conf/stacked_datasets.txt') as f:
    for data in f:
        file = f'../results/{data.rstrip()}.tsv'
        df = pd.read_csv(file, sep='\t')
        df = df.set_index(df.columns[:3].to_list())
        df = df.unstack(level=2).droplevel(0,axis=1)
        df.to_csv(file, sep='\t')

