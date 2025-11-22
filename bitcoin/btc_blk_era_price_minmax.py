import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from coinmetrics.api_client import CoinMetricsClient

def CurrencyFormatter(x, pos):
    if x >= 10 ** 6:
        return '${:,.0f}M'.format(x / (10 ** 6))
    elif  x >= 10 ** 3:
        return '${:,.0f}k'.format(x / (10 ** 3))
    elif x >= 1:
        return '${:,.0f}'.format(x)
    elif x >= 0.1:
        return '${:,.1f}'.format(x)
    else:
        return '${:,.2f}'.format(x)

def MinMax(x):
    return (x - x.min()) / (x.max() - x.min())

# Data ETL
df_btc_data = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD', 'BlkCnt'], page_size=10000).to_dataframe()
df_btc_data = df_btc_data.drop(df_btc_data.index[-1])

df_btc_data['time'] = pd.to_datetime(df_btc_data['time']).dt.tz_localize(None)
df_btc_data['PriceUSD'] = df_btc_data['PriceUSD'].astype(float)
df_btc_data['BlkHgt'] = df_btc_data['BlkCnt'].astype(int).cumsum()
df_btc_data = df_btc_data[df_btc_data['time'] >= '2010-07-18']

gen = df_btc_data[(df_btc_data['BlkHgt'] < 210000)]
h1 = df_btc_data[(df_btc_data['BlkHgt'] >= 210000) & (df_btc_data['BlkHgt'] < 420000)]
h2 = df_btc_data[(df_btc_data['BlkHgt'] >= 420000) & (df_btc_data['BlkHgt'] < 630000)]
h3 = df_btc_data[(df_btc_data['BlkHgt'] >= 630000) & (df_btc_data['BlkHgt'] < 840000)]
h4 = df_btc_data[(df_btc_data['BlkHgt'] >= 840000) & (df_btc_data['BlkHgt'] < 1050000)]

h1['MinMax_PriceUSD'] = (h1['PriceUSD'] - h1['PriceUSD'].min()) / (h1['PriceUSD'].max() - h1['PriceUSD'].min())
h2['MinMax_PriceUSD'] = (h2['PriceUSD'] - h2['PriceUSD'].min()) / (h2['PriceUSD'].max() - h2['PriceUSD'].min())
h3['MinMax_PriceUSD'] = (h3['PriceUSD'] - h3['PriceUSD'].min()) / (h3['PriceUSD'].max() - h3['PriceUSD'].min())
h4['MinMax_PriceUSD'] = (h4['PriceUSD'] - h4['PriceUSD'].min()) / (h4['PriceUSD'].max() - h4['PriceUSD'].min())

print(h1)

# Plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.045, right=0.98, top=0.985, bottom=0.065)
ax.grid(axis='both', which='major', zorder=1, alpha=0.5)
ax.grid(axis='both', which='minor', zorder=1, alpha=0.25)

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)

#ax.semilogy(gen['BlkHgt'], gen['PriceUSD'], label='Genesis')
ax.plot(h1['BlkHgt'] - 210000, h1['MinMax_PriceUSD'], label='Halving 1', zorder=2)
ax.plot(h2['BlkHgt'] - 420000, h2['MinMax_PriceUSD'], label='Halving 2', zorder=2)
ax.plot(h3['BlkHgt'] - 630000, h3['MinMax_PriceUSD'], label='Halving 3', zorder=2)
ax.plot(h4['BlkHgt'] - 840000, h4['MinMax_PriceUSD'], label='Halving 4', zorder=2)

ax.xaxis.set_major_locator(ticker.MultipleLocator(52500))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5250))

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

#ax.yaxis.set_major_formatter(CurrencyFormatter)

plt.xlabel('Block Height relative to Block Reward Era')
plt.ylabel('Min-Max Scaled Closing Price')
plt.xlim(0, 210000)
plt.ylim(0, 1)
plt.legend(title='Block Reward Era')
plt.show()