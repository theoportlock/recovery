#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

psd = pd.read_csv("../data/DhakaBangladeshLEAPE-EEGProcessedVariable_DATA_LABELS_2024-07-18_2304.csv", index_col=0).iloc[:,:-1]

psd.index = psd.index + psd['Event Name'].replace(
        {'12_month (Arm 2: Intervention)':'000',
         '12_month  (Arm 1: Control)':'000',
         '24_month (Arm 1: Control)':'052',
         '24_month (Arm 2: Intervention)':'052',
         '36_month (Arm 3: Outcome Reference)':'104'})

psd = psd.iloc[:,2:]

f.save(psd, 'psd')
