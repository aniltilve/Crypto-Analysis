from matplotlib import (
    dates as mdates,
    pyplot as plt,
    ticker
)
import pandas as pd
from coinmetrics.api_client import CoinMetricsClient
from scipy.signal import savgol_filter

df_btc = CoinMetricsClient().get_asset_metrics(
    assets='BTC',
    metrics=['SplyCur', 'SplyAct1d', 'SplyAct7d', 'SplyAct30d', 'SplyAct90d', 'SplyAct180d', 
             'SplyAct1yr', 'SplyAct2yr', 'SplyAct3yr', 'SplyAct4yr', 'SplyAct5yr', 'SplyAct10yr'],
    page_size=10000).to_dataframe()

df_btc['time'] = pd.to_datetime(df_btc['time'])

df_btc['Pct_SplyAct1d'] = df_btc['SplyAct1d'] / df_btc['SplyCur']
df_btc['Pct_SplyAct7d'] = df_btc['SplyAct7d'] / df_btc['SplyCur']
df_btc['Pct_SplyAct30d'] = df_btc['SplyAct30d'] / df_btc['SplyCur']
df_btc['Pct_SplyAct90d'] = df_btc['SplyAct90d'] / df_btc['SplyCur']
df_btc['Pct_SplyAct180d'] = df_btc['SplyAct180d'] / df_btc['SplyCur']
df_btc['Pct_SplyAct1Yr'] = df_btc['SplyAct1yr'] / df_btc['SplyCur']
df_btc['Pct_SplyAct2Yr'] = df_btc['SplyAct2yr'] / df_btc['SplyCur']
df_btc['Pct_SplyAct3Yr'] = df_btc['SplyAct3yr'] / df_btc['SplyCur']
df_btc['Pct_SplyAct4Yr'] = df_btc['SplyAct4yr'] / df_btc['SplyCur']
df_btc['Pct_SplyAct5Yr'] = df_btc['SplyAct5yr'] / df_btc['SplyCur']
df_btc['Pct_SplyAct10Yr'] = df_btc['SplyAct10yr'] / df_btc['SplyCur']

df_btc['Liquidity Index'] = (
    df_btc['Pct_SplyAct1d'] +
    df_btc['Pct_SplyAct7d'] * 1/7 +
    df_btc['Pct_SplyAct30d'] * 1/30 +
    df_btc['Pct_SplyAct90d'] * 1/90 +
    df_btc['Pct_SplyAct180d'] * 1/180 +
    df_btc['Pct_SplyAct1Yr'] * 1/365 +
    df_btc['Pct_SplyAct2Yr'] * 1/730 +
    df_btc['Pct_SplyAct3Yr'] * 1/1095 +
    df_btc['Pct_SplyAct4Yr'] * 1/1460 +
    df_btc['Pct_SplyAct5Yr'] * 1/1825 +
    df_btc['Pct_SplyAct10Yr'] * 1/3650
) / (1 + 1/7 + 1/30 + 1/90 + 1/180 + 1/365 + 1/730 + 1/1095 + 1/1460 + 1/1825 + 1/3650) * 100

sg_filtered = savgol_filter(df_btc['Liquidity Index'], 60, 2)

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.035, right=0.99, top=0.985, bottom=0.05)


print(df_btc)
ax.semilogy(df_btc['time'], df_btc['Liquidity Index'], label='BTC - Liquidity Index')
ax.semilogy(df_btc['time'], sg_filtered, label='BTC - Normalized Liquidity Index')

ax.xaxis.set_major_locator(mdates.YearLocator())


#ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
#ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
#plt.ylim(0, 1)
plt.grid(which='major', axis='both', alpha=0.3)
plt.legend(title='Percent of DOGE supply held for...')
plt.show()