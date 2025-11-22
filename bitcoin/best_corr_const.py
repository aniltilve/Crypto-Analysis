import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
import scipy.stats as stats
import scipy.optimize as optimize

# Helper functions



# Data ETL

df_btc_price_early = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTC_Price_Pre_2010_07_18.csv')
df_btc_price_early['time'] = pd.to_datetime(df_btc_price_early['time'])
df_btc_price_early = (df_btc_price_early.set_index('time')
    .reindex(pd.date_range(df_btc_price_early['time'].iloc[0], df_btc_price_early['time'].iloc[-1], freq='D'))
    .rename_axis(['time'])
    .reset_index())
df_btc_price_early['PriceUSD'] = df_btc_price_early['PriceUSD'].interpolate(method='akima')

client = CoinMetricsClient()

df_btc_price = client.get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc_price = df_btc_price.drop(columns=['asset'])
df_btc_price = pd.concat([df_btc_price_early, df_btc_price])
df_btc_price['PriceUSD'] = df_btc_price['PriceUSD'].astype(float)
eth_price_log = np.log(df_btc_price['PriceUSD'])

r_vals = pd.DataFrame(columns=['Offset', 'R^2'])

for offset in np.arange(1, 400, 0.01):
    test_index_log = np.log(df_btc_price.index + offset)
    a, b, r, p, stderr = stats.linregress(test_index_log, eth_price_log)
    r_vals = pd.concat([r_vals, pd.DataFrame(data={'Offset': [offset], 'R^2': [r ** 2]})], ignore_index=True)


print(r_vals.loc[r_vals['R^2'].idxmax(), 'Offset']) # current best is 124

