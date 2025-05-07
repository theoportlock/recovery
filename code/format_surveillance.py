#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import numpy as np
import pandas as pd

# Load data
df1 = pd.read_excel('../data/LEAP Surveillance (Group-A) till 31-Aug-2023 [Full Variable].xlsx', index_col=0)
df2 = pd.read_excel('../data/LEAP Surveillance (Group-B) till 31-Aug-2023 [Full Variable].xlsx', index_col=0)

# Clean and merge
df1 = df1.replace(99, np.nan)
df2 = df2.replace(99, np.nan)
df = pd.concat([df1, df2], axis=0)

# Convert symptom responses to boolean cleanly
cols = ['Cough', 'Rash', 'Antibio', 'ORS', 'Zinc']
df_bool = (df[cols] - 2).mul(-1).fillna(0).astype(bool)
df[cols] = df_bool.astype('boolean')  # Nullable BooleanDtype for compatibility

# Drop irrelevant columns
#df.drop(['Food', 'Date', 'Recover', 'Reason', 'Remarks'], axis=1, inplace=True)
df.drop(['Date', 'Recover', 'Remarks'], axis=1, inplace=True)

# Index renaming
df.index = 'LCC' + df.index.astype(str)

# Exclusive breast feeding (1 = True)
df['BF'] = df['BF'] == 1

# Fever defined as temperature > 38
df['Fever'] = df['Temp'].gt(38)

# Capsule calculation (half = 0.5)
df['Capsule'] = (df['Capsule'] - 1).div(2)

# Calculate timepoint in weeks, then round up
df['timepoint'] = pd.to_timedelta(df['Day'] - 1, unit='D') / np.timedelta64(1, 'W')
df = df.dropna(subset=['timepoint'])
df['timepoint'] = df['timepoint'].apply(np.ceil).astype(int)

# Set index
df['subjectID'] = df.index
df = df.set_index(['subjectID', 'timepoint'])

# Work out days to recovery
days_of_catchup = df.reset_index().groupby(['Food','subjectID'])['Day'].last().xs(1)
#days_of_catchup[days_of_catchup == 90.0] = np.nan
days_of_catchup = days_of_catchup.rename('days_of_catchup')

## quick and dirty analyis
#meta= pd.read_csv('../results/meta.tsv', sep='\t', index_col=0)
#meta['dtr'] = days_to_recovery
#sns.kdeplot(data=meta,x='dtr', hue='Feed')

# Base core body temperature
base_body_temp = df.reset_index().groupby(['subjectID'])['Temp'].first()
base_body_temp = base_body_temp.rename('base_temp')

# Comorbidities
## Sort out vomiting and diarrhoea so that it's just at least once per day
df['DS'] = df['DS'] != 0.0
df['Vomiting'] = df['Vomiting'] != 0.0
avs = df.reset_index().groupby(['subjectID']).mean()
avs = avs[['Fever','DS','Cough','Rash','Antibio','ORS','Zinc']].astype(float)
avs = avs.set_axis(['fever','diarrhoea','cough','rash','antibiotic','ors','zinc'], axis=1)

# Comp foods
comp = df.reset_index().groupby(['subjectID'])['Complemt'].value_counts(normalize=True, dropna=False).unstack().fillna(0)
comp.columns = comp.columns.astype(str)
mapping = {'1.0':'comp_khichuri',
           '2.0':'comp_suji',
           '3.0':'comp_halwa',
           '4.0':'comp_cookies.ruti.bread',
           '5.0':'comp_rice.and.curry',
           '6.0':'comp_tea.drinks.juice',
           '7.0':'comp_others',
           'nan':'comp_none'}
comp = comp.rename(columns=mapping)

# Reason for feeding failure
b = df.reset_index().groupby(['subjectID'])['Reason'].value_counts(normalize=True, dropna=False).unstack().fillna(0)
b.columns = b.columns.astype(str)
mapping = {'1.0':'fail_child.refused.to.take',
           '2.0':'fail_parents.refused.to.feed',
           '3.0':'fail_child.or.parents.not.at.home',
           '4.0':'fail_child.vomiting',
           '5.0':'fail_child.is.sick',
           '6.0':'fail_other',
           'nan':'fail_no.failure'}
fail = b.rename(columns=mapping)

# Concatenate all dataframes
surveillance = pd.concat([days_of_catchup, base_body_temp, avs, comp, fail], axis=1)

# Save result
surveillance.to_csv('../results/surveillance.tsv', sep='\t')
