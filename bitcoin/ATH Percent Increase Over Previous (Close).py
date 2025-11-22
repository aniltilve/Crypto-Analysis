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
df_cum_max['PctIncrease'] = df_cum_max['PriceUSD'].pct_change()
df_cum_max.dropna(inplace=True)
print(df_cum_max)

df_train = df_cum_max[df_cum_max['time'].isin([
    '2010-11-06',
    '2013-11-18',
    '2017-12-07',
    '2024-11-11'
])]

print(df_train.index - df_train.index[0])

popt, _ = curve_fit(exp_decay, df_train.index - df_train.index[0], df_train['PctIncrease'], p0=[df_train['PctIncrease'].iloc[0], -0.00001, 0.05])

print(popt)

dr_fit = pd.date_range(df_train['time'].iloc[0], '2030-01-01')
idx = np.arange(len(dr_fit))
fit = exp_decay(idx, *popt)

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.05, right=0.98, top=0.98, bottom=0.06)

ax.scatter(df_cum_max['time'], df_cum_max['PctIncrease'])
ax.plot(dr_fit, fit, color='tab:red')

ax.xaxis.set_major_locator(mdates.YearLocator())

#ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:.1f}'))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

#plt.xlim(8e-2, 2e5)
plt.ylim(0, 0.6)
plt.ylabel('% Increase from Previous ATH')
plt.grid(which='major', axis='both', alpha=0.4)
plt.grid(which='minor', axis='both', alpha=0.2)
plt.show()