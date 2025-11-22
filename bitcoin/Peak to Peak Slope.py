import math
import pandas as pd
import numpy as np
from matplotlib import (
    dates as mdates,
    pyplot as plt
)
import datetime as dt

df_btc = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time'])
df_btc['time ordinal'] = ((df_btc['time'] - dt.datetime(2009, 1, 3)).dt.days) / 365
df_btc['log10 high'] = np.log10(df_btc['high'])

df_peaks = df_btc[df_btc['time'].isin([
    '2009-10-09',
    '2011-06-08',
    '2013-11-29',
    '2017-12-17',
    '2021-04-14',
    '2025-08-14'
])]

df_peaks['slope'] = df_peaks['log10 high'].diff() / df_peaks['time ordinal'].diff()

print(df_peaks)

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)

ax.semilogy(df_btc['time'], df_btc['high'])
ax.semilogy(df_peaks['time'], df_peaks['high'], color='black')

plt.annotate(
    f'{df_peaks['slope'].iloc[1]:.2f}', 
    (mdates.date2num(df_peaks['time'].iloc[0]), df_peaks['high'].iloc[0]),
    (mdates.date2num(df_peaks['time'].iloc[0]), df_peaks['high'].iloc[0] + 0.1),
    color='red'
)

plt.show()