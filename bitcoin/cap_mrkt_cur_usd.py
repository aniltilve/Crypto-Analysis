import sys
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient



def fmt_func(x, pos):
    if x >= 10 ** 12:
        return '${:,.0f}T'.format(x / (10 ** 12))
    elif x >= 10 ** 9:
        return '${:,.0f}B'.format(x / (10 ** 9))
    elif x >= 10 ** 6:
        return '${:,.0f}M'.format(x / (10 ** 6))
    elif  x >= 10 ** 3:
        return '${:,.0f}k'.format(x / (10 ** 3))
    elif x >= 1:
        return '${:,.0f}'.format(x)
    elif x >= 0.1:
        return '${:,.1f}'.format(x)
    else:
        return '${:,.2f}'.format(x)

def power(x, a, b):
    return a * np.power(x, b)

df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['CapMrktCurUSD'], page_size=10000).to_dataframe()
df_btc['Date'] = df_btc['time'].dt.tz_localize(None)
df_btc['CapMrktCurUSD'] = df_btc['CapMrktCurUSD'].astype(float)

popt, _ = curve_fit(power, df_btc.index, df_btc['CapMrktCurUSD'])
fit = power(df_btc.index, popt[0], popt[1])

plt.semilogy(df_btc['Date'], df_btc['CapMrktCurUSD'])
plt.semilogy(df_btc['Date'], fit)

plt.show()