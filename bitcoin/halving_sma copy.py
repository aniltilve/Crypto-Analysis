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
    if x >= 10 ** 6:
        return '${:,.0f}M'.format(x / 1e6)
    elif x >= 10 ** 3:
        return '${:,.0f}k'.format(x / 1e3)
    elif x <= 10 ** - 4:
        return '${:,.4f}'.format(x)
    elif x <= 10 ** -3:
        return '${:,.3f}'.format(x)
    elif x <= 10 ** -2:
        return '${:,.2f}'.format(x)
    elif x <= 10 ** -1:
        return '${:,.1f}'.format(x)
    else:
        return '${:,.0f}'.format(x)
    

# Data ETL

df_btc_price_early = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTC_Price_Pre_2010_07_18.csv')
df_btc_price_early['time'] = pd.to_datetime(df_btc_price_early['time'])
df_btc_price_early = (df_btc_price_early.set_index('time')
    .reindex(pd.date_range(df_btc_price_early['time'].iloc[0], df_btc_price_early['time'].iloc[-1], freq='D'))
    .rename_axis(['time'])
    .reset_index())
df_btc_price_early['PriceUSD'] = df_btc_price_early['PriceUSD'].interpolate(method='akima')

client = CoinMetricsClient()

df_btc_data = client.get_asset_metrics(assets='BTC', metrics=['PriceUSD', 'BlkCnt'], page_size=10000).to_dataframe()
df_btc_data['BlkHgt'] = df_btc_data['BlkCnt'].astype(int).cumsum()
df_btc_data = df_btc_data.drop(columns=['asset'])
df_btc_data.loc[(df_btc_data['time'] >= '2009-10-05') & (df_btc_data['time'] <= '2010-07-17'), 'PriceUSD'] = df_btc_price_early['PriceUSD']
df_btc_data = df_btc_data[df_btc_data['BlkHgt'] > 0]
df_btc_data = df_btc_data.dropna()
df_btc_data = (
    df_btc_data.set_index(df_btc_data['BlkHgt'])
    .reindex(np.arange(df_btc_data['BlkHgt'].iloc[0], df_btc_data['BlkHgt'].iloc[-1], 1))
) 
df_btc_data['PriceUSD'] = df_btc_data['PriceUSD'].ffill()
df_btc_data['sma'] = df_btc_data['PriceUSD'].rolling(window=210000).mean()
print(df_btc_data)
#sys.exit()

# Plotting

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.07, right=0.98, top=0.98, bottom=0.055)
ax.grid(axis='both', which='major', color='silver', zorder=1)
ax.grid(axis='both', which='minor', color='gainsboro', zorder=1)
plt.tick_params(axis='y',which='minor')


ax.semilogy(df_btc_data.index, np.array(df_btc_data['PriceUSD']), label='BTC - Closing Price in USD', zorder=4)
ax.semilogy(df_btc_data.index, df_btc_data['sma'], label='210,000 block SMA', zorder=4)

peak_2011 = df_btc_data[df_btc_data.index == 129691]
peak_2013 = df_btc_data[df_btc_data.index == 273109]
peak_2017 = df_btc_data[df_btc_data.index == 499689]
peak_2021 = df_btc_data[df_btc_data.index == 708845]

ax.plot(
    [peak_2011.index[0], peak_2013.index[0]], 
    [peak_2011['PriceUSD'].iloc[0], peak_2011['PriceUSD'].iloc[0]],
    color='black',
    zorder=5
)

ax.plot(
    [peak_2013.index[0], peak_2013.index[0]], 
    [peak_2011['PriceUSD'].iloc[0], peak_2013['PriceUSD'].iloc[0]],
    color='black',
    zorder=5
)

ax.plot(
    [peak_2013.index[0], peak_2017.index[0]], 
    [peak_2013['PriceUSD'].iloc[0], peak_2013['PriceUSD'].iloc[0]],
    color='black',
    zorder=5
)

ax.plot(
    [peak_2017.index[0], peak_2017.index[0]], 
    [peak_2013['PriceUSD'].iloc[0], peak_2017['PriceUSD'].iloc[0]],
    color='black',
    zorder=5
)

ax.plot(
    [peak_2017.index[0], peak_2021.index[0]], 
    [peak_2017['PriceUSD'].iloc[0], peak_2017['PriceUSD'].iloc[0]],
    color='black',
    zorder=5
)

ax.plot(
    [peak_2021.index[0], peak_2021.index[0]], 
    [peak_2017['PriceUSD'].iloc[0], peak_2021['PriceUSD'].iloc[0]],
    color='black',
    zorder=5
)

ax.plot(
    [peak_2021.index[0], 1.05e6], 
    [peak_2021['PriceUSD'].iloc[0], peak_2021['PriceUSD'].iloc[0]],
    color='black',
    zorder=5
)

ax.xaxis.set_major_locator(ticker.MultipleLocator(2.1e5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(2.1e4))
#ax.xaxis.set_major_formatter(ticker.M('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator(numticks=500))
ax.yaxis.set_major_formatter(PriceFormatter)

ax.format_coord = (lambda x, y: f'x={x:,.0f}, y=${y:,.2f}')

plt.xlabel('BTC - Block Height (\'000s)')
plt.ylabel('BTC - Closing Price in USD')
plt.xlim(0, 1.05e6)
plt.ylim(1e-4, 1e6)
plt.legend(title='Legend')
plt.show()