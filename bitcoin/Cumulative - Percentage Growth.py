import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from scipy.optimize import curve_fit

def exp_decay(x, a, b, c):
    return a * np.exp(x * b) + c


# Data ETL
df_btc = pd.read_csv('./Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time']).dt.tz_localize(None)
df_btc['high'] = df_btc['high'].astype(float)
df_btc['Date Index'] = (df_btc['time'] - df_btc['time'].min()).dt.days
df_btc['CumMax Percent Growth'] = df_btc['high'].cummax().pct_change()
df_btc['Log10 CumMax Percent Growth'] = np.log10(df_btc['CumMax Percent Growth'])
df_btc_no_zeroes = df_btc[df_btc['CumMax Percent Growth'] > 0]


#Curve Fitting
df_peaks = df_btc[df_btc['time'].isin([
    '2010-07-14',
    #'2011-01-31',
    '2013-11-18',
    '2017-12-07',
    '2021-01-02',
    '2024-11-11'
])]

popt, _ = curve_fit(exp_decay, df_peaks['Date Index'], df_peaks['Log10 CumMax Percent Growth'], p0=[1.75, -0.0005, -1])
print(popt)
fit = exp_decay(df_btc['Date Index'], *popt)
resid = df_peaks['Log10 CumMax Percent Growth'] - exp_decay(df_peaks['Date Index'], *popt)

lb = np.percentile(resid, 0)
ub = np.percentile(resid, 100)

# Plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)

ax.scatter(df_btc_no_zeroes['time'], df_btc_no_zeroes['CumMax Percent Growth'], zorder=4, label='BTC - Cumulative ATH - Percentage Growth')
ax.plot(df_btc['time'], 10 ** fit, zorder=4, color='tab:red')
ax.fill_between(df_btc['time'], 10 ** (fit + lb), 10 ** (fit + ub), color='tab:red', alpha=0.5)
#ax.set_yscale('log')

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))

ax.grid(which='major', alpha=0.5)
ax.grid(which='minor', alpha=0.25)
ax.legend()

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y*100:,.2f}%')

plt.ylim(0.01, 3)
plt.show()