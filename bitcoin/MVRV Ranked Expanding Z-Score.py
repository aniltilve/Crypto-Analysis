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
from scipy.stats import zscore

def expanding_zscore(series):
    """
    Computes expanding Z-score for a pandas Series.
    
    Z_t = (x_t - mean_{1..t}) / std_{1..t}
    Only computed when at least min_periods observations exist.
    """
    exp_mean = series.expanding().mean()
    exp_std  = series.expanding().std()

    z = (series - exp_mean) / exp_std
    return z

# Get data from Coinmetrics, calculate MVRV, and generate time ordinal

df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics='CapMVRVCur', page_size=10000).to_dataframe()
df_btc.dropna(inplace=True)

df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['Log10 MVRV'] = np.log10(df_btc['CapMVRVCur'])
df_btc['Expanding ZScore'] = expanding_zscore(df_btc['Log10 MVRV'])
df_btc['Ranked Expanding ZScore'] = df_btc['Expanding ZScore'].rank(pct=True)


#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.03, right=0.98, top=0.98, bottom=0.04)

#ax.plot(df_btc['time'], df_btc['Zscore'], color='black', zorder=3, linewidth=1, label='BTC - MVRV')
ax.plot(df_btc['time'], df_btc['Ranked Expanding ZScore'], color='red', zorder=3, linewidth=1, label='BTC - MVRV')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
#ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
#ax.yaxis.set_minor_formatter(ticker.StrMethodFormatter('{x:g}'))


ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y:,.3f}')

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
#plt.ylim(-3.5, 4)
plt.grid(axis='both', which='major', alpha=0.5, zorder=1)
plt.grid(axis='both', which='minor', alpha=0.25, zorder=1)
plt.legend(title='Legend')
plt.show()