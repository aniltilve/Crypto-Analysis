import sys
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime
from coinmetrics.api_client import CoinMetricsClient
import scipy.stats as stats

def logregress(x, a, b, c, d):
    return a * np.log(x * b + c) + d

# Data ETL
client = CoinMetricsClient()
df_btc_diff = client.get_asset_metrics(assets='BTC', metrics=['DiffLast'], page_size=10000).to_dataframe()
df_btc_diff = df_btc_diff[df_btc_diff['DiffLast'] > 1]
df_btc_diff['time'] = df_btc_diff['time'].dt.tz_localize(None)
df_btc_diff['timeOrdinal'] = df_btc_diff['time'].apply(lambda x: x.toordinal())
df_btc_diff['DiffLast'] = df_btc_diff['DiffLast'].astype(float)
df_btc_diff['DiffLast_Log'] = np.log(df_btc_diff['DiffLast'])
df_btc_diff['Index_Log'] = np.log1p(df_btc_diff.index)

a, b, r, _, _ = stats.linregress(df_btc_diff['Index_Log'], df_btc_diff['DiffLast_Log'])
fit = a * df_btc_diff['Index_Log'] + b
resid = df_btc_diff['DiffLast_Log'] - fit
std = np.std(resid)

forecast_dates = pd.date_range(df_btc_diff['time'].iloc[0], '2030-01-01')
dr_forecast_ord = forecast_dates.to_series().apply(lambda x: x.toordinal())
dr_forecast_ord = np.log(dr_forecast_ord - dr_forecast_ord[0] + 1)
forecast_diff = a * dr_forecast_ord + b


# Plotting
figure, ax = plt.subplots()
figure.subplots_adjust(left=0.06, right=0.98, top=0.95, bottom=0.075)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')

plt.tick_params(axis='y',which='minor')

ax.semilogy(df_btc_diff['time'], df_btc_diff['DiffLast'])
ax.semilogy(forecast_dates, np.exp(forecast_diff - 2 * std), color='green', linestyle='dashed')
ax.semilogy(forecast_dates, np.exp(forecast_diff), color='dimgray', linestyle='dashed')
ax.semilogy(forecast_dates, np.exp(forecast_diff + 2 * std), color='red', linestyle='dashed')

ax.xaxis.set_major_locator(dates.YearLocator(1))
ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(dates.MonthLocator(7))
ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator(subs='all',numticks=500))
ax.yaxis.set_major_formatter(ticker.EngFormatter())

plt.title('BTC Difficulty')
plt.xlabel('Year')
plt.ylabel('Difficulty')
plt.ylim(1, 1e16)
plt.xlim(df_btc_diff['time'].iloc[0], datetime.datetime(2030,1,1))
plt.show()