import math
import pandas as pd
import numpy as np
from matplotlib import (
    dates as mdates,
    pyplot as plt
)
import datetime as dt
from scipy.stats import linregress

df_btc = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time'])
df_btc['index'] = (df_btc['time'] - df_btc['time'].iloc[0]).dt.days
df_btc['log10 high'] = np.log10(df_btc['high'])

df_peaks = df_btc[df_btc['time'].isin([
    '2011-06-08',
    '2013-11-29',
    '2013-12-04',
    '2013-12-05',
    '2017-12-16',
    '2017-12-17',
    '2021-04-14',
    '2021-10-20',
    '2021-11-10'
    #'2025-08-14'
])]

highest_r2 = 0
best_offset = 0
a_0 = 0
b_0 = 0

for offset in np.arange(0.01, 1000, 0.01):
    a, b, r, _, _ = linregress(np.log10(df_peaks['index'] + offset), df_peaks['log10 high'])

    if r ** 2 > highest_r2:
        highest_r2 = r ** 2
        best_offset = offset
        a_0, b_0 = a, b
        print(f'Offset: {offset}    Highest R2: {highest_r2}')


fit = 10 ** (a_0 * np.log10(df_btc['index'] + best_offset) + b_0)

plt.semilogy(df_btc['time'], df_btc['high'], alpha=0.4)
plt.semilogy(df_btc['time'], fit)
plt.ylim(1e-2)
plt.show()