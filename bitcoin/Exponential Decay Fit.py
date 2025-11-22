import math
import pandas as pd
import numpy as np
from matplotlib import (
    dates as mdates,
    pyplot as plt
)
import datetime as dt
from scipy.optimize import curve_fit


def exp_decay(t, a, b, c):
    return a * (1 - np.exp(b * t)) + c

df_btc = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time'])
df_btc['time ordinal'] = (df_btc['time'] - dt.datetime(2009, 1, 3)).dt.days
df_btc['log10 low'] = np.log10(df_btc['low'])
df_btc['log10 high'] = np.log10(df_btc['high'])

df_peaks = df_btc[df_btc['time'].isin([
    '2011-06-08',
    '2013-11-29',
    '2017-12-17',
    '2021-04-14',
    '2021-11-10',
    '2025-07-14',
    '2025-08-14',
    '2025-10-06'
])]

df_troughs = df_btc[df_btc['time'].isin([
    '2010-01-15',
    '2010-10-08',

    '2011-04-04',
    '2011-11-19',

    '2013-01-05',

    '2015-08-18',

    '2017-04-15',

    '2018-12-15',

    '2020-03-13',
    '2020-10-08',
    '2022-11-21',
    '2023-01-11'
])]

print(df_peaks)


popt_peaks, _ = curve_fit(
    exp_decay, 
    df_peaks['time ordinal'],
    df_peaks['log10 high'], 
    p0=[1, -0.000001, -6]
)

popt_troughs, _ = curve_fit(
    exp_decay, 
    df_troughs['time ordinal'],
    df_troughs['log10 low'], 
    p0=[1, -0.000001, -6],
    maxfev=1000000
)

print(popt_peaks)

dr_time_fit = pd.date_range('2009-01-03', '2030-01-01')
time_ordinal_fit = np.arange(len(dr_time_fit))
fit_peaks = np.power(10, exp_decay(time_ordinal_fit, *popt_peaks))
fit_troughs = np.power(10, exp_decay(time_ordinal_fit, *popt_troughs))

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)

ax.semilogy(df_btc['time'], df_btc['high'], color='tab:green')
ax.semilogy(df_btc['time'], df_btc['low'], color='tab:red')

ax.scatter(df_troughs['time'], df_troughs['low'], color='tab:red')

ax.semilogy(dr_time_fit, fit_peaks, color='tab:green', linestyle='dashed')
ax.semilogy(dr_time_fit, fit_troughs, color='tab:red', linestyle='dashed')

plt.show()