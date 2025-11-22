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

# Plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.025, right=0.98, top=0.985, bottom=0.1)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')



ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator())
#ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
#ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

ax.semilogy(df_btc['time'], df_btc['PriceUSD'])

#ax.set_ylim(0, 150)
ax.set_xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])


ax_window = plt.axes([0.13, 0.01, 0.8, 0.03])
slider_window = Slider(ax_window, 'window length', 1, 500, valinit=80, valstep=1)

sg_filter, = ax.semilogy(df_btc['time'], savgol_filter(df_btc['PriceUSD'], 80, 2))

def update(val):
    window = slider_window.val
    sg_filter.set_ydata(savgol_filter(df_btc['PriceUSD'], window, 2))
    fig.canvas.draw_idle()

slider_window.on_changed(update)

#plt.legend(title='Legend')
plt.show()