import sys
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient

def PercentileFormatter(x, pos):
    x *= 100
    if (x >= 1):
        return '{:.0f}%'.format(x)
    elif (x >= 0.1):
        return '{:.1f}%'.format(x)
    elif (x >= 0.01):
        return '{:.2f}%'.format(x)
    elif (x >= 0.001):
        return '{:.3f}%'.format(x)
    elif (x >= 0.0001):
        return '{:.4f}%'.format(x)
    elif (x >= 0.00001):
        return '{:.5f}%'.format(x)

# Data ETL

client = CoinMetricsClient()

df_doge_adr_bal = client.get_asset_metrics(assets='BTC', 
    metrics=[
        'AdrBalCnt',
        'AdrBalUSD1Cnt',
        'AdrBalUSD10Cnt',
        'AdrBalUSD100Cnt',
        'AdrBalUSD1KCnt',
        'AdrBalUSD10KCnt',
        'AdrBalUSD100KCnt',
        'AdrBalUSD1MCnt',
        'AdrBalUSD10MCnt'], 
    page_size=10000).to_dataframe()
df_doge_adr_bal['time'] = df_doge_adr_bal['time'].dt.tz_localize(None)
df_doge_adr_bal.dropna(inplace=True)
df_doge_adr_bal.loc[:,'AdrBalCnt':'AdrBalUSD1MCnt'] = df_doge_adr_bal.loc[:,'AdrBalCnt':'AdrBalUSD1MCnt'].astype(float)

df_doge_adr_bal.loc[:,'AdrBalUSD100Cnt':] = df_doge_adr_bal.loc[:,'AdrBalUSD100Cnt':].div(df_doge_adr_bal['AdrBalCnt'], axis=0).astype(float)
print(df_doge_adr_bal)

# Plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.055, right=0.98, top=0.985, bottom=0.04)


ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD1Cnt'],
    1,
    label='< $1'
)

ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD10Cnt'],
    df_doge_adr_bal['AdrBalUSD1Cnt'],
    label='>= $1'
)

ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD100Cnt'],
    df_doge_adr_bal['AdrBalUSD10Cnt'],
    label='>= $10'
)

ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD1KCnt'],
    df_doge_adr_bal['AdrBalUSD100Cnt'],
    label='>= $100'
)

ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD10KCnt'],
    df_doge_adr_bal['AdrBalUSD1KCnt'],
    label='>= $1K'
)

ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD100KCnt'],
    df_doge_adr_bal['AdrBalUSD10KCnt'],
    label='>= 10K'
)

ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD1MCnt'],
    df_doge_adr_bal['AdrBalUSD100KCnt'],
    label='>= $100K'
)

ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD10MCnt'],
    df_doge_adr_bal['AdrBalUSD1MCnt'],
    label='>= $1M'
)

ax.fill_between(
    df_doge_adr_bal['time'],
    df_doge_adr_bal['AdrBalUSD10MCnt'],
    0,
    label='>= $10M'
)

ax.xaxis.set_major_locator(mdates.YearLocator())

ax.set_yscale('log')
ax.yaxis.set_major_formatter(PercentileFormatter)

plt.ylim(1e-7, 1)
plt.xlim(df_doge_adr_bal['time'].iloc[0], df_doge_adr_bal['time'].iloc[-1])
plt.grid(axis='both', which='major', alpha=0.5)
plt.grid(axis='both', which='minor', alpha=0.25)

plt.legend(title='Percent of Bitcoin Addresses with', ncol=2)
plt.show()