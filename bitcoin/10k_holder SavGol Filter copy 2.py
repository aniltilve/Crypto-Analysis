import pandas as pd
from matplotlib.widgets import Slider
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
from scipy.signal import savgol_filter

def GetStdLineLabel(z_score):
    dec_places = 3 if z_score > 3 else 2

    if z_score > 0:
        return f'μ + {z_score}σ ({100 - stats.norm.cdf(z_score) * 100:.{dec_places}f}% chance of going higher)'
    elif z_score < 0:
        return f'μ - {abs(z_score)}σ ({stats.norm.cdf(z_score) * 100:.{dec_places}f}% chance of going lower)'
    else:
        return 'Mean Trendline (μ)'

# Data ETL

client = CoinMetricsClient()

df_btc = client.get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['Log10 Price'] = np.log10(df_btc['PriceUSD'])
sg_filter = savgol_filter(df_btc['Log10 Price'], 80, 2)

resid = df_btc['Log10 Price'] - sg_filter
std = np.std(resid)

# Plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.025, right=0.98, top=0.985, bottom=0.1)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')


ax.semilogy(df_btc['time'], df_btc['PriceUSD'])
ax.semilogy(df_btc['time'], 10 ** sg_filter)
ax.semilogy(df_btc['time'], 10 ** (sg_filter - 3 * std))
ax.semilogy(df_btc['time'], 10 ** (sg_filter + 3 * std))


#ax.semilogy(df_btc['time'], resid)

ax.xaxis.set_major_locator(mdates.YearLocator())
#ax.xaxis.set_minor_locator(mdates.DayLocator(7))
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%m'))

#ax.yaxis.set_major_locator(ticker.LogLocator())
#ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
#ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))


#ax.set_ylim(0, 150)
#ax.set_xlim(df_btc['time'].iloc[-1] - pd.tseries.offsets.DateOffset(months=2), df_btc['time'].iloc[-1])

#plt.legend(title='Legend')
plt.show()