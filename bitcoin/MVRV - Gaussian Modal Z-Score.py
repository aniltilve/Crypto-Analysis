import pandas as pd
from matplotlib.ticker import FuncFormatter
from joblib import Parallel, delayed
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

import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

def expanding_kde_mode(series):
    print('Getting Gaussian modes:')
    
    def kde_mode_at_index(i):
        if i == 0:
            return series.iloc[0]
                
        window = series.iloc[:i+1].values
        kde = gaussian_kde(window)

        window_max = window.max() if i < 800 else 2
        num_kde_points = len(series) * 16 if i < 800 else 1000

        x_grid = np.linspace(1.25, window_max, num_kde_points)
        density = kde(x_grid)
        mode = x_grid[np.argmax(density)]
        print(f'Iteraion {i}    Mode: {mode}')
        return mode
    
    # Parallel computation
    modes = Parallel(-1)(delayed(kde_mode_at_index)(i) for i in range(len(series)))
    
    return pd.Series(modes, index=series.index)

def expanding_modal_absolute_deviation(series, modes):

    print('Getting Modal Absolute Deviations:')

    abs_devs = pd.Series(abs(series.values - modes.values), index=series.index)

    def modal_absolute_deviation_at_index(i):
        if i == 0:
            return abs_devs.iloc[0]
        
        window = abs_devs.iloc[:i+1].values
        kde = gaussian_kde(window)

        window_max = window.max() if i < 500 else 2
        num_kde_points = len(series) * 16 if i < 500 else 1000

        x_grid = np.linspace(0, window_max, num_kde_points)
        density = kde(x_grid)
        modal_abs_dev = x_grid[np.argmax(density)]
        print(f'Iteraion {i}    MAD: {modal_abs_dev}')
        return modal_abs_dev
    
    modal_abs_devs = Parallel(-1)(delayed(modal_absolute_deviation_at_index)(i) for i in range(len(series)))

    return pd.Series(modal_abs_devs, index=series.index)


df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics='CapMVRVCur', page_size=10000).to_dataframe()
df_btc.dropna(inplace=True)
df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['Mode'] = expanding_kde_mode(df_btc['CapMVRVCur'])
df_btc['MAD'] = expanding_modal_absolute_deviation(df_btc['CapMVRVCur'], df_btc['Mode'])
df_btc['Modal Score'] = (df_btc['CapMVRVCur'] - df_btc['Mode']) / df_btc['MAD']
df_btc['Ranked Modal Score'] = df_btc['Modal Score'].rank(pct=True)


print(df_btc)
 
#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.03, right=0.98, top=0.98, bottom=0.04)

#ax.semilogy(df_btc['time'], df_btc['CapMVRVCur'], color='black', zorder=3, linewidth=1, label='BTC - MVRV')
ax.plot(df_btc['time'], df_btc['Ranked Modal Score'], color='blue', zorder=3, linewidth=1, label='Mode')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

#ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
#ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
#ax.yaxis.set_minor_formatter(ticker.StrMethodFormatter('{x:g}'))


ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y:,.3f}')

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
#plt.ylim(-3.5, 4)
plt.grid(axis='both', which='major', alpha=0.5, zorder=1)
plt.grid(axis='both', which='minor', alpha=0.25, zorder=1)
plt.legend(title='Legend')
plt.show()