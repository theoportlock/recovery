#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import metatoolkit.functions as f
import seaborn as sns
import matplotlib.pyplot as plt

df = f.load('allrecover')

ndf = df.iloc[:, :2]

nndf = ndf.div(100).apply(np.tanh)

nndf['B_improvement(%)'].sub(nndf['A_improvement(%)']).sort_values().plot.barh()
f.savefig('recoverydiff')

f.clustermap(nndf, figsize=(1.2,4))
f.savefig('recoverycluster')

f.polar(ndf.T)
plt.yscale('symlog')
f.savefig('polarrecovery')


