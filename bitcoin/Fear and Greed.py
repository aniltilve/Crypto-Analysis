import requests
import pandas as pd
from matplotlib import (
    dates as mdates,
    pyplot as plt,
    ticker as ticker
)

def CurrencyFormatter(x, pos):
    if x >= 1e6:
        return '${:,.0f}M'.format(x / 1e6)
    elif x >= 1e3:
        return '${:,.0f}k'.format(x / 1e3)
    elif x >= 1:
        return '${:,.0f}'.format(x)
    else:
        return '{:g}¢'.format(x * 100)

# Fetch circulating-supply-profit-loss data
headers = {
    'X-API-Key': 'ci_live_48c91977f26e537622060c113061582325c46197b0b3ff354f7d80e48b5d2dee'
}

response = requests.get(
    'https://chartinspect.com/api/v1/onchain/circulating-supply-profit-loss',
    headers=headers
)
df_btc = pd.DataFrame(response.json()['data'])
df_btc['date'] = pd.to_datetime(df_btc['date'])
df_btc['supply_in_profit_percent_rank'] = df_btc['supply_in_profit_percent'].rank(pct=True)
print(df_btc)

plt.style.use('dark_background')

fig, ax = plt.subplots(3, 1)
fig.subplots_adjust(left=0.005, right=0.96, top=0.99, bottom=0.03, hspace=0.08)


ax[0].scatter(df_btc['date'], df_btc['btc_price'], c=df_btc['supply_in_profit_percent_rank'], s=5, cmap='RdYlGn', zorder=3)
ax[0].scatter(
    df_btc['date'].iloc[-1], 
    df_btc['btc_price'].iloc[-1],
    c=df_btc['supply_in_profit_percent_rank'].iloc[-1],
    norm=plt.Normalize(df_btc['supply_in_profit_percent_rank'].min(), df_btc['supply_in_profit_percent_rank'].max()),
    s=100,
    cmap='RdYlGn',
    zorder=4,
    linewidths=4,
    edgecolors=[
        (1, 1, 1, 0.6),
        (1, 1, 1, 0.9)
    ]
)
ax[0].set_yscale('log')
ax[0].yaxis.set_major_formatter(CurrencyFormatter)
ax[0].legend(title='Bitcoin Price')
ax[0].tick_params(axis='x', labelcolor='none')

ax[1].scatter(df_btc['date'], df_btc['supply_in_profit_percent'], c=df_btc['supply_in_profit_percent_rank'], s=5, cmap='RdYlGn', zorder=3)
ax[1].scatter(
    df_btc['date'].iloc[-1], 
    df_btc['supply_in_profit_percent'].iloc[-1],
    c=df_btc['supply_in_profit_percent_rank'].iloc[-1],
    norm=plt.Normalize(df_btc['supply_in_profit_percent_rank'].min(), df_btc['supply_in_profit_percent_rank'].max()),
    s=100,
    cmap='RdYlGn',
    zorder=4,
    linewidths=4,
    edgecolors=[
        (1, 1, 1, 0.6),
        (1, 1, 1, 0.9)
    ]
)
ax[1].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
ax[1].set_ylim(30, 100)
ax[1].legend(title='Percent of Supply in Profit')
ax[1].tick_params(axis='x', labelcolor='none')

ax[2].scatter(df_btc['date'], df_btc['supply_in_profit_percent_rank'], c=df_btc['supply_in_profit_percent_rank'], s=5, cmap='RdYlGn', zorder=3)
ax[2].scatter(
    df_btc['date'].iloc[-1], 
    df_btc['supply_in_profit_percent_rank'].iloc[-1],
    c=df_btc['supply_in_profit_percent_rank'].iloc[-1],
    norm=plt.Normalize(df_btc['supply_in_profit_percent_rank'].min(), df_btc['supply_in_profit_percent_rank'].max()),
    s=100,
    cmap='RdYlGn',
    zorder=4,
    linewidths=4,
    edgecolors=[
        (1, 1, 1, 0.6),
        (1, 1, 1, 0.9)
    ]
)
ax[2].yaxis.set_major_formatter(lambda x, pos: '{:g}'.format(x * 100))
ax[2].set_ylim(0, 1)
ax[2].legend(title='Fear and Greed Index')

dt_start_offset = pd.tseries.offsets.DateOffset(weeks=1)
dt_end_offset = pd.tseries.offsets.DateOffset(months=1)

for axis in ax:
    axis.xaxis.set_major_locator(mdates.YearLocator())
    axis.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    axis.grid(which='major', alpha=0.25)
    axis.grid(which='minor', alpha=0.125)
    axis.set_xlim(df_btc['date'].iloc[0] - dt_start_offset, df_btc['date'].iloc[-1] + dt_end_offset)
    axis.yaxis.tick_right()

#plt.plot(df['date'], df['supply_in_profit_percent_rank'])
plt.show()