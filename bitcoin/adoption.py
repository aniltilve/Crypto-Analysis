import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime
import AppKit

btcData = pandas.read_csv('/Users/user/Desktop/Python/Bitcoin/BTC_Adoption.csv', delimiter='\t')
btcData["Date"] = pandas.to_datetime(btcData["Date"])
btc_addr = numpy.log(btcData["AddressCount"])
btcData.index += 1

def modelling_func(x, a, b, c, d):
    return a * numpy.log(x * b + c) + d

extendedDates = pandas.date_range(btcData["Date"].iloc[0], "2040-01-01")

popt, pcov = curve_fit(modelling_func, btcData.index.to_list(), btc_addr)
extendedFittedYdata = modelling_func(numpy.array([date_index + 1 for date_index in range(len(extendedDates))]), popt[0], popt[1], popt[2], popt[3])

#plotting
figure, axes = pyplot.subplots()
axes.grid(axis='both', which='major', color="silver")
axes.grid(axis='both', which='minor', color="gainsboro")

mng = pyplot.get_current_fig_manager()
mng.full_screen_toggle()

axes.semilogy(btcData["Date"], btcData["AddressCount"])
axes.semilogy(extendedDates, numpy.exp(extendedFittedYdata), color="lime")

axes.xaxis.set_major_locator(dates.YearLocator(2,month=1,day=1))
axes.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

axes.yaxis.set_major_locator(ticker.LogLocator(numticks=19))
axes.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))


pyplot.title("BTC adoption")
pyplot.ylabel("AddressCount")
pyplot.xlim(btcData["Date"].iloc[0], datetime.datetime(2040,1,1))
pyplot.ylim(10,100000000)
pyplot.show()