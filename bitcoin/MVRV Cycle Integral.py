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

mvrv_gt_1_c1 = df_btc[df_btc['time'].between(df_btc['time'].iloc[0], '2011-09-08')]
mvrv_gt_1_c2 = df_btc[df_btc['time'].between('2012-01-04', '2014-12-16')]
mvrv_gt_1_c3 = df_btc[df_btc['time'].between('2015-10-23', '2018-11-18')]
mvrv_gt_1_c4 = df_btc[df_btc['time'].between('2019-04-02', '2022-06-12')]
mvrv_gt_1_c5 = df_btc[df_btc['time'].between('2023-01-23', '2027-01-01')]


mvrv_gt_1_c1['CapMVRVCur Integral'] = mvrv_gt_1_c1['CapMVRVCur'].cumsum()
mvrv_gt_1_c2['CapMVRVCur Integral'] = mvrv_gt_1_c2['CapMVRVCur'].cumsum()
mvrv_gt_1_c3['CapMVRVCur Integral'] = mvrv_gt_1_c3['CapMVRVCur'].cumsum()
mvrv_gt_1_c4['CapMVRVCur Integral'] = mvrv_gt_1_c4['CapMVRVCur'].cumsum()
mvrv_gt_1_c5['CapMVRVCur Integral'] = mvrv_gt_1_c5['CapMVRVCur'].cumsum()


#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.03, right=0.98, top=0.98, bottom=0.04)

#ax.semilogy(df_btc['time'], df_btc['CapMVRVCur'], color='black', zorder=3, linewidth=1, label='BTC - MVRV')
ax.fill_between(mvrv_gt_1_c1['time'], 1, mvrv_gt_1_c1['CapMVRVCur Integral'], color='tab:green', alpha=0.5)
ax.fill_between(mvrv_gt_1_c2['time'], 1, mvrv_gt_1_c2['CapMVRVCur Integral'], color='tab:green', alpha=0.5)
ax.fill_between(mvrv_gt_1_c3['time'], 1, mvrv_gt_1_c3['CapMVRVCur Integral'], color='tab:green', alpha=0.5)
ax.fill_between(mvrv_gt_1_c4['time'], 1, mvrv_gt_1_c4['CapMVRVCur Integral'], color='tab:green', alpha=0.5)
ax.fill_between(mvrv_gt_1_c5['time'], 1, mvrv_gt_1_c5['CapMVRVCur Integral'], color='tab:green', alpha=0.5)


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

#ax.yaxis.set_major_locator(ticker.LogLocator())
#ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
#ax.yaxis.set_minor_formatter(ticker.StrMethodFormatter('{x:g}'))
ax.set_yscale('log')

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y:,.3f}')

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1] + pd.tseries.offsets.DateOffset(months=1))
plt.ylim(1, 3000)
plt.grid(axis='both', which='major', alpha=0.5, zorder=1)
plt.grid(axis='both', which='minor', alpha=0.25, zorder=1)
plt.legend(title='Legend')
plt.show()