import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
import scipy.stats as stats

# Helper functions
def CurrencyFormatter(x, pos):
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


df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc['time'] = pd.to_datetime(df_btc['time']).dt.tz_localize(None)
df_btc['PriceUSD'] = pd.to_numeric(df_btc['PriceUSD'])
df_btc['Mean'] = df_btc['PriceUSD'].expanding().mean()
df_btc['Median'] = df_btc['PriceUSD'].expanding().median()
df_btc['Mean Ratio'] = df_btc['PriceUSD'] / df_btc['Mean']
df_btc['Median Ratio'] = df_btc['PriceUSD'] / df_btc['Median']

print(df_btc)

# Plotting 
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)

df_btc_price_early = df_btc[df_btc['time'] < '2010-07-18']

ax.plot(df_btc['time'], df_btc['Mean Ratio'], label='Mean Ratio')
ax.plot(df_btc['time'], df_btc['Median Ratio'], label='Median Ratio')


#ax.yaxis.set_major_locator(ticker.LogLocator(numticks=12))
#ax.yaxis.set_minor_locator(ticker.LogLocator(numticks=500, subs=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)))
#ax.yaxis.set_major_formatter(CurrencyFormatter)

#ax.set_xlim(dr_forecast[0], dr_forecast[-1])
#ax.set_ylim(1e-2, 1e6)
ax.grid(axis='both', which='major', alpha=0.5, zorder=1)
ax.grid(axis='y', which='minor', alpha=0.25, zorder=1)
ax.legend(title='Legend')
plt.show()