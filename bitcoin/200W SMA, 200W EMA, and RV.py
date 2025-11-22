import sys
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient


# Helper functions

def PriceFormatter(x, pos):
    if x >= 1e6:
        return '${:,.0f}M'.format(x / 1e6)
    elif x >= 1e3:
        return '${:,.0f}k'.format(x / 1e3)
    elif x >= 1:
        return '${:,.0f}'.format(x)
    elif x >= 1e-2:
        return '{:,.0f}¢'.format(x * 100)
    elif x >= 1e-3:
        return '{:,.1f}¢'.format(x * 100)
    else:
        return '{:,.2f}¢'.format(x * 100)
    

# Data ETL

df_btc_price_early = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTC_Price_Pre_2010_07_18.csv')
df_btc_price_early['time'] = pd.to_datetime(df_btc_price_early['time'])
df_btc_price_early = (df_btc_price_early.set_index('time')
    .reindex(pd.date_range(df_btc_price_early['time'].iloc[0], df_btc_price_early['time'].iloc[-1], freq='D'))
    .rename_axis(['time'])
    .reset_index())
df_btc_price_early['PriceUSD'] = df_btc_price_early['PriceUSD'].interpolate(method='akima')

client = CoinMetricsClient()

df_btc_price = client.get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc_price['time'] = df_btc_price['time'].dt.tz_localize(None)
df_btc_price = df_btc_price.drop(columns=['asset'])

df_btc_price = pd.concat([df_btc_price_early, df_btc_price])
df_btc_price['PriceUSD'] = df_btc_price['PriceUSD'].astype(float)
df_btc_price['timeOrdinal'] = df_btc_price['time'].apply(lambda x: x.toordinal())

df_btc_price['sma_200w'] = df_btc_price['PriceUSD'].rolling(1400, 1).mean()
df_btc_price['ema_200w'] = df_btc_price['PriceUSD'].ewm(span=1400, adjust=False).mean()

df_btc_price_real = client.get_asset_metrics(assets='BTC', metrics=['CapMrktCurUSD', 'CapMVRVCur', 'SplyCur'], page_size=10000).to_dataframe()
df_btc_price_real['time'] = df_btc_price_real['time'].dt.tz_localize(None)
df_btc_price_real['CapRealUSD'] = df_btc_price_real['CapMrktCurUSD'] / df_btc_price_real['CapMVRVCur']
df_btc_price_real['CapRealUSD'] = pd.to_numeric(df_btc_price_real['CapRealUSD'], errors='coerce')
df_btc_price_real['SplyCur'] = pd.to_numeric(df_btc_price_real['SplyCur'], errors='coerce')


# Plotting

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)
ax.grid(axis='both', which='major', color='silver', zorder=1)
ax.grid(axis='both', which='minor', color='gainsboro', zorder=1)
plt.tick_params(axis='y',which='minor')

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)


ax.semilogy(df_btc_price['time'], np.array(df_btc_price['PriceUSD']), label='BTC - Closing Price in USD', zorder=4)
ax.semilogy(df_btc_price['time'], np.array(df_btc_price['sma_200w']), label='200 week SMA', zorder=4)
ax.semilogy(df_btc_price['time'], np.array(df_btc_price['ema_200w']), label='200 week EMA', zorder=4)
ax.semilogy(df_btc_price_real['time'], np.array(df_btc_price_real['CapRealUSD'] / df_btc_price_real['SplyCur']), label='Realized Price', zorder=4)


# 2011-06-08
peak_2011 = df_btc_price[df_btc_price['time'] == '2011-06-08']
peak_2013 = df_btc_price[df_btc_price['time'] == '2013-12-04']
peak_2017 = df_btc_price[df_btc_price['time'] == '2017-12-16']
peak_2021 = df_btc_price[df_btc_price['time'] == '2021-11-08']


ax.plot(
    [peak_2011['time'].iloc[0], peak_2013['time'].iloc[0]], 
    [peak_2011['PriceUSD'].iloc[0], peak_2011['PriceUSD'].iloc[0]],
    color='black',
    linestyle='dashed',
    zorder=5
)

ax.plot(
    [peak_2013['time'].iloc[0], peak_2013['time'].iloc[0]], 
    [peak_2011['PriceUSD'].iloc[0], peak_2013['PriceUSD'].iloc[0]],
    color='black',
    linestyle='dashed',
    zorder=5
)

ax.plot(
    [peak_2013['time'].iloc[0], peak_2017['time'].iloc[0]], 
    [peak_2013['PriceUSD'].iloc[0], peak_2013['PriceUSD'].iloc[0]],
    color='black',
    linestyle='dashed',
    zorder=5
)

ax.plot(
    [peak_2017['time'].iloc[0], peak_2017['time'].iloc[0]], 
    [peak_2013['PriceUSD'].iloc[0], peak_2017['PriceUSD'].iloc[0]],
    color='black',
    linestyle='dashed',
    zorder=5
)

ax.plot(
    [peak_2017['time'].iloc[0], peak_2021['time'].iloc[0]], 
    [peak_2017['PriceUSD'].iloc[0], peak_2017['PriceUSD'].iloc[0]],
    color='black',
    linestyle='dashed',
    zorder=5
)

ax.plot(
    [peak_2021['time'].iloc[0], peak_2021['time'].iloc[0]], 
    [peak_2017['PriceUSD'].iloc[0], peak_2021['PriceUSD'].iloc[0]],
    color='black',
    linestyle='dashed',
    zorder=5
)

ax.plot(
    [peak_2021['time'].iloc[0], dt.datetime(2026, 12, 31)], 
    [peak_2021['PriceUSD'].iloc[0], peak_2021['PriceUSD'].iloc[0]],
    color='black',
    linestyle='dashed',
    zorder=5
)

ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator(numticks=500))
ax.yaxis.set_major_formatter(PriceFormatter)

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y=${y:,.2f}')

plt.xlim(df_btc_price['time'].iloc[0], dt.datetime(2027, 1, 1))
plt.ylim(1e-4, 1e6)
plt.legend(title='Legend')
plt.show()