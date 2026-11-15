#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Theo Portlock
'''
import os

import pandas as pd

df = pd.read_excel(os.path.join(os.environ["DATA"], '04._Bangladesh_baby_delivery_mode_and_supplements_during_pregnancy.xlsx'), sheet_name='Mother Enrollment', index_col=0)
df.index = 'LCC' + df.index.astype(str)
df['Delivery_Mode'] = df['Mode'].map({1:'Vaginal',2:'Caesarean'})
df['Supplementation'] = df['Supple'].map({1:True,2:False})
df = df[['Delivery_Mode','Supplementation']]

df.index.name = 'subjectID'

df.to_csv(os.path.join(os.environ["WORK"], 'cleaned/deliverysupp.tsv'), sep='\t')
