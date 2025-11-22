import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
import scipy.stats as stats
import statsmodels.api as sm
from scipy.optimize import curve_fit

def exp_decay(x, a, b, c):
    return a * np.exp(x * b) + c

df_btc = pd.read_csv('./Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time'])

lows = df_btc[df_btc['time'].isin([
    '2009-12-17',
    '2011-11-17',
    '2015-08-18',
    '2018-12-15',
    '2022-11-21'
])].reset_index(drop=True)

highs = df_btc[df_btc['time'].isin([
    '2011-06-08',
    '2013-11-29',
    '2017-12-17',
    '2021-11-10',
    '2025-10-06'
])].reset_index()

print(lows)
print(highs)

pcts = (highs['high'] - lows['low']) / lows['low']
ratios = highs['high'] / lows['low']

print(pcts)
print(ratios)

# popt, _ = curve_fit(exp_decay, highs['index'], ratios)

# idx_fit = np.linspace(0, 6000, 6000)
# fit = exp_decay(idx_fit, *popt)

fig, ax = plt.subplots()
#ax.semilogy(df_btc['time'], df_btc['low'], color='tab:red')
#ax.semilogy(df_btc['time'], df_btc['high'], color='tab:green')
#ax.scatter(highs['index'], ratios)
ax.semilogy(highs['index'], ratios, color='tab:orange')
#ax.plot(idx_fit, fit)
#plt.ylim(0)
plt.show()