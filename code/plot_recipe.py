#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('data/recipe.xlsx', index_col=0)

fdf = df.loc[:,df.columns.str.contains('100')].dropna().astype(float)

sns.clustermap(fdf.apply(np.log), cmap='coolwarm', figsize=(2,4))

plt.savefig('tmp.svg')

plt.show()
