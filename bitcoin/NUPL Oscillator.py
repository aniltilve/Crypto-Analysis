import pandas as pd
from matplotlib.ticker import FuncFormatter
from matplotlib.collections import LineCollection
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
peaks_res = peak_fit + np.percentile(resid, 100)


df_troughs = df_btc[df_btc['time'].isin([
    '2011-10-19',
    '2015-01-14',
    '2018-12-15',
    '2022-11-09'
])]

popt, _ = curve_fit(inv_exp_decay, df_troughs.index, df_troughs['NUPL'], p0=[3, 0.0008, -3.25])
trough_fit = inv_exp_decay(df_btc.index, *popt)
resid = df_troughs['NUPL'] - inv_exp_decay(df_troughs.index, *popt)
troughs_sup = trough_fit + np.percentile(resid, 0)

df_btc['NUPL Norm'] = (df_btc['NUPL'] - troughs_sup) / (peaks_res - troughs_sup)

df_btc = (df_btc.set_index('time')
    .reindex(pd.date_range(df_btc['time'].iloc[0], df_btc['time'].iloc[-1], freq='H'))
    .rename_axis(['time'])
    .reset_index())
df_btc['NUPL Norm'] = df_btc['NUPL Norm'].interpolate(method='linear')

df_btc = df_btc[df_btc['NUPL Norm'] <= 1]

# Plotting
plt.style.use('dark_background')
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)

points = np.array([mdates.date2num(df_btc['time']), df_btc['NUPL Norm']]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

lc = LineCollection(segments, cmap='RdYlGn_r', norm=plt.Normalize(df_btc['NUPL Norm'].min(), df_btc['NUPL Norm'].max()))
lc.set_array(df_btc['NUPL Norm'])
lc.set_linewidth(1.5)

ax.add_collection(lc)

ax.scatter(
    df_btc['time'].iloc[-1], 
    df_btc['NUPL Norm'].iloc[-1],
    c=df_btc['NUPL Norm'].iloc[-1],
    s=100,
    cmap='RdYlGn_r',
    norm=plt.Normalize(df_btc['NUPL Norm'].min(), df_btc['NUPL Norm'].max()),
    zorder=4,
    linewidths=4,
    edgecolors=[
        (1, 1, 1, 0.6),
        (1, 1, 1, 0.9)
    ]
)

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y:,.3f}')

start_dt_offset = pd.tseries.offsets.DateOffset(weeks=1)
end_dt_offset = pd.tseries.offsets.DateOffset(months=1)


plt.xlim(df_btc['time'].iloc[0] - start_dt_offset, df_btc['time'].iloc[-1] + end_dt_offset)
plt.ylim(0, 1)
plt.grid(axis='both', which='major', alpha=0.5, zorder=1)
plt.grid(axis='both', which='minor', alpha=0.25, zorder=1)
plt.legend(title='Legend')
plt.show()