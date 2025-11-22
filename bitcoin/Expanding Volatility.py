import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
from scipy.stats import linregress
from coinmetrics.api_client import CoinMetricsClient
import matplotlib.dates as mdates
from scipy.signal import sawtooth
from matplotlib.widgets import Slider
import datetime as dt


df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc['time'] = pd.to_datetime(df_btc['time']).dt.tz_localize(None)
df_btc['Log Returns'] = np.log10(df_btc['PriceUSD'] / df_btc['PriceUSD'].shift(1))
df_btc.dropna(inplace=True)
df_btc['Volatility'] = df_btc['Log Returns'].expanding().std()

print(df_btc)
plt.plot(df_btc['time'], df_btc['Volatility'])
plt.show()