#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Theo Portlock
For project setup
'''
import metatoolkit.functions as f
import numpy as np
import pandas as pd

#anthro1 = pd.read_excel('../data/06. LEAP_Child_anthropometry_for_1_Yrs_MAM (Baseline to ATP 3.02) on 01-Jan-2024 2.xlsx', index_col=0)
anthro1 = pd.read_excel('../data/06. LEAP_Child_anthropometry_for_1_Yrs_MAM (Baseline to ATP 3.04) on 26-May-2024.xlsx', index_col=0)
names1 = {1.00: 0,
          2.01: 1,
          2.02: 2,
          2.03: 3,
          2.04: 4,
          2.05: 5,
          2.06: 6,
          2.07: 7,
          2.08: 8,
          2.09: 9,
          2.10: 10,
          2.11: 11,
          2.12: 12,
          2.13: 13,
          3.01: 14,
          3.02: 28,
          3.03: 40,
          3.04: 52,
          3.05: 64,
          3.06: 76,
          3.07: 88}

anthro2 = pd.read_excel('../data/07. LEAP_Child_Anthropometry_for_1_Yrs_Normal (Baseline to ATP 3.04) on 01-Jan-2024 2.xlsx', index_col=0)
names2 = {1.00: 0,
          2.00: 4,
          2.01: 8,
          2.02: 12, 
          3.01: 14,
          3.02: 28,
          3.03: 40,
          3.04: 52,
          3.05: 64,
          3.06: 76,
          3.07: 88}

anthro1.An_Time = anthro1.An_Time.replace(names1)
anthro2.An_Time = anthro2.An_Time.replace(names2)
anthro = pd.concat([anthro1, anthro2])
anthro.loc[anthro.Weight == 99.99, 'Weight'] = np.nan
anthro.loc[anthro.Length == 99.9, 'Length'] = np.nan
anthro.loc[anthro.MUAC == 99.9, 'MUAC'] = np.nan
anthro.loc[anthro.HC == 99.9, 'HC'] = np.nan
anthro.loc[anthro.HC == 99.0, 'HC'] = np.nan
anthro.loc[anthro.WLZ_WHZ == 99.99, 'WLZ_WHZ'] = np.nan
anthro.loc[anthro.WLZ_WHZ == 99.9, 'WLZ_WHZ'] = np.nan
anthro.index = anthro.index.astype(str) + anthro.An_Time.astype(int).astype(str).str.pad(width=3, side='left', fillchar='0')
anthro.drop(['An_Time', 'SEX', 'DOB', 'DOM', 'Missed', 'Group', 'Remarks'], axis=1, inplace=True)
anthro.index = 'LCC' + anthro.index.astype(str)

idcol, timecol = anthro.index.str[:7], anthro.index.str[8:].astype(int)
anthro.insert(0, 'timepoint',timecol)
anthro.insert(0, 'subjectID',idcol)
anthro = anthro.set_index(['subjectID', 'timepoint'])

f.save(anthro, 'anthro')
