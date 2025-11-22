import sys
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import datetime
from coinmetrics.api_client import CoinMetricsClient

df_doge = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_doge['time'] = pd.to_datetime(df_doge['time']).dt.tz_localize(None)
df_doge['Annual Returns Rank'] = df_doge['PriceUSD'].pct_change(periods=365).rank(pct=True)
df_doge.dropna(inplace=True)

plt.plot(df_doge['time'], df_doge['Annual Returns Rank'])

plt.xlim(df_doge['time'].iloc[0], df_doge['time'].iloc[-1])
plt.ylim(0, 1)
plt.show()