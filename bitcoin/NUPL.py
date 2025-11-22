import pandas as pd
from matplotlib.ticker import FuncFormatter
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset
from scipy.stats import linregress


def inv_exp_decay(x, a, b, c):
    return a * (1 - np.exp(b * -x)) + c

# Data ETL

client = CoinMetricsClient()
df_btc = client.get_asset_metrics(assets='BTC', metrics=['CapMrktCurUSD', 'CapRealUSD'], page_size=10000).to_dataframe()
print(df_btc)
df_btc.dropna(inplace=True)
df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['NUPL'] = (df_btc['CapMrktCurUSD'] - df_btc['CapRealUSD']) / df_btc['CapMrktCurUSD']


# Regression

df_peaks = df_btc[df_btc['time'].isin([
    '2010-11-06',
    '2011-06-04',
    '2013-11-18',
    '2017-12-07',
    '2021-02-21'
])]

a, b, _, _, _ = linregress(df_peaks.index, df_peaks['NUPL'])
peak_fit = a * df_btc.index + b
resid = df_peaks['NUPL'] - (a * df_peaks.index + b)

peaks_sup = np.percentile(resid, 0)
peaks_res = np.percentile(resid, 100)


df_troughs = df_btc[df_btc['time'].isin([
    '2011-10-19',
    '2015-01-14',
    '2018-12-15',
    '2022-11-09'
])]

popt, _ = curve_fit(inv_exp_decay, df_troughs.index, df_troughs['NUPL'], p0=[3, 0.0008, -3.25])
trough_fit = inv_exp_decay(df_btc.index, *popt)
resid = df_troughs['NUPL'] - inv_exp_decay(df_troughs.index, *popt)

troughs_sup = np.percentile(resid, 0)
troughs_res = np.percentile(resid, 100)

# Plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)

ax.plot(df_btc['time'], df_btc['NUPL'], zorder=3, label='BTC - NUPL')
#ax.plot(df_btc['time'], fit, zorder=3, label='Linear fit')
ax.fill_between(df_btc['time'], peak_fit + peaks_sup, peak_fit + peaks_res, color='tab:red', alpha=0.5)
ax.fill_between(df_btc['time'], trough_fit + troughs_sup, trough_fit + troughs_res, color='tab:green', alpha=0.5)


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator())
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}'.rstrip('0').rstrip('.')))

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y:,.3f}')

#plt.xlim(df_btc['date'].iloc[0], dt_forecast[-1])
plt.ylim(-2, 1)
plt.grid(axis='both', which='major', alpha=0.5, zorder=1)
plt.grid(axis='both', which='minor', alpha=0.25, zorder=1)
plt.legend(title='Legend')
plt.show()