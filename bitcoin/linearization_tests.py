import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import requests
from coinmetrics.api_client import CoinMetricsClient
import sys

# Helper functions

def GetIdealOffsetLog(index, price_log):
    best_r2 = 0.0
    best_offset = 0

    for offset in np.arange(1, 200, 1):
        test_index_log = np.log(index + offset) 
        a, b, r, p, stderr = stats.linregress(test_index_log, price_log)

        if (r ** 2 > best_r2):
            best_r2 = r ** 2
            best_offset = offset
        else:
            continue
    print(f'Ideal offset log: {best_offset}')
    return best_offset

def GetIdealOffsetBoxcox(index, price_bc):
    best_r2 = 0.0
    best_offset = 0

    for offset in np.arange(1, 500, 1):
        test_index_bc, lmbda = stats.boxcox(index + offset) 
        a, b, r, p, stderr = stats.linregress(test_index_bc, price_bc)

        if (r ** 2 > best_r2):
            best_r2 = r ** 2
            best_offset = offset
        else:
            continue
    print(f'Ideal offset boxcox: {best_offset}')
    return best_offset


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
df_btc_price = df_btc_price.drop(columns=['asset'])
df_btc_price = pd.concat([df_btc_price_early, df_btc_price], ignore_index=True)

y_log = np.log(df_btc_price['PriceUSD'])
x_log = np.log(df_btc_price.index + GetIdealOffsetLog(df_btc_price.index, y_log))

y_bc, lmbda_y = stats.boxcox(df_btc_price['PriceUSD'])
x_bc, lmbda_x = stats.boxcox(df_btc_price.index + GetIdealOffsetBoxcox(df_btc_price.index, y_bc))

y_root4 = np.power(df_btc_price['PriceUSD'], 1/10)
x_root4 = df_btc_price.index


transformations = {
    "Log-Log": (x_log, y_log),
    "BoxCox-BoxCox": (x_bc, y_bc),
    "QdRt-QdRt": (x_root4, y_root4)
}

fig, axes = plt.subplots(1, 3, figsize=(12, 10))
axes = axes.ravel()

for i, (title, (X_trans, y_trans)) in enumerate(transformations.items()):
    #model = LinearRegression()
    #model.fit(X_trans, y_trans)
    #y_pred = model.predict(X_trans)
    #r2 = r2_score(y_trans, y_pred)
    a, b, r, p, stderr = stats.linregress(X_trans, y_trans)
    fit = a * X_trans + b
    
    axes[i].scatter(X_trans, y_trans, alpha=0.5, label=f'R^2 = {r ** 2:.4f}')
    axes[i].plot(X_trans, fit, color='red', linewidth=2)
    axes[i].set_title(title)
    axes[i].legend()

plt.tight_layout()
plt.show()

