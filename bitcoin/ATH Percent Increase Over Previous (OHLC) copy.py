import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient


# Data ETL
df_btc = pd.read_csv('./Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time'])

df_cum_max = df_btc[df_btc['high'].isin(df_btc['high'].cummax())]
df_cum_max['PctIncrease'] = df_cum_max['high'].pct_change()
df_cum_max.dropna(inplace=True)
print(df_cum_max)


fig, ax = plt.subplots()
fig.subplots_adjust(left=0.05, right=0.98, top=0.98, bottom=0.06)

ax.scatter(df_cum_max['time'], df_cum_max['PctIncrease'])

#ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:.1f}'))

ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

#plt.xlim(8e-2, 2e5)
plt.ylim(0, 0.6)
plt.ylabel('% Increase from Previous ATH')
plt.grid(which='major', axis='both', alpha=0.4)
plt.grid(which='minor', axis='both', alpha=0.2)
plt.show()