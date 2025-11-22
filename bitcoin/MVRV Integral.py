import pandas as pd
from matplotlib.ticker import FuncFormatter
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset


def exp_decay(x, a, b, c):
    return a * np.exp(x * b) + c

def inv_exp_decay(x, a, b, c):
    return a * (1- np.exp(x * b)) + c

# Get data from Coinmetrics, calculate MVRV, and generate time ordinal

df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['CapMrktCurUSD', 'CapRealUSD'], page_size=10000).to_dataframe()
df_btc.dropna(inplace=True)

df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['MVRV'] = df_btc['CapMrktCurUSD'] / df_btc['CapRealUSD']
df_btc['Log10 Index'] = np.log(df_btc.index)
df_btc['Log10 MVRV'] = np.log(df_btc['MVRV'])
df_btc['MVRV Integral'] = df_btc['MVRV'].cumsum()

# df_peaks = df_btc[df_btc['time'].isin([
#      '2010-11-06',
#      '2011-06-04',
#      '2013-11-18',
#      '2017-12-07',
#      '2021-02-21'
# ])]

# df_troughs = df_btc[df_btc['time'].isin([
#      '2011-10-19',
#      '2015-01-14',
#      '2018-12-15',
#      '2022-11-09'
# ])]


# popt_peak, _ = curve_fit(exp_decay, df_peaks.index, df_peaks['Log10 MVRV'], p0=[1, -0.001, 0.1])
# log10_peak_fit = exp_decay(df_btc.index, *popt_peak)
# peak_resid = df_peaks['Log10 MVRV'] - exp_decay(df_peaks.index, *popt_peak)

# popt_trough, _ = curve_fit(inv_exp_decay, df_troughs.index, df_troughs['Log10 MVRV'], p0=[-1, -0.001, 0.1])
# log10_trough_fit = inv_exp_decay(df_btc.index, *popt_trough)
# trough_resid = df_troughs['Log10 MVRV'] - inv_exp_decay(df_troughs.index, *popt_trough)

# dr_fcast = pd.date_range(df_btc['time'].iloc[0], '2027-01-01')
# idx_fcast = np.arange(df_btc.index[0], df_btc.index[0] + len(dr_fcast))
# log10_peak_fcast = exp_decay(idx_fcast, *popt_peak)
# log10_trough_fcast = inv_exp_decay(idx_fcast, *popt_trough)

# res_lb = np.exp(log10_peak_fcast + np.percentile(peak_resid, 0))
# res_ub = np.exp(log10_peak_fcast + np.percentile(peak_resid, 100))

# sup_lb = np.exp(log10_trough_fcast + np.percentile(trough_resid, 0))
# sup_ub = np.exp(log10_trough_fcast + np.percentile(trough_resid, 100))


fig2, ax2 = plt.subplots()
ax2.loglog(df_btc.index + 1, df_btc['MVRV Integral'])

#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.03, right=0.98, top=0.98, bottom=0.04)

ax.plot(df_btc['time'], df_btc['MVRV Integral'], color='black', zorder=3, label='BTC - MVRV')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

#ax.yaxis.set_major_locator(ticker.LogLocator())
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
ax.yaxis.set_minor_formatter(ticker.StrMethodFormatter('{x:g}'))


ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y:,.3f}')

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1] + pd.tseries.offsets.DateOffset(years=2))
#plt.ylim(0.3, 9)
plt.grid(axis='both', which='major', alpha=0.5, zorder=1)
plt.grid(axis='both', which='minor', alpha=0.25, zorder=1)
plt.legend(title='Legend')
plt.show()