import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime

period = 365

btcData = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv')
btcData["Date"] = pandas.to_datetime(btcData["Date"])

#print(btcData)

ret_dates = pandas.date_range(btcData["Date"].iloc[period], btcData["Date"].iloc[-1])
#ret_values = [x+1 for x in range(len(ret_dates))]

ret_values = []

for cur_loc in range(period,len(btcData.index)):
    ret_values.append((btcData["Value"].iloc[cur_loc] - btcData["Value"].iloc[cur_loc - period]) / btcData["Value"].iloc[cur_loc - period] * 100)

figure, axes = pyplot.subplots()
axes.grid(axis='both', which='major', color="silver")
axes.grid(axis='both', which='minor', color="gainsboro")
axes.plot(ret_dates, ret_values)
pyplot.tick_params(axis='y',which='minor')

pyplot.ylim(bottom=-100,top=10000)
pyplot.show()
