#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

df1 = pd.read_excel('../data/LEAP Surveillance (Group-A) till 31-Aug-2023 [Full Variable].xlsx', index_col=0)
df2 = pd.read_excel('../data/LEAP Surveillance (Group-B) till 31-Aug-2023 [Full Variable].xlsx', index_col=0)

df1 = df1.replace(99, np.nan)
df2 = df2.replace(99, np.nan)
df = pd.concat([df1, df2], axis=0)
df.loc[:, ['Cough','Rash','Antibio','ORS','Zinc']] = (df[['Cough','Rash','Antibio','ORS','Zinc']] -2).mul(-1).astype(bool)

df.drop(['Food','Date','Recover','Reason','Remarks'], axis=1, inplace=True)
df.index = 'LCC' + df.index.astype(str)

# Just look at exclusive breast feeding
df['BF'] = df.BF == 1

# Define Fever
df['Fever'] = df.Temp.gt(38)

# Calculate capsule (half is half)
df['Capsule'] = (df.Capsule - 1).div(2)

# Save
f.save(df, 'surveillance')

