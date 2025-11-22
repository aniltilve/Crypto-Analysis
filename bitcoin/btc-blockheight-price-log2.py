import sys
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
btc_price_data['Date'] = pandas.to_datetime(btc_price_data['Date'])

#btc_price_data_early = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price_Early.csv')
#btc_price_data_early['Date'] = pandas.to_datetime(btc_price_data_early['Date'])


#print(btc_price_data.dtypes)
#print(btc_price_data_early.dtypes)


#btc_price_data = btc_price_data.merge(btc_price_data_early, how='left', left_on='Date', right_on='Date')

#print(btc_price_data)

#plotting
fig, ax = pyplot.subplots()
fig.subplots_adjust(left=0.1, right=0.98, top=0.955, bottom=0.07)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')
pyplot.tick_params(axis='y',which='minor')

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

for blk_hgt_mult in range(1, 11):
    pyplot.axvline(210000 * blk_hgt_mult, color='black')

ax.loglog(btc_price_data['BlockHeight'], btc_price_data['Price'], color='steelblue',  basex=2, basey=2)
#ax.set_xscale('log', bas)

ax.xaxis.set_major_locator(ticker.LogLocator(base=2, numticks=500))
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

ax.yaxis.set_major_locator(ticker.LogLocator(base=2, numticks=500))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))

pyplot.title('BTC price - upper bound, fair value, and lower bound curves')
pyplot.xlabel('Block Height')
pyplot.ylabel('Price in USD')
pyplot.xlim(2**15,2**21)
pyplot.ylim(2**-6, 2**22)
#pyplot.xlim(datetime.datetime(2010,7,18), datetime.datetime(2026,1,1))
pyplot.show()