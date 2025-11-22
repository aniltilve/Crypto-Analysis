import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
from scipy.optimize import curve_fit

def exp_decay(x, a, b, c):
    return a * np.exp(b * x) + c

# Data ETL
df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc.drop(columns=['asset'], inplace=True)

df_cum_max = df_btc[df_btc['PriceUSD'].isin(df_btc['PriceUSD'].cummax())]
df_cum_max['Days to ATH'] = df_cum_max['time'].diff().dt.days

cur_diff = (dt.datetime.today() - df_cum_max['time'].iloc[-1]).days


fig, ax = plt.subplots()
fig.subplots_adjust(left=0.05, right=0.98, top=0.98, bottom=0.06)

ax.plot(df_cum_max['time'], df_cum_max['Days to ATH'])
ax.plot([df_cum_max['time'].iloc[-1], dt.datetime.today()], [0, cur_diff])


ax.xaxis.set_major_locator(mdates.YearLocator())

#ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:.1f}'))
#ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
#ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

#plt.xlim(8e-2, 2e5)
#plt.ylim(0, 0.6)
plt.ylabel('% Increase from Previous ATH')
plt.grid(which='major', axis='both', alpha=0.4)
plt.grid(which='minor', axis='both', alpha=0.2)
plt.show()