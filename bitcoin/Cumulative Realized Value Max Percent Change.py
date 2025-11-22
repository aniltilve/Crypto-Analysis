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

df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['CapMVRVCur', 'CapMrktCurUSD'], page_size=10000).to_dataframe()
df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['CapRealUSD'] = df_btc['CapMrktCurUSD'] / df_btc['CapMVRVCur']
df_btc['CapRealUSD CumMax PctChange'] = df_btc['CapRealUSD'].cummax().pct_change()
df_btc = df_btc[df_btc['CapRealUSD CumMax PctChange'] != 0]
print(df_btc)


#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.03, right=0.98, top=0.98, bottom=0.04)

ax.scatter(df_btc['time'], df_btc['CapRealUSD CumMax PctChange'], color='black', zorder=3, label='BTC - MVRV')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))
ax.yaxis.set_major_formatter(ticker.PercentFormatter(1))


ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y*100:,.3f}%')

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
plt.ylim(0, 1.25)
plt.grid(axis='both', which='major', alpha=0.5, zorder=1)
plt.grid(axis='both', which='minor', alpha=0.25, zorder=1)
plt.legend(title='Legend')
plt.show()