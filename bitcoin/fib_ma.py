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

def fib_sequence(n):
    """Generates a Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [5]
    else:
        list_fib = [5, 8]
        while len(list_fib) < n:
            next_fib = list_fib[-1] + list_fib[-2]
            list_fib.append(next_fib)
        return list_fib

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


fib = fib_sequence(10)
print(fib)

for i in fib:
    col_name = 'sma' + str(i)
    df_btc_price[col_name] = df_btc_price['PriceUSD'].rolling(window=i).mean()




# Plotting

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)
ax.grid(axis='both', which='major', color='silver', zorder=1)
ax.grid(axis='both', which='minor', color='gainsboro', zorder=1)
plt.tick_params(axis='y',which='minor')

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)


ax.semilogy(df_btc_price['time'], np.array(df_btc_price['PriceUSD']), label='BTC - Closing Price in USD', zorder=4)

for i in fib:
    col_name = 'sma' + str(i)
    ax.semilogy(df_btc_price['time'], df_btc_price[col_name], label=i, zorder=4)




ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator(numticks=500))
ax.yaxis.set_major_formatter(PriceFormatter)

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y=${y:,.2f}')

plt.xlim(df_btc_price['time'].iloc[0], dt.datetime(2026, 1, 1))
plt.ylim(1e-4, 1e6)
plt.legend(title='Legend')
plt.show()