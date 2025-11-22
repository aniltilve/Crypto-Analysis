import pandas as pd
import numpy as np
from matplotlib import(
    pyplot as plt,
    ticker as ticker,
)
from scipy.optimize import curve_fit

def exp_decay(x, a, b, c):
    return a * np.exp(x * b) + c

df_btc = pd.read_csv('./Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time'])

df_highs = df_btc[df_btc['time'].isin([
    '2013-11-29',
    '2017-12-17',
    '2021-11-10'
])].reset_index(drop=True)

df_lows = df_btc[df_btc['time'].isin([
    '2011-11-17',
    '2015-08-18',
    '2018-12-15'
])].reset_index(drop=True)

date_diffs = (df_highs['time'] - df_lows['time']).dt.days
pct_incr = (df_highs['high'] - df_lows['low']) / df_lows['low']

print(date_diffs)

popt, _ = curve_fit(exp_decay, date_diffs - date_diffs[0], pct_incr, p0=[600, -0.001, 0], maxfev=10000)
print(popt)

idx_fit = np.arange(1000)
fit = exp_decay(idx_fit, *popt)

cur_low = df_btc[df_btc['time'].isin(['2022-11-21'])].reset_index()
cur_high = df_btc[df_btc['high'] == df_btc['high'].max()].reset_index()

cur_date_diff = (cur_high['time'] - cur_low['time']).dt.days
cur_pct_incr = (cur_high['high'] - cur_low['low']) / cur_low['low']

print(cur_low)

fig, ax = plt.subplots()

ax.scatter(date_diffs, pct_incr)
ax.scatter(cur_date_diff, cur_pct_incr)
ax.plot(idx_fit + date_diffs[0], fit)

ax.yaxis.set_major_formatter(ticker.PercentFormatter(1))

plt.ylim(0)

plt.show()