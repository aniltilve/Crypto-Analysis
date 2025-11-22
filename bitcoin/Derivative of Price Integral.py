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
df_btc['DaysFromGen'] = df_btc.index + (df_btc['time'].iloc[0] - pd.to_datetime('2009-01-03')).days
df_btc['Log_DaysFromGen'] = np.log10(df_btc['DaysFromGen'])
df_btc['Log_Price'] = np.log10(df_btc['PriceUSD'])
df_btc['Price_Integral'] = df_btc['PriceUSD'].cumsum()
df_btc['Price_Integral_Diff'] = df_btc['Price_Integral'].pct_change()

plt.plot(df_btc['time'], df_btc['Price_Integral_Diff'])
plt.show()