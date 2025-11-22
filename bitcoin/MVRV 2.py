import pandas as pd
from matplotlib.ticker import FuncFormatter
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset


# Get data from Coinmetrics, calculate MVRV, and generate time ordinal

df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics='CapMVRVCur', page_size=10000).to_dataframe()
df_btc.dropna(inplace=True)

df_btc['time'] = df_btc['time'].dt.tz_localize(None)

mvrv_gt_1 = df_btc[df_btc['CapMVRVCur'] > 1]
mvrv_gt_1 = (mvrv_gt_1.set_index('time')
    .reindex(pd.date_range(mvrv_gt_1['time'].iloc[0], mvrv_gt_1['time'].iloc[-1], freq='D'))
    .rename_axis(['time'])
    .reset_index())


mvrv_lt_1 = df_btc[df_btc['CapMVRVCur'] < 1]
mvrv_lt_1 = (mvrv_lt_1.set_index('time')
    .reindex(pd.date_range(mvrv_lt_1['time'].iloc[0], mvrv_lt_1['time'].iloc[-1], freq='D'))
    .rename_axis(['time'])
    .reset_index())

#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.03, right=0.98, top=0.98, bottom=0.04)

ax.semilogy(df_btc['time'], df_btc['CapMVRVCur'], color='black', zorder=3, linewidth=1, label='BTC - MVRV')
ax.fill_between(mvrv_gt_1['time'], 1, mvrv_gt_1['CapMVRVCur'], color='tab:green', alpha=0.5)
ax.fill_between(mvrv_lt_1['time'], mvrv_lt_1['CapMVRVCur'], 1, color='tab:red', alpha=0.5)


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator())
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
ax.yaxis.set_minor_formatter(ticker.StrMethodFormatter('{x:g}'))


ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y:,.3f}')

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
plt.ylim(0.3, 9)
plt.grid(axis='both', which='major', alpha=0.5, zorder=1)
plt.grid(axis='both', which='minor', alpha=0.25, zorder=1)
plt.legend(title='Legend')
plt.show()