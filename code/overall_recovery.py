#!/usr/bin/env python
import pandas as pd
import sys 

# Load data
#subject = 'anthro'
subject = sys.argv[1]
dataset = pd.read_csv(subject, sep='\t', index_col=0)

def PERMANOVA(df, pval=True, full=False):
    np.random.seed(0)
    Ar_dist = distance.squareform(distance.pdist(df, metric="braycurtis"))
    DM_dist = skbio.stats.distance.DistanceMatrix(Ar_dist)
    result = permanova(DM_dist, df.index)
    if full:
        return result
    if pval:
        return result['p-value']
    else:
        return result['test statistic']

# Load metadata
meta = pd.read_csv('results/timemeta.tsv', sep='\t', index_col=0)
meta['Refeed'] = meta['Feed'].fillna('Healthy').str.replace('.*\(','', regex=True).str.replace(')','').str.replace('Healthy','H', regex=True)

# Calculate |Ct2-Mt2X| / |Ct1-Mt1X| 
Ct2samples = meta.query("timepoint == 52 and Condition == 'Well-nourished'") # 65
Ct2 = dataset.loc[Ct2samples[Ct2samples.index.isin(dataset.index)].index]

Ct1samples = meta.query("timepoint == 0 and Condition == 'Well-nourished'") # 65
Ct1 = dataset.loc[Ct1samples[Ct1samples.index.isin(dataset.index)].index]

Mt2Xsamples = meta.query("timepoint == 52 and Condition == 'MAM' and Refeed == 'A'") # 65
Mt2X = dataset.loc[Mt2Xsamples[Mt2Xsamples.index.isin(dataset.index)].index]

Mt2Ysamples = meta.query("timepoint == 52 and Condition == 'MAM' and Refeed == 'B'") # 65
Mt2Y = dataset.loc[Mt2Ysamples[Mt2Ysamples.index.isin(dataset.index)].index]

Mt1Xsamples = meta.query("timepoint == 0 and Condition == 'MAM' and Refeed == 'A'") # 65
Mt1X = dataset.loc[Mt1Xsamples[Mt1Xsamples.index.isin(dataset.index)].index]

Mt1Ysamples = meta.query("timepoint == 0 and Condition == 'MAM' and Refeed == 'B'") # 65
Mt1Y = dataset.loc[Mt1Ysamples[Mt1Ysamples.index.isin(dataset.index)].index]

Ct1.index = ['Ct1']*Ct1.shape[0]
Ct2.index = ['Ct2']*Ct2.shape[0]
Mt1Y.index = ['Mt1Y']*Mt1Y.shape[0]
Mt1X.index = ['Mt1X']*Mt1X.shape[0]
Mt2Y.index = ['Mt2Y']*Mt2Y.shape[0]
Mt2X.index = ['Mt2X']*Mt2X.shape[0]

t2x = PERMANOVA(pd.concat([Ct2, Mt2X]), pval=False)
t2y = PERMANOVA(pd.concat([Ct2, Mt2Y]), pval=False)
t1x = PERMANOVA(pd.concat([Ct1, Mt1X]), pval=False)
t1y = PERMANOVA(pd.concat([Ct1, Mt1Y]), pval=False)

x = 100*((t1x/t2x)-1)
y = 100*((t1y/t2y)-1)

df = pd.concat([Ct1,Ct2,Mt1Y,Mt1X,Mt2Y,Mt2X])

t2xsig = PERMANOVA(pd.concat([Ct2, Mt2X]))
t2ysig = PERMANOVA(pd.concat([Ct2, Mt2Y]))
t1xsig = PERMANOVA(pd.concat([Ct1, Mt1X]))
t1ysig = PERMANOVA(pd.concat([Ct1, Mt1Y]))

output = pd.DataFrame([x, y, t1xsig, t1ysig, t2xsig,t2ysig], columns=[subject], index=['A_improvement(%)', 'B_improvement(%)', 'A_t1_pval', 'B_t1_pval', 'A_t2_pval', 'B_t2_pval']).T
print(output)

output.to_csv('results/{subject}recovery.tsv', sep='\t')


