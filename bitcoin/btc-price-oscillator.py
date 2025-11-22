import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
from scipy import stats


# Data ETL

client = CoinMetricsClient()
df_btc_data = client.get_asset_metrics(assets='BTC', metrics=['PriceUSD', 'BlkCnt']).to_dataframe()
df_btc_data['time'] = df_btc_data['time'].dt.tz_localize(None)
df_btc_data['BlkHgt'] = df_btc_data['BlkCnt'].astype(int).cumsum()
df_btc_data = df_btc_data[df_btc_data['time'] >= "2010-07-18"]


a, b, r, p, std_err = stats.linregress(np.log(df_btc_data['BlkHgt']), np.log(df_btc_data['PriceUSD']))

df_price_fit = np.exp(a * np.log(df_btc_data['BlkHgt']) + b)

print(r ** 2)

# Plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.1, right=0.98, top=0.955, bottom=0.07)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')

mng = plt.get_current_fig_manager()
mng.window.showMaximized()

plt.axvline(dt.datetime(2012, 11, 28), color='black')
plt.axvline(dt.datetime(2016, 7, 9), color='black')
plt.axvline(dt.datetime(2020, 5, 11), color='black')
plt.axvline(dt.datetime(2024, 4, 19), color='black')

plt.hlines(1, df_btc_data['time'].iloc[0], df_btc_data['time'].iloc[-1], color='dimgray', linestyles='dashed')

ax.semilogy(df_btc_data['time'], (df_btc_data['PriceUSD'] / df_price_fit))

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator())
#ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))

plt.title('BTC price - oscillator')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.ylim(0.1, 100)
plt.xlim(df_btc_data['time'].iloc[0], df_btc_data['time'].iloc[-1])
plt.show()