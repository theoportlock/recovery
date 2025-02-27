#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

bayley = pd.read_csv('../data/DhakaBangladeshLEAPE-BayleyCompletes_DATA_LABELS_2024-07-18_2237.csv', index_col=0)

bayley.index = bayley.index + bayley['Event Name'].replace(
        {'12_month (Arm 2: Intervention)':'000',
         '12_month  (Arm 1: Control)':'000',
         '24_month (Arm 1: Control)':'052',
         '24_month (Arm 2: Intervention)':'052',
         '36_month (Arm 3: Outcome Reference)':'104'})
bayley = bayley.loc[:,bayley.columns.str.contains('Raw')]
bayley.columns = bayley.columns.str.replace(' Raw','')
bayley = bayley.astype(float)
bayley = bayley.dropna()
bayley = bayley.astype(int)

idcol, timecol = bayley.index.str[:7], bayley.index.str[8:].astype(int)
bayley.insert(0, 'timepoint',timecol)
bayley.insert(0, 'subjectID',idcol)
bayley = bayley.set_index(['subjectID', 'timepoint'])

f.save(bayley, 'bayley')
