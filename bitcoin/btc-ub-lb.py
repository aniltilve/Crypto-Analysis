import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker

btcData = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv')

fv_offset = 1
ub_offset = 1.7
lb_offset = 1.3

btcData["Date"] = pandas.to_datetime(btcData["Date"])

def modellingFunc(x, a, b):
    return a * numpy.log(x) + b

extendedDates = pandas.date_range(btcData["Date"].iloc[0], "2026-01-01")

fv_xData = [x+fv_offset for x in range(len(btcData))]
fv_yData = numpy.log(btcData["Value"])

popt, pcov = curve_fit(modellingFunc, fv_xData, fv_yData)
fv_extendedFittedYdata = modellingFunc(numpy.array([x+fv_offset for x in range(len(extendedDates))]), popt[0],popt[1])

#plotting
figure, axes = pyplot.subplots()
axes.grid(axis='both', which='major', color="lightgray")
axes.semilogy(btcData["Date"], btcData["Value"])
pyplot.yscale('log', subsy=[1])

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

currencyFormatter = ticker.StrMethodFormatter('${x:,.2f}')

axes.yaxis.set_major_formatter(currencyFormatter)
axes.yaxis.set_minor_formatter(currencyFormatter)
#pyplot.plot(extendedDates, numpy.exp((fv_extendedFittedYdata * 2 - 4)*0.6), color="red")
#pyplot.plot(extendedDates, numpy.exp(fv_extendedFittedYdata * 1.2 - 0.9), color="orange")
#pyplot.plot(extendedDates, numpy.exp(fv_extendedFittedYdata + ub_offset), color="lime")

pyplot.plot(extendedDates, numpy.exp(fv_extendedFittedYdata))
pyplot.plot(extendedDates, numpy.exp(fv_extendedFittedYdata * 0.9) + 2, color="red")



pyplot.title("BTC price fair value")
pyplot.ylabel("Price in USD")
pyplot.ylim(0.01,1000000)
pyplot.xlim(btcData["Date"].iloc[0],extendedDates[-1])
pyplot.show()