#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Theo Portlock
'''
import os

import pandas as pd

df = pd.read_excel(os.path.join(os.environ["DATA"], '03._Bangladesh_Breast_Feeding_periods_16-Nov-2023.xlsx'), sheet_name='Sheet1', index_col=0)
df.index = 'LCC' + df.index.astype(str) 
df['BF'] = df['Duration of Exclusive Breast Feeding (Month.Day)']
df['PoB'] = df['H/O Place of birth (1=Home, 2 = Health Facility)'].map({1:'Home', 2:'Clinic'})
df = df[['BF','PoB']]
df.index.name = 'subjectID'

df.to_csv(os.path.join(os.environ["WORK"], 'cleaned/bfpob.tsv'), sep='\t')
