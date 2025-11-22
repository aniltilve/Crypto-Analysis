import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime as dt

def func(x, a, b, c, d):
    return a * np.log(x * b + c) + d


btc_price_data = pd.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv', delimiter='\t')
btc_price_data['Date'] = pd.to_datetime(btc_price_data['Date'])
btc_price_data.index += 1


popt, pcov = curve_fit(func, btc_price_data.index.to_list(), np.log(btc_price_data['Price']))
fitted_prices = func(np.array(btc_price_data.index), popt[0],popt[1], popt[2], popt[3])

#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.1, right=0.98, top=0.955, bottom=0.07)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')
plt.tick_params(axis='y',which='minor')

fig_manager = plt.get_current_fig_manager()
fig_manager.window.showMaximized()

plt.axvline(dt.datetime(2012,11,28), color='black')
plt.axvline(dt.datetime(2016,7,9), color='black')
plt.axvline(dt.datetime(2020,5,11), color='black')
plt.axvline(dt.datetime(2024,4,18), color='black')

#ax.semilogy(btc_price_data['Date'], btc_price_data['Price'], color='steelblue')
ax.plot(btc_price_data['Date'], btc_price_data['Price'] / np.exp(fitted_prices), color='orange')

ax.xaxis.set_major_locator(dates.YearLocator(1))
ax.xaxis.set_minor_locator(dates.MonthLocator(7))
ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.1f}'))

plt.title('BTC price - upper bound, fair value, and lower bound curves')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.xlim(dt.datetime(2010,7,18), dt.datetime(2026,1,1))
plt.ylim(0,18)
plt.show()