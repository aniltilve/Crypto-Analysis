import sys
import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime
import get_btc_price_data
from coinmetrics.api_client import CoinMetricsClient

def modelling_func(x, a, b):
    return a * numpy.power(x,b)

def format_large_number(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])



btc_diff_data = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Difficulty.csv', delimiter='\t')
btc_diff_data['Date'] = pandas.to_datetime(btc_diff_data['Date'])

btc_price_data = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv', delimiter='\t')
btc_price_data['Date'] = pandas.to_datetime(btc_price_data['Date'])


#plotting
figure, axes = pyplot.subplots()
#figure.subplots_adjust(left=0.135, right=0.98, top=0.95, bottom=0.075)
axes.grid(axis='y', which='major', color='dodgerblue')
axes.grid(axis='x', which='major', color="silver")
axes.grid(axis='x', which='minor', color="gainsboro")


mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

axes.semilogy(btc_diff_data['Date'], btc_diff_data['Difficulty'], color='dodgerblue')


axes.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
axes.yaxis.limit_range_for_scale(1,100000000000000)

axes2 = axes.twinx()
axes2.grid(axis='x', which='major', color='gainsboro')
axes2.grid(axis='y', which='major', color='orange')

axes2.semilogy(btc_price_data['Date'], btc_price_data['Price'], color='orange')

axes2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.2f}'))


axes2.xaxis.set_major_locator(dates.YearLocator(1,month=1,day=1))
axes2.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
axes2.xaxis.set_minor_locator(dates.MonthLocator(7))
axes2.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

axes2.set_ylabel('Price')
axes2.set_ylim(0.01,100000)


pyplot.title('BTC Difficulty')
pyplot.xlabel('Year')
pyplot.xlim(datetime.datetime(2009,12,30), datetime.datetime(2026,1,1))
pyplot.show()