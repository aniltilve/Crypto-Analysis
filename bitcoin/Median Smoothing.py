from coinmetrics.api_client import CoinMetricsClient
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.special import inv_boxcox
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter



# Data ETL
df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc['time'] = pd.to_datetime(df_btc['time']).dt.tz_localize(None)
df_btc = df_btc.drop(columns=['asset'])



df_btc['Median Smooth'] = df_btc['PriceUSD'].rolling(7).median()


# Plotting 
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.043, right=0.98, top=0.98, bottom=0.04)
ax.grid(axis='both', which='major', color='silver', zorder=1)
ax.grid(axis='both', which='minor', color='gainsboro', zorder=1)



ax.semilogy(df_btc['time'], df_btc['Median Smooth'], zorder=4, label='Median Smooth Price')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
plt.ylim(0)
plt.show()