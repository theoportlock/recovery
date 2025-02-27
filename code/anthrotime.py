#!/usr/bin/env python
import metatoolkit.functions as f
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

meta = f.load('meta')
anthro = f.load('anthro')
timemeta = f.load('meta')

anthro['ID'] = anthro.index.str[:7]
anthro['Weeks'] = anthro.index.str[7:].astype(float)
#df = anthro.set_index('ID').join(timemeta.set_index('ID'))
df = anthro.set_index('ID').join(timemeta)

x='Weeks'
#var = 'Weight'
y = 'WLZ_WHZ'
#var = 'Length'
#var = 'MUAC'
#metavar = 'Place of birth'
hue = 'Recovery'
#metavar = 'Delivery Mode'

def line(df, x, y, hue):
    fig, ax= plt.subplots(figsize=(6,6))
    #sns.lineplot(data=df.reset_index(), x=x, y=y, hue=metavar, err_style="bars", ax=ax)
    #sns.lineplot(data=df.reset_index(), x=x, y=y, estimator=None, units='ID', ax=ax, hue='Recovery', alpha=0.2, )
    sns.lineplot(data=df.reset_index(), x=x, y=y, estimator=None, units='ID', ax=ax, hue='Recovery', alpha=0.8)
    sns.pointplot(data=df.reset_index(), x=x, y=y, ax=ax, hue=hue)
    f.savefig(f'{y}{hue}line')
line(df.query('Weeks <= 12'), 'Weeks', 'WLZ_WHZ', 'Recovery')
line(df.query('Weeks <= 12'), 'Weeks', 'Length', 'Recovery')
line(df.query('Weeks <= 12'), 'Weeks', 'Weight', 'Recovery')

#x='Length'
#y='Weight'
#hue='Recovery'

#sns.lineplot(data=df.query('Weeks <= 12').reset_index(), x=x, y=y, hue=hue, estimator=None, units='ID')
