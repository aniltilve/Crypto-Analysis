from matplotlib import ticker
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import requests
from coinmetrics.api_client import CoinMetricsClient
import sys
    

df_btc_price_early = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTC_Price_Pre_2010_07_18.csv')
df_btc_price_early['time'] = pd.to_datetime(df_btc_price_early['time'])
df_btc_price_early = (df_btc_price_early.set_index('time')
    .reindex(pd.date_range(df_btc_price_early['time'].iloc[0], df_btc_price_early['time'].iloc[-1], freq='D'))
    .rename_axis(['time'])
    .reset_index())
df_btc_price_early['PriceUSD'] = df_btc_price_early['PriceUSD'].interpolate(method='akima')

df_btc_price = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc_price['time'] = pd.to_datetime(df_btc_price['time']).dt.tz_localize(None)
df_btc_price['PriceUSD'] = df_btc_price['PriceUSD'].astype(float)
df_btc_price.drop(columns=['asset'], inplace=True)
df_btc_price = pd.concat([df_btc_price_early, df_btc_price], ignore_index=True)

offsets = np.arange(0, 500, 0.1)
df_r2_scores = pd.DataFrame(columns=['x_offset', 'y_offset', 'r2_score'])

for x_offset in np.arange(120, 130, 0.1):
    print(f'Current x-axis offset iteration: {x_offset}')
    x = np.log10(df_btc_price.index + x_offset)

    for y_offset in offsets:
        y = np.log10(df_btc_price['PriceUSD'] + x_offset)
        _, _, r, _, _ = stats.linregress(x, y)
        df_cur_r2 = pd.DataFrame(data={'x_offset': [x_offset], 'y_offset':[y_offset], 'r2_score': [r ** 2]})
        df_r2_scores = pd.concat([df_r2_scores, df_cur_r2])

    #print(df_r2_scores)
    #max_r2 = r2_scores[r2_scores['r2_score'] == r2_scores['r2_score'].max()]
    print(f'Max R2 so far: {df_r2_scores}')


""" 
fig, ax = plt.subplots()

ax.plot(offsets['x_offset'], offsets['r2'], label='Ln')



ax.scatter(max_r2['x_offset'], max_r2['r2'], color='red')

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.01))

plt.xlim(offsets['x_offset'].min(), offsets['x_offset'].max())
plt.ylim(0.95, 1)
plt.grid(True)
plt.show() """