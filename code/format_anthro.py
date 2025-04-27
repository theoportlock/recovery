#!/usr/bin/env python

import numpy as np
import pandas as pd

def an_time_mapping(tdf):
    # Convert 'DOM' column to datetime if it isn't already
    df = tdf.copy()
    df['DOM'] = pd.to_datetime(df['DOM'], errors='coerce')

    # Calculate baseline date (DOB + 12 months)
    baseline_date = df['DOB'] + pd.DateOffset(months=12)

    # Calculate number of days between DOM and baseline
    days_since_baseline = (df['DOM'] - baseline_date).dt.days

    # Convert days to weeks (floating point)
    weeks_since_baseline = days_since_baseline / 7

    # Add to the dataframe
    df['Weeks_since_baseline'] = weeks_since_baseline

    # Sort by weeks since baseline
    df.sort_values('Weeks_since_baseline', inplace=True)

    # Calculate the difference of weeks for each ID (SID_LCC)
    # The first diff value for each group should be NaN, the rest will be the differences
    df['diffweeks'] = df.groupby('SID_LCC')['Weeks_since_baseline'].diff()

    # Fix the issue by using transform to keep the index aligned
    df['diffweeks'] = df.groupby('SID_LCC')['diffweeks'].transform(lambda x: x.fillna(np.nan))

    # Optional: If you want to calculate the cumulative sum of 'diffweeks' for each SID_LCC
    df['timepoint'] = df.groupby('SID_LCC')['diffweeks'].cumsum()

    df.sort_values(['SID_LCC', 'An_Time'], inplace=True)

    grouped = df[['Weeks_since_baseline','An_Time','diffweeks','timepoint']].groupby('An_Time').mean()
    grouped['rounded']= grouped['timepoint'].round(0).fillna(0).astype(int)
    return grouped

# Read the data
anthro1 = pd.read_excel('../data/06. LEAP_Child_anthropometry_for_1_Yrs_MAM (Baseline to ATP 3.04) on 26-May-2024.xlsx')
anthro2 = pd.read_excel('../data/07. LEAP_Child_Anthropometry_for_1_Yrs_Normal (Baseline to ATP 3.04) on 01-Jan-2024 2.xlsx')

# Generate mapping
names1 = an_time_mapping(anthro1).rounded.to_dict()
names2 = an_time_mapping(anthro2).rounded.to_dict()

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
anthro.set_index('SID_LCC', inplace=True)
anthro.index = anthro.index.astype(str) + anthro.An_Time.astype(int).astype(str).str.pad(width=3, side='left', fillchar='0')
anthro.drop(['An_Time', 'SEX', 'DOB', 'DOM', 'Missed', 'Group', 'Remarks'], axis=1, inplace=True)
anthro.index = 'LCC' + anthro.index.astype(str)

idcol, timecol = anthro.index.str[:7], anthro.index.str[8:].astype(int)
anthro.insert(0, 'timepoint',timecol)
anthro.insert(0, 'subjectID',idcol)
df = anthro.set_index(['subjectID', 'timepoint'])

mapping = df.index.to_frame()
mapping['sampleID'] = mapping['subjectID'] + '_' + mapping['timepoint'].astype(str)
mapping = mapping[['sampleID', 'subjectID', 'timepoint']]
df.index = mapping['sampleID']

df.to_csv('../results/anthro.tsv', sep='\t', index=True)
