import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime

ub_offset = 70
lb_offset = 350

ub_xData = [
    # Jun 2011
    326,
    327,
    # Nov-Dec 2013
    1231,
    1232,
    1236,
    # Dec 2017
    2709,
    # 2021
    3923,
    4132
]

ub_xData = [x+ub_offset for x in ub_xData]

ub_yData = numpy.log([
    # Jun 2011
    29.0299213267095,
    28.79054401811810,
    # Nov-Dec 2013
    1128.7254880187,
    1119.29671478667,
    1134.93223088837,
    # Dec 2017
    19640.5138834015,
    # 2021
    63445.638314436,
    67541.7555081824
])


lb_xData = [
    80,
    #267,

    #2012
    489,
    584,

    #Jul 2015-Mar 2017
    #1642,
    1864,
    2208,
    2370,
    2442,

    #3073,
    3526,
    3530
]

lb_yData = numpy.log([
    0.0614,
    #0.73315682057277,

    #2012
    2.10506600321449,
    4.31511560198714,

    #Jul 2015-Mar 2017
    #175.637640561075,
    211.955917592051,
    526.981148334307,
    788.314655990649,
    935.063496201052,

    #3185.07404383402,
    4959.31341437756,
    5012.92738778492
])

lb_xData = [x+lb_offset for x in lb_xData]

btcData = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv')

btcData["Date"] = pandas.to_datetime(btcData["Date"])

def modellingFunc(x, a, b):
    return a * numpy.log(x) + b

extendedDates = pandas.date_range(btcData["Date"].iloc[0], "2026-01-01")

popt, pcov = curve_fit(modellingFunc, ub_xData, ub_yData)
ub_extendedFittedYdata = modellingFunc(numpy.array([x+ub_offset for x in range(len(extendedDates))]), popt[0],popt[1])

popt, pcov = curve_fit(modellingFunc, lb_xData, lb_yData)
lb_extendedFittedYdata = modellingFunc(numpy.array([x+lb_offset for x in range(len(extendedDates))]), popt[0],popt[1])

#plotting
figure, axes = pyplot.subplots()
axes.grid(axis='both', which='major', color="darkgray")
axes.grid(axis='both', which='minor', color="lightgray")
axes.semilogy(btcData["Date"], btcData["Value"])
pyplot.yscale('log', subsy=[1])

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

currencyFormatter = ticker.StrMethodFormatter('${x:,.2f}')

axes.xaxis.set_major_locator(dates.YearLocator(1,month=1,day=1))
axes.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
axes.xaxis.set_minor_locator(dates.MonthLocator(7))
axes.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
axes.yaxis.set_major_formatter(currencyFormatter)
axes.yaxis.set_minor_formatter(currencyFormatter)

pyplot.plot(extendedDates, numpy.exp(ub_extendedFittedYdata), color="lime")
pyplot.plot(extendedDates, numpy.exp(lb_extendedFittedYdata), color="red")
pyplot.plot(extendedDates, numpy.exp((ub_extendedFittedYdata + lb_extendedFittedYdata)/2), color="orange")

pyplot.title("BTC price upper and lower bound curves")
pyplot.ylabel("Price in USD")
pyplot.ylim(0.01,1000000)
pyplot.xlim(datetime.datetime(2010, 1, 1), datetime.datetime(2026,1,1))
pyplot.show()