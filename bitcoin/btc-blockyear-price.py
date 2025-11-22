import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime
import os

def modelling_func(x, a, b, c, d):
    return a * numpy.log(x * b + c) + d


btc_price_data = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_BlockHeight_Price.csv', delimiter='\t')
btc_price_data_early = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_BlockHeight_Price.csv')


btc_price_data['BlockYear'] = btc_price_data['BlockHeight'] / 52500

print(btc_price_data)


#plotting
fig, ax = pyplot.subplots()
fig.subplots_adjust(left=0.1, right=0.98, top=0.955, bottom=0.07)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

for blk_hgt_mult in range(1, 44):
    pyplot.axvline(52500 * blk_hgt_mult, color='black')

ax.loglog(btc_price_data['BlockYear'], btc_price_data['Price'], color='steelblue', basex=2, basey=2)

#ax.xaxis.set_major_locator(ticker.LogLocator(base=2, numticks=500))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(4))
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:n}'))
ax.xaxis.set_minor_formatter(ticker.StrMethodFormatter(''))


ax.yaxis.set_major_locator(ticker.LogLocator(base=2, numticks=500))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))

pyplot.title('BTC price - upper bound, fair value, and lower bound curves')
pyplot.xlabel('Block Year')
pyplot.ylabel('Price in USD')
pyplot.xlim(0, 64)
pyplot.ylim(2**-6, 2**22)
pyplot.show()