#!/usr/bin/env python
import pandas as pd
import numpy as np
import metatoolkit.functions as f
from statsmodels.stats.multitest import fdrcorrection

# load data
chisq = f.load('categories_chisq')
kruskal = f.load('numbersfilter_kruskal')
cor = f.load("numbersfiltercorrsimple")

# Apply log of odds to get negative association and tanh to make -1 to 1
chisq['effect'] = chisq.cramers_v
chisq['pval'] = chisq['pval']
chisq['test'] = 'chisq'
chisq = chisq.reset_index().set_index(['source','target'])

# Have to use diffmean here to preserve effect direction for negative numbers
kruskal['effect'] = kruskal['statistic'].apply(np.log)
kruskal['pval'] = kruskal['p_value']
kruskal['test'] = 'kruskal'
kruskal = kruskal.reset_index().set_index(['source','target'])

cor['effect'] = cor['weight']
cor['pval'] = (~cor['weight'].abs().gt(0.6)).astype(int)
cor['test'] = 'spearman'
cor = cor.reset_index().set_index(['source','target'])

# Merge
outdf = pd.concat([cor[['effect', 'pval', 'test']],
                   kruskal[['effect', 'pval', 'test']],
                   chisq[['effect', 'pval', 'test']]],
                  axis=0)

# Drop NA
outdf = outdf.dropna()

# Adjust p-values to q-values
outdf['qval'] = fdrcorrection(outdf['pval'])[1]

# Remove self connections
outdf = outdf.drop_duplicates()

# save
f.save(outdf, 'edges')
