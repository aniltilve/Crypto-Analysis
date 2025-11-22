import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient


btc_price_data = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
btc_price_data['time'] = pd.to_datetime(btc_price_data['time'])
btc_price_data['PctChange'] = btc_price_data['PriceUSD'].pct_change()

#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.1, right=0.98, top=0.955, bottom=0.07)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')
plt.tick_params(axis='y',which='minor')

ax.plot(btc_price_data['time'], btc_price_data['PctChange'], color='steelblue')

ax.xaxis.set_major_locator(dates.YearLocator(1))
ax.xaxis.set_minor_locator(dates.MonthLocator(7))
ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))

plt.title('BTC price - upper bound, fair value, and lower bound curves')
plt.xlabel('time')
plt.ylabel('Price in USD')
plt.xlim(btc_price_data['time'].iloc[0], btc_price_data['time'].iloc[-1])
plt.show()