from coinmetrics.api_client import CoinMetricsClient
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.special import inv_boxcox
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter


def exp_decay(x, a, b, c):
    return a * np.exp(x * b) + c

# Data ETL
df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc['time'] = pd.to_datetime(df_btc['time']).dt.tz_localize(None)
df_btc = df_btc.drop(columns=['asset'])

df_btc['Monthly Returns'] = df_btc['PriceUSD'].pct_change(90)


df_peaks = df_btc[df_btc['time'].isin([
    '2011-05-13',
    '2013-11-29',
    '2017-12-12',
    '2021-01-09'
])]

#popt, _ = curve_fit(exp_decay, df_peaks.index, df_peaks['Monthly Returns'], p0=[5, -0.001, 1])

#fit = exp_decay(df_btc.index, *popt)

# Plotting 
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.043, right=0.98, top=0.98, bottom=0.04)
ax.grid(axis='both', which='major', color='silver', zorder=1)
ax.grid(axis='both', which='minor', color='gainsboro', zorder=1)


ax.plot(df_btc['time'], df_btc['Monthly Returns'], zorder=4, label='Monthly Returns')
#ax.plot(df_btc['time'], fit, zorder=4, label='Fit')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y*100:,.2f}%')

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
plt.show()