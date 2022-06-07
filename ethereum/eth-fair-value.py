import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker

ub_xData = [
    6,
    2104,
    2285
]

ub_yData = numpy.log([
    1.8848,
    4155.77199766219,
    4811.1564628872
])

lb_xData = [
    508,
    1683
]

lb_yData = numpy.log([
    7.15374168614845,
    110.34905873758
])

ethData = pandas.read_csv(r'C:\Users\user\Desktop\Python\ethereum\ETH_Price.csv')

ethData["Date"] = pandas.to_datetime(ethData["Date"])

def modellingFunc(x, a, b):
    return a * numpy.log(x) + b

extendedDates = pandas.date_range(ethData["Date"].iloc[0], "2026-01-01")

fv_xData = [x+1 for x in range(len(ethData))]
fv_yData = numpy.log(ethData["Value"])

popt, pcov = curve_fit(modellingFunc, fv_xData, fv_yData)
fv_extendedFittedYdata = modellingFunc(numpy.array([x+1 for x in range(len(extendedDates))]), popt[0],popt[1])

popt, pcov = curve_fit(modellingFunc, ub_xData, ub_yData)
ub_extendedFittedYdata = modellingFunc(numpy.array([x+1 for x in range(len(extendedDates))]), popt[0],popt[1])

popt, pcov = curve_fit(modellingFunc, lb_xData, lb_yData)
lb_extendedFittedYdata = modellingFunc(numpy.array([x+1 for x in range(len(extendedDates))]), popt[0],popt[1])

#plotting
figure, axes = pyplot.subplots()
axes.grid(axis='both', which='major', color="lightgray")
axes.semilogy(ethData["Date"], ethData["Value"])
pyplot.yscale('log', subsy=[1])

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

currencyFormatter = ticker.StrMethodFormatter('${x:,.2f}')

axes.yaxis.set_major_formatter(currencyFormatter)
axes.yaxis.set_minor_formatter(currencyFormatter)
pyplot.plot(extendedDates, numpy.exp(fv_extendedFittedYdata), color="orange")
pyplot.plot(extendedDates, numpy.exp(ub_extendedFittedYdata), color="lime")
pyplot.plot(extendedDates, numpy.exp(lb_extendedFittedYdata), color="red")

pyplot.title("ETH price in USD - fair value, absolute upper bound, and absolute lower bound")
pyplot.ylabel("Price in USD")
pyplot.ylim(0.1,10000)
pyplot.xlim(ethData["Date"].iloc[0],extendedDates[-1])
pyplot.show()